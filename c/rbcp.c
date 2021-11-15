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

    return sockfd;
}

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

int get_reg_byte_stream(char *remote_ip, unsigned int address, unsigned char *buf, int len)
{
    struct sitcp_rbcp_header rbcp_request_header, rbcp_reply_header;

    rbcp_request_header.ver_type = 0xff;
    rbcp_request_header.cmd_flag = 0xc0; /* READ */
    rbcp_request_header.id       = 1;
    rbcp_request_header.length   = len;
    rbcp_request_header.address  = ntohl(address);
    
    int sockfd = udp_socket();
    if (sockfd < 0) {
        return -1;
    }
    if (connect_udp(sockfd, remote_ip, RBCP_PORT) < 0) {
        return -1;
    }

    int n;
    n = write(sockfd, &rbcp_request_header, sizeof(rbcp_request_header));
    if (n < 0) {
        warn("send rbcp request packet to %s failed", remote_ip);
        return -1;
    }

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

unsigned char get_reg_byte(char *remote_ip, unsigned int address)
{
    unsigned char buf[1];
    memset(buf, 0, sizeof(buf));
    get_reg_byte_stream(remote_ip, address, buf, sizeof(buf));
    unsigned char rv = buf[0];
    return rv;
}

unsigned short get_reg_short(char *remote_ip, unsigned int address)
{
    unsigned char buf[2];
    memset(buf, 0, sizeof(buf));
    get_reg_byte_stream(remote_ip, address, buf, sizeof(buf));
    unsigned short rv = ntohs(*(unsigned short *)buf);
    return rv;
}

unsigned int get_reg_int(char *remote_ip, unsigned int address)
{
    unsigned char buf[4];
    memset(buf, 0, sizeof(buf));
    get_reg_byte_stream(remote_ip, address, buf, sizeof(buf));
    unsigned int rv = ntohl(*(unsigned int *)buf);
    return rv;
}

#ifdef DO_MAIN
int main(int argc, char *argv[])
{
    unsigned int reg = get_reg_int("192.168.10.16", 0xffffff00);
    printf("%x\n", reg);
    return 0;
}
#endif
