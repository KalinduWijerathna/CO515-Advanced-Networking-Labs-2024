from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.arp import arp


# Get a logger for debugging
log = core.getLogger()

class SimpleRouter(object):
    def __init__(self, connection):
        self.connection = connection  # Save the connection to the switch
        connection.addListeners(self)  # Listen for events on this connection


    def _handle_PacketIn(self, event):
        """
        This function is called whenever a packet is received from the switch.
        """
        packet = event.parsed  # The parsed packet data
        in_port = event.port  # The port on which the packet was received

        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        # Handle ARP packets
        if packet.type == ethernet.ARP_TYPE:
            log.debug("Handling ARP packet")
            self._handle_arp(packet, in_port, event.ofp)
        # Handle IP packets
        elif packet.type == ethernet.IP_TYPE:
            log.debug("Handling IP packet")
            self._handle_static_routes(packet, in_port, event.ofp)
        else:
            log.debug("Ignoring non-IP/ARP packet type: %s", packet.type)

    def _handle_arp(self, packet, in_port, ofp):
         
         '''  Handle ARP packets
	 '''
        arp_packet = packet.payload
        if arp_packet.opcode == arp.REQUEST or arp_packet.opcode == arp.REPLY:
            log.debug("Flooding ARP packet: %s", arp_packet)

            ether = ethernet()
            ether.type = ethernet.ARP_TYPE
            ether.dst = EthAddr("ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
            ether.src = packet.src  # Use the source MAC address from the packet
            ether.payload = arp_packet

            msg = of.ofp_packet_out()
            msg.data = ether.pack()
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            msg.in_port = in_port
            self.connection.send(msg)



    def _handle_static_routes(self, packet, in_port, ofp):

	'''  Handle Ip packets with static routing configured below
	 '''
        ipv4_packet = packet.payload  # Extract the IP payload
        ipv4_dst_ip = ipv4_packet.dstip  # Get the destination IP address from the IP packet

        log.debug("IP packet recieved with destined to: %s.", ipv4_dst_ip)
        
   	#static routes for hosts h1,h2.h3	

        if(ipv4_dst_ip == '10.0.0.1'):
         out_port = 1

        elif(ipv4_dst_ip == '10.0.0.2'):
            out_port = 2

        elif(ipv4_dst_ip == '10.0.0.3'):
            out_port = 3

        else:
            log.debug("Unknown destination IP")
            return

        # Create actions to forward the packet to the determined port
        actions = [of.ofp_action_output(port=out_port)]
        # Create a flow match based on the received packet
        match = of.ofp_match.from_packet(packet, in_port)
        # Create a flow mod message to install the flow rule
        msg = of.ofp_flow_mod()
        msg.match = match
        msg.idle_timeout = 10  # Flow idle timeout
        msg.hard_timeout = 30  # Flow hard timeout
        msg.actions = actions
        msg.data = ofp  # Include the original packet in the message
        self.connection.send(msg)

        log.debug("Flow installed for %s to %s out port %s", ipv4_packet.srcip, ipv4_dst_ip, out_port)

def launch():
    """
    Start the SimpleRouter component.
     """
    def start_switch(event):
        log.debug("Controlling %s" % (dpid_to_str(event.dpid)))
        SimpleRouter(event.connection)  # Create an instance of SimpleRouter for each switch connection
    core.openflow.addListenerByName("ConnectionUp", start_switch)  # Add a listener for switch connections


                                                



