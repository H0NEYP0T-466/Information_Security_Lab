marks = float(input("Enter marks (1-100): "))
if marks < 50:
    print("Grade: F")
elif marks <= 60:
    print("Grade: E")
elif marks <= 70:
    print("Grade: D")
elif marks <= 80:
    print("Grade: C")
elif marks <= 90:
    print("Grade: B")
elif marks <= 100:
    print("Grade: A")
else:
    print("Invalid marks")