  
#Python libraries that we need to import for our bot
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import random
from flask import Flask, request, Response
from pymessenger.bot import Bot
from wit import Wit
import requests
import random
import pathlib
import os
from bs4 import BeautifulSoup
import urllib.request
import ssl
import json
import csv
import logging
from requests.exceptions import ConnectionError
app = Flask(__name__)
# ACCESS_TOKEN = 'ACCESS_TOKEN'
ACCESS_TOKEN = 'EAAIbv66Rh8wBAPIKp9fYSZCDO7KbJI19Ydjr33Q8MZBcclyDxZCyQKgAwqDb00qu01LfyUO1MuFtrhoQQr93yfjt177DaJkhZAZABBDxAP55T92nYVX963ZCMoOo1uqL6v6sUQmNBviX95rVwUcw7EFVSjshNkVxsCdDlOyp98wAQKc5IiMtDX'
VERIFY_TOKEN = 'VERIFY_TOKEN'
WIT_TOKEN    = '6OGZVMSELXTJM5HVSWH2IRBRRMLNGKGK'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/webhook", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        """
        Handler for webhook (currently for postback and messages)
        """
        data = request.json
        if data['object'] == 'page':
            for entry in data['entry']:
                # get all the messages
                messages = entry['messaging']
                # print('message: ', messages)
                if messages[0]:
                    # Get the first message
                    message = messages[0]
                    # Yay! We got a new message!
                    # We retrieve the Facebook user ID of the sender
            
                    fb_id = message['sender']['id']
                    print('fb_id :', fb_id)
                    # We retrieve the message content
                    text = message['message']['text']
                    print('text:', text)
                    # Let's forward the message to Wit /message
                    # and customize our response to the message in handle_message
                    response = client.message(text)
                    # response ={'text': 'hello bot', 'intents': [{'id': '742387059668438', 'name': 'greating', 'confidence': 0.9787}], 'entities': {}, 'traits': {'wit$greetings': [{'id': '5900cc2d-41b7-45b2-b21f-b950d3ae3c5c', 'value': 'true', 'confidence': 0.9997}]}}
                    handle_message(response=response, fb_id=fb_id)
        else:

            return 'Received Different Event'
    return 'Message Processed!!!'


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + ACCESS_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    return resp.content

# def first_trait_value(traits, trait):
#     """
#     Returns first trait value
#     """
#     if trait not in traits:
#         return None
#     val = traits[trait][0]['value']
#     if not val:
#         return None
#     return val
def first_entity_value(entities, entity):
    """
    Returns first trait value
    """
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val
    # return val['value'] if isinstance(val, dict) else val  

