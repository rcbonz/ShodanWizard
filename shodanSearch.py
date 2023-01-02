#!/usr/bin/env python
# by rcbonz https://github.com/rcbonz/ShodanWizard/
import os
import shodan
import shodan.exception
from pathlib import Path
import json
from colorama import Back, Fore, Style
from datetime import datetime
import requests
import readline


"This script was made with many information available at https://shodan.readthedocs.io/en/latest/api.html"
"The following section was stracted from https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running/66558182#66558182 and adapted for better suit"
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager
        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self._thread = Thread(target=self._animate, daemon=True)
        self.steps0 = ["--|","--|","--|","-| ","-| ","-| ","|  ","|  ","|  ","|  ","|  ","|  ","|  ","|  ","-| ","--|"]
        self.steps = ["=      ","==-    ","==---  "," ==----","  ---==","    -==","      =","      |","      =","    -==","  ---==","----== ","==---  ","==-    ","=      ","|      "]
        self.steps1 = ["  |","  |","  |","  |","  |","  |"," |-","|--","|--","|--","|--"," |-"," |-"," |-","  |","  |"]
        self.steps2 = ["⢿","⣻","⣽","⣾","⣷","⣯","⣟","⡿","⢿","⣻","⣽","⣾","⣷","⣯","⣟","⡿"]
        self.steps3 = ["⣀","⣶","⣿","⣿","⣿","⣿","⣭","⣭","⣉","⣉","⣒","⣒","⣀","⣀","⣀","⣀"]
        self.steps4 = ["-","\\","|","/","-","\\","|","/","-","\\","|","/","-","\\","|","/"]
        self.done = False
        
    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c,d,e,f,g,h in cycle(zip(self.steps,self.steps1,self.steps0,self.steps2,self.steps3,self.steps4)):
            if self.done:
                break
            out(f"{self.desc} " + fyb(e) + fgb(f"{c}") + fyb(d) + f" | " + fcb(f) + " | " + fmb(g) + " | " + frb(h) + "  ", msg_type=1, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        out(f"{self.end}" + " " * cols,msg_type=1,end="")

    def __exit__(self, exc_type, exc_value, tb):

        self.stop()


"Bonz's script starts here."

description = """********************************************************
*                                                      *
*      shodanSearchTool 0.1b - The Shodan Helper       *
*                                                      *
*                 Coded by: B0nz                       *
*                                                      *
********************************************************
"""

SHODAN_API_FILE = 'shodan_api.txt'
HISTORY_LIMIT = '20'
HISTORY_FILE = "searchHistory.txt"

yes_list = ["y","yes","yeah","yup",""]
no_list = ["n","no","nope"]

"Coloring, time and print outputs"
def fr(msg):
	return Fore.RED + msg + Fore.RESET
def fg(msg):
	return Fore.GREEN + msg + Fore.RESET
def fy(msg):
	return Fore.YELLOW + msg + Fore.RESET
def fb(msg):
	return Fore.BLUE + msg + Fore.RESET
def fc(msg):
	return Fore.CYAN + msg + Fore.RESET
def fm(msg):
	return Fore.MAGENTA + msg + Fore.RESET
def frb(msg):
	return Fore.RED + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fgb(msg):
	return Fore.GREEN + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fyb(msg):
	return Fore.YELLOW + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fbb(msg):
	return Fore.BLUE + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fcb(msg):
	return Fore.CYAN + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def fmb(msg):
	return Fore.MAGENTA + Style.BRIGHT + msg + Fore.RESET + Style.RESET_ALL
def br(msg):
	return Back.RED + msg + Back.RESET
def bg(msg):
	return Back.GREEN + msg + Back.RESET
def by(msg):
	return Back.YELLOW + msg + Back.RESET
def bm(msg):
	return Back.YELLOW + Fore.BLACK + Style.NORMAL + " "+msg+" " + Back.RESET + Fore.RESET + Style.RESET_ALL

"Input function"
def inp(prefill=''):
    try:
        print(Fore.CYAN + Style.BRIGHT, end="")
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        inpi = input(" ")
        print(Fore.RESET + Style.RESET_ALL, end="")
        return inpi
    except KeyboardInterrupt:
        print(Fore.RESET + Style.RESET_ALL)
        out("Exiting...", msg_type=-1)
        exit()
    except Exception as err:
        print(Fore.RESET + Style.RESET_ALL)
        print("Input function: "+str(err))
    finally:
        readline.set_startup_hook()


"Helping keep the terminal looking good with time stamp"
def nowF(style="Time"):
    if style == "Time":
        return str(datetime.now().strftime("%H:%M:%S"))
    elif style == "Date":
        return str(datetime.now().strftime("%d/%m/%Y"))
    elif style == "DateTime":
        return str(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
    elif style == "FolderName":
        return str(datetime.now().strftime("%Y.%m.%d-%H.%M"))


"Instead of just printing, function for adding some colors, time info etc"
def out(msg, counter=" ", msg_type=0, end=False):
    if end == False:
        if msg_type == 1: # Positive message
            return print(f'\r[{counter}]' + fg("! ") + fy(str(nowF())) + (' - ') + str(msg))
        elif msg_type == 0: # Neutral message
            return print(f'\r[{counter}]  ' + fy(str(nowF())) + (' - ') + str(msg))
        elif msg_type == -1: # Negative message
            return print(f'\r[{counter}]' + fr("! ") + fy(str(nowF())) + (' - ') + str(msg))
        elif msg_type == 2: # Question message
            return print(f'\r[{counter}]' + fb("? ") + fy(str(nowF())) + (' - ') + str(msg))
    else:    
        if msg_type == 1: # Positive message
            return print(f'\r[{counter}]' + fg("! ") + fy(str(nowF())) + (' - ') + str(msg), end=end)
        elif msg_type == 0: # Neutral message
            return print(f'[{counter}]  ' + fy(str(nowF())) + (' - ') + str(msg), end=end)
        elif msg_type == -1: # Negative message
            return print(f'[{counter}]' + fr("! ") + fy(str(nowF())) + (' - ') + str(msg), end=end)
        elif msg_type == 2: # Question message
            return print(f'\r[{counter}]' + fb("? ") + fy(str(nowF())) + (' - ') + str(msg), end=end)


BADMOFO = """
............. ............*#@&@@&%(&@%((%%((&#/#%%,,,.//(,,,*(**........................................................
........................,@@@@@@@@@@%@@@@%&@@*&&&#*&(%##,(//(,(.,........................................................
.......................%%@@@@@@@&@@@&&&&&@&#&%#%(#(*(%((%#/(%,(*.*......................................................
......................*#@@@@@@@@@@@@@@@@@&&&@@&@*&&&#(%%#(&*#(/#,,.,....................................................
......................@@@@@@@@@@@@@@@@@&@@@@@&&#&&@/##/%#%%#*%//.*(**...................................................
.....................&@@@@@@@@@@@@@@@@@@&@@@@%@@&@@#&((/%((&(/((&,(*/...................................................
....................*%@@@@@@@@@@@@@@@@@@@@@@&@&@%@%@&/(/**(&/(%%*.(#*,..................................................
 ...................*&@@@@@@@@@@@@@@@@@&@@@@@@@@@&&##/%%%(%&@.#%*&/(*/..................................................
....................*@@@@@@@@@@@&&&@@@@&&&&&&&&&%&&&&%(,%#*##&*%##%#**..................................................
....................*%&@@@@@@@@&%%%%%&&&&&%%%&%&%%%%#/(*,.((&&#((//*(...................................................
....................,##@@@@@@&&&&&&&%&@@@&&&%%&@@&&&&&&&#//#@@@/##*(,...................................................
......................*&@@@@&&&&&&&%%&&@@&&&&&&&&@@&@&@@##&#&@%(#%**....................................................
.......................*@@@@&%%%%%&&&&&&&&&&&%,,(#(%&&&%/,,*%&&%/*......................................................
......................./&&@@&%%%%%%&&&&&&%%%%%%,  (&/.  .../((#%*.......................................................
......................../#@&@%%%%%%%%&&&%%&@@@@@@&%%&%*,.,*//*#.........................................................
.........................(&%&%%%%%%%&&&&@@@@@%(. .  /&%/**/##*..........................................................
............................%@&%%%%%@@@@%&&&&&&#*.*.  //**#(............................................................
............................&@@@@&&&@&&&&&&&&&*,*,(%(***//%.............................................................
.............................&@&&&%&&&&&%%%@@@&&&&&#(/#*%*/.............................................................
.............................#%%%%&@@&&&&&&&&&&&&@&%#%&,,((/,...........................................................
.............................,%%%%&@@&%%%&%&&&&#/#%(,   #(/((/,.........................................................
.............................,%&&&&&@@@&&&&&&&&@&%,.  %%###%%#%#((,.....................................................
..............................#&&&&&&&&&&&&&(*,.  ..&&%#%%&@@#&##%%##((########((((/....................................
............................@/,*/&@@@****,,,,,..,*%@&%%&&@@@&&##%&%&&&&&%%%%%%#####((((*................................
..........................@@@,..@@@@@,,,,,,,,,,*/@@&&&@@@@#@&&@&&@@@@@@@@&%#(%@%%%&%%###(*..............................
......................(@@@@@&**,@@@@%/*,,,****/@@&@@@@@@@@%@@@@@@@@@@@@@&&&&%%(###%@@@@&#((.............................
.................*@@@@@@@@@&/,,.@@/**(//*****%@@@@@@@@@@@@@@@@@@@@@@@@@&%&&&%#%@@@&&#(#&&%#(............................
.............,@@@@@@@@@@@@****,@@@(*##(//**/@@@@@@@@@@@@@@@@@@@@@&@@@@&&&%%&%%###((&@@@%#%##*...........................
..........%@@@@@@@@@@@@@@%*,,,@@@&%&%&#(***@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@&&###(##@@@&##(...........................
........&@@@@@@@@@@@@@@@#**//@@@@@@@&%#(//@@@@@@@@@@@@@@@@@@@@@@@@%%@@@@@@@@@@@@@%&@@%(@@@@%(...........................
.......&@@@@@@@@@@@@@@@@#/*,*@@@@@@@&%#*/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&%#@@@@@%%##@@&#...........................
.......@@@@@@@@@@@@@@@%*,,,,@@@@@@@@&/*/&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&%%&%%%%##@@@@%%#&/...........................
......#@@@@@@@@@@@@@@&/****@@@@@@@@%///(@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&%%%%%#%@@@#%&&&%#/......................
......@@@@@@@@@@@@@@@%/*//%@@@@@@@#((/(@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&&&%%%%%/*,,/#&&&%/*/*................
.....(@@@@@@@@@@@@@@@(/**/@@@@@@@&##*(/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&@@&&&&%%%%%(///*****/(%&&#(##(*............
.....@@@@@@@@@@@@@@@#***,@@@@@@@@%%*(*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&@&&&&((&%%/,**/***/(#&&&%%#((,.......
.....@@@@@@@@@@@@@@%**,,&@@@@@@@@%*/*,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@&&&&&&&&&@@@/,*/#%(((/****//(#&&&%%#(/*,..
..../@@@@@@@@@@@@@@,,,,.@@@@@@@@%/*/,%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&@@@&#((/(%##((((###(////(####.  /,
....@@@@@@@@@@@@@@%***,@@@@@@@@&#,/,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&%%%&&&@@&%##(#(.,#&&&&&%#(///*//(%@&#(.
....@@@@@@@@@@@@@@(*,,/@@@@@@@@%,*/,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%##%%&&&&&%%&&&&&&&#**//////////((###*.
...*@@@@@@@@@@@@@@*,*,@@@@@@@@&*,**,/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#(&##%&@@&(((##%&&&#*,#/,...  .//(((/..
...%@@@@@@@@@@@@@%/***@@@@@@@@#,**.*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/&@%(#%%%%%%%&&&&&&%(/,.   .,,.*.......
...@@@@@@@@@@@@@@%,**@@@@@@@@@,,**,.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/%@#%%%#####%%%%%%(,,******(##(........
...@@@@@@@@@@@@@@**,*@@@@@@@@#,,**,,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/%#(%%&%%%#%%%%%%%%%#(((/*,...........
                        ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
                        :::::::::::::::'########:::::'###::::'########::::::::::::::::::
                        ::::::::::::::: ##.... ##:::'## ##::: ##.... ##:::::::::::::::::
                        ::::::::::::::: ##:::: ##::'##:. ##:: ##:::: ##:::::::::::::::::
                        ::::::::::::::: ########::'##:::. ##: ##:::: ##:::::::::::::::::
                        ::::::::::::::: ##.... ##: #########: ##:::: ##:::::::::::::::::
                        ::::::::::::::: ##:::: ##: ##.... ##: ##:::: ##:::::::::::::::::
                        ::::::::::::::: ########:: ##:::: ##: ########::::::::::::::::::
                        :::::::::::::::........:::..:::::..::........:::::::::::::::::::
                        '##::::'##::'#######::'########:'##::::'##:'########:'########::
                        :###::'###:'##.... ##:... ##..:: ##:::: ##: ##.....:: ##.... ##:
                        :####'####: ##:::: ##:::: ##:::: ##:::: ##: ##::::::: ##:::: ##:
                        :## ### ##: ##:::: ##:::: ##:::: #########: ######::: ########::
                        :##. #: ##: ##:::: ##:::: ##:::: ##.... ##: ##...:::: ##.. ##:::
                        :##:.:: ##: ##:::: ##:::: ##:::: ##:::: ##: ##::::::: ##::. ##::
                        :##:::: ##:. #######::::: ##:::: ##:::: ##: ########: ##:::. ##:
                        ..:::::..:::.......::::::..:::::..:::::..::........::..:::::..::
                        ':########:'##::::'##::'######::'##:::'##:'########:'########:::
                        ::##.....:: ##:::: ##:'##... ##: ##::'##:: ##.....:: ##.... ##::
                        ::##::::::: ##:::: ##: ##:::..:: ##:'##::: ##::::::: ##:::: ##::
                        ::######::: ##:::: ##: ##::::::: #####:::: ######::: ########:::
                        ::##...:::: ##:::: ##: ##::::::: ##. ##::: ##...:::: ##.. ##::::
                        ::##::::::: ##:::: ##: ##::: ##: ##:. ##:: ##::::::: ##::. ##:::
                        ::##:::::::. #######::. ######:: ##::. ##: ########: ##:::. ##::
                        :..:::::::::.......::::......:::..::::..::........::..:::::..:::
                        ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
"""


"English, do you speak it?"
def english_mofo():
    try:
        while True:
            out("What country you're from?",msg_type=2, end="")
            country = inp()
            out(f"{country.title()} ain't no country I've ever heard of. They speak english in {country.title()}???",msg_type=2, end="")
            speak = inp()
            if speak.lower() in yes_list:
                print("|"+44*"-")
                out("I'll give you one more chance, lets continue.",msg_type=1)
                return True
            else:
                out("English, motherfucker, do you speak it? [y/n]:",msg_type=2, end="")
                en = inp()
                if en.lower() in yes_list:
                    print("|"+44*"-")
                    out("Goddammit, I'll forgive you this time. Lets continue.",msg_type=1)
                    return True
                else:
                    out(f"Say {en} again! SAY {en.upper()} AGAIN!!! I DARE YOU! I DOUBLE DARE YOU MOTHERFUCKER! SAY {en.upper()} ONE MORE GODDAMN TIME:",msg_type=2, end="")
                    last = inp()
                    if last != en:
                        print("|"+44*"-")
                        out("I knew you didn't have balls. Lets continue.",msg_type=1)
                        return True
                    else:
                        out("Do I look like a bitch? [y/n]:",msg_type=2, end="")
                        en = inp()
                        print(fmb(BADMOFO))
                        print("\n\n\n")
                        print(fmb("Wrong answer motherfucker. This file was deleted, download it again and start over motherfucker."))
                        print("\n\n\n\n\n\n\n\n\n\n\n\n")
                        file_to_rem = Path(__file__)
                        file_to_rem.unlink()
                        exit()
    except KeyboardInterrupt:
        print("")
        out("Exiting...", msg_type=-1)
        exit()
    except Exception as err:
        print("english_mofo: "+str(err))


"Get Shodan API Key status"
def shodan_status(api):
    print("|"+44*"-")
    try:
        out(bm("Shodan API Status") + ' - Shodan account usage.')
        loader = Loader("Getting API information...", "Done.", 0.05).start()
        account_info = api.info()
        loader.stop()
        account_info_msg = f"Here's your " + fy("API INFO") + ":\n\n\t- " + fy("Plan") + ": " + fg(account_info.get("plan")) + "\n\t" + (8+len(account_info.get("plan")))*"-" + "\n\t- " + fy("Query Credits") + ": " + fg(str('{:,}'.format(account_info.get("query_credits")))) + " available from " + fg(str('{:,}'.format(account_info.get("usage_limits").get("query_credits")))) + " plan credits\n\t- " + fy("Monitored IPs") + ": " + fg(str('{:,}'.format(account_info.get("monitored_ips")))) + " available from " + fg(str('{:,}'.format(account_info.get("usage_limits").get("monitored_ips")))) + " plan credits\n\t- " + fy("Scan Credits") + ": " + fg(str('{:,}'.format(account_info.get("scan_credits")))) + " available from " + fg(str('{:,}'.format(account_info.get("usage_limits").get("scan_credits")))) + " plan credits\n"
        out(account_info_msg)
    except KeyboardInterrupt:
        print("")
        out("Exiting...", msg_type=-1)
        exit()
    except Exception as err:
        print("shodan_status: "+str(err))
        print("Exiting")
        exit()


"Handle API Key"
def shodan_api_exists():
    "Check if Shodan API Key exists."
    api_shodan_key_file = Path(SHODAN_API_FILE)
    if api_shodan_key_file.is_file() == False:
        out(f"No Shodan API Key found on {SHODAN_API_FILE}, please type a valid API Key now or " + fyb('e') + " to exit:", msg_type=2, end=" \nType here: ")
        api_shodan_key_to_file = inp()
        if api_shodan_key_to_file == "e":
            out("Exiting...", msg_type=-1)
            exit()
        out('Do you want to store this API Key [Y/n]:', msg_type=2, end="")
        store_shodan_api_key = inp()
        if store_shodan_api_key.lower() in yes_list:
            with open(api_shodan_key_file, "w") as api:
                api.write(api_shodan_key_to_file)
            out("API Key stored.", msg_type=1)
        elif store_shodan_api_key.lower() in no_list:
            out("The API Key won't be stored.", msg_type=1)
        else:
            english_mofo()
            out("Invalid answer anyways. API Key won't be stored.", msg_type=-1)
        return shodan.Shodan(api_shodan_key_to_file)
    else:
        api_shodan_key = open(api_shodan_key_file, "r").read().rstrip()
        return shodan.Shodan(api_shodan_key)


"Chosing Shodan facets search"
def chose_shodan_facets():
    facets_dic = {'1': 'city', '2': 'country', '3': 'device', '4': 'domain', '5': 'has_screenshot', '6': 'hash', '7': 'http.favicon.hash', '8': 'http.title', '9': 'http.waf', '10': 'ip', '11': 'isp', '12': 'link', '13': 'mongodb.database.name', '14': 'org', '15': 'os', '16': 'port', '17': 'product', '18': 'region', '19': 'state', '20': 'tag', '21': 'version', '22': 'vuln', '23': 'vuln.verified'}
    while True:
        try:
            out("Those are the facets options.",msg_type=2)
            for i, item in facets_dic.items():
                print(f"\t[" + fgb(str(i)) + "] - " + fy(f"{item}"))
            print('\t[' +
                fyb('b') + '] - To go ' + fy("back") + '\n\t[' + 
                fyb('e') + '] - To go ' + fy('EXIT') + '')
            out("Choose one or more facets to improve your query filtering or one of the above options:",msg_type=2,end="")
            facet_choice = inp()
            if facet_choice == "b":
                return ""
            elif facet_choice == "e":
                out("Exiting.", msg_type=-1)
                exit()
            out("How many facets contents do you want display per chosen facet? (1-100, default: 10)",msg_type=2,end="")
            facet_qtt = inp()
            if facet_qtt == "":
                facet_qtt = 10
            x = int(facet_qtt)
            faces_list = []
            for faceidx in facet_choice.replace(" ","").split(","):
                faces_list.append((facets_dic[faceidx],x))
            return faces_list
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()
        except Exception as err:
            out(fmb("Error: ")+str(err),msg_type=-1)
            continue



"Handling Shodan facets search"
def shodan_facets_choo(api, query):
    "The code of this function was stracted and adapted from https://shodan.readthedocs.io/en/latest/examples/query-summary.html"
    while True:
        try:
            faces_list = chose_shodan_facets()
            loader = Loader("Getting query facets...", "Done.", 0.05).start()
            result = api.count(query, facets=faces_list)
            loader.stop()
            out('', msg_type=1)
            print(fy(f"\tShodan Summary Information -----"))
            print(f'\tQuery: ' + fg(query))
            print('\tTotal Results: ' + fg(str('{:,}'.format(result['total']))) + "\n")
            a = 1
            facets_opt = {}
            for facet in result['facets']:
                print("\t" + fy(facet + " ---"))
                for term in result['facets'][facet]:
                    print(f"\t[" + fgb(str(a)) + "] - " + fy(f"{term['value']}") + ": " + fg(str('{:,}'.format(term['count']))) + " devices")
                    facets_opt[a] = facet + "," + str(term['value'])
                    a+=1
                print('')
            out("Chose one or more " + fy("filter(s)") + ", [" + fyb("S") + "] to skip (default), [" + fyb("b") + "] to go back or [" + fyb("e") + "] to exit:", msg_type=2, end="")
            facet_filter = inp()
            if facet_filter in ["s","","S"]:
                out("Skipping.")
                return query
            elif facet_filter == "e":
                out("Exiting.", msg_type=-1)
                exit()
            elif facet_filter == "b":
                return query
            facet_query = ""
            facet_filter_list = facet_filter.split(',')
            facet_chosen_dict = {}
            chosen_facet_list = []
            for facet_idx in facet_filter_list:
                facet_chosen_dict[facets_opt[int(facet_idx)].split(",")[1]] = facets_opt[int(facet_idx)].split(",")[0]
                chosen_facet_list.append(facets_opt[int(facet_idx)].split(",")[0])
            chosen_facet_list = list(set(chosen_facet_list))
            for chosen_facet in chosen_facet_list:
                facet_query = facet_query + f"{chosen_facet}:"
                facet_values = [k for k,v in facet_chosen_dict.items() if v == chosen_facet]
                for facet_value in facet_values:
                    facet_query = facet_query + f'"{facet_value}",'
                facet_query = facet_query[:-1] + " "
            facet_query = facet_query[:-1]
            out('To your query will be added: "' + fy(facet_query) + '"')
            query = query + " " + facet_query
            out('Your query now is: "' + fy(query) + '"')
            return query
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()
        except Exception as err:
            out(fmb("Error: ")+str(err),msg_type=-1)
            continue


"Why not to be able to choose Shodan facets filters as one wants?"
def shodan_facets(api, query):
    print("|"+44*"-")
    out("Do you want to see the " + bm("FACETS") + " before continuing [y/N]?", msg_type=2, end="")
    see_facets = inp()
    if see_facets.lower() in ["n","no",""]:
        return query
    while True:
        print("|"+44*"-")
        try:
            query = shodan_facets_choo(api, query)
            print("|"+44*"-")
            out("Do you want to see even more " + bm("FACETS") + " for your query " + fy(f"'{query}'") + " before continuing [y/N]?", msg_type=2, end="")
            see_more_facets = inp()
            if see_more_facets.lower() in ["y","yes"]:
                continue
            elif see_more_facets.lower() in ["","n","no"]:
                return query
            else:
                if english_mofo():
                    continue
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()
        except Exception as err:
            out(fmb("Error: ")+str(err),msg_type=-1)
            continue


"Shodan queries shared by community helper"
def shodan_shared_queries(api, sort='timestamp', page=1):
    shared_dic = {}
    if sort not in ["timestamp","votes"]:
        result = api.queries_search(sort, page=[1,2,3])
    else:
        result = api.queries(page=page, sort=sort, order='desc')
    if len(result["matches"]) < 1:
        out("No results found.", msg_type=-1)
        return ""
    a = 1
    for queries in result["matches"]:
        print("\t|----------------")
        print(fy("\t    Time") + ": " + fg(str(queries["timestamp"][:10])) + fy("\n\t    Votes") + ": " + fg(f"{queries['votes']}") + "\n\t" + fy("    Descr.") + ":" + fg(f" {queries['description']}"))
        print(fy("\t    Title") + ": " + fg(queries["title"]))
        print("\t[" + fyb(str(a)) + "] " + fy("Query") + ": " + fyb(f"{queries['query']}"))
        shared_dic[a] = queries['query']
        a += 1
    print("\t|----------------")
    print("\t[" + fyb("b") + "] to go " + fy("back") + " to previous list" + "\n\t[" + fyb("e") + "] to " + fy("EXIT"))
    return shared_dic


"Shodan queries shared by community"
def shared_queries(api):
    print("|"+44*"-")
    while True:
        try:
            out(bm("Shared queries") + " - Do you want to:", msg_type=2)
            print("\t[" + fgb("1") + "] list shared " + fy("queries") + " sorted by votes desc." + 
            "\n\t[" + fgb("2") + "] list shared " + fy("queries") + " sorted by date desc." + 
            "\n\t[" + fgb("3") + "] search in shared " + fy("queries") + " with a keyword" + 
            "\n\t[" + fyb("b") + "] to go " + fy("back") + " to previous list" +
            "\n\t[" + fyb("e") + "] to " + fy("EXIT"))
            out("Please choose one option:", msg_type=2, end="")
            shared_opt = inp()
            if shared_opt == "1":
                out("What page number of results do you want?", msg_type=2, end="")
                shared_opt_1 = inp()
                if int(shared_opt_1) in range(1,100):
                    shared_dic = shodan_shared_queries(api, sort='votes', page=int(shared_opt_1))
                else:
                    out("Invalid page number. Try again", msg_type=-1)
            elif shared_opt == "2":
                out("What page number of results do you want?", msg_type=2, end="")
                shared_opt_2 = inp()
                if int(shared_opt_2) in range(1,100):
                    shared_dic = shodan_shared_queries(api, sort='timestamp', page=int(shared_opt_2))
                else:
                    out("Invalid page number. Try again", msg_type=-1)
            elif shared_opt == "3":
                out("What keyword do you want to search in shared queries?", msg_type=2, end="")
                shared_que_keyw = inp()
                out("What page number of results do you want?", msg_type=2, end="")
                shared_opt_3 = inp()
                if int(shared_opt_3) in range(1,100):
                    shared_dic = shodan_shared_queries(api, sort=shared_que_keyw, page=int(shared_opt_3))
            elif shared_opt == "b":
                return ""
            elif shared_opt == "e":
                out("Exiting.",msg_type=-1)
                exit()
            if type(shared_dic) == str:
                continue
            out("Chose one of the " + fy("queries") + " or " + fy("options") + " above:", msg_type=2, end="")
            optionsha = inp()
            if optionsha == "b":
                print(optionsha)
                return ""
            elif optionsha == "e":
                out("Exiting.",msg_type=-1)
                exit()
            else:
                
                query = shared_dic[int(optionsha)]
                print(query)
                return query
        except Exception as err:
            out(fmb("Invalid option, try again."),msg_type=-1)
            continue
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()


"Shodan Wizard step 1"
def wizard_step1():
    print("|"+44*"-")
    while True:
        try:
            out(bm("Step 1") + ' - Shodan search options:\n\t[' + 
                fgb('1') + '] - for query ' + fy('EXAMPLES') + '\n\t[' + 
                fgb('2') + '] - for query ' + fy('BUILDER') + '\n\t[' + 
                fgb('3') + '] - for ' + fy('API INFO') + '\n\t[' + 
                fgb('4') + '] - to check information of a specific ' + fy('HOST') + '\n\t[' + 
                fgb('5') + '] - use one query from ' + fy('HISTORY') + '\n\t[' +
                fgb('6') + '] - type a ' + fy('CUSTOM') + ' query\n\t[' +
                fgb('7') + '] - to check queries ' + fy('SHARED') + ' by users\n\t[' +
                fgb('8') + '] - to find and build a query based on ' + fy('VULNERABILITIES') + ' \n\t[' +
                fyb('e') + '] - to ' + fy('EXIT') + '', msg_type=1)
            out('Enter one ' + fgb('option') + ' from above:', msg_type=2, end="")
            query = str(inp())
            if query in ["1","2","3","4","5","6","7","8","e"]:
                return query
            else:
                print("|"+44*"-")
                out(fmb("Invalid option, try again."),msg_type=-1)
                continue
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()


query_examples_dic = {"1":['"Server: CarelDataServer" "200 Document follows"','Refrigeration Units'],
                    "2":['"Siemens, SIMATIC" port:161','Siemens Industrial Automation'],
                    "3":['"Android Debug Bridge" "Device" port:5555','Android Root Bridges'],
                    "4":["country:KP","All 36 devices in North Korea"],
                    "5":["port:37777 country:UA","Dahua DVRs in Ukraine"]}


"Shodan Wizard query examples"
def query_examples():
    print("|"+44*"-")
    while True:
        try:
            out(bm("Examples") + ' - Check https://github.com/jakejarvis/awesome-shodan-queries for AWESOME Shodan queries!\n\tSome query ' + fy('EXAMPLES') + ' are:')
            options_dic = []
            for key, value in query_examples_dic.items():
                options_dic.append(key)
                q = value[0]
                d = value[1]
                print('\n\t[' + fgb(key) + "] - " + fy(f'{q}') + f" -> {d}")
            print('\n\t[' +
                fyb('b') + '] - go ' + fy("back") + '\n\t[' + 
                fyb('e') + '] - to ' + fy('EXIT') + '')
            out('Enter one ' + fgb('option') + ' from above:', msg_type=2, end="")
            example_option = str(inp())
            if example_option in query_examples_dic.keys():
                query = query_examples_dic[example_option][0]
                return query
            elif example_option == "b":
                return False
            elif example_option == "e":
                print("|"+44*"-")
                out("Exiting.",msg_type=-1)
                exit()
            else:
                print("\n|"+44*"-")
                out(fm("Invalid option '") + fyb(example_option) + fm("' , try again."),msg_type=-1)
                continue
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()


"Just type a custom query"
def custom_query():
    try:
        print("|"+44*"-")
        out(bm("Custom query") + " - Type your custom query, " + fyb("b") + " to go " + fyb("back") + " or " + fyb("e") + " to exit.", msg_type=2, end="")
        query = inp()
        if query == "b":
            return ""
        elif query == "e":
            out("Exiting.",msg_type=-1)
            exit()
        else:
            return query
    except KeyboardInterrupt:
        print("")
        out("Exiting...", msg_type=-1)
        exit()
    except Exception as err:
        out(fmb(str(err)),msg_type=-1)


"Shodan Wizard Start"
def shodan_wizard(api, step=""):
    step1 = ""
    while True:
        try:
            if step1 == "":
                step1 = wizard_step1()
                q1 = step1
            if q1 == "e":
                print("|"+44*"-")
                out("Exiting.",msg_type=-1)
                exit()
            elif q1 == "1" or step == "examples":
                query = query_examples()
                if query == False:
                    step1 = ""
                    continue
                else:
                    return query, "examples"
            elif q1 == "2" or step == "query_builder":
                query = query_builder()
                if query == "":
                    step1 = ""
                    continue
                else:
                    return query, "query_builder"
            elif q1 == "3":
                shodan_status(api)
                step1 = ""
                continue
            elif q1 == "4":
                shodan_host(api)
                step1 = ""
                continue
            elif q1 == "5" or step == "history_search":
                query = history_search()
                if query == "":
                    step1 = ""
                    continue
                else:
                    return query, "history_search"
            elif q1 == "6" or step == "custom":
                query = custom_query()
                if query == "":
                    step1 = ""
                    continue
                return query, "custom"
            elif q1 == "7" or step == "shared_queries":
                query = shared_queries(api)
                if query == "":
                    step1 = ""
                    continue
                else:
                    return query, "shared_queries"
            elif q1 == "8" or step == "search_vuln":
                print("|"+44*"-")
                query = search_vuln()
                return query, "custom"
            elif q1 in ["2","4","5","6","8"]:
                break
            else:
                print("|"+44*"-")
                out(fm("Invalid option '") + fyb(q1) + fm("' , try again."),msg_type=-1)
            # return query
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()
        except Exception as err:
            out(fmb(str(err)),msg_type=-1)
            continue


"Use history search as query"
def history_search():
    print("|"+44*"-")
    while True:
        try:
            history_file_path = Path(HISTORY_FILE)
            if not history_file_path.is_file():
                out(bm("Histrory") + " - There are no history records. Try another option.", msg_type=-1)
                return ""
            out(bm("History") + " - Choose one of your recent queries:", msg_type=1)
            with history_file_path.open("r", encoding="utf-8") as f:
                content_lines = f.read().splitlines()
            if len(content_lines) < int(HISTORY_LIMIT):
                hist_lim = len(content_lines)
            else:
                hist_lim = HISTORY_LIMIT
            for line in range(1,hist_lim+1,1):
                print("\t[" + fgb(str(line)) + f'] - {content_lines[line-1].split("|")[0]} - ' + fy(f"'{content_lines[line-1].split('|')[1]}'"))
            print("\t[" + fyb("b") + f'] - To go ' + fy("back") + "\n\t[" + fyb("e") + f'] - To ' + fy("exit"))
            out("Type the number corresponding to the query:", msg_type=2, end="")
            query_line = inp()
            if query_line == "e":
                out("Exiting...", msg_type=-1)
                exit()
            if query_line == "b":
                return ""
            query = content_lines[int(query_line)-1].split("|")[1]
            content_lines.remove(content_lines[int(query_line)-1])
            with history_file_path.open("w+", encoding="utf-8") as s:
                for idx in range(0,len(content_lines),1):
                    s.write(content_lines[idx] + "\n")
            line = f'{str(datetime.now().strftime("%d/%m/%Y at %H:%M:%S"))}|{query}'
            with history_file_path.open("a", encoding="utf-8") as a:
                a.write(line + "\n")
            return query
        except Exception as err:
            out(fmb(str(err)),msg_type=-1)
            continue
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()


"Query builder"
def query_builder():
    print("|"+44*"-")
    while True:
        try:
            shodan_query = ""
            out(bm("Query Builder") + " - This builder will help you to build a query. Each question adds a filter. " + fyb("Leave blank") + " if you don't want any of the filters. At anytime type " + fyb("b") + " to go " + fyb("back") + " or " + fyb("e") + " to exit.")
            out("Enter a " + fgb("country") + " (two letter format, i.e.: 'US'):", msg_type=2, end="")
            country = str(inp()).upper()
            if len(country) == 2:
                shodan_query = shodan_query + 'country:"'+country+'"'
            elif country == "E":
                out("Exiting...", msg_type=-1)
                exit()
            elif country == "B":
                return ""
            out("Enter a " + fgb("city") + " name:", msg_type=2, end="")
            city = str(inp())
            if len(city) >= 2:
                shodan_query = shodan_query + ' city:"'+city+'"'
            elif city == "e":
                out("Exiting...", msg_type=-1)
                exit()
            elif city == "b":
                return ""
            out("Enter one " + fgb("port") + " or more, using comma to separate them (i.e.: '80,443,8080' or '554'):", msg_type=2, end="")
            port = str(inp())
            if len(port) >= 2:
                shodan_query = shodan_query + ' port:'+port+''
            elif port == "e":
                out("Exiting...", msg_type=-1)
                exit()
            elif port == "b":
                return ""
            out("Finaly, you can optionaly enter any " + fgb("word") + " as filter (i.e.: 'linux upnp avtech'):", msg_type=2, end="")
            word = str(inp())
            if len(word) >= 2:
                shodan_query = shodan_query + f' "{word}"'
            elif word == "e":
                out("Exiting...", msg_type=-1)
                exit()
            elif word == "b":
                return ""
            if shodan_query[0] == " ":
                shodan_query = shodan_query[1:]
            out("This query will be used: '" + fy(shodan_query) + "'. Confirm? [Y/n]", msg_type=2, end="")
            confirm = inp()
            if confirm.lower() in yes_list:
                return shodan_query
            out("Edit your query as you wish or hit " + fy("ENTER") + " to start over:", msg_type=1, end="")
            query = inp(shodan_query)
            if query == shodan_query:
                out("OK, let's start again.",msg_type=1)
                continue
            else:
                out("This query will be used: '" + fy(query) + "'.",msg_type=1)
                return query
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()
        except Exception as err:
            print("Error: "+str(err))
            exit()


"Vunlerabilities info from nvd.nist.gov"
def vuln_info(vuln):
    while True:
        try:
            print("|"+44*"-")
            vuln = str(vuln).upper()
            if vuln[:3] != "CVE":
                out("You can only get more information on CVEs vulnerabilities. Do you want to use " + fy(f"vuln:{vuln}") + " as query (" + fgb("y") + ") or try another one (" + fgb("n") + ")?", msg_type=2, end="")
                vuln_opt1 = inp()
                if vuln_opt1 in ["y",""]:
                    query = "vuln:"+vuln
                    out("Continuing with query " + fy(query) + ".")
                    return query
                else:
                    return False
            loader = Loader(f"Getting {vuln} information...", "Done.", 0.05).start()
            response = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={vuln}")
            loader.stop()
            out(f"Official information about " + fy(vuln) + ".")
            if response.status_code == 200:
                json_response = response.json()
                print(fy(f'\tPublished') + ": " + fg(f'{str(json_response["vulnerabilities"][0]["cve"]["published"])[:10]}'))
                print(fy(f'\tLast Modified') + ": " + fg(f'{str(json_response["vulnerabilities"][0]["cve"]["lastModified"])[:10]}'))
                print(fy('\tDescription') + ": ", end="")
                a = 0
                b = 100
                descrp = str(json_response["vulnerabilities"][0]["cve"]["descriptions"][0]["value"])
                l = (round(len(descrp)/b))+ (len(descrp) % b > 0)
                for i in range(0,l):
                    if i == 0:
                        print(fg(f'{descrp[a:a+b]}'))
                    else:
                        print(fg(f'\t\t     {descrp[a:a+b]}'))
                    a+=b
                cvsskey = str(list(json_response["vulnerabilities"][0]["cve"]["metrics"].keys())[0])
                print(fy(f'\tCVSSDATA') + ": ")
                cvssData = json_response["vulnerabilities"][0]["cve"]["metrics"][cvsskey][0]["cvssData"]
                for key, value in cvssData.items():
                    print(fy(f"\t\t{str(key).capitalize()}") + ": " + fg(f"{str(value).capitalize()}"))
                print("\t\t----------")
                metrics = json_response["vulnerabilities"][0]["cve"]["metrics"][cvsskey][0]
                for key, value in metrics.items():
                    if type(value) != dict:
                        print(fy(f"\t\t{str(key).capitalize()}") + ": " + fg(f"{str(value).capitalize()}"))
                print("\n\t\tFor more information access: " + fy(f"https://nvd.nist.gov/vuln/detail/{vuln}\n"))
                out("Do you want to use " + fy(f"vuln:{vuln}") + " as query [" + fyb("Y") + "], try another one [" + fyb("n") + "], go back [" + fyb("b") + "] or [" + fyb("e") + "] exit?", msg_type=2, end="")
                vuln_opt2 = inp()
                if vuln_opt2 in yes_list:
                    query = "vuln:"+vuln
                    out("Continuing with query " + fy(query) + ".")
                    return query
                elif vuln_opt2 == "e":
                    out("Exiting...", msg_type=-1)
                    exit()
                elif vuln_opt2 == "b":
                    return ""
                else:
                    return False
            else:
                out("API returned error [" + fy(str(response.status_code)) + "] status code.", msg_type=-1)
                out("Exiting.", msg_type=-1)
                exit()
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()


"Build a query based on vulns"
def search_vuln():
    print("|"+44*"-")
    while True:
        try:
            out(bm("Vulnerabilities") + " - Choose one of the following vulnerabilities:", msg_type=2)
            vulns = ["cve-2015-0204","cve-2015-4000","cve-2015-1635","ms15-034","cve-2020-0796","cve-2014-0160","cve-2019-0708","cve-2021-31206","cve-2022-32548","cve-2021-43798","cve-2019-1652","cve-2019-1653","cve-2017-7269","ms17-010","cve-2021-26855","cve-2021-26857","cve-2021-26858","cve-2021-27065","cve-2021-31207","cve-2021-34473","cve-2021-34523","cve-2015-2080","cve-2022-36804","cve-2013-1899","cve-2019-19781","cve-2019-11510","cve-2013-1391","cve-2020-5902","cve-2016-9244","cve-2020-11651","cve-2020-11652"]
            for vuln_number in range(1,len(vulns)):
                if vuln_number < 10:
                    numb = f" {str(vuln_number)}"
                else:
                    numb = str(vuln_number)
                print("\t[" + fgb(numb) + f"] - {vulns[vuln_number-1].upper()}" + (21-len(vulns[vuln_number-1]))*" ", end=" ")
                if vuln_number % 3 == 0:
                    print("\n",end="")
            print("\t[ " + fyb("b") + "] to go " + fy("back") + " to previous list" +
            "\n\t[ " + fyb("e") + "] to " + fy("EXIT"))
            out("Your choice:", msg_type=2, end="")
            selected_vuln = inp()
            if selected_vuln == "e":
                out("Exiting...", msg_type=-1)
                exit()
            elif selected_vuln == "b":
                return ""
            out("You selected " + fy(vulns[int(selected_vuln)-1]) + ".")
            query = vuln_info(vulns[int(selected_vuln)-1])
            if query == False:
                continue
            else:
                return query
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()
        except Exception as err:
            print("search_vuln: "+str(err))
            out(f"Invalid input " + fy(str(selected_vuln)) + ". Try again.", msg_type=-1)
            exit()


"Get Shodan info for specific host"
def shodan_host(api):
    print("|"+44*"-")
    while True:
        try:
            out(bm("Host") + " - Type the host IP address (IPV4), [" + fyb("e") + "] to " + fy("exit") + " or [" + fyb("b") + "] to go " + fy("back") + " and start over.", msg_type=2, end="")
            host = inp()
            if host == "e":
                print("")
                out("Exiting...", msg_type=-1)
                exit()
            elif host == "b":
                print("")
                return ""
            else:
                out("Confirm search for " + fg(host) + "? [Y/n]", msg_type=2, end="")
                confhost = inp()
                if confhost not in yes_list:
                    continue
            out("Starting Shodan search for " + fg(host) + "...")
            loader = Loader("CStarting Shodan host...", "Done.", 0.05).start()
            host_result = api.host(host)
            loader.stop()
            out("Do you want to " + fyb("print") + " the output [Y/n]?", msg_type=2, end="")
            print_output = inp()
            if print_output.lower() in yes_list:
                out("Shodan returned the following information:")    
                print("\tIP: " + fg(f"{host_result.get('ip_str','n/a')} ") + "\n\tOrganization: " + fg(f"{host_result.get('org', 'n/a')} ") + "\n\tOperating System: " + fg(f"{host_result.get('os', 'n/a')} "))
                for item in host_result['data']:
                        print("\n\tPort: \t" + fg(str(item['port'])) + "\n\tBanner:")
                        for itens in str(item['data']).splitlines():
                            print("\t\t" + fg(itens))
            out("Do you want to save the output? Type " + fyb("n") + " or the " + fyb("file name") + " , i.e.: result.json):", msg_type=2, end="")
            filename = inp()
            if filename != "n":
                if filename == "":
                    filename = f"{str(host_result.get('ip_str','result'))}.json"
                resp_json = json.dumps(host_result)
                with open(Path(filename), "w") as test:
                    test.write(resp_json)
                out("Result saved as " + fy(filename) + ".")
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()
        except Exception as err:
            print("shodan_host: "+str(err))


"Edit the query"
def edit_query(query):
    while True:
        try:
            print("|"+44*"-")
            out("Do you want to " + bm("EDIT") + " the query " + fy(f'"{query}"') + "?")
            print("\t[" + fyb("y") + "] To " + fy("edit") + " before continuing")
            print("\t[" + fyb("N") + "] To " + fy("use") + " as is")
            print("\t[" + fyb("b") + "] To go " + fy("back") + " and start over.")
            print("\t[" + fyb("e") + "] To " + fy("exit"))
            out("Please choose one of the above:", msg_type=2, end="")
            edit_query = inp()
            if edit_query.lower() in ["y","yes","yup"]:
                print("")
                out("Edit the query as you wish:",end="")
                query = inp(query)
                continue
            elif edit_query.lower() in ["n","","no"]:
                print("")
                return query
            elif edit_query.lower() in ["e"]:
                print("")
                out("Exiting...", msg_type=-1)
                exit()
            elif edit_query.lower() in ["b"]:
                print("")
                return ""
            else:
                out("Invalid input. Try again.", msg_type=-1)
                continue
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()
        except Exception as err:
            print("edit_query: "+str(err))


"Set a query results limit"
def shodan_query_limit():
    print("|"+44*"-")
    out(("Chose a results " + bm("LIMIT") + " up to 1,000, every " + fgb("100") + " results consumes " + fgb("1") + " credit (default = 100):"), msg_type=2, end="")
    query_limit_in = inp()
    if query_limit_in == "":
        query_limit = 100
    else:
        query_limit = int(query_limit_in)
    return query_limit


"Count how many queries before consuming the credits"
def shodan_query_count(api, query, qlimit=False):#, query_limit):
    try:
        print("|"+44*"-")
        loader = Loader("Checking Shodan search count...", "Done.", 0.05).start()
        account_info = api.info()
        result_count = api.count(query)
        if qlimit != False:
            total_c = int(qlimit)
        else:
            total_c = result_count["total"]
        total_c = result_count["total"]
        loader.stop()
        out(f"Your query " + fy(f'{query}') + " will return up to " + fy(str('{:,}'.format(result_count["total"]))) + " results, consuming " + fy(str(round(total_c/100) + (total_c % 100 > 0))) + " query credits from the remaining " + fy(str('{:,}'.format(account_info.get("query_credits")))) + " credits you have.", msg_type=2)
    except Exception as err:
        print("shodan_query_count: "+str(err))
        exit()


"Last step, Shodan search"
def shodan_search(api, query, hosts_file, m):
    while True:
        try:
            shodan_query_count(api, query)
            query_limit = shodan_query_limit()
            out(f"Choose one of the suggested set of " + bm("OUTPUT COLUMNS") + " or type the number respective to the columns in the order you want it to be saved (i.e.: '1,2,5,7' = 'ip_str,port,country_code,product'):", msg_type=2)
            columns_list = ["ip_str", "port", "city", "region_code", "country_code", "country_name", "version", "product", "timestamp", "isp", "hostnames", "domains", "org", "data"]
            print("\t --- Suggestions ---")
            print("\t[" + fgb("ENTER") + f'] - ' + fy("ip_str,port") + " 1,2 [Default]")
            print("\t[" + fgb("a") + f'] - ' + fy("ip_str,port,city,country_code") + " 1,2,3,5")
            print("\t --- Customize ---")
            for item in range(1,len(columns_list)+1,1):
                print("\t[" + fgb(str(item)) + f'] - ' + fy(columns_list[item-1]))
            print("\t[" + fyb("b") + "] To go " + fy("back") + " and start over.")
            print("\t[" + fyb("e") + "] To " + fy("exit"))
            out("Choose one of the seggested above or type the numbers corresponding in the desired order separated by commas (i'e': 1,2,7,8):", msg_type=2, end="")
            query_columns = str(inp())
            if query_columns.lower() in ["e"]:
                print("")
                out("Exiting...", msg_type=-1)
                exit()
            elif query_columns.lower() in ["b"]:
                print("")
                return ""
            elif query_columns in [""]:
                query_columns = "1,2"
            elif query_columns == "a":
                query_columns = "1,2,3,5"
            else:
                output_columns = query_columns.split(",")
                for sel in output_columns:
                    if sel not in ['1','2','3','4','5','6','7','8','9','10','11','12','13','']:
                        print("")
                        out("Invalid input. Try again.", msg_type=-1)
                        exit()
            output_columns = query_columns.split(",")
            columns_headers = []
            for num in output_columns:
                columns_headers.append(columns_list[int(num)-1])
            sel_cols = ""
            for col_item in columns_headers:
                sel_cols = sel_cols + col_item + ","
            sel_cols = sel_cols[:-1]
            out("Selected columns: " + fy(f"'{sel_cols}'") + ".", msg_type=1)
            print("|"+44*"-")
            if hosts_file != "print_to_terminal":
                out(f"What " + bm("SEPARATOR") + " do you want to use (i.e.: " + fgb("','") + " = '10.10.10.10,8080'; " + fgb("':'") + " = 10.10.10.10:8080, default:',')?", msg_type=2, end="")
                columns_separator = str(inp())
                if columns_separator == "":
                    columns_separator = ','
            shodan_query_count(api, query, qlimit=query_limit)
            out("Ready to continue with " + fy("search") + " [Y/n]?", msg_type=2, end="")
            cont_search = inp()
            if cont_search not in yes_list:
                out("Choose one of the following:",msg_type=2)
                print("\t[" + fyb("q") + "] To " + fy("edit") + " the query and continue.")
                print("\t[" + fyb("b") + "] To go " + fy("back") + " and start over.")
                print("\t[" + fyb("e") + "] To " + fy("exit"))
                out("You choose:", msg_type=2, end="")
                whatodo = inp()
                if whatodo.lower() in ["e"]:
                    print("")
                    out("Exiting...", msg_type=-1)
                    exit()
                elif whatodo.lower() in ["b"]:
                    print("")
                    return ""
                elif whatodo.lower() == "q":
                    query = inp(query)
            out("Search parameters are:")
            print(fy("\tQuery" + ": " + fg(query)) + fy("\n\tLimit" + ": " + fg(str(query_limit))))
            loader = Loader("Continuing Shodan search...","Done.", 0.05).start()
            response = api.search(query, limit=query_limit)
            loader.stop()
            resp_json = json.dumps(response)
            with open(Path('response.json'), "w") as test:
                test.write(resp_json)
            print("")
            if response["total"] == 0:
                out('The query ' + fy(f'"{query}"') + ' returned ' + fy('no results') + '. Try another query.', msg_type=-1)
                out('Exiting.', msg_type=-1)
                exit()
            if hosts_file == "print_to_terminal":
                out("Those are the results found for the query " + fyb(f"'{query}'") + ":")
                head = "\t|  "
                for col_head in columns_headers:
                    head = head + (15-len(col_head))*" " + col_head.replace("_"," ").title() + "  |  "
                print(fyb(head))
                for host in response['matches']:
                    line = "\t|  "
                    for col_head in columns_headers:
                        if col_head in ["city","region_code","country_code","country_name"]:
                            conte = str(host.get("location").get(col_head,"")).replace("\n"," - ").replace(",","_").replace("\r"," - ")
                            line = line + (15-len(conte))*" " + conte[:15] + "  |  "
                        else:
                            conte = str(host.get(col_head,"")).replace("\n"," - ").replace(",","_").replace("\r"," - ")
                            line = line + (15-len(conte))*" " +  conte[:15] + "  |  "
                    line = line[:-1]
                    print(fg(line))
                account_info = api.info()
                out(f"Found " + fg(str('{:,}'.format(len(response['matches'])))) + " hosts and  " + fg("printed") + " above. Remaining query credits: " + fg(str('{:,}'.format(account_info.get("query_credits")))) + " from " + fg(str('{:,}'.format(account_info.get("usage_limits").get("query_credits")))), msg_type=1)
            else:
                with open(hosts_file, m) as host_write:
                    for host in response['matches']:
                        line = ""
                        for col_head in columns_headers:
                            if col_head in ["city","region_code","country_code","country_name"]:
                                line = line + str(host.get("location").get(col_head,"")).replace("\n"," - ").replace(",","_").replace("\r"," - ") + columns_separator
                            else:
                                line = line + str(host.get(col_head,"")).replace("\n"," - ").replace(",","_").replace("\r"," - ") + columns_separator
                        line = line[:-1] + "\n"
                        host_write.write(line)
                account_info = api.info()
                out(f"Found " + fg(str('{:,}'.format(len(response['matches'])))) + " hosts and saved to " + fg(str(hosts_file)) + ". Remaining query credits: " + fg(str('{:,}'.format(account_info.get("query_credits")))) + " from " + fg(str('{:,}'.format(account_info.get("usage_limits").get("query_credits")))), msg_type=1)
            out("This search generated " + fy('response.json') + " file. If you choose to keep, be sure to rename it before doing another search. If you don't you'll lose it. Do you want to keep it [Y/n]?", msg_type=2,end="")
            keep = inp()
            if keep in yes_list:
                return ""
            else:
                file_to_rem = Path('response.json')
                file_to_rem.unlink()
                return ""
        except shodan.APIError as e:
            if "The search query was invalid" in str(e.args):
                out("The search query was invalid")
            print('Error: {}'.format(e))
        except Exception as err:
            if "Insufficient query credits" in str(err):
                shodan_status(api)
                out(fy("Insufficient query credits. Exiting."))
                exit()
            print('Error: {}'.format(err))
            print("Exiting.")
            exit()


"Saves search query to history file"
def search_history_save(query):
    file_path = Path(HISTORY_FILE)
    if not file_path.is_file():
        with file_path.open("w", encoding="utf-8") as c:
            c.write("")
    current_history = open(file_path).read().splitlines()
    for i, line in enumerate(current_history):
        if line.split("|")[1] == query:
            toDel = i
            current_history.pop(toDel)
            with open(file_path, 'w') as f:
                for line in current_history:
                    f.write(line + '\n')
    new_line = f'{str(datetime.now().strftime("%d/%m/%Y at %H:%M:%S"))}|{query}'
    with file_path.open("r+", encoding="utf-8") as f:
        content_lines = f.read().splitlines()
        if len(content_lines) >= int(HISTORY_LIMIT):
            f.close()
            with file_path.open("w+", encoding="utf-8") as s:
                for idx in range(1,int(HISTORY_LIMIT),1):
                    s.write(content_lines[idx] + "\n")
        with file_path.open("a", encoding="utf-8") as a:
            a.write(new_line + "\n")


"Handle output file exists"
def hosts_file_exists(hosts_file):
    try:
        while True:
            hosts_file = Path(hosts_file)
            if hosts_file.is_file() == False:
                return "w", hosts_file
            else:
                file_len = str(len(open(Path(hosts_file)).read().splitlines()))
                out(f"You already have a " + fgb(str(hosts_file)) + " file with " + fgb(file_len) + " hosts. You can:" +
                "\n\t[" + fgb('a') + "] - append to file" +
                "\n\t[" + fgb('w') + "] - overwrite the file" +
                "\n\t[" + fgb('b') + f"] - backup the existing " + fy(str(hosts_file)) + " file as " + fy(f"backup_{hosts_file}") + " and create a new " + fy(str(hosts_file)) +
                " file\n\tType a different " + fgb('file name') + " to be created.", msg_type=-1)
                out("Please choose " + fgb('a') + " (append), " + fgb('w') + " (overwrite - DEFAULT), " + fgb('b') + " (backup), " + fyb('e') + " (exit) or type a " + fgb('new file name') + ":", msg_type=2, end="")
                mr = inp()
                if mr in["a","w","b","","e"]:
                    if mr == "a":
                        return "a+", hosts_file
                    elif mr == "w" or mr == "":
                        return "w", hosts_file
                    elif mr == "b":
                        os.rename(hosts_file, 'backup_'+hosts_file)
                        return "w", hosts_file
                    elif mr == "e":
                        out("Exiting.", msg_type=-1)
                        exit()
                    else:
                        out("Invalid option. Exiting.", msg_type=-1)
                        exit()
                else:
                    hosts_file = mr
    except KeyboardInterrupt:
        print("")
        out("Exiting...", msg_type=-1)
        exit()
    except Exception as err:
        print("hosts_file_exists: "+str(err))


"Handle output file"
def hosts_file_chose():
    print("|"+44*"-")
    try:
        while True:
            out(f" - You want to " + bm("OUTPUT") + " the results to:" +
            "\n\t[" + fgb('d') + "] - Save to default " + fy("hosts.txt") +
            "\n\t[" + fgb('p') + "] - " + fy("Print") + " results on terminal only (no output file will be created)" +
            "\n\t[" + fyb("b") + "] - To go " + fy("back") +
            "\n\t[" + fyb("e") + "] - To " + fy("EXIT"))
            out("Chose one from above or type a different " + fy('file name') + " to be created:", msg_type=2, end="")
            mr = inp()
            if mr in["","d","p"]:
                if mr in ["d",""]:
                    return "hosts.txt"
                elif mr == "p":
                    return "print_to_terminal"
            elif mr == "e":
                out("Exiting.", msg_type=-1)
                exit()
            elif mr == "b":
                return False
            else:
                out(f"File output will be saved as " + fbb(mr) + ". Continue? [Y/n]", msg_type=2)
                conf = inp()
                if conf.lower() in yes_list:
                    return mr
                elif conf.lower() in no_list:
                    continue
                else:
                    if english_mofo() == True:
                        continue
                    else:
                        exit()
    except KeyboardInterrupt:
        print("")
        out("Exiting...", msg_type=-1)
        exit()
    except Exception as err:
        print("Error: "+str(err))
        exit()


"Start the wizard"
def start_wizard():
    "Get API:"
    step = ""
    while True:
        try:
            api = shodan_api_exists()
            query, step = shodan_wizard(api,step)
            query = edit_query(query)
            if query == "":
                continue
            query = shodan_facets(api, query)
            shodan_query_count(api, query)
            query = edit_query(query)
            hosts_filepre = hosts_file_chose()
            if hosts_filepre == False:
                continue
            if hosts_filepre == "print_to_terminal":
                hosts_file = hosts_filepre
                m = "w"
            else:
                m, hosts_file = hosts_file_exists(hosts_filepre)
            search_history_save(query)
            shodan_search(api, query, hosts_file, m)
        except KeyboardInterrupt:
            print("")
            out("Exiting...", msg_type=-1)
            exit()
        except Exception as err:
            print("start_wizard: "+str(err))


if __name__ == '__main__':
    start_wizard()

# separate shodan_search in shodan_search and shodan_search_count and ask what user wants to change after he said no on line 1108

# "Full list of facets (not currently being used):"
# facets_list = ["asn","bitcoin.ip","bitcoin.ip_count","bitcoin.port","bitcoin.user_agent","bitcoin.version","city","cloud.provider","cloud.region","cloud.service","country","cpe","device","domain","has_screenshot","hash","http.component","http.component_category","http.favicon.hash","http.headers_hash","http.html_hash","http.robots_hash","http.status","http.title","http.waf","ip","isp","link","mongodb.database.name","ntp.ip","ntp.ip_count","ntp.more","ntp.port","org","os","port","postal","product","redis.key","region","rsync.module","screenshot.hash","screenshot.label","snmp.contact","snmp.location","snmp.name","ssh.cipher","ssh.fingerprint","ssh.hassh","ssh.mac","ssh.type","ssl.alpn","ssl.cert.alg","ssl.cert.expired","ssl.cert.extension","ssl.cert.fingerprint","ssl.cert.issuer.cn","ssl.cert.pubkey.bits","ssl.cert.pubkey.type","ssl.cert.serial","ssl.cert.subject.cn","ssl.chain_count","ssl.cipher.bits","ssl.cipher.name","ssl.cipher.version","ssl.ja3s","ssl.jarm","ssl.version","state","tag","telnet.do","telnet.dont","telnet.option","telnet.will","telnet.wont","uptime","version","vuln","vuln.verified"]