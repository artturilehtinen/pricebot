import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from bitcoin_value import currency


def create_reply_markup():
    keyboard = [

        [InlineKeyboardButton("Bitcoin", callback_data="btc")],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I check crypto prices for you!")
    await update.message.reply_text("Select currency:", reply_markup=create_reply_markup())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bitcoin_value = currency("EUR")
    query = update.callback_query

    await query.answer()

    await query.edit_message_text(text=f"BTC price is {bitcoin_value:.2f} €")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Select currency:", reply_markup=create_reply_markup())


def main():
    load_dotenv()
    key = os.getenv('TELEGRAM_API_KEY')

    app = ApplicationBuilder().token(key).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
