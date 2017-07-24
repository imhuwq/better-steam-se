# import requests
#
# headers = {'user-agent': 'User-Agent:Mozilla/5.0 (X11; Linux x86_64) '
#                          'AppleWebKit/537.36 (KHTML, like Gecko) '
#                          'Chrome/55.0.2883.75 Safari/537.36',
#            'host': 'store.steampowered.com',
#            'connection': 'keep-alive'
#            }
#
# cookies = {'birthtime': '667753201',
#            'lastagecheckage': '1-March-1991',
#            'Steam_Language': 'english',
#            'steamCountry': 'CN',
#            'mature_content': '1'
#            }
#

import sys

from crawl.steam import steam

try:
    cmd, *opt = sys.argv[1:]
except IndexError:
    cmd, *opt = None, None


def trigger(chain, init):
    steam.trigger(chain, init)


if __name__ == "__main__":
    if cmd == "trigger":
        trigger(*opt)
