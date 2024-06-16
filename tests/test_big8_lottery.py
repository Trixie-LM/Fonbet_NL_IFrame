import time
import allure
import pytest
from fonbet_test_project.utils import utils
from fonbet_test_project.database.db_queries import db
from fonbet_test_project.utils.utils import comparison_elements_to_expected_texts


PRODUCT_CODE = '104101'


@allure.feature('Лотерея Премьер')
@allure.story('Функциональность')
class TestFunctionality:

    @allure.title('Вызов окна авторизации')
    @allure.tag('smoke', 'regress')
    def test_authorization(self, open_browser, request):
        # GIVEN
        module_name = request.module.__name__.split('.')[-1]

        # WHEN
        with allure.step("Переход в раздел лотереи согласно названию тестового модуля"):
            locator = open_browser.get_lottery_locator_by_module_name(module_name)
            open_browser.navigate_to_lottery_section_by_locator(locator)

        with allure.step("Нажатие на кнопку для случайной генерации комбинации"):
            logging_modal_title = open_browser.auth_via_buy()

        # THEN
        with allure.step('Заголовок в модальном окне "Вход в Личный кабинет"'):
            assert logging_modal_title == 'Вход в Личный кабинет'

    @allure.title('Покупка одного билета')
    @allure.tag('smoke', 'regress')
    def test_buy_ticket(self, lottery_section):
        # GIVEN
        timestamp = utils.get_current_timestamp()

        # WHEN
        with allure.step("Нажатие на кнопку для случайной генерации комбинации"):
            lottery_section.generate_combination()

        with allure.step("Покупка билета"):
            lottery_section.purchase_confirmation_in_cupis()

        # THEN
        with allure.step("В БД найден 1 проданный билет с начала теста"):
            count = db.get_count_tickets_purchased_after_time(lottery_section.sensitive_data.OWNER_ID, timestamp)
            assert 1 == count, "Количество купленных билетов у клиента не равно 1"

    @allure.title('Покупка одной комбинации на все доступные тиражи')
    @allure.tag('smoke', 'regress')
    def test_buy_ticket_few_draws(self, lottery_section):
        # GIVEN
        timestamp = utils.get_current_timestamp()
        count_draws_db = db.get_count_tickets_sale_draws_by_product_code(PRODUCT_CODE)

        # WHEN
        with allure.step("Нажатие на кнопку для случайной генерации комбинации"):
            lottery_section.generate_combination()

        with (allure.step("Нажатие на кнопку выбора тиражей")):
            lottery_section.click_element(lottery_section.lottery_page_locators.Tickets.SELECT_DRAW_BUTTON)

        with allure.step("Выбор всех тиражей"):
            for draw_number in range(2, count_draws_db + 1):
                draws_xpath = lottery_section.lottery_page_locators.Draws.DRAWS[1]
                draw = f'{draws_xpath}[{draw_number}]'
                lottery_section.click_element(('xpath', draw))

        with allure.step("Нажатие на кнопку подтверждения выбранных тиражей"):
            lottery_section.click_element(lottery_section.lottery_page_locators.Draws.CONFIRM_BUTTON)

        with allure.step("Покупка билета"):
            lottery_section.purchase_confirmation_in_cupis()

        # THEN
        with allure.step(f"Подсчет количества купленных билетов в БД за период начало теста: {timestamp}"):
            count_tickets = db.get_count_tickets_purchased_after_time(lottery_section.sensitive_data.OWNER_ID, timestamp)

        with allure.step("В БД найдены все проданные билеты с начала теста"):
            assert count_tickets == count_draws_db

    @allure.title('Покупка нескольких билетов одновременно')
    @allure.tag('smoke', 'regress')
    def test_ticket(self, lottery_section):
        # GIVEN
        timestamp = utils.get_current_timestamp()

        # WHEN
        with allure.step("Добавление 10 билетов в корзину"):
            lottery_section.select_few_tickets(10)

        with allure.step("Покупка билета"):
            lottery_section.purchase_confirmation_in_cupis()

        # THEN
        with allure.step(f"В БД найдены все проданные билеты с начала теста: {timestamp}"):
            count_tickets = db.get_count_tickets_purchased_after_time(lottery_section.sensitive_data.OWNER_ID, timestamp)
            assert count_tickets == 10

    @allure.title('Покупка билета с повышенной ставкой')
    @allure.tag('smoke', 'regress')
    def test_buy_ticket_increased_rate(self, lottery_section):
        # GIVEN
        timestamp = utils.get_current_timestamp()

        # WHEN
        with allure.step("Генерация комбинации"):
            lottery_section.click_element(lottery_section.lottery_page_locators.GenerateCombination.TOP_HALF_FIELD_BUTTON)
            time.sleep(0.5)

        with allure.step("Добавление по одному числу на каждом поле"):
            lottery_section.click_element(lottery_section.lottery_page_locators.GenerateCombination.LAST_NUMBER_FIRST_FIELD)
            lottery_section.click_element(lottery_section.lottery_page_locators.GenerateCombination.LAST_NUMBER_SECOND_FIELD)
            time.sleep(0.5)

        with allure.step("Покупка билета"):
            lottery_section.purchase_confirmation_in_cupis()

        # THEN
        with allure.step(f"В БД найдены все проданные билеты с начала теста: {timestamp}"):
            count_tickets = db.get_count_tickets_purchased_after_time(lottery_section.sensitive_data.OWNER_ID, timestamp)
            assert count_tickets == 1


