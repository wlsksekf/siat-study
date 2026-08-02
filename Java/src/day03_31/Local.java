package day03_31;

public class Local {
    public static void main(String args[]) {
        short num1 = 12;                // num1 변수의 선언문
        System.out.println(num1);

        double num2 = 12.75;            // num2 변수의 선언문
        System.out.println(num2);

        char ch = 'A';                  // ch 변수의 선언문
        System.out.println(ch);
        
        int num = 10;
        {
        	num = 30;
        }
        System.out.println(num);
    }
}
