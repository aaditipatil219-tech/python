cpu_hour=int(input("enter no. of cpu hours"))
storage=int(input("enter storage in gb"))
data_transfer=int(input("enter data transfer in gb"))
cpu_cost=cpu_hour*5
storage_cost=storage*2
data_transfer_cost=data_transfer*1
total_amount=cpu_cost+storage_cost+data_transfer_cost
if cpu_hour>100:
    print(total_amount+500)
else:
    print(total_amount)
    

