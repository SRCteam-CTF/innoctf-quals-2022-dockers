#include <stdio.h>
#include <string.h>
#include <stdlib.h>


void encrypt(char *data, char *key)
{
	for(int i = 0; i < strlen(data); i++)
	{
		data[i] = data[i] ^ key[i];
	}
}

void vuln()
{
	char localbuf[1024];
	puts("[+] String Encrypter v0.228");
	for(int i = 0; i < 2; i++)
	{
		char *data = (char *)calloc(1024, sizeof(char));
		char *key = (char *)calloc(1024, sizeof(char));
		printf("Enter string to encrypt: ");
		fgets(localbuf, 1024, stdin);
		for(int j = 0; j < 1024; j++)
			data[j] = localbuf[j];
		printf("Enter encryption key: ");
		fgets(key, 1024, stdin);
		key[strlen(key)-1] = '\0';
		encrypt(data, key);
		puts("[+] Encrypted data:");
		printf(data);
		putchar('\n');
		puts("-------------------------------");
		free(data);
		free(key);
	}
	puts("[+] Only two encryptions in this version! Goodbye!");
}

int main(void)
{
        setvbuf(stdin, NULL, _IONBF, 0);
        setvbuf(stdout, NULL, _IONBF, 0);

	vuln();

	return 0;
}
