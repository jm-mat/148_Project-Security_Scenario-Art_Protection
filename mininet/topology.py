"""
ArtVault Mininet Topology
-------------------------

Run inside Mininet container:
    python3 /app/mininet/topology.py

From Mininet CLI:

    # Start server
    mininet> srv python3 /app/flask_app/app.py &

    # Human clients
    mininet> h_casual python3 /app/scrapers/casual_human.py
    mininet> h_multi python3 /app/scrapers/multitasking_human.py
    mininet> h_expert python3 /app/scrapers/experienced_human.py

    # Individual scraper bots
    mininet> b_fast python3 /app/scrapers/fast_repeater_bot.py
    mininet> b_enum python3 /app/scrapers/enumerator_bot.py
    mininet> b_rand python3 /app/scrapers/randomizer_bot.py
    mininet> b_adapt python3 /app/scrapers/adaptive_bot.py
    mininet> b_strat python3 /app/scrapers/strategy_rotating_bot.py

    # High-volume parallel cluster
    mininet> load1 python3 /app/scrapers/fast_repeater_bot.py
    mininet> load2 python3 /app/scrapers/randomizer_bot.py
    mininet> load3 python3 /app/scrapers/enumerator_bot.py
    mininet> load4 python3 /app/scrapers/adaptive_bot.py
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.log  import setLogLevel
from mininet.cli  import CLI

def build_topology():
    setLogLevel("info")

    # controller
    net = Mininet(controller=Controller, link=TCLink)
    net.addController("c0")

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

    print("\n=== ArtVault Mininet Topology ===\n")

    print("Server:")
    print("  srv (10.0.0.1)\n")

    print("Human Clients:")
    print("  h_casual (10.0.0.2)")
    print("  h_multi  (10.0.0.3)")
    print("  h_expert (10.0.0.4)\n")

    print("Individual Scraper Bots:")
    print("  b_fast   (10.0.0.5)")
    print("  b_enum   (10.0.0.6)")
    print("  b_rand   (10.0.0.7)")
    print("  b_adapt  (10.0.0.8)")
    print("  b_strat  (10.0.0.9)\n")

    print("High-Volume Parallel Cluster:")
    print("  load1    (10.0.0.10)")
    print("  load2    (10.0.0.11)")
    print("  load3    (10.0.0.12)")
    print("  load4    (10.0.0.13)\n")

    CLI(net)
    net.stop()

if __name__ == "__main__":
    build_topology()
