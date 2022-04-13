#include <stdio.h>
#include <string.h>

void vuln()
{
	char name[256];
	printf("Enter your name: ");
	fgets(name, 512, stdin);
	name[strlen(name)-1] = '\0';
	printf("[+] Hello %s!\n", name);
}

int main(void)
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	//while(1)
	//{
	vuln();
	//}
	puts("[DEBUG] nothing implemented yet.");

	return 0;
}
