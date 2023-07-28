import requests
import bs4
import urllib.parse as parse

final = {'name': [], 'webpage': [], 'birthplace': []}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def get_info(first_name, last_name):
    url = "https://www.thehendonmob.com/search/?q=" + first_name + "+" + last_name
    scraped = requests.get(url, headers=headers)

    hendonmob_search = bs4.BeautifulSoup(scraped.content.decode(), 'lxml')
    players = []
    first_player = hendonmob_search.find('div', attrs={'class': 'db-gallery__item'})
    players.append(first_player)

    i = 0
    while players[i].next_sibling.next_sibling is not None:
        next_player = players[i].next_sibling.next_sibling
        players.append(next_player)
        i += 1

    for player in players:
        player_info = bs4.BeautifulSoup(player.decode(), 'lxml')
        player_name = player_info.find('div', attrs={'class': 'name'}).string
        final.setdefault('name', []).append(player_name)

        player_web = player_info.find('a').get('href')
        player_web = parse.parse_qsl(player_web)
        final.setdefault('webpage', []).append(player_web[1][1])

        player_birth = player_info.find('div', attrs={'class': 'db-gallery__item-subtext'}).string
        final.setdefault('birthplace', []).append(player_birth)


get_info('robert', 'kaplan')
print(final['name'], final['webpage'], final['birthplace'])
