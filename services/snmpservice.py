import subprocess
from dotenv import load_dotenv,dotenv_values
from pathlib import Path
import re
pathenv = Path('../.env')
load_dotenv(dotenv_path=pathenv)
config = dotenv_values()

def extract_value(output):
    # Regular expressions for extracting values
    string_pattern = re.compile(r'=\s*STRING:\s*"([^"]+)"')
    gauge_pattern = re.compile(r'=\s*Gauge32:\s*(\d+)')
    
    # Try to match STRING pattern
    match = string_pattern.search(output)
    if match:
        return match.group(1)
    
    # Try to match Gauge32 pattern
    match = gauge_pattern.search(output)
    if match:
        return match.group(1)
    
    # Return raw output if no pattern matched
    return output

def snmpwalk(ip, community, oid):
    command = f"snmpwalk -v 2c -c {community} {ip} {oid}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

# Router details
router_ip = config.get('ROUTER_IP') or "localhost"  # Replace with the router's IP address
community = config.get('COMMUNITY') or "public"  # Replace with your community string

oids = [
    {
    "name":"router_name",
    "oid":"1.3.6.1.2.1.1.5"
},
    {
    "name":"interface_names",
    "oid":"1.3.6.1.2.1.2.2.1.2"
},
    {
    "name":"bandwidth",
    "oid":"1.3.6.1.2.1.2.2.1.5"
},
       ]
def show_snmpwalk():
    for item in oids:
        name = item["name"]
        oid_value = item["oid"]
        result = snmpwalk(router_ip, community, oid_value)
        format_result = extract_value(result)
        print(f"\n{name.replace('_', ' ').title()}: {format_result}")