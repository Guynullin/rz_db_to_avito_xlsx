import requests
import bs4

def get_brands_models_avito(url: str):
    
    brands_dict = {}

    resp = requests.get(url)
    
    soup = bs4.BeautifulSoup(resp.content, 'lxml')

    brands_list = soup.find_all('make')

    if len(brands_list) > 0:
        for item in brands_list:
            name = item.get('name')
            brands_dict[name] = []
            models = item.find_all('model')
            if len(models) > 0:
                for model in models:
                    model_name = model.get('name')
                    brands_dict[name].append(model_name)
            

    if brands_dict:
        return brands_dict
    else:
        return 0







