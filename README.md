# POX-firewall

Firewall implementation for Software Defined Network controller POX. 

The network has been emulated with Mininet and a custom test topology is provided. 
However, the firewall is unrelated to the net and should work in any POX controlled SDN.

## Setup

Install Mininet and POX.

Move the custom topology file in the `mininet/custom` directory.

Move the firewall and policy files in the `pox/pox/misc` directory.

## Running the simulation

To run the simulation, open two terminal windows.

In the first one, run the POX controller

```bash
~/pox$ ./pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning misc.firewall
```

In the second one, run the custom topology with Mininet

```bash
~/custom$ python3 customTopo.py --switch ovsk --controller remote
```

To test the firewall run the command `mininet> pingall` in the miniet CLI. 
Each host will start pinging the others, except for the ones with MAC addresses matching the firewall rules.
