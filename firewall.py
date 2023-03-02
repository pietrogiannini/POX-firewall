from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv
from csv import DictReader
from pox.lib.util import str_to_bool
import time

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall_policy.csv" % os.environ['HOME']


class Firewall(EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)

        self.mac_couples = []  # Data structure to save rules as MAC address couples
        with open(policyFile, 'r') as rules:  # Reading policy file
            reader = csv.DictReader(rules)

            for row in reader:  # Storing rules in the data structure
                self.mac_couples.append((EthAddr(row['mac_0']), EthAddr(row['mac_1'])))
                self.mac_couples.append((EthAddr(row['mac_1']), EthAddr(row['mac_0'])))

        log.debug("Enabling Firewall Module")

    # This method is called every time a connection between an
    # OpenFlow switch and the controller is established
    def _handle_ConnectionUp(self, event):

        # Iterate through mac_couples, for each pair install a rule on each switch
        for (src, dst) in self.mac_couples:  # Turn each couple into a rule
            # Set of headers for packets to match against if MAC addresses correspond
            match = of.ofp_match()  # Create a match
            match.dl_src = src  # Source MAC address
            match.dl_dst = dst  # Destination MAC address
            log.debug("~~> Source Mac is %s", match.dl_src)
            log.debug("~~> Destination Mac is %s", match.dl_dst)

            # An OpenFlow message is sent to the switch, instructing it to install the
            # rules in its flow table, blocking incoming packets with matching fields
            msg = of.ofp_flow_mod()  # OpenFlow message to install a flow on a switch
            msg.priority = 20  # Set message priority to avoid conflict with the learning bridge setup
            msg.match = match
            event.connection.send(msg)  # Send instruction to switch

        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))


def launch():
    print("Starting the Firewall module")
    core.registerNew(Firewall)
