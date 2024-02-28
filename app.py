#!/usr/bin/python3.12

# c 2024-02-08
# m 2024-02-28

from base64 import b64encode
# from datetime import datetime
from json import loads
import os
# from pytz import timezone
from time import sleep

from discord_webhook import DiscordEmbed, DiscordWebhook
from requests import get, post


uid_file:  str   = os.path.abspath('./last_uid.txt')
url_core:  str   = 'https://prod.trackmania.core.nadeo.online'
url_live:  str   = 'https://live-services.trackmania.nadeo.live'
wait_time: float = 0.5


def format_race_time(input_ms: int) -> str:
    min: int = int(input_ms / 60000)
    sec: int = int((input_ms - (min * 60000)) / 1000)
    ms:  int = input_ms % 1000

    return f'{min}:{str(sec).zfill(2)}.{str(ms).zfill(3)}'


def get_account_name(id: str) -> str:
    print(f'getting account name for {id}')

    sleep(wait_time)
    req = get(
        f'https://api.trackmania.com/api/display-names?accountId[]={id}',
        headers={'Authorization': get_token('OAuth')}
    )

    loaded: dict = loads(req.text)
    name:   str  = loaded[id]

    print(f'getting account name for {id} ({name}) done')

    return name


def get_likely_style(account_id: str) -> str:
    if account_id in (
        'ce6c0db0-2dd9-463f-aaec-463032bad4c5',  # emlan
    ):
        return 'Bobsleigh/Grass'

    if account_id in (
        '041623e9-57de-4dea-8fd2-6adf967ba558',  # ealipse
        '3d71524d-922d-4755-9f9a-86bd93cedbf9',  # intax
        'eb46a97e-2057-4544-8557-bc8e9d425d37',  # microvert
    ):
        return 'Dirt/Grass Tech'

    if account_id in (
        '85c745ee-d3b4-46d1-bd21-3566b5e9f3f6',  # habe
        '7599d4de-2ced-46d0-abf6-91612e1dca30',  # spec
    ):
        return 'Dirt Tech'

    if account_id in (
        '435ecb19-a003-4a79-9f3c-a5572a0dc8a8',  # agrabou
        'babd5821-8cad-4ccd-9a80-218d0e3afd50',  # aries
        '701b9536-bc38-4a98-88eb-abe6cb174c0d',  # striderin
        'e5ed5a9c-fdaf-4c8a-872b-50da739f91a4',  # vekisis
    ):
        return 'Fullspeed'

    if account_id in (
        'd3d84336-fc5f-49fd-b866-b15ca80152a8',  # andybaguette
        '17c3f129-c877-45b8-8bd1-80d7a4f9fc29',  # capman
        '78332411-010f-4d61-84d8-0db1d6b5f8c0',  # henkisme
    ):
        return 'Ice'

    if account_id in (
        'fc42881d-56fd-4206-9515-3a7222a67304',  # souldrinker
    ):
        return 'Plastic Tech'

    if account_id in (
        'dcc6b861-acdb-44bd-b73c-345a78d58a98',  # oregox
        '3468343f-bc7f-4ddd-938f-0f118d13cdc9',  # proff
    ):
        return 'Speed Tech'

    if account_id in (
        '8ffe695a-8aff-4378-a85f-a503a1abb256',  # ddolla
        'a0f1b480-7b9b-44e7-9ca3-2196fc16cb3a',  # sloopkogel
    ):
        return 'Tech'

    return ''


def get_map_info(track: dict) -> dict:
    print(f'getting map info for {track['uid']}')

    sleep(wait_time)
    req = get(
        f'{url_core}/maps?mapUidList={track['uid']}',
        headers={'Authorization': get_token('NadeoServices')}
    )

    loaded: dict = loads(req.text)
    single: dict = loaded[0]

    track['author_id']   = single['author']
    track['author_time'] = format_race_time(single['authorScore'])
    track['name']        = strip_format_codes(single['name'])
    track['thumb_url']   = single['thumbnailUrl']

    track['author_name'] = get_account_name(track['author_id'])
    track['likely_style'] = get_likely_style(track['author_id'])

    print(f'getting map info for {track['uid']} ({track['name']}) done')

    return track


