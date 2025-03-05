#!/usr/bin/python3

import requests
import os
import sys
import re
from datetime import datetime
import xml.etree.ElementTree as ET


class PsScan:
    global target
    global envWithoutVersion
    adminPanelList = ['/admin', '/iadmin', '/adminpanel', '/admin123']
    installList = ['/install', '/install123', '/install321', '/.install']
    defaultModules = ["blindinvoices", "blockreassurance", "blockwishlist", "contactform", "dashactivity", "dashgoals", "dashproducts", "dashtrends", "followup", "graphnvd3", "gridhtml", "gsitemap", "pagesnotfound", "productcomments", "ps_banner", "ps_bestsellers", "ps_brandlist", "ps_cashondelivery", "ps_categoryproducts", "ps_categorytree", "ps_checkpayment", "ps_contactinfo", "ps_crossselling", "ps_currencyselector", "ps_customeraccountlinks", "ps_customersignin", "ps_customtext", "ps_dataprivacy", "ps_distributionapiclient", "ps_emailalerts", "ps_emailsubscription", "ps_facetedsearch", "ps_faviconnotificationbo", "ps_featuredproducts", "psgdpr", "ps_googleanalytics", "ps_imageslider", "ps_languageselector", "ps_linklist", "ps_mainmenu", "ps_newproducts", "ps_reminder", "ps_searchbar", "ps_sharebuttons", "ps_shoppingcart", "ps_socialfollow", "ps_specials", "ps_supplierlist", "ps_themecusto", "ps_viewedproduct", "ps_wirepayment", "referralprogram", "statsbestcategories", "statsbestcustomers", "statsbestmanufacturers", "statsbestproducts", "statsbestsuppliers", "statsbestvouchers", "statscarrier", "statscatalog", "statscheckup", "statsdata", "statsforecast", "statsnewsletter", "statspersonalinfos", "statsproduct", "statsregistrations", "statssales", "statssearch", "statsstock"]
    headers = {'User-Agent': 'PsScan'} # Default user-agent

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

Autor: Jakub "TheMrEviil" Przepióra
Contact: jakub.przepioraa@gmail.com
Version: 1.0.4

