# Simple Port Scanner

import os
import time
import argparse
import socket

from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

N_THREADS = 200               
q = Queue()                            
print_lock = Lock()

def port_scan(port):                       
    try:
        s = socket.socket()
        s.connect((targetIP, port))
    except:
        with print_lock:
             print(f"{GRAY}{targetIP:15}:{port:5} is closed  {RESET}", end="\r")

    else:
        with print_lock:
            print(f"{GREEN}{targetIP:15}:{port:5} is open  {RESET}")

    finally:
        s.close()

def scan_thread():                          
    global q
    while True:
        worker = q.get()                       
        port_scan(worker)
        q.task_done()

def main(targetIP, ports):
    global q
    for t in range(N_THREADS):                      
        t = Thread(target=scan_thread)
        t.deamon = True                         
        t.start()                               

    for worker in ports:                        
            q.put(worker)
                                             
    q.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple port scanner")  
    parser.add_argument("targetIP", help="targetIP to scan.")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
    args = parser.parse_args()
    targetIP, port_range = args.targetIP, args.port_range

    startPort, endPort = port_range.split("-")                    
    startPort, endPort = int(startPort), int(endPort)

    ports = [ p for p in range(startPort, endPort)]

    main(targetIP, ports)