import time
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
        self.MY_TICKETS_BUTTON = HeaderMenuLocators.MY_TICKETS_BUTTON

        # Локаторы класса MainPageLocators
        self.QUICK_BUY_AREA = QuickBuyLocators.AREA
        self.QUICK_LOTTERIES = [
            QuickBuyLocators.LOTTERY_1,
            QuickBuyLocators.LOTTERY_2,
            QuickBuyLocators.LOTTERY_3,
            QuickBuyLocators.LOTTERY_4,
        ]
        self.LOTTERY_1_PLUS_BUTTON = QuickBuyLocators.LOTTERY_1_PLUS_BUTTON
        self.LOTTERY_1_MINUS_BUTTON = QuickBuyLocators.LOTTERY_1_MINUS_BUTTON
        self.LEFT_ARROW_ACTION = QuickBuyLocators.LEFT_ARROW_ACTION
        self.LEFT_ARROW_STATUS = QuickBuyLocators.LEFT_ARROW_STATUS
        self.RIGHT_ARROW_ACTION = QuickBuyLocators.RIGHT_ARROW_ACTION
        self.TICKETS_QUANTITY = QuickBuyLocators.TICKETS_QUANTITY
        self.TICKETS_PRICE = QuickBuyLocators.TICKETS_PRICE
        self.PAY_BUTTON_QUICK_BUY_CART = QuickBuyLocators.PAY_BUTTON
        self.SHOWCASE_AREA = ShowcaseLocators.AREA
        self.PREMIER_LOTTERY = ShowcaseLocators.PREMIER_LOTTERY

        # Локаторы класса AuthLocators
        self.LOGIN_FIELD = AuthLocators.LOGIN_FIELD
        self.PASSWORD_FIELD = AuthLocators.PASSWORD_FIELD
        self.ENTER_BUTTON = AuthLocators.ENTER_BUTTON
        self.LOGIN_MODAL_TITLE = AuthLocators.LOGIN_MODAL_TITLE

    def log_in(self) -> None:
        self.click_my_tickets_header_button()
        self.switch_to_default_content()

        self.send_keys_by_locator(self.LOGIN_FIELD, self.LOGIN)
        self.send_keys_by_locator(self.PASSWORD_FIELD, self.PASSWORD)
        self.click_element(self.ENTER_BUTTON)
        time.sleep(1)

        self.switch_to_nl_iframe_and_wait()

    def click_my_tickets_header_button(self) -> None:
        self.click_element(self.MY_TICKETS_BUTTON)

    def add_first_lottery_in_quick_buy(self) -> None:
        self.click_element(self.QUICK_LOTTERIES[0])

    def press_pay_button_quick_buy(self) -> None:
        self.click_element(self.PAY_BUTTON_QUICK_BUY_CART)

    def get_logging_modal_title(self) -> str:
        """
        Returns: Заголовок модального окна
        """
        self.switch_to_default_content()
        return self.find_element(self.LOGIN_MODAL_TITLE).text

    def click_few_times_on_element_by_locator(self, locator, counts) -> None:
        element = self.find_element(locator)
        for count in range(counts):
            element.click()

    def click_and_wait_on_element_by_locator(self, locator) -> None:
        element = self.find_element(locator)
        element.click()
        # TODO: Добавить явное ожидание
        time.sleep(1)

    def get_elements_count_in_quick_buy(self) -> int:
        return self.get_elements_count(self.QUICK_BUY_AREA)

    def get_elements_count_in_showcase(self) -> int:
        return self.get_elements_count(self.SHOWCASE_AREA)

    def add_all_lottery_in_quick_buy(self) -> None:
        self.click_and_wait_on_element_by_locator(self.QUICK_LOTTERIES[0])
        self.click_and_wait_on_element_by_locator(self.QUICK_LOTTERIES[1])
        self.click_and_wait_on_element_by_locator(self.RIGHT_ARROW_ACTION)
        self.click_and_wait_on_element_by_locator(self.QUICK_LOTTERIES[2])
        self.click_and_wait_on_element_by_locator(self.RIGHT_ARROW_ACTION)
        self.click_and_wait_on_element_by_locator(self.QUICK_LOTTERIES[3])
        self.click_and_wait_on_element_by_locator(self.LEFT_ARROW_ACTION)
        self.click_and_wait_on_element_by_locator(self.LEFT_ARROW_ACTION)

    def get_cart_info_in_quick_buy(self) -> tuple[str, str]:
        """
        Returns: Количество билетов и цена билетов из корзины
        """
        tickets_quantity = self.find_element(self.TICKETS_QUANTITY).text
        tickets_price = self.find_element(self.TICKETS_PRICE).text
        return tickets_quantity, tickets_price

    def add_tickets_in_quick_cart(self, amount) -> None:
        self.click_few_times_on_element_by_locator(self.LOTTERY_1_PLUS_BUTTON, amount)

    def remove_tickets_in_quick_cart(self, amount) -> None:
        self.click_few_times_on_element_by_locator(self.LOTTERY_1_MINUS_BUTTON, amount)
