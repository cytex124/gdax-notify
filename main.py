import configparser
import gdax
from win10toast import ToastNotifier
import time

toaster = ToastNotifier()

config = configparser.ConfigParser()
config.read('creds.ini')

credentials = dict(config['ACCESS'])


public_client = gdax.PublicClient()
auth_client = gdax.AuthenticatedClient(
    credentials['key'],
    credentials['secret'],
    credentials['passphrase']
)

open_orders = {}

if __name__ == '__main__':
    while True:
        check_order = []
        oos = auth_client.get_orders()[0]
        for my_oo in open_orders:
            found = False
            for oo in oos:
                if oo['id'] == my_oo:
                    found = True
                    break
            if not found:
                check_order.append(oo)

        for oo in oos:
            if oo['id'] not in open_orders:
                open_orders[oo['id']] = oo

        for co in check_order:
            try:
                fills = auth_client.get_fills(order_id=co['id'])[0]
                size = 0
                for fill in fills:
                    size += float(fill['size'])
                toaster.show_toast("GDax Fill",
                                   "%s: %s for %s €".format(fills[0]['side'],
                                                          size,
                                                          fills[0]['price']),
                                   icon_path="custom.ico",
                                   duration=10)
            except:
                del open_orders[co['id']]

        time.sleep(3)
