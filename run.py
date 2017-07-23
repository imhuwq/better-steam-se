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

from crawl.steam import steam

steam.trigger("game_list", "https://www.baidu.com/")
