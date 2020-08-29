from bs4 import BeautifulSoup
import urllib.request
import ssl
import requests
import json
import csv
context = ssl._create_unverified_context()
# print('context', context)

def get_new_feed():
    url = 'https://ncov.moh.gov.vn/web/guest/trang-chu'
    # page = urllib.request.urlopen(url, context=context)
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')
    new_feed = soup.find(class_='journal-content-article')
    print(new_feed)
    return new_feed
# get_new_feed()
def to_soup(html):
    return BeautifulSoup(html, 'html.parser')
def get_journey():
    url = 'https://ncov.moh.gov.vn/dong-thoi-gian'
    page = requests.get(url, verify=False)
    soup = to_soup(page.text)
    journey = soup.find_all("div",class_='timeline')[:5]

    print(len(journey))
    print(journey[0])
    dt_arr= []
    cnt_arr = []

    for j in journey:
        print(j.find("h3").text)
        dt_arr.append(j.find("h3").text)
        print(j.find("p").text)
        cnt_arr.append(j.find("p").text)


    return dt_arr,cnt_arr
# get_journey()
def get_hotline(all=False):
    if all:
        url = 'https://ncov.moh.gov.vn/documents/20182/6848000/Duongdaynong/'
    else:
        url = 'Đường dây nóng: 19009095 / 19003228'
    return url
# get_hotline(True)
def get_video(video_id=0):
    video_list = {
        # Khuyen cao chung
        0:"https://ncov.moh.gov.vn/documents/20182/6863405/video003/",
        # Dieu khien phuong tien
        1:"https://ncov.moh.gov.vn/documents/20182/6863405/video002/",
        # Cach ly tai nha
        2:"https://ncov.moh.gov.vn/documents/20182/6863405/c%C3%A1ch+ly+01/",
        # Nhugn ai can cach ly
        3:"https://ncov.moh.gov.vn/documents/20182/6863405/C%C3%A1ch+ly+t%E1%BA%A1i+nh%C3%A0/",
        # Huong dan cach ly
        4:"https://ncov.moh.gov.vn/documents/20182/6863405/H%C6%B0%E1%BB%9Bng+d%E1%BA%ABn+c%C3%A1ch+ly+tai+nh%C3%A0%281%29/"
    }
    return video_list[video_id]
def get_symptom():
    symptom_txt = """"""
    return symptom_txt
def get_summary():
    url = 'https://suckhoetoandan.vn/'
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')

    main_row = soup.find_all("div",class_ ="box-heading")[1:]


    # print(main_row)

    all_of_it = "SỐ LIỆU LŨY KẾ ĐẾN HIỆN TẠI:\n"
    all_of_it += "Toàn cầu:\n"

    number = main_row[0].find_all("span",class_ = "box-total")
    all_of_it += "Số người bị nhiễm: " + number[0].text + "\n"
    all_of_it += "Số người tử vong: " + number[2].text+ "\n"
    all_of_it += "Số người bình phục: " + number[4].text+ "\n"

    all_of_it += "Việt Nam:\n"

    number = main_row[0].find_all("span", class_="box-total")
    all_of_it += "Số người bị nhiễm: " + number[1].text + "\n"
    all_of_it += "Số người tử vong: " + number[3].text + "\n"
    all_of_it += "Số người bình phục: " + number[5].text + "\n"

    all_of_it += "SỐ LƯỢNG TĂNG TRONG NGÀY:\n"
    all_of_it += "Toàn cầu:\n"

    number = main_row[1].find_all("span", class_="box-total")
    all_of_it += "Số người bị nhiễm: " + number[0].text + "\n"
    all_of_it += "Số người tử vong: " + number[2].text + "\n"
    all_of_it += "Số người bình phục: " + number[4].text + "\n"

    all_of_it += "Việt Nam:\n"

    number = main_row[1].find_all("span", class_="box-total")
    all_of_it += "Số người bị nhiễm: " + number[1].text + "\n"
    all_of_it += "Số người tử vong: " + number[3].text + "\n"
    all_of_it += "Số người bình phục: " + number[5].text + "\n"

    print(all_of_it)
def sort_by_year(d):
    '''
    helper function for sorting a list of dictionaries'''
    return d.get('ma', None)
