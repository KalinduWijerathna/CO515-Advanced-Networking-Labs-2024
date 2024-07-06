from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info

def createDataCenter():
    net = Mininet(controller=Controller, link=TCLink, switch=OVSSwitch)
    
    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding switches\n')
    # Core switches
    info('*** ||||||||| Adding Core Layer....\n')
    core1 = net.addSwitch('s1')
    core2 = net.addSwitch('s2')
    
    # Aggregation switches
    info('*** ||||||||| Adding Aggregation Layer....\n')
    agg1 = net.addSwitch('s3')
    agg2 = net.addSwitch('s4')
    agg3 = net.addSwitch('s5')
    
    # Edge/access switches
    info('*** ||||||||| Adding Access Layer....\n')
    edge1 = net.addSwitch('s6')
    edge2 = net.addSwitch('s7')
    edge3 = net.addSwitch('s8')
    edge4 = net.addSwitch('s9')
    edge5 = net.addSwitch('s10')
    edge6 = net.addSwitch('s11')
    
    info('*** Adding hosts\n')
    # Hosts for different VLANs
    hosts = []
    vlans = [10, 20, 30, 40]  # VLANs: mgmt, srv, storage, bkp
    for i in range(12):
        vlan_id = vlans[i // 4]  # Assign VLAN based on host number
        ip = '10.{}.{}.{}'.format(vlan_id, i % 4, i % 256)
        host = net.addHost('h%s' % i, ip=ip)
        hosts.append(host)
    
    info('*** Creating links\n')
    # Core to Aggregation
    net.addLink(core1, agg1)
    net.addLink(core1, agg2)
    net.addLink(core2, agg2)
    net.addLink(core2, agg3)

    # Aggregation to Edge
    net.addLink(agg1, edge1)
    net.addLink(agg1, edge2)
    net.addLink(agg2, edge3)
    net.addLink(agg2, edge4)
    net.addLink(agg3, edge5)
    net.addLink(agg3, edge6)
    
    # Edge to Hosts
    for i in range(2):
        net.addLink(edge1, hosts[i], params1={'vlan': 10})
        net.addLink(edge2, hosts[i+2], params1={'vlan': 20})
        net.addLink(edge3, hosts[i+4], params1={'vlan': 30})
        net.addLink(edge4, hosts[i+6], params1={'vlan': 40})
        net.addLink(edge5, hosts[i+8], params1={'vlan': 30})
        net.addLink(edge6, hosts[i+10], params1={'vlan': 40})
    
    info('*** Starting network\n')
    net.start()
    
    info('*** Configuring VLANs on switches\n')
    # Configure VLANs on edge switches
    edge_switches = [edge1, edge2, edge3, edge4, edge5, edge6]
    for i, edge in enumerate(edge_switches):
        vlan_id = vlans[i // 2]
        edge.cmd('ovs-vsctl add-port %s %s-tagged -- set port %s-tagged tag=%d' % (edge.name, edge.name, edge.name, vlan_id))
    
    info('*** Running CLI\n')
    CLI(net)
    
    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createDataCenter()

