from urllib import request
from bs4 import BeautifulSoup as bs
import pymysql
import sys
from wordcloud import WordCloud
from imageio import imread
import matplotlib.pyplot as plt
from matplotlib import font_manager


def get_hpl(html):
    resp = request.urlopen(html)
    html_data = resp.read()
    soup = bs(html_data, 'html.parser')
    rate = soup.find_all('span', class_='game_review_summary positive')
    print(rate[2], rate[3])
    print(rate[2]['data-tooltip-html'], rate[3]['data-tooltip-html'])

    '''
    game = soup.find_all('tr', class_='player_count_row')

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
    '''


def main():
    html = 'https://store.steampowered.com/app/271590/Grand_Theft_Auto_V/'
    get_hpl(html)
    '''
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
    draw_chart()
    '''


if __name__ == '__main__':
    main()
