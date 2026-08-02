package day03_31;

import java.io.InputStream;
import java.util.Scanner;
//ctrl + shift + o

public class Oper_input {
    public static void main(String[] args) {
        //System.in은 키보드로 데이터를 입력 받을때 사용합니다.
        //InputStream java.lang.System.in
        InputStream is = System.in;

        //java.util.Scanner.Scanner(InputStream source)
        // 클래스명      참조형 변수  연산자           생성자 호출
        Scanner sc = new Scanner(is);

        //콘솔에서 "정수를 입력 하세요>" 다음에 커서를 위치하고 숫자 입력 후 엔터
        System.out.print("정수를 입력 하세요>");
        int a = sc.nextInt();//정수를 읽어 변수 a에 저장합니다.

        System.out.println("입력값은 " + a + "입니다.");

        System.out.print("정수를 입력 하세요>");
        int b = sc.nextInt();
        System.out.println("입력값은 " + b + "입니다.");
        
        sc.close();
    }
}