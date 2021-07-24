import requests
import datetime
from pydub import AudioSegment
from pydub.playback import play

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

districts = {
    'South West Delhi': 150,
    'West Delhi': 142,
    'Central Delhi': 141,
    'South Delhi': 149,
    'South East Delhi': 144,
    'New Delhi': 140,
    'East Delhi': 145,
    'North Delhi': 146,
    'North East Delhi': 147,
    'North West Delhi': 143,
    'Shahdara': 148

}

c = 0
while True:
    print(f'\n\nRunning {c} times.')
    c += 1
    for i in range(DAY_RANGE):
        date = (datetime.datetime.now() + datetime.timedelta(days=i + 1)).strftime('%d-%m-%Y')
        print(f'*******************************************{date} *******************************************')
        for district_name, district_id in districts.items():
            print(f'Checking slots in {district_name}.')
            params = (
                ('district_id', district_id),
                ('date', date),
            )
            response = requests.get(API_URL, headers=HEADERS, params=params)
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
