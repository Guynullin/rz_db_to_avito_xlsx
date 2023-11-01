import logging

from collect_cards.get_brands_models_avito import get_brands_models_avito
from info_bot import send_message
from collect_cards.parse_rim import parse_rim
from collect_cards.parse_tire import parse_tire
from collect_cards.parse_spring import parse_spring


def get_cards_from_db(conn):
    with conn.cursor() as curs:

        brands_models_dict_avito = get_brands_models_avito('https://autoload.avito.ru/format/tyres_make.xml')
        if brands_models_dict_avito == 0:
            send_message('ERROR\n brands_dict is empty')
            logging.error('brands_dict is empty')
            return 0
        
        cards_dict = {}
        
        # rims alloy + forged
        curs.execute("SELECT * FROM app_product WHERE LOWER(name) LIKE LOWER('%диск%') AND show=true")
        products = curs.fetchall()
        rims_id_list = []
        for prod in products:
            id = prod[0]
            rims_id_list.append(id)

        rims_id_list = list(map(str, rims_id_list))
        curs.execute(f"SELECT * FROM app_rim WHERE product_ptr_id IN ({','.join(rims_id_list)})")
        rim_rows = curs.fetchall()
        alloy_cards = parse_rim('alloy', products=products, rim_rows=rim_rows)
        if alloy_cards != 0:
            cards_dict['alloy'] = alloy_cards
        
        forged_cards = parse_rim('forged', products=products, rim_rows=rim_rows)
        if forged_cards != 0:
            cards_dict['forged'] = forged_cards

        curs.execute("SELECT * FROM app_brand")
        app_brand = curs.fetchall()
        brands_dict = {}
        for brand in app_brand:
            brands_dict[brand[0]] = brand[1]

        # tires
        curs.execute("SELECT * FROM app_product WHERE LOWER(name) LIKE LOWER('%шин%') AND show=true")
        products = curs.fetchall()
        tire_id_list = []
        for prod in products:
            id = prod[0]
            tire_id_list.append(id)
        tire_id_list = list(map(str, tire_id_list))
        curs.execute(f"SELECT * FROM app_tire WHERE product_ptr_id IN ({','.join(tire_id_list)})")
        tire_rows = curs.fetchall()
        tire_cards = parse_tire(products=products, tire_rows=tire_rows, brands=brands_dict, brands_avito=brands_models_dict_avito)
        if tire_cards != 0:
            cards_dict['tires'] = tire_cards

        # springs
        curs.execute("SELECT * FROM app_product WHERE typeof_id=7 AND show=true")
        products = curs.fetchall()
        spring_cards = parse_spring(products=products)
        if spring_cards != 0:
            cards_dict['springs'] = spring_cards

        
        if 'alloy' in cards_dict and 'forged' in cards_dict and 'tires' in cards_dict and 'springs' in cards_dict:
            return cards_dict
        else:
            logging.error('<get_cards_from_db> Cards dict not received')
            send_message(f"ERROR\nCards dict not received")
            return 0
        

        