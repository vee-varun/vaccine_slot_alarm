import re
import requests
import datetime
from pydub import AudioSegment
from pydub.playback import play

from constants import DISTRICT_IDS

API_URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict'
DAY_RANGE = 1  # for how many days you want to check the slot
PATH_TO_AUDIO = "Media/beep_beep_beep.wav"  # path to the audio file
MIN_AGE_LIMIT = 18
DOSE_NUMBER = 1  # first or second dose?
FEE_TYPE = 'Free'  # Fee type 'Free' or 'Paid'

sound = AudioSegment.from_wav(PATH_TO_AUDIO)


HEADERS = {
    'accept': 'application/json',
    'Accept-Language': 'hi_IN',
}

for d in DISTRICT_IDS:
    print(f'Pass {d["state_id"]} state id for {d["state_name"]}.')
print('\n')
while True:
    try:
        state_id = input('In which state you want to search for slots? : ')
        state_id = int(state_id)
        districts = None
        for d in DISTRICT_IDS:
            if d['state_id'] == state_id:
                districts = d['districts']
                state_name = d['state_name']
        if not districts:
            print(f'Invalid state_id passed.', end='\n\n')
        else:
            break
    except Exception:
        print(f'Invalid state_id passed.', end='\n\n')

print('\n')

f_districts = {}
for d in districts:
    print(f'Input {d["district_id"]} for {d["district_name"]}.')
while True:
    print('\n')
    district_ids = input(
        f'In which district of {state_name}? You can pass multiple district '
        f'ids separated with comma : '
    )
    m = re.match('([0-9]+,\s*)*[0-9]+,?$', district_ids)
    if not m:
        print(f'1-Invalid input - {district_ids}. Please check.')
        continue
    district_ids = district_ids.split(',')
    try:
        district_ids = [int(id) for id in district_ids]
        for id in district_ids:
            for district in districts:
                if district['district_id'] == id:
                    f_districts[district['district_name']] = district['district_id']
                    break
            else:
                print(f'Invalid district id found - {id}')
                break
        if f_districts:
            break
    except ValueError:
        print(f'2-Invalid input - {district_ids}. Please check.')


c = 0
while True:
    print(f'\n\nRunning {c} times.')
    c += 1
    for i in range(DAY_RANGE):
        date = (datetime.datetime.now() + datetime.timedelta(days=i + 1)).strftime('%d-%m-%Y')
        print(f'*******************************************{date} *******************************************')
        for district_name, district_id in f_districts.items():
            print(f'Checking slots in {district_name}.')
            params = (
                ('district_id', district_id),
                ('date', date),
            )
            try:
                response = requests.get(API_URL, headers=HEADERS, params=params)
            except Exception:
                print(
                    'Failed to request the API URL. Please check your internet connection.'
                )
            if not response.ok:
                print('Not working. Please try after some time.')
            data = response.json()
            centers = data['sessions']
            for center in centers:
                if (
                        center['min_age_limit'] == MIN_AGE_LIMIT
                        and center['available_capacity_dose1' if DOSE_NUMBER == 1 else 'available_capacity_dose2'] > 0
                        and center['fee_type'] == FEE_TYPE
                ):
                    print(
                        center['district_name'], ' | ',
                        center['name'], ' | ',
                        center['address'], ' | ',
                        center['date'], ' | ',
                        center['vaccine'], ' | ',
                        center['available_capacity']
                    )
                    try:
                        while True:
                            play(sound)
                    # to turn off audio press ctrl+c, the alarm will stop and
                    # script will continue to search for slots
                    except KeyboardInterrupt:
                        continue
