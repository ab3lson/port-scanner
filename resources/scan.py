import socket
import subprocess
from datetime import datetime
import logging
import shlex
from scapy.all import *

logger = logging.getLogger("scan.py")
start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def tcp(ips, ports):
  logger.info(f"{'='*5} {start_time} - Starting TCP Scan {'='*5}")
  for target in ips:
    logger.info(f"Scanning: {target}")
    found = False
    filtered_list = []
    for port in ports:
      try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(.5)
        result = sock.connect((target, int(port)))
        logger.debug(f"Port {port} returned: {result}")
        if result == None: 
          logger.info(f"\t[+] Port {port} is open")
          found = True
        else: logger.debug(f"\t[-] Port {port} is closed.")
        sock.close()
      except Exception as e:
        logger.debug(f"[-] Port {port} is closed. Connection Error: {e}")
        if "Connection refused" in str(e):
          filtered_list.append(port)
    if len(ports) == len(filtered_list):
      found = True
      logger.info(f"\t[-] All ports are filtered")
    elif len(filtered_list) != 0:
      found = True
      for port in filtered_list:
        logger.info(f"\t[+] Port {port} is filtered")
    elif not found: logger.info(f"\t[-] No open ports were found")

def udp(ips, ports):
  logger.info(f"{'='*5} {start_time} - Starting UDP Scan {'='*5}")
  for target in ips:
    logger.info(f"Scanning: {target}")
    found = False
    for port in ports:
      try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(.5)
        result = sock.connect((target, int(port)))
        if result == None: 
          logger.info(f"\t[+] Port {port} is open")
          found = True
        else: logger.debug(f"\t[-] Port {port} is closed.")
      except Exception as e:
        if "Connection refused" in str(e):
          found = True
          logger.info(f"\t[+] Port {port} is filtered")
        elif "No route to host" in str(e):
          logger.debug(f"\t[-] Port {port}: {str(e)}")
        elif "timed out" not in str(e):
          found = True
          logger.info(f"\t[+] Port {port} is up")
        else:
          logger.debug(f"[-] Port {port} is closed. Connection Error: {e}")
    if not found: logger.info(f"\t[-] No open ports were found")

def ping(ips):
  logger.info(f"{'='*5} {start_time} - Starting Ping Scan {'='*5}")
  for target in ips:
    logger.debug(f"Scanning: {target}")
    found = False
    cmd = f"ping -c 1 -w 3 {target}"
    result = subprocess.call(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result == 0:
      try:
        logger.info(f"Scanning: {target}\n\t[+] {socket.gethostbyaddr(target)} ({target}) is up")
      except:
        logger.info(f"Scanning: {target}\n\t[+] {target} is up")
      found = True
    else: logger.debug(f"\t[-] {target} is down")

def trace(ips):
  logger.info(f"{'='*5} {start_time} - Starting Traceroute Scan {'='*5}")
  for target in ips:
    logger.info(f"{'='*5} {start_time} - Traceroute for {target} {'='*5}")
    try:
      hostname, *_ = socket.gethostbyaddr(target)
      for i in range(1, 28):
        pkt = IP(dst=hostname, ttl=i) / UDP(dport=33434)
        # Send the packet and get a reply
        reply = sr1(pkt, verbose=0)
        if reply is None:
            break
        elif reply.type == 3:
            # We've reached our destination
            logger.info(f"\t[+] Done! {reply.src}")
            break
        else:
            # We're in the middle somewhere
            logger.info(f"\t[+] {i} hops away: {reply.src}")
    except Exception as e:
      logger.error(f"\t[-] Couldn't get hostname for {target}: Skipping traceroute. {e}")
 

if __name__ == '__main__':
   target = input('Enter the host to be scanned: ')
