import socket
import subprocess
from datetime import datetime
import logging
import shlex

logger = logging.getLogger("scan.py")
start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def tcp(ips, ports):
  logger.info(f"{'='*5} {start_time} - Starting TCP Scan {'='*5}")
  for target in ips:
    logger.info(f"Scanning: {target}")
    found = False
    for port in ports:
      try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, int(port)))
        if result == 0: 
          logger.info(f"\t[+] Port {port} is open")
          found = True
        else: logger.debug(f"\t[-] Port {port} is closed")
        sock.close()
      except Exception as e: logger.debug(f"\tException: {e}")
    if not found: logger.info(f"\t[-] No open ports were found")

def ping(ips):
  logger.info(f"{'='*5} {start_time} - Starting Ping Scan {'='*5}")
  for target in ips:
    logger.info(f"Scanning: {target}")
    found = False
    cmd = f"ping -c 1 -w 3 {target}"
    result = subprocess.call(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result == 0: 
      logger.info(f"\t[+] {target} is alive")
      found = True
    else: logger.info(f"\t[-] {target} is dead")




if __name__ == '__main__':
   target = input('Enter the host to be scanned: ')
