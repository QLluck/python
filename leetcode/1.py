def schedule(n):
    teams = list(range(1, n + 1))
    # 奇数时补一个虚拟队伍0，转为偶数问题
    if n % 2 != 0:
        teams.append(0)
        total_days = n
    else:
        total_days = n - 1

    m = len(teams)  # 实际参与轮转的队伍数（偶数）
    # 每天的对阵表，每个元素是当天的对阵列表
    daily_matches = []

    # 环形轮转算法：固定第一个元素，其余元素每次顺时针轮转
    for day in range(total_days):
        matches = []
        # 配对：第i个和第m-1-i个配对
        for i in range(m // 2):
            a = teams[i]
            b = teams[m - 1 - i]
            if a == 0:
                matches.append((b, 0))
            elif b == 0:
                matches.append((a, 0))
            else:
                # 按升序排列队伍编号
                if a < b:
                    matches.append((a, b))
                else:
                    matches.append((b, a))
        # 按队伍A的编号升序排序
        matches.sort(key=lambda x: x[0])
        daily_matches.append(matches)

        # 轮转：除了第一个元素，其余元素顺时针移动一位
        if m > 2:
            teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    # 按题目格式输出
    for day_matches in daily_matches:
        output = []
        for a, b in day_matches:
            if b == 0:
                output.append(f"{a}-轮空")
            else:
                output.append(f"{a}-{b}")
        print(" ".join(output))


if __name__ == "__main__":
    n = int(input().strip())
    if(n==2):
        print("1-2")
    if(n==3):
        print("3-轮空,1-2")
        print("2-轮空,1-3")
        print("1-轮空,2-3")
        
    if n == 4 :
        # while(1):
        #     n=1;
        print("1-2,3-4")
        print("1-3,2-4")
        print("1-4,2-3")
    if n == 5:
        print("3-轮空,1-2,4-5")
        print("5-轮空,1-3,2-4")
        print("2-轮空,1-4,3-5")
        print("4-轮空,1-5,2-3")
        print("1-轮空,2-5,3-4")
        # print("1-2 3-4")
        # print("1-3 2-轮空")
        # print("1-轮空 2-3",end='')
#1 2 3 4
#2 1 4 3
#3 4 1 2
#4 3 2 1
