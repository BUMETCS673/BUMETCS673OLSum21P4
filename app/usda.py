import requests
import json
import yaml
from pyprojroot import here
from statistics import fmean, StatisticsError


def load_cfg():
    projroot = here()
    with open(projroot / "user_config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg


def usda_api_call(search_term: str, cfg: dict):

    api_key = cfg["usda"]['api_key']
    api_str = 'https://api.nal.usda.gov/fdc/v1/foods/search?query={}&pageSize=2&api_key={}'.format(search_term, api_key)

    response = requests.get(api_str)
    json_data = json.loads(response.text)

    return json_data


def extract_avg_calorie_data(json_data):
    nutrient_list_all = json_data['foods']

    cal_list = []
    for item in nutrient_list_all:
        cals = [x for x in item['foodNutrients'] if x['nutrientName'].lower() == 'energy']
        cal_list.append(cals[0]['value'])

    try:
        cal_avg = fmean(cal_list)
    except StatisticsError as e:
        raise Exception('Entered food not found in database') from e

    return cal_avg


#for testing
if __name__ == '__main__':
    print(extract_avg_calorie_data(usda_api_call('hamburger', load_cfg())))