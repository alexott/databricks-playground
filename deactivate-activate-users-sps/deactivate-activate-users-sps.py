import logging

from databricks.sdk import WorkspaceClient
import argparse
import json
import os

from databricks.sdk.service.iam import Patch, PatchSchema, PatchOp

default_file_name = "deactivated_users.json"
default_schemas = [PatchSchema.URN_IETF_PARAMS_SCIM_API_MESSAGES_2_0_PATCH_OP]

def find_non_admin_users_sps(wc: WorkspaceClient):
    admin_users = set()
    admin_sps = set()
    res = list(wc.groups.list(attributes="members", filter="displayName eq \"admins\""))
    if not res:
        raise Exception("Can't find 'admins' group")
    for member in res[0].members:
        if member.ref.startswith("Users/"):
            admin_users.add(member.value)
        elif member.ref.startswith("ServicePrincipals/"):
            admin_sps.add(member.value)

    users_to_deactivate = []
    attrs = "id,displayName,userName,active"
    all_active_users = wc.users.list(attributes=attrs, filter="active eq true")
    for user in all_active_users:
        if user.id not in admin_users:
            users_to_deactivate.append({"id": user.id, "display_name": user.display_name, "user_name": user.user_name})

    sps_to_deactivate = []
    all_active_sps = wc.service_principals.list(attributes=attrs, filter="active eq true")
    for sp in all_active_sps:
        if sp.id not in admin_sps:
            sps_to_deactivate.append({"id": sp.id, "display_name": sp.display_name,
                                      "application_id": sp.application_id})

    return {"users": users_to_deactivate, "service_principals": sps_to_deactivate}


def make_patch_op(active: bool):
    return [Patch(op=PatchOp.REPLACE, path="active", value=[
        {
            "value": active
        }
    ])]


def switch_user_active_status(wc: WorkspaceClient, user_id: str, active: bool):
    wc.users.patch(user_id, schemas=default_schemas, operations=make_patch_op(active))


def switch_sp_active_status(wc: WorkspaceClient, sp_id: str, active: bool):
    wc.service_principals.patch(sp_id, schemas=default_schemas, operations=make_patch_op(active))


def scan_identities_to_deactivate(wc: WorkspaceClient):
    identities = find_non_admin_users_sps(wc)
    users = identities['users']
    sps = identities['service_principals']
    print(f"Found {len(users)} users and {len(sps)} service principals.")
    print("Users:")
    for user in users:
        print(f"\tSCIM ID: {user['id']}, Display Name: {user['display_name']}, User Name: {user['user_name']}")
    print("\nService Principals:")
    for sp in sps:
        print(f"\tSCIM ID: {sp['id']}, Display Name: {sp['display_name']}, Application ID: {sp['application_id']}")


def deactivate_users_sps(wc: WorkspaceClient, fname: str, verbose: bool):
    print("Deactivating users and service principals...")
    identities = find_non_admin_users_sps(wc)
    users = identities['users']
    sps = identities['service_principals']
    print(f"Found {len(users)} users and {len(sps)} service principals.")
    with open(args.file, "w") as f:
        json.dump(identities, f, indent=2)

    switch_users_status(wc, users, False, verbose)
    switch_sps_status(wc, sps, False, verbose)

    print(f"All users & SPs are deactivated. The list of identities is saved in {fname}")


def switch_sps_status(wc: WorkspaceClient, sps: list, active: bool, verbose: bool):
    for sp in sps:
        switch_sp_active_status(wc, sp['id'], active)
        if verbose:
            status = "Reactivated" if active else "Deactivated"
            print(
                f"{status} service principal '{sp['display_name']} ({sp['application_id']})' with SCIM ID {sp['id']}")


def switch_users_status(wc: WorkspaceClient, users: list, active: bool, verbose: bool):
    for user in users:
        switch_user_active_status(wc, user['id'], active)
        if verbose:
            status = "Reactivated" if active else "Deactivated"
            print(f"{status} user '{user['display_name']} ({user['user_name']})' with SCIM ID {user['id']}")


def reactivate_users_sps(wc: WorkspaceClient, fname: str, verbose: bool):
    print(f"Activating users/SPs from {fname}")
    with open(args.file, "r") as f:
        identities = json.load(f)

    users = identities['users']
    sps = identities['service_principals']
    print(f"Loaded {len(users)} users and {len(sps)} service principals.")
    switch_users_status(wc, users, True, verbose)
    switch_sps_status(wc, sps, True, verbose)
    print(f"Users/SPs are reactivated. Removing {fname}...")
    os.remove(fname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deactivate or reactivate Databricks users and service principals')
    supported_commands = ['scan', 'deactivate', 'reactivate']
    parser.add_argument('command', choices=supported_commands)
    parser.add_argument('--file', default=default_file_name,
                        help=f'File to store deactivated users/SPs (default: {default_file_name})')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()
    if args.command not in supported_commands:
        print(f"Unknown command {args.command}")
        exit(1)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    client = WorkspaceClient()
    if args.command == 'scan':
        scan_identities_to_deactivate(client)
    elif args.command == 'deactivate':
        deactivate_users_sps(client, args.file, args.verbose)
    elif args.command == 'reactivate':
        reactivate_users_sps(client, args.file, args.verbose)


