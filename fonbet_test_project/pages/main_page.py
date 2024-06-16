import time

import allure

from fonbet_test_project.pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, driver, wait, action):
        super().__init__(driver, wait, action)
        self.driver = driver
        self.wait = wait
        self.action = action

        # Локаторы класса HeaderMenuLocators
        self.my_tickets_button = self.header_menu_locators.MY_TICKETS_BUTTON

        # Локаторы класса MainPageLocators
        self.quick_buy_lottery_1 = self.main_page_locators.QuickBuy.LOTTERY_1
        self.quick_buy_pay_button = self.main_page_locators.QuickBuy.PAY_BUTTON
        self.premier_lottery = self.main_page_locators.Showcase.PREMIER_LOTTERY

        # Локаторы класса AuthLocators
        self.login_field = self.authorization_locators.LOGIN_FIELD
        self.password_field = self.authorization_locators.PASSWORD_FIELD
        self.enter_button = self.authorization_locators.ENTER_BUTTON
        self.login_modal_title = self.authorization_locators.LOGIN_MODAL_TITLE

    def sign_in(self):
        self.click_element(self.my_tickets_button)

        self.driver.switch_to.default_content()

        self._send_keys_by_locator(self.login_field, self.sensitive_data.LOGIN)

        self._send_keys_by_locator(self.password_field, self.sensitive_data.PASSWORD)

        self.click_element(self.enter_button)

        time.sleep(1)
        self.click_element(self.enter_button)
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
            self.click_element(self.quick_buy_lottery_1)
            self.click_element(self.quick_buy_pay_button)

        with allure.step('Получение заголовка в открывшемся модальном окне'):
            self.switch_to_default_content()
            logging_modal_title = self.find_element(self.login_modal_title).text

        return logging_modal_title

    def click_few_times_on_element_by_locator(self, locator, counts):
        element = self.find_element(locator)
        for count in range(counts):
            element.click()
        return self

    def click_and_wait_on_element_by_locator(self, locator):
        element = self.find_element(locator)
        element.click()
        time.sleep(1)
        return self
