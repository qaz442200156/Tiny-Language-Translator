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

setting_auto_save_log = True
# use `global`` to access global variable

# source language
src_language = 'en'
# language to translate
dest_language = 'zh-Tw'
# auto save log file name
auto_log_file_name = "translated.txt"

def check_help(command):
    if "-h" in command:
        print("-s to check on used settings")
        print("-AutoSave to Auto Save Log into text file")
        print("Sample:-AutoSave")
        command = ""
        return True
    return False

def check_setting(command):
    global setting_auto_save_log
    any_change = False
    if "-autosave" in command.lower():
        setting_auto_save_log = setting_auto_save_log is not True
        any_change = True

    return any_change

def show_setting_state(command,force_show=False):
    global setting_auto_save_log
    if "-s" in command.lower() or force_show:
        state = "On" if setting_auto_save_log else "Off"
        print("Auto Save Log Is",state)
        return True
    return False

# Clean console output
def clean_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_quit(world):
    if len(world) == 1 and world.isalpha() and world.lower().strip() in ['e','q']:
        return True
    return False

def translate_world(world):
    if is_quit(world):
        return ""
    global src_language
    global dest_language
    translated = translator.translate(world, src=src_language, dest=dest_language)
    result = f"{src_language}:{world} -> {dest_language}:{translated.text}"
    print(result)
    return result

def correct_grammar_and_translate(sentence,matches):
    if is_quit(sentence):
        return ""
    global src_language
    global dest_language
    corrected_text = language_tool_python.utils.correct(sentence,matches)
    translated = translator.translate(sentence, src=src_language, dest=dest_language)
    result = f"{src_language}:{sentence} #[Fix]:{corrected_text} -> {dest_language}:{translated.text}"
    print(result)
    return result

def save_translate_result(text):
    global auto_log_file_name
    with open(auto_log_file_name, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

def command_reader(command):    
    # clear old result
    result = ""
    first_command = command.lower().strip()

    if len(command) == 0:
        return True
    elif first_command[0] in ['e','q']:
        return False
    elif first_command == 'cls':
        clean_console()
        return True
    elif first_command[0] == 'w':
        command = input("Enter a world (or 'e'/'q' to quit): ")
        result = translate_world(command)
    elif first_command[0] == 's':
        command = input("Enter a sentence (or 'e'/'q' to quit): ")
        matches = tool.check(command)
        if len(matches) == 0:
            result = translate_world(command)
        else:
            result = correct_grammar_and_translate(command,matches)
    
    if len(result) > 0:
        save_translate_result(result)
    return True

def main():
    while True:
        command = input("Enter S(sentence) or W(a word) to set translate mode (or 'e'/'q' to quit '-h' for help): ")
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