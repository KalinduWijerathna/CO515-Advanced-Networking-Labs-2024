from mininet.net import Containernet
from mininet.node import Docker,Controller,OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI  # Import CLI for Containernet


def setup_network():
    net = Containernet(controller=Controller, switch=OVSSwitch)

    print("*** Adding controller")
    net.addController('c0')

    info('*** Adding docker containers\n')
    h1 = net.addDocker('h1', ip='10.0.0.1', dimage="ubuntu:latest", mac='00:00:00:00:00:01', shell='/bin/bash')
    h3 = net.addDocker('h3', ip='10.0.0.3', dimage="ubuntu:latest", mac='00:00:00:00:00:03', shell='/bin/bash')
    # old config
    # h2 = net.addDocker('h2', ip='10.0.0.2', dimage="ubuntu:latest", mac='00:00:00:00:00:02', shell='/bin/bash')
    
    # new config
    h2 = net.addDocker( # exposing zabbix server ports
        'h2',
        ip='10.0.0.2',
        dimage="ubuntu:latest",
        mac='00:00:00:00:00:02',
        ports=[10051, 80],
        port_bindings={10051: 10051, 32770: 80},
        shell='/bin/bash'
    )


    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')

    info('*** Creating links\n')
    net.addLink(h1, s1, cls=TCLink)
    net.addLink(h2, s1, cls=TCLink)
    net.addLink(h3, s1, cls=TCLink)
    
    # Install necessary packages and configure IP addresses
    for h, ip in zip([h1, h2, h3], ['10.0.0.1', '10.0.0.2', '10.0.0.3']):
        h.cmd('apt-get update')
        h.cmd('apt-get install -y iputils-ping net-tools snmpd snmp vim')

        # Set IP address using ifconfig command
        h.cmd(f'ifconfig {h}-eth0 {ip} netmask 255.255.255.0')

        # Start SNMP service
        h.cmd('service snmpd start')


    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)  # Use CLI(net) to enter the CLI

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_network()


