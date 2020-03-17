import time
import schedule
from Reposter.reposter import Reposter


def run(reposter: Reposter):
    reposter.main()


if __name__ == "__main__":
    r = Reposter()
    schedule.every(3).hours.do(run, r)

    while True:
        schedule.run_pending()
        time.sleep(1)
