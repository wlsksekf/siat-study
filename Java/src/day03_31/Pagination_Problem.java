package day03_31;

import java.util.Scanner;

public class Pagination_Problem {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        // 1번
        System.out.print("1번 - 정수를 입력하세요: ");
        int input1 = sc.nextInt();
        int result1 = input1 / 10;
        System.out.println(result1);
        
        // 2번
        System.out.print("2번 - 정수를 입력하세요: ");
        int input2 = sc.nextInt();
        int result2 = (input2 - 1) / 10;
        System.out.println(result2);
        
        // 3번
        System.out.print("3번 - 정수를 입력하세요: ");
        int input3 = sc.nextInt();
        int result3 = ((input3 - 1) / 10) * 10;
//        System.out.println(result3);

        // 4번
        System.out.print("4번 - 정수를 입력하세요: ");
        int input4 = sc.nextInt();
        int result4 = ((input4 - 1) / 10) * 10 + 1;
        System.out.println(result4);

        // 5번
        System.out.print("5번 - page를 입력하세요: ");
        int page = sc.nextInt();
        int startpage = ((page - 1) / 10) * 10 + 1;
        System.out.println("startpage=" + startpage);

        // 6번
        System.out.print("6번 - limit를 입력하세요: ");
        int limit = sc.nextInt();
        System.out.print("6번 - listcount를 입력하세요: ");
        int listcount = sc.nextInt();
        
        int maxpage = (listcount + limit - 1) / limit;
        System.out.println("maxpage = " + maxpage);

        sc.close();
    }
}