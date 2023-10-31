
def get_make_for_spring(card: dict):
    if 'astra' in card['title'].lower():
        card['make'] = 'Opel'
    elif 'octavia' in card['title'].lower() or 'rapid' in card['title'].lower()\
        or 'jetta' in card['title'].lower():
        card['make'] = 'Skoda'
    elif 'golf' in card['title'].lower() or 'polo' in card['title'].lower():
        card['make'] = 'Volkswagen'
    elif 'camry' in card['title'].lower() or 'corolla' in card['title'].lower():
        card['make'] = 'Toyota'
    elif 'outlander' in card['title'].lower() or 'lancer' in card['title'].lower():
        card['make'] = 'Mitsubishi'
    elif 'ваз' in card['title'].lower() or 'веста' in card['title'].lower():
        card['make'] = 'Lada'
    elif 'ceed' in card['title'].lower() or 'rio' in card['title'].lower()\
        or 'cerato' in card['title'].lower() or 'optima' in card['title'].lower()\
        or 'sportage' in card['title'].lower():
        card['make'] = 'Kia'
    elif 'i-30' in card['title'].lower() or 'solaris' in card['title'].lower():
        card['make'] = 'Hyundai'
    elif 'mazda' in card['title'].lower():
        card['make'] = 'Mazda'
    elif 'focus' in card['title'].lower():
        card['make'] = 'Ford'
    elif 'cruze' in card['title'].lower():
        card['make'] = 'Chevrolet'
    elif 'subaru' in card['title'].lower():
        card['make'] = 'Subaru'
    elif 'accord' in card['title'].lower():
        card['make'] = 'Honda'
    else:
        card['make'] = None


def parse_spring(products: list):
    cards = []
    count = 0

    flag = 0
    for prod in products:
        if prod[17] == 7:
            count += 1
            card = {'id' : prod[0]}
            card['title'] = prod[2]
            card['brand'] = 'Технорессор'
            card['slug'] = prod[3]
            get_make_for_spring(card)
            if prod[21] != None and prod[21] > prod[6]:
                card['price'] = int(prod[21])
            elif prod[6] != None:
                card['price'] = int(prod[6])
            else:
                card['price'] = None
                continue
            if card['price'] == 0:
                flag = 1
                continue
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

    if len(cards) > 0:
        return cards
    else:
        return 0
