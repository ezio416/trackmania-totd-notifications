# c 2024-02-08
# m 2024-02-08

# from json import loads
import os

# from discord_webhook import DiscordEmbed, DiscordWebhook
# from requests import get


# def format_race_time(input_ms: int) -> str:
#     min: int = int(input_ms / 60000)
#     sec: int = int((input_ms - (min * 60000)) / 1000)
#     ms:  int = input_ms % 1000

#     return f'{min}:{str(sec).zfill(2)}.{str(ms).zfill(3)}'


# def strip_format_codes(raw: str) -> str:
#     clean: str = ''
#     flag:  int = 0

#     for c in raw:
#         if flag and c.lower() in 'gilnostwz$<>':
#             flag = 0
#             continue
#         if flag and c.lower() in '0123456789abcdef':
#             flag -= 1
#             continue
#         if c == '$':
#             flag = 3
#             continue
#         flag = 0
#         clean += c

#     return clean.strip()


def main():
    # print(os.environ['DEV_TMIO_API_BASE'])
    print(os.environ)

    # req = get(
    #     url = os.environ['DEV_TMIO_API_BASE'] + 'totd/0',
    #     headers={'User-Agent': os.environ['DEV_TOTD_NOTIF_AGENT_TMIO']}
    # )

    # loaded: dict = loads(req.text)

    # year:  int  = loaded['year']
    # month: int  = loaded['month']
    # day:   int  = len(loaded['days'])
    # map:   dict = loaded['days'][-1]['map']

    # author_id:     str = map['author']
    # name:          str = strip_format_codes(map['name'])
    # authorTime:    int = map['authorScore']
    # uid:           str = map['mapUid']
    # thumbnail_url: str = map['thumbnailUrl']
    # author_name:   str = map['authorplayer']['name']

    # tmio_author_url: str = 'https://trackmania.io/#/player/' + author_id
    # tmio_map_url:    str = 'https://trackmania.io/#/leaderboard/' + uid

########################################################################################################################

    # webhook = DiscordWebhook(os.environ['DEV_TOTD_NOTIF_DISCORD_WEBHOOK'])

    # embed = DiscordEmbed(
    #     title=f'Track of the Day for {year}-{str(month).zfill(2)}-{str(day).zfill(2)}',
    #     color='00a719'
    # )

    # embed.add_embed_field('Map',          f'[{name}]({tmio_map_url})',           False)
    # embed.add_embed_field('Author',       f'[{author_name}]({tmio_author_url})', False)
    # embed.add_embed_field('Author Medal', format_race_time(authorTime),          False)
    # embed.set_thumbnail(thumbnail_url)

    # webhook.add_embed(embed)

    # resp = webhook.execute()

    # print('hi')


if __name__ == '__main__':
    main()
