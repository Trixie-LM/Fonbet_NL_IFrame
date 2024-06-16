from selenium.webdriver.support import expected_conditions as ec

from fonbet_test_project.pages.base_page import BasePage


class PaymentWidget(BasePage):
    def __init__(self, driver, wait, action):
        super().__init__(driver, wait, action)
        self.driver = driver
        self.wait = wait
        self.action = action

        # Локаторы класса IframeLocators
        self.nl_iframe = self.iframe_locators.NL_IFRAME
        self.first_cupis_iframe = self.iframe_locators.FIRST_CUPIS_IFRAME
        self.second_cupis_iframe = self.iframe_locators.SECOND_CUPIS_IFRAME

        # Локаторы класса LotteryPageLocators
        self.payment_button_in_cart = self.lottery_page_locators.Cart.PAY_BUTTON
        self.cupis_pay_button = self.lottery_page_locators.CUPIS_PAY_BUTTON
        self.to_my_tickets_button = self.lottery_page_locators.Payment.TO_MY_TICKETS_BUTTON

    def press_pay_button_in_cart(self):
        """
        Нажимает кнопку оплаты в корзине.
        """
        self.click_element(self.payment_button_in_cart)

    def purchase_confirmation_in_cupis(self):
        """
        Подтверждает покупку билетов через систему CUPIS.
        """
        # Нажимает кнопку оплаты в корзине
        self.press_pay_button_in_cart()

        self.driver.switch_to.default_content()

        # Переключается во внутренний iframe первого уровня
        self.switch_to_frame(self.first_cupis_iframe)
        # Переключается во внутренний iframe второго уровня
        self.switch_to_frame(self.second_cupis_iframe)

        # Нажимает кнопку оплаты в системе CUPIS
        self.click_element(self.cupis_pay_button)

        # Возвращается к основному содержимому страницы
        self.driver.switch_to.default_content()

        # Переключается во внутренний iframe на странице
        self.switch_to_frame(self.nl_iframe)

        # Ожидает появления кнопки "К моим билетам" после оплаты
        self.wait.until(ec.visibility_of_element_located(self.to_my_tickets_button))
