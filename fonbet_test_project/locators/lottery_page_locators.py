class LotteryPageLocators:
    class Alert:
        # Пустая покупка
        EMPTY_BUY = ('xpath', '//*[@class="sc-362e80da-0 hQkTIo"]/child :: *')

    class Tickets:
        # Ближайший тираж
        NEAREST_DRAW = ('xpath', '//span[contains(text(),"Ближайший тираж:")]/following-sibling::span')
        NEAREST_DRAW_TEXT = ('xpath', '//span[contains(text(),"Ближайший тираж:")]')
        SELECT_DRAW_BUTTON = ('xpath', '//p[text()="Выберите тираж"]/parent::*//button')
        SELECT_DRAW_BUTTON_TEXT = ('xpath', '//p[text()="Выберите тираж"]/parent::*//button//p')
        ADD_MORE_TICKET_BUTTON = ('xpath', '//*[text()="Добавить еще билет"]/parent::*')

    class GenerateCombination:
        # Кнопки генерации комбинации
        ALL_RANDOM_NUMBERS_BUTTON = ('xpath', '//*[@data-tip="Случайно"]')
        ODD_NUMBERS_BUTTON = ('xpath', '//*[@data-tip="Нечетные числа"]')
        EVEN_NUMBERS_BUTTON = ('xpath', '//*[@data-tip="Четные числа"]')
        TOP_HALF_FIELD_BUTTON = ('xpath', '//*[@data-tip="Случайные из верхней половины поля"]')
        BOTTOM_HALF_FIELD_BUTTON = ('xpath', '//*[@data-tip="Случайные из нижней половины поля"]')
        LAST_NUMBER_FIRST_FIELD = ('xpath', '(//*[@data-field="field1"])[last()]/child :: *')
        LAST_NUMBER_SECOND_FIELD = ('xpath', '(//*[@data-field="field2"])[last()]/child :: *')

    class Draws:
        # Выбор количества тиражей
        DRAWS = ('xpath', '//span[text()="Выберите количество тиражей"]/parent::*/div[1]/div')
        CANCEL_BUTTON = ('xpath', '//span[text()="Выберите количество тиражей"]/parent::*/div[2]/button[1]')
        CONFIRM_BUTTON = ('xpath', '//span[text()="Выберите количество тиражей"]/parent::*/div[2]/button[2]')

    class HowToPlay:
        # Как играть
        TAB = ('xpath', "//span[contains(text(),'Как играть?')]/parent::*")
        LOTTERY_INFO_AREA = ('xpath', "(//p[contains(text(),'Мин. цена билета')]/parent::*/parent::*/parent::*//span)")
        HOW_TO_PLAY_AREA = ('xpath', "(//*[@class='textPrimary'])")
        LEGAL_INFO_AREA = ('xpath', "((//*[@class='mb32'])//*[text()])")

    class AnotherLottery:
        # Другая лотерея
        AREA = ('xpath', '//*[@class="swiper-wrapper"]/child :: *')

    class Cart:
        # Корзина
        SELECTED_TICKETS_TEXT_LOCATOR = ('xpath', '//*[text()="Билетов"]')
        SELECTED_TICKETS_AMOUNT = ('xpath', '//*[text()="Билетов"]/parent::*/p')
        SELECTED_DRAWS_TEXT_LOCATOR = ('xpath', '(//*[text()="Количество тиражей"])[2]/parent::*/span[1]')
        SELECTED_DRAWS_AMOUNT = ('xpath', '(//*[text()="Количество тиражей"])[2]/parent::*/span[2]')
        TOTAL_TEXT = ('xpath', "//*[text()='Итого']/parent::*/div[2]")
        PAY_BUTTON = ('xpath', '//*[text()="Оплатить"]')

    class Payment:
        # Оплата
        TO_MY_TICKETS_BUTTON = ('xpath', "//p[contains(text(),'Перейти в мои билеты')]/parent::*/parent::*")
        STAY_ON_PAGE_BUTTON = ('xpath', "//p[contains(text(),'Остаться на странице')]/parent::*/parent::*")

    # Кнопка оплаты через CUPIS
    CUPIS_PAY_BUTTON = ('xpath', "//span[contains(text(),' Оплатить ')]")


lottery_page_locators = LotteryPageLocators
