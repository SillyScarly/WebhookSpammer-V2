from concurrent.futures import thread
import os
import threading
import time
import sys
import random

import requests
from colorama import Fore


webhooks = open("webhooks.txt", "r").read().split("\n")

proxies = open("proxy.txt", "r").read().split("\n")

os.system('cls & title SillyScarlys Webhook Spammer')

message = input(Fore.RED + "Message to Spam: ")
ratelimit = int(input("how many messages per second: "))
tospam = int(input("how many messages to spam: "))
hthreads = int(input("how many threads to use: "))

global newset
newset = set()

def control():
    global newset
    newstring = str(random.randint(1,4000))
    newset.add(newstring)
    time.sleep(1.3)
    newset.remove(newstring)
    

global threadkill
threadkill = False


def spam(message):
    global newset
    global spammed
    global threadkill
    cc = 0
    while True:
        if threadkill:
            break
        if len(newset) >= ratelimit:
            time.sleep(0.5)
            continue
        try:
            https_proxy = str(random.choice(proxies)).rstrip()

            proxies = { 
                  "https" : "https://"+https_proxy, 
                }
            web = random.choice(webhooks)
            if cc>= spammed:
                break
            cc+=1
            r = requests.post(web, json={"content": message}, proxies=proxies)
            s = [200, 201, 204]
            if r.status_code in s:
                print(Fore.GREEN + f"Sent Message > {message}")
                threading.Thread(target=control).start()
            elif r.status_code == 429:
                b = r.json()
                print(Fore.RED + f"Ratelimited, retrying in 10 seconds")
                time.sleep(2)

        except KeyboardInterrupt:
            threadkill = True
            break

        except:
            print("error with | "+web)
            break

def spamming():
    for i in range(hthreads):
        threading.Thread(target=spam, args=(message,)).start()

global spammed
spammed = tospam


spamming()

while True:
    try:
        time.sleep(0.00011)
    except KeyboardInterrupt:
        threadkill = True
        break
