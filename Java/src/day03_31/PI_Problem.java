package day03_31;

public class PI_Problem {

	public static void main(String[] args) {
		final double PI = 3.14;
		
		double radius = 2.0;
		
		double circum = 2 * PI * radius;
		
		double area = PI * radius * radius;
		
		System.out.println("원주율 = "  + PI);
		System.out.println("반지름 = " + radius);
		System.out.println("원의 둘레 = " + circum);
		System.out.println("원의 넓이 = " + area);
	}

}
