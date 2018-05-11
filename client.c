#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
 
int main(int argc, char *argv[])
{

  if(argc < 3)
  {
    printf("Error: Hostname and port is not given\n");
    exit(1);
  }  

  int sockfd = 0,n = 0;
  char recvBuff[1024];
  char sendBuff[1024];
  char hostname[1024];
  struct hostent *h;

  struct sockaddr_in serv_addr;
 
  memset(recvBuff, '0' ,sizeof(recvBuff));

  if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0)
    {
      printf("\n Error : Could not create socket \n");
      return 1;
    }
  
//  looks for hostname information and assigns to host entity fields
  h = gethostbyname(argv[1]);
  if(h == NULL)
  {
    printf("Host not found\n");
    exit(1);
  }
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(atoi(argv[2]));
  bcopy((char *)h->h_addr,(char *)&serv_addr.sin_addr.s_addr,h->h_length);

//  gethostname(hostname, 1024);
//  struct hostent *h;
//  h = gethostbyname(hostname);

//  serv_addr.sin_family = AF_INET;
//  serv_addr.sin_port = htons(5000);
//  serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
 
  if((connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)))<0)
    {
      printf("\n Error : Connect Failed \n");
      return 1;
    }
//  fgets(sendBuff, sizeof(sendBuff), stdin);
  scanf("%s", sendBuff);
  write(sockfd, sendBuff, sizeof(sendBuff));
 
  while((n = read(sockfd, recvBuff, sizeof(recvBuff)-1)) > 0)
    {
      recvBuff[n] = 0;
    	      
      if(fputs(recvBuff, stdout) == EOF)
      {
      	printf("\n Error : Fputs error");
      }
      printf("\n");
    }
 
  if( n < 0)
    {
      printf("\n Read Error \n");
    }
 
 
  return 0;
}
