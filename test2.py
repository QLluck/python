def f(i):
    if(i<=1):
        return 1
    else :
        return i*f(i-1);
sum =0 ;
for i in range(1,100):
    sum+=f(i);
    print(sum);
