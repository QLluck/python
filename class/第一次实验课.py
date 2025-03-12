
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
    import random
    num = random.randint(-99999,999999)
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
            
    print("你输了")
class_10();
    