import re
from urllib import request
from bs4 import BeautifulSoup as bs
import pymysql
import sys
from wordcloud import WordCloud
from imageio import imread
import matplotlib.pyplot as plt
from matplotlib import font_manager
from threading import Thread

cookie = '''wants_mature_content=1; browserid=1359458084329624432; timezoneOffset=28800,0; _ga=GA1.2.1926505665.1578798454; lastagecheckage=1-0-1908; _gid=GA1.2.1264468100.1587909879; steamCountry=CN%7C36b9cc369137cd46d91178768314b178; sessionid=a7a26f9422b6827f7ded755c; app_impressions=271590@1_4_4__129_1|1090630@1_7_15__13|219990@1_7_15__13|683320@1_7_15__13|815370@1_7_15__13|271590@1_7_15__13|880940@1_4_4__129_1|683320@1_4_4__139_3|418240@1_4_4__139_3|595520@1_4_4__139_3|559650@1_4_4__139_2|578080@1_4_4__139_2|214490@1_4_4__43_1; birthtime=-1959321599; recentapps=%7B%22271590%22%3A1587996043%2C%221151340%22%3A1587909886%2C%22761890%22%3A1587821084%2C%22440%22%3A1587817884%2C%22730%22%3A1587736768%2C%22359550%22%3A1587736279%2C%22578080%22%3A1587736011%2C%2248700%22%3A1586706897%2C%221085660%22%3A1586706840%2C%22397540%22%3A1586706726%7D'''


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
            if count == 1:
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
def get_tag(first_html, tags_list, index):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': cookie
    }
    resp = request.urlopen(request.Request(url=first_html, headers=headers))
    first_html_data = resp.read()
    soup = bs(first_html_data, 'html.parser')

    datatags = []
    for i in soup.find_all('a', class_="app_tag"):
        datatags.append(i.text)

    tags_list[index] = clean(datatags)


def get_rate(first_html, rate_list, index):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': cookie
    }
    resp = request.urlopen(request.Request(url=first_html, headers=headers))
    first_html_data = resp.read()
    soup = bs(first_html_data, 'html.parser')

    rate = []
    for j in soup.find_all('span', class_=re.compile("game_review_summary.*"))[0:2]:
        rate.append(j.text)

    # if len(rate) != 0 and rate[0] != '':
    #     print(format(rate[0] + '^' + rate[1]))
    # else:
    #     print(" ")

    rate_list[index] = rate


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
    word_cloud.to_file('output/wordcloud.jpg')
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


# 绘制图表
def draw_chart():
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
    plt.savefig('output/chart.jpg')
    plt.show()
    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库


def main():
    html = 'https://store.steampowered.com/stats/'
    all_gamehtml = get_data(html)
    # read__db()
    tagsdt = [''] * 100
    ratedt = [['']] * 100
    # for j in all_gamehtml:
    #     get_rate(j)
    threads = []
    for n in range(100):
        first_html = all_gamehtml[n]
        # get_tag_thread = Thread(target=get_tag, args=(first_html, tagsdt, n))
        # threads.append(get_tag_thread)
        # get_tag_thread.start()

        get_rate_thread = Thread(target=get_rate, args=(first_html, ratedt, n))
        threads.append(get_rate_thread)
        get_rate_thread.start()

    for thread in threads:
        thread.join()

    output = sys.stdout
    outputfile = open("output/rate.txt", 'w', encoding='utf-8')
    sys.stdout = outputfile

    for rate in ratedt:
        if len(rate) != 0 and rate[0] != '':
            print(format(rate[0] + "^" + rate[1]))
        else:
            print(" ")

    outputfile.close()
    sys.stdout = output

    # merge_string = ''.join(tagsdt)
    # draw_word_cloud(merge_string)
    # draw_chart()


if __name__ == '__main__':
    main()
