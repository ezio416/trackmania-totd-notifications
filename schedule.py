# c 2024-02-10
# m 2024-02-10

from datetime import datetime
from pytz import timezone
import time

import app


def main() -> None:
    while True:
        now = datetime.now(timezone('Europe/Paris'))

        if now.hour == 17 and now.minute == 00:
            for i in range(5):
                try:
                    app.main()
                    break
                except Exception as e:
                    print(e)
                    print(f'attempt {i + 1}/5 failed, waiting 5 seconds')
                    time.sleep(5)

            print('waiting 60 seconds')
            time.sleep(60)
        else:
            print(f'waiting ({now.strftime('%Y-%m-%d %H:%M:%S')})')
            time.sleep(1)


if __name__ == '__main__':
    main()
