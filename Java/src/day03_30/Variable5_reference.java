package day03_30;

public class Variable5_reference {

	public static void main(String[] args) {
		String s1 = "자바";
		
		String s2 = new String("자바");
		
		System.out.println("s1=" + s1 + " s2=" + s2);
		
		if (s1 == s2) {
			System.out.println("같은 주소");
		} else {
			System.out.println("다른 주소");
		}
		
		if (s1.equals(s2)) {
			System.out.println("같은 값");
		} else {
			System.out.println("다른 값");
		}

	}

}
