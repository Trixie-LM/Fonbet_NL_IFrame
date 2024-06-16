import pytest
import allure

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from config.base_test import BaseTest


@pytest.fixture(scope='function')
def open_browser():
    options = Options()
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    action = ActionChains(driver)

    driver = BaseTest(driver, wait, action)

    with allure.step("Открытие браузера с выбранными настройками"):
        driver.open_website()

    with allure.step("Переключение драйвера на iFrame NL"):
        driver.switch_to_nl_iframe_and_wait()

    yield driver

    with allure.step("Добавление данных для проверки теста"):
        driver.add_screenshot()
        driver.add_logs()
        driver.add_html()
        driver.add_html_xml()
        # driver.add_video()


@pytest.fixture(scope='function')
def authorization(open_browser):
    with allure.step("Авторизация на сайте под тестовой учетной записью"):
        open_browser.sign_in()

    yield open_browser


@pytest.fixture(scope='function')
def lottery_section(authorization, request):
    """
    Открывает необходимую страничку лотереи, ориентируясь на название модуля, в котором находится тест-кейс
    """
    module_name = request.module.__name__.split('.')[-1]

    # Переход в раздел лотереи согласно названию тестового модуля
    locator = authorization.get_lottery_locator_by_module_name(module_name)
    authorization.navigate_to_lottery_section_by_locator(locator)

    yield authorization
