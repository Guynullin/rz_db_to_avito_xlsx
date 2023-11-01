
def parse_rim(type: str, products: list, rim_rows: list):
    
    cards = []
    for rim in rim_rows:
        if rim[11] == type:
            card = {'id': rim[0]}
            card['diameter'] = rim[1]
            card['bolts'] = rim[4]
            if rim[5] != 0:
                card['bolts2'] = rim[5]
            card['pcd'] = rim[7]
            if rim[8] != 0:
                card['pcd2'] = rim[8]
            card['width'] = rim[3]
            card['et'] = rim[2]
            card['dia'] = rim[6]
            card['color'] = rim[9]
            card['type'] = type
            card['et2'] = rim[12]
            card['width2'] = rim[13]

            flag = 0
            for prod in products:
                if prod[0] == rim[0]:
                    card['title'] = prod[2].replace('В СТИЛЕ', 'в стиле').replace('В стиле', 'в стиле')
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
                    card['brand_id'] = prod[9]
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