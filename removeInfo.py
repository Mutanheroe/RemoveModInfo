# Written by Mu based on petrascyll

import os
import argparse
import time
import traceback
import magic

from pathlib import Path



def main():
    filesModified = [[],[]]
    parser = argparse.ArgumentParser(
        prog="remove mod info",
        description=('')
    )
    
    print("Remove mod info")

    parser.add_argument('ini_filepath', nargs='?', default=None, type=str)
    args = parser.parse_args()

    if args.ini_filepath:
        if args.ini_filepath.endswith('.ini'):
            print('Passed .ini file:', args.ini_filepath)
            filesModified = upgrade_ini(args.ini_filepath,filesModified)
      
        else:
            raise Exception('Passed file is not an Ini')

    else:
      #  print('CWD: {}'.format(os.path.abspath('.')))
        filesModified =process_folder('.',filesModified)

    drawbuda()
    if(len(filesModified[0]) == 0 and len(filesModified[1]) == 0):
        print('Done! there is nothink to update')
    else:
        print('The next files has been created:')
        for p in filesModified[0]:
            print(p)
        print('The next files has been updated:')
        for p in filesModified[1]:
            print(p)

def process_folder(folder_path,filesModified):
    for filename in os.listdir(folder_path):
        if filename.upper().startswith('DISABLED') and filename.lower().endswith('.ini'):
            continue
        if filename.upper().startswith('DESKTOP'):
            continue

        filepath = os.path.join(folder_path, filename)
        if os.path.isdir(filepath):
            filesModified = process_folder(filepath,filesModified)
        elif filename.endswith('.ini'):
            print('Found .ini file at:', filepath)
            upgrade_ini(filepath,filesModified)

    return filesModified

def upgrade_ini(filepath,filesModified):
    content = ''
    enco = ''
    try:
        blob = open(filepath, 'rb').read()
        m = magic.Magic(mime_encoding=True)
        enco = m.from_buffer(blob) 
       # print ('encoding '+enco)

    except:    
        raise Exception('Unable to retrive encoding')

    try:
        content = open(filepath,encoding=enco)
    
    except UnicodeDecodeError:
        print ('error reading the file: ' +filepath + " encoding: "+ enco)

    text = ''
    found = False
   
    for line in content:
   
        firstString = line.split(' ')[0] 
        if firstString == 'data' or  firstString == 'data'.encode(enco):
            print ('found and ocurrence on' +filepath)
            line = ';'+line
            found = True 
        text += line 

    content.close()    
    
    if found:
        try:
            filesModified= save(filepath,text,enco,filesModified)
    
        except Exception as X:
            print('Fatal error occurred while saving changes for {}!'.format(filepath))
            print(traceback.format_exc())
            print()
                
    return filesModified

def pause():
   input('Press Enter to close')

def save(filepath,text,encoding,filesModified):

        basename = filepath.split("\\")[-1]
        dir_path = filepath.split(basename)[0]
        backup_filename = f'DISABLED_BACKUP_{int(time.time())}.{basename}'
        backup_fullpath = os.path.join(dir_path, backup_filename)

        os.rename(filepath, backup_fullpath)

        filesModified[0].append(backup_fullpath)

        print(f'Created Backup: {backup_filename} at {dir_path}')
        with open(filepath, 'w', encoding=encoding) as updated_ini:
            updated_ini.write(text)
            updated_ini.flush()
            print('\tSaved: {}'.format(filepath))
            
            filesModified[1].append(filepath)
            
        print('Update applied')
        return filesModified

def drawbuda():
    print()
    print()
    print("                       _oo0oo_") 
    print("                      o8888888o")
    print("                      8`' . `'8")
    print("                      (| -_- |)")
    print("                      0|  =  |0")
    print("                    ___|`----'|___")
    print("                  .'  |     |  '.")
    print("                 |  |||  :  |||||  ")
    print("                | _||||| -:- |||||- ||")
    print("               |   | |||  -  ||| |   |")
    print("               | |_|  ''|---|''  |_| |")
    print("               |  .-|__  '-'  ___|-. |")
    print("             ___'. .'  |--.--|  `. .'___")
    print("          .`  '<  `.___|_<|>_|___.' >' `.")
    print("         | | :  `- |`.;`| _ |`;.`| - ` : | |")
    print("         |  | `_.   |_ __| |__ _|   .-` |  |")
    print("     =====`-.____`.___ |_____|___.-`___.-'=====")
    print("                       `=---='")
    print()
    print()
main()

pause()
#python -m PyInstaller  --onefile  removeInfo.py   