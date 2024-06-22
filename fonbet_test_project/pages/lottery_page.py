import time
import random

import allure

from fonbet_test_project.pages.payment_widget import PaymentWidget
from fonbet_test_project.locators import LotteryPageLocators, AuthLocators


class Lottery(PaymentWidget):
    def __init__(self, driver, wait, action):
        super().__init__(driver, wait, action)
        self.driver = driver
        self.wait = wait
        self.action = action

        # Локаторы класса AuthLocators
        self.LOGIN_MODAL_TITLE = AuthLocators.LOGIN_MODAL_TITLE

        # Локаторы класса LotteryPageLocators.GenerateCombination
        self.ALL_RANDOM_NUMBERS_BUTTON = LotteryPageLocators.GenerateCombination.ALL_RANDOM_NUMBERS_BUTTON
        self.ODD_NUMBERS_BUTTON = LotteryPageLocators.GenerateCombination.ODD_NUMBERS_BUTTON
        self.EVEN_NUMBERS_BUTTON = LotteryPageLocators.GenerateCombination.EVEN_NUMBERS_BUTTON
        self.TOP_HALF_FIELD_BUTTON = LotteryPageLocators.GenerateCombination.TOP_HALF_FIELD_BUTTON
        self.BOTTOM_HALF_FIELD_BUTTON = LotteryPageLocators.GenerateCombination.BOTTOM_HALF_FIELD_BUTTON
        self.LAST_NUMBER_FIRST_FIELD = LotteryPageLocators.GenerateCombination.LAST_NUMBER_FIRST_FIELD
        self.LAST_NUMBER_SECOND_FIELD = LotteryPageLocators.GenerateCombination.LAST_NUMBER_SECOND_FIELD

        # Локаторы класса LotteryPageLocators.Tickets
        self.SELECT_DRAW_BUTTON = LotteryPageLocators.Tickets.SELECT_DRAW_BUTTON
        self.NEAREST_DRAW = LotteryPageLocators.Tickets.NEAREST_DRAW
        self.ADD_MORE_TICKET_BUTTON = LotteryPageLocators.Tickets.ADD_MORE_TICKET_BUTTON

        # Локаторы класса LotteryPageLocators.Draws
        self.DRAWS = LotteryPageLocators.Draws.DRAWS
        self.CONFIRM_BUTTON = LotteryPageLocators.Draws.CONFIRM_BUTTON

        # Локаторы класса LotteryPageLocators.Cart
        self.SELECTED_TICKETS_TEXT_LOCATOR = LotteryPageLocators.Cart.SELECTED_TICKETS_TEXT_LOCATOR
        self.SELECTED_TICKETS_AMOUNT = LotteryPageLocators.Cart.SELECTED_TICKETS_AMOUNT
        self.SELECTED_DRAWS_TEXT_LOCATOR = LotteryPageLocators.Cart.SELECTED_DRAWS_TEXT_LOCATOR
        self.SELECTED_DRAWS_AMOUNT = LotteryPageLocators.Cart.SELECTED_DRAWS_AMOUNT
        self.TOTAL_TEXT = LotteryPageLocators.Cart.TOTAL_TEXT

        # Локаторы класса LotteryPageLocators.AnotherLottery
        self.AREA = LotteryPageLocators.AnotherLottery.AREA

        # Локаторы класса LotteryPageLocators.Alert
        self.EMPTY_BUY = LotteryPageLocators.Alert.EMPTY_BUY

        # Локаторы класса LotteryPageLocators.HowToPlay
        self.HOW_TO_PLAY_TAB = LotteryPageLocators.HowToPlay.TAB
        self.LOTTERY_INFO_AREA = LotteryPageLocators.HowToPlay.LOTTERY_INFO_AREA
        self.HOW_TO_PLAY_AREA = LotteryPageLocators.HowToPlay.HOW_TO_PLAY_AREA
        self.LEGAL_INFO_AREA = LotteryPageLocators.HowToPlay.LEGAL_INFO_AREA

    def navigate_to_lottery_section_by_locator(self, locator):
        self.scroll_to_element(locator)
        self.click_element(locator)
        time.sleep(0.5)

    def auth_via_buy(self):
        self.generate_combination()

        self.press_pay_button_in_cart()

        self.switch_to_default_content()

        logging_modal_title = self.find_element(self.LOGIN_MODAL_TITLE).text

        return logging_modal_title

    def click_on_how_to_play_tab(self):
        self.click_element(self.HOW_TO_PLAY_TAB)

    def generate_combination(self):
        locators = [
            self.ALL_RANDOM_NUMBERS_BUTTON,
            self.ODD_NUMBERS_BUTTON,
            self.EVEN_NUMBERS_BUTTON,
            self.TOP_HALF_FIELD_BUTTON,
            self.BOTTOM_HALF_FIELD_BUTTON
        ]
        locator = random.choice(locators)

        self.click_element(locator)

    def generate_top_half_combination(self):
        self.click_element(self.TOP_HALF_FIELD_BUTTON)
        time.sleep(0.5)

    def generate_combination_top_half_field(self):
        self.click_element(self.TOP_HALF_FIELD_BUTTON)
        time.sleep(0.5)

    def add_last_numbers_in_each_field(self):
        self.click_element(self.LAST_NUMBER_FIRST_FIELD)
        self.click_element(self.LAST_NUMBER_SECOND_FIELD)
        time.sleep(0.5)

    def draw_selection(self):
        self.click_element(self.SELECT_DRAW_BUTTON)

    def get_draws_count(self):
        return self.get_elements_count(self.DRAWS)

    def get_nearest_draw_text(self):
        return self.get_text_by_locator(self.NEAREST_DRAW)

    def select_draws(self, count):
        for draw_number in range(2, count + 1):
            draw = f'{self.DRAWS[1]}[{draw_number}]'
            self.click_element(('xpath', draw))

    def press_confirm_button_selected_draws(self):
        self.click_element(self.CONFIRM_BUTTON)

    def get_cart_info(self) -> tuple:
        """
        Получает информацию о выбранных билетах в корзине.

        Returns:
            tuple: Кортеж состоит из текста о выбранных билетах, количестве билетов, текста о выбранных тиражах,
                   количестве тиражей и общей цены.
        """
        # Получаем текст о выбранных билетах и количестве билетов
        tickets_text = self.get_text_by_locator(self.SELECTED_TICKETS_TEXT_LOCATOR)
        tickets_amount = int(self.get_text_by_locator(self.SELECTED_TICKETS_AMOUNT))

        # Получаем текст о выбранных тиражах и количестве тиражей
        draws_text = self.get_text_by_locator(self.SELECTED_DRAWS_TEXT_LOCATOR)
        draws_amount = int(self.get_text_by_locator(self.SELECTED_DRAWS_AMOUNT))

        # Получаем общую цену
        total_price_text = self.get_text_by_locator(self.TOTAL_TEXT)
        total_price = int(total_price_text.replace(" ", "").replace("₽", ""))

        return tickets_text, tickets_amount, draws_text, draws_amount, total_price

    def select_few_tickets(self, amount):
        for index in range(1, amount+1):
            all_random_numbers_button_by_index = ('xpath', f'({self.ALL_RANDOM_NUMBERS_BUTTON[1]})[{index}]')

            # Скролл к кнопке "Сгенерировать случайную комбинацию"
            self.scroll_to_element(all_random_numbers_button_by_index)

            # Клик по кнопке "Сгенерировать случайную комбинацию"
            self.click_element(all_random_numbers_button_by_index)

            if index != amount:
                # Скролл к кнопке "Добавить еще билет"
                self.scroll_to_element(self.ADD_MORE_TICKET_BUTTON)

                # Клик по кнопке "Добавить еще билет"
                self.click_element(self.ADD_MORE_TICKET_BUTTON)

    def scroll_to_another_lottery_menu(self):
        self.scroll_to_element(self.AREA)

    def count_elements_another_lottery_menu(self):
        count = self.get_elements_count(self.AREA)
        return count

    def get_alert_text(self):
        return self.get_text_by_locator(self.EMPTY_BUY)

    def get_lottery_info_elements(self):
        return self.find_elements(self.LOTTERY_INFO_AREA)

    def get_how_to_play_elements(self):
        return self.find_elements(self.HOW_TO_PLAY_AREA)

    def get_legal_info_elements(self):
        return self.find_elements(self.LEGAL_INFO_AREA)
