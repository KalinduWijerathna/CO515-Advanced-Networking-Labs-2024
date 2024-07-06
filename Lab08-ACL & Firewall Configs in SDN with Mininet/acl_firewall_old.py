# Import necessary POX modules
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.addresses import IPAddr

# Logger for outputting information and debug messages
log = core.getLogger()

# Define Access Control List (ACL) rules
acl_rules = [
    {'src_ip': IPAddr("10.0.0.1"), 'action': 'permit'},  # Allow traffic from h1
    {'src_ip': IPAddr("10.0.0.2"), 'action': 'deny'},    # Deny traffic from h2
    {'src_ip': IPAddr("10.0.0.3"), 'action': 'permit'},  # Allow traffic from h3
    
]

class ACLFirewall(object):
    def __init__(self):
        # Add listeners for OpenFlow events
        core.openflow.addListeners(self)
        # Dictionary to store MAC to port mappings for each switch
        self.mac_to_port = {}

    def _handle_ConnectionUp(self, event):
        # Log when a switch connects to the controller
        log.info("Switch %s has connected", event.dpid)
        # Set the table-miss flow entry to send unknown packets to the controller
        self.set_table_miss_flow(event.connection)

    def set_table_miss_flow(self, connection):
        # Create a flow mod message to set the table-miss entry
        msg = of.ofp_flow_mod()
        msg.priority = 0  # Lowest priority for table-miss flow
        msg.match = of.ofp_match()  # Match all packets
        # Action to send packets to the controller
        msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
        connection.send(msg)
        log.info("Set table-miss flow on switch %s", connection.dpid)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            # Log and ignore incomplete packets
            log.warning("Ignoring incomplete packet")
            return

        # Update MAC to port mapping for the switch
        self.mac_to_port[event.dpid] = self.mac_to_port.get(event.dpid, {})
        self.mac_to_port[event.dpid][packet.src] = event.port

        # Check if the packet is an IPv4 packet
        ipv4_packet = packet.find('ipv4')
        if ipv4_packet:
            # Apply ACL rules to the IPv4 packet
            if self.apply_acl_rules(ipv4_packet):
                log.info("Dropping packet from %s", ipv4_packet.srcip)
                return

        # If the packet is not dropped, flood it to all ports
        self.flood_packet(event, packet)

    def apply_acl_rules(self, ipv4_packet):
        # Check if the IPv4 packet matches any deny rules in the ACL
        for rule in acl_rules:
            if ipv4_packet.srcip == rule['src_ip'] and rule['action'] == 'deny':
                return True
        # Permit by default if no deny rule matches
        return False

    def flood_packet(self, event, packet):
        # Create a packet out message to flood the packet to all ports
        msg = of.ofp_packet_out()
        msg.data = event.ofp  # Use the original packet data
        # Add action to flood the packet
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("Flooding packet from %s", packet.src)

def launch():
    # Register the ACLFirewall class with the POX core
    core.registerNew(ACLFirewall)
    log.info("ACL Firewall module running")

