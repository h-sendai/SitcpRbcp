#include "rbcp.h"

/* MY_SOCKET */
static int udp_socket(void)
{
    int sockfd;
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        warn("socket(AF_INET, SOCK_DGRAM, 0)");
        return -1;
    }

    struct timeval tm_out = { 2, 0 }; /* timeout 2 seconds */
    if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &tm_out, sizeof(tm_out)) < 0) {
        warn("socket timeout setting for READ");
        return -1;
    }
    if (setsockopt(sockfd, SOL_SOCKET, SO_SNDTIMEO, &tm_out, sizeof(tm_out)) < 0) {
        warn("socket timeout setting for WRITE");
        return -1;
    }

    return sockfd;
}

/* connect() udp socket to use read(), readv(), write(), writev() */
static int connect_udp(int sockfd, char *host, int port)
{
    struct sockaddr_in servaddr;
    struct sockaddr_in *resaddr;
    struct addrinfo    hints;
    struct addrinfo    *res;
    int err;

    res = 0;
    memset((char *)&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_protocol = 0;
    if ( (err = getaddrinfo(host, 0, &hints, &res)) != 0) {
        return -1;
    }

    resaddr = (struct sockaddr_in *)res->ai_addr;
    memset((char *)&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port   = htons(port);
    servaddr.sin_addr   = resaddr->sin_addr;
    freeaddrinfo(res);

    if (connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("connect");
        return -1;
    }
    //return connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
    return 0;
}
/* MY_SOCKET */

int open_rbcp(char *remote_ip)
{
    int sockfd = udp_socket();
    if (sockfd < 0) {
        return -1;
    }
    if (connect_udp(sockfd, remote_ip, RBCP_PORT) < 0) {
        return -1;
    }

    return sockfd;
}

int get_reg_byte_stream(char *remote_ip, unsigned int address, unsigned char *buf, int len)
{
    int sockfd = open_rbcp(remote_ip);
    if (sockfd < 0) {
        return -1;
    }

    struct sitcp_rbcp_header rbcp_request_header, rbcp_reply_header;

    /* send read request */
    rbcp_request_header.ver_type = 0xff;
    rbcp_request_header.cmd_flag = 0xc0; /* READ */
    rbcp_request_header.id       = 1;
    rbcp_request_header.length   = len;
    rbcp_request_header.address  = ntohl(address);
    int n;
    n = write(sockfd, &rbcp_request_header, sizeof(rbcp_request_header));
    if (n < 0) {
        warn("send rbcp request packet to %s failed", remote_ip);
        return -1;
    }

    /* receive read request reply */
    struct iovec iov[2];
    iov[0].iov_base = &rbcp_reply_header;
    iov[0].iov_len  = sizeof(rbcp_reply_header);
    iov[1].iov_base = buf;
    iov[1].iov_len  = len;
    n = readv(sockfd, iov, sizeof(iov)/sizeof(iov[0]));
    if (n < 0) {
        warn("rbcp reply packet from %s read failed", remote_ip);
        return -1;
    }

    /* To Do */
    /* error check here */

    return 0;
}

int set_reg_byte_stream(char *remote_ip, unsigned int address, unsigned char *buf, int len)
{
    int sockfd = open_rbcp(remote_ip);
    if (sockfd < 0) {
        return -1;
    }

    struct sitcp_rbcp_header rbcp_request_header, rbcp_reply_header;

    /* send write request packet */
    rbcp_request_header.ver_type = 0xff;
    rbcp_request_header.cmd_flag = 0x80; /* WRITE */
    rbcp_request_header.id       = 1;
    rbcp_request_header.length   = len;
    rbcp_request_header.address  = ntohl(address);
    
    struct iovec iov[2];
    iov[0].iov_base = &rbcp_request_header;
    iov[0].iov_len  = sizeof(rbcp_request_header);
    iov[1].iov_base = buf;
    iov[1].iov_len  = len;
    int n;
    n = writev(sockfd, iov, sizeof(iov)/sizeof(iov[0]));
    if (n < 0) {
        warn("rbcp send write packet to %s failed", remote_ip);
    }

    /* receive write reply packet */
    unsigned char *reply_data_buf = malloc(len);
    if (reply_data_buf < 0) {
        warn("malloc for write reply data");
        return -1;
    }

    iov[0].iov_base = &rbcp_reply_header;
    iov[0].iov_len  = sizeof(rbcp_reply_header);
    iov[1].iov_base = reply_data_buf;
    iov[1].iov_len  = len;
    n = readv(sockfd, iov, sizeof(iov)/sizeof(iov[0]));

    /* To Do */
    /* error check here */
    free(reply_data_buf);

    return 0;
}

int set_reg_byte(char *remote_ip, unsigned int address, unsigned char data)
{
    int n;
    n = set_reg_byte_stream(remote_ip, address, &data, sizeof(data));
    if (n < 0) {
        warn("write to %s failed", remote_ip);
        return -1;
    }
    
    return 0;
}

int set_reg_short(char *remote_ip, unsigned int address, unsigned short data)
{
    int n;
    data = htons(data);
    n = set_reg_byte_stream(remote_ip, address, (unsigned char *)&data, sizeof(data));
    if (n < 0) {
        warn("write to %s failed", remote_ip);
        return -1;
    }
    
    return 0;
}

int set_reg_int(char *remote_ip, unsigned int address, unsigned int data)
{
    int n;
    data = htonl(data);
    n = set_reg_byte_stream(remote_ip, address, (unsigned char *)&data, sizeof(data));
    if (n < 0) {
        warn("write to %s failed", remote_ip);
        return -1;
    }
    
    return 0;
}

char get_reg_byte(char *remote_ip, unsigned int address)
{
    unsigned char buf[1];
    memset(buf, 0, sizeof(buf));
    if (get_reg_byte_stream(remote_ip, address, buf, sizeof(buf)) < 0) {
        return -1;
    }
    char rv = buf[0];
    return rv;
}

short get_reg_short(char *remote_ip, unsigned int address)
{
    unsigned char buf[2];
    memset(buf, 0, sizeof(buf));
    if (get_reg_byte_stream(remote_ip, address, buf, sizeof(buf)) < 0) {
        return -1;
    }
    short rv = ntohs(*(unsigned short *)buf);
    return rv;
}

int get_reg_int(char *remote_ip, unsigned int address)
{
    unsigned char buf[4];
    memset(buf, 0, sizeof(buf));
    if (get_reg_byte_stream(remote_ip, address, buf, sizeof(buf)) < 0) {
        return -1;
    }
    int rv = ntohl(*(unsigned int *)buf);
    return rv;
}

#ifdef DO_MAIN
int main(int argc, char *argv[])
{
    int reg;
    reg = get_reg_int("192.168.10.16", 0xffffff00);
    if (reg < 0) {
        fprintf(stderr, "error");
        exit(1);
    }
    printf("%x\n", reg);

    unsigned char data[4] = { 0x12, 0x34, 0x56, 0x78 };
    set_reg_byte_stream("192.168.10.16", 0xffffff3c /* user area */, data, sizeof(data));
    reg = get_reg_int("192.168.10.16", 0xffffff3c);
    if (reg < 0) {
        fprintf(stderr, "error");
    }
    printf("%x\n", reg);

    set_reg_byte("192.168.10.16", 0xffffff3c, 0xfe);
    set_reg_short("192.168.10.16", 0xffffff3c, 0xfeed);
    set_reg_int("192.168.10.16", 0xffffff3c, 0xfeedface);
    return 0;
}
#endif
