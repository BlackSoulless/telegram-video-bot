from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import yt_dlp

def start(update, context):
    user_first_name = update.effective_user.first_name
    keyboard = [
        ["📥 İndir", "ℹ️ Yardım"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(
        f"Merhaba {user_first_name}! Link gönder, video veya sesi indireyim.\n\n"
        "Butonlardan işlem seçebilirsin.",
        reply_markup=reply_markup
    )

def handle_buttons(update, context):
    text = update.message.text
    if text == "📥 İndir":
        update.message.reply_text("Lütfen video veya ses linkini gönder.")
    elif text == "ℹ️ Yardım":
        update.message.reply_text("Bu bot video ve ses linklerini indirir. Link gönder yeter!")

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def handle_message(update, context):
    url = update.message.text
    # Eğer buton mesajı değilse (link olabilir)
    if url not in ["📥 İndir", "ℹ️ Yardım"]:
        update.message.reply_text("İndiriliyor, lütfen bekle...")
        try:
            filepath = download_video(url)
            with open(filepath, 'rb') as video:
                update.message.reply_video(video)
            os.remove(filepath)
        except Exception as e:
            update.message.reply_text(f"Hata oluştu: {e}")

def main():
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex("^(📥 İndir|ℹ️ Yardım)$"), handle_buttons))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

