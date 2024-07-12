from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import openpyxl

# Создание Excel файла и запись заголовков
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Movies"
sheet.append(["Название", "Год", "Ссылка"])

# Параметры для создаваемого экземпляра браузера
options = webdriver.ChromeOptions()
useragent = UserAgent
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Отключение GPU
options.add_argument('--no-sandbox')  # Отключение песочницы
options.add_argument("start-maximized")
options.add_argument(f"user-agent={useragent.chrome}")
options.add_argument("--disable-blink-features=AutomationControlled")

# Создание экземпляра WebDriver для Chrome
driver = webdriver.Chrome(options=options)

try:
    # Открытие страницы
    url = "https://www.kinopoisk.ru/s/type/film/list/1/find/%D0%BE%D0%B4%D0%B8%D0%BD/"
    driver.get(url)
    print("Страница открыта...")
    time.sleep(3)

    # Согласие с Cookies (Если пригодится)
    # driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    # print("Cookies приняты...")
    # time.sleep(3)

    # Сбор информации о фильмах
    titles1 = driver.find_elements(By.XPATH, ".//div[@class='element']/div[@class='info']/p[@class='name']/a[@class='js-serp-metrika']")
    titles2 = driver.find_elements(By.XPATH, ".//div[@class='element width_2']/div[@class='info']/p[@class='name']/a[@class='js-serp-metrika']") # Элементы на первой странице разделены разными классами
    titles3 = driver.find_elements(By.XPATH, ".//div[@class='element width_3']/div[@class='info']/p[@class='name']/a[@class='js-serp-metrika']")

    years1 = driver.find_elements(By.XPATH, ".//div[@class='element']/div[@class='info']/p[@class='name']/span[@class='year']")
    years2 = driver.find_elements(By.XPATH, ".//div[@class='element width_2']/div[@class='info']/p[@class='name']/span[@class='year']")
    years3 = driver.find_elements(By.XPATH, ".//div[@class='element width_3']/div[@class='info']/p[@class='name']/span[@class='year']")

    links1 = driver.find_elements(By.XPATH, ".//div[@class='element']/div[@class='info']/p[@class='name']/a[@class='js-serp-metrika']")
    links2 = driver.find_elements(By.XPATH, ".//div[@class='element width_2']/div[@class='info']/p[@class='name']/a[@class='js-serp-metrika']")
    links3 = driver.find_elements(By.XPATH, ".//div[@class='element width_3']/div[@class='info']/p[@class='name']/a[@class='js-serp-metrika']")

    print(f"Найдено элементов: {len(titles1) + len(titles2) + len(titles3)}")

    # Запись данных о фильмах
    for number in range(0, len(titles1)):
        sheet.append([titles1[number].text, years1[number].text, links1[number].get_attribute('href')])

    for number in range(0, len(titles2)):
        sheet.append([titles2[number].text, years2[number].text, links2[number].get_attribute('href')])

    for number in range(0, len(titles3)):
        sheet.append([titles3[number].text, years3[number].text, links3[number].get_attribute('href')])

except Exception as ex:
    print(ex)

finally:
    # Закрытие страницы
    driver.close()

# Сохранение файла
workbook.save("movies.xlsx")
print("Данные успешно сохранены в файл movies.xlsx")