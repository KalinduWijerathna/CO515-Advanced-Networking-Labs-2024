# switch.py

# import the necessary POX components
from pox.core import core
import pox.openflow.libopenflow_01 as of

# Create a logger for this component
log = core.getLogger()

class SimpleSwitch(object):
    def __init__(self, connection):
        # Store a reference to the connection object
        self.connection = connection
        # Bind this object to listen for PacketIn messages
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        """
        Handles PacketIn messages from the switch.
        This method is called whenever the switch sends a packet to the controller.
        """
        packet = event.parsed  # Parse the incoming packet

        # Learn the source MAC address to avoid flooding next time.
        # Store the port where the packet came from
        self.mac_to_port[packet.src] = event.port

        # Check if the destination MAC address is known
        if packet.dst in self.mac_to_port:
            # Destination MAC is known, retrieve the output port
            out_port = self.mac_to_port[packet.dst]
            log.debug("Sending packet to port %s", out_port)
            # Create a PacketOut message to send the packet out the correct port
            msg = of.ofp_packet_out()
            msg.data = event.ofp  # Include the original packet data
            action = of.ofp_action_output(port=out_port)  # Specify the output port
            msg.actions.append(action)  # Add the action to the message
            self.connection.send(msg)  # Send the message to the switch
        else:
            # Destination MAC is unknown, flood the packet out all ports
            log.debug("Flooding packet")
            msg = of.ofp_packet_out()
            msg.data = event.ofp  # Include the original packet data
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  # Specify flooding action
            self.connection.send(msg)  # Send the message to the switch

    def _handle_ConnectionUp(self, event):
        """
        Handles ConnectionUp messages from the switch.
        This method is called when a switch connects to the controller.
        """
        log.info("Connection %s" % (event.connection,))
        # Initialize a dictionary to map MAC addresses to switch ports
        self.mac_to_port = {}

def launch():
    """
    Starts the SimpleSwitch controller.
    This function is called when the module is run.
    """
    def start_switch(event):
        log.info("Controlling %s" % (event.connection,))
        # Create an instance of SimpleSwitch for each new switch connection
        SimpleSwitch(event.connection)

    # Add an event listener for when switches connect to the controller
    core.openflow.addListenerByName("ConnectionUp", start_switch)


