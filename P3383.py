perim=[];
me={};
n=int(1e3+7);


def per():
    for i in range(2,n):
        if i not in me :
            perim.append(i);
        for j in perim :
                if j*i >n :
                    break;
                me[i*j]=1;
                
                if i%j==0:
                    break;
per();
a,b = map(int ,input().split())
for i in range(b):
    c = int(input())
    print(perim[c-1])