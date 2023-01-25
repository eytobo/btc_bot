from bs4 import BeautifulSoup
from datetime import datetime
import requests
import schedule
import datetime
import json
import time

def bot_send_text():
    requester_id = get_last_message()[0]['chat']['user_id']
    bot_message = f'Hola, el precio de Bitcoin es: {btc_scraping()}'
    bot_token = '5851070038:AAFRL_6ez9bUMZocOsRtHII6kTHgbzvvajE'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + requester_id + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response

def btc_scraping():
    url = requests.get('https://btcdirect.eu/es-es/precio-bitcoin')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('div', { 'class': 'text-nowrap price coin-ticker'})
    format_result = result.text
    print(format_result)
    return 'fadsf'
    return format_result

def get_users_messages():
  data_json = requests.get('https://api.telegram.org/bot5851070038:AAFRL_6ez9bUMZocOsRtHII6kTHgbzvvajE/getUpdates').text
  data_dic = json.loads(data_json)
  chats = data_dic['result']
  users_messages = []
  for chat in range(len(chats)):
    try:
      user_id = str(chats[chat]['message']['from']['id'])
      date = chats[chat]['message']['date']
      message = chats[chat]['message']['text']
      if message == '/btc_price':
        users_messages.append({'chat': {'user_id': user_id, 'date': date, 'message': message}})
    except:
      continue
  return users_messages

def get_last_message():
    messages = get_users_messages()
    messages_date = []
    users_messages = get_users_messages()
    for index in range(len(messages)):
        message = users_messages[index]['chat']['date']
        messages_date.append(message)
    last_message_date = max(messages_date)
    return [messages[i] for i in range(len(messages)) if messages[i]['chat']['date'] == last_message_date]

if __name__ == '__main__':
    past_len = 0
    act_len = 0
    while True:
        messages = get_users_messages()
        act_len = len(messages)
        if act_len > past_len:
            bot_send_text()
            print('Send!!')
            past_len = len(messages)
        else:
            print('Waiting...')
