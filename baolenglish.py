import time
import PySimpleGUI as sg
import pyautogui
import win32gui
import win32con

# Define the image filenames.  These need to be in the same order of tooltip_data_list.
image_filenames = [
    'Images/mainwindow.png',
    'Images/rightclick.png',
    'Images/configheader.png',
    'Images/pickit.png',
    'Images/basic.png',
    'Images/skills.png',
    'Images/area.png',
    'Images/autolvl.png',
    'Images/autolvlstats.png',
    'Images/team.png',
]
# Define the tooltip positions and messages for each target image
tooltip_data_list = [
    { #main window
        (444, 710): 'Email',
        (444, 740): 'Realm\nUS\nEU\nAS',
        (626, 709): 'PASS',
        (626, 735): 'CHAR',
        (781, 709): 'LICENSE',
        (781, 740): 'CLASS\nAMAZON\nSORC\nNECRO\nPALA\nBARB\nDRUID\nASSASSIN',
        (970, 750): 'CREATE CHAR',
        (1045, 750): 'LADDER',
        (1098, 750): 'HC',
        (1160, 750): 'CLASSIC',
        (1048, 710): 'BNET PATH',
        (1287, 738): 'ADD/EDIT/SAVE',
        (1400, 738): 'DELETE',
        (480, 325): 'START/STOP',
        (560, 325): 'LICENSE',
        (860, 325): 'EXPIRATION',
        (1060, 325): 'VERSION',
    },
    { #right click to do
        (400, 300): 'RIGHT CLICK SCREEN\nF11 START/RESUME BOT MUST BE IN GAME\nF12 STOP/PAUSE BOT MUST BE IN GAME\n\nDROP LOG IN CLEINT VIEW\nTOGGLE WINDOW\nBOT INFO\nEXPORT DROP LOG\n\nENABLE AUTO MULE\nDIABLE AUTO MULE\nIMPORT CONFIG\nIMPORT ITEM CONFIG\nCOPY CONFIG TO\nCOPY PICKIT TO\nSYNC ALL CONFIG\nSYNC ALL PICKIT\nEDIT LICENSE\nMODIFY REALM\n\nRESTORE BNET\nENDGAME\nQUIT',
    },
     { #config header
        (625, 257): 'SAVE',
        (926, 257): 'DEFAULT CONFIG',
        (1015, 257): 'IMPORT CONFIG',
        (1105, 257): 'EXPORT CONFIG',
        (615, 285): 'PICKIT',
        (680, 285): 'BASIC',
        (740, 285): 'SKILLS',
        (800, 285): 'AREA',
        (860, 285): 'AUTOLVL',
        (925, 285): 'CRAFTGAMBLE',
        (1005, 285): 'TEAM',
        (1060, 285): 'AUTOGEAR',
        (1135, 285): 'AUTOSKILL',
        (1200, 285): 'MERC'
    },
    { #pickit
        (620, 320): 'TESTPICKIT',
        (690, 320): 'TESTSTASH',
        (760, 320): 'TESTSELL',
    },
    { #basic
        (620, 300): 'POTION SETTINGS',
        (640, 325): 'LESS THAN',
        (640, 345): 'LESS THAN',
        (640, 370): 'LESS THAN',
        (640, 390): 'LESS THAN',
        (640, 410): 'LESS THAN',
        (640, 440): 'LESS THAN',
        (640, 460): 'MERC BELOW',
        (640, 480): 'MERC BELOW',
        (725, 325): '% HP USE HP POT',
        (725, 345): '% HP USE REJUV POT',
        (725, 370): '% HP CHICKEN',
        (725, 390): '% MP USE MP POT',
        (725, 410): '% MP USE REJUV POT',
        (725, 440): '%STAMINA USE POT',
        (765, 460): '% USE HP',
        (765, 480): '% USE REJUV',
        (640, 500): 'RESURECT MERC',
        (640, 520): 'EXIT MERCDEATH',
        (745, 520): 'RES MERCDEATH',
        (620, 550): 'VENDOR/BELT SETTINGS',
        (640, 575): 'HP POTS',
        (640, 595): 'MP POTS',
        (640, 615): 'KEYS',
        (640, 640): 'ID SCROLLS/TOME',
        (640, 660): 'TP SCROLLS/TOME',
        (640, 685): 'GOLD',
        (640, 705): 'BUY GEAR',
        (760, 575): 'REJUV POTS',
        (890, 575): 'ONLY JUVS',
        (760, 595): 'STAMINA POTS',
        (760, 615): 'ARROW STACKS',
        (760, 640): 'BOLT STACKS',
        (760, 660): 'USE CAIN TO ID',
        (890, 300): 'GENERAL SETTINGS',
        (865, 325): 'STUCK',
        (865, 345): 'WAIT',
        (865, 390): 'ON CRASH',
        (865, 415): 'INV',
        (850, 435): 'LEFT RIGHT BLOCKSLOTS',
        (870, 460): 'MIN AREA TIME',
        (870, 480): 'GROUND ITEMS',
        (870, 500): 'LEGACY GFX',
        (870, 520): 'CLASSIC',
        (1050, 300): 'GLOBAL LOOT SETTINGS',
        (1055, 320): 'WHITE BASES IF %ED+',
        (1080, 350): 'INCLUDE PALA SHIELDS',
        (1055, 370): 'ETH ARMOR DEFENSE ABOVE',
        (1055, 395): 'ALL UNIQUE',
        (1140, 395): 'ALL SETS',
        (1050, 420): 'SAFEGUARD SETTINGS',
        (1055, 445): 'DODGE IF',
        (1155, 445): '% HP BELOW',
        (1055, 465): 'DODGE IF',
        (1175, 465): '% MERC HP BELOW',
    },
    { #skills
        (620, 305): 'SKILL SETTINGS',
        (640, 325): 'LEFT SKILL(S)',
        (650, 350): 'ELITE ONLY',
        (650, 380): 'BOSS ONLY',
        (860, 330): 'RIGHT SKILL(S)',
        (885, 350): 'ELITE ONLY',
        (885, 380): 'BOSS ONLY', 
        (725, 405): 'NORM SKILL ONLY', 
        (650, 420): 'BARB SPECIFIC SETTINGS',
        (651, 438): 'USE FIND ITEM',
        (770, 438): 'SWITCH OFF-HAND',  
        (651, 458): 'SKIP NORM',
        (725, 458): 'SKIP ELITE',
        (800, 458): 'SKIP BOSS',
        (651, 482): 'ONLY POP MONSTERS LISTED BELOW',
        (630, 602): 'NAME', 
        (630, 622): 'SORC SPECIFIC SETTINGS',
        (655, 640): 'CHANGE SKILLS ON IMMUNE',
        (655, 665): 'STATIC FIELD DISTANCE',
        (655, 685): 'USE TELEKINESIS',
        (655, 710): 'ENCHANT MERC',
        (780, 710): 'OFF-HAND\nENCHANT',
        (875, 430): 'PREBUFF\nSKILLS\nGO HERE\nCHKBOX\nTO\nSWAP\nHANDS',
        (875, 555): 'CURSES',
        (875, 580): 'SUMMONS\nSKILLS\nGO\nHERE',
        (875, 700): 'AURAS\nSKILLS\nGO\nHERE',
        (1120, 330): 'TELE SPEED',
        (1120, 350): '1=SLOWEST 10=FASTEST DEFAULT 10',
        (1140, 370): 'OFF-HAND TELE SWAP',
        (1140, 390): 'DO NOT USE TELEPORT',
        (1140, 410): 'TELESTOMP MONSTERS\nSORC, NECRO, AMAZON, DRUID\nNORM            ELITE        BOSS',
        (1140, 480): 'RIGHT HAND MS',
        (1270, 480): 'SPEED',
        (1140, 505): '1 SEC0ND = 1000 MS',
        (1140, 525): 'HYBRID SKILLS? LEFT+RIGHT?',
        (1140, 545): 'RIGHT SKILL ON IMMUNE?',
        (1140, 565): 'RIGHT SKILL ON MAGIC\nIMMUNE HOLY BOLT?',
        (1140, 615): 'PALADIN USE VIGOR',
        (1140, 635): 'PALA BARB ASSASIN\nATTACK MELEE DISTANCE',
        (1140, 690): 'CORPSE EXP',
        (1220, 690): 'PSN NOVA',
        (1140, 710): 'SUMMON SKELETONS\nNECROMANCER ONLY',
        (1140, 765): 'DRUID USE WEREWOLF',
        (1140, 785): 'DRUID USE BEAR',
    },
    { #area menue
        (620, 305): 'AREA BOSS SETTINGS',
        (620, 325): 'DIFFICULTY',
        (620, 345): 'NORM/NM/HELL',
        (750, 305): 'RESET CLEAR ORDER',
        (850, 305): 'DEFAULT SETTINGS',
        (980, 325): 'RANDOM ZONES',
        (980, 345): 'TZ END OF RUN',
        (870, 345): 'ONLY TZ RUNS?',
        (1070, 310): 'MAX AREA TIME IN SECONDS',
        (1235, 325): 'SELL IN TOWN',
        (1070, 345): 'NO EXP IN',
        (1085, 370): '0 EXP',
        (1085, 390): '0 EXP',
        (1085, 410): 'NO MOVES',
        (1085, 430): 'REPAIR PERCENT',
        (1085, 450): 'TP RESTOCK',
        (1085, 470): 'TP LOW HP',
        (1085, 490): 'TP LOW MP',
        (1155, 470): '0 HP EXIT',
        (1155, 490): '0 MP EXIT',
        (1225, 470): 'DONT PICK HP',
        (1225, 490): 'DONT PICK MP', 
        (1085, 510): 'MORE THAN', 
        (1085, 530): 'LESS THAN', 
        (1085, 550): 'LESS THAN', 
        (1085, 575): 'PICKUP GOLD',
        (1200, 575): 'AND MORE',
        (1225, 510): 'GOLD, STASH IT', 
        (1225, 530): 'GOLD, PICK JUNK',
        (1225, 550): 'STOP BOT', 
        (1145, 600): 'UNID ITEM SETTINGS',
        (1165, 345): 'MINUTES CLOSE GAME',
        (1165, 365): 'MINUTES NEXT AREA',
        (1165, 385): 'MINUTES EXIT GAME',
        (1083, 625): 'SKIP DIABLO',
        (1083, 645): 'SKIP BAAL',
        (1083, 660): 'SKIP ICEFST',
        (1083, 680): 'SKIP COLD',
        (1083, 700): 'SKIP FIRE',
        (1083, 720): 'SKIP LITE',
        (1083, 740): 'SKIP PHYS',
        (1083, 760): 'SKIP PSN',
        (1083, 780): 'SKIP MAGIC',
        (1270, 780): 'FROZEN?',
        (1165, 625): 'STOMP SEIS',
        (1245, 625): 'NITH WALLHUG',
        (1165, 645): 'KITE NITH',
        (1165, 660): 'ONLY SHENK',
        (1245, 660): 'ONLY ELD',
        (1165, 680): 'NO DODGE',
        (1165, 700): 'MOVE BEFORE LOADED',
        (1165, 720): 'KILL BEFORE LOADED',
        (1165, 740): 'PIRORITIZE LOOT',
        (1165, 760): 'CHEST SWAP WEPS',
        (1165, 780): 'SKIP MAGIC',   
        (650, 395): 'ANDARIEL\nCOUNTESS\nPINDLE\nELD-SHENK\nCOW LVL\nCRYPT 1 & 2\nSUMMONER\nANCIENT TUNNELS\nDURIEL\nMEPHISTO\nNIHLATHAK\nBAAL\nBLOODMOOR\nCOLD PLAINS\nSTONY FIELD\nDARKWOODS\nTAHOME HIGHLANDS\nDEN OF EVIL\nCAVE LVL 1\nCAVE LVL 2\nUND PASSAGE 1\nUND PASSAGE 2\nHOLE LVL 1\nHOLE LVL 2',        
    },
    { #auto lvl
        (640, 310): 'ENABLE QUESTING',
        (640, 330): 'MAKE SPIRIT CS',
        (640, 350): 'MAKE SPIRIT MON',
        (775, 310): 'STOP',
        (775, 330): 'NORM',
        (860, 330): 'STATS>',
        (775, 350): 'GOLD IN SHARED',
        (895, 350): 'UNCLEAR MP? IDK',
        (1025, 310): 'FINISH NORM',
        (1175, 310): 'FINISH NM',
        (1025, 330): 'FINISH HELL',
        (530, 390): 'A1-ANDARIEL\nA1-DEN OF EVIL\n\n\nA1-CAIN\n\nA2-DUREL\nA2-RADEMENT\n\n\nA3-MEPHISTO\nA3-LAM ESEN\n\n\nA3-COLDEN BIRD\n\n\nA4-DIABLO\nA4-IZUAL\n\nA5-BAAL\nA5-SHENK\nA5-BARBQUEST\nANYAQUEST',
        (845, 375): 'NORM',
        (895, 375): 'NM',
        (925, 375): 'HELL',
        (990, 770): 'LVL',
        (1050, 770): 'AREA',
    },
    { #autolvl stats
        (810, 285): 'TOTAL STATS',
        (810, 310): 'STR',
        (900, 310): 'DEX',
        (980, 310): 'VIT',
        (1040, 310): 'ENE',
        (810, 340): 'TOTAL SKILLS',
    },
    { #team and automule
        (650, 300): 'TEAM FARMING SETTINGS',
        (650, 325): 'MAX PLAYERS',
        (650, 350): 'JOIN VIA FLIST',
        (800, 350): 'NON-LADDER',
        (650, 375): 'LEADER ACCT',
        (870, 375): 'LEADER ACCT\nFRIENDSLIST NAME?',
        (650, 400): 'EXIT WHEN LEADER EXITS',
        (650, 425): 'CHARACTER PLAY STYLE',
        (800, 450): 'MANUAL PLAY CHAR',
        (800, 470): 'FOLLOW BOT (FOLLOWS LEADER)',
        (650, 495): 'TEAM SETTINGS',
        (650, 520): 'FOLLOW',
        (795, 520): 'CNAME',
        (645, 545): 'MAKE TP FOR FOLLOWERS',
        (790, 545): 'PRIORITIZE SEALS',
        (890, 545): 'FOLLOWERS ATTACK',
        (645, 570): 'START FOLLOW CHAT CMD',
        (645, 595): 'STOP FOLLOW CHAT CMD',
        (670, 620): 'PRE-DEFINED HOTKEYS\n(DISABLES CUSTOM START/STOP FOLLOW MSGS)',
        (645, 655): 'TEAM FARMING OPTIONS',
        (650, 675): 'ENABLE TEAM FARM',
        (765, 675): 'ENABLE TEAM QUESTING',
        (650, 705): 'FOLLOW',
        (835, 705): 'CNAME',
        (670, 725): 'SOLO COWS',
        (765, 725): 'USE WP',
        (765, 750): 'FOLLOWER ENTER TP AND AFK\nBAAL?',
        (870, 725): 'FOLLOWER EXPLOR MAP',
        (670, 750): 'NO ATTACK',
        (1100, 300): 'AUTOMULE SETTINGS',
        (990, 345): 'ITEM # TRIGGER',
        (1110, 345): 'MULE MUST BE ENABLED IN PICKIT',
        (1005, 325): 'ENABLE AUTOMULE',
        (1005, 380): 'MULE CHARNAME',
        (1005, 400): 'MULE BNET ACCT',
        (1005, 420): 'MULE GAMENAME',
        (1005, 445): 'MULE GAMEPASS',
        (1020, 473): 'FARMER',
        (1130, 473): 'MULER',
        (1020, 495): 'TIME TRIGGER',
        (1020, 520): 'ITEM NAME TRIGGER',
    },    
]

