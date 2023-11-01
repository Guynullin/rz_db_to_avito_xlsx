from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

model = 'WINTER I*PIKE RS 2 W429'.lower()
avito = "Winter I'Pike RS2 W429".lower()
avito = "Winter I'Pike RS+ W419D".lower()

print(similar(model, avito))

'''
Winter I'Pike LV RW15"/>
<model name="Winter I'Pike RS W419"/>
<model name="Winter I'Pike RS+ W419D"/>
<model name="Winter I'Pike RS2 W429"/>
<model name="Winter I'Pike W409"/>
<model name="Winter I'Pike X SUV"/>'''