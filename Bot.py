import telebot
from config import keys, TOKEN
from extensions import ConvertException, ValuteConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.chat.username}. "
                                      f"Данный телеграмм бот разработан для быстрой конвертации валюты. "
                                      f"Чтобы начать работу, введите команду боту в следующем формате:\n<имя конвертируемой валюты>"
                                      f"<имя валюты, в которую переводится конвертируемая валюта>"
                                      f"<количество конвертируемой валюты>"
                                      f"\nСписок всех доступрных валют можно увидеть по команде: /values")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert_text(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertException('Ведите 3 параметра')

        base, quote, quantity = values
        converted = ValuteConverter.get_price(quote, base, quantity)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка ввода: \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: \n{e}')

    else:
        text = f'{quantity} {base} в {quote} составляет: {converted}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)