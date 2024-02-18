#!/usr/bin/python3


import requests
import os
import sys

class PsScan:

    adminPanelList = ['/admin', '/iadmin', '/adminpanel', '/admin123']
    installList = ['/install', '/install123', '/install321', '/.install']


    def __init__(self, args) -> None:
        print('''

░▒▓███████▓▒░ ░▒▓███████▓▒░             ░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░ ░▒▓██████▓▒░              ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░             ░▒▓█▓▒░                   ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░             ░▒▓█▓▒░                   ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓███████▓▒░             ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                                                                             
                                                                                             

''')
        if sys.argv[2]:
            target = sys.argv[2]
            if not self.isPresta(target):
                print("This target don't use Prestashop")
            
            self.checkInstallDir(target)
            self.checkAdminDir(target)
            pass
    
    def isPresta(self, target):
        resp = requests.get(target)
        
        if "prestashop" in resp.text:
            print("Website using Prestashop")
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
        PsScan(sys.argv)