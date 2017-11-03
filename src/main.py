from core import GDax
import asyncio
import logging


logger = logging.getLogger('__GDAX__')
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    gdax = GDax()
    gdax.start_notify()
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print('Loop stopped')

