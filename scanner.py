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

  if args.tcp:
    create_live_servers.create_multiple(args.create[0])
  elif args.udp:
    create_live_servers.create_one(args.create_one[0])
  elif args.ping:
    delete_live_servers.delete_multiple()
  elif args.trace:
    delete_live_servers.delete_one(args.delete_one[0])
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
    if user_choice == "1":
      webscanner.menu("tcp")
    elif user_choice == "2":
      delete_live_servers.menu()
    elif user_choice == "3":
      admin_tools.menu("enter")
    elif user_choice == "4":
      admin_tools.menu("move")
    else:
      exit()
  else:
    raise Exception("Invalid arguments were chosen.")
    exit()
    
  
  
