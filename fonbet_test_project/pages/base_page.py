import time

from selenium.webdriver.support import expected_conditions as ec
from data.sensitive_data import SensitiveData
from fonbet_test_project.locators import IframeLocators, QuickBuyLocators, ShowcaseLocators


class BasePage:
    def __init__(self, driver, wait, action):
        self.driver = driver
        self.wait = wait
        self.action = action

        # Данные класса SensitiveData
        self.WEBSITE = SensitiveData.WEBSITE

        # Локаторы класса IframeLocators
        self.nl_iframe = IframeLocators.NL_IFRAME

        # Локаторы класса MainPageLocators
        self.first_lottery_quick_buy = QuickBuyLocators.LOTTERY_1
        self.PREMIER_LOTTERY = ShowcaseLocators.PREMIER_LOTTERY
        self.BIG8_LOTTERY = ShowcaseLocators.BIG8_LOTTERY
        self.LOTTERY_4X4 = ShowcaseLocators.LOTTERY_4X4
        self.TURNIR = ShowcaseLocators.TURNIR

    def open_website(self):
        self.driver.get(self.WEBSITE)
        time.sleep(1)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def switch_to_frame(self, locator):
        iframe = self.wait.until(ec.presence_of_element_located(locator))
        self.driver.switch_to.frame(iframe)

    def switch_to_nl_iframe_and_wait(self):
        self.switch_to_frame(self.nl_iframe)
        self.wait.until(ec.visibility_of_element_located(self.first_lottery_quick_buy))

    def get_lottery_locator_by_module_name(self, module_name) -> tuple:
        """
        module_name = request.module.__name__.split('.')[-1]

        :param module_name: Имя модуля
        :return: Локатор лотереи на основе module_name
        """
        locator_map = {
            'test_premier_lottery': self.PREMIER_LOTTERY,
            'test_big8_lottery': self.BIG8_LOTTERY,
            'test_lottery_4X4': self.LOTTERY_4X4,
            'test_turnir': self.TURNIR
        }

        # Получаем локатор для лотереи
        locator = locator_map.get(module_name)

        # Если локатор не найден, выбрасываем исключение
        if not locator:
            raise ValueError(f"Не найден локатор для лотереи: {module_name}")

        return locator

    def send_keys_by_locator(self, locator, value):
        field = self.driver.find_element(*locator)
        field.send_keys(value)

    def find_element(self, locator):
        # self.wait.until(ec.element_to_be_clickable(locator))
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        self.wait.until(ec.element_to_be_clickable(locator))
        return self.driver.find_elements(*locator)

    def click_element(self, locator):
        """
        Ожидает появления и нажимает на элемент, указанный в локаторе
        """
        self.wait.until(ec.visibility_of_element_located(locator))
        element = self.driver.find_element(*locator)
        element.click()

    def get_elements_count(self, locator):
        count = len(self.driver.find_elements(*locator))
        return count

    def get_text_by_locator(self, locator):
        text = self.find_element(locator).text
        return text

    def quit(self):
        self.driver.quit()

    # TODO: Область скроллов. Оставить ли в этом модули или выделить отдельный?

    # Скролл по x и y
    def scroll_by(self, x, y):
        self.driver.execute_script(f"window.scrollTo({x}, {y})")

    # Скролл в самый низ страницы
    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    # Скролл на самый верх страницы
    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0)")

    # Скролл к элементу с раскрытием контента под ним
    def scroll_to_element(self, locator):
        element = self.find_element(locator)

        self.action.scroll_to_element(element).perform()
        self.driver.execute_script("""
            window.scrollTo({
                top: window.scrollY + 700,
            });
        """)
