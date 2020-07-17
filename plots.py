import requests
import datetime
from googleapiclient.discovery import build
import random

DEVELOPER_KEY = 'AIzaSyAGRSWOtvBl31fHHZS8CG7gRBeZDyxDo_E'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

prefix = ['IMG ', 'IMG_', 'IMG-', 'DSC ']
postfix = [' MOV', '.MOV', ' .MOV']

def youtube_search():
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=random.choice(prefix) + str(random.randint(999, 9999)) + random.choice(postfix),
    part='snippet',
    maxResults=5
  ).execute()

  videos = []

  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append('%s' % (search_result['id']['videoId']))
  return (videos[random.randint(0, 2)])


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def get_mess(self, update):
        message = update['message']['text']
        return message

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

greet_bot = BotHandler("1092200670:AAEiRT250PQBeyYPAVAn_2nmHIZxqijiyyE")
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.isoweekday()
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']


        if today == 3:
            greet_bot.send_message(last_chat_id, "https://www.youtube.com/watch?v=Oct2xKMGOno")
            today += 1

        if last_chat_text.lower() == "random":
            greet_bot.send_message(last_chat_id, "https://www.youtube.com/watch?v={}".format(youtube_search()))
        else: greet_bot.send_message(last_chat_id, "Try type random")
        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()



