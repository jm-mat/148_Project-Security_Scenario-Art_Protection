"""
Mininet topology for the ArtVault scraping simulation.

Network layout:
    h1 (Flask server)  — s1 — h2 (single-source bot)
                              h3 (distributed bot 1)
                              h4 (distributed bot 2)
                              h5 (distributed bot 3)

Run inside the Mininet Docker container:
    sudo python3 topology.py

Then from the Mininet CLI:
    mininet> h1 python3 /app/flask_app/app.py &
    mininet> h2 python3 /app/scrapers/single_source_bot.py --host 10.0.0.1
    mininet> h3 python3 /app/scrapers/distributed_scraper.py --host 10.0.0.1 --bots 3
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.log  import setLogLevel
from mininet.cli  import CLI

def build_topology():
    setLogLevel("info")
    net = Mininet(controller=Controller, link=TCLink)

    # Controller
    net.addController("c0")

    # Switch
    s1 = net.addSwitch("s1")

    # Hosts
    h1 = net.addHost("h1", ip="10.0.0.1")   # Flask server
    h2 = net.addHost("h2", ip="10.0.0.2")   # Single-source bot
    h3 = net.addHost("h3", ip="10.0.0.3")   # Distributed bot 1
    h4 = net.addHost("h4", ip="10.0.0.4")   # Distributed bot 2
    h5 = net.addHost("h5", ip="10.0.0.5")   # Distributed bot 3

    # Links (10 Mbps, 5ms delay to simulate real network)
    net.addLink(h1, s1, bw=10, delay="5ms")
    net.addLink(h2, s1, bw=10, delay="5ms")
    net.addLink(h3, s1, bw=10, delay="5ms")
    net.addLink(h4, s1, bw=10, delay="5ms")
    net.addLink(h5, s1, bw=10, delay="5ms")

    net.start()

    print("\n=== ArtVault Mininet Topology ===")
    print("  h1 (10.0.0.1) = Flask server")
    print("  h2 (10.0.0.2) = Single-source scraper")
    print("  h3-h5         = Distributed scrapers")
    print("\nQuick start:")
    print("  mininet> h1 python3 /app/flask_app/app.py &")
    print("  mininet> h2 python3 /app/scrapers/single_source_bot.py --host 10.0.0.1")
    print("  mininet> xterm h1 h2 h3   # open terminals for each host")
    print("")

    CLI(net)
    net.stop()

if __name__ == "__main__":
    build_topology()
