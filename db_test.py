import re
from bs4 import BeautifulSoup
import requests
import sqlite3


def get_chosenDate_soup():
    page = 1

    video_title = []
    video_content = []
    video_performer = []
    video_date = []


    while True:
        base_url = 'https://jshow.tv/more-post/page/' + str(page)
        print(page)
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        div_titles = soup.find_all('div', class_='des')
        date_pattern = re.compile(r'\d\d\d\d\d\d')
        try:
            for div_title in div_titles:
                video_date_num = date_pattern.search(div_title.getText()).group(0)
                for div_child in div_title.children:
                    print('標題: ' + div_child.getText())
                    if date_pattern.search(div_child.getText()[-6:]) is not None:
                        content = div_title.getText()
                        content_list = re.split('内容：|出演：', content)
                        link = div_title.find_previous_sibling('div').findChild('a')['href']
                        print('內容: '+content_list[1])
                        print('出演者: '+ content_list[2])
                        print('影片連結: '+ link)
                        print('日期: '+ video_date_num)
                        break
                    else:
                        print('date pattern not pass!!')
        except Exception as e:
            print(e)

        page += 1

        #return



if __name__ == "__main__":
    get_chosenDate_soup()