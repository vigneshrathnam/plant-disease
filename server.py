from bot import telegram_chatbot
import predict
bot = telegram_chatbot("./config/config.cfg")
from classes import class_names

def make_reply(msg,photo,user_msg):
    """ Send reply to the user"""
    
    reply = None
    if photo is not None:
        url,ext,size=bot.get_photo_url(photo["file_id"])
        print(url,ext,size)
        if ext not in ['.jpeg','.jpg','.png']:
            reply = """Accepted formats are <b>JPEG/JPG,PNG</b>
            Please try to send the file with current format"""
        elif size > 1024*1024:
            reply = "Uploaded file must be 1MB or less."
        else:
            reply = predict.predict_model(url)
    elif 'help' in user_msg.lower():
        reply=""" <b>Upload an Image</b> to Predict:\n
            <b>(*)</b> Accepts one image per prediction
            <b>(*)</b> Sending Multiple files will be Ignored
            <b>(*)</b> Sending Image as a File will not be Accepted as of now
            <b>(*)</b> Accepted formats are JPEG/JPG,PNG
            <b>(*)</b> This bot can currently Predict 38 classes of diseases of plants
                including healthy ones.
            <b>(*)</b> Out of which 14 classes are healthy while others are unhealthy
            <b>(*)</b> There are total of 10 plants to be classified.
            <b>(*)</b> Uploaded file must be 1MB or less.
        User must satisfy the following conditions to get the prediction.
        """
    elif 'list' in user_msg.lower():
        msg = "<b>List of classes can be predicted:</b>\n\n"
        index = 1
        for cls in class_names:
            msg+="<b>{}.</b> {}\n".format(index,cls.replace("_"," ").strip())
            index+=1
        reply=msg
    else:
        reply=msg
    return reply

update_id = None

 # loop runs for every 100 seconds
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
                message = "Upload a Photo to classify the disease"
                photo = None
            try:
                user_msg = item["message"]["text"]
            except KeyError:
                user_msg = ''
            print(photo)
            try:
                from_ = item["message"]["from"]["id"]
            except:
                from_ = None
            if from_:
                reply = make_reply(message,photo,user_msg)
                bot.send_message(reply, from_)
            