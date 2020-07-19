import os
import json
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer
import asyncio
import aiohttp


class MagicMagnet():
    def __init__(self):
        self.links = {'foundLinks': 0}

    async def search(self, searchContent, sites: [str], total_search_pages=5):
        search_params = json.load(open("search_parameters.json"))
        for site in search_params:
            if search_params[site]["alias"] in sites:
                if "urlEncode" not in search_params[site] or search_params[site]["urlEncode"] == "":
                    search_params[site]["searchURL"] = str(search_params[site]["searchURL"]).replace("{searchContent}",
                                                                                                     str(
                                                                                                         urllib.parse.quote_plus(
                                                                                                             searchContent)))
                elif search_params[site]["urlEncode"] == "utf-8":
                    search_params[site]["searchURL"] = str(search_params[site]["searchURL"]).replace("{searchContent}",
                                                                                                     str(
                                                                                                         urllib.parse.quote(
                                                                                                             searchContent)))
                else:
                    search_params[site]["searchURL"] = str(search_params[site]["searchURL"]).replace("{searchContent}",
                                                                                                     str(
                                                                                                         urllib.parse.quote_plus(
                                                                                                             searchContent,
                                                                                                             encoding=
                                                                                                             search_params[
                                                                                                                 site][
                                                                                                                 "urlEncode"])))
                if "multiple_page" in search_params[site] and search_params[site]["multiple_page"]:
                    for page in range(1, total_search_pages):
                        search_params[site]['searchURL'] = search_params[site]['searchURL'].replace("{page}", str(page))
                        if search_params[site]["need_param"]:
                            await self._getDownloadPages(search_params[site]['searchURL'],
                                                   resultURL=search_params[site]["resultURL"],
                                                   start=search_params[site]['start'],
                                                   notIn=search_params[site]['notIn'],
                                                   sliceString=search_params[site]['sliceString'])
                        else:
                            await self._getPageLinks(search_params[site]["searchURL"])
                else:
                    if search_params[site]["need_param"]:
                        await self._getDownloadPages(search_params[site]['searchURL'],
                                               resultURL=search_params[site]["resultURL"],
                                               start=search_params[site]['start'],
                                               notIn=search_params[site]['notIn'],
                                               sliceString=search_params[site]['sliceString'])
                    else:
                        await self._getPageLinks(search_params[site]["searchURL"])

    async def _getDownloadPages(self, searchURL,start, resultURL = None,  notIn = None, sliceString = None):
        if resultURL == "":
            resultURL = None
        if notIn == "":
            notIn = None
        if sliceString == "":
            sliceString = None
        async with aiohttp.ClientSession() as client:
        
	        async with client.get(searchURL) as request:
		        result = BeautifulSoup(await request.text(), 'lxml', parse_only = SoupStrainer('a'))
		
		        linksChecked = []
		
		        for i in result.find_all('a', href = True):
		            if i.get('href').startswith(start) and i.get('href') not in linksChecked and ('#download' not in i.get('href')):
		                
		                valid = True
		
		                if (start != None) and (notIn != None):
		                    for link in notIn:
		                        if link in i.get('href'):
		                            valid = False
		
		                if valid == True:
		                    linksChecked.append(i.get('href'))
		                    if resultURL != None:
		                        if sliceString != None:
		                            await self._getPageLinks(f'{resultURL}{i.get("href")[sliceString[0]:sliceString[1]]}')
		                        else:
		                            await self._getPageLinks(f'{resultURL}{i.get("href")}')
		                    else:
		                        if sliceString != None:
		                            await self._getPageLinks(i.get('href')[sliceString[0]:sliceString[1]])
		                        else:
		                            await self._getPageLinks(i.get('href'))

    async def _getPageLinks(self, searchURL):
        if searchURL.endswith('/&s'):
            searchURL = searchURL[:-2] 

        #sg.Print(f'Searching in: {searchURL}\n', font=('Segoe UI', 10), no_button=True)
        print(f'Searching in: {searchURL}\n')
        
        async with aiohttp.ClientSession() as client:
        	async with client.get(searchURL) as request:
	      
		        result = BeautifulSoup(await request.text(), 'lxml', parse_only = SoupStrainer('a'))
		
		        for i in result.find_all('a', href = True):
		            if (i.get('href') != None) and (i.get('href').startswith('magnet:?xt=')) and (len(i.get('href')) > 64):
		                if i.get('href') not in self.links:
		                    self.links[self._getTorrentName(i.get('href'))] = i.get('href')
		        
		        self.links['foundLinks'] = len(self.links)

    def _getTorrentName(self, magnetLink):
        name = magnetLink.split('tr=')[0][64:-1]

        if name.startswith(';dn=') and name.endswith('&amp'):
            name = name[4:-4]

        return urllib.parse.unquote_plus(name)

    async def magnetsToJSON(self, filename):
        if os.path.exists(os.path.join(os.getcwd(), 'json')) == False:
            os.mkdir(os.path.join(os.getcwd(), 'json'))

        pathToFile = os.path.join(os.getcwd(), 'json')

        data = json.dumps(self.links, indent = 4)

        with open(os.path.join(pathToFile, f'{filename}.json'), 'w', encoding = 'utf-8') as file:
            file.write(data)

async def main():  
	magic_magnet = MagicMagnet()
	await magic_magnet.search('Ubuntu', google = False, tpb = True)
	print(magic_magnet.links)
	
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
