from urllib import request
from bs4 import BeautifulSoup as bs
import pymysql
import sys
from wordcloud import WordCloud
from imageio import imread
import matplotlib.pyplot as plt
from matplotlib import font_manager


def get_data(html):
    resp = request.urlopen(html)
    html_data = resp.read()
    soup = bs(html_data, 'html.parser')
    game = soup.find_all('tr', class_='player_count_row')

    output = sys.stdout
    outputfile = open("output/gamelist.txt", 'w', encoding='utf-8')
    sys.stdout = outputfile
    print(format('当前玩家人数' + '^' + '今日峰值' + '^' + '游戏'))
    all_gamehtml = []
    for item in game:
        data = []

        for span in item.find_all('span', class_='currentServers'):
            data.append(span.text.replace(',', ''))

        games = item.find('a', class_='gameLink').text
        data.append(games)

        gamehtml = item.find('a', class_='gameLink').get('href')
        all_gamehtml.append(gamehtml)

        print(format(data[0] + '^' + data[1] + '^' + data[2]))
    outputfile.close()
    sys.stdout = output

    return all_gamehtml


# 连接数据库
def read__db():
    db = pymysql.connect(host="localhost", user='root', passwd='123456', database="fzl661")
    cursor = db.cursor()
    cursor.execute("truncate table gamelist")
    count = 0
    fr = open("output/gamelist.txt", "r", encoding='utf-8')
    try:
        for line in fr:
            count += 1
            if (count == 1):
                continue
            line = line.strip().split('^')
            cursor.execute(
                "insert into gamelist(current,peak,game) values('%d','%d','%s')" %
                (int(line[0]), int(line[1]), pymysql.escape_string(line[2])))
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    cursor.close()
    db.close()
    fr.close()


# 获取标签
def get_tag(first_html):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    resp = request.urlopen(request.Request(url=first_html, headers=headers))
    first_html_data = resp.read()
    soup = bs(first_html_data, 'html.parser')

    datatags = []
    for i in soup.find_all('a', class_="app_tag"):
        datatags.append(i.text)
    return datatags


# 数据清洗
def clean(datatags):
    comments = ''
    for k in range(len(datatags)):
        comments = comments + (str(datatags[k]))
    return comments


# 绘制词云
def draw_word_cloud(commentsdt):
    color_mask = imread('resource/background.jpg')
    cloud = WordCloud(
        font_path='simhei.ttf',
        background_color='white',
        mask=color_mask,
        max_words=2000,
        max_font_size=120
    )
    word_cloud = cloud.generate(commentsdt)
    word_cloud.to_file('output/output.jpg')
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


# 绘制图表
def draw_charts():
    # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
    db = pymysql.connect(host="localhost", user='root', passwd='123456', database="fzl661")
    cursor = db.cursor()  # 获取一个游标
    cursor.execute("select * from gamelist order by current limit 90,10")
    result = cursor.fetchall()  # result为元组
    # 将元组数据存进列表中
    current = []
    peak = []
    game = []
    for x in result:
        current.append(x[0])
        peak.append(x[1])
        game.append(x[2])

    # 直方图
    # 调用中文字体
    my_font = font_manager.FontProperties(fname="C:/WINDOWS/Fonts/msyh.ttc")

    # 设置图形大小
    plt.figure(figsize=(15, 12), dpi=80)

    height = 0.2
    g1 = list(range(len(game)))
    g2 = [i + height for i in g1]  # 坐标轴偏移

    # 绘图
    plt.barh(range(len(game)), current, height=height, label="当前", color="#FFC125")
    plt.barh(g2, peak, height=height, label="峰值", color="#969696")

    # 绘制网格
    plt.grid(alpha=0.4)

    # y轴坐标刻度标识
    plt.yticks(g2, game, fontproperties=my_font, fontsize=10)

    # 添加图例
    plt.legend(prop=my_font)

    # 添加横纵坐标，标题
    plt.xlabel("人数", fontproperties=my_font, fontsize=16)
    # plt.ylabel("游戏名称", fontproperties=my_font, fontsize=16)
    plt.title("Steam在线人数排名前十的游戏人数统计图", fontproperties=my_font, fontsize=24)


    # 显示图形
    plt.show()
    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库


def main():
    html = 'https://store.steampowered.com/stats/'
    all_gamehtml = get_data(html)
    read__db()
    commentsdt = []
    for n in range(5):
        first_html = all_gamehtml[n]
        datatags = get_tag(first_html)
        comments = clean(datatags)
        commentsdt.append(comments)
        merge_string = ''.join(commentsdt)
    # draw_word_cloud(merge_string)
    draw_charts()


if __name__ == '__main__':
    main()
