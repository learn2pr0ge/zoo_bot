import telebot
import config
from quiz import QuizModule
from config import valid_commands, user_scores, creatures, result_dict
from api import *



token = config.BOT_TOKEN
bot = telebot.TeleBot(token)

#обработчик команды /start



@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Начать викторину 🦁")
    button2 = telebot.types.KeyboardButton(text="Попробовать еще раз 🐘")
    button3 = telebot.types.KeyboardButton(text="Поделиться результатом в соцсети 🦒")
    button4 = telebot.types.KeyboardButton(text="Связаться со службой поддержки 📨")
    button5 = telebot.types.KeyboardButton(text="Вернуться в главное меню 🐘")

    keyboard.add(button1,button2,button3,button4,button5)
    with open('/home/a1nix/Desktop/fullstack_factory/python/moscow_zoo/zoo_bot/static/images/zoo_logo.jpeg', 'rb') as photo1:
        bot.send_photo(chat_id, photo1)
    bot.send_message(
        chat_id,
        """
        <b>Добро пожаловать в Telegram бота Московского Зоопарка!</b> 🦁🐘🦒\n\n
        <i>Используйте кнопки меню ниже для навигации:</i>\n
        - <b>Кнопка "Начать викторину"</b> поможет вам выбрать ваше тотемное животное 🐯\n
        - <b>Кнопка "Попробовать еще раз"</b> позволит пройти еще раз нашу викторину 💌\n
        - <b>Кнопка "Поделиться результатом"</b> поможет сделать пост о вашем тотемном животном в соцсети 📝\n
        - Чтобы задать вопрос службе поддержки, нажмите на кнопку <b>"Связаться со службой поддержки"</b> ❓\n\n
        <b>Для выдачи изображения животного введите команду: <code>/animal имя_животного</code> на английском языке 🔤</b>\n
        <b>Примеры команд:</b> \n
        <code>/animal dog</code> \n
        <code>/animal elephant</code>
        
        """,
        parse_mode='HTML',
        reply_markup=keyboard
    )
    #делаем проверку на ввод правильной команды
    if message.text not in config.valid_commands and not message.text.startswith('/animal'):
        bot.send_message(chat_id, 'Вы ввели неверную команду')

