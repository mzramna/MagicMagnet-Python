import PySimpleGUI as sg
import os,json,sys
import pyperclip
from scripts.algorithm import MagicMagnet
from scripts.settings import Settings
import argparse

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
sg.LOOK_AND_FEEL_TABLE['MagicMagnetLight'] = {
    'BACKGROUND': 'white',
    'TEXT': '#323232',
    'INPUT': '#dfe2e8',
    'TEXT_INPUT': '#000000',
    'SCROLL': '#c7e78b',
    'BUTTON': ('white', '#ff0000'),
    'PROGRESS': ('white', 'black'),
    'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
}

sg.LOOK_AND_FEEL_TABLE['MagicMagnetDark'] = {
    'BACKGROUND': '#292929',
    'TEXT': '#cccccc',
    'INPUT': '#dfe2e8',
    'TEXT_INPUT': '#000000',
    'SCROLL': '#c7e78b',
    'BUTTON': ('white', '#ff0000'),
    'PROGRESS': ('white', 'black'),
    'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
}

settings = Settings()
setting = settings.read_settings()

sg.change_look_and_feel(setting['theme'])
font = ('Segoe UI Light', 12)
try:
    search_params = json.load(open("search_parameters.json"))
except:
    search_params=json.load(open(resource_path("search_parameters.json")))
    json.dump(search_params,open("search_parameters.json",'w+'))

sites_alias=[]
sites_code_name=search_params.keys()
for site in search_params:
    sites_alias.append(search_params[site]["alias"])



def create_table(websites_names: [str]):
    checkboxs = []
    for website_name_index in range(0,len(websites_names),3):
        checkbox_line =[]
        if len(websites_names)>website_name_index+2:
            checkbox_line.append(sg.Checkbox(websites_names[website_name_index],font=font))
            checkbox_line.append(sg.Checkbox(websites_names[website_name_index+1], font=font))
            checkbox_line.append(sg.Checkbox(websites_names[website_name_index + 2], font=font))
        elif len(websites_names)>website_name_index+1:
            checkbox_line.append(sg.Checkbox(websites_names[website_name_index],font=font))
            checkbox_line.append(sg.Checkbox(websites_names[website_name_index+1], font=font))
        else:
            checkbox_line.append(sg.Checkbox(websites_names[website_name_index],font=font))
        checkboxs.append(checkbox_line)
    column=sg.Column(checkboxs,scrollable=True,vertical_scroll_only=True,size=[350,100])
    return column

def layout_builder(website_names:[str]):
    result=[]

    result.append([sg.Text('\n', font=('Segoe UI Light', 5))])
    result.append([sg.Text('  Magic Magnet', font=('Segoe UI Light', 24), text_color='#ff0000', justification='left'), sg.Image(resource_path('icon.png'))])
    result.append([sg.Text('    Search for something', font=('Segoe UI Light', 14))])
    result.append([sg.Text('\n', font=('Segoe UI Light', 1))])
    result.append([sg.Text('  '), sg.InputText(size=(28, 6), font=font), sg.VerticalSeparator(pad=(4, (3, 4))), sg.Submit('Search', size=(12, 0), font=('Segoe UI Light', 10, 'bold'))])
    result.append([sg.Text('\n', font=('Segoe UI Light', 1))])
    result.append([sg.Text('    Choose your search source for content', font=('Segoe UI Light', 14))])
    result.append([sg.Text('\n', font=('Segoe UI Light', 1))])
    result.append([create_table(website_names)])
    result.append([sg.Text('\n', font=('Segoe UI Light', 1))])
    result.append([sg.Text('                total of pages to search(if applied):', font=font),sg.Spin([i for i in range(1,30)], initial_value=5)])
    result.append([sg.Text(f'    Application theme', font=('Segoe UI Light', 14)),
                   sg.Radio('Light', 'theme', default=True if 'Light' in setting['theme'] else False, font=font),
                    sg.Radio('Dark', 'theme', default=True if 'Dark' in setting['theme'] else False, font=font),
                    sg.Button('Apply', size=(7, 0), font=('Segoe UI Light', 10, 'bold'))])
    result.append([sg.Text('\n', font=('Segoe UI Light', 1))])
    result.append([sg.Text('  '), sg.Button('Support this project', size=(17, 0), font=('Segoe UI Light', 10, 'bold')),
     sg.VerticalSeparator(pad=(6, 3)), sg.Button('About', size=(7, 0), font=('Segoe UI Light', 10, 'bold')),
     sg.VerticalSeparator(pad=(6, 3)), sg.Button('Exit', size=(12, 0), font=('Segoe UI Light', 10, 'bold'))])
    result.append([sg.Text('\nDeveloped by Pedro Lemos (@pedrolemoz) and mzramna (@mzramna)', font=font, size=(42, 0), justification='center')])
    return result

