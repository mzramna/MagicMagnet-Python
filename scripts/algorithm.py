import json
import os
import urllib.parse

import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup, SoupStrainer


class MagicMagnet():
    def __init__(self):
        self.links = {'foundLinks': 0}

    def search(self, searchContent, sites: [str], total_search_pages=5):
        search_params = json.load(open("search_parameters.json"))
        for site in search_params:
            if search_params[site]["alias"] in sites:
                search_params[site]["searchURL"]=str(search_params[site]["searchURL"]).replace("{searchContent}",str(urllib.parse.quote_plus(searchContent)))
                if search_params[site]["need_param"]:
                    self._getDownloadPages(search_params[site]['searchURL'],resultURL=search_params[site]["resultURL"], start=search_params[site]['start'], notIn=search_params[site]['notIn'],
                                           sliceString=search_params[site]['sliceString'])
                else:
                    for page in range(1,total_search_pages):
                        self._getPageLinks(search_params[site]["searchURL"].replace("{page}",str(page)))

    def _getDownloadPages(self, searchURL, resultURL="", start="", notIn="", sliceString=""):
        if resultURL == "":
            resultURL = None
        if start == "":
            start = None
        if notIn == "":
            notIn = None
        if sliceString == "":
            sliceString = None
        request = requests.get(searchURL)
        result = BeautifulSoup(request.content, 'lxml', parse_only=SoupStrainer('a'))

        linksChecked = []

        for i in result.find_all('a', href=True):
            if i.get('href').startswith(start) and i.get('href') not in linksChecked and (
                    '#download' not in i.get('href')):

                valid = True

                if (start != None) and (notIn != None):
                    for link in notIn:
                        if link in i.get('href'):
                            valid = False

                if valid == True:
                    linksChecked.append(i.get('href'))
                    if resultURL != None:
                        if sliceString != None:
                            self._getPageLinks(f'{resultURL}{i.get("href")[sliceString[0]:sliceString[1]]}')
                        else:
                            self._getPageLinks(f'{resultURL}{i.get("href")}')
                    else:
                        if sliceString != None:
                            self._getPageLinks(i.get('href')[sliceString[0]:sliceString[1]])
                        else:
                            self._getPageLinks(i.get('href'))

    def _getPageLinks(self, searchURL):
        if searchURL.endswith('/&s'):
            searchURL = searchURL[:-2]
        print(searchURL)

        sg.Print(f'Searching in: {searchURL}\n', font=('Segoe UI', 10), no_button=True)
        # print(f'Searching in: {searchURL}\n')

        try:
            request = requests.get(searchURL)
        except:
            print('Something went wrong.')
            return 0

        result = BeautifulSoup(request.content, 'lxml', parse_only=SoupStrainer('a'))

        for i in result.find_all('a', href=True):
            if (i.get('href') != None) and (i.get('href').startswith('magnet:?xt=')) and (len(i.get('href')) > 64):
                if i.get('href') not in self.links:
                    self.links[self._getTorrentName(i.get('href'))] = i.get('href')

        self.links['foundLinks'] = len(self.links)

    def _getTorrentName(self, magnetLink):
        name = magnetLink.split('tr=')[0][64:-1]

        if name.startswith(';dn=') and name.endswith('&amp'):
            name = name[4:-4]

        return urllib.parse.unquote_plus(name)

    def magnetsToJSON(self, filename):
        if os.path.exists(os.path.join(os.getcwd(), 'json')) == False:
            os.mkdir(os.path.join(os.getcwd(), 'json'))

        pathToFile = os.path.join(os.getcwd(), 'json')

        data = json.dumps(self.links, indent=4)

        with open(os.path.join(pathToFile, f'{filename}.json'), 'w', encoding='utf-8') as file:
            file.write(data)
