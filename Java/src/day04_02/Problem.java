package day04_02;

import java.util.Arrays;

public class Problem {

	public static void main(String[] args) {
		int[] a = {5, 4, 3, 2, 1};
		
		for(int i=0; i < a.length-1; i++) {
			System.out.printf("a[%d]번째 데이터 선택, 비교 후 두 수 바꾸기\n", i);
			System.out.println("원본 데이터: " + Arrays.toString(a));
			
			for (int j = i + 1; j < a.length; j++) {
				if(a[i] > a[j]) {
					System.out.printf("i=%d\tj=%d\ta[%d]=%d > a[%d]=%d ", i, j, i, a[i], j, a[j]);
					
					int temp = a[i];
					
					a[i] = a[j];
					a[j] = temp;
				
				System.out.println(Arrays.toString(a));
				}
			}
			System.out.println("=======================================");
		}
	}
}
