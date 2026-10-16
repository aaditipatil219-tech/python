

weight=float(input("Enter your weight: "))
height=float(input("Enter your height: "))
bmi=weight/(height**2)
if bmi<18.5:
    category="underweight"
elif bmi<25:
    category="normal"
elif bmi<30:
    category="overweight"
else:category="obese"
print("BMI:",bmi)
print("Category:",category)



units=int(input("enter number units used"))
if units<=100:
    bill=units*1
elif units<=200:
    bill=100*1+(units-100)*2
else:
    bill=100*1+100*2+(units-200)*5
    print("Electricity bill:",bill)
    
    
    
a=int(input("Enter first angle:"))
b=int(input("Enter second angle"))
c=int(input("Enter third angle:"))
if a==b and b==c and c==a:
        print("Equilateral triangle")
elif(a==b or b==c or a==c):
        print("isosceles triangle")
else:
        print("Scalene triangle")
        
        
    
age=int(input("enter age"))
if age>=18:
    print("allowed for match")
    if age>=18 and age<30:
        print("2$ ticket price")
    elif age>=30 and age<60:
        print("1$ ticket price")
    else:
        print("0$ ticket price")
else:
    print("not allowed for match")