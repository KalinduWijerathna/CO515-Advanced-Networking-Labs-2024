from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_topology():
    net = Mininet(controller=None, switch=OVSSwitch)

    # Adding switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Adding hosts
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.1.1/24')
    h3 = net.addHost('h3', ip='10.0.2.1/24')
    h4 = net.addHost('h4', ip='10.0.3.1/24')

    # Adding links with interface IPs for switches
    net.addLink(h1, s1, params1={'ip': '10.0.0.2/24'})
    net.addLink(h2, s2, params1={'ip': '10.0.1.2/24'})
    net.addLink(h3, s3, params1={'ip': '10.0.2.2/24'})
    net.addLink(h4, s1, params1={'ip': '10.0.3.2/24'})

    net.addLink(s1, s2, params1={'ip': '10.0.5.1/24'}, params2={'ip': '10.0.5.2/24'})
    net.addLink(s2, s3, params1={'ip': '10.0.6.1/24'}, params2={'ip': '10.0.6.2/24'})
    net.addLink(s3, s1, params1={'ip': '10.0.7.1/24'}, params2={'ip': '10.0.7.2/24'})
    
    # Start the network
    net.start()

    # Add a Ryu controller
    #ryu_controller = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    # Assign switch to the controller
    #net.controllers = [ryu_controller]
    #for switch in net.switches:
    #   switch.start([ryu_controller])
    
    # Add a POX controller
    pox_controller = net.addController('c0', controller=Controller, ip='127.0.0.1', port=6633)

    # Assign switch to the controller
    net.controllers = [pox_controller]
    for switch in net.switches:
        switch.start([pox_controller])


    # Start the Mininet CLI
    CLI(net)

    # Clean up the network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()


