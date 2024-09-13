from bot import *

@bot.message_handler(func=lambda message: message.text == "Поделиться результатом в соцсети 🦒")
def share_soc(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    # проверка нет ли нашего результата в списке
    if user_id not in result_dict or not result_dict[user_id]:
        bot.send_message(chat_id, 'Вы еще не проходили викторину и у вас нет результата. Нажмите кнопку Начать викторину 🦁')
    else:
        keyboard = telebot.types.InlineKeyboardMarkup()
        button_vk = telebot.types.InlineKeyboardButton(text="VK", callback_data='vk')
        button_odn = telebot.types.InlineKeyboardButton(text="Odnoklassniki", callback_data='odn')
        button_twit = telebot.types.InlineKeyboardButton(text="Twitter", callback_data='twit')
        keyboard.add(button_vk,button_odn,button_twit)