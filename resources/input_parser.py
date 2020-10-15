from . import variables
import ipaddress
import logging

logger = logging.getLogger(__name__)

def parse_ips(ips):
  if "/" in ips:
    parsed = [str(ip) for ip in ipaddress.IPv4Network(ips)]
    return parsed
  elif "-" in ips:
    parsed = []
    temp_ips = []
    temp_ips2 = []
    temp_ips3 = []
    octets = ips.split(".")
    for enum, octet in enumerate(octets):
      if "-" in octet:
        first, last = octet.split("-")
        if enum == 0:
          for number in range(int(first),int(last)+1):
            temp_ips.append(str(number) + ".")
        elif enum == 1:
          for ip_template in temp_ips:
            for number in range(int(first),int(last)+1):
              temp_ips2.append(ip_template + str(number) + ".")
        elif enum == 2:
          for ip_template in temp_ips2:
            for number in range(int(first),int(last)+1):
              temp_ips3.append(ip_template + str(number) + ".")
        elif enum == 3:
          for ip_template in temp_ips3:
            for number in range(int(first),int(last)+1):
              parsed.append(ip_template + str(number))       
      else:
        if enum == 0:
          temp_ips.append(str(octet) + ".")
        elif enum == 1:
          for ip_template in temp_ips:
            temp_ips2.append(ip_template + str(octet) + ".")
        elif enum == 2:
          for ip_template in temp_ips2:
            temp_ips3.append(ip_template + str(octet) + ".")
        elif enum == 3:
          for ip_template in temp_ips3:
            parsed.append(ip_template + str(octet))
    return parsed
  elif "*" in ips:
    parsed = []
    temp_ips = []
    temp_ips2 = []
    temp_ips3 = []
    octets = ips.split(".")
    for enum, octet in enumerate(octets):
      if "*" in octet:
        if enum == 0:
          for number in range(1,256):
            temp_ips.append(str(number) + ".")
        elif enum == 1:
          for ip_template in temp_ips:
            for number in range(1,256):
              temp_ips2.append(ip_template + str(number) + ".")
        elif enum == 2:
          for ip_template in temp_ips2:
            for number in range(1,256):
              temp_ips3.append(ip_template + str(number) + ".")
        elif enum == 3:
          for ip_template in temp_ips3:
            for number in range(1,256):
              parsed.append(ip_template + str(number))       
      else:
        if enum == 0:
          temp_ips.append(str(octet) + ".")
        elif enum == 1:
          for ip_template in temp_ips:
            temp_ips2.append(ip_template + str(octet) + ".")
        elif enum == 2:
          for ip_template in temp_ips2:
            temp_ips3.append(ip_template + str(octet) + ".")
        elif enum == 3:
          for ip_template in temp_ips3:
            parsed.append(ip_template + str(octet))
    return parsed
  elif "," in ips:
    parsed = ips.replace(" ", "").split(",")
    return parsed
  else:
    return [ips]

def parse_ports(ports):
  parsed = []
  split = ports.replace(" ", "").split(",")
  for i, value in enumerate(split):
    if "-" in value:
      first, last = value.split("-")
      for number in range(int(first),int(last)+1):
            parsed.append(str(number))
    else: parsed.append(str(value))
  return parsed


def menu():
  ip_input = input("What IP address(s) do you want to scan?: ")
  port_input = input("What ports do you want to scan?: ")
  ips = parse_ips(ip_input)
  ports = parse_ports(port_input)  
  return ips, ports 

if __name__ == "__main__":
  menu("tcp")