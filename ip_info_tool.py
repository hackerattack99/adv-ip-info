import os
import sys
import requests
import socket
from rich.console import Console
from rich.table import Table
from colorama import Fore, init, Style

# Set a timeout value (Fix for NameError)
DEFAULT_TIMEOUT = 5  # Timeout in seconds

init(autoreset=True)
console = Console()

def banner():
    console.print(f"""
{Fore.GREEN}=============================================
          Hacker.Tools.Kail - IP Information
             Version: 1.02 | Owner: hackerattack99
============================================={Style.RESET_ALL}
""")

def resolve_domain(domain):
    """Converts a domain name to its corresponding IP address."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        console.print(f"{Fore.RED}[!] Error: Unable to resolve domain {domain}.{Style.RESET_ALL}")
        sys.exit(1)

def get_ip_info(ip):
    """Fetches IP information from ip-api.com"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=DEFAULT_TIMEOUT)
        data = response.json()
        if response.status_code == 200 and data.get('status') == 'success':
            lat = data.get('lat')
            lon = data.get('lon')
            if lat and lon:
                data['map_link'] = f"https://www.google.com/maps?q={lat},{lon}"
            return data
        else:
            console.print(f"{Fore.RED}[!] Failed to retrieve IP information.{Style.RESET_ALL}")
            return None
    except requests.RequestException as e:
        console.print(f"{Fore.RED}[!] Error retrieving IP information: {e}{Style.RESET_ALL}")
        return None

def display_ip_info(ip_info):
    """Displays IP information in a formatted table."""
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Key", style="bold white", justify="left", min_width=15)
    table.add_column("Value", style="bold yellow", justify="left", min_width=50)

    for key, value in ip_info.items():
        table.add_row(str(key), str(value))

    console.print(table)

    if 'map_link' in ip_info:
        console.print(f"\n{Fore.YELLOW}[+] View location on map: {ip_info['map_link']}{Style.RESET_ALL}")

def main(target):
    banner()
    console.print(f"{Fore.WHITE}[*] Fetching IP info for: {target}{Style.RESET_ALL}")

    # Convert domain to IP if needed
    if not target.replace('.', '').isdigit():  
        target = resolve_domain(target)

    ip_info = get_ip_info(target)

    if ip_info:
        display_ip_info(ip_info)
    else:
        console.print(f"{Fore.RED}[!] No IP information found.{Style.RESET_ALL}")

    console.print(f"{Fore.CYAN}[*] IP info retrieval completed.{Style.RESET_ALL}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        main(target)
    else:
        console.print(f"{Fore.RED}[!] No target provided. Please pass a domain, URL, or IP address.{Style.RESET_ALL}")
        sys.exit(1)
