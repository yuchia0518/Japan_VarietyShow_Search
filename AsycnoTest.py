from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import re

from bs4 import BeautifulSoup
import requests

import asyncio
from aiohttp import ClientSession

url = "https://jshow.tv/"

def getReqeust():
    # res = requests.get(url)

    page = 1
    title_list = []
    link_list = []
    keyword = "有吉弘行"
    date_num = 210505

    while True:
        base_url = 'https://jshow.tv/more-post/page/' + str(page)
        print("page" + str(page))

        # html_body = response.text()
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'lxml')
        div_titles = soup.find_all('div', class_='des')
        video_date_num = int()
        date_pattern = re.compile(r'\d\d\d\d\d\d')
        try:
            for div_title in div_titles:
                video_date_num = date_pattern.search(div_title.getText()).group(0)
                if keyword in div_title.getText():
                    for div_child in div_title.children:
                        if date_pattern.search(div_child.getText()[-6:]) is not None:
                            title_list.append(div_title.getText())
                            link_list.append(div_title.find_previous_sibling('div').findChild('a')['href'])
                            break
                        else:
                            print('date pattern not pass!!')

        except Exception as e:
            print(e)

        if int(video_date_num) >= int(date_num):
            page += 1
            # print('page: ' + str(page))
        else:
            break

    return title_list, link_list


if __name__ == "__main__":
    t_list, l_list = getReqeust()
    print(t_list)
    print(l_list)
    # getReqeust()getReqeust
