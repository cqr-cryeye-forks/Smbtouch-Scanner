import os
import fileinput
import argparse
import json
import pathlib
from typing import Final

OLD_IP = '      <value>127.0.0.1</value>'
TEMP_IP = OLD_IP


def update_xml(ip, old_ip, new_ip):
    for line in fileinput.input('Smbtouch-1.1.1.xml', inplace=True):
        print(line.rstrip().replace(old_ip, new_ip))


def run_scan(ip):
    command = r"Smbtouch-1.1.1.exe"
    output = os.popen(command).read()
    output = output.split('<config', 1)[0]
    return output


def main(target_ip, output_file):
    results = {}
    new_ip = f'      <value>{target_ip}</value>'
    update_xml(target_ip, TEMP_IP, new_ip)

    try:
        output = run_scan(target_ip)
        results[target_ip] = "Touch success" if '[-] Touch failed' not in output else "Touch failed"
        print(
            f"[+] Touch success: {target_ip}" if '[-] Touch failed' not in output else f"[-] Touch failed: {target_ip}")
    finally:
        update_xml(target_ip, new_ip, OLD_IP)

    with open(output_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automatically scan the target IP using Smbtouch.exe')
    parser.add_argument('--target', type=str, required=True, help='Target IP address to scan')
    parser.add_argument('--output', type=str, required=True, default='data.json',
                        help='Output file to save the results in JSON format')
    args = parser.parse_args()

    OUTPUT_JSON: Final[pathlib.Path] = pathlib.Path(__file__).parent / args.output

    main(args.target, OUTPUT_JSON)
