
def parse_tire(products: list, tire_rows: list, brands: dict):
    cards = []
    count = 0

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
        card['seasonality'] = tire[8].replace('Летняя', 'Летние').replace('Зимняя', 'Зимние')\
        .replace('Всесезонная', 'Всесезонные')
        card['suv'] = tire[9]
        if tire[10] == 0:
            card['runflat'] = 'Нет'
        else:
            card['runflat'] = 'Да'

        flag = 0
        for prod in products:
            if prod[0] == tire[0]:
                card['title'] = prod[2]
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
                if prod[9] in brands:
                    card['brand'] = brands[prod[9]]
                else:
                    card['brand'] = prod[9]
                card['model'] = prod[10]
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
                        count += 1

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
        cards.append(card)
    print(f'count: {count}')
    if len(cards) > 0:
        return cards
    else:
        return 0
