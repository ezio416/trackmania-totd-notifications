# c 2024-02-10
# m 2024-02-11

from datetime import datetime
from pytz import timezone
import time

import app


def main() -> None:
    attempts:              int = 5
    wait_between_attempts: int = 10

    while True:
        now = datetime.now(timezone('Europe/Paris'))

        if now.hour == 17 and now.minute == 0:
            for i in range(attempts):
                try:
                    app.main()
                    break
                except Exception as e:
                    print(e)
                    print(f'attempt {i + 1}/{attempts} failed, waiting {wait_between_attempts} seconds')
                    time.sleep(wait_between_attempts)

            print('waiting 60 seconds')
            time.sleep(60)
        else:
            print(f'waiting ({now.strftime('%Y-%m-%d %H:%M:%S')})')
            time.sleep(1)


if __name__ == '__main__':
    main()