def handle_message(response, fb_id):
    """
    Customizes our response to the message and sends it
    """

    text = 'Xin lỗi, mình chưa hiểu ý của bạn !'

    entities = response['entities']
    greetings = first_entity_value(entities, 'greetings:greetings')
    cuss=first_entity_value(entities, 'cuss:cuss')
    thanks=first_entity_value(entities, "thanks:thanks")
    bye = first_entity_value(entities, "bye:bye")
    good = first_entity_value(entities, "good:good")
    info_name = first_entity_value(entities, "info_name:info_name")
    info_age = first_entity_value(entities, "info_age:info_age")
    tutorial = first_entity_value( entities, "tutorial:tutorial")
    info_covid = first_entity_value( entities, "info_covid:info_covid")
    hotline = first_entity_value( entities, "hotline:hotline")
    symptom = first_entity_value(entities, "symptom:symptom")
    summary = first_entity_value(entities, "summary:summary")
    protect = first_entity_value( entities, "protect:protect")
    indentify = first_entity_value(entities, "indentify:indentify")
    sentiment = first_entity_value( entities, "sentiment:sentiment")
    if greetings:
        sample_responses = ["Chào bạn, tôi có thể giúp gì cho bạn.",
                            "Mình là trợ lí ảo Covid-19, mình giúp gì được cho bạn",
                            "hello ",
                            "rất hân hạnh được làm quen với bạn",
                            "hi",
                            "xin chào",
                            "Cứ nói đi đừng sợ"]
        
        text = random.choice(sample_responses)
    elif cuss:
        sample_responses = ["Sao lại chửi mình!",
                            "Bạn nói vậy mình đau lòng lắm!, bạn có gì muốn hỏi nữa không?",
                            "Nè, hơi mất dạy đấy!Có tin tui kêu công an bắt không"]
        text = random.choice(sample_responses)
    elif thanks:
        sample_responses = ['Cảm ơn bạn đã nhắn tin với mình, nhớ hỏi thăm mình thường xuyên nhé!',
                            "Cảm ơn bạn rất nhiều, nhớ ghé thăm mình nhé.",
                            "Bạn có biết mình dui lắm không?",
                            "Dù biết chắc là nói dối nhưng vẫn cảm ơn",
                            "Thanks"]
        text = random.choice(sample_responses)
    elif bye:
        sample_responses = ['Bye bạn, chúc bạn 1 ngày vui vẻ',
                            'Bye, chắc bạn sẽ không quay lại nữa đâu!',
                            'Bye',
                            'Đừng đi mà !!'
                            'Tạm biệt nhé']
        text = random.choice(sample_responses)
    elif good:
        sample_responses = ['Bạn quá khen',
                            'Khen vừa thôi, có biết người ta vui lắm không',
                            'Chuyện bình thường mà',
                            'Đơn giản vì tôi có ông chủ giỏi']
        text = random.choice(sample_responses)
    elif info_name:
        text = 'Em tên bé Bô ạ!'
    elif info_age:
        text = 'Dạ em năm nay vừa tròn 1 tuổi'
    elif info_covid:
        sample_responses = ['Vi rút Corona là một họ vi rút lớn được tìm thấy ở cả động vật và người. Một số vi rút có thể gây bệnh cho người từ cảm lạnh thông thường đến các bệnh nghiêm trọng hơn như Hội chứng hô hấp Trung Đông (MERS) và Hội chứng hô hấp cấp tính nặng (SARS).',
                            'Vi rút Corona mới là một chủng mới của vi rút Corona chưa từng xác định được ở người trước đây. Vi rút mới này hiện gọi là 2019-nCoV, chưa từng được phát hiện trước khi dịch bệnh được báo cáo tại Vũ Hán, Trung Quốc vào tháng 12 năm 2019. Đây là một loại vi rút đường hô hấp mới gây bệnh viêm đường hô hấp cấp ở người và cho thấy có sự lây lan từ người sang người. Vi rút mới này cùng họ với vi rút gây Hội chứng hô hấp cấp tính nặng (SARS-CoV) nhưng không phải là cùng một vi rút.']
        text = random.choice(sample_responses)
    elif sentiment:
        text = " Bạn nên liên hệ hotline để được tư vấn và hỗ trợ kịp thời nhất (19009095 / 19003228)"
    elif tutorial:
        text = get_tutorial()
    elif summary:
        text = get_summary()
    elif hotline:
        text  = get_hotline()
    elif symptom:
        text  = get_symptom()
    elif protect:
        text  = get_protect()
    elif indentify:
        text  = get_indentify()
    # else:

    #     text = "We've received your message: " + response['text']

    # send message
    fb_message(fb_id, text)

def get_summary():
    all_of_it=""
    try:
        # all_of_it = 'https://suckhoetoandan.vn/'
        url = 'https://suckhoetoandan.vn/'
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')

        main_row = soup.find_all("div",class_ ="box-heading")[1:]
        # print(main_row)
        all_of_it += "🛑 SỐ LIỆU ĐẾN HIỆN TẠI:\n"
        all_of_it += "🌐 Toàn cầu:\n"

        number = main_row[0].find_all("span",class_ = "box-total")
        all_of_it += "Số người bị nhiễm: " + number[0].text + "\n"
        all_of_it += "Số người tử vong: " + number[2].text+ "\n"
        all_of_it += "Số người bình phục: " + number[4].text+ "\n"

        all_of_it += "🇻🇳 Việt Nam:\n"

        number = main_row[0].find_all("span", class_="box-total")
        all_of_it += "Số người bị nhiễm: " + number[1].text + "\n"
        all_of_it += "Số người tử vong: " + number[3].text + "\n"
        all_of_it += "Số người bình phục: " + number[5].text + "\n"

        all_of_it += "🛑 SỐ LƯỢNG TĂNG TRONG NGÀY:\n"
        all_of_it += "🌐 Toàn cầu:\n"

        number = main_row[1].find_all("span", class_="box-total")
        all_of_it += "Số người bị nhiễm: " + number[0].text + "\n"
        all_of_it += "Số người tử vong: " + number[2].text + "\n"
        all_of_it += "Số người bình phục: " + number[4].text + "\n"

        all_of_it += "🇻🇳 Việt Nam:\n"

        number = main_row[1].find_all("span", class_="box-total")
        all_of_it += "Số người bị nhiễm: " + number[1].text + "\n"
        all_of_it += "Số người tử vong: " + number[3].text + "\n"
        all_of_it += "Số người bình phục: " + number[5].text + "\n"

        # print(all_of_it)
    except ConnectionError as e:
        all_of_it += 'error connect url'
    return all_of_it

