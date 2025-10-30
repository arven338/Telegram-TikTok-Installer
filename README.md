# Telegram-TikTok-Installer
🌴 Telegram-bot for installing videos from TikTok platform using a url 📱

## Features
- Download TikTok videos directly in Telegram
- Simple URL-based interface
- Automatic video cleanup after sending
- 24/7 server availability

## Setup instructions

### Prerequisites
- Python 3.11+
- Telegram-bot API (from 👉 @BotFather)
- Deployment platform

### Environment Variables
Set the following environment variable:
```env
api_key=YOUR_TELEGRAM_BOT_API_KEY
```

### Installation
1. Clone this repitisory:
   ```bash
   git clone https://github.com/arven338/Telegram-TikTok-Installer.git
   cd Telegram-TikTok-Installer
   ```
2. Install librares:
   ```shell
   pip install -r requirements.txt
   ```
3. Launch the bot:
   ```shell
   python launch.py
   ```

### Deployment
**Method 1**: Using Docker
```bash
docker build -t telegram-tiktok-bot .
docker run -e api_key=YOUR_BOT_API_KEY telegram-tiktok-bot
```
**Method 2**: Using start.sh
```bash
chmod +x start.sh
./start.sh
```

## Usage
1. Start a conservation with your bot on Telegram.
2. Send <code>/start</code> to see the welcome message.
3. Send any TikTok video URL to download and receive the video directly in Telegram

## Libraries
- **telebot** - Telegram API client.
- **yt-dlp** - Video installer
- **Flask** - Web framework for keeping the bot alive.
- **gunicorn** - WSGI HTTP server for production

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request 🥥.
