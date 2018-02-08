/**
* =====================================================================================
*@file udp.c
*
*@brief init and close function for socket(udp)
*
*@version 1.0
*
*@author Shu
*
*Email :  ierenshu@163.com
*
*@date Juni,2017

*Organization:  LIKE @ FAU
*   
*Copyright (c)  LIKE @ FAU
*
* =====================================================================================
*/
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<linux/in.h>
/** this function will initialize the socket which use udp protocal
*
*@param strptr parameter for ip address of the server,
*	which should be a 15 bit char array
*	or simplely like this: const char  strptr[] = "192.168.199.120"
*@param portnum port number of the server
*	eg: unsigned short portnum = 0x1031
*@return if the socket_init is ok, it will the return the handle of the socket
*	 if something wrong, it will return -1 and print a message
*
*/

int init_udp(const char* strptr, unsigned short portnum)
{
	int cfd;
		struct sockaddr_in s_add, c_add;
		cfd = socket(AF_INET, SOCK_DGRAM, 0); // SOCK_DGRAM means udp
		if (-1 == cfd)
		{
			printf("socket fail!\n");
			return -1;
		}
		bzero(&s_add, sizeof(struct sockaddr_in));
		s_add.sin_family = AF_INET;
		s_add.sin_addr.s_addr = inet_addr(strptr); //ip for server
		s_add.sin_port = htons(portnum);

		if(-1 == connect(cfd, (struct sockaddr *)(&s_add), sizeof(struct sockaddr)))
		{
			printf("connect fail!\n");
			return -1;
		}
		return cfd;
}

/** close socket after use
*
*@param cfd handle of socket
*
*/

int close_udp(int cfd)
{
	close(cfd);
	return 0;
}

