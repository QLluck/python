import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("test1Data.csv")
npData = df.values
npx = npData[:,0]
npy=npData[:,1]
theta= np.random.rand(4)
mu=npx.mean()
sigma=npx.std()
def standardize(x):
    return (x - mu)/sigma
npz = standardize(npx)
def to_matrix(x):
    return np.vstack([np.ones(x.shape[0]), x, x ** 2,x**3]).T
X = to_matrix(npz)
def f(x):
    return np.dot(x,theta)
def E(x,y):
    return 0.5*np.sum( (y - f(x) )**2 )

ETA=1e-3
diff=1
count=0
error = E(X, npy)
while diff > 1e-2 :
   
    theta=theta-ETA * np.dot(f(X) - npy, X)
    
    current_error = E(X,npy)
    diff = error - current_error
    error = current_error
    
    count+=1
    log = "第{}次 theta0={:.3f} , theta1 = {:.3f},差值={:.4f}"
    print(diff)
  #  print(log.format(count,theta0,theta1,diff))

x = np.linspace(-3, 3, 100)

plt.plot(npz,npy,'o')
plt.plot(x,f(to_matrix(x)))
plt.show()