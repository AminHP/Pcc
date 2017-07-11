int main()
{
	int i = 0;
	int x = 50;
	while ((i * 5) < x)
	{
		printf(i, int);
		i = i + 1;
	}

	printf('-', char);

	int a = 6;
	int b = 3;

	for (int j = 0; j < 10; j = j + 1)
	{
		if ((j <= a && j >= b) || (a == b * j))
		{
			printf(j, int);
		}
	}
}