import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
df = pd.read_csv("test1Data.csv")
npData = df.values
npx = npData[:,0]
npy=npData[:,1]
theta0= np.random.rand()
theta1=np.random.rand()
def f(x):
    return theta0 + theta1 *x
def E(x,y):
    return 0.5*np.sum( (y - f(x) )**2 )
mu=npx.mean()
sigma=npx.std()
def standardize(x):
    return (x - mu)/sigma
npz = standardize(npx)
ETA=1e-3
diff=1
count=0
error = E(npz, npy)
theta0List=[]
theta1List=[]
while diff > 1e-2 :
    tmp0 = theta0 - ETA*np.sum(f(npz)-npy)
    tmp1= theta1 -ETA*np.sum((f(npz)-npy)*npz)
    theta0 = tmp0 
    theta1 = tmp1; 
    
    current_error = E(npz,npy)
    diff = error - current_error
    error = current_error
    
    count+=1
    theta0List.append(theta0)
    theta1List.append(theta1)




fig, ax = plt.subplots() 
x = np.linspace(-3, 3, 100)
line, = ax.plot(x, theta0List[0] + theta1List[0]*x)
def update(frame):    
    
    num=frame%count# 定义动画更新函数，每帧调用一次
    ax.plot(npz, npy, 'o')
    line.set_ydata(theta0List[num]+theta1List[num]*x )  # 更新曲线的y值，实现相位移动
    # 不设置坐标轴范围，让Matplotlib自动调整
    return line, 
ani = FuncAnimation(                # 创建动画对象
    fig,                            # 指定图形对象
    update,                         # 指定更新函数
    frames=range(100),              # 帧数范围(0到99)
    interval=50                     # 帧间隔(毫秒)，控制动画速度
)

plt.show()