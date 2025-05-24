import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
x = np.linspace(0, 2*np.pi, 100)
line, = ax.plot(x, np.sin(x))

def update(frame):
    line.set_ydata(np.sin(x + frame/10))  # 更新y值
    # 不设置坐标轴范围，让Matplotlib自动调整
    return line,

ani = FuncAnimation(fig, update, frames=range(100), interval=50)
plt.show()