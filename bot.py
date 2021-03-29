import telebot
import config

#TODO add API for 24/7 monitoring
#TODO read documentation for flixer
#TODO JSON parser




bot = telebot.TeleBot(config.TOKEN)

currencies = ['евро', 'доллар']

def check_currency(message):
    for c in currencies:
        if c in message.text.lower():
            return True
        return False


def check_currency_value(text):
    currency_value = {'евро' : 70, 'доллар' : 60}
    for currency, value in currency_value.items():
        if currency in text.lower():
            return currency, value

    return None, None

@bot.message_handler(func=check_currency)
def handle_currency(message):
    print(message)
    currency, value = check_currency_value(message.text())
    if currency:
        bot.send_message(message.chat.id, text='Курс {} равен {}.'.format(currency, value))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, как дела?")



@bot.message_handler(content_types = ['photo'])
def text_handler(message):
    chat_id = message.chat.chat.id
    bot.send_message(chat_id, "Красиво, но команды должны быть текстовыми")

bot.polling(none_stop=True, interval=0)