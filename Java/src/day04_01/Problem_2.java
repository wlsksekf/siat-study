package day04_01;

import java.util.Scanner;

public class Problem_2 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("입력할 숫자의 개수를 입력하세요: ");
        int count = sc.nextInt();
        
        int[] data = new int[count];

        System.out.println(count + "개의 정수를 입력하세요:");
        for (int i = 0; i < data.length; i++) {
            data[i] = sc.nextInt();
        }

        int max = data[0];
        int min = data[0];

        for (int i = 1; i < data.length; i++) {
            if (data[i] > max) {
                max = data[i];
            }
            if (data[i] < min) {
                min = data[i];
            }
        }

        System.out.println("최대값: " + max);
        System.out.println("최소값: " + min);
        
        sc.close();
    }
}