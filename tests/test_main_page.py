import allure

from data.sensitive_data import SensitiveData
from fonbet_test_project.database.db_queries import db
from fonbet_test_project.locators import QuickBuyLocators, ShowcaseLocators
from fonbet_test_project.utils import utils


@allure.feature('Главная страница')
@allure.story('Функциональность')
class TestFunctionality:

    @allure.title('Авторизация через нажатие кнопки "Мои билеты"')
    @allure.tag('smoke', 'regress')
    def test_auth_via_button_my_tickets(self, open_browser):
        with allure.step('Нажатие на кнопку "Мои билеты"'):
            open_browser.click_my_tickets_header_button()

        with allure.step('Получение текста заголовка в открывшемся модальном окне'):
            logging_modal_title = open_browser.get_logging_modal_title()

        with allure.step('Заголовок в модальном окне "Вход в Личный кабинет"'):
            assert logging_modal_title in ('Вход в Личный кабинет', 'Log in to My Account')

    @allure.title('Авторизация через меню быстрой покупки')
    @allure.tag('smoke', 'regress')
    def test_auth_via_quick_buy(self, open_browser):
        with allure.step('Покупка билета через меню быстрой покупки'):
            open_browser.add_first_lottery_in_quick_buy()
            open_browser.press_pay_button_quick_buy()

        with allure.step('Получение текста заголовка в открывшемся модальном окне'):
            logging_modal_title = open_browser.get_logging_modal_title()

        with allure.step('Заголовок в модальном окне "Вход в Личный кабинет"'):
            assert logging_modal_title in ('Вход в Личный кабинет', 'Log in to My Account')

    @allure.title('Количество лотерей в меню быстрой покупки')
    @allure.tag('smoke', 'regress')
    def test_elements_count_quick_buy(self, open_browser):
        with allure.step("Получение количества лотерей в меню быстрой покупки"):
            lottery_amount = open_browser.get_elements_count_in_quick_buy()

        with allure.step("В меню быстрой покупки находятся 4 лотереи"):
            assert 4 == lottery_amount, "Количество лотерей в меню быстрой покупки не равно 4"

    @allure.title('Добавление в корзину билетов каждой лотереи')
    @allure.tag('smoke', 'regress')
    def test_get_tickets_every_lottery_in_cart_quick_buy(self, open_browser):
        with allure.step("Добавление всех билетов в корзину быстрой покупки"):
            open_browser.add_all_lottery_in_quick_buy()

        with allure.step("Возврат необходимых переменных функции"):
            cart_info_ui = open_browser.get_cart_info_in_quick_buy()

        with allure.step("Сравнение данных"):
            assert cart_info_ui == ('x 4', '700 ₽')

    @allure.title('Добавление и удаление билетов из корзины')
    @allure.tag('smoke', 'regress')
    def test_add_and_remove_some_tickets_in_cart_quick_buy(self, open_browser):
        with allure.step("Добавление 30 билетов в корзину быстрой покупки"):
            open_browser.add_tickets_in_quick_cart(30)

        with allure.step("Удаление 7 билетов из корзины быстрой покупки"):
            open_browser.remove_tickets_in_quick_cart(7)

        with allure.step("Возврат необходимых переменных функции"):
            cart_info_ui = open_browser.get_cart_info_in_quick_buy()
            tickets_quantity = cart_info_ui[0]

        with allure.step("Сравнение данных"):
            assert tickets_quantity == 'x 23'

    @allure.title('Покупка билетов')
    @allure.tag('smoke', 'regress')
    def test_buy_tickets_in_quick_buy(self, open_browser):
        timestamp = utils.get_current_timestamp()

        with allure.step("Авторизация"):
            open_browser.log_in()

        with allure.step("Добавление всех билетов в корзину быстрой покупки"):
            open_browser.add_all_lottery_in_quick_buy()

        with allure.step("Покупка билета"):
            open_browser.purchase_confirmation_in_cupis()

        with allure.step("Подсчет количества купленных билетов в БД за период начало теста"):
            count = db.get_count_tickets_purchased_after_time(SensitiveData.OWNER_ID, timestamp)

        with allure.step("В БД найдено 4 проданных билета с начала теста"):
            assert 4 == count, "Количество купленных билетов у клиента не равно 4"

    @allure.title('Количество лотерей на витрине')
    @allure.tag('smoke', 'regress')
    def test_get_elements_count_showcase(self, open_browser):
        with allure.step("Скролл в самый низ страницы"):
            open_browser.scroll_to_bottom()

        with allure.step("На витрине находятся 4 лотереи"):
            assert 4 == open_browser.get_elements_count_in_showcase(), "Количество лотерей на витрине не равно 4"
