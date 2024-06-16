import allure

from fonbet_test_project.database.db_queries import db
from fonbet_test_project.utils import utils


@allure.feature('Главная страница')
@allure.story('Функциональность')
class TestFunctionality:

    @allure.title('Авторизация через нажатие кнопки "Мои билеты"')
    @allure.tag('smoke', 'regress')
    def test_auth_via_button_my_tickets(self, open_browser):
        with allure.step('Заголовок в модальном окне "Вход в Личный кабинет"'):
            assert open_browser.auth_via_button_my_tickets() == 'Вход в Личный кабинет'

    @allure.title('Авторизация через меню быстрой покупки')
    @allure.tag('smoke', 'regress')
    def test_auth_via_quick_buy(self, open_browser):
        logging_modal_title = open_browser.auth_via_quick_buy()

        with allure.step('Заголовок в модальном окне "Вход в Личный кабинет"'):
            assert logging_modal_title == 'Вход в Личный кабинет'

    @allure.title('Количество лотерей в меню быстрой покупки')
    @allure.tag('smoke', 'regress')
    def test_elements_count_quick_buy(self, open_browser):
        with allure.step("Получение количества лотерей в меню быстрой покупки"):
            count = open_browser.get_elements_count(open_browser.main_page_locators.QuickBuy.AREA)

        with allure.step("В меню быстрой покупки находятся 4 лотереи"):
            assert 4 == count, "Количество лотерей в меню быстрой покупки не равно 4"

    @allure.title('Добавление в корзину билетов каждой лотереи')
    @allure.tag('smoke', 'regress')
    def test_get_tickets_every_lottery_in_cart_quick_buy(self, open_browser):
        with allure.step("Добавление всех билетов в корзину быстрой покупки"):
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LOTTERY_1)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LOTTERY_2)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.RIGHT_ARROW_ACTION)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LOTTERY_3)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.RIGHT_ARROW_ACTION)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LOTTERY_4)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LEFT_ARROW_ACTION)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LEFT_ARROW_ACTION)

        with allure.step("Возврат необходимых переменных функции"):
            tickets_quantity = open_browser.find_element(open_browser.main_page_locators.QuickBuy.TICKETS_QUANTITY).text
            tickets_price = open_browser.find_element(open_browser.main_page_locators.QuickBuy.TICKETS_PRICE).text
            left_arrow_status = open_browser.find_element(open_browser.main_page_locators.QuickBuy.LEFT_ARROW_STATUS).get_attribute('aria-disabled')

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
            open_browser.click_few_times_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LOTTERY_1_PLUS_BUTTON, 30)

        with allure.step("Удаление 7 билетов из корзины быстрой покупки"):
            open_browser.click_few_times_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LOTTERY_1_MINUS_BUTTON, 7)

        with allure.step("Возврат необходимых переменных функции"):
            tickets_quantity = open_browser.find_element(open_browser.main_page_locators.QuickBuy.TICKETS_QUANTITY).text

        with allure.step("В корзине быстрой покупки находятся 23 билета"):
            assert tickets_quantity == 'x 23'

        # TODO: добавить проверку итоговую сумму

    @allure.title('Покупка билетов')
    @allure.tag('smoke', 'regress')
    def test_buy_tickets_in_quick_buy(self, open_browser):
        timestamp = utils.get_current_timestamp()

        with allure.step("Авторизация"):
            open_browser.sign_in()

        with allure.step("Добавление всех билетов в корзину быстрой покупки"):
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LOTTERY_1)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LOTTERY_2)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.RIGHT_ARROW_ACTION)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LOTTERY_3)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.RIGHT_ARROW_ACTION)
            open_browser.click_and_wait_on_element_by_locator(open_browser.main_page_locators.QuickBuy.LOTTERY_4)

        with allure.step("Покупка билета"):
            open_browser.purchase_confirmation_in_cupis()

        with allure.step("Подсчет количества купленных билетов в БД за период начало теста"):
            count = db.get_count_tickets_purchased_after_time(open_browser.sensitive_data.OWNER_ID, timestamp)

        with allure.step("В БД найдено 4 проданных билета с начала теста"):
            assert 4 == count, "Количество купленных билетов у клиента не равно 4"

    @allure.title('Количество лотерей на витрине')
    @allure.tag('smoke', 'regress')
    def test_get_elements_count_showcase(self, open_browser):
        with allure.step("Скролл в самый низ страницы"):
            open_browser.scroll_to_bottom()

        with allure.step("Получение количества лотерей на витрине"):
            count = open_browser.get_elements_count(open_browser.main_page_locators.Showcase.AREA)

        with allure.step("На витрине находятся 4 лотереи"):
            assert 4 == count, "Количество лотерей на витрине не равно 4"

