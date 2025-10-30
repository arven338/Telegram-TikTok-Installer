# Import librares
import threading
import telebot # Telegram client
from yt_dlp import YoutubeDL # Video installer
import os # For video cache
from flask import Flask # For alive

# Telegram-bot client
bot = telebot.TeleBot(os.environ.get("api_key"))

# == Parameters ==
ydl_opts = {
    'format': 'best',
    'outtmpl': 'downloaded_video.%(ext)s',
    'quiet': True,
    'no_warnings': True,
}

# Server client
app = Flask('')

@app.route('/')
def home():
    return "Server alive!"

def run():
    app.run(host='0.0.0.0', port=7678)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# Start command
@bot.message_handler(commands=['start'])
def start_message(message):
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name
    bot.send_message(message.chat.id, f" Привет {first_name} {last_name}! \n \n Это Telegram-Бот для скачивания видео с TikTok прямо в Telegram! Просто кинь ссылку на видео, и Бот - Загрузит.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    
    # Checking a TikTok url:
    if 'tiktok.com' not in url:
        bot.send_message(message.chat.id, " Пожалуйста, отправь ссылку именно с TikTok.")
        return
    
    msg = bot.send_message(message.chat.id, " Видео скачиваеться...")
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info)
        
        with open(video_filename, 'rb') as video:
            bot.send_video(message.chat.id, video)
        
        os.remove(video_filename) # Deleting video in disc
        bot.edit_message_text("Видео успешно скачано и отправлено ✅!", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text("Упсс... Не удалось скачать видео с платформы. Попробуйте чуть позже.", message.chat.id, msg.message_id)

if __name__ == "__main__":
  keep_alive()
  bot.polling()
