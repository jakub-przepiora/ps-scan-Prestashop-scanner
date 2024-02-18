#!/usr/bin/python3

from datetime import datetime
import requests
import os
import sys
import re

class PsScan:

    adminPanelList = ['/admin', '/iadmin', '/adminpanel', '/admin123']
    installList = ['/install', '/install123', '/install321', '/.install']
    informationFromScan = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")




    def __init__(self, args) -> None:
        print('''

░▒▓███████▓▒░ ░▒▓███████▓▒░             ░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░ ░▒▓██████▓▒░              ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░             ░▒▓█▓▒░                   ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░             ░▒▓█▓▒░                   ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓███████▓▒░             ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                                                                             
Autor: TheMrEviil                                                                                

''')
        if sys.argv[2]:
            target = sys.argv[2]
            if not self.isPresta(target):
                print("This target don't use Prestashop")
                return None
            self.getPrestaInfoFile(target)
            self.checkInstallDir(target)
            self.checkAdminDir(target)
            
            pass

    def isPresta(self, target):
        resp = requests.get(target)
        
        if "prestashop" in resp.text:
            print("[+] Website using Prestashop")
            return True
        resp = requests.get(target+'/INSTALL.txt')
        if "prestashop" in resp.text:
            print("[+] Website using Prestashop")
            return True
        return False

    def checkAdminDir(self, target):
        
        for path in self.adminPanelList:
            resp = requests.get(target+path)
            if resp.status_code == 200:
                print(f'[-] Found Admin panel path: {target}{path}')

    def checkInstallDir(self, target):
        
        for path in self.installList:
            resp = requests.get(target+path)
            if resp.status_code == 200:
                print(f'[-] Found Installation path: {target}{path}')
    def getThemeName(self, target):
        pass

    def getPrestaVersion(self, target):
        pass
    def getPrestaVersionFromFile(self, file):

        try:
            with open(file, 'r', encoding='utf-8') as fileReaded:
                content = fileReaded.read()

                match = re.search(r'PrestaShop\s+(\d+(\.\d+)*)', content)

                if match:
                    version_number = match.group(1)
                    print(f"[+] The PrestaShop version found in the file INSTALL is: {version_number}")
                    return version_number
                else:
                    print("[-] PrestaShop version not found in the file.")
                    return None

        except FileNotFoundError:
            print(f"The file '{file}' was not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def getPrestaInfoFile(self, target):
        resp = requests.get(target+"/INSTALL.txt")
        if resp.status_code == 200:
            self.createFolderForScanInfo()
            open(self.informationFromScan+'/install.txt', 'w', encoding='utf-8').write(resp.text)
            self.getPrestaVersionFromFile(self.informationFromScan+'/install.txt')

    def createFolderForScanInfo(self):
        
        fullPath = os.path.join(os.getcwd(), self.informationFromScan)

        if not os.path.exists(fullPath):
            os.mkdir(fullPath)

if __name__ == "__main__":
    if not sys.argv[1]:
        print("You can check flags using: ps-scan.py help")
        pass
    
    if sys.argv[1] == 'help':
        
        helpFlags = ''' 
    -h      Host to scan (https://example.com)
        '''
        print(helpFlags)
    
    if '-h' in sys.argv:
        ans =input("\nDo you have permission to scan this website? [y/n] ")
        if ans == 'y':
            PsScan(sys.argv)
        else:
            pass