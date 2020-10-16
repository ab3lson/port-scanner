#!/usr/bin/python3

import argparse
import os
import sys
import logging
from resources import *

class color:
  PURPLE = '\033[95m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  RESET = '\033[00m'

def main_menu(menu_options):
  print(f"""
███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
{color.YELLOW}Optional{color.RESET}: Use with -h or --help for command line arguments""")

  for i, option in enumerate(menu_options):
    if i %2 == 0: print("")
    print(f"{color.BLUE}[{i + 1}]{color.RESET} {menu_options[i]:<16s}", end='')
  print("\n")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog='scanner.py', description="Port scanner for IT 567.")
  tools = parser.add_argument_group("Ping scans").add_mutually_exclusive_group()
  scans = parser.add_argument_group("Port scans").add_mutually_exclusive_group()

  parser.add_argument('-v', '--verbose', action='count', default=0, help='-v,-vv supported for increased verbosity')
  parser.add_argument('-p','--ports', type=str, action='store', metavar='PORTS', nargs=1, help='Ports to scan (Comma separated).')
  parser.add_argument('--top-ports', type=str, action='store', metavar='PORTS', nargs=1, help='Most common ports will be scanned (20 or 1000)')
  parser.add_argument('-o','--output', type=str, action='store', metavar='PATH', nargs=1, help='Path to output file to save the results.')
  scans.add_argument('-t','--tcp', type=str, action='store', metavar='IP', nargs=1, help='Conducts a TCP scan on the provided IP(s)')
  scans.add_argument('-u','--udp', type=str, action='store', metavar='IP', nargs=1, help='Conducts a UDP scan on the provided IP(s)')
  tools.add_argument('-P','--ping', type=str, action='store', metavar='IP', nargs=1, help='Conducts a ping scan on the provided IP(s)')
  tools.add_argument('-T','--trace', type=str, action='store', metavar='IP', nargs=1, help='Conducts a traceroute on the provided IP.')

  args = parser.parse_args()
  if ((args.tcp or args.udp) and (args.ports is None and args.top_ports is None)):
    parser.error("TCP/UDP scans require --ports or --top-ports.")
  levels = [logging.WARNING, logging.INFO, logging.DEBUG]
  level = levels[min(len(levels)-1,args.verbose)]  # capped to number of levels


  if args.top_ports:
    if args.top_ports[0] not in ['20', '1000']:
      parser.error("--top-ports must be 20 or 1000.")
  root = logging.getLogger()
  root.setLevel(logging.DEBUG)
  console = logging.StreamHandler(sys.stdout)
  console.setLevel(level)
  if args.verbose >= 2:
    console.setFormatter(logging.Formatter("%(name)-12s %(levelname)-8s: %(message)s"))
  elif args.verbose == 1:
    console.setFormatter(logging.Formatter("%(asctime)-15s: %(message)s"))
  else:
    console.setFormatter(logging.Formatter("%(message)s"))
  root.addHandler(console)

  if args.output:
    output_file = logging.FileHandler(args.output[0], 'w+')
    output_file.setLevel(logging.INFO)
    output_file.setFormatter(logging.Formatter("%(message)s"))
    root.addHandler(output_file)
  
  logging.debug(args) #prints the supplied arguments

  if args.ports:
    args.ports[0] = input_parser.parse_ports(args.ports[0])
    logging.debug(f"Scanning Ports: {args.ports[0]}")
  if args.top_ports:
    args.ports = ['']
    if args.top_ports[0] == '1000':
      args.ports[0] = input_parser.parse_ports(variables.top_1000_ports)
    elif args.top_ports[0] == '20':
      args.ports[0] = input_parser.parse_ports(variables.top_20_ports)
    logging.debug(f"Scanning Ports: {args.ports[0]}")
  if args.tcp:
    args.tcp[0] = input_parser.parse_ips(args.tcp[0])
    logging.debug(f"Running TCP Scan for IPs: {args.tcp[0]}")
    scan.tcp(args.tcp[0], args.ports[0])
  elif args.udp:
    args.udp[0] = input_parser.parse_ips(args.udp[0])
    logging.debug(f"Running UDP Scan for IPs: {args.udp[0]}")
    scan.udp(args.udp[0], args.ports[0])
  elif args.ping:
    args.ping[0] = input_parser.parse_ips(args.ping[0])
    logging.debug(f"Running ICMP Scan for IPs: {args.ping[0]}")
    scan.ping(args.ping[0])
  elif args.trace:
    args.trace[0] = input_parser.parse_ips(args.trace[0])
    logging.debug(f"Running Traceroute for IPs: {args.trace[0]}")
    scan.trace(args.trace[0])
  elif len(sys.argv) < 2 or args.verbose or args.output:
    #more options can be created in main menu by appending to this array
    menu_options = ["TCP Scan", "UDP Scan", "Ping Scan", "Traceroute"]
    main_menu(menu_options) #prints main menu
    user_choice = input("Pick an action: ")
    try:
      if not 0<int(user_choice)<len(menu_options)+1:
        logging.error("Invalid input.")
        exit()
    except: #Fails if user input is not an int
      logging.error("Invalid input.")
      exit()
    ips, ports = input_parser.menu() #prompts user to input ip and port ranges for scans and returns lists
    if user_choice == "1":
      scan.tcp(ips, ports)
    elif user_choice == "2":
      scan.udp(ips, ports)
    elif user_choice == "3":
      scan.ping(ips,)
    elif user_choice == "4":
      scan.trace(ips)
    else:
      exit()
  else:
    parser.error("Invalid argument.")
    exit()
    
  
  
