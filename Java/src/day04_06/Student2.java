package day04_06;

public class Student2 {
    String name;
    int kor, eng, math;
    static int korTotal, engTotal, mathTotal;

    public Student2(String name, int kor, int eng, int math) {
        this.name = name;
        this.kor = kor;
        this.eng = eng;
        this.math = math;

        korTotal += kor;
        engTotal += eng;
        mathTotal += math;
    }

    public int getTotal() {
        return kor + eng + math;
    }

    public float getAverage() {
        return getTotal() / 3.0f;
    }

    public static void sort(Student2[] students) {
        for (int i = 0; i < students.length - 1; i++) {
            for (int j = 0; j < students.length - 1; j++) {
                if (students[j].getTotal() < students[j + 1].getTotal()) {
                    Student2 s = students[j];
                    students[j] = students[j + 1];
                    students[j + 1] = s;
                }
            }
        }
    }

    public static void main(String[] args) {
        Student2[] students = {
            new Student2("유재석", 80, 70, 90),
            new Student2("박명수", 100, 95, 85),
            new Student2("하하", 75, 80, 70)
        };

        System.out.println("--- 정렬 전 ---");
        for (Student2 s : students) {
            System.out.println(s.name + " | 총점: " + s.getTotal() + " | 평균: " + s.getAverage());
        }

        Student2.sort(students);

        System.out.println("\n--- 정렬 후 (성적순) ---");
        for (Student2 s : students) {
            System.out.println(s.name + " | 총점: " + s.getTotal() + " | 평균: " + s.getAverage());
        }

        System.out.println("\n--- 전체 과목 총점 ---");
        System.out.println("국어 전체 총점: " + Student2.korTotal);
        System.out.println("영어 전체 총점: " + Student2.engTotal);
        System.out.println("수학 전체 총점: " + Student2.mathTotal);
    }
}