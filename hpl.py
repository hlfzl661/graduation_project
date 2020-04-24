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
    rate = soup.find_all('div', class_='user_reviews_summary_row')
    print(rate[0]['data-tooltip-html'], rate[1]['data-tooltip-html'])
    '''
    print(rate[2], rate[3])
    print(rate[2]['data-tooltip-html'], rate[3]['data-tooltip-html'])
    '''


def main():
    html = 'https://store.steampowered.com/app/578080/PLAYERUNKNOWNS_BATTLEGROUNDS/'
    get_hpl(html)


if __name__ == '__main__':
    main()
