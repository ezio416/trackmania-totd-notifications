#!/usr/bin/python3.12

# c 2024-02-10
# m 2024-02-26

from datetime import datetime
from pytz import timezone
import time

import app


def log(msg: str) -> None:
    with open('errors.log', 'a', newline='\n') as f:
        f.write(f'{msg}\n')


def main() -> None:
    try:
        app.main()
    except Exception as e:
        print(e)
        log(e)

    attempts:              int = 20
    wait_between_attempts: int = 10

    while True:
        now = datetime.now(timezone('Europe/Paris'))

        if now.hour == 19 and now.minute == 0:
            for i in range(attempts):
                try:
                    app.main()
                    break
                except Exception as e:
                    print(e)
                    log(e)

                    msg: str = f'attempt {i + 1}/{attempts} failed, waiting {wait_between_attempts} seconds (currently {now.strftime('%Y-%m-%d %H:%M:%S')})'
                    print(msg)
                    log(msg)

                    time.sleep(wait_between_attempts)

            print('waiting 60 seconds')
            time.sleep(60)
        else:
            print(f'waiting (currently {now.strftime('%Y-%m-%d %H:%M:%S')})')
            time.sleep(1)


if __name__ == '__main__':
    main()
