class QuickBuyLocators:
    # Область быстрого заказа
    AREA = ('xpath', '(//*[@class="swiper-wrapper"])[2]/child :: *')

    # Лотереи в области быстрого заказа
    LOTTERY_1 = ('xpath', '(//*[@class="swiper-wrapper"])[2]/div[1]')
    LOTTERY_2 = ('xpath', '(//*[@class="swiper-wrapper"])[2]/div[2]')
    LOTTERY_3 = ('xpath', '(//*[@class="swiper-wrapper"])[2]/div[3]')
    LOTTERY_4 = ('xpath', '(//*[@class="swiper-wrapper"])[2]/div[4]')

    # Кнопки изменения количества билетов для первой лотереи
    LOTTERY_1_MINUS_BUTTON = ('xpath', '(//*[@class="swiper-wrapper"])[2]/div[1]//button[1]')
    LOTTERY_1_PLUS_BUTTON = ('xpath', '(//*[@class="swiper-wrapper"])[2]/div[1]//button[2]')

    # Стрелки для перемещения по списку лотерей
    LEFT_ARROW_ACTION = ('xpath', '(//button)[11]')
    LEFT_ARROW_STATUS = ('xpath', '(//button)[11]/parent::*')
    RIGHT_ARROW_ACTION = ('xpath', '(//button)[12]')
    RIGHT_ARROW_STATUS = ('xpath', '(//button)[12]/parent::*')

    # Количество билетов и их цена
    TICKETS_QUANTITY = ('xpath', '(//*[@class="sc-559b9dc4-5 hesXEM mr4 ml4"])[1]')
    TICKETS_PRICE = ('xpath', '(//*[@class="sc-559b9dc4-5 hesXEM mr4 ml4"])[2]')

    # Кнопка оплаты
    PAY_BUTTON = ('xpath', '(//button)[13]')


class ShowcaseLocators:
    # Область витрины
    AREA = ('xpath', "//h2[contains(text(),'заполняйте, побеждайте!')]/following-sibling::div/div/child::*")

    # Лотереи на витрине
    SHOWCASE = '//*[text()=" заполняйте, побеждайте!"]/parent::*'
    PREMIER_LOTTERY = ('xpath', f'{SHOWCASE}//*[@href="/lottery/digital-4x20-premier"]')
    BIG8_LOTTERY = ('xpath', f'{SHOWCASE}//*[@href="/lottery/digital-8x20-big8"]')
    LOTTERY_4X4 = ('xpath', f'{SHOWCASE}//*[@href="/lottery/bingo-4x4-2"]')
    TURNIR = ('xpath', f'{SHOWCASE}//*[@href="/lottery/turnir"]')
