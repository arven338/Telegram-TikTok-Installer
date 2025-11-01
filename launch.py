# Import librares.  
import threading  
import telebot # Telegram client.  
from yt_dlp import YoutubeDL # Video. installer.  
import os # For video cache.  
from flask import Flask # For alive.  
import requests  # For resolving short TikTok URLs
  
# Telegram-bot client.  
bot = telebot.TeleBot(os.environ.get("api_key"))  
  
# == Parameters ==  
ydl_opts = {  
    'format': 'best',  
    'outtmpl': 'downloaded_video.%(ext)s',  
    'quiet': True,  
    'no_warnings': True,  
}  
  
# Server client.
app = Flask('')  
  
@app.route('/')  
def home():  
    return "Server alive!"  
  
def run():  
    app.run(host='0.0.0.0', port=7678)  
  
def keep_alive():   
    t = threading.Thread(target=run)  
    t.daemon = True  
    t.start()  
  
# Start command.  
@bot.message_handler(commands=['start'])  
def start_message(message):  
    first_name = message.from_user.first_name or ""  
    last_name = message.from_user.last_name or ""  
      
    bot.send_message(message.chat.id, f"Привет {first_name} {last_name}! 👋\n\n"
                                      "Это Telegram-Бот для скачивания видео с TikTok прямо в Telegram!\n"
                                      "Просто отправь ссылку на видео — и Telegram-бот всё сделает 🎥")  
  
# Handler for any message.  
@bot.message_handler(func=lambda message: True)  
def handle_message(message):  
    url = message.text.strip()  
      
    if 'tiktok.com' not in url:  
        bot.send_message(message.chat.id, "Пожалуйста, отправь ссылку именно с TikTok 📱")  
        return  
      
    msg = bot.send_message(message.chat.id, "⏳ Видео загружается, подожди немного...")  

    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        if response.url and 'tiktok.com' in response.url:
            url = response.url
    except Exception as e:
        print(f"[ WARN ] Failed to expand short link: {e}")
    
    try:  
        with YoutubeDL(ydl_opts) as ydl:  
            info = ydl.extract_info(url, download=True)  
            video_filename = ydl.prepare_filename(info)  
  
        with open(video_filename, 'rb') as video:  
            bot.send_video(message.chat.id, video)  
  
        if os.path.exists(video_filename):  
            os.remove(video_filename)  
  
        try:  
            bot.edit_message_text("✅ Видео успешно скачано и отправлено!", message.chat.id, msg.message_id)  
        except:  
            pass  
  
    except Exception as e:  
        print(f"[ FAILED ] {e}")
        try:  
            bot.edit_message_text("❌ Упс... Не удалось скачать видео. Попробуй чуть позже.", message.chat.id, msg.message_id)  
        except:  
            bot.send_message(message.chat.id, "❌ Упс... Не удалось скачать видео. Попробуй чуть позже.")  
  
# App launch.
if __name__ == "__main__":  
    keep_alive()  
    print("Bot started...")  
    bot.polling(none_stop=True, interval=0, timeout=20)
