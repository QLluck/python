
def class_7():
    import random
    list = [random.randint(1,100) for i in range(30)]
    for i in range(20):
        for j in range(20):
            if j+1<20 and list[j] <list[j+1]:
                list[j],list[j+1]=list[j+1],list[j];
    for i in range(20,30):
        for j in range(20,30):
            if j +1<30 and list[j]>list[j+1]:
                list[j],list[j+1]=list[j+1],list[j];
    print(list);

def class_8():
    import random
    list = [ random.randint(1,100) for i in range(1000)]
    #先使用冒泡排序确保重复元素相邻
    for i in range(len(list)):
        for j in range(len(list)):
            if j+1<len(list) and list[j]>list[j+1]:
                list[j],list[j+1]=list[j+1],list[j];
    #用while 循环判断 如果 相邻两个元素相同 则删除一个元素
    for i in range(len(list)):
        while i+1<len(list) and list[i]==list[i+1]:
            list.pop(i+1);
    print(list);
def class_9():
    
        year = int(input("请输入年份"))
        
        
        if (year%4==0 and year%100!=0) or (year %400 ==0):
            print(f"{year}是闰年");
        else :
            print(f"{year}不是闰年");
def class_10():
       #使用类来存储车牌对于的数据
        import math
        class car:
            def __init__(self,car_id1:str=None,car_way1:str=None ):
               self.car_id:str=car_id
               self.car_way:str=car_way
            def free_sum(self,num):
                if self.car_way=="按月租车" or "月" in self.car_way :
                    return 0
                elif num<12 :
                    return 0
                elif num<=12 and num<=60 :
                    return 5
                elif   60<num  :
                    return 5 + math.ceil((num-60)/60)*3
        car_id = input("请输入您的车牌号");
        car_way=input("请输入您的停车方式(按月租车，或临时停车)")       
        you_car:car = car(car_id,car_way);
        time = int(input("请输入您的停车时间"));
        print(f"车牌号:{you_car.car_id}\n {you_car.car_way}花费{you_car.free_sum(time)}元 ")
        
def class_11():
    import random
    num = random.randint(-99,99)
    res =1 ;
    while res<=8 :
        a =int(input("请输入竞猜年龄"));
        if a ==num:
            print("真厉害,你赢了")
            return;
        elif a <num:
            print("小了");
        elif a>num:
            print("大了");
        res+=1;
            
    print("你输了")
def class_12():
    import random
    num = random.randint(101,500)
    num2=random.randint(101,500)
    num3 = input("请输入您的座位号(101~500)")
    print(f"中奖号码为{num} {num2}")
   #输入为字符串 可直接用字符串的切片操作
    if num3==str(num) or num3==str(num2):
        print("您获得一等奖!!!!!")
    elif num3==str(num)[::-1] or num3==str(num2)[::-1] :
        print("您中了二等奖!!!")
    else:
        print("抱歉,您没有中奖!")
class_10()

    