import subprocess
import re
from ipwhois import IPWhois

def trace_route(target):
    result = subprocess.run(['tracert', target], capture_output=True, text=True)
    return result.stdout

def extract_ips(traceroute_output):
    ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
    return ip_pattern.findall(traceroute_output)

def get_as_number(ip):
    try:
        ip_info = IPWhois(ip)
        as_info = ip_info.lookup_whois()
        return as_info['asn']
    except Exception:
        return None

def main():
    target = input("Введите доменное имя или IP адрес: ")
    traceroute_output = trace_route(target)
    ip_addresses = extract_ips(traceroute_output)

    print("Number         IP           AS")
    print("*******************************")

    for idx, ip in enumerate(ip_addresses, start=1):
        if "***" in ip:
            break
        as_number = get_as_number(ip)
        print(f"{idx}       {ip}      {as_number if as_number else '---'}")

if __name__ == "__main__":
    main()
