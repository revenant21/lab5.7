import unittest
from unittest.mock import patch
from app import create_app


class ConverterTestCase(unittest.TestCase):
    def setUp(self):
        # Инициализация приложения для каждого теста
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_index_get(self):
        # Проверка, что главная страница открывается
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'USD', response.data)  # Проверяем наличие валюты по умолчанию

    @patch('app.converter.routes.get_exchange_rate')
    def test_conversion_success(self, mock_get_rate):
        # Тест успешной конвертации с подменой ответа API
        # Заставляем функцию в utils всегда возвращать курс 75.0
        mock_get_rate.return_value = 75.0

        response = self.client.post('/', data={
            'base': 'USD',
            'target': 'RUB',
            'amount': '10'
        })

        self.assertEqual(response.status_code, 200)
        # 10 * 75.0 = 750.0. Ищем это число в ответе
        self.assertIn(b'750.0', response.data)

    def test_invalid_input(self):
        # Тест на ввод букв вместо цифр
        response = self.client.post('/', data={
            'base': 'USD',
            'target': 'RUB',
            'amount': 'not_a_number'
        })

        self.assertEqual(response.status_code, 200)
        # Проверяем, что сработал блок except и вывелась ошибка
        self.assertIn("Введите корректное число.".encode('utf-8'), response.data)

    @patch('app.converter.routes.get_exchange_rate')
    def test_api_failure(self, mock_get_rate):
        # Тест ситуации, когда API вернул None
        mock_get_rate.return_value = None

        response = self.client.post('/', data={
            'base': 'USD',
            'target': 'RUB',
            'amount': '10'
        })

        self.assertIn("Не удалось получить курс валют.".encode('utf-8'), response.data)


if __name__ == '__main__':
    unittest.main()