from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import openpyxl
from unittest.mock import patch, MagicMock

# Создание Excel файла и запись заголовков
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Tracks"
sheet.append(["Название", "Ссылка"])

def create_driver():
    options = webdriver.ChromeOptions()
    useragent = UserAgent()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Отключение GPU
    options.add_argument('--no-sandbox')  # Отключение песочницы
    options.add_argument("start-maximized")
    options.add_argument(f"user-agent={useragent.chrome}")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Создание экземпляра WebDriver для Chrome
    return webdriver.Chrome(options=options)

def collect_tracks(driver, sheet):
    url = f"https://soundcloud.com/shedou-prou/sets/shin-megami-tensei-v-ost"
    driver.get(url)
    print("Страница открыта...")
    time.sleep(3)

    # Прокрутка страницы вниз для загрузки всех треков
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Необходимо дать время для загрузки страницы через AJAX.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Если высота страницы не меняется, это означает, что прокрутка достигла низа.
        last_height = new_height
    print("Плейлист прокручен до конца...")
    time.sleep(3)

    # Сбор информации о треках
    tracks = driver.find_elements(By.XPATH, ".//a[@class='trackItem__trackTitle sc-link-dark sc-link-primary sc-font-light']")
    tracks_count = len(tracks)
    print(f"Найдено элементов: {tracks_count}")

    # Запись данных о треках
    for number in range(0, len(tracks)):
        sheet.append([tracks[number].text, tracks[number].get_attribute('href')])

def main():
    try:
        driver = create_driver()
        collect_tracks(driver, sheet)
    except Exception as ex:
        print(ex)
    finally:
        # Закрытие страницы
        driver.close()

    # Сохранение файла
    workbook.save("tracks.xlsx")
    print("Данные успешно сохранены в файл tracks.xlsx")

if __name__ == "__main__":
    main()
