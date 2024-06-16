from config.config import connection


class DB:
    def get_count_tickets_purchased_after_time(self, owner_id: str, sold_time: str) -> int:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT 
                    is_sold, sold_time, number 
                FROM number_handler.number_ticket
                where 
                    true
                    and owner_id = '{owner_id}'
                    and sold_time > '{sold_time}'
                union
                SELECT
                    is_sold, sold_time, number
                FROM bingo_handler.bingo_ticket bt
                where 
                    true
                    and owner_id = '{owner_id}'
                    and sold_time > '{sold_time}'
                union
                SELECT
                    is_sold, sold_time, number
                FROM betting_handler.betting_ticket
                where 
                    true
                    and owner_id = '{owner_id}'
                    and sold_time > '{sold_time}'
                """
            )
            response = len(cursor.fetchall())

        return response

    def get_count_tickets_sale_draws_by_product_code(self, product_code: str) -> str:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT   
                     count(*)
                FROM scheduler.draw where product_id in   
                    (select id from configurator.product where product_code = '{product_code}')   
                and status IN (
                      'TICKETS_SALE'
                  )   
                """
            )
            # Максимум 10 тиражей
            response = min(cursor.fetchall()[0][0], 10)

        return response

    def get_ticket_price_by_product_code(self, product_code: str) -> str:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                select 
                    settings ->> 'price'
                from configurator.product 
                where 
                    product_code = '{product_code}'
                """
            )
            response = cursor.fetchall()[0][0]

        return response

    def get_nearest_draw_date(self, product_code) -> str:
        # owner_id соответствует пользователю 4062359
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT   
                     draw_date
                FROM scheduler.draw where product_id in   
                    (select id from configurator.product where product_code = '{product_code}')   
                and status IN (
                      'TICKETS_SALE'
                  )   
                order by draw_date 
                limit 1 ;
                """
            )
            response = cursor.fetchall()[0][0]

            formatted_date = response.strftime("%d %b., в %H:%M")

            months_translation = {
                'Jan.': 'янв.',
                'Feb.': 'фев.',
                'Mar.': 'мар.',
                'Apr.': 'апр.',
                'May': 'мая',
                'Jun.': 'июня',
                'Jul.': 'июля',
                'Aug.': 'авг.',
                'Sep.': 'сен.',
                'Oct.': 'окт.',
                'Nov.': 'ноя.',
                'Dec.': 'дек.'
            }

            # Замена английских названий месяцев на русские
            for eng_month, rus_month in months_translation.items():
                formatted_date = formatted_date.replace(eng_month, rus_month)

        return formatted_date


db = DB()
