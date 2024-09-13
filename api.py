import json
import requests
import config

ACCESS_KEY = config.API_KEY
#API метод получения случайной картинки
class APIError(Exception):
    pass

class ApiAnimal:
    @staticmethod
    def get_api(animal):
        url = 'https://api.unsplash.com/photos/random'
        params = {
            'query': animal,
            'client_id': ACCESS_KEY,
            'count': 1
        }
        response = requests.get(url, params=params)

        try:
            if response.status_code == 200:
                data = response.json()
                image_url = data[0]['urls']['regular']
                return image_url

            else:
                raise APIError(f'Невозможно получить ответ от API')
        except APIError as e:
            return f"Ошибка: {e}"
        except Exception as e:
            return f"Ошибка при обработке API запроса: {e}"


