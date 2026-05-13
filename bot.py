import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-lite')

async def start(update: Update, context):
    await update.message.reply_text("🤖 হ্যালো! আমি কোগিটোন বট। আপনার প্রশ্নের উত্তর দিতে প্রস্তুত!")

async def handle_message(update: Update, context):
    user_msg = update.message.text
    await update.message.reply_text("🤔 চিন্তা করছি...")
    
    try:
        response = model.generate_content(user_msg)
        reply = response.text
    except Exception as e:
        reply = f"সার্ভার সমস্যা: {e}"
    
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ বট চালু আছে")
    app.run_polling()

if __name__ == "__main__":
    main()
