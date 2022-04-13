#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int wins = 0;

void menu()
{
	puts("[1]. Test your luck!");
	puts("[2]. Hack!");
	puts("[3]. Exit");
	printf("$> ");
}

void kazino()
{
	puts("! ! ! ![sTarTed!]! ! ! !");
	usleep(500000);
	puts("3");
	usleep(500000);
	puts("2");
	usleep(500000);
	puts("1!");
	int rnd = rand();
	if (rnd != 0)
	{
		puts("bad luck");
		puts("bye!");
		exit(0);
	} else
	{
		wins++;
		printf("You win! Win %d more times to get the prize!\n", 10 - wins);
		if (wins == 10)
		{
			FILE *fp;
			char flag[255];

			fp = fopen("flag.txt", "r");
			fscanf(fp, "%s", flag);
			printf("[PRIZE]: %s\n", flag);
			fclose(fp);
		}
	}

}

void hack()
{
	char *where;
	scanf("%p", &where);
	where[0] = '\0';
}

void kazino_exit()
{
	char answer[8];
	puts("U rly want to exit?");
	printf("(yes/no): ");
	fgets(answer, 8, stdin);
	answer[strlen(answer) - 1] = '\0';
	if (!strcmp(answer, "yes"))
	{
		puts("Bye!");
		exit(-1);
	}
	if (!strcmp(answer, "no"))
	{
		puts("Nice!");
		printf("*i have gift for you**%p*\n", puts);
	} else
		puts("???");
}

int main(void)
{
	int input;
	srand(time(NULL));
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	puts("(+) Test your luck! (+)");
	while (1)
	{
		menu();
		scanf("%d", &input);
		getchar();
		if (input == 1)
			kazino();
		else if (input == 2)
			hack();
		else if (input == 3)
			kazino_exit();
		else
			puts("[!] Wrong option!");
	}
	return 0;
}
