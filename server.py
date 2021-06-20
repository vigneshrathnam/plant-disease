from bot import telegram_chatbot
import predict
bot = telegram_chatbot("./config/config.cfg")


def make_reply(msg,photo):
    reply = None
    if photo is not None:
        url=bot.get_photo_url(photo["file_id"])
        reply = predict.predict_model(url)
    else:
        reply=msg
    return reply

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    print(updates)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                photo = item["message"]["photo"][0]
                message=None
            except:
                message = "Send a Photo to classify disease"
                photo = None
            print(photo)
            from_ = item["message"]["from"]["id"]
            reply = make_reply(message,photo)
            bot.send_message(reply, from_)