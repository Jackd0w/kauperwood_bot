import telebot
import datetime
import pytz
import json
import traceback
from analyzer.api.handlers import config
from analyzer.utils import currency

#TODO add API for 24/7 monitoring
#TODO read documentation for flixer
#TODO XML parsing
#TODO Valute converting


P_TIMEZONE = pytz.timezone(config.TIMEZONE)
TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message, 'Greetings! I can show you exchange rates.\n'+
                            'To get help press /help.')


@bot.message_handler(commands=['help'])  
def help_command(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    bot.send_message(  
        message.chat.id,  
        '1) To receive a list of available currencies press /exchange.\n' +  
        '2) Click on the currency you are interested in.\n' +  
        '3) You will receive a message containing information regarding the source and the target currencies, ' +  
        'buying rates and selling rates.\n' +  
        '4) Click “Update” to receive the current information regarding the request. ' +  
        'The bot will also show the difference between the previous and the current exchange rates.\n',
        reply_markup=keyboard  
    )

@bot.message_handler(commands=['exchange'])  
def exchange_command(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.row(  
        telebot.types.InlineKeyboardButton('USD', callback_data='get-USD')  
    )  
    keyboard.row(  
        telebot.types.InlineKeyboardButton('EUR', callback_data='get-EUR'),  
        telebot.types.InlineKeyboardButton('RUR', callback_data='get-RUR'),
        telebot.types.InlineKeyboardButton('AUD', callback_data='get-AUD'),
        telebot.types.InlineKeyboardButton('AZN', callback_data='get-AZN'),
        telebot.types.InlineKeyboardButton('GBP', callback_data='get-GBP'),
        telebot.types.InlineKeyboardButton('AMD', callback_data='get-AMD'),
        telebot.types.InlineKeyboardButton('BYN', callback_data='get-BYN'),
        telebot.types.InlineKeyboardButton('BGN', callback_data='get-BGN'),
        telebot.types.InlineKeyboardButton('HUF', callback_data='get-HUF'),
        telebot.types.InlineKeyboardButton('HKD', callback_data='get-HKD'),
        telebot.types.InlineKeyboardButton('DKK', callback_data='get-DKK'),
        telebot.types.InlineKeyboardButton('INR', callback_data='get-INR'),
        telebot.types.InlineKeyboardButton('KZT', callback_data='get-KZT'),
        telebot.types.InlineKeyboardButton('CAD', callback_data='get-CAD'),
        telebot.types.InlineKeyboardButton('KGS', callback_data='get-KGS'),
        telebot.types.InlineKeyboardButton('CNY', callback_data='get-CNY'),
        telebot.types.InlineKeyboardButton('MDL', callback_data='get-MDL'),
        telebot.types.InlineKeyboardButton('NOK', callback_data='get-NOK'),
        telebot.types.InlineKeyboardButton('UAK', callback_data='get-UAK'),
    )  
  
    bot.send_message(  
        message.chat.id,   
        'Click on the currency of choice:',  
        reply_markup=keyboard  
    )

@bot.callback_query_handler(func=lambda call: True)  
def iq_callback(query):  
    data = query.data  
    if data.startswith('get-'):  
        get_ex_callback(query)

def get_ex_callback(query):  
    bot.answer_callback_query(query.id)  
    send_exchange_result(query.message, query.data[4:])


def send_exchange_result(message, ex_code):  
    bot.send_chat_action(message.chat.id, 'typing')  
    ex = currency.get_exchange(ex_code)  
    bot.send_message(  
        message.chat.id, serialize_ex(ex),  
        reply_markup=get_update_keyboard(ex),  
	parse_mode='HTML'  
    )


def get_update_keyboard(ex):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.row(  
        telebot.types.InlineKeyboardButton(  
            'Update',  
	    callback_data=json.dumps({  
                't': 'u', 'e': {  
                    'b': ex['buy'],  
		            's': ex['sale'],  
		            'c': ex['ccy']  
                }  
            }).replace(' ', '')  
        ),  
	telebot.types.InlineKeyboardButton('Share', switch_inline_query=ex['ccy'])  
    )  
    return keyboard


def serialize_ex(ex_json, diff=None):  
    result = '<b>' + ex_json['base_ccy'] + ' -> ' + ex_json['ccy'] + ':</b>\n\n' + 'Buy: ' + ex_json['buy']  
    if diff:  
        result += ' ' + serialize_exchange_diff(diff['buy_diff']) + '\n' + 'Sell: ' + ex_json['sale'] + ' ' + serialize_exchange_diff(diff['sale_diff']) + '\n'  
    else:  
        result += '\nSell: ' + ex_json['sale'] + '\n'  
    return result


def serialize_exchange_diff(diff):  
    result = ''  
    if diff > 0:  
        result = '(' + str(diff) + ' <img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="↗️" src="https://s.w.org/images/core/emoji/2.3/svg/2197.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2197.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2197.svg">" src="https://s.w.org/images/core/emoji/72x72/2197.png">" src="https://s.w.org/images/core/emoji/72x72/2197.png">)'  
    elif diff < 0:  
        result = '(' + str(diff)[1:] + ' <img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="<img draggable="false" data-mce-resize="false" data-mce-placeholder="1" data-wp-emoji="1" class="emoji" alt="↘️" src="https://s.w.org/images/core/emoji/2.3/svg/2198.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2198.svg">" src="https://s.w.org/images/core/emoji/2.3/svg/2198.svg">" src="https://s.w.org/images/core/emoji/72x72/2198.png">" src="https://s.w.org/images/core/emoji/72x72/2198.png">)'  
    return result


bot.polling(none_stop=True, interval=0)