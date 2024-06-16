import time

from selenium.webdriver.support import expected_conditions as ec
from data.sensitive_data import sensitive_data
from fonbet_test_project.locators import authorization_locators, header_menu_locators, iframe_locators, \
    lottery_page_locators, main_page_locators


class BasePage:
    def __init__(self, driver, wait, action):
        self.driver = driver
        self.wait = wait
        self.action = action

        # Локаторы
        self.nl_iframe = iframe_locators.NL_IFRAME
        self.first_lottery_quick_buy = main_page_locators.QuickBuy.LOTTERY_1

        # Ссылки на локаторы
        self.sensitive_data = sensitive_data
        self.authorization_locators = authorization_locators
        self.header_menu_locators = header_menu_locators
        self.iframe_locators = iframe_locators
        self.lottery_page_locators = lottery_page_locators
        self.main_page_locators = main_page_locators

    def open_website(self):
        self.driver.get(self.sensitive_data.WEBSITE)
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
            'test_premier_lottery': self.main_page_locators.Showcase.PREMIER_LOTTERY,
            'test_big8_lottery': self.main_page_locators.Showcase.BIG8_LOTTERY,
            'test_lottery_4X4': self.main_page_locators.Showcase.LOTTERY_4X4,
            'test_turnir': self.main_page_locators.Showcase.TURNIR
        }

        # Получаем локатор для лотереи
        locator = locator_map.get(module_name)

        # Если локатор не найден, выбрасываем исключение
        if not locator:
            raise ValueError(f"Не найден локатор для лотереи: {module_name}")

        return locator

    def _send_keys_by_locator(self, locator, value):
        field = self.driver.find_element(*locator)
        field.send_keys(value)

    def find_element(self, locator):
        self.wait.until(ec.element_to_be_clickable(locator))
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
