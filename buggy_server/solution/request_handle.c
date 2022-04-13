#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>

char *method, *uri, *qs, *prot;

int open_file(char *filename, char *content);
void send_payload(int fd, char *content_type, char *payload);
void not_found(int fd);
void not_implemented(int fd);
void forbidden(int fd);

void serve_files(int fd)
{
  char *buf = malloc(4096);
  int n = recv(fd, buf, 4095, 0);

  buf[n] = 0;

  method = strtok(buf, " \t\r\n");
  uri = strtok(NULL, " \t");
  prot = strtok(NULL, "\t\r\n");

  if (!strcmp(method, "GET"))
  {
    if ((!strcmp(uri, "/index.html")) || (!strcmp(uri, "/")))
    {
      char *file_buf = malloc(16384);
      open_file("index.html", file_buf);
      send_payload(fd, "text/html", file_buf);
      free(file_buf);
    } else if (!strcmp(uri, "/style.css"))
    {
      char *file_buf = malloc(16384);
      open_file("style.css", file_buf);
      send_payload(fd, "text/css", file_buf);
      free(file_buf);
    }
    else if (!strcmp(uri, "/flag.txt"))
    {
      char *file_buf = malloc(4096);
      open_file("flag.txt", file_buf);
      forbidden(fd);
      free(file_buf);
    }
    else
      not_found(fd);
  }
  else if (!strcmp(method, "POST"))
  {
    if (!strcmp(uri, "/api/reflect"))
    {
      bool flag = false;
      int content_lenght = 0;
      char *k, *v;
      v = strtok(NULL, " ");
      k = strtok(NULL, "\n");
      while(k != NULL)
      {
	if (!strcmp(v, "Content-Length:") || !strcmp(v, "\nContent-Length:"))
          content_lenght = atoi(k);
        v = strtok(NULL, " ");
        k = strtok(NULL, "\n");

      }
      char *json_head = "{\"post data\":\"";
      char *payload = malloc(4096);
      strcpy(payload, json_head);
      for (int i = 2; i < content_lenght+2; i++)
      {
        if (v[i] == '\0')
          continue;
        payload[strlen(json_head) + i - 2] = v[i];
      }
      char *json_foot = "\"}";
      strcpy(payload+strlen(payload), json_foot);
      payload[content_lenght+strlen(json_head)+strlen(json_foot) + 2] = 0;
      send_payload(fd, "text/html", payload);
      free(payload);
    }
    else
      not_found(fd);
  }
  else
    not_implemented(fd);
}


int open_file(char *filename, char *content)
{
  FILE *fp;
  fp = fopen(filename, "r");
  if (fp)
  {
    fseek(fp, 0, SEEK_END);
    int filesize = ftell(fp);
    rewind(fp);
    int n = fread(content, sizeof(char), filesize, fp);
    content[n] = 0;
    fclose(fp);
  }
  else
  {
    return -1;
  }
  return 1;
}

void send_payload(int fd, char *content_type, char *payload)
{
  FILE *file_sock = fdopen(fd, "w");
  fprintf(file_sock,
          "HTTP/1.1 200 OK\n"
          "Server: Super Server 0.0.1\n"
          "Content-Type: %s\n"
          "Content-Length: %d\n\n"
          "%s", content_type, strlen(payload), payload);
  fflush(file_sock);
  fclose(file_sock);
}

void not_found(int fd)
{
  write(fd, "HTTP/1.1 404 Not Found\n"
        "Server: Super Server 0.0.1\n"
        "Content-Type: text/plain\n"
        "Content-Length: 0\n\n", 92);
}

void forbidden(int fd)
{
  write(fd, "HTTP/1.1 403 Forbidden\n"
        "Server: Super Server 0.0.1\n"
        "Content-Type: text/plain\n"
        "Content-Length: 0\n\n", 92);
}

void not_implemented(int fd)
{
  write(fd, "HTTP/1.1 501 Not Implemented\n"
        "Server: Super Server 0.0.1\n"
        "Content-Type: text/plain\n"
        "Content-Length: 0\n\n", 98);
}