''')
        if sys.argv[2]:
            self.target = sys.argv[2]
            if len(sys.argv) > 3 and (sys.argv[3] == "-wv" or sys.argv[3] == "--without-version"):
                print("[INFO] CVE will search without version")
                self.envWithoutVersion = 1
            self.createFolderForScanInfo()
            if not self.isPresta():
                print("This target don't use Prestashop")
                return None
            self.getPrestaInfoFile()
            self.checkInstallDir()
            self.checkAdminDir()
            self.getThemeName()
            self.getModulesDefault()
            self.getModules()
            pass

    # Check version prestashop
    def isPresta(self):
        resp = requests.get(self.target)

        if "prestashop" in resp.text:
            print("[+] Website using Prestashop")
            open(self.informationFromScan+'/home.txt', 'w', encoding='utf-8').write(resp.text)
            return True
        resp = requests.get(target+'/INSTALL.txt',  headers=self.headers)
        if "prestashop" in resp.text:
            print("[+] Website using Prestashop")
            open(self.informationFromScan+'/home.txt', 'w', encoding='utf-8').write(resp.text)
            return True
        return False
    # Try bruteforce admin panel dir
    def checkAdminDir(self):

        for path in self.adminPanelList:
            resp = requests.get(self.target+path,  headers=self.headers)
            if resp.status_code == 200:
                print(f'[-] Found Admin panel path: {self.target}{path}')
    # Try find install dir
    def checkInstallDir(self):

        for path in self.installList:
            resp = requests.get(self.target+path,  headers=self.headers)
            if resp.status_code == 200:
                print(f'[-] Found Installation path: {self.target}{path}')

    # Get theme name
    def getThemeName(self):
        try:
            with open(self.informationFromScan+'/home.txt', 'r', encoding='utf-8') as fileReaded:
                content = fileReaded.read()
                match = re.search(r'/themes/([^/]+)/', content)
                if match:
                    themeName = match.group(1)
                    print(f"[+] Found theme: {themeName}")
                    return themeName
                else:
                    print("[-] Theme not found")
                    return None

        except FileNotFoundError:
            print(f"The file 'home.txt' was not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def getPrestaVersion(self):
        pass

    # Try get Prestashop verstion from INSTALL file
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

    def getPrestaInfoFile(self):
        resp = requests.get(self.target+"/INSTALL.txt",  headers=self.headers)
        if resp.status_code == 200:
            open(self.informationFromScan+'/install.txt', 'w', encoding='utf-8').write(resp.text)
            self.getPrestaVersionFromFile(self.informationFromScan+'/install.txt')

    def getModules(self):
        print("\n============================ Modules =======================================\n")
        try:
            with open(self.informationFromScan+'/home.txt', 'r', encoding='utf-8') as fileReaded:
                content = fileReaded.read()

                # Use a regular expression to find module names in different patterns
                matches = re.finditer(r'/module/([^/]+)/|/modules/([^/]+)/|/module/([^/]+)/|/modules/([^/]+)/|modules ([^/]+)|module ([^/]+)', content)

                # List to store unique module names
                unique_module_names = []

                for match in matches:
                    moduleName = match.group(1) or match.group(2) or match.group(3) or match.group(4) or match.group(5) or match.group(6)

                    # Check if the module name is not in the list
                    if moduleName and moduleName not in unique_module_names:
                        unique_module_names.append(moduleName)
                        print(f"[+] Module: {moduleName}")

                # Check for the presence of the specific comment and extract "Block Search"
                # comment_match = re.search(r'<!-- Block search module (\w+) -->', content)
                # if comment_match:
                #     comment_text = comment_match.group(1)
                #     print(f"[+] Detected <!-- {comment_text} -->")

        except FileNotFoundError:
            print(f"The file '{self.informationFromScan}/home.txt' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        self.getModulesVersion(unique_module_names)

    # Check default modules
    def getModulesDefault(self):
        print("\n============================ Try get default modules XML =======================================\n")
        for module in self.defaultModules:
            responseNormal = requests.get(self.target+"/modules/"+module+'/config.xml',  headers=self.headers)
            responseRewrite = requests.get(self.target+"/module/"+module+'/config.xml',  headers=self.headers)
            response = ''
            if responseNormal.status_code == 200:
                response = responseNormal
            if responseRewrite.status_code == 200:
                response = responseRewrite

            if not response:
                continue

            open(self.informationFromScan+'/'+module+'.xml', 'w', encoding='utf-8').write(response.text)
            print(f'\n[+] Found and save config file: '+module+'/config.xml')
            moduleVersion = self.parseModuleConfigXML(module)
            self.findCve(module, moduleVersion)

    def getModulesVersion(self, moduleList):
        print("\n============================ Try get modules XML =======================================\n")
        for module in moduleList:
            resp = requests.get(self.target+"/modules/"+module+'/config.xml',  headers=self.headers)
            if resp.status_code == 200:
                open(self.informationFromScan+'/'+module+'.xml', 'w', encoding='utf-8').write(resp.text)

                print(f'\n[+] Found and save config file: '+module+'.xml')
                moduleVersion = self.parseModuleConfigXML(module)
                self.findCve(module, moduleVersion)


    def parseModuleConfigXML(self, module):
        try:
            # Parse the XML file
            tree = ET.parse(self.informationFromScan+'/'+module+'.xml')
            root = tree.getroot()

            # Find the version element and extract its text
            version_element = root.find('.//version')

            if version_element is not None:
                version = version_element.text
                print(f"[!] The module version is: {version}")
                return version
                # self.findCve(module, version)
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    # FIND IN CVE MITRE

    def findCve(self, module, version):
        try:
            response = requests.get('https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword='+module+'%20'+version,  headers=self.headers)

            if response.status_code == 200:
                cve_pattern = re.compile(r'CVE-\d+-\d+')
                matches = cve_pattern.findall(response.text)

                if matches:
                    # Print the first 10 CVEs or all if there are fewer than 10
                    print(f"[!] Found CVE(s) in the response: {', '.join(matches[:10])}")
                else:
                    print("No CVEs found in the response with version.")
            
            else:
                print(f"Error: HTTP status code {response.status_code}")

            if self.envWithoutVersion == 1:
                    print("[+} Try find CVEs without version")
                    response = requests.get('https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword='+module+'%20'+version,  headers=self.headers)

                    if response.status_code == 200:
                        cve_pattern = re.compile(r'CVE-\d+-\d+')
                        matches = cve_pattern.findall(response.text)
                        if matches:
                            print(f"[!] Found CVE(s) without version in the response: {', '.join(matches[:10])}")
        except requests.RequestException as e:
            print(f"An error occurred during the request: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        print(f'[+] More CVE https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={module}%20{version}')

    def createFolderForScanInfo(self):

        fullPath = os.path.join(os.getcwd(), self.informationFromScan)

        if not os.path.exists(fullPath):
            os.mkdir(fullPath)

    def scanPopularScripts(self):
        targetsScripts = ['/unzipper.php','/adminer.php', '/phpmyadmin.php', '/monstra-ftp/index.php', '/info.php']
        for target in targetsScripts:
            resp = requests.get(self.target+targetsScripts,  headers=self.headers)
            if resp.status_code == 200:
                print(f'[+] Found popular script: {self.target}{target}')

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("\nYou can check flags using: ps-scan.py help\n")
        sys.exit()

    if not sys.argv[1]:
        print("\nYou can check flags using: ps-scan.py help\n")
        sys.exit()

    if sys.argv[1] == 'help':

        helpFlags = '''
    -h      --host              Host to scan (https://example.com)
    -wv     --without-version   searching CVEs without number version 
        '''
        print(helpFlags)

    if '-h' in sys.argv:
        ans =input("\nDo you have permission to scan this website? [y/n] ")
        if ans == 'y':
            PsScan(sys.argv)
        else:
            pass
    else:
        print("\nExample using: python3 ps-scan.py -h https://example.com")
        pass
