from configparser import ConfigParser
from telethon import TelegramClient, events, sync

config_url="./config/config2.cfg"
cfg=ConfigParser()
cfg.read(config_url)
api_id = cfg.get("creds","api_id")
api_hash = cfg.get("creds","api_hash")

client = TelegramClient('session_name', api_id, api_hash)
client.start()

print(client.get_me().stringify())

client.send_message('BotFather', 'Hello! Talking to you from Telethon')
client.send_file('BotFather',r"C:\Users\8TIN\Downloads\apple black rot.jpg")

client.download_profile_photo('me')
messages = client.get_messages('BotFather')
messages[0].download_media()

@client.on(events.NewMessage(pattern='(?i)hi|hello'))
async def handler(event):
    await event.respond('Hey!')