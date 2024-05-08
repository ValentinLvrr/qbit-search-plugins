# VERSION: 1.0
# AUTHORS: ValentinLvrr

from novaprinter import prettyPrinter
import requests
from bs4 import BeautifulSoup


class nextorrent(object):
    url = 'https://www.nextorrent.me'
    name = 'NexTorrent'
    supported_categories = {'all': '0'}

    def get_magnet_link(self, link):
        res = requests.get(self.url+link)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.find(
            'div', {'class': 'btn-magnet'}).find('a')['href']

    def parseHTML(self, el):
        return {
            'link': self.get_magnet_link(el.find('a')['href']),
            'name': el.find('a').text,
            'size': el.find_all('td')[1].text,
            'seeds': el.find_all('td')[2].text,
            'leech': el.find_all('td')[3].text,
            'engine_url': self.url,
            'desc_link': self.url+el.find('a')['href']
        }

    def search(self, what, cat='all'):
        res = requests.get(self.url + '/recherche/' + what)
        soup = BeautifulSoup(res.text, 'html.parser')
        elements = soup.select('#contenu > div > table > tbody')[
            0].find_all('tr')

        for el in elements:
            try:
                data = self.parseHTML(el=el)
                prettyPrinter(data)
            except:
                continue