def get_hotline():
    try:
        text = '🛑 Khi cần tư vấn hỗ trợ hoặc khám bệnh, bạn có thể liên hệ các số điện thoại dưới đây:'+'\n'+\
                    '🔸 Bệnh viện Bạch Mai: 0969.851.616'+'\n'+\
                    '🔸 Bệnh viện Nhiệt đới Trung ương: 0969.241.616'+'\n'+\
                    '🔸 Bệnh viện E: 0912.168.887'+'\n'+\
                    '🔸 Bệnh viện Nhi trung ương: 0372.884.712'+'\n'+\
                    '🔸 Bệnh viện Phổi trung ương: 0967.941.616'+'\n'+\
                    '🔸 Bệnh viện Việt Nam - Thụy Điển Uông Bí: 0966.681.313'+'\n'+\
                    '🔸 Bệnh viện Đa khoa trung ương Thái Nguyên: 0913.394.495'+'\n'+\
                    '🔸 Bệnh viện Trung ương Huế: 0965.301.212'+'\n'+\
                    '🔸 Bệnh viện Chợ Rẫy: 0969.871.010'+'\n'+\
                    '🔸 Bệnh viện Đa khoa trung ương Cần Thơ: 0907.736.736'+'\n'+\
                    '🔸 Bệnh viện Xanh Pôn Hà Nội: 0904.138.502'+'\n'+\
                    '🔸 Bệnh viện Vinmec Hà Nội: 0934.472.768'+'\n'+\
                    '🔸 Bệnh viện Đà Nẵng: 0903.583.881'+'\n'+\
                    '🔸 Bệnh viện Nhiệt đới TP.HCM: 0967.341.010'+'\n'+\
                    '🔸 Bệnh viện Nhi đồng 1: 0913.117.965'+'\n'+\
                    '🔸 Bệnh viện Nhi đồng 2: 0798.429.841'+'\n'+\
                    '🔸 Bệnh viện Đa khoa tỉnh Đồng Nai: 0819.634.807'+'\n'+\
                    '🔸 Bệnh viện Nhiệt đới Khánh Hòa: 0913.464.257'+'\n'+\
                    '🔸 Bệnh viện tỉnh Khánh Hòa: 0965.371.515'+'\n'+\
                    '🔸 Bệnh viện tỉnh Thái Bình: 0989.506.515'+'\n'+\
                    '🔸 Bệnh viện tỉnh Lạng Sơn: 0396.802.226.'
        return text
    except ConnectionError as e:
        return 'Đường dây nóng: 19009095 / 19003228'

