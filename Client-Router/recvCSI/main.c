/**
* =====================================================================================
*@file main.c
*
*@brief main function: log CSI to file or to server or to both.
*
*Here is an example for receiving CSI matrix,
*Basic CSi procesing fucntion is also implemented and called,
*Check csi_fun.c for detail of the processing function;
*
*A function which log the CSI to a server is added in. 
*
*@version:  2.0
*
*@author:  Yaxiong Xie
*
*modified by: Shu Ren
*
*Email :  <xieyaxiongfly@gmail.com>; ierenshu@163.com

*Organization:  WANDS group @ Nanyang Technological University;
*		LIKE @ FAU
*   
*Copyright (c)  WANDS group @ Nanyang Technological University;
*		LIKE @ FAU
*
* =====================================================================================
*/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <pthread.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "csi_fun.h"
#include "udp.c"

#define BUFSIZE 4096

int quit;
unsigned char buf_addr[BUFSIZE];
unsigned char data_buf[1500];

COMPLEX csi_matrix[3][3][114];
csi_struct*   csi_status;

void sig_handler(int signo)
{
    if (signo == SIGINT)
        quit = 1;
}

/**
*
*receive CSI and save to a file or send to a server or both
*
*Usage 1: recv_csi <output_file>
*
*Usage 2: recv_csi <Server-ip> <port>
*
*Usage 3: recv_csi <ip> <port> <output_file>
*
*/
int main(int argc, char* argv[])
{
    FILE*       fp;
    int         fd;
    int         i;
    int         total_msg_cnt,cnt;
    int         log_to_file, log_to_server;
    unsigned char endian_flag;
    u_int16_t   buf_len;

    int		cfd; //for udp
    const char  strptr[] = "192.168.199.120"; //server's ip
    unsigned short portnum = 0x1031; //server's port
    
    log_to_file = 1;
    log_to_server = 1;
    csi_status = (csi_struct*)malloc(sizeof(csi_struct));

    /* check usage */
    if (1 == argc){
        /* If you want to log the CSI for off-line processing,
         * you need to specify the name of the output file
         */
        log_to_file  = 0;
	log_to_server = 0;
        printf("/*********************************************/\n");
        printf("/*   Usage 1: recv_csi <output_file>         */\n");
	printf("/*   Usage 2: recv_csi <Server-ip> <port>    */\n");
	printf("/*Usage 3: recv_csi <ip> <port> <output_file>*/\n");
        printf("/*********************************************/\n");
    }
    if (2 == argc)
	{
		log_to_server = 0;
		fp = fopen(argv[1],"w");
		if (!fp)
			{
			    printf("Fail to open <output_file>, are you root?\n");
			    fclose(fp);
			    return 0;
			}
/*
		if(is_big_endian())
		    endian_flag = 0xff;
		else
		    endian_flag = 0x0;

//for our experiment. all equipment use little endian. 

		//fwrite(&endian_flag,1,1,fp); 


*/
    	}

    if (3 == argc)
	{
		log_to_file = 0;
		strcpy(strptr, argv[1]);
		//printf("ip:%s", strptr);
		portnum =(unsigned short) atoi(argv[2]);
		//printf("protnum: %d", portnum);
		cfd = init_udp(strptr, portnum);
		if (-1 == cfd)
			{
				printf("socket init error!\n");
				return 0;
			}
	}
    if (4 == argc)
	{
		strcpy(strptr, argv[1]);
		portnum =(unsigned short) atoi(argv[2]);
		cfd = init_udp(strptr, portnum);
		if (-1 == cfd)
			{
				printf("socket init error!\n");
				return 0;
			}

		fp = fopen(argv[3],"w");

        	if (!fp)
		{
            		printf("Fail to open <output_file>, are you root?\n");
            		fclose(fp);
            		return 0;
        	}
	}

    if (argc > 4){
        printf(" Too many input arguments !\n");
        return 0;
    }

    fd = open_csi_device();
    
    if (fd < 0){
        perror("Failed to open the device...");
        return errno;
    }
    
    printf("#Receiving data! Press Ctrl+C to quit!\n");

    quit = 0;
    total_msg_cnt = 0;
    
    while(1){
        if (1 == quit){
            return 0;
            fclose(fp);
            close_csi_device(fd);
            close(cfd);
        }

        /* keep listening to the kernel and waiting for the csi report */
        cnt = read_csi_buf(buf_addr,fd,BUFSIZE);

        if (cnt){
            total_msg_cnt += 1;

            /* fill the status struct with information about the rx packet */
            record_status(buf_addr, cnt, csi_status);

            /* 
             * fill the payload buffer with the payload
             * fill the CSI matrix with the extracted CSI value
             */
            record_csi_payload(buf_addr, csi_status, data_buf, csi_matrix); 
            
            /* Till now, we store the packet status in the struct csi_status 
             * store the packet payload in the data buffer
             * store the csi matrix in the csi buffer
             * with all those data, we can build our own processing function! 
             */
            //porcess_csi(data_buf, csi_status, csi_matrix);   
            
            printf("Recv %dth msg with rate: 0x%02x | payload len: %d\n",total_msg_cnt,csi_status->rate,csi_status->payload_len);
            
            /* log the received data for off-line processing */
            if (log_to_file){
                buf_len = csi_status->buf_len;
                fwrite(&buf_len,1,2,fp);
                fwrite(buf_addr,1,buf_len,fp);
            }
	    /*log the received data to server*/
	    if(log_to_server & (csi_status->csi_len>0) )
            {
		buf_len = csi_status->buf_len;
		//write(cfd,&buf_len,sizeof(buf_len));
            	write(cfd,buf_addr,csi_status->buf_len);
		printf("~~~~~~valid CSI! length is: %d, udp send scuess!~~~~~~\n", csi_status->csi_len);
            }
        }
    }
    close(cfd);
    fclose(fp);
    close_csi_device(fd);
    free(csi_status);
    return 0;
}
