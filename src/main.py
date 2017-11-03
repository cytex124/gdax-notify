from core import GDax
import asyncio
import logging
import argparse

logger = logging.getLogger('__GDAX__')
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--browser", action="store_true",
                    help="Opens Webbrowser on filled Orders")
args = parser.parse_args()


if __name__ == '__main__':
    gdax = GDax(browser=args.browser)
    gdax.start_notify()
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logger.info('GDax Notify stopped...')
