import os
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ✅ Telegram API ma'lumotlari
API_ID = 25395049  # O'zingizning API_ID ni kiriting
API_HASH = "f967e09ec0a096ffbf948690d4bf4070"  # O'zingizning API_HASH ni kiriting
BOT_TOKEN = "7879165433:AAHLL72NZdnPJa_DOaJzbVKCWRdxGPPNk2o"  # O'zingizning BOT_TOKEN ni kiriting

# 🔥 Video formatlari ro‘yxati
VIDEO_FORMATS = {
    "128p": "worst",
    "360p": "best[height<=360]",
    "720p": "best[height<=720]",
    "1080p": "best[height<=1080]",
    "2K": "best[height<=1440]",
    "4K": "best[height<=2160]"
}

# 📝 YouTube video yuklash funksiyasi
def download_youtube_video(url, format_code):
    ydl_opts = {
        'format': format_code,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'geo_bypass': True,
        'age_limit': 0,
        'merge_output_format': 'mp4',
        'cookies_from_browser': ('chrome',)  # 🔑 Chrome-dan cookie-larni avtomatik olish
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info), info.get('title', 'video')

# 🚀 Telegram botni ishga tushirish
app = Client("youtube_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🔥 Start komandasi
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text(
        "👋 Salom! Men YouTube-dan video yuklab beruvchi botman.\n\n"
        "🎥 Video yuklab olish uchun menga YouTube havolasini yuboring.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Dasturchi", url="https://t.me/yourusername")]
        ])
    )

# 📩 YouTube havolasini qabul qilish va format tanlash
@app.on_message(filters.text & filters.regex(r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"))
def youtube_format_selection(client, message):
    url = message.text
    buttons = [
        [InlineKeyboardButton("🎬 128p", callback_data=f"download|{url}|128p")],
        [InlineKeyboardButton("🎬 360p", callback_data=f"download|{url}|360p")],
        [InlineKeyboardButton("🎬 720p HD", callback_data=f"download|{url}|720p")],
        [InlineKeyboardButton("🎬 1080p Full HD", callback_data=f"download|{url}|1080p")],
        [InlineKeyboardButton("🎬 2K", callback_data=f"download|{url}|2K")],
        [InlineKeyboardButton("🎬 4K Ultra HD", callback_data=f"download|{url}|4K")]
    ]
    message.reply_text("🔽 Yuklab olmoqchi bo‘lgan formatni tanlang:", reply_markup=InlineKeyboardMarkup(buttons))

# 📥 Video yuklab olish
@app.on_callback_query(filters.regex(r"^download\|(.+)\|(.+)$"))
def youtube_download(client, query: CallbackQuery):
    _, url, format_choice = query.data.split("|")
    format_code = VIDEO_FORMATS.get(format_choice, "best")

    query.message.reply_text(f"📥 *{format_choice} formatida yuklab olinmoqda...*")

    try:
        file_path, title = download_youtube_video(url, format_code)
        caption = f"📹 *{title}* - {format_choice}"

        with open(file_path, "rb") as file:
            client.send_video(query.message.chat.id, file, caption=caption)

        os.remove(file_path)
        query.message.reply_text("✅ Video yuklab olindi!")
    except Exception as e:
        query.message.reply_text(f"❌ Xatolik yuz berdi: {str(e)}")

# 🔥 Botni ishga tushirish
if name == "__main__":
    app.run()
