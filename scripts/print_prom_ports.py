"""Print the Prometheus endpoint ports of all border routers of a given AS.

Usage: manage.py runscript print_prom_ports --script-args <ASN>
"""

from scionlab.defines import BR_PROM_PORT_OFFSET
from scionlab.models.core import BorderRouter


def run(*args):
    if len(args) < 1:
        print("Specify an ASN.")
        return

    for br in BorderRouter.objects.filter(AS__as_id=args[0]):
        print(br.internal_port + BR_PROM_PORT_OFFSET)
