import argparse
from typing import List
import copy
import itertools

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.settings import IpAccessListInfo, ListType

import ipaddress


def process_lists(orig: List[IpAccessListInfo]) -> List[IpAccessListInfo]:
    lsts = copy.deepcopy(orig)

    all_ips = list(itertools.chain(*[l.ip_addresses for l in lsts]))
    uniq_ips = set(all_ips)
    if len(all_ips) != len(uniq_ips):
        print(f"There are duplicates in the list! len(all_ips)={len(all_ips)}, len(uniq_ips)={len(uniq_ips)}")

    for i in range(len(lsts)):
        l = lsts[i]
        print(f"Processing list: {l.label} ({l.list_id})")
        to_remove = []
        ip_addresses = l.ip_addresses
        # find duplicates inside the list
        if len(set(ip_addresses)) != len(ip_addresses):
            print("\tThere are duplicates in IP list, removing")
            print(f"\tOld list: {ip_addresses}")
            ip_addresses = list(set(ip_addresses))
            print(f"\tNew list: {ip_addresses}")

        # find duplicates & overlaps with other lists
        for l2 in lsts:
            if l2.list_id == l.list_id:
                continue
            dups = set(ip_addresses).intersection(l2.ip_addresses)
            if len(dups) > 0:
                print(f"\tFound intersection with list {l2.label}")
                if l2.list_type == ListType.BLOCK or (l.list_type == ListType.ALLOW):
                    print("Modifying current list...")
                    to_remove.extend(dups)

            # finding subranges
            for oip in l2.ip_addresses:
                if oip.find("/") == -1:
                    continue
                try:
                    oip_net = ipaddress.ip_network(oip)
                    for ip in ip_addresses:
                        if ip.find("/") == -1:
                            if ipaddress.ip_address(ip) in oip_net and l2.list_type == l.list_type:
                                print(f"{ip} is part of {oip} in '{l2.label}', removing...")
                                to_remove.append(ip)
                        else:
                            if oip_net.supernet_of(ipaddress.ip_network(ip)) and l2.list_type == l.list_type:
                                print(f"{ip} is subnet of {oip} in '{l2.label}', removing...")
                                to_remove.append(ip)
                except ValueError as ex:
                    print(f"\tWarn: Incorrect IP Address or Network: '{ex}'")

        # Find private & local IPs
        for ip in ip_addresses:
            try:
                if ip.find("/") == -1:
                    ip_addr = ipaddress.ip_address(ip)
                else:
                    ip_addr = ipaddress.ip_network(ip)
                if ip_addr.is_loopback or ip_addr.is_private:
                    print(f"\tWe can ignore {ip} because it's local or private...")
                    to_remove.append(ip)
            except ValueError as ex:
                print(f"\tWarn: Incorrect IP Address or Network: '{ip}': {ex}")

            # TODO: find subranges, in the list as well...

        if len(to_remove) > 0:
            print(f"\tRemoving from {l.label}: {to_remove}")
            for ip in set(to_remove):
                ip_addresses.remove(ip)

        lsts[i] = IpAccessListInfo(address_count=len(ip_addresses), list_type=l.list_type,
                                   list_id=l.list_id, label=l.label,
                                   ip_addresses=ip_addresses, enabled=l.enabled)

    return lsts


def apply_modifications(w: WorkspaceClient, make_changes: bool, orig: List[IpAccessListInfo],
                        new: List[IpAccessListInfo]):
    ol = dict([(l.list_id, l) for l in orig])
    for l in new:
        if len(l.ip_addresses) == 0:
            print(f"Going to remove list '{l.label}' ({l.list_id}) as it's empty")
            if make_changes:
                w.ip_access_lists.delete(l.list_id)
            continue
        old = ol[l.list_id]
        if len(l.ip_addresses) == len(old.ip_addresses):
            print(f"List '{l.label}' ({l.list_id}) isn't modified")
        else:
            print(f"Going to modify list '{l.label}' ({l.list_id})")
            print(f"\tfrom: {old}")
            print(f"\tto  : {l}")
            if make_changes:
                w.ip_access_lists.update(label=l.label, list_id=l.list_id, list_type=l.list_type,
                                         enabled=l.enabled, ip_addresses=l.ip_addresses)


def main():
    parser = argparse.ArgumentParser(description='Analyze and fix Databricks IP Access Lists')
    parser.add_argument('--apply', help="Do analysis and apply changes",
                        action='store_true', default=False)
    args = parser.parse_args()
    # print(args)
    if args.apply:
        print("Performing analysis & fixing issues...")
    else:
        print("Performing only analysis...")

    w = WorkspaceClient()
    print(f"Processing IP Access Lists for host {w.config.host}")

    ipls = list(w.ip_access_lists.list())
    new_ipls = process_lists(ipls)

    apply_modifications(w, args.apply, ipls, new_ipls)


if __name__ == '__main__':
    main()
