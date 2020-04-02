from matplotlib import pyplot as plt
from matplotlib import font_manager

# 调用中文字体
my_font = font_manager.FontProperties(fname="C:/WINDOWS/Fonts/msyh.ttc")

# 设置图形大小
plt.figure(figsize=(10, 7), dpi=80)

# 数据
a = ["唐人街探案", "中国女排", "战狼2", "刺杀小说家", "大闹天宫", "肖申克的救赎"]
b_1 = [23, 34, 12, 45, 34, 45]
b_2 = [34, 12, 35, 13, 26, 32]
b_3 = [23, 15, 25, 36, 24, 17]

height = 0.2
a1 = list(range(len(a)))
a2 = [i + height for i in a1]  # 坐标轴偏移
a3 = [i + height * 2 for i in a1]

# 绘图
plt.barh(range(len(a)), b_1, height=height, label="第一天", color="#FFC125")
plt.barh(a2, b_2, height=height, label="第二天", color="#969696")
plt.barh(a3, b_3, height=height, label="第三天", color="#473C8B")

# 绘制网格
plt.grid(alpha=0.4)

# y轴坐标刻度标识
plt.yticks(a2, a, fontproperties=my_font, fontsize=14)

# 添加图例
plt.legend(prop=my_font)

# 添加横纵坐标，标题
plt.xlabel("票房/亿元", fontproperties=my_font, fontsize=16)
plt.ylabel("电影名称", fontproperties=my_font, fontsize=16)
plt.title("1,2,3号电影实时票房统计图", fontproperties=my_font, fontsize=24)

# 显示图形
plt.show()
