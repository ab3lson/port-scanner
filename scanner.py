#!/usr/bin/python3

import argparse
import os
import sys
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

  parser.add_argument('-t','--tcp', type=str, action='store', metavar='IP', nargs=1, help='Conducts a TCP scan on the provided IP(s)')
  parser.add_argument('-u','--udp', type=str, action='store', metavar='IP', nargs=1, help='Conducts a UDP scan on the provided IP(s)')
  parser.add_argument('-p','--ports', type=str, action='store', metavar='PORTS', nargs=1, help='Ports to scan (Comma separated).')
  parser.add_argument('-i','--input', type=str, action='store', metavar='PATH', nargs=1, help='Text file with csv of desired ports.')
  parser.add_argument('-o','--out', type=str, action='store', metavar='PATH', nargs=1, help='Path to output file to save the results.')
  tools.add_argument('-P','--ping', type=str, action='store', metavar='IP', nargs=1, help='Conducts a ping scan on the provided IP(s)')
  tools.add_argument('-T','--trace', type=str, action='store', metavar='IP', nargs=1, help='Conducts a traceroute on the provided IP.')


  args = parser.parse_args()
  print(args)
  if args.tcp:
    scan.tcp(args.tcp)
  elif args.udp:
    scan.udp(args.udp)
  elif args.ping:
    scan.ping(args.ping)
  elif args.trace:
    scan.trace(args.trace)
  elif len(sys.argv) < 2:
    #more options can be created in main menu by appending to this array
    menu_options = ["TCP Scan", "UDP Scan", "Ping Scan", "Traceroute"]
    main_menu(menu_options) #prints main menu
    user_choice = input("Pick an action: ")
    try:
      if not 0<int(user_choice)<len(menu_options)+1:
        print(f"{color.RED}[ERROR]{color.RESET} Invalid input.")
        exit()
    except: #Fails if user input is not an int
      print(f"{color.RED}[ERROR]{color.RESET} Invalid input.")
      exit()
    ips, ports = input_parser.menu() #prompts user to input ip and port ranges for scans and returns lists
    if user_choice == "1":
      scan.tcp(ips, ports)
    elif user_choice == "2":
      scan.udp(ips, ports)
    elif user_choice == "3":
      scan.ping(ips, ports)
    elif user_choice == "4":
      scan.trace(ips, ports)
    else:
      exit()
  else:
    raise Exception("Invalid arguments were chosen.")
    exit()
    
  
  