@bot.message_handler(commands=['animal'])
def show_animal(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Начать викторину 🦁")
    button2 = telebot.types.KeyboardButton(text="Попробовать еще раз 🐘")
    button3 = telebot.types.KeyboardButton(text="Поделиться результатом в соцсети 🦒")
    button4 = telebot.types.KeyboardButton(text="Связаться со службой поддержки 📨")
    button5 = telebot.types.KeyboardButton(text="Вернуться в главное меню 🐘")

    keyboard.add(button1, button2, button3, button4,button5)
    try:
        command_parts = message.text.split()
        if len(command_parts) != 2:
            raise ValueError(f'Введите команду формата /animal имя_животного')

        elif not command_parts[1].isalpha():
            raise ValueError(f'Введите команду формата /animal имя_животного')
        elif command_parts[1] not in creatures:
            raise ValueError(f'Недопустимое имя животного')
        else:
            command_parts = command_parts[1]
            animal_link = ApiAnimal.get_api(command_parts)
            if animal_link.startswith('http'):
                bot.send_photo(chat_id, photo=animal_link, reply_markup=keyboard)
            else:
                bot.send_message(chat_id, animal_link)

    except ValueError as e:
        bot.send_message(chat_id, f'Ошибка {e}')
        return
    except Exception as e:
        bot.send_message(chat_id, f'Ошибка {e}')
        return




@bot.message_handler(func=lambda message: message.text == "Связаться со службой поддержки 📨")
def contact_support(message):
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_telegram = telebot.types.InlineKeyboardButton(text="Telegram", url= 'https://t.me/Moscowzoo_official')


    keyboard.add(button_telegram)

    with open('/home/a1nix/Desktop/fullstack_factory/python/moscow_zoo/zoo_bot/static/images/owl.jpg', 'rb') as photo1:
        bot.send_photo(chat_id, photo1)
    bot.send_message(chat_id, 'По всем вопросам взятия животного на попечение свяжитесь с нашей службой поддержки ✒ \n'
                              'a.zhemchugov@moscowzoo.ru \n'
                              'Телефон: +7 (499) 252-29-51', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Поделиться результатом в соцсети 🦒")
def share_soc(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    # проверка нет ли нашего результата в списке
    if user_id not in result_dict or not result_dict[user_id]:
        bot.send_message(chat_id, 'Вы еще не проходили викторину и у вас нет результата. Нажмите кнопку Начать викторину 🦁')
    else:
        text, link = result_dict[user_id]
        enc_text = QuizModule.quiz_result(text)
        url = 'https://t.me/MoscowZooQueryBot'

        # получаем первые 4 слова
        title = text.split()
        title = title[:4]
        fin_title = ' '.join(title)
        fin_title = fin_title[3:]


        #делает inline клавиатуру для открытия ссылки
        keyboard = telebot.types.InlineKeyboardMarkup()
        button_vk = telebot.types.InlineKeyboardButton(text="VK", url=f'https://vk.com/share.php?url={url}&title={fin_title}&comment={enc_text}')
        button_odn = telebot.types.InlineKeyboardButton(text="Odnoklassniki", url=f'https://connect.ok.ru/offer?url={url}&title={fin_title}&comment={enc_text}')
        button_twit = telebot.types.InlineKeyboardButton(text="Twitter", url=f'https://twitter.com/intent/tweet?text={enc_text[:200]}&url={url}')
        keyboard.add(button_vk,button_odn,button_twit)
        description, photo = result_dict[user_id]
        bot.send_photo(chat_id, photo=photo)
        bot.send_message(
            chat_id,
            description,
            parse_mode='HTML'
        )
        bot.send_message(chat_id, 'Выберете соцсеть для того чтобы поделиться результатом', reply_markup= keyboard)




@bot.message_handler(func=lambda message: message.text == "Попробовать еще раз 🐘")
def try_again(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    # проверка нет ли нашего результата в списке
    if user_id not in result_dict or not result_dict[user_id]:
        bot.send_message(chat_id, 'Вы еще не проходили викторину. Нажмите кнопку Начать викторину 🦁')
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="Начать викторину 🦁")
        button2 = telebot.types.KeyboardButton(text="Попробовать еще раз 🐘")
        button3 = telebot.types.KeyboardButton(text="Поделиться результатом в соцсети 🦒")
        button4 = telebot.types.KeyboardButton(text="Связаться со службой поддержки 📨")

        keyboard.add(button1, button2, button3, button4)
    else:
        del result_dict[user_id]
        game(message)

@bot.message_handler(func=lambda message: message.text == "Начать викторину 🦁")
def game(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    #проверка нет ли нашего результата в списке
    if user_id not in result_dict or not result_dict[user_id]:

        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="Поехали 🐿")
        keyboard.add(button1)
        bot.send_message(chat_id,'Вам будет задано 10 вопросов которые помогут выбрать вашего тотемного'
                         'животного. Нажимайте кнопки от 1 до 4 чтобы выбрать варианты ответа.',reply_markup=keyboard)
    else:
        bot.send_message(chat_id, """<b>Вы уже проходили викторину. Чтобы сбросить результат и пройти еще раз нажмите кнопку Попробовать еще раз 🐘 \n
        Ваш результат: </b>""", parse_mode='HTML')
        description, photo = result_dict[user_id]
        bot.send_photo(chat_id, photo=photo)
        bot.send_message(
            chat_id,
            description,
            parse_mode='HTML'
        )
#функции викторины
@bot.message_handler(func=lambda message: message.text == "Поехали 🐿")
def start_quiz(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    # инициализация очков пользователя
    if user_id not in user_scores:
        user_scores[user_id] = 0
        send_question(chat_id, 0)
    else:
        user_scores[user_id] = 0
        send_question(chat_id, 0)

def send_question(chat_id, question_index):
    line1 = QuizModule.quiz_quest(question_index)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    answer_list = []
    for question, answers in line1.items():
        # проходим по вложенному словарю, который содержит ответы и их баллы
        for answer, points in answers.items():
            answer_list.append(answer)
    button1 = telebot.types.KeyboardButton(text=f"Ответ 1")
    button2 = telebot.types.KeyboardButton(text=f"Ответ 2")
    button3 = telebot.types.KeyboardButton(text=f"Ответ 3")
    button4 = telebot.types.KeyboardButton(text=f"Ответ 4")
    button5 = telebot.types.KeyboardButton(text="Вернуться в главное меню 🐘")
    keyboard.add(button1, button2, button3, button4, button5)
    bot.send_message(chat_id, f"""<b>{question}</b>""", reply_markup=keyboard, parse_mode='HTML')
    bot.send_message(chat_id, f"""
    <b>Варианты ответа:</b>
    <i>Ответ 1: {answer_list[0]}</i>
    <i>Ответ 2: {answer_list[1]}</i>
    <i>Ответ 3: {answer_list[2]}</i>
    <i>Ответ 4: {answer_list[3]}</i>
    """, parse_mode='HTML')

    # пегистрируем обработчик следующего шага для получения ответа
    bot.register_next_step_handler_by_chat_id(chat_id, process_answer, question_index, answer_list)

def process_answer(message, question_index, answer_list):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text == "Вернуться в главное меню 🐘":
        start(message)
        return

    if message.text == "Ответ 1":
        selected_answer = answer_list[0]
    elif message.text == "Ответ 2":
        selected_answer = answer_list[1]
    elif message.text == "Ответ 3":
        selected_answer = answer_list[2]
    elif message.text == "Ответ 4":
        selected_answer = answer_list[3]

    #selected_answer = message.text.split(":")[1].strip()  # Извлекаем ответ из сообщения


    # получаем правильные ответы и баллы для текущего вопроса
    line1 = QuizModule.quiz_quest(question_index)
    for question, answers in line1.items():
        for answer, points in answers.items():
            if answer == selected_answer:
                user_scores[user_id] += points

    bot.send_message(chat_id, f"""<i>Ваш текущий результат: {user_scores[user_id]} баллов</i>""", parse_mode='HTML')


    if question_index + 1 < 10:
        send_question(chat_id, question_index + 1)
    else:
        # проверка количества набранных баллов
        bot.send_message(chat_id,
                         f"""<b>Викторина завершена! Ваш итоговый результат: {user_scores[user_id]} баллов</b>""",
                         parse_mode='HTML')
        if user_scores[user_id] <= 15:
            animal_link = ApiAnimal.get_api('turtle')
            result_dict[user_id] = ["""
                <b>Твое тотемное животное Черепаха 🐢</b> 
                <b>Ты всегда стремишься к гармонии и внутреннему покою, как черепаха в своём медленном и размеренном ритме.</b>\n\n
                <i>Взяв черепаху на попечение, ты будешь поддерживать не только себя, но и животное, чьё спокойствие и долгожительство вдохновляют.</i>\n\n
                <b>Черепаха научит тебя ценить каждый момент жизни, не спеша, но уверенно достигая целей.</b>\n\n
                <i>Забота о черепахе — это символ твоей заботы о мире и природной гармонии</i>.
                """, animal_link]
            description, link = result_dict[user_id]
            bot.send_photo(chat_id, photo=animal_link)
            bot.send_message(
                chat_id,
                description,
                parse_mode='HTML'
            )
        elif 15 < user_scores[user_id] <= 22:
            animal_link = ApiAnimal.get_api('leopard')
            result_dict[user_id] = ["""
                <b>Твое тотемное животное Кошка 🐆</b>
                <b>Как и кошка, ты независим и любишь создавать комфорт вокруг себя, но всегда ценишь время, проведённое с близкими.</b>\n\n
                <i>Взяв кошку под своё крыло, ты поможешь ей чувствовать себя защищённой, а взамен она подарит тебе уют и тепло.</i>\n\n
                <b>Кошка — это символ грациозности и спокойствия, как и твоя жизнь, где ты находишь баланс между свободой и домашним уютом.</b>\n\n
                <i>Забота о кошке — это возможность создать прочную связь с животным, которое, как и ты, любит свободу и комфорт.</i>
                """, animal_link]
            description, link = result_dict[user_id]
            bot.send_photo(chat_id, photo=animal_link)
            bot.send_message(
                chat_id,
                description,
                parse_mode='HTML'
            )

        elif 22 < user_scores[user_id] <= 30:
            animal_link = ApiAnimal.get_api('wolf')
            result_dict[user_id] = ["""
                <b>Твое тотемное животное Волк 🐺</b>
                <b>Ты, как волк, стремишься к новым горизонтам, всегда в поиске приключений, но одновременно ценишь свою команду и друзей.</b>\n\n
                <i>Волк символизирует силу, сплочённость и верность — поддерживая его, ты проявляешь эти качества и в себе.</i>\n\n
                <b>Забота о волкедаст тебе возможность стать частью природного мира, напоминая о важности дружбы и единства.</b> \n\n
                <i>Волк всегда действует в интересах своей стаи, и твоя помощь ему — это вклад в сохранение природного мира.</i>
                """, animal_link]
            description, link = result_dict[user_id]
            bot.send_photo(chat_id, photo=animal_link)
            bot.send_message(
                chat_id,
                description,
                parse_mode='HTML'
            )
        elif user_scores[user_id] > 30:
            animal_link = ApiAnimal.get_api('dolphin')
            result_dict[user_id] = ["""
                            <b>Твое тотемное животное Дельфин 🐬 </b>
                            <b>Ты энергичен, как дельфин, и всегда находишь радость в движении и общении с окружающими.</b>\n\n
                            <i>Взяв на попечение дельфина, ты поддержишь животное, которое символизирует жизнелюбие, свободу и любознательность.</i>\n\n
                            <b>Дельфин вдохновит тебя быть ещё более открытым миру и помогать тем, кто находится в его водных просторах.</b>\n\n
                            <i>Забота о дельфине — это напоминание, что вместе мы можем сделать мир более живым, ярким и дружелюбным.</i>
                            """, animal_link]
            description, link = result_dict[user_id]
            bot.send_photo(chat_id, photo=animal_link)
            bot.send_message(
                chat_id,
                description,
                parse_mode='HTML'
            )



@bot.message_handler(func=lambda message: message.text == "Вернуться в главное меню 🐘")
def quit_quiz(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Начать викторину 🦁")
    button2 = telebot.types.KeyboardButton(text="Попробовать еще раз 🐘")
    button3 = telebot.types.KeyboardButton(text="Поделиться результатом в соцсети 🦒")
    button4 = telebot.types.KeyboardButton(text="Связаться со службой поддержки 📨")
    button5 = telebot.types.KeyboardButton(text="Вернуться в главное меню 🐘")
    keyboard.add(button1, button2, button3, button4, button5)

    with open('/home/a1nix/Desktop/fullstack_factory/python/moscow_zoo/zoo_bot/static/images/zoo_logo.jpeg',
              'rb') as photo1:
        bot.send_photo(chat_id, photo1)
    bot.send_message(
        chat_id,
        """
        <b>Добро пожаловать в Telegram бота Московского Зоопарка!</b> 🦁🐘🦒\n\n
        <i>Используйте кнопки меню ниже для навигации:</i>\n
        - <b>Кнопка "Начать викторину"</b> поможет вам выбрать ваше тотемное животное 🐯\n
        - <b>Кнопка "Попробовать еще раз"</b> позволит пройти еще раз нашу викторину 💌\n
        - <b>Кнопка "Поделиться результатом"</b> поможет сделать пост о вашем тотемном животном в соцсети 📝\n
        - Чтобы задать вопрос службе поддержки, нажмите на кнопку <b>"Связаться со службой поддержки"</b> ❓\n\n
        <b>Для выдачи изображения животного введите команду: <code>/animal имя_животного</code> на английском языке 🔤</b>\n
        <b>Примеры команд:</b> \n
        <code>/animal dog</code> \n
        <code>/animal elephant</code>
        
        """,
        parse_mode='HTML',
        reply_markup=keyboard
    )
    # делаем проверку на ввод правильной команды
    if message.text not in config.valid_commands and not message.text.startswith('/animal'):
        bot.send_message(chat_id, 'Вы ввели неверную команду')




