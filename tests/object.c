struct
{
	long a, w;
	char c;
	float k;
	long p;
} Test;


int main()
{
	struct Test t;

	t.a = 5;
	t.w = 19;
	t.p = (t.w % t.a) - 2;
	t.c = '$';

	t.k = 5.2;
	float s = 2.5;
	t.k = s * t.k;

	printf(t.p, long);
	printf(t.c, char);
	printf(t.k, float);
}