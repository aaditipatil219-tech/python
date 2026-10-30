# lst=[0]*10
# print(lst)



# lst=[0,1,2]*5
# print(lst)


# lst=[10,20,30,40,50,60,70]
# print(lst[0])
# print(lst[::])
# print(lst[1:5])


profit=[200,450,300]
max_profit=profit[0]
for p in profit:
    if p>max_profit:
        max_profit=p
        print("highest profit:",max_profit)