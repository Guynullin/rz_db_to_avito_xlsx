import re

def format_alloy_title(card: dict):
    et = card['et']
    if 'et2' in card and card['et2'] != 0:
        et = f'{et}/{card["et2"]}'

    clear_title_J_et = card['title'].replace('ЛИТОЙ ДИСК', 'Литой диск')\
    .replace(card['model'], '').replace(f"({card['color']})", '')\
    .replace(str(card['dia']), '')\
    .replace('dia', '').replace('DIA', '').strip()
    if card['width2'] == 0:
        if card['width'].is_integer():
            clear_string_et = re.sub(rf'\s{int(card["width"])}\w\b', '', clear_title_J_et)                
        else:
            clear_string_et = re.sub(rf'\s{card["width"]}\w\b', '', clear_title_J_et)
    else:
        if card['width'].is_integer():
            width1 = int(card['width'])
        else:
            width1 = card['width']
        if card['width2'].is_integer():
            width2 = int(card['width2'])
        else:
            width2 = card['width2']
        width = f'{width1}/{width2}'
        clear_string_et = re.sub(rf'\s{width}\w\b', '', clear_title_J_et)
    
    clear_string = re.sub(rf"\bET{et}\b", "", clear_string_et).replace(f'ET{card["et"]}', '')
    title = re.sub(" +", " ", clear_string).replace('*', '-').strip()

    return title



def format_forged_title(card: dict):
    et = card['et']
    if 'et2' in card and card['et2'] != 0:
        et = f'{et}/{card["et2"]}'

    clear_title_J_et = card['title'].replace('КОВАНЫЙ ДИСК', 'Кованый диск')\
    .replace(card['model'], '').replace(f"({card['color']})", '')\
    .replace(str(card['dia']), '')\
    .replace('dia', '').replace('DIA', '').strip()
    if card['width2'] == 0:
        if card['width'].is_integer():
            clear_string_et = re.sub(rf'\s{int(card["width"])}\w\b', '', clear_title_J_et)                
        else:
            clear_string_et = re.sub(rf'\s{card["width"]}\w\b', '', clear_title_J_et)
    else:
        if card['width'].is_integer():
            width1 = int(card['width'])
        else:
            width1 = card['width']
        if card['width2'].is_integer():
            width2 = int(card['width2'])
        else:
            width2 = card['width2']
        width = f'{width1}/{width2}'
        clear_string_et = re.sub(rf'\s{width}\w\b', '', clear_title_J_et)
    
    clear_string = re.sub(rf"\bET{et}\b", "", clear_string_et).replace(f'ET{card["et"]}', '')
    title = re.sub(" +", " ", clear_string).replace('*', '-').strip()

    if len(title) > 50:
        title = title.replace('RZ FORGED ', '')
        if len(title) > 50:
            title = title.replace(f"{card['bolts']}x{card['pcd']}", '')\
                .replace(f"{card['bolts']}X{card['pcd']}", '').strip()

    return title
