package day03_30;

public class Literal4_printf {
    public static void main(String args[]) {
        /*
         * 1. System.out.println() : 괄호안의 내용을 출력한 후 한 행을 띄웁니다.
         * 2. System.out.print()   : 괄호안의 내용을 출력한 후 한 행을 띄지 않고 유지합니다.
         * 3. System.out.printf()  : 서식을 지정해서 출력합니다.
         * 형식: System.out.printf("포맷 명시자", 데이터)
         * 주의점: %로 시작하는 포맷 갯수와 데이터의 갯수가 일치해야 합니다.
         */
        // 리터럴(literal)- 그 자체로 값을 의미 하는 것

        // 정수 42를 정수 서식(%d)으로 출력해라
        System.out.printf("%d\n", 42);

        // 실수 42.195를 실수 서식(%f)으로 출력해라
        // (기본 소수점이하 6자리)
        System.out.printf("%f", 42.195);
        System.out.println(); // 줄을 바꿉니다.

        // 실수 42.195를 실수 서식 소수점 이하 2자리(%.2f)로 출력해라. 소수점 아래 3자리에서 반올림
        // \n(%n)은 출력 후 줄 바꾸라는 서식
        System.out.printf("%.2f\n", 42.195);

        // 전체 6자리에 소수점과 소수점 이하 자리 3자리를 출력
        System.out.printf("%6.3f%n", 42.195);
        System.out.printf("%7.3f%n", 42.195); // 전체 7자리에 소수점과 소수점 이하 자리 3자리를 출력
        
        System.out.printf("\n나의 이름은 %10s, 나의 나이는 %d세 입니다.", "홍길동", 21);
        
        System.out.printf("%10d", 42);
    }
}