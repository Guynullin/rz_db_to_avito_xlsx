from difflib import SequenceMatcher

def similar(db: str, avito: str, p_ratio: float):
    db_model = db.lower()
    avito_model = avito.lower()
    ratio = SequenceMatcher(None, db_model, avito_model).ratio()

    if ratio > p_ratio:
        return True
    else:
        return False

def select_brand_model(db_brand, db_model: str, brands_avito: dict):
    
    card_brand = 'Nobrand'
    card_model = 'Nomodel'

    clear_model = db_model.replace('IV', '').replace('III', '').replace('SF-988', 'SF988')\
    .replace('EH 23', 'EH23').replace('5 STUDDED', '5').replace('ALL-TERRAIN A/T', 'All-Terrain T/A')\
    .replace('L-ZEAL 56','L-Zeal56').replace('CROCODILE M/T', 'CROCODILE').replace('(БЕЗ ШИПОВ)', '')\
    .replace('X-PRIVILO TX3', 'X-Privilo TX3').replace('WINTER I*PIKE RS 2 W429', "WINTER I'PIKE RS2").strip()

    if db_brand:
        if 'NOKIAN TYRES'.lower() in db_brand.lower():
            db_brand = 'NOKIAN TYRES'
        if 'KAMA'.lower() in db_brand.lower():
            db_brand = 'КАМА'
        if 'TORQUE TIRES'.lower() in db_brand.lower():
            db_brand = 'TORQUE'
        if 'TRI-ACE'.lower() in db_brand.lower():
            db_brand = 'Tri Ace'
        if 'RAZI TIRE'.lower() in db_brand.lower():
            db_brand = 'RAZI'
        if 'БАРНАУЛЬСКИЙ'.lower() in db_brand.lower():
            db_brand = 'Барнаул'
        if 'КИРОВСКИЙ'.lower() in db_brand.lower():
            db_brand = 'КШЗ'


        for key in brands_avito:
            if db_brand.lower() in key.lower():
                card_brand = key
                for av_model in brands_avito[key]:
                    if similar(clear_model, av_model, 0.9):
                        card_model = av_model                        
                        break
                if card_model == 'Nomodel':
                    for av_model in brands_avito[key]:
                        if similar(clear_model, av_model, 0.83):
                            card_model = av_model                        
                            break
                if card_model == 'Nomodel':
                    for av_model in brands_avito[key]:
                        if similar(clear_model, av_model, 0.56):
                            card_model = av_model                        
                            break
                break
            

    return {'brand': card_brand, 'model' : card_model}

def parse_tire(products: list, tire_rows: list, brands: dict, brands_avito: dict):
    cards = []

    for tire in tire_rows:
        card = {'id': tire[0]}
        card['season'] = tire[1]
        card['spikes'] = tire[2]
        card['load_index'] = tire[3]
        if tire[4] == '-':
            card['speed_index'] = 'U'
        else:
            card['speed_index'] = tire[4]
        card['diameter'] = tire[5]
        card['height'] = tire[6]
        card['width'] = tire[7]
        card['seasonality'] = tire[8]
        
        tyre_type = card['seasonality'].replace('Летняя', 'Летние').replace('Зимняя', 'Зимние')\
            .replace('Всесезонная', 'Всесезонные')
        if card['spikes']:
            tyre_type = f"{tyre_type} шипованные"
        elif tyre_type == 'Зимние':
            tyre_type = f"{tyre_type} нешипованные"
        card['tire_type'] = tyre_type
        card['suv'] = tire[9]
        if tire[10] == 0:
            card['runflat'] = 'Нет'
        else:
            card['runflat'] = 'Да'

        flag = 0
        for prod in products:
            if prod[0] == tire[0]:
                card['title'] = prod[2].replace('*', '-')
                card['slug'] = prod[3]
                if prod[21] != None and prod[21] > prod[6]:
                    card['price'] = int(prod[21])
                elif prod[6] != None:
                    card['price'] = int(prod[6])
                else:
                    card['price'] = None
                    flag = 1
                    break
                if card['price'] == 0:
                    flag = 1
                    break
                
                brand_model = select_brand_model(brands[prod[9]], prod[10], brands_avito)
                card['brand'] = brand_model['brand']
                card['model'] = brand_model['model']

                title = prod[2].replace('Шина', f"{card['seasonality']} шина")\
                    .replace('(Нижнекамский шинный завод) ', '')
                
                brand = card['brand'].replace('(Нижнекамский шинный завод)', '')
                
                if len(title) > 50:
                    title = f"{card['seasonality']} шина {brand} {card['model']} R{card['diameter']} {card['height']} {card['width']}"
                    if len(title) > 50:
                        title = f"{card['seasonality']} шина {brand} R{card['diameter']} {card['height']} {card['width']}"
                card['title'] = title.replace('*', '-')

                data = prod[16]
                if isinstance(data, dict):
                    if 'replace_bottom_pics' in data and data['replace_bottom_pics'] != None\
                    and isinstance(data['replace_bottom_pics'], list) and\
                    len(data['replace_bottom_pics']) > 0:
                        card['live_photo'] = data['replace_bottom_pics']

                    elif 'replace_bottom_pics' in data and\
                    isinstance(data['replace_bottom_pics'], str):
                        card['live_photo'] = [data['replace_bottom_pics']]
                    if 'replace_pics' in data and data['replace_pics'] != None:
                        if isinstance(data['replace_pics'], list)\
                        and len(data['replace_pics']) > 0:
                            card['photo'] = data['replace_pics']
                        elif isinstance(data['replace_pics'], str):
                            card['photo'] = [data['replace_pics']]

                    if 'photo' not in card:
                        if isinstance(prod[5], str):
                            card['photo'] = [prod[5]]
                        elif isinstance(prod[5], list): 
                            card['photo'] = prod[5]
                        else:
                            if 'live_photo' not in card:
                                flag = 1
                            break
                elif isinstance(prod[5], str):
                        card['photo'] = [prod[5]]
                elif isinstance(prod[5], list): 
                    card['photo'] = prod[5]
                else:
                    flag = 1
                break
        if card['price'] == None or flag == 1:
            continue
        if card['model'] == 'Nomodel' or card['brand'] == 'Nobrand':
            continue
        cards.append(card)

    if len(cards) > 0:
        return cards
    else:
        return 0