# Create the tooltip windows for each target image
tooltip_windows_list = []
for tooltip_data in tooltip_data_list:
    tooltip_windows = []
    for _, tooltip_message in tooltip_data.items():
        tooltip_layout = [
            [sg.Text(tooltip_message, background_color='white', text_color='black', font=('Impact', 10),
                     key='-TOOLTIP-', pad=(0, 0))]
        ]
        tooltip_window = sg.Window('', tooltip_layout,
                                   location=(0, 0), no_titlebar=True, keep_on_top=True, grab_anywhere=False,
                                   finalize=True, element_padding=(0, 0), margins=(0, 0))
        hwnd = win32gui.GetParent(tooltip_window.TKroot.winfo_id())  # Get window handle
        old_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_style = old_style | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
        tooltip_windows.append(tooltip_window)
    tooltip_windows_list.append(tooltip_windows)

# Set the loop flag
running = True

# Hide the tooltips initially
for tooltip_windows in tooltip_windows_list:
    for window in tooltip_windows:
        window.hide()

while running:
    # Capture the screen
    screenshot = pyautogui.screenshot()

    for i, tooltip_data in enumerate(tooltip_data_list):
        target_image = image_filenames[i]
        found = pyautogui.locate(target_image, screenshot, confidence=0.9)

        # Image found, display tooltips
        if found:
            tooltip_windows = tooltip_windows_list[i]
            for j, (tooltip_position, _) in enumerate(tooltip_data.items()):
                tooltip_x, tooltip_y = tooltip_position
                tooltip_windows[j].move(tooltip_x, tooltip_y)
                tooltip_windows[j].un_hide()
                tooltip_windows[j].read(timeout=0)  # Update the window and process events
        else:
            # Hide tooltips
            tooltip_windows = tooltip_windows_list[i]
            for window in tooltip_windows:
                window.hide()

    # Add a delay before the next iteration
    time.sleep(1)

# Close the tooltip windows when finished
for tooltip_windows in tooltip_windows_list:
    for window in tooltip_windows:
        window.close()
