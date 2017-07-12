from bs4 import BeautifulSoup
import sys, os
import urllib2, urllib
import argparse

# Colors
W  = '\033[0m'  # white (normal)
R  = '\033[0;31m' # red
G  = '\033[0;32m' # green
O  = '\033[0;33m' # orange
B  = '\033[0;34m' # blue
P  = '\033[0;35m' # purple
C  = '\033[0;36m' # Cyan
lR  = '\033[1;31m' # red
lG  = '\033[1;32m' # green
lO  = '\033[1;33m' # orange
lB  = '\033[1;34m' # blue
lP  = '\033[1;35m' # purple
lC  = '\033[1;36m' # Cyan

Parser = argparse.ArgumentParser(prog='whoUR.py', description="Tool for information gathering")

Parser.add_argument("-d", "--dic-path", help="Dictonaries Path, Example: -d /root/", action="store", default="dics/", dest="dicPath")
Parser.add_argument("-a", "--dic-adminspage", help="Admin Page dictonary, Example: -a adminspage.txt", action="store", default="adminspage.txt", dest="dicAdminsPage")

Args = Parser.parse_args()

# Dictonaries
dics_path = Args.dicPath
dic_adminsPage = dics_path+'/'+Args.dicAdminsPage


# IP Reverse Lookup
def ipReverse(url_input):
    url = urllib.urlopen('http://viewdns.info/reverseip/?host='+url_input+'&t=1').read()
    soup = BeautifulSoup(url, "lxml")

    tables = soup.find_all('table',{"border": "1"})
    sites = []
    for table in tables:
        trs = table.find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            tmp_sites = []
            tmp_count = 0
            for td in tds:
                tmp_sites.append(td.text)
            sites.append(tmp_sites)

    print P+"\n---------------------------------"
    print P+"-I P  R E V E R S E  L O O K U P-"
    print P+"---------------------------------\n"
    print B+"\n[!] Scann in Process..."
    for site in sites:
        print P+'[#] '+G+'http://'+site[0]
        print P+'[!] '+B+'Last Revision Date: '+lG+site[1]+'\n'

# WHOIS Lookup
def whois(url_input):
    print P+"\n-------------------------"
    print P+"-W H O  I S  L O O K U P-"
    print P+"-------------------------\n"
    print B+"[!] Scann in Process...\n"

    url = urllib2.urlopen('http://api.hackertarget.com/whois/?q='+url_input).read()
    soup = BeautifulSoup(url, 'lxml')

    print G+soup.p.string

# DNS Lookup
def dnsLookup(url_input):
    print P+"\n--------------------"
    print P+"-D N S  L O O K U P-"
    print P+"--------------------\n"
    print B+"[!] Scann in Process...\n"

    url = urllib2.urlopen('https://api.hackertarget.com/dnslookup/?q='+url_input).read()
    soup = BeautifulSoup(url, 'lxml')

    print G+soup.p.string

# Admin Pages Finder
def adminFinder(url_input):
    print P+"\n-------------------------"
    print P+"-A D M I N  F I N D E R -"
    print P+"-------------------------\n"
    print B+"[!] Scann in Process...\n"
    with open(dic_adminsPage) as f:
        adminPageFound = []
        adminPageNotFound = 0
        contents = f.readlines()
        print P+'[+] Please be Patient, This May Take a While\n'
        for content in contents:
            url_request = url_input+'/'+content
            url = urllib2.Request('http://'+url_request)
            try:
                request = urllib2.urlopen(url)
            except urllib2.HTTPError as e:
                if e.code == 401:
                    adminPageFound.append('http://'+url_request)
                else:
                    ++adminPageNotFound
            except urllib2.URLError:
                pass
            else:
                if request.url == url_request:
                    adminPageFound.append('http://'+request.url)
                else:
                    ++adminPageNotFound

        print G+'[!] Admin Pages Found: '+str(len(adminPageFound))

        for page in adminPageFound:
            print lB+'\n[+] '+ page

# Validation of url
def validateUrl():
    url_input = str(raw_input(P+"[+] Please Enter a Site:: "+B))
    url = urllib2.Request('http://'+url_input)
    try:
        request = urllib2.urlopen(url)
    except urllib2.URLError:
        print lR+"Please Enter a Valid URL(www.example.com)"
        validateUrl()
    else:
        return url_input

# Select a Choice
def selectChoice(url_input):
    print G+"\n[-] 1) Whois Lookup"
    print G+"[-] 2) DNS Lookup"
    print G+"[-] 3) IP Reverse Lookup"
    print G+"[-] 4) Admin Panel Finder\n"

    option_input = raw_input(P+"[+] Please Enter a Choice Separated With Comma(1,2,3) or 0 for all:: "+B)
    options_selected = []
    option_input = option_input.split(',')

    for option in option_input:
        option = int(option)
        if option not in (0,1,2,3,4):
            print lR+"[!] Option "+str(option)+" is Wrong."
            selectChoice(url_input)
        options_selected.append(option)

    if len(options_selected) == 1 and options_selected[0] == 0:
        whois(url_input)
        dnsLookup(url_input)
        ipReverse(url_input)
        adminFinder(url_input)
    else:
        for option in options_selected:
            if option == 1:
                whois(url_input)
            elif option == 2:
                dnsLookup(url_input)
            elif option == 3:
                ipReverse(url_input)
            elif option == 4:
                adminFinder(url_input)

def main():
    print '\n'
    print B+"             _                                ___  "
    print B+" __      __ | |__     ___      _   _   _ __  |__ \ "
    print B+" \ \ /\ / / | '_ \   / _ \    | | | | | '__|   / / "
    print B+"  \ V  V /  | | | | | (_) |   | |_| | | |     |_|  "
    print B+"   \_/\_/   |_| |_|  \___/     \__,_| |_|     (_)  "
    print '\n'
    print lC+"Beta 1.0                                       JopCode"
    print '\n'

    url_input = validateUrl()

    selectChoice(url_input)

    print lG+"\n---------"
    print lG+"- C Y A -"
    print lG+"---------\n"
    print lR+"[+] Script by JopCode\n"

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print lG+"\n---------"
        print lG+"- C Y A -"
        print lG+"---------\n"
        print lR+"[+] Script by JopCode\n"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
