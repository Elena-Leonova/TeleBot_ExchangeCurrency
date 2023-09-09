import telebot
from config import keys
from extensions import CryptoConverter, APIException
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'To start working, enter the command in the following format(separated by space):' \
           ' \n- <Name of currency whose price you want to know>  \n- <Name of currency in which you want to know ' \
           'the price of the first currency> \n- <Amount of the first currency>\n \
 List of available currencies: /currencies'

    bot.reply_to(message, text)


@bot.message_handler(commands=['currencies'])
def currencies(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Wrong number of parameters')

        base, dif_currency, amount = values

        total_base = CryptoConverter.get_price(base, dif_currency, amount)
    except APIException as e:
        bot.reply_to(message, f"User's error is happened. \n{e}")

    except Exception as e:
        bot.reply_to(message, f"\n{e}")
    else:
        text = f"Price {amount} {base.lower()} in {dif_currency.lower()}: {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
