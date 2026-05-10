import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import subprocess
import os
from flask import Flask
from threading import Thread

TOKEN = '8651122286:AAGauaH_E3LbjJBHQzxUfaAk_z3Mr62r3K8'
GITHUB_TOKEN = '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'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

xray_process = None

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_start = KeyboardButton('▶️ استارت سرور و دریافت لینک')
    btn_stop = KeyboardButton('🛑 توقف سرور')
    markup.add(btn_start, btn_stop)
    bot.send_message(message.chat.id, "سلام! ربات کنترلر G2Ray فعال شد.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    global xray_process
    chat_id = message.chat.id

    if message.text == '▶️ استارت سرور و دریافت لینک':
        if xray_process is None or xray_process.poll() is not None:
            try:
                xray_process = subprocess.Popen(['/usr/local/bin/xray', '-c', '/etc/config.json'])
                codespace_name = os.environ.get('CODESPACE_NAME', 'unknown-codespace')
                sni = f"{codespace_name}-443.app.github.dev"
                
                vless_link = f"vless://550e8400-e29b-41d4-a716-446655440000@94.130.50.12:443?encryption=none&security=tls&type=xhttp&host={sni}&path=/#G2Ray-Bot"
                
                msg = "✅ سرور Xray روشن شد!\n\n"
                msg += f"🔗 ` {vless_link} `\n\n"
                msg += f"• SNI: {sni}"
                bot.send_message(chat_id, msg, parse_mode='Markdown')
            except Exception as e:
                bot.send_message(chat_id, f"❌ خطا: {e}")
        else:
            bot.send_message(chat_id, "⚠️ سرور از قبل روشن است.")

    elif message.text == '🛑 توقف سرور':
        if xray_process and xray_process.poll() is None:
            xray_process.terminate()
            xray_process.wait()
            bot.send_message(chat_id, "🛑 سرور متوقف شد.")
        else:
            bot.send_message(chat_id, "⚠️ سرور خاموش است.")

if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    bot.infinity_polling()
