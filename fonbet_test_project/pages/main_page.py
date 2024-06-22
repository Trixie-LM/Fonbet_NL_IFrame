import time

import allure

from data.sensitive_data import SensitiveData
from fonbet_test_project.locators import QuickBuyLocators, ShowcaseLocators, AuthLocators, HeaderMenuLocators
from fonbet_test_project.pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, driver, wait, action):
        super().__init__(driver, wait, action)
        self.driver = driver
        self.wait = wait
        self.action = action

        # Данные класса SensitiveData
        self.LOGIN = SensitiveData.LOGIN
        self.PASSWORD = SensitiveData.PASSWORD

        # Локаторы класса HeaderMenuLocators
        self.my_tickets_button = HeaderMenuLocators.MY_TICKETS_BUTTON

        # Локаторы класса MainPageLocators
        self.QUICK_BUY_AREA = QuickBuyLocators.AREA
        self.LOTTERY_1 = QuickBuyLocators.LOTTERY_1
        self.LOTTERY_2 = QuickBuyLocators.LOTTERY_2
        self.LOTTERY_3 = QuickBuyLocators.LOTTERY_3
        self.LOTTERY_4 = QuickBuyLocators.LOTTERY_4
        self.LEFT_ARROW_ACTION = QuickBuyLocators.LEFT_ARROW_ACTION
        self.LEFT_ARROW_STATUS = QuickBuyLocators.LEFT_ARROW_STATUS
        self.RIGHT_ARROW_ACTION = QuickBuyLocators.RIGHT_ARROW_ACTION
        self.TICKETS_QUANTITY = QuickBuyLocators.TICKETS_QUANTITY
        self.TICKETS_PRICE = QuickBuyLocators.TICKETS_PRICE
        self.quick_buy_pay_button = QuickBuyLocators.PAY_BUTTON
        self.premier_lottery = ShowcaseLocators.PREMIER_LOTTERY

        # Локаторы класса AuthLocators
        self.login_field = AuthLocators.LOGIN_FIELD
        self.password_field = AuthLocators.PASSWORD_FIELD
        self.enter_button = AuthLocators.ENTER_BUTTON
        self.login_modal_title = AuthLocators.LOGIN_MODAL_TITLE

    def log_in(self):
        self.click_element(self.my_tickets_button)

        self.driver.switch_to.default_content()

        self._send_keys_by_locator(self.login_field, self.LOGIN)

        self._send_keys_by_locator(self.password_field, self.PASSWORD)

        self.click_element(self.enter_button)

        time.sleep(1)

        self.switch_to_nl_iframe_and_wait()

    # TODO: Все методы авторизации (и внутри раздела лотереи) имеют общую специфику. Отрефакторить
    def auth_via_button_my_tickets(self) -> str:
        """
        :return: Заголовок модального окна
        """
        with allure.step('Нажатие на кнопку "Мои билеты"'):
            self.click_element(self.my_tickets_button)

        with allure.step('Получение текста заголовка в открывшемся модальном окне'):
            self.switch_to_default_content()
            logging_modal_title = self.find_element(self.login_modal_title).text

        return logging_modal_title

    def auth_via_quick_buy(self) -> str:
        """
        :return: Заголовок модального окна
        """
        with allure.step('Покупка билета через меню быстрой покупки'):
            self.click_element(self.LOTTERY_1)
            self.click_element(self.quick_buy_pay_button)

        with allure.step('Получение заголовка в открывшемся модальном окне'):
            self.switch_to_default_content()
            logging_modal_title = self.find_element(self.login_modal_title).text

        return logging_modal_title

    def click_few_times_on_element_by_locator(self, locator, counts):
        element = self.find_element(locator)
        for count in range(counts):
            element.click()

    def click_and_wait_on_element_by_locator(self, locator):
        element = self.find_element(locator)
        element.click()
        time.sleep(1)

    def get_elements_count_in_quick_buy(self):
        return self.get_elements_count(self.QUICK_BUY_AREA)

    def add_all_lottery_in_quick_buy(self):
        self.click_and_wait_on_element_by_locator(self.LOTTERY_1)
        self.click_and_wait_on_element_by_locator(self.LOTTERY_2)
        self.click_and_wait_on_element_by_locator(self.RIGHT_ARROW_ACTION)
        self.click_and_wait_on_element_by_locator(self.LOTTERY_3)
        self.click_and_wait_on_element_by_locator(self.RIGHT_ARROW_ACTION)
        self.click_and_wait_on_element_by_locator(self.LOTTERY_4)
        self.click_and_wait_on_element_by_locator(self.LEFT_ARROW_ACTION)
        self.click_and_wait_on_element_by_locator(self.LEFT_ARROW_ACTION)

    def get_text_in_cart_in_quick_buy(self):
        tickets_quantity = self.find_element(self.TICKETS_QUANTITY).text
        tickets_price = self.find_element(self.TICKETS_PRICE).text
        left_arrow_status = self.find_element(self.LEFT_ARROW_STATUS).get_attribute('aria-disabled')

        return tickets_quantity, tickets_price, left_arrow_status
