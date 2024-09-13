import json
import re

class QuizModule:
    @staticmethod
    #функция по выдаче вопросов поштучно
    def quiz_quest(n):
        with open('quiz_questions.txt', 'r') as file1:
            quiz1 = file1.read()
            quiz1 = json.loads(quiz1)
            return quiz1[n]
    def quiz_result(text):
        # функция убирания html тегов из текста и замены пробелов
        clean_text = re.sub(r'<.*?>', '', text)
        clean_text = clean_text.replace('\n', ' ').replace('\r', '').strip()
        encoded_text = clean_text.replace(' ', '%20')

        return encoded_text




