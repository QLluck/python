def class1():
    import numpy as np
    l1 = [[i*j for i in range(1,3) ]  for j in range(1,4) ]
    l2 =[[i*j for i in range(1,5) ]  for j in range(1,3) ]
    print(l1)
    np1 = np.array(l1)
    np2=np.array(l2)
    print(np1)
    print(np2)
    print(np1.dot(np2))
def class2():
    import numpy as np 
    import matplotlib.pyplot as plt
    np1 = np.zeros((512,512),dtype=np.uint8)
    for i in range(8):
        for j in range(8):
            sr=i*64
            er = (i+1 )*64
            sc = j*64 
            ec =(j+1)*64
            if(i+j)%2==0:
                color = 255
            else :
                color = 0
                
            np1[sr:er,sc:ec]=color
    
    plt.imshow(np1, cmap='gray')
   # plt.axis('off')  # 关闭坐标轴
    plt.title('国际象棋棋盘')
    plt.show()
def class3():
    import pandas as pd

    # （1）创建 DataFrame
    data = {
        'A': [38, 48, 29, 40],
        'B': [23.5, 63, 58, 77],
        'C': [40.2, 44, 2, 31],
        'D': [23, 44, 25, 56]
    }
    df = pd.DataFrame(data)
    print(df)
    df = df.sort_values(by='D').reset_index(drop=True)
    # （2）按列 D 排序并更新行号索引
    
    print(df)
    df_mean = df.iloc[1].mean()
    print(df_mean)
    df['标准差'] = df.apply(lambda row: row.std(), axis=1)
    print(df)
    df.to_excel(__file__.replace("class.py",'data.xlsx'), index=False)

def class4():
    import matplotlib.pyplot as plt
    import numpy as np
    sub = ['语文', '数学', '英语', '物理', '化学', '生物']
    cm = [85.5, 91, 72, 59, 66, 55]
    cf=[94, 82, 89.5, 62, 49, 53]
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    x = np.arange(len(sub))
    width = 0.35  # 柱状图的宽度
    plt.figure(figsize=(6, 6))
    plt.bar(x - width/2, cm, width, label='男', color='b')
    plt.bar(x + width/2, cf, width, label='女', color='m')

    plt.xlabel('学科')
    plt.ylabel('平均成绩')
    plt.title('平均成绩柱形图')
    plt.xticks(x, sub)
    plt.legend()
    plt.tight_layout()  # 自动调整子图参数
    plt.show()  # 显示图表
    plt.figure(figsize=(6, 6))  # 创建另一个新图形，大小为6x6英寸

    plt.bar(sub, cm, label='男', color='b')
    plt.bar(sub, cf, bottom=cm, label='女', color='m')

    plt.xlabel('学科')
    plt.ylabel('平均成绩')
    plt.title('平均成绩堆积柱形图')
    plt.legend()
    plt.tight_layout()  # 自动调整子图参数
    plt.show()  # 显示图表
def class5():
        import matplotlib.pyplot as plt

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 定义数据
        sub_categories = ['服装鞋帽', '日用品', '家用电器和音像器材', '粮油食品', '化妆品', '通讯器材', 
                        '电子出版物及音像制品', '工具及家居装修', '美容及个人护理', '厨房和餐厅', '其他']
        sales_percentage = [22.00, 14.50, 10.60, 8.70, 7.50, 5.10, 3.00, 4.40, 5.40, 7.00, 11.80]

        # 创建饼图
        plt.figure(figsize=(10, 8))  # 设置图形大小
        plt.pie(sales_percentage, labels=sub_categories, autopct='%1.1f%%', startangle=90)
        plt.title('子类商品销售额占比')  # 设置标题
        plt.tight_layout()  # 自动调整布局
        plt.show()
def class6():
    import matplotlib.pyplot as plt

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 定义数据
    months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    business_2022 = [87.7, 72, 92.2, 84.6, 92.3, 102.7, 96.5, 94.4, 94.3, 98.6, 103.4, 103.7]
    business_2023 = [94.1, 89.8, 103.6, 101.1, 106.4, 110.4, 109.5, 109.1, 107.6, 103.5, 136.4, 132.6]

    # 设置主题风格
    plt.style.use('fivethirtyeight')

    # 创建折线图
    plt.figure(figsize=(12, 6))
    plt.plot(months, business_2022, color='#8B0000', marker='^', linestyle='--', linewidth=1.5, label='2022年业务量')
    plt.plot(months, business_2023, color='#006374', marker='d', linestyle='-', linewidth=1.5, label='2023年业务量')

    # 添加图例
    plt.legend()

    # 添加轴标签
    plt.xlabel('月份')
    plt.ylabel('业务量（亿件）')

    # 添加标题
    plt.title('2022年和2023年快递业务量趋势')

    # 显示图表
    plt.tight_layout()
    plt.show()
class6()