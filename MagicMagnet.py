import PySimpleGUI as sg
import os,json
import pyperclip
from scripts.algorithm import MagicMagnet
from scripts.settings import Settings

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
search_params = json.load(open("search_parameters.json"))
sites=[]
for site in search_params:
    sites.append(search_params[site]["alias"])
def create_checkboc(name: str):
    return sg.Checkbox(name, font=font, size=(11, 1))


def create_table(websites_names: [str]):
    result = []
    for website_name_index in range(0,len(websites_names),3):
        if website_name_index+2 <len(websites_names):
            result.append([sg.Text('  '), sg.Checkbox(websites_names[website_name_index], font=font, default=True),
     sg.Checkbox(websites_names[website_name_index+1], font=font), sg.Checkbox(websites_names[website_name_index+2], font=font)])
        elif website_name_index+1 <len(websites_names):
            result.append(
                [sg.Text('  '), sg.Checkbox(websites_names[website_name_index], font=font, default=True),
                 sg.Checkbox(websites_names[website_name_index + 1], font=font,)])
        else:
            result.append(
                [sg.Text('  '), sg.Checkbox(websites_names[website_name_index], font=font,  default=True)])
    return result

def layout_builder(website_names:[str]):
    result=[]

    result.append([sg.Text('\n', font=('Segoe UI Light', 5))])
    result.append([sg.Text('  Magic Magnet', font=('Segoe UI Light', 24), text_color='#ff0000', justification='left'), sg.Image('icon.png')])
    result.append([sg.Text('    Search for something', font=('Segoe UI Light', 14))])
    result.append([sg.Text('\n', font=('Segoe UI Light', 1))])
    result.append([sg.Text('  '), sg.InputText(size=(28, 6), font=font), sg.VerticalSeparator(pad=(4, (3, 4))), sg.Submit('Search', size=(12, 0), font=('Segoe UI Light', 10, 'bold'))])
    result.append([sg.Text('\n', font=('Segoe UI Light', 1))])
    result.append([sg.Text('    Choose your search source for content', font=('Segoe UI Light', 14))])
    result.append([sg.Text('\n', font=('Segoe UI Light', 1))])
    for line in create_table(website_names):
        result.append(line)

    result.append([sg.Text('\n', font=('Segoe UI Light', 1))])
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

mainLayout = layout_builder(sites)

window = sg.Window('Magic Magnet', mainLayout, size=(430, 510), icon='icon.ico')

process = MagicMagnet()

while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        window.close()
        break
    
    if event == 'Apply':
        status = False

        if values[10]:
            status = settings.change_theme('MagicMagnetLight')
        
        elif values[11]:
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
        for i in range(2,len(values)):
            if values[i]:
                search_sites.append(sites[i-2])
        process.search(values[1], search_sites)

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
