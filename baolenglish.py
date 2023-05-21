import json
import PySimpleGUI as sg
import pyautogui
import win32gui
import win32con

# Read the JSON config file
with open('config.json', 'r') as f:
    config_data = json.load(f)

# Extract the image filenames from the configs
image_filenames = [item['image'] for item in config_data]

# Define the tooltip positions and messages for each target image
tooltip_data_list = [item['positions'] for item in config_data]

# Create the tooltip windows for target images
tooltip_windows_list = []
dragged_tooltip_window = None  # Variable to track the dragged tooltip window

for tooltip_data in tooltip_data_list:
    tooltip_windows = []
    for tooltip_position, tooltip_message in tooltip_data.items():
        tooltip_x, tooltip_y = map(int, tooltip_position.split(','))
        tooltip_layout = [
            [sg.Text(tooltip_message, background_color='white', text_color='black', font=('Impact', 10),
                     key='-TOOLTIP-', pad=(0, 0))]
        ]
        tooltip_window = sg.Window('', tooltip_layout,
                                   location=(tooltip_x, tooltip_y), no_titlebar=True, keep_on_top=True,
                                   grab_anywhere=True, finalize=True, element_padding=(0, 0), margins=(0, 0))
        hwnd = win32gui.GetParent(tooltip_window.TKroot.winfo_id())  # Get window handle
        old_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_style = old_style | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
        tooltip_windows.append(tooltip_window)

        # Add event handler to capture tooltip dragging
        tooltip_window.bind('<B1-Motion>', '-TOOLTIP-DRAG-')

    tooltip_windows_list.append(tooltip_windows)

# Set the loop flag
running = True

# Define the GUI layout
layout = [
    [sg.Button('Toggle Tooltips', key='-TOGGLE-')],
    [sg.Button('Toggle Click-Through', key='-CLICK_THROUGH-')],
    [sg.Text('Tooltips: Off', key='-TOOLTIP_STATUS-', size=(15, 1))],
    [sg.Text('Click-Through: Enabled', key='-CLICK_THROUGH_STATUS-', size=(15, 1))]
]

# Create the GUI window
window = sg.Window('Tooltip Control', layout, grab_anywhere=True)

# Toggle the visibility of tooltips
for tooltip_windows in tooltip_windows_list:
    for tooltip_window in tooltip_windows:
        if tooltip_window.TKroot.winfo_viewable():
            tooltip_window.hide()
        else:
            tooltip_window.un_hide()

click_through_enabled = True  # Click-through is enabled by default
tooltips_enabled = False

def update_tooltip_positions():
    for i, tooltip_data in enumerate(tooltip_data_list):
        updated_tooltip_data = {}
        for j, tooltip_window in enumerate(tooltip_windows_list[i]):
            tooltip_position = list(tooltip_data.keys())[j]
            tooltip_x, tooltip_y = tooltip_window.current_location()
            updated_tooltip_data[f"{tooltip_x},{tooltip_y}"] = tooltip_data[tooltip_position]
        tooltip_data.clear()
        tooltip_data.update(updated_tooltip_data)

while running:
    event, values = window.read(timeout=100)

    if event == '-TOGGLE-':
        # Toggle the visibility of tooltips
        tooltips_enabled = not tooltips_enabled
        tooltip_status = 'On' if tooltips_enabled else 'Off'
        window['-TOOLTIP_STATUS-'].update(f'Tooltips: {tooltip_status}')
        for tooltip_windows in tooltip_windows_list:
            for tooltip_window in tooltip_windows:
                if tooltips_enabled and not tooltip_window.TKroot.winfo_viewable():
                    tooltip_window.un_hide()
                else:
                    tooltip_window.hide()

    if event == '-CLICK_THROUGH-':
        # Toggle click-through
        click_through_enabled = not click_through_enabled
        click_through_status = 'Enabled' if click_through_enabled else 'Disabled'
        window['-CLICK_THROUGH_STATUS-'].update(f'Click-Through: {click_through_status}')
        extended_style = (
            win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
            if click_through_enabled
            else win32con.WS_EX_LAYERED
        )
        for tooltip_windows in tooltip_windows_list:
            for tooltip_window in tooltip_windows:
                hwnd = win32gui.GetParent(tooltip_window.TKroot.winfo_id())
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, extended_style)

    if tooltips_enabled:
        # Capture the screen
        screenshot = pyautogui.screenshot()

        for i, tooltip_windows in enumerate(tooltip_windows_list):
            target_image = image_filenames[i]
            found = pyautogui.locate(target_image, screenshot, confidence=0.9)

            # Image found, display tooltips
            if found:
                for tooltip_window in tooltip_windows:
                    tooltip_window.un_hide()
                    tooltip_window.read(timeout=0)  # Update the window and process events
            else:
                # Hide tooltips
                for tooltip_window in tooltip_windows:
                    tooltip_window.hide()

    if event == '-TOOLTIP-DRAG-':
        if dragged_tooltip_window is not None:
            tooltip_x, tooltip_y = map(int, values[event].split(','))
            dragged_tooltip_window.move(tooltip_x, tooltip_y)

    if event == sg.WINDOW_CLOSED:
        # Save tooltip positions to the JSON file
        update_tooltip_positions()
        with open('config.json', 'w') as f:
            json.dump(config_data, f, indent=4)
        running = False

window.close()
