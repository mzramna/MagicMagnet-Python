import json
import os
import urllib.parse

import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup, SoupStrainer


class MagicMagnet():
    def __init__(self,debug=True,search_param_json="search_parameters.json"):
        self.links = {'foundLinks': 0}
        self.debug=debug
        self.search_params = json.load(open(search_param_json))

    def search(self,sites: [str], searchContent:str,  total_search_pages=5):

        for site in self.search_params:
            if self.search_params[site]["alias"] in sites:
                if "urlEncode" not in self.search_params[site] or self.search_params[site]["urlEncode"] == "":
                    self.search_params[site]["searchURL"]=str(self.search_params[site]["searchURL"]).replace("{searchContent}",str(urllib.parse.quote_plus(searchContent)))
                elif self.search_params[site]["urlEncode"]=="utf-8":
                    self.search_params[site]["searchURL"] = str(self.search_params[site]["searchURL"]).replace("{searchContent}",str(urllib.parse.quote(searchContent)))
                else:
                    self.search_params[site]["searchURL"] = str(self.search_params[site]["searchURL"]).replace("{searchContent}",str(urllib.parse.quote_plus(searchContent,encoding=self.search_params[site]["urlEncode"])))
                if "multiple_page" in self.search_params[site] and self.search_params[site]["multiple_page"]:
                    for page in range(1, total_search_pages):
                        self.search_params[site]['searchURL']=self.search_params[site]['searchURL'].replace("{page}", str(page))
                        if self.search_params[site]["need_param"]:
                            self._getDownloadPages(self.search_params[site]['searchURL'],
                                                   resultURL=self.search_params[site]["resultURL"],
                                                   start=self.search_params[site]['start'],
                                                   notIn=self.search_params[site]['notIn'],
                                                   sliceString=self.search_params[site]['sliceString'])
                        else:
                            self._getPageLinks(self.search_params[site]["searchURL"])
                else:
                    if self.search_params[site]["need_param"]:
                        self._getDownloadPages(self.search_params[site]['searchURL'],
                                               resultURL=self.search_params[site]["resultURL"],
                                               start=self.search_params[site]['start'],
                                               notIn=self.search_params[site]['notIn'],
                                               sliceString=self.search_params[site]['sliceString'])
                    else:
                        self._getPageLinks(self.search_params[site]["searchURL"])

    def _getDownloadPages(self, searchURL, start, resultURL="", notIn="", sliceString=""):
        if resultURL == "":
            resultURL = None
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
        if self.debug:
            if self.ui:
                sg.Print(f'Searching in: {searchURL}\n', font=('Segoe UI', 10), no_button=True)
            else:
                print(f'Searching in: {searchURL}\n')
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
