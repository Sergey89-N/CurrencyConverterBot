import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_handler(message: telebot.types.Message):
    text = 'Чтобы начать конвертировать валюту, введите команду боту в следующем формате:\n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nДля просмотра доступных валют введите: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def begin_handler(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert_handler(message: telebot.types.Message):
    try:
        parameters = message.text.split(' ')

        if len(parameters) != 3:
            raise APIException('Введите три параметра.')

        base, quote, amount = parameters
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base * float(amount)}'
        bot.send_message(message.chat.id, text)

bot.polling()
