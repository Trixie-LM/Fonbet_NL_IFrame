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
        with allure.step('Заголовок в модальном окне "Вход в Личный кабинет"'):
            assert open_browser.auth_via_button_my_tickets() in ('Вход в Личный кабинет', 'Log in to My Account')

    @allure.title('Авторизация через меню быстрой покупки')
    @allure.tag('smoke', 'regress')
    def test_auth_via_quick_buy(self, open_browser):
        logging_modal_title = open_browser.auth_via_quick_buy()

        with allure.step('Заголовок в модальном окне "Вход в Личный кабинет"'):
            assert logging_modal_title in ('Вход в Личный кабинет', 'Log in to My Account')

    @allure.title('Количество лотерей в меню быстрой покупки')
    @allure.tag('smoke', 'regress')
    def test_elements_count_quick_buy(self, open_browser):
        with allure.step("Получение количества лотерей в меню быстрой покупки"):
            count = open_browser.get_elements_count_in_quick_buy()

        with allure.step("В меню быстрой покупки находятся 4 лотереи"):
            assert 4 == count, "Количество лотерей в меню быстрой покупки не равно 4"

    @allure.title('Добавление в корзину билетов каждой лотереи')
    @allure.tag('smoke', 'regress')
    def test_get_tickets_every_lottery_in_cart_quick_buy(self, open_browser):
        with allure.step("Добавление всех билетов в корзину быстрой покупки"):
            open_browser.add_all_lottery_in_quick_buy()

        with allure.step("Возврат необходимых переменных функции"):
            tickets_quantity, tickets_price, left_arrow_status = open_browser.get_text_in_cart_in_quick_buy()

        with allure.step("В корзине быстрой покупки находятся 4 билета"):
            assert tickets_quantity == 'x 4'

        with allure.step("В корзине быстрой покупки находятся билеты на сумму 700 рублей"):
            assert tickets_price == '700 ₽'

        with allure.step("В меню быстрой покупки левая стрелка неактивна"):
            assert left_arrow_status == 'true'

    @allure.title('Добавление и удаление билетов из корзины')
    @allure.tag('smoke', 'regress')
    def test_add_and_remove_some_tickets_in_cart_quick_buy(self, open_browser):
        with allure.step("Добавление 30 билетов в корзину быстрой покупки"):
            open_browser.click_few_times_on_element_by_locator(QuickBuyLocators.LOTTERY_1_PLUS_BUTTON, 30)

        with allure.step("Удаление 7 билетов из корзины быстрой покупки"):
            open_browser.click_few_times_on_element_by_locator(QuickBuyLocators.LOTTERY_1_MINUS_BUTTON, 7)

        with allure.step("Возврат необходимых переменных функции"):
            tickets_quantity = open_browser.find_element(QuickBuyLocators.TICKETS_QUANTITY).text

        with allure.step("В корзине быстрой покупки находятся 23 билета"):
            assert tickets_quantity == 'x 23'

        # TODO: добавить проверку итоговую сумму

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

        with allure.step("Получение количества лотерей на витрине"):
            count = open_browser.get_elements_count(ShowcaseLocators.AREA)

        with allure.step("На витрине находятся 4 лотереи"):
            assert 4 == count, "Количество лотерей на витрине не равно 4"

