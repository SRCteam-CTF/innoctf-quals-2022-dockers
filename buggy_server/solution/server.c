#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <signal.h>

#include "request_handle.c"

#define BACKLOG 32

void clientHandle(int fd);
//void responseGET(int fd, char *payload);

int serverLoop(int lport)
{
  int serverSock = socket(AF_INET, SOCK_STREAM, 0);

  struct sockaddr_in serverAddr;

  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(lport);
  serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);

  if (bind(serverSock, (struct sockaddr *) &serverAddr, sizeof(serverAddr)) < 0)
  {
    puts("bind error.");
    return 1;
  }

  if (listen(serverSock, BACKLOG) < 0)
  {
    puts("listen error.");
    return 1;
  }

  signal(SIGCHLD,SIG_IGN);

  struct sockaddr_in clientAddr;
  int clientAddrLen = sizeof(clientAddr);
  while (1)
  {
    int client = accept(serverSock, (struct sockaddr *) &clientAddr, (socklen_t*) &clientAddrLen);
    if (client < 0)
      puts("accept error.");
    else
    {
      if (fork() == 0)
      {
        close(serverSock);
        clientHandle(client);
        exit(0);
      }
      else
      {
        close(client);
      }
    }
  }
}

void clientHandle(int fd)
{
  while (true)
  {
    serve_files(fd);
   // close(fd);
  }
}

int main(int argc, char *argv[])
{
  if (argc != 2)
  {
    printf("Usage: %s lport\n", argv[0]);
    return 1;
  }
  serverLoop(atoi(argv[1]));
  return 0;
}