# get_summary()
def get_detail_domestic():
    url = 'https://ncov.moh.gov.vn/web/guest/trang-chu'
    page = requests.get(url, verify=False)

    with open('crawler/data/info_citylist.txt', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]: rows[1] for rows in reader}
        # print(reader)
    # print(mydict)
    # print(page.text)
    #28856
    #65976
    key = "function getInfoByMa(ma)"
    html = page.text
    start_domestic = html.index(key) + len(key)
    html = html[start_domestic:]
    key = "_congbothongke_WAR_coronadvcportlet_jsonData : '"
    start_domestic = html.index(key) + len(key)
    key = "}]'"
    end_domestic = html.index(key, start_domestic) + len(key) - 1;

    json_str = html[start_domestic:end_domestic]

    json_obj = json.loads(json_str)

    print(json_obj)

    all_of_it = "🛑CHI TIẾT TÌNH HÌNH COVID-19 TRONG NƯỚC"
    for row in sorted(json_obj, key=sort_by_year,reverse=True):
            if row['ma']!='' and row['ma']!='--Chọn địa phương--' and row['soCaNhiem']!='0':
                all_of_it += ("\n%s - Nhiễm: %s - Tử vong: %s - Nghi nhiễm: %s - Bình phục: %s" % (mydict[row['ma']].strip(), row['soCaNhiem'],row['tuVong'],row['nghiNhiem'],row['binhPhuc']))  # test

    print(all_of_it)
# get_detail_domestic()
def get_news():
    url = 'https://suckhoetoandan.vn/'
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')

    main_row = soup.find("div",class_ ="list-new-left-type3").find_all("div", class_ ="item-new")

    message_str = """{
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    [CONTENT]
                ]
            }
        }
    }"""

    inside_cnt_template = """{
                        "title": "[TITLE]",
                        "image_url": "[IMG]",
                        "subtitle": "[SUBTITLE]",
                        "default_action": {
                            "type": "web_url",
                            "url": "[URL]",
                            "webview_height_ratio": "full"
                        },
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": "[URL]",
                                "title": "Xem tin ngay"
                            }
                        ]
                    },"""
    inside_cnt =""
    for row in main_row:
        tmp = inside_cnt_template.replace("[TITLE]",row.find('a').get('title'))
        tmp = tmp.replace("[URL]",row.find('a').get('href'))
        if row.find('img').get('src')[:4] == "http":
            tmp = tmp.replace("[IMG]",row.find('img').get('src'))
        else:
            tmp = tmp.replace("[IMG]", url+row.find('img').get('src'))

        tmp = tmp.replace("[SUBTITLE]",row.find('a').get('title'))
        inside_cnt += tmp

    message_str = message_str.replace("[CONTENT]",inside_cnt[:-1])

    message = json.loads(message_str)

    print(message)

def get_new_source():
    url = 'https://beta.dantri.com.vn/suc-khoe/nua-dem-bo-y-te-cong-bo-cung-luc-9-ca-mac-covid-19-moi-20200319211303006.htm'
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')

    main_row = soup.find("div", class_="dantri-widget dantri-widget--corona")

    print(main_row)