def get_token(audience: str) -> str:
    print(f'getting token for {audience}')

    sleep(wait_time)

    if audience == 'OAuth':
        req = post(
            'https://api.trackmania.com/api/access_token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': os.environ['TM_OAUTH_IDENTIFIER'],
                'client_secret': os.environ['TM_OAUTH_SECRET']
            }
        )

        loaded: dict = loads(req.text)
        token:  str  = loaded['access_token']

    else:
        req = post(
            f'{url_core}/v2/authentication/token/basic',
            headers={
                'Authorization': f'Basic {b64encode(f'{os.environ['TM_TOTD_NOTIF_SERVER_USERNAME']}:{os.environ['TM_TOTD_NOTIF_SERVER_PASSWORD']}'.encode('utf-8')).decode('ascii')}',
                'Content-Type': 'application/json',
                'Ubi-AppId': '86263886-327a-4328-ac69-527f0d20a237',  # TM2020's ID
                'User-Agent': os.environ['TM_TOTD_NOTIF_AGENT'],
            },
            json={'audience': audience}
        )

        loaded: dict = loads(req.text)
        token:  str  = f'nadeo_v1 t={loaded['accessToken']}'

    print(f'got token for {audience}')

    return token


def get_track() -> dict:
    print('getting today\'s TOTD')

    sleep(wait_time)
    req = get(
        f'{url_live}/api/token/campaign/month?length=1&offset=0',
        headers={'Authorization': get_token('NadeoLiveServices')}
    )

    loaded:    dict = loads(req.text)
    monthList: dict = loaded['monthList'][0]

    year:  int = monthList['year']
    month: int = monthList['month']

    uid: str = ''
    day: int = 0
    season: str = ''

    for map in reversed(monthList['days']):
        if map['mapUid'] != '':
            uid    = map['mapUid']
            day    = map['monthDay']
            season = map['seasonUid']
            break

    track: dict = {
        'date': f'{year}-{str(month).zfill(2)}-{str(day).zfill(2)}',
        'season': season,
        'uid': uid
    }

    print(f'getting today\'s TOTD ({track['date']}) done')

    return track


def track_is_from_yesterday(uid: str) -> bool:
    # now = datetime.now(timezone('Europe/Paris'))
    # today = f'{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}'

    # return today != date

####################

    # req = get('https://raw.githubusercontent.com/ezio416/trackmania-json-tracking/main/CampaignCompletionist/next_totd.json')

    # loaded: dict = loads(req.text)
    # items = list(loaded.items())
    # last_track = items[-1][1]

    # return uid == last_track['uid']

####################

    if os.path.isfile(uid_file):
        with open(uid_file, 'r') as f:
            last_uid: str = f.read()

        if uid == last_uid:
            return True

    return False


def strip_format_codes(raw: str) -> str:
    clean: str = ''
    flag:  int = 0

    for c in raw:
        if flag and c.lower() in 'gilnostwz$<>':
            flag = 0
            continue
        if flag and c.lower() in '0123456789abcdef':
            flag -= 1
            continue
        if c == '$':
            flag = 3
            continue
        flag = 0
        clean += c

    return clean.strip()


def main():
    track: dict = get_map_info(get_track())

    if track_is_from_yesterday(track['uid']):
        raise Exception(f'old track: {track['uid']}')

    print('webhook starting')

    webhook = DiscordWebhook(
        os.environ['TM_TOTD_NOTIF_DISCORD_WEBHOOK_URL'],
        content='<@&1205378175601745970>'
    )

    embed = DiscordEmbed(
        title=f'Track of the Day for {track['date']}',
        color='00a719'
    )

    embed.add_embed_field('Map', f'[{track['name']}](https://trackmania.io/#/totd/leaderboard/{track['season']}/{track['uid']})', False)
    embed.add_embed_field('Author', f'[{track['author_name']}](https://trackmania.io/#/player/{track['author_id']})', False)
    embed.add_embed_field('Author Medal', track['author_time'], False)

    if track['likely_style'] != '':
        embed.add_embed_field('Likely Style (based on author)', track['likely_style'], False)

    embed.set_thumbnail(track['thumb_url'])

    webhook.add_embed(embed)

    webhook.execute()

    print('webhook done, writing last_uid.txt')

    with open(uid_file, 'w') as f:  # not working?
        f.write(track['uid'])

    sleep(1)

    with open(uid_file, 'r') as f:
        print(f'last_uid: {f.read()}')


if __name__ == '__main__':
    main()
