int main()
{
    int low, high, i, flag;
    low = 3;
    high = 120;
    int count = 0;

    while (low < high)
    {
        flag = 0;

        for(i = 2; i <= low/2; i = i + 1)
        {
            if(low % i == 0)
            {
                flag = 1;
                break;
            }
        }

        if (flag == 0)
            count = count + 1;

        ++low;
    }

    return 0;
}