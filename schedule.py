#!/usr/bin/python3.12

# c 2024-02-10
# m 2024-02-28

from datetime import datetime as dt
from pytz import timezone
import time

import app


def log(msg, print_term: bool = True) -> None:
    text: str = f'{now()} {msg}'

    if print_term:
        print(text)

    with open('errors.log', 'a', newline='\n') as f:
        f.write(f'{text}\n')


def now() -> str:
    return f'[{dt.now().strftime('%Y-%m-%d %H:%M:%S')}]'


def main() -> None:
    try:
        app.main()
    except Exception as e:
        log(e)

    attempts:              int = 20
    wait_between_attempts: int = 10

    while True:
        now_paris = dt.now(timezone('Europe/Paris'))

        if now_paris.hour == 19 and now_paris.minute == 0:
            for i in range(attempts):
                try:
                    app.main()
                    break
                except Exception as e:
                    log(e)

                    log(f'attempt {i + 1}/{attempts} failed, waiting {wait_between_attempts} seconds')

                    time.sleep(wait_between_attempts)

                log('max attempts reached')

            print('waiting 60 seconds')
            time.sleep(60)
        else:
            print(f'{now()} waiting (now_paris: {now_paris.strftime('%Y-%m-%d %H:%M:%S')})')
            time.sleep(1)


if __name__ == '__main__':
    main()