# get_new_source()
        # text = '🛑TRIỆU CHỨNG NHIỄM CORONA QUA TỪNG NGÀY'+'\n'+\
        #         '🔸Ngày 1 ~ Ngày 3'+'\n'+\
        #             '▪ Triệu chứng giống bệnh cảm'+'\n'+\
        #             '▪ Viêm họng nhẹ, hơi đau'+'\n'+\
        #             '▪ Không nóng sốt. Không mệt mỏi. Vẫn ăn uống bình thường'+'\n'+\
        #         '🔸Ngày 4'+'\n'+\
        #             '▪ Cổ họng đau nhẹ, người nôn nao.'+'\n'+\
        #             '▪ Bắt đầu khan tiếng.'+'\n'+\
        #             '▪ Nhiệt độ cơ thể dao động 36.5~ (tuỳ người)'+'\n'+\
        #             '▪ Bắt đầu chán ăn.'+'\n'+\
        #             '▪ Đau đầu nhẹ'+'\n'+\
        #             '▪ Tiêu chảy nhẹ'+'\n'+\
        #         '🔸Ngày 5'+'\n'+\
        #             '▪ Đau họng, khan tiếng hơn'+'\n'+\
        #             '▪ Cơ thể nóng nhẹ. Nhiệt độ từ 36.5~36.7'+'\n'+\
        #             '▪ Người mệt mỏi, cảm thấy đau khớp xương'+'\n'+\
        #             '** Giai đoạn này khó nhận ra là cảm hay là nhiễm corona'+'\n'+\
        #         '🔸Ngày 6'+'\n'+\
        #             '▪ Bắt đầu sốt nhẹ, khoảng 37'+'\n'+\
        #             '▪ Ho có đàm hoặc ho khan'+'\n'+\
        #             '▪ Đau họng khi ăn, nói hay nuốt nước bọt'+'\n'+\
        #             '▪ Mệt mỏi, buồn nôn'+'\n'+\
        #             '▪ Thỉnh thoảng khó khăn trong việc hít thở'+'\n'+\
        #             '▪ Lưng, ngón tay đau lâm râm'+'\n'+\
        #             '▪ Tiêu chảy, có thể nôn ói'+'\n'+\
        #         '🔸Ngày 7'+'\n'+\
        #             '▪ Sốt cao hơn từ 37.4~37.8'+'\n'+\
        #             '▪ Ho nhiều hơn, đàm nhiều hơn.'+'\n'+\
        #             '▪ Toàn thân đau nhức. Đầu nặng như đeo đá'+'\n'+\
        #             '▪ Tần suất khó thở vẫn như cũ.'+'\n'+\
        #             '▪ Tiêu chảy nhìu hơn'+'\n'+\
        #             '▪ Nôn ói'+'\n'+\
        #         '🔸Ngày 8'+'\n'+\
        #             '▪ Sốt gần mức 38 hoặc trên 38'+'\n'+\
        #             '▪ Khó thở hơn, mỗi khi hít thở cảm thấy nặng lồng ngực. Hơi thở khò khè'+'\n'+\
        #             '▪ Ho liên tục, đàm nhiều, tắt tiếng'+'\n'+\
        #             '▪ Đầu đau, khớp xương đau, lưng đau...'+'\n'+\
        #         '🔸Ngày 9'+'\n'+\
        #             '▪ Các triệu chứng không thay đổi mà trở nên nặng hơn.'+'\n'+\
        #             '▪ Sốt tăng giảm lộn xộn'+'\n'+\
        #             '▪ Ho không bớt mà nặng hơn trước.'+'\n'+\
        #             '▪ Dù cố gắng vẫn cảm thấy khó hít thở.'+'\n'+\
        #             '** Tại thời điểm này, nên đi xét nghiệm máu và chụp XQuang phổi để kiểm tra'+'\n'+\
        #         '🛑Chú ý:'+'\n'+\
        #         '▪ Thông tin để tham khảo.'+'\n'+\
        #         '▪ Triệu chứng thay đổi tuỳ theo sức đề kháng của từng người. Ai khoẻ thì mất 10-14 ngày mới phát hiện. Ai không khoẻ thì 4-5 ngày'


# def get_summary():
#     url = 'https://suckhoetoandan.vn/'
#     page = requests.get(url, verify=False)
#     soup = BeautifulSoup(page.text, 'html.parser')

#     main_row = soup.find_all("div",class_ ="box-heading")[1:]


#     # print(main_row)

#     all_of_it = "🛑 SỐ LIỆU ĐẾN HIỆN TẠI:\n"
#     all_of_it += "🌐 Toàn cầu:\n"

#     number = main_row[0].find_all("span",class_ = "box-total")
#     all_of_it += "Số người bị nhiễm: " + number[0].text + "\n"
#     all_of_it += "Số người tử vong: " + number[2].text+ "\n"
#     all_of_it += "Số người bình phục: " + number[4].text+ "\n"

#     all_of_it += "🇻🇳 Việt Nam:\n"

#     number = main_row[0].find_all("span", class_="box-total")
#     all_of_it += "Số người bị nhiễm: " + number[1].text + "\n"
#     all_of_it += "Số người tử vong: " + number[3].text + "\n"
#     all_of_it += "Số người bình phục: " + number[5].text + "\n"

#     all_of_it += "🛑 SỐ LƯỢNG TĂNG TRONG NGÀY:\n"
#     all_of_it += "🌐 Toàn cầu:\n"

#     number = main_row[1].find_all("span", class_="box-total")
#     all_of_it += "Số người bị nhiễm: " + number[0].text + "\n"
#     all_of_it += "Số người tử vong: " + number[2].text + "\n"
#     all_of_it += "Số người bình phục: " + number[4].text + "\n"

#     all_of_it += "🇻🇳 Việt Nam:\n"

#     number = main_row[1].find_all("span", class_="box-total")
#     all_of_it += "Số người bị nhiễm: " + number[1].text + "\n"
#     all_of_it += "Số người tử vong: " + number[3].text + "\n"
#     all_of_it += "Số người bình phục: " + number[5].text + "\n"

#     # print(all_of_it)
#     return all_of_it
# def get_hotline():
#     url = 'https://ncov.moh.gov.vn/documents/20182/6848000/Duongdaynong/'
#     page = requests.get(url, verify=False)
#     soup = BeautifulSoup(page.text, 'html.parser')
#     img  = soup.find_all("a")
#     print(page)
#     # return img

# get_hotline()