def Search(value_to_search,sites_to_search,amount_of_pages,process):
    process.search(value_to_search, sites_to_search, total_search_pages=amount_of_pages)

def UI(process):
    mainLayout = layout_builder(sites_alias)

    window = sg.Window('Magic Magnet', mainLayout, icon='icon.ico')



    while True:
        event, values = window.read()

        if event in (None, 'Exit'):
            window.close()
            break

        if event == 'Apply':
            status = False
            print(values)
            if values[len(values)-1]:
                status = settings.change_theme('MagicMagnetLight')

            elif values[len(values)]:
                status = settings.change_theme('MagicMagnetDark')

            if status:
                restartLayout = [
                    [sg.Text('\n', font=('Segoe UI Light', 5))],
                    [sg.Text('Restart to apply changes', font=('Segoe UI Light', 14), size=(20, 0), justification='left')],
                    [sg.Text('\n', font=('Segoe UI Light', 1))]
                ]

                restartWindow = sg.Window('Sucess!', restartLayout, auto_close=True, icon='icon.ico')

                restartEvent, restartResult = restartWindow.read()

        if event == 'Support this project':
            os.startfile('https://github.com/mzramna/MagicMagnet-Python/')

        if event == 'About':
            aboutLayout = [
                [sg.Text('\n', font=('Segoe UI Light', 1))],
                [sg.Text('This project was born with an idea for automatize torrent downloading.\nI don\'t wanna search for torrent and see boring adverts. This program search on many sources and return all found magnet links and is able to start the default torrent application, copy links and save its to file.', font = ('Segoe UI', 12), size = (56, 0), justification='left')],
                [sg.Text('\n', font=('Segoe UI Light', 1))],
                [sg.Text(' ' * 101), sg.Button('Close', size=(12, 0), font = ('Segoe UI Light', 10, 'bold'))],
                [sg.Text('\n', font = ('Segoe UI Light', 1))]
            ]

            aboutWindow = sg.Window('About project', aboutLayout, icon='icon.ico')

            while True:
                aboutEvent, aboutValues = aboutWindow.read()
                if aboutEvent in (None, 'Close'):
                    aboutWindow.close()
                    break

        if event == 'Search':
            search_sites=[]
            for i in range(2,len(values)-3):
                if values[i]:
                    search_sites.append(sites_alias[i - 2])
            Search(value_to_search=values[1], sites_to_search=search_sites,amount_of_pages=int(values[len(values)-2]),process=process)

            downloadLinks = []

            [downloadLinks.append(i) if i != 'foundLinks' else None for i in process.links.keys()]

            results_Layout = [
                [sg.Text('\n', font = ('Segoe UI Light', 5))],
                [sg.Text('Process finished sucessfully!', font = ('Segoe UI Light', 14), size = (30, 0), justification = 'left')],
                [sg.Text('\n', font = ('Segoe UI Light', 1))],
                [sg.Listbox(values = downloadLinks, size = (90, 15), font=('Segoe UI', 10), enable_events=True)],
                [sg.Text('\n', font=('Segoe UI Light', 1))],
                [sg.Text(' ' * 16), sg.Button('Save all links to file', size=(22, 0), font=('Segoe UI Light', 10, 'bold')), sg.Button('Open magnet link', size=(16, 0), font=('Segoe UI Light', 10, 'bold')), sg.Button('Copy magnet link', size=(16, 0), font=('Segoe UI Light', 10, 'bold')), sg.Button('Close', size=(12, 0), font=('Segoe UI Light', 10, 'bold'))],
                [sg.Text('\n', font=('Segoe UI Light', 1))]
            ]

            sg.PrintClose()

            resultsWindow = sg.Window('Sucess!', results_Layout, icon='icon.ico')

            while True:
                resultsEvent, resultsValues = resultsWindow.read()

                if resultsEvent in (None, 'Close'):
                    process.links, downloadLinks = {}, []
                    process.links['foundLinks'] = 0
                    resultsWindow.close()
                    break

                if resultsEvent == 'Save all links to file':
                    process.magnetsToJSON(values[1])

                    saveLayout = [
                        [sg.Text('\n', font=('Segoe UI Light', 5))],
                        [sg.Text(f'Magnet links saved sucessfully!', size=(25, 0), font=('Segoe UI Light', 14), justification='left')],
                        [sg.Text('\n', font=('Segoe UI Light', 1))],
                        [sg.Text(' ' * 6), sg.Button('Open file', size=(12, 0), font=('Segoe UI Light', 10, 'bold')), sg.Button('Close', size=(12, 0), font=('Segoe UI Light', 10, 'bold'))],
                        [sg.Text('\n', font=('Segoe UI Light', 1))]
                    ]

                    saveWindow = sg.Window('Sucess!', saveLayout, icon='icon.ico')

                    while True:
                        saveEvent, saveResult = saveWindow.read()

                        if saveEvent in (None, 'Close'):
                            saveWindow.close()
                            break

                        if saveEvent == 'Open file':
                            os.startfile(os.path.join(os.getcwd(), 'json', f'{values[1]}.json'))

                if resultsEvent == 'Open magnet link':
                    os.startfile(process.links[resultsValues[0][0]])

                if resultsEvent == 'Copy magnet link':
                    pyperclip.copy(process.links[resultsValues[0][0]])

                    clipboardLayout = [
                        [sg.Text('\n', font=('Segoe UI Light', 5))],
                        [sg.Text('Copied to clipboard!', font=('Segoe UI Light', 14), size=(17, 0), justification='left')],
                        [sg.Text('\n', font=('Segoe UI Light', 1))]
                    ]

                    clipboardWindow = sg.Window('Sucess!', clipboardLayout, auto_close=True, icon='icon.ico')

                    clipboardEvent, clipboard_result = clipboardWindow.read()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("-w","--search-websites",help="the websites where will search, default 5")
    parser.add_argument("-n","--number-of-pages",help="the amount of pages that will search in each compatible website, default all")
    parser.add_argument("-s","--value-to-search",help="the text wich will be researched")
    args=parser.parse_args()
    print(args)
    empty_params=0
    process = MagicMagnet()
    for i in args.__dict__ :
        if args.__dict__[i] == None:
            empty_params+=1
    if empty_params == len(args.__dict__):
        print("open UI")
        process.ui = True
        UI(process)
    else:
        parameters = {}
        if args.value_to_search == None:
            print("the parameter --value-to-search is mandatory in console mode")
            exit(1)
        else:
            parameters["value_to_search"]=args.value_to_search

        if args.search_websites == None or args.search_websites == "all" :
            parameters["search_websites"]=sites_alias
        else:
            try:
                tmp_sites=args.search_websites.split(",")
                tmp_sites[0]
            except :
                tmp_sites=[tmp_sites]
            for site in tmp_sites:
                print(site)
                if site not in sites_code_name:
                    print("all the parameters of --search-websites must be one of the codes into the json file,not alias name")
                    exit(1)
            parameters["search_websites"]=tmp_sites
        if args.number_of_pages == None:
            parameters["number_of_pages"]=5
        else:
            parameters["number_of_pages"]=int(args.number_of_pages)

        print(parameters)
        process.ui=False
        Search(value_to_search=parameters["value_to_search"],sites_to_search=parameters["search_websites"],amount_of_pages=parameters["number_of_pages"],process=process)
if __name__ == "__main__":
    main()