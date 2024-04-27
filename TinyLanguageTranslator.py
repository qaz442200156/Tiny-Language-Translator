# Last Update: 2024/04/28
# Author: Luke Kaser
# Description: Tiny Language Translator
# E-mail:qaz442200156@gmail.com

import googletrans
from googletrans import Translator
# For translate language
import language_tool_python
# If you got an error when using language_too_python
# -Is already Installed language_tool_python module -> pip install language-tool-python
# -Is already Installed Java(JDK) -> https://adoptopenjdk.net/
import os
# For using clean console output
import time
# For stop a while

translator = Translator()
tool = language_tool_python.LanguageTool('en-US')

setting_keep_log = False
setting_auto_save_log = True
skip_clean_console = False
# use `global`` to access global variable

src_language = 'en'
dest_language = 'zh-Tw'

def check_help(command):
    global skip_clean_console
    if "-h" in command:
        print("-s to check on used settings")
        print("-log to Keep old log")
        print("-AutoSave to Auto Save Log into text file")
        print("Sample:-log -AutoSave")
        command = ""
        skip_clean_console = True
        return True
    return False

def check_setting(command):
    global setting_keep_log
    global setting_auto_save_log
    any_change = False
    if "-log" in command.lower():
        setting_keep_log = setting_keep_log is not True
        any_change = True
    if "-autosave" in command.lower():
        setting_auto_save_log = setting_auto_save_log is not True
        any_change = True

    return any_change

def show_setting_state(command,force_show=False):
    global skip_clean_console
    global setting_keep_log
    global setting_auto_save_log
    if "-s" in command.lower() or force_show:
        if setting_keep_log:
            print("Keep Log Is On")
        else:
            print("Keep Log Is Off")
        if setting_auto_save_log:
            print("Auto Save Log Is On")
        else:
            print("Auto Save Log Is Off")
        skip_clean_console = True
        return True
    return False

# Clean console output
def clean_console(force = False):
    global skip_clean_console
    if skip_clean_console:
        skip_clean_console = False
        return
    if not setting_keep_log or force:
        os.system('cls' if os.name == 'nt' else 'clear')

def translate_world(world):
    translated = translator.translate(world, src=src_language, dest=dest_language)
    result = "{src_language}:"+world+" -> {dest_language}:"+translated.text
    print(result)
    return result

def correct_grammar_and_translate(sentence):    
    corrected_text = language_tool_python.utils.correct(sentence,matches)
    translated = translator.translate(sentence, src=src_language, dest=dest_language)
    result = "{src_language}:"+sentence+" #[Fix]:"+corrected_text+" -> {dest_language}:"+translated.text
    print(result)
    return result

def save_translate_result(text):
    with open('translated.txt', 'a') as f:
        f.write(text + '\n')

def command_reader(command):    
    # clear old result
    result = ""

    if len(command) == 0:
        return True
    elif command.lower() == 'e':
        return False
    elif command.lower() == 'cls':
        clean_console(True)
        return True
    elif command.lower() == 'w':
        clean_console()
        command = input("Enter a world (or 'e' to quit): ")
        result = translate_world(command)
    elif command.lower() == 's':
        clean_console()
        command = input("Enter a sentence (or 'e' to quit): ")
        matches = tool.check(command)
        if len(matches) == 0:
            result = translate_world(command)
        else:
            result = correct_grammar_and_translate(command)
    
    if len(result) > 0:
        save_translate_result(result)
    return True

def main():
    while True:    
        clean_console()
        
        command = input("Enter S(sentence) or W(world) to set translate mode (or 'e' to quit '-h' for help): ")
        if check_help(command):
            continue
        if check_setting(command):
            show_setting_state(command, True)
            continue
        if show_setting_state(command):
            continue
        if command_reader(command) == False:
            break

        time.sleep(0.5)

if __name__ == "__main__":
    main()