@allure.feature('Лотерея Премьер')
class TestDisplaying:

    @allure.story('Отображение содержания на вкладке "Игра"')
    class TestGameTab:

        @allure.title('Текст в корзине по умолчанию')
        @allure.tag('smoke', 'regress')
        def test_default_text_in_cart(self, lottery_section):
            # THEN
            with allure.step("Проверка информации в корзине по умолчанию"):
                cart_info = lottery_section.get_cart_info()
                assert ("Билетов", 0, "Количество тиражей", 0, 0) == cart_info

        @allure.title('Дата ближайшего тиража')
        @allure.tag('smoke', 'regress')
        def test_nearest_draw(self, lottery_section):
            # GIVEN
            nearest_draw_db = db.get_nearest_draw_date(PRODUCT_CODE)

            # THEN
            with allure.step("Сравнение ближайшего тиража в БД и отображенного на UI"):
                nearest_draw_ui = lottery_section.get_nearest_draw_text()
                assert nearest_draw_db == nearest_draw_ui

        @allure.title('Отображение всех доступных тиражей')
        @allure.tag('smoke', 'regress')
        def test_count_draws(self, lottery_section):
            # GIVEN
            count_draws_db = db.get_count_tickets_sale_draws_by_product_code(PRODUCT_CODE)

            # WHEN
            with allure.step("Генерация случайной комбинации"):
                lottery_section.generate_combination()

            with allure.step("Нажатие на кнопку выбора тиражей"):
                lottery_section.draw_selection()

            # THEN
            with allure.step("Сравнение доступных тиражей в БД и отображенных на UI"):
                draws_count = lottery_section.get_draws_count()
                assert count_draws_db == draws_count, "Количество тиражей не сходится"

        @allure.title('Отображение в корзине всех выбранных тиражей на одну комбинацию')
        @allure.tag('smoke', 'regress')
        def test_select_few_draws(self, lottery_section):
            # GIVEN
            ticket_price = int(db.get_ticket_price_by_product_code(PRODUCT_CODE))
            count_draws_db = db.get_count_tickets_sale_draws_by_product_code(PRODUCT_CODE)

            # WHEN
            with allure.step("Генерация случайной комбинации"):
                lottery_section.generate_combination()

            with allure.step("Нажатие на кнопку выбора тиражей"):
                lottery_section.draw_selection()

            with allure.step("Выбор всех тиражей"):
                lottery_section.select_draws(count_draws_db)

            with allure.step("Нажатие на кнопку подтверждения выбранных тиражей"):
                lottery_section.press_confirm_button_selected_draws()

            # THEN
            total_price = ticket_price * count_draws_db

            with (allure.step("Проверка итоговой информации в корзине")):
                cart_info = lottery_section.get_cart_info()
                assert ("Билетов", 1, "Количество тиражей", count_draws_db, total_price) == cart_info

        @allure.title('Покупка без выбора комбинации')
        @allure.tag('smoke', 'regress')
        def test_empty_buy_ticket(self, lottery_section):
            # WHEN
            with allure.step("Нажатие на кнопку \"Оплатить\""):
                lottery_section.press_pay_button_in_cart()

            # THEN
            with allure.step("Проверка алерта при покупки пустой корзины"):
                alert_text = lottery_section.get_alert_text()
                assert "Заполните хотя бы один билет" == alert_text

        @allure.title('Отображение суммы билета с повышенной ставкой')
        @allure.tag('smoke', 'regress')
        def test_buy_ticket_increased_rate(self, lottery_section):
            # WHEN
            with allure.step("Генерация комбинации"):
                lottery_section.generate_combination_top_half_field()

            with allure.step("Добавление по одному числу на каждом поле"):
                lottery_section.add_last_numbers_in_2_fields()

            # THEN
            with allure.step("Проверка итоговой информации в корзине"):
                cart_info = lottery_section.get_cart_info()
                assert ("Билетов", 1, "Количество тиражей", 1, 3600) == cart_info

        @allure.title('Количество лотерей в блоке "Другие лотереи"')
        @allure.tag('smoke', 'regress')
        def test_get_another_lottery_menu_items_count(self, lottery_section):
            # WHEN
            with allure.step("Скролл к блоку \"Другие лотереи\""):
                lottery_section.scroll_to_another_lottery_menu()

            # THEN
            with allure.step('В блоке "Другие лотереи" находятся 3 лотереи'):
                another_lottery = lottery_section.count_elements_another_lottery_menu()
                assert 3 == another_lottery, "Количество лотерей в блоке других лотерей не равно 3"

    @allure.story('Отображение содержания на вкладке "Как играть?"')
    class TestHowToPlayTab:

        @allure.title('Блок "Информация о лотереи"')
        @allure.tag('smoke', 'regress')
        def test_lottery_info_area(self, lottery_section):
            # GIVEN
            with allure.step("Переход во вкладку \"Как играть?\""):
                lottery_section.click_on_how_to_play_tab()

            # WHEN
            with allure.step("Получение списка элементов в блоке информации о лотереи"):
                lottery_info_elements = lottery_section.get_lottery_info_elements()

            # THEN
            expected_texts = [
                '200 ₽',
                'Ежедневно, каждые 15 мин¹',
                '70%',
                'Числовая'
            ]

            # Проверяем текст каждого элемента
            with allure.step("Сравнение ожидаемого текста с полученным"):
                comparison_elements_to_expected_texts(lottery_info_elements, expected_texts)

        @allure.title('Блок "Как играть?"')
        @allure.tag('smoke', 'regress')
        def test_how_to_play_area(self, lottery_section):
            # GIVEN
            with allure.step("Переход во вкладку \"Как играть?\""):
                lottery_section.click_on_how_to_play_tab()

            # WHEN
            with allure.step("Получение списка элементов в блоке лотереи \"Как играть?\""):
                how_to_play_elements = lottery_section.get_how_to_play_elements()

            # THEN
            expected_texts = [
                'Перед вами лотерейный билет с двумя игровыми полями.',
                'Заполните первое игровое поле, выбрав восемь чисел от 1 до 20. Повторяться нельзя.',
                'Во втором игровом поле выберите число от 1 до 4.',
                'Оплатите билет и участвуйте в розыгрыше. Билет будет доступен в вашем личном кабинете.',
                'Желаем удачи!'
            ]

            # Проверяем текст каждого элемента
            with allure.step("Сравнение ожидаемого текста с полученным"):
                comparison_elements_to_expected_texts(how_to_play_elements, expected_texts)

        @allure.title('Блок "Правовая информация"')
        @allure.tag('smoke', 'regress')
        def test_legal_info_area(self, lottery_section):
            # GIVEN
            with allure.step("Переход во вкладку \"Как играть?\""):
                lottery_section.click_on_how_to_play_tab()

            # WHEN
            with allure.step("Получение списка элементов в блоке лотереи \"Как играть?\""):
                legal_info_elements = lottery_section.get_legal_info_elements()

            # THEN
            expected_texts = [
                '«ВГЛ-4Т Спорт Союз», алгоритм определения выигрышей №10, таблица 16.',
                'Срок проведения лотереи — до 29 августа 2034 г.',
                'Призовой фонд — 70% от выручки.',
                'Лотерея проводится на основании распоряжения Правительства Российской Федерации от 29 августа 2019 г. N 1921-р.',
                'Организатор лотереи: Министерство финансов Российской Федерации',
                'Оператор лотереи: ООО «Спортивные Лотереи», тел. 8 800 333-7-333',
                '8 800 333-7-333',
                'Место проведения розыгрыша призового фонда тиража — г. Москва.',
                'Результаты розыгрыша тиража публикуются на сайтах https://nloto.ru и www.en-gzt.ru в течение 10 дней после его проведения.',
                'https://nloto.ru',
                'www.en-gzt.ru',
                'Условия проведения лотереи размещены на сайте https://nloto.ru и http://publication.pravo.gov.ru'
            ]

            # Проверяем текст каждого элемента
            with allure.step("Сравнение ожидаемого текста с полученным"):
                comparison_elements_to_expected_texts(legal_info_elements, expected_texts)
