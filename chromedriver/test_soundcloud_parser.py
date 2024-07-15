import unittest
from unittest.mock import MagicMock, patch
from openpyxl import Workbook
from soundcloud_parser import collect_tracks

class TestCollectTracks(unittest.TestCase):
    @patch('soundcloud_parser.webdriver.Chrome')
    def test_collect_tracks(self, MockWebDriver):
        # Моковый экземпляр веб-драйвера
        mock_driver = MockWebDriver.return_value

        # Моковый возврат find_elements
        mock_elements = [MagicMock() for _ in range(117)]
        for i, elem in enumerate(mock_elements):
            elem.text = f'Track {i}'
            elem.get_attribute = MagicMock(return_value=f'https://example.com/track/{i}')

        mock_driver.find_elements.return_value = mock_elements

        # Создание мокового листа Excel
        workbook = Workbook()
        sheet = workbook.active

        # Вызов тестируемой функции
        collect_tracks(mock_driver, sheet)

        # Проверка количества найденных треков
        self.assertEqual(len(sheet['A']), 117)  # Включая заголовок
        self.assertEqual(len(sheet['B']), 117)

        # Проверка значения переменной tracks_count
        tracks_count = len(mock_elements)
        self.assertEqual(tracks_count, 117)

if __name__ == '__main__':
    unittest.main()
