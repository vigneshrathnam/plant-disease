import requests
import json
import configparser as cfg


class telegram_chatbot():

    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
    
    def get_photo_url(self,file_id):
        url=self.base+"getFile?file_id="+file_id
        res=requests.get(url).content
        content=json.loads(res)
        print(file_id)
        file_path=content["result"]["file_path"]
        photo_url="https://api.telegram.org/file/bot{}/{}".format(self.token,file_path)
        return photo_url