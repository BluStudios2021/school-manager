#!/usr/bin/env python3

from os.path import exists, expanduser
from os import remove, system
from pdf2image import convert_from_path
import PySimpleGUI as sg

# Variables
homePath = expanduser('~')
fileName = homePath + '/Documents/Scripts/assets/paths.txt'
subjectFile = homePath + '/Documents/Scripts/assets/subjects.txt'
exportPath = '/assets/'
selectedSubject = ''
pages = ['home', 'name', 'open']
currentPage = pages[0]
lastPage = ''

# Functions

# replaces a given line with the given string in file
def __changeLine(line, string):
    if not exists(fileName):
        with open(fileName, 'w') as f:
            f.write('')
    with open(fileName, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()
    with open(fileName, 'w') as f:
        if (line < len(lines)):
            lines[line] = string
        else:
            lines.append(string)
        f.writelines('\n'.join(lines))

# saves the last used fetch path
def setFetchPath(path):
    path = path[:path.rfind('/') + 1]
    __changeLine(0, path)

# gets the last used fetch path
def getFetchPath():
    if exists(fileName):
        with open(fileName, 'r') as f:
            lines = f.readlines()
            if len(lines) > 0:
                return lines[0].rstrip()
    return '~/'

# checks if filename is valid
def isValid(name):
    try:
        with open(name, 'x') as tempfile: # OSError if file exists or is invalid
            pass
        remove(name)
        return True
    except OSError:
        return False

# reads the subjects from file
def getSubjects():
    with open(subjectFile, 'r') as f:
        string = f.readline().rstrip()
        subjects = string.split(',')
        subjects.pop(0)
        return subjects
    return []

# reads the parent folder path from file
def getParentFolder():
    with open(subjectFile, 'r') as f:
        string = f.readline().rstrip()
        strings = string.split(',')
        path = strings[0]
        if path[-1:] != '/':
            path += '/'
            print(path)
        return path
    return ''

# creates the Buttons for the Subjects
def createSubjectButtons(key, prefix = '', postfix = ''):
    subjects = getSubjects()
    counter = 0
    cols = [[], [], [], []]
    for subject in subjects:
        button = sg.Button(prefix + subject + postfix, expand_x=True)
        cols[counter].append([button])
        counter+= 1
        if counter > 3:
            counter = 0

    row = []
    for i in range(4):
        row.append(sg.Column(cols[i], key='-' + key + str(i) +'-', expand_x=True, vertical_alignment='top', pad=(0, 0)))

    return row

# switches page
def switchPage(key):
    global lastPage
    global currentPage
    for page in pages:
        if page == key:
            window[page].update(visible=True)
            lastPage = currentPage
            currentPage = key
        else:
            window[page].update(visible=False)

# Main

sg.theme('DarkGrey5')

subjects = getSubjects()

# main page

page0 = [   [sg.Text('Open Subject')],
            createSubjectButtons('open', '[', ']'),
            [sg.Text('')],
            [sg.Text('Import pdf file')],
            [sg.InputText(key='-filepath-', expand_x=True), sg.FileBrowse('Browse', key='-filebrowse-', file_types=(('PDF Files', '*.pdf'),), initial_folder=getFetchPath())],
            [sg.Button('Import')] ]

# choose name for pdf page

page1 = [   [sg.Text('Choose name')],
            [sg.InputText(key='-name-')],
            [sg.Text('Select Subject')],
            createSubjectButtons('select'),
            [sg.Text('')],
            [sg.Button('Back')] ]

# select what to open for each subject

page2 = [   [sg.Text('Select what to open')],
            [sg.Button('Heft', expand_x=True)],
            [sg.Button('Übungen', expand_x=True)],
            [sg.Text('')],
            [sg.Button('Back')] ]

# main layout

layout = [  [sg.Column(page0, key=pages[0]), 
            sg.Column(page1, key=pages[1], visible=False),
            sg.Column(page2, key=pages[2], visible=False),
            ] ]

window = sg.Window('School Manager', layout, icon='~/Pictures/Icons/module_icon.png')

while True:
    export = False
    event, values = window.read()
    # handles close event
    if event == sg.WIN_CLOSED:
        break
    # confirms the pdf and continues to second page
    if event == 'Import':
        filePath = values['-filepath-']
        # check if file is a pdf and exists
        if exists(filePath) and filePath[-4:] == ".pdf":
            # saves the folder from the pdf for next use
            setFetchPath(filePath)
            # switches the pages
            switchPage('name')
            # updates the name
            window['-name-'].update(filePath[filePath.rfind('/') + 1:-4])
        else:
            sg.popup('The specified PDF file does not exist!', title='Wrong Input')

    # swiches back to first page
    if event in ['Back', 'Back0']:
        switchPage(lastPage)
    
    for subject in subjects:
        if event == subject:
            selectedSubject = subject
            export = True
        if event == '[' + subject + ']':
            selectedSubject = subject
            switchPage('open')

    if event == 'Heft':
        system('xdg-open "' + getParentFolder() + selectedSubject + '/_Heft-' + selectedSubject + '.xopp"')
        switchPage('home')

    if event == 'Übungen':
        system('xdg-open "' + getParentFolder() + selectedSubject + '/_Übungen-' + selectedSubject + '.xopp"')
        switchPage('home')
        

    # Exports the Images
    if export:
        # get values
        name = values['-name-']
        dpi = 200
        filePath = values['-filepath-']
        savePath = getParentFolder() + selectedSubject + exportPath
        print(savePath)
        # check if savePath is empty
        if (len(savePath) > 1):
            # checks if the name is valid and exists
            if isValid(savePath + name + '-0.jpg'):
                # checks if the path exists on the system
                if exists(savePath):
                    # converts the images
                    images = convert_from_path(filePath, dpi=dpi)
                    # saves the images with added page count
                    for i in range(len(images)):
                        images[i].save(savePath + name + '-' + str(i) +'.jpg', 'JPEG')
                    # saves the save path for the next use
                    # tells the user that it was succesful
                    sg.popup('Images have been exported!', title='Successful')
                    # swichtes back to first page
                    switchPage('home')
                else:
                    sg.popup('The export folder does not exist!', title='Wrong Path')
            else:
                sg.popup('The name is invalid or already exists!', title='Invalid Name')
        else:
            sg.popup('The export folder does not exist!', title='Wrong Path')

window.close()
