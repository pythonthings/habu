#!/usr/bin/env python3

import ipaddress
import json
import logging

import click
import regex as re


def extract_ipv4(data):

    #regexp = re.compile(r'\s?((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\s?', flags=re.MULTILINE)
    regexp = re.compile(r'[\s():{}\[\]]{1}((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)[\s():{}\[\]]{1}', flags=re.MULTILINE)

    regexp = re.compile(r'[^0-9]?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[^0-9]?', flags=re.MULTILINE)

    match = regexp.finditer(data)

    result = []

    for m in match:
        try:
            ipaddress.ip_address(m.group(1))
            result.append(m.group(1))
        except ValueError:
            continue
        #ip = m.group(0).strip(' ():{}[]')
        #ip = ip.strip()
        #if ip:
        #    result.append(ip)

    return result

@click.command()
@click.argument('infile', type=click.File('r'), default='-')
@click.option('--json', 'jsonout', is_flag=True, default=False, help='JSON output')
@click.option('-v', 'verbose', is_flag=True, default=False, help='Verbose output')
def cmd_extract_ipv4(infile, jsonout, verbose):
    """Extract IPv4 addresses from a file or stdin.

    Example:

    \b
    $ cat /var/log/auth.log | habu.extract.ipv4
    172.217.162.4
    23.52.213.96
    190.210.43.70
    """

    if verbose:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    data = infile.read()

    result = extract_ipv4(data)

    if jsonout:
        print(json.dumps(result, indent=4))
    else:
        print('\n'.join(result))


if __name__ == '__main__':
    cmd_extract_ipv4()
