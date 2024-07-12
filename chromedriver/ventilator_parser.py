from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import openpyxl

# Создание Excel файла и запись заголовков
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Products"
sheet.append(["Название", "Цена", "Ссылка"])

for page in range (1, 34):
    try:
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

        # Открытие страницы
        url = f"https://www.vseinstrumenti.ru/category/kanalnye-ventilyatory-11760/page{page}/"
        driver.get(url)
        print(f"Открыл страницу {page}...")

        # Сбор информации о товарах
        titles = driver.find_elements(By.XPATH, ".//a[@data-qa='product-name']")
        prices = driver.find_elements(By.XPATH, ".//p[@data-qa='product-price-current']")
        links = driver.find_elements(By.XPATH, ".//a[@class='uNCHtF']")
        print(f"Найдено элементов: {len(links)}")

        # Запись данных о товарах
        for number in range(0, len(links)):
            sheet.append([titles[number].text, prices[number].text, links[number].get_attribute("href")])

    except Exception as ex:
        print(ex)

    # Закрытие страницы
    finally:
        driver.close()

# Сохранение файла
workbook.save("products.xlsx")
print("Данные успешно сохранены в файл products.xlsx")