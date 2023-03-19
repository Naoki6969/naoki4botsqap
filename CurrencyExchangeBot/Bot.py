import telebot
from extensions import APIException, CurrencyConverter

from config import TOKEN, Currency


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Привет! Я Бот-Конвертер валют и я могу: \n'
                                      '1.Показать список доступных валют через команду /values \n'
                                      '2.Вывести конвертацию валюты используя следующие команды: \n'
                                      '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n'
                                      'Например: "usd rub 10".\n'
                                      '3.Напомнить, что я могу через команду /help'
                                      )


@bot.message_handler(commands=['values'])
def handle_values(message):
    bot.send_message(message.chat.id, f'Доступные валюты: {", ".join(Currency.keys())}.')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Ошибка: неверное количество параметров.')
        base, quote, amount = values
        result = CurrencyConverter.get_price(base, quote, float(amount))
        if base == quote and int(amount) < 0:
            bot.send_message(message.chat.id, f'Ошибка: невозможно перевести одинаковые валюты {base}, a также неверно указано количество переводимой валюты "{amount}", скорее всего оно меньше 0')
        elif int(amount) < 0:
            bot.send_message(message.chat.id, f'Ошибка: неверно указано количество переводимой валюты "{amount}", скорее всего оно меньше 0')
        elif base == quote:
            bot.send_message(message.chat.id, f'Ошибка: невозможно перевести одинаковые валюты {base}')
        elif base.upper() not in Currency or quote.upper() not in Currency:
            bot.send_message(message.chat.id, f'Вы указали неподдерживаемую валюту, чтобы уточнить какие валюты доступны для конвертации введите /values')
        else:
            bot.send_message(message.chat.id, f'{amount} {base} = {result} {quote}.')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка: неверное количество.')

bot.polling()
