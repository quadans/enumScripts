# network tools for 
import requests           # from http requests
import sys                # sys argv
import socket   # port scanner 
import pyfiglet # banner
import hashlib  # hash cracking
import keyboard # keylogger
from scapy.all import *   # arp network scan

# Intro
ascii_banner = pyfiglet.figlet_format("Werkzeuge")
print(ascii_banner)

print("\n")

print("Press number to select option:\n")
print("1. Subdomain enumeration\n")
print("2. Directory enumeration\n")
print("3. Local network enumeration\n")
print("4. Port scanner\n")
print("5. Download files\n")
print("6. Hash cracker\n")
print("7. keylogger")


# subdomains check
sub_list = open("subdomains.txt").read() 
subdoms = sub_list.splitlines()

for sub in subdoms:
    sub_domains = f"http://{sub}.{sys.argv[1]}" 

    try:
        requests.get(sub_domains)
    
    except requests.ConnectionError: 
        pass
    
    else:
        print("Valid domain: ",sub_domains)   


# dir enum
sub_list = open("wordlist.txt").read() 
directories = sub_list.splitlines()

for dir in directories:
    dir_enum = f"http://{sys.argv[1]}/{dir}.html" 
    r = requests.get(dir_enum)
    if r.status_code==404: 
        pass
    else:
        print("Valid directory:" ,dir_enum)

# local network enum

interface = "eth0"
ip_range = "10.10.X.X/24"
broadcastMac = "ff:ff:ff:ff:ff:ff"

packet = Ether(dst=broadcastMac)/ARP(pdst = ip_range) 

ans, unans = srp(packet, timeout =2, iface=interface, inter=0.1)

for send,receive in ans:
        print (receive.sprintf(r"%Ether.src% - %ARP.psrc%"))

# port scanner
ip = '192.168.1.6' 
open_ports =[] 

ports = range(1, 65535)

def probe_port(ip, port, result = 1): 
  try: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.settimeout(0.5) 
    r = sock.connect_ex((ip, port))   
    if r == 0: 
      result = r 
    sock.close() 
  except Exception as e: 
    pass 
  return result


for port in ports: 
    sys.stdout.flush() 
    response = probe_port(ip, port) 
    if response == 0: 
        open_ports.append(port) 

if open_ports: 
  print ("Open Ports are: ") 
  print (sorted(open_ports)) 
else: 
  print ("Looks like no ports are open :(")

# download files
url = 'https://download.sysinternals.com/files/PSTools.zip'
r = requests.get(url, allow_redirects=True)
open('PSTools.zip', 'wb').write(r.content)

# hash cracker
wordlist_location = str(input('Enter wordlist file location: '))
hash_input = str(input('Enter hash to be cracked: '))

with open(wordlist_location, 'r') as file:
    for line in file.readlines():
        hash_ob = hashlib.md5(line.strip().encode())
        hashed_pass = hash_ob.hexdigest()
        if hashed_pass == hash_input:
            print('Found cleartext password! ' + line.strip())
            exit(0)

# keylogger
keys = keyboard.record(until ='ENTER')
keyboard.play(keys)
