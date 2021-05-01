import re
from bs4 import BeautifulSoup
import requests
import sqlite3


def get_chosenDate_soup(dateNum):
    page = 1

    video_title = ''
    video_content = ''
    video_performer = ''
    video_date = ''
    video_link = ''

    videoInfoLists = []

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
                    video_title = str(div_child.getText())
                    video_title = video_title.replace(u'\u3000', u'')
                    # print('標題: ' + div_child.getText())
                    if date_pattern.search(div_child.getText()[-6:]) is not None:
                        content = div_title.getText()
                        content_list = re.split('内容：|出演：', content)
                        link = div_title.find_previous_sibling('div').findChild('a')['href']
                        # print('內容: ' + content_list[1])
                        video_content = content_list[1]
                        # print('出演者: ' + content_list[2])
                        video_performer = content_list[2]
                        # print('影片連結: ' + link)
                        video_link = link
                        # print('日期: ' + video_date_num)
                        video_date = video_date_num
                        break

                    else:
                        print('date pattern not pass!!')

                videoInfoList = [video_date, video_title, video_content, video_performer, video_link]
                videoInfoLists.append(videoInfoList)
                # print(videoInfolist)
            # print(videoInfoLists)
        except Exception as e:
            print(e)

        if int(video_date_num) >= int(dateNum):
            page += 1
            # print('page: ' + str(page))
        else:
            break

    return videoInfoLists


def insertDB(videoInfoLists):
    dbfile = "J_VarietyShow.db"

    conn = sqlite3.connect(dbfile)
    print(len(videoInfoLists))
    for v1 in videoInfoLists:
        conn.execute("Insert into Japan_VarietyShow_Table (datenum, title, content, performer,link) values (?,?,?,?,?)",
                     (v1[0], v1[1], v1[2], v1[3], v1[4]))
        conn.commit()

    conn.close()


if __name__ == "__main__":
    li = get_chosenDate_soup(201001)
    insertDB(li)
