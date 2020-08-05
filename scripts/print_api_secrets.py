"""Print all host IDs and secrets for use with the coordinator's API.

Usage: manage.py runscript print_api_secrets
"""

from scionlab.models.core import Host

def run():
    for host in Host.objects.all():
        print(host.AS.isd_as_str(), host.uid, host.secret)
