from tkinter import *
from tkinter.ttk import *
import PySimpleGUI as sg
from settings import *

defaultSettings = Settings("Default",1000)
debugSettings = Settings("Debug",10)
customSettings = Settings()

def callback(var, index, mode,window):
    window.write_event_value("preset", window['preset'].TKStringVar.get())

def gui():
    settings = Settings()

    sg.theme('DarkGrey8')
    sg.set_options(font=("Calibri", 16))

    customLayout = [
        [
            sg.CB('Phase 1'),
            sg.CB('Phase 2'),
            sg.CB('Phase 3'),
            sg.CB('Phase 4'),
            sg.CB('Phase 5'),
            sg.CB('Phase 6')
        ],
        [
            sg.Text('Number to Generate per Phase:'),
            sg.InputText('num',size=6,key='generateNum')
        ],
        [
            sg.Text('Output Path:'),
            sg.InputText('OutputData',size=45,font='Helvetica12',key='outputPathText'),
            sg.FolderBrowse(key='outputPathBrowse')
        ]
    ]

    advancedLayout = [
        [
            sg.Text('Number of armor plates:'),
            sg.InputText('Min',size=4),
            sg.InputText('Max',size=4)
        ]
    ]

    advancedDropdown = [
        [
            sg.T(sg.SYMBOL_UP+' Advanced Settings', enable_events=True, key='advancedButton'),
        ],
        [
            sg.pin(sg.Column(advancedLayout, key='advancedDropdown',visible=False,metadata=(sg.SYMBOL_DOWN+' Advanced Settings', sg.SYMBOL_UP+' Advanced Settings')))
        ]
    ]

    layout = [
        [
            sg.OptionMenu(default_value='Default',values=('Default','Debug','Custom'),key='preset'),
            sg.Push(),sg.Button('Generate Data',key='generate')
        ],
        [
            sg.pin(sg.Column(customLayout, visible=False, key='custom')), 
        ],
        [
            sg.pin(sg.Column(advancedDropdown,visible=False, key='advanced'))
        ]
    ]
    window = sg.Window('CU-ROBOTICS Data Generator', layout,finalize=True)
    window['preset'].TKStringVar.trace("w", lambda var, index, mode: callback(var, index, mode, window))

    while True:
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED:
            break
        # Preset was changed
        elif event == 'preset':
            if values['preset'] == 'Custom':
                window['custom'].update(visible=True)
                window['advanced'].update(visible=True)
            else:
                window['custom'].update(visible=False)
                window['advanced'].update(visible=False)
        # Output Folder Path was chosen
        elif event == 'outputPathBrowse':
            window['outputPathText'].update(window['outputPathBrowse'].get())
        # Advanced Dropdown was clicked
        elif event.startswith('advanced'):
            window['advancedDropdown'].update(visible=not window['advancedDropdown'].visible)
            window['advancedButton'].update(window['advancedDropdown'].metadata[0] if window['advancedDropdown'].visible else window['advancedDropdown'].metadata[1])
        # Generate Data Button was clicked
        elif event == 'generate':
            if values['preset'] == 'Default': 
                settings = defaultSettings
            elif values['preset'] == 'Debug': 
                settings = debugSettings
            elif values['preset'] == 'Custom':
                settings = Settings('Custom',values['generateNum'],values['Phase 1'],values['Phase 2'],values['Phase 3'],values['Phase 4'],values['Phase 5'],values['Phase 6'])
            window.close()
            # sg.PopupNoButtons('AYO')
            return settings

    window.close()

gui()