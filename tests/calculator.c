int main() {

    char operator = '*';
    double firstNumber,secondNumber;
    double result;

    // find the match operator

    switch(operator)
    {
        case '+':
            result = firstNumber + secondNumber;
            break;

        case '-':
            result = firstNumber - secondNumber;
            break;

        case '*':
            result = firstNumber * secondNumber;
            break;

        case '/':
            result = firstNumber / secondNumber;
            break;

        // operator doesn't match any case constant (+, -, *, /)
        default:
            result = -1;
    }

    return 0;
}