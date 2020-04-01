from urllib import request
from bs4 import BeautifulSoup as bs
import pymysql
import sys
from wordcloud import WordCloud
from imageio import imread
import matplotlib.pyplot as plt


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
                (int(line[0]), int(line[0]), pymysql.escape_string(line[2])))
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


'''
# 绘制图表
def draw_charts():
    labels = '>1000000', '>100000且<1000000', '>10000且<100000', '<10000'
    sizes = [15, 30, 45, 10]
    # 设置分离的距离，0表示不分离
    explode = (0, 0.1, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio 保证画出的图是正圆形
    plt.axis('equal')
    plt.show()
'''


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
    draw_word_cloud(merge_string)


if __name__ == '__main__':
    main()