def get_symptom():
    try:
        text = '🛑TRIỆU CHỨNG NHIỄM CORONA QUA TỪNG NGÀY'+'\n'+\
                '🔸Ngày 1 ~ Ngày 3'+'\n'+\
                    '▪ Triệu chứng giống bệnh cảm'+'\n'+\
                    '▪ Viêm họng nhẹ, hơi đau'+'\n'+\
                    '▪ Không nóng sốt. Không mệt mỏi. Vẫn ăn uống bình thường'+'\n'+\
                '🔸Ngày 4'+'\n'+\
                    '▪ Cổ họng đau nhẹ, người nôn nao.'+'\n'+\
                    '▪ Bắt đầu khan tiếng.'+'\n'+\
                    '▪ Nhiệt độ cơ thể dao động 36.5~ (tuỳ người)'+'\n'+\
                    '▪ Bắt đầu chán ăn.'+'\n'+\
                    '▪ Đau đầu nhẹ'+'\n'+\
                    '▪ Tiêu chảy nhẹ'+'\n'+\
                '🔸Ngày 5'+'\n'+\
                    '▪ Đau họng, khan tiếng hơn'+'\n'+\
                    '▪ Cơ thể nóng nhẹ. Nhiệt độ từ 36.5~36.7'+'\n'+\
                    '▪ Người mệt mỏi, cảm thấy đau khớp xương'+'\n'+\
                    '** Giai đoạn này khó nhận ra là cảm hay là nhiễm corona'+'\n'+\
                '🔸Ngày 6'+'\n'+\
                    '▪ Bắt đầu sốt nhẹ, khoảng 37'+'\n'+\
                    '▪ Ho có đàm hoặc ho khan'+'\n'+\
                    '▪ Đau họng khi ăn, nói hay nuốt nước bọt'+'\n'+\
                    '▪ Mệt mỏi, buồn nôn'+'\n'+\
                    '▪ Thỉnh thoảng khó khăn trong việc hít thở'+'\n'+\
                    '▪ Lưng, ngón tay đau lâm râm'+'\n'+\
                    '▪ Tiêu chảy, có thể nôn ói'+'\n'+\
                '🔸Ngày 7'+'\n'+\
                    '▪ Sốt cao hơn từ 37.4~37.8'+'\n'+\
                    '▪ Ho nhiều hơn, đàm nhiều hơn.'+'\n'+\
                    '▪ Toàn thân đau nhức. Đầu nặng như đeo đá'+'\n'+\
                    '▪ Tần suất khó thở vẫn như cũ.'+'\n'+\
                    '▪ Tiêu chảy nhìu hơn'+'\n'+\
                    '▪ Nôn ói'+'\n'+\
                '🔸Ngày 8'+'\n'+\
                    '▪ Sốt gần mức 38 hoặc trên 38'+'\n'+\
                    '▪ Khó thở hơn, mỗi khi hít thở cảm thấy nặng lồng ngực. Hơi thở khò khè'+'\n'+\
                    '▪ Ho liên tục, đàm nhiều, tắt tiếng'+'\n'+\
                    '▪ Đầu đau, khớp xương đau, lưng đau...'+'\n'+\
                '🔸Ngày 9'+'\n'+\
                    '▪ Các triệu chứng không thay đổi mà trở nên nặng hơn.'+'\n'+\
                    '▪ Sốt tăng giảm lộn xộn'+'\n'+\
                    '▪ Ho không bớt mà nặng hơn trước.'+'\n'+\
                    '▪ Dù cố gắng vẫn cảm thấy khó hít thở.'+'\n'+\
                    '** Tại thời điểm này, nên đi xét nghiệm máu và chụp XQuang phổi để kiểm tra'+'\n'+\
                '🛑Chú ý:'+'\n'+\
                    '▪ Thông tin để tham khảo.'+'\n'+\
                    '▪ Triệu chứng thay đổi tuỳ theo sức đề kháng của từng người. Ai khoẻ thì mất 10-14 ngày mới phát hiện. Ai không khoẻ thì 4-5 ngày.'
        return text
    except ConnectionError as e:
        return 'Ho, nhức đầu!!'
def get_tutorial():
    try:
        text =  '📨Em chuyên hổ trợ, cung cấp thông tin'+'\n'+\
                '📣 Diễn biến mới nhất Covid tại VN và thế giới'+'\n'+\
                '😰 Triệu chứng COVID-19'+'\n'+\
                '✍ Khai báo y tế'+'\n'+\
                '📞 Đường dây nóng'+'\n'+\
                '🇻🇳Tình hình các tỉnh thành.'
        return text
    except ConnectionError as e:
        return 'Tự tìm hiểu đi bạn'
def get_protect():
    try:
        text =  '🛑 Rửa tay: thường xuyên bằng dung dịch chứa cồn, xà phòng, nước'+'\n'+\
                '🛑 Khử trùng bề mặt'+'\n'+\
                '🛑 Tránh đi lại nơi đông người'+'\n'+\
                '🛑 Nếu không khỏe thì ở nhà và liên hệ bác sĩ'+'\n'+\
                '🛑 Cài đặt ứng dụng Bluezone.'
        return text
    except ConnectionError as e:
        return 'Tự tìm hiểu đi bạn'

def get_indentify():
    try:
        url = 'https://tokhaiyte.vn/m/?page=Mobile.Declare.home'
        return url

    except ConnectionError as e:
        return 'Lên mạng search đi'
@app.route("/", methods=['GET', 'POST'])
def show():
    return 'show bot ngu qua!!!!!!!'

# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)
# client.interactive()
# client.logger.setLevel(logging.WARNING)
resp = client.message('tin tức')
print('Yay, got Wit.ai response: ' + str(resp))
response = resp
entities = response['entities']
print('1111111111111',entities)
print('2222222222',entities['summary:summary'][0]['value'])

if __name__ == "__main__":
    app.run(debug= True)