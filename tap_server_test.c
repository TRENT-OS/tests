/*
 *  SEOS Nw Stack, Socket Server test App
 *
 *  Copyright (C) 2019, Hensoldt Cyber GmbH

 *  This app tries to connect to a SEOS socket server, sends text msgs and then reads back
 *  the echoed data from Server
 */


#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>


#define SERVER_PORT 5555   /* Server is listening on this port */
#define SERVERADDR  "192.168.82.92"  /* IP addr of server to connect to */


int main(int argc, char const *argv[])
{
    struct sockaddr_in address;
    int sock = 0;
    struct sockaddr_in serv_addr;
    char msg[]  = "Hello from client...!";   /* Msg to send */
    char msg2[] = "Say 2nd Hi from client...!!"; /* 2nd msg to send */
    static char buffer2[1024] = {0};  /* to read data from server */

    printf("Starting tap_server_test client\n");

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error in test app \n");
        return -1;
    }

    memset(&serv_addr, '0', sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(SERVER_PORT);

    if(inet_pton(AF_INET, SERVERADDR, &serv_addr.sin_addr)<=0)
    {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }
    int retry =0;
    int error = 0;
    while (retry < 4)
    {

        int result = connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
        if(result < 0)
        {
            ++retry;
            error =1;
        }
        else
        {
            error = 0;
            break;     //  0 is success
        }
    }
    if(1 == error)
    {
        printf("\nFailed to connect to the server \n");
        return -1;
    }

    printf("\nConnected to Server ....Sending data now \n");

    error = send(sock , msg , sizeof(msg) , 0);
    if (error < 0)
    {
        printf("Error sending msg 1\n");
        return -1;
    }
    printf("\nWaiting for data from server \n");

    int toRead = sizeof(msg);
    int alreadyRead = 0;
    int r = 0;
    memset(buffer2, 0, sizeof(buffer2));

    while (toRead > 0)
    {
        r = recv(sock, buffer2 + alreadyRead, toRead, 0);
        if (r > 0)
        {
            alreadyRead += r;
            toRead -= r;
            printf("Got %d bytes, still %d bytes to read, buffer receiving echo -> %s\n", alreadyRead, toRead, buffer2);
        }
        else
        {
            printf("socket unexpextedly closed\n");
            return -1;
        }
    }

    error = send(sock , msg2, sizeof(msg2) , 0);
    if (error < 0)
    {
        printf("Error sending msg 1\n");
        return -1;
    }
    printf("\nWaiting for data from server \n");

    toRead = sizeof(msg2);
    alreadyRead = 0;
    memset(buffer2, 0, sizeof(buffer2));

    while (toRead > 0)
    {
        r = recv(sock , buffer2 + alreadyRead, toRead, 0);
        if (r > 0)
        {
            alreadyRead += r;
            toRead -= r;
            printf("Got %d bytes, still %d bytes to read, buffer receiving echo -> %s\n", alreadyRead, toRead, buffer2);
        }
        else
        {
            printf("socket unexpextedly closed\n");
            return -1;
        }
    }
    return 0;
}