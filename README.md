
<p align="center">
  <img src="https://github.com/pedrolemoz/MagicMagnet-Python/raw/python/assets/logo_256x256.png" alt="Logo"/>

<p align="center">
  <img src="http://ForTheBadge.com/images/badges/made-with-python.svg" alt="Made with Python"/>


![GitHub repo size](https://img.shields.io/github/repo-size/mzramna/MagicMagnet-Python?color=red)
[![Project Owner](https://img.shields.io/badge/owner-Pedro%20Lemos-orange)](https://github.com/pedrolemoz/)
[![Project Owner](https://img.shields.io/badge/owner-mzramna-red)](https://github.com/mzramna/)
![GitHub stars](https://img.shields.io/github/stars/mzramna/MagicMagnet-Python?style=social)
[![GitHub forks](https://img.shields.io/github/forks/mzramna/MagicMagnet-Python?style=social)](https://github.com/mzramna/MagicMagnet-Python/fork)

## Get magnet links from internet without any effort! :magnet:

## Screenshots

<p align="center">
  <img src="./assets/screenshot_main_menu_light.png" alt="Menu light"/>
  <img src="./assets/screenshot_main_menu_dark.png" alt="Menu light"/>
  
*Main menu in light and dark themes*

## Getting started

### How to use

Type what content you wanna links for, in the search box, select one or more of sources and click in the search button.

By now, supported sources are:

* Google (Slow, but works fine for dubbed content)
* The Pirate Bay (Fast, and works for every content)
* 1337x (Fast, and works for every content)
* Nyaa (Fast, focused in anime RAW's)
* EZTV (Fast, focused in TV Shows)
* YTS (Fast, focused in lightweight movies)
* Demonoid (Fast, focused in TV Shows)
* ETTV (Slow, focused in TV Shows)

After the search is finished, you can:

* Save all links to a JSON
* Open the selected magnet link with your default torrent client
* Copy the magnet link to your clipboard

> JSONS are saved to '/MagicMagnet/json/' by default.

We plan to add new features, such:

* Save magnet links as a ```.torrent``` file
* Get info about seeders and leechers and use it to rate torrents
* Download torrents without a external client

For development, we plan to use the ```asyncio``` library (for a asynchronous code), since we are dealing with web requests to fetch our magnet links, and try to optimize the speed and stability. Futhermore, we plan to use regular expressions, since our API is a litte bit primitive.

### From an executable (for Windows)

Download the latest [build](https://github.com/mzramna/MagicMagnet-Python/blob/python/build/MagicMagnet-amd64.rar) and you're done.

### From source

In order to run this program from source, you'll need:

* Latest version of Python3
* Git (optional)
* Install dependencies

To install Python3, please visit [Python official website](https://www.python.org/downloads/), download and install the latest package available. If you are using GNU/Linux, you may already have Python3 installed in your system. Type ```python3 --version``` to check.

To install Git, please visit [Git official website](https://git-scm.com/downloads), download and install the latest package available. Setup Git with your name and email. Clone the repository to your machine using the following command:

``` 
git clone https://github.com/pedrolemoz/MagicMagnet-Python.git
```

If you don't wanna install Git, just download the ```.zip``` from this repository (the green button above), and unzip it in your machine.

To install dependencies, type the following command in your command prompt or terminal (make sure to be in the project directory):

```
pip install -r requirements.txt
```

### Building the application

If you forked this project and want to build your executable, there's a script to do it. I used ```cx_Freeze``` to build the program.

Install ```cx_Freeze``` using ```pip``` with the following command:

```
pip install cx-Freeze
```

To build the application:

```
python build_application.py build
```

It will create a folder called ```build``` with the executable inside.

> Note 1: I don't know why, but cx_Freeze doesn't work for me in Python 3.8. I'm currently using Python 3.7.6 to build this project.

> Note 2: If your executable fail to start, try rename the folder Tkinter in lib directory to tkinter.


to add new websites just edit the `search_parameters.json` file like this:
```
"google": { ##website reference for easy debug
    "need_param": true,                                                                 ##  parameter that defines if the folowing parameters will be needed
    "multiple_page":false,                                                              ##  parameter that determine if page 
    "alias": "Google",                                                                  ##  name shown in options
    "searchURL": "https://www.google.com/search?q={searchContent}+download+torrent",    ##  url with the tag {searchContent} that will be replaced by the searching keyords,and it necessary the {page} tag that symbolizes the result page if aplies to website
    "resultURL": "",                                                                    ##  url where the query result will be shown
    "start": "/url?q=",                                                                 ##  begining of the result url string
    "notIn": [                                                                          ##  will not accept results in this hostnames
      "accounts.google.com",
      ".org",
      "youtube.com",
      "facebook.com"
    ],
    "sliceString": [                                                                    ##  how to slice the result strings
      7,
      -88
    ],
    "urlEncode": ""                                                                     ##  define,if necessary,the url encode, probly if empty not work, replace with "utf-8"
```
