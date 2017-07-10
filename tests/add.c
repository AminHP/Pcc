struct
{
	int a, w;
	char c[51];
	float b[56];
	long p;
} Test;

int main()
{
	struct Test t;
	t.a = 2;
	int z[2];
	z[1] = 5;

	int x = (t.a + 5) % z[1];

	/*
    //char a, c = 'a';
    int i, sum = 0;
    {
    char a[50] = "Asd";}
    //int l[2] = {1, 2};

    for (i = 1; i <= n; i = i+1) {
      int x = 10 - ((i + 2) * (x / 7)) + 10;
    } /*-for-*/

	//int i = 11;
	//int b = 10;
    //int x = 10 - ((i + 2) * (b / 7)) + 20;
    //int y = i && b;

	/*float f1, f2 = 2.3;
	f1 = f2 + 5.2;
	int a = 2, w = 4;
	int c;
	c = (a + w) / 2;
	float x[11];
	x[c] = (f1 + f2) * 2.0;
	char x = 'a';
	double d, d1 = 25.2;
	double d2 = d1 + 152.5;
	long l1, l2 = 2512312313132;
	long l3;
	l3 = (l2 + 152312312) * 112;*/

    /*int a = 1, w = a + 2;
    int b[10];
    int d = 2;
    d = 5 + a + w;
    b[d] = 16;

    int c[17];
    c[13 + a] = (67 + b[d]) * 2;*/

    /*int a = 2;
    int b = 3;
    {
    	int c = a + b;
    	int d = c + 5;
    }
    int x = c + a;*/

    return 0;
}
