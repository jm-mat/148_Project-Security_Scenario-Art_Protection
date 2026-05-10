"""
ArtVault Mininet Topology
-------------------------

Run inside Mininet container:
    python3 /app/mininet/topology.py

From Mininet CLI:

    # Start server
    mininet> srv python3 /home/cloudy/project/app/flask_app/app.py &

    # Human clients
    mininet> h_casual python3 /home/cloudy/project/app/scrapers/casual_human.py
    mininet> h_multi python3 /home/cloudy/project/app/scrapers/multitasking_human.py
    mininet> h_expert python3 /home/cloudy/project/app/scrapers/experienced_human.py

    # Individual scraper bots
    mininet> b_fast python3 /home/cloudy/project/app/scrapers/fast_repeater_bot.py
    mininet> b_enum python3 /home/cloudy/project/app/scrapers/enumerator_bot.py
    mininet> b_rand python3 /home/cloudy/project/app/scrapers/randomizer_bot.py
    mininet> b_adapt python3 /home/cloudy/project/app/scrapers/adaptive_bot.py
    mininet> b_strat python3 /home/cloudy/project/app/scrapers/strategy_rotating_bot.py

    # High-volume parallel cluster
    mininet> load1 python3 /home/cloudy/project/app/scrapers/fast_repeater_bot.py
    mininet> load2 python3 /home/cloudy/project/app/scrapers/randomizer_bot.py
    mininet> load3 python3 /home/cloudy/project/app/scrapers/enumerator_bot.py
    mininet> load4 python3 /home/cloudy/project/app/scrapers/adaptive_bot.py
"""

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.log  import setLogLevel
from mininet.cli  import CLI
from mininet.nodelib import NAT
import os

def build_topology():
    setLogLevel("info")

    # controller
    net = Mininet(controller=None, link=TCLink)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Single switch
    s1 = net.addSwitch("s1")

    # Flask Server
    srv = net.addHost("srv", ip="10.0.0.1/24")

    # Human-like clients
    h_casual = net.addHost("h_casual", ip="10.0.0.2/24")
    h_multi  = net.addHost("h_multi",  ip="10.0.0.3/24")
    h_expert = net.addHost("h_expert", ip="10.0.0.4/24")

    # Individual scraper bots
    b_fast  = net.addHost("b_fast",  ip="10.0.0.5/24")
    b_enum  = net.addHost("b_enum",  ip="10.0.0.6/24")
    b_rand  = net.addHost("b_rand",  ip="10.0.0.7/24")
    b_adapt = net.addHost("b_adapt", ip="10.0.0.8/24")
    b_strat = net.addHost("b_strat", ip="10.0.0.9/24")

    # High-volume parallel cluster
    load1 = net.addHost("load1", ip="10.0.0.10/24")
    load2 = net.addHost("load2", ip="10.0.0.11/24")
    load3 = net.addHost("load3", ip="10.0.0.12/24")
    load4 = net.addHost("load4", ip="10.0.0.13/24")

    # Link all hosts to switch
    hosts = [
        srv,
        h_casual, h_multi, h_expert,
        b_fast, b_enum, b_rand, b_adapt, b_strat,
        load1, load2, load3, load4
    ]

    for h in hosts:
        net.addLink(h, s1, bw=10, delay="5ms")
        
    net.start()
    # --- AUTO-CONNECT HOST MACHINE TO MININET NETWORK ---
    print("Creating veth pair to connect host ↔ Mininet...")

    # Delete old interfaces if they exist
    os.system("ip link delete veth-host 2>/dev/null")

    # Create veth pair
    os.system("ip link add veth-host type veth peer name veth-s1")

    # Bring up host side
    os.system("ip link set veth-host up")
    os.system("ip addr flush dev veth-host")
    os.system("ip addr add 10.0.0.253/24 dev veth-host")

    # Attach Mininet side to switch s1
    os.system("ovs-vsctl add-port s1 veth-s1")
    os.system("ip link set veth-s1 up")

    print("Host is now connected to Mininet via veth-host ↔ veth-s1")
    print("\n=== ArtVault Mininet Topology ===\n")
    
    # --- AUTO-START APPLICATIONS ON HOSTS ---
    print("\n=== Auto-starting ArtVault services ===\n")

    # Start Flask server
    # Change absolute path to app.py
    srv.cmd("python3 /home/cloudy/project/app/flask_app/app.py &")
    print("Started Flask server on srv")

    # Human clients
    # Change absolute path to scrapers folder
    h_casual.cmd("python3 /home/cloudy/project/app/scrapers/casual_human.py &")
    h_multi.cmd("python3 /home/cloudy/project/app/scrapers/multitasking_human.py &")
    h_expert.cmd("python3 /home/cloudy/project/app/scrapers/experienced_human.py &")
    print("Started human clients")

    # Individual scraper bots
    # Change absolute path to scrapers folder
    b_fast.cmd("python3 /home/cloudy/project/app/scrapers/fast_repeater_bot.py &")
    b_enum.cmd("python3 /home/cloudy/project/app/scrapers/enumerator_bot.py &")
    b_rand.cmd("python3 /home/cloudy/project/app/scrapers/randomizer_bot.py &")
    b_adapt.cmd("python3 /home/cloudy/project/app/scrapers/adaptive_bot.py &")
    b_strat.cmd("python3 /home/cloudy/project/app/scrapers/strategy_rotating_bot.py &")
    print("Started individual scraper bots")

    # High-volume parallel cluster
    # Change absolute path to scrapers folder
    load1.cmd("python3 /home/cloudy/project/app/scrapers/fast_repeater_bot.py &")
    load2.cmd("python3 /home/cloudy/project/app/scrapers/randomizer_bot.py &")
    load3.cmd("python3 /home/cloudy/project/app/scrapers/enumerator_bot.py &")
    load4.cmd("python3 /home/cloudy/project/app/scrapers/adaptive_bot.py &")
    print("Started high-volume cluster\n")


    CLI(net)
    net.stop()

if __name__ == "__main__":
    build_topology()
