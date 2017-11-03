import configparser
import gdax as gdax_lib
from win10toast import ToastNotifier
import logging
import asyncio
import os
import sys
import webbrowser
import requests
import json

GDAX_URL = 'https://www.gdax.com/'

file_path = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger('__GDAX__')
WIN10_TOASTER = ToastNotifier()


class GDax(object):

    def __init__(self, interval=.5, browser=False):
        config = configparser.ConfigParser()
        config.read(os.path.join(file_path, '..\creds.ini'))
        credentials = dict(config['ACCESS'])

        self.browser = browser

        self._open_orders = {}
        self._public_client = gdax_lib.PublicClient()
        self._auth_client = gdax_lib.AuthenticatedClient(
            credentials['key'],
            credentials['secret'],
            credentials['passphrase']
        )

        self._loop = asyncio.get_event_loop()
        self._interval = interval
        self._handler_notify = None

    def _check_lost_orders(self, oos):
        check_order = []
        for my_oo in self._open_orders:
            found = False
            for oo in oos:
                if oo['id'] == my_oo:
                    found = True
                    break
            if not found:
                check_order.append(self._open_orders[my_oo])
        return check_order

    def _add_new_orders(self, oos):
        for oo in oos:
            if oo['id'] not in self._open_orders:
                logger.info('Order: {0} {1} for {2} €'.format(
                    oo['side'].upper(),
                    oo['size'],
                    oo['price']
                ))
                self._open_orders[oo['id']] = oo

    def _notify_if_new_fills(self, check_orders):
        for check_order in check_orders:
            try:
                fills = self._auth_client.get_fills(
                    order_id=check_order['id']
                )[0]
            except json.decoder.JSONDecodeError:
                message = "Canceled {0}: {1} for {2} €".format(
                    check_order['side'].upper(),
                    check_order['size'],
                    check_order['price']
                )
            else:
                size = 0
                for fill in fills:
                    size += float(fill['size'])
                message = "Filled {0}: {1} for {2} €".format(
                    fills[0]['side'].upper(), size, fills[0]['price']
                )
                self.note(message)
                self.open_gdax_website()
            del self._open_orders[check_order['id']]
            logger.info(message)

    def _check_fills(self, loop=True):
        try:
            oos = self._auth_client.get_orders()[0]
        except requests.exceptions.ConnectionError:
            logger.error("No Connection to GDax..")
            sys.exit(1)
        lost_order = self._check_lost_orders(oos)
        self._add_new_orders(oos)
        self._notify_if_new_fills(lost_order)
        if loop:
            self._start_notify()

    def _start_notify(self):
        self._handler_notify = self._loop.call_later(
            self._interval, self._check_fills
        )

    def start_notify(self):
        logger.info("GDax Notify started...")
        self.note("Started...")
        self.open_gdax_website()
        self._start_notify()

    @staticmethod
    def note(msg):
        WIN10_TOASTER.show_toast("GDax Notify", msg)

    def open_gdax_website(self):
        if self.browser:
            webbrowser.open_new_tab(GDAX_URL)
