import requests
import json
from datetime import datetime, timedelta
import telebot
import time
from helper import API_ZAMG_10MIN, TELEGRAM_TOKEN, CHANNEL_NAME
import logging

stations = {
    'ibk':
    {
        'type': 'INDIVIDUAL',
        'id': '11121',
        'group_id': None,
        'name': 'INNSBRUCK-FLUGHAFEN (AUTOMAT)',
        'state': 'Tirol',
        'lat': 47.26,
        'lon': 11.356666666666666,
        'altitude': 578.0,
        'valid_from': '2002-07-01T00:00+00:00',
        'valid_to': '2025-06-30T16:35+00:00',
        'has_sunshine': False,
        'has_global_radiation': False,
        'is_active': True
    },
    'ldk':
    {'type': 'INDIVIDUAL',
     'id': '11112',
     'group_id': None,
     'name': 'LANDECK',
     'state': 'Tirol',
     'lat': 47.140277777777776,
     'lon': 10.563611111111111,
     'altitude': 796.0,
     'valid_from': '1972-01-01T00:00+00:00',
     'valid_to': '2025-06-30T16:35+00:00',
     'has_sunshine': False,
     'has_global_radiation': False,
     'is_active': True
     },
    'jbh':
    {'type': 'INDIVIDUAL',
     'id': '11325',
     'group_id': None,
     'name': 'JENBACH',
     'state': 'Tirol',
     'lat': 47.388333333333335,
     'lon': 11.756388888888889,
     'altitude': 529.0,
     'valid_from': '1995-01-19T00:00+00:00',
     'valid_to': '2025-06-30T16:35+00:00',
     'has_sunshine': False,
     'has_global_radiation': False,
     'is_active': True
     }
}


def convert_time_stamps(time_stamps: list[str]):
    for i in range(len(time_stamps)):
        time_stamps[i] = datetime.strptime(
            time_stamps[i], '%Y-%m-%dT%H:%M:%S+0000') + timedelta(hours=2)

    return time_stamps


def get_data_from_api():
    r = requests.get(API_ZAMG_10MIN)

    content = json.loads(r.content.decode('utf-8'))

    timestamp = datetime.strptime(content['timestamps'][0].split('+')[0], '%Y-%m-%dT%H:%M')

    ibk = list()
    jbh = list()
    ldk = list()

    for station in content['features']:
        cur_station = None
        if station['properties']['station'] == stations['ibk']['id']:
            cur_station = ibk
        elif station['properties']['station'] == stations['ldk']['id']:
            cur_station = ldk
        elif station['properties']['station'] == stations['jbh']['id']:
            cur_station = jbh

        for key, value in station['properties']['parameters'].items():
            cur_station.append({key: value['data'][0]})

    return timestamp, ldk, ibk, jbh

def print_dashes(length: int=60):
    print('-'*length)

def print_data(timestamps, ldks, ibks, jbhs):
    print_dashes()
    print('Zeit\t\t\t\t\t| Landeck\t| Innsbruck\t| Jenbach')
    print_dashes()
    for timestamp, ldk, ibk, jbh in zip(timestamps, ldks, ibks, jbhs):
        print(timestamp, '\t|', ldk[0]['DD'], '\t|', ibk[0]['DD'], '\t|', jbh[0]['DD'])
    print_dashes()
    print_dashes()
    print()


def main():

    print('todo: git init, commit, push, run on pi as is')
    ten_min_periods = 10

    ldk = list()
    ibk = list()
    jbh = list()
    timestamps = list()

    last_time_stamp = datetime(year=1900, month=1, day=1)
    while True:
        cur_timestamp, cur_ldk, cur_ibk, cur_jbh = get_data_from_api()

        if cur_timestamp != last_time_stamp:
            if len(timestamps) > ten_min_periods:
                ldk.pop(0)
                ibk.pop(0)
                jbh.pop(0)
                timestamps.pop(0)

            timestamps.append(cur_timestamp)
            ldk.append(cur_ldk)
            ibk.append(cur_ibk)
            jbh.append(cur_jbh)

            last_time_stamp = cur_timestamp

            print_data(timestamps, ldk, ibk, jbh)
            time.sleep(9*60)
        else:
            time.sleep(10)


if __name__ == '__main__':
    main()