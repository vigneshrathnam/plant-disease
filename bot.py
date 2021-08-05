import requests
import json
import configparser as cfg
import os


class telegram_chatbot():
    """This Model is used to have communication between the server and Telegram messenger"""
    
    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        """Checks for message Updates by the user for every 100 seconds."""
        
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        """This function is used to send message to the telegram"""
        
        url = self.base + "sendMessage?chat_id={}&text={}&parse_mode=html".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_token_from_config_file(self, config):
        """Read the API token from the \"./config/config.cfg\" file"""
        
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
    
    def get_photo_url(self,file_id):
        """Get the photo URL of the Image uploaded in messenger
                Example: https://api.telegram.org/bot{API_TOKEN}/getFile?file_id=1
                returns (URL of file,Extention of File,Size of the file)
        """
        
        url=self.base+"getFile?file_id="+file_id
        res=requests.get(url).content
        content=json.loads(res)
        print(content)

        file_path=content["result"]["file_path"]
        ext = os.path.splitext(file_path)[1]
        size = content["result"]["file_size"]
        
        photo_url="https://api.telegram.org/file/bot{}/{}".format(self.token,file_path)
        return (photo_url,ext,size)