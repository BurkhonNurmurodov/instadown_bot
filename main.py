from telebot.async_telebot import AsyncTeleBot
from telebot import types
import instaloader
from config import *
import os
import asyncio
import lzma

L = instaloader.Instaloader()
L.load_session_from_file("mr_vampire_0207", "session-mr_vampire_0207") 

token = "5426802738:AAFwEeC4y73s3QFoUuIqrzciWVTbiD-2tc4"
bot = AsyncTeleBot(token)

@bot.message_handler(commands=["start"])
async def start(mess:types.Message):
    users = get_json("users.json")
    if not is_user(mess.chat.id):
        users.append(mess.chat.id)
    await bot.send_message(mess.chat.id, "Welecome to <b>Instagram Downloader Bot</b>", "html")
    await bot.send_message(mess.chat.id, "Send me a post link, which is you are going to download.")
    add_json("users.json", users)

@bot.message_handler(content_types=["text"])
async def worker(mess:types.Message):
    def get_code(url:str):
        url = url.split("/")
        return url[4]
    try:
        post = instaloader.Post.from_shortcode(L.context, get_code(mess.text))
        s_mess = await bot.send_message(mess.chat.id, "Downloading...")
        L.download_post(post, f"{mess.chat.id}")
        post_items = []
        for root, dirs, files in os.walk(f"{mess.chat.id}"):
            for file in files:
                if file.endswith(".mp4"):
                    try:
                        os.remove(f"{mess.chat.id}/{file[0: -3]+'jpg'}")
                    except:
                        pass
        caption = ""
        for root, dirs, files in os.walk(f"{mess.chat.id}"):
            for file in files:
                if file.endswith(".jpg"):
                    post_items.append(types.InputMediaPhoto(open(f"{mess.chat.id}/{file}", "rb")))
                elif file.endswith(".mp4"):
                    post_items.append(types.InputMediaVideo(open(f"{mess.chat.id}/{file}", "rb")))
                elif file.endswith(".xz"):
                    strobj = lzma.open(f'{mess.chat.id}/{file}', mode='rb').read()
                    with open(f"{mess.chat.id}/data.json", "wb") as json:
                        json.write(strobj)
                    caption = get_text(str(mess.chat.id))
                
        post_items[0].caption = str(caption) + "\n\n⬇️ Downloaded by <a href='https://t.me/Insta_Downloader_0207_bot'>📸 Instagram Downloader Bot</a>"
        post_items[0].parse_mode = "html"
        await bot.delete_message(mess.chat.id, s_mess.message_id)
        try:
            await bot.send_media_group(mess.chat.id, post_items)
        except:
            await bot.send_message(mess.chat.id, "Sorry, something went wrong. Please try again later.")
        for root, dirs, files in os.walk(str(mess.chat.id)):
            for file in files:
                os.unlink(os.path.join(root, file))
        for root, dirs, files in os.walk(str(mess.chat.id)):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(str(mess.chat.id))
    except:
        await bot.send_message(mess.chat.id, "Invalid post link.")

asyncio.run(bot.infinity_polling())
