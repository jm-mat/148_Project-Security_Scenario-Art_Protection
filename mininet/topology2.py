"""
ArtVault Mininet Topology 2 — 50 Node Stress Test
-------------------------------------------------

Run inside Mininet container:
    python3 /app/mininet/topology2.py

From Mininet CLI:

    # Start server
    mininet> srv python3 /home/cloudy/project/app/flask_app/app.py &

    # Human clients
    mininet> h_casual1 python3 /home/cloudy/project/app/scrapers/casual_human.py
    mininet> h_casual2 python3 /home/cloudy/project/app/scrapers/casual_human.py
    mininet> h_multi1 python3 /home/cloudy/project/app/scrapers/multitasking_human.py
    mininet> h_multi2 python3 /home/cloudy/project/app/scrapers/multitasking_human.py
    mininet> h_expert1 python3 /home/cloudy/project/app/scrapers/experienced_human.py
    mininet> h_expert2 python3 /home/cloudy/project/app/scrapers/experienced_human.py

    # Individual scraper bots
    mininet> b_adapt1 python3 /home/cloudy/project/app/scrapers/adaptive_bot.py
    mininet> b_adapt2 python3 /home/cloudy/project/app/scrapers/adaptive_bot.py
    mininet> b_strat1 python3 /home/cloudy/project/app/scrapers/strategy_rotating_bot.py
    mininet> b_strat2 python3 /home/cloudy/project/app/scrapers/strategy_rotating_bot.py
    mininet> b_rand1 python3 /home/cloudy/project/app/scrapers/randomizer_bot.py
    mininet> b_rand2 python3 /home/cloudy/project/app/scrapers/randomizer_bot.py
    mininet> b_fast1 python3 /home/cloudy/project/app/scrapers/fast_repeater_bot.py
    mininet> b_enum1 python3 /home/cloudy/project/app/scrapers/enumerator_bot.py

    # Cluster bots (A, B, C)
    # Each cluster: 4× randomizer, 4× fast repeater, 4× enumerator
"""

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import RemoteController
from mininet.log  import setLogLevel
from mininet.cli  import CLI
import os


def build_topology():
    setLogLevel("info")

    # controller
    net = Mininet(controller=None, link=TCLink)
    net.addController('c0', controller=RemoteController,
                      ip='127.0.0.1', port=6633)

    # Single switch
    s1 = net.addSwitch("s1")

    # Flask Server
    srv = net.addHost("srv", ip="10.0.0.1/24")

    # Human-like clients (6 total)
    h_casual1 = net.addHost("h_casual1", ip="10.0.0.2/24")
    h_casual2 = net.addHost("h_casual2", ip="10.0.0.3/24")

    h_multi1  = net.addHost("h_multi1",  ip="10.0.0.4/24")
    h_multi2  = net.addHost("h_multi2",  ip="10.0.0.5/24")

    h_expert1 = net.addHost("h_expert1", ip="10.0.0.6/24")
    h_expert2 = net.addHost("h_expert2", ip="10.0.0.7/24")

    # Individual scraper bots (8 total)
    b_adapt1 = net.addHost("b_adapt1", ip="10.0.0.8/24")
    b_adapt2 = net.addHost("b_adapt2", ip="10.0.0.9/24")

    b_strat1 = net.addHost("b_strat1", ip="10.0.0.10/24")
    b_strat2 = net.addHost("b_strat2", ip="10.0.0.11/24")

    b_rand1  = net.addHost("b_rand1",  ip="10.0.0.12/24")
    b_rand2  = net.addHost("b_rand2",  ip="10.0.0.13/24")

    b_fast1  = net.addHost("b_fast1",  ip="10.0.0.14/24")
    b_enum1  = net.addHost("b_enum1",  ip="10.0.0.15/24")

    # Cluster A (12 bots)
    A_rand1 = net.addHost("A_rand1", ip="10.0.0.20/24")
    A_rand2 = net.addHost("A_rand2", ip="10.0.0.21/24")
    A_rand3 = net.addHost("A_rand3", ip="10.0.0.22/24")
    A_rand4 = net.addHost("A_rand4", ip="10.0.0.23/24")

    A_fast1 = net.addHost("A_fast1", ip="10.0.0.24/24")
    A_fast2 = net.addHost("A_fast2", ip="10.0.0.25/24")
    A_fast3 = net.addHost("A_fast3", ip="10.0.0.26/24")
    A_fast4 = net.addHost("A_fast4", ip="10.0.0.27/24")

    A_enum1 = net.addHost("A_enum1", ip="10.0.0.28/24")
    A_enum2 = net.addHost("A_enum2", ip="10.0.0.29/24")
    A_enum3 = net.addHost("A_enum3", ip="10.0.0.30/24")
    A_enum4 = net.addHost("A_enum4", ip="10.0.0.31/24")

    # Cluster B (12 bots)
    B_rand1 = net.addHost("B_rand1", ip="10.0.0.32/24")
    B_rand2 = net.addHost("B_rand2", ip="10.0.0.33/24")
    B_rand3 = net.addHost("B_rand3", ip="10.0.0.34/24")
    B_rand4 = net.addHost("B_rand4", ip="10.0.0.35/24")

    B_fast1 = net.addHost("B_fast1", ip="10.0.0.36/24")
    B_fast2 = net.addHost("B_fast2", ip="10.0.0.37/24")
    B_fast3 = net.addHost("B_fast3", ip="10.0.0.38/24")
    B_fast4 = net.addHost("B_fast4", ip="10.0.0.39/24")

    B_enum1 = net.addHost("B_enum1", ip="10.0.0.40/24")
    B_enum2 = net.addHost("B_enum2", ip="10.0.0.41/24")
    B_enum3 = net.addHost("B_enum3", ip="10.0.0.42/24")
    B_enum4 = net.addHost("B_enum4", ip="10.0.0.43/24")

    # Cluster C (12 bots)
    C_rand1 = net.addHost("C_rand1", ip="10.0.0.44/24")
    C_rand2 = net.addHost("C_rand2", ip="10.0.0.45/24")
    C_rand3 = net.addHost("C_rand3", ip="10.0.0.46/24")
    C_rand4 = net.addHost("C_rand4", ip="10.0.0.47/24")

    C_fast1 = net.addHost("C_fast1", ip="10.0.0.48/24")
    C_fast2 = net.addHost("C_fast2", ip="10.0.0.49/24")
    C_fast3 = net.addHost("C_fast3", ip="10.0.0.50/24")
    C_fast4 = net.addHost("C_fast4", ip="10.0.0.51/24")

    C_enum1 = net.addHost("C_enum1", ip="10.0.0.52/24")
    C_enum2 = net.addHost("C_enum2", ip="10.0.0.53/24")
    C_enum3 = net.addHost("C_enum3", ip="10.0.0.54/24")
    C_enum4 = net.addHost("C_enum4", ip="10.0.0.55/24")

    # Link all hosts to switch
    hosts = [
        srv,
        h_casual1, h_casual2,
        h_multi1, h_multi2,
        h_expert1, h_expert2,
        b_adapt1, b_adapt2,
        b_strat1, b_strat2,
        b_rand1, b_rand2,
        b_fast1, b_enum1,
        A_rand1, A_rand2, A_rand3, A_rand4,
        A_fast1, A_fast2, A_fast3, A_fast4,
        A_enum1, A_enum2, A_enum3, A_enum4,
        B_rand1, B_rand2, B_rand3, B_rand4,
        B_fast1, B_fast2, B_fast3, B_fast4,
        B_enum1, B_enum2, B_enum3, B_enum4,
        C_rand1, C_rand2, C_rand3, C_rand4,
        C_fast1, C_fast2, C_fast3, C_fast4,
        C_enum1, C_enum2, C_enum3, C_enum4,
    ]

    for h in hosts:
        net.addLink(h, s1, bw=10, delay="5ms")

    net.start()

    # --- AUTO-CONNECT HOST MACHINE TO MININET NETWORK ---
    print("Creating veth pair to connect host ↔ Mininet...")

    os.system("ip link delete veth-host 2>/dev/null")
    os.system("ip link add veth-host type veth peer name veth-s1")
    os.system("ip link set veth-host up")
    os.system("ip addr flush dev veth-host")
    os.system("ip addr add 10.0.0.253/24 dev veth-host")
    os.system("ovs-vsctl add-port s1 veth-s1")
    os.system("ip link set veth-s1 up")

    print("Host is now connected to Mininet via veth-host ↔ veth-s1")
    print("\n=== ArtVault Mininet Topology 2 ===\n")

    # --- AUTO-START APPLICATIONS ON HOSTS ---
    print("\n=== Auto-starting ArtVault services ===\n")

    # Start Flask server with topology2 mappings
    srv.cmd(
        "TOPOLOGY=topology2_mappings "
        "PYTHONPATH=/home/cloudy/project/app "
        "python3 /home/cloudy/project/app/flask_app/app.py &"
    )
    print("Started Flask server on srv")

    # Human clients
    h_casual1.cmd("python3 /home/cloudy/project/app/scrapers/casual_human.py &")
    h_casual2.cmd("python3 /home/cloudy/project/app/scrapers/casual_human.py &")

    h_multi1.cmd("python3 /home/cloudy/project/app/scrapers/multitasking_human.py &")
    h_multi2.cmd("python3 /home/cloudy/project/app/scrapers/multitasking_human.py &")

    h_expert1.cmd("python3 /home/cloudy/project/app/scrapers/experienced_human.py &")
    h_expert2.cmd("python3 /home/cloudy/project/app/scrapers/experienced_human.py &")

    print("Started human clients")

    # Individual scraper bots
    b_adapt1.cmd("python3 /home/cloudy/project/app/scrapers/adaptive_bot.py &")
    b_adapt2.cmd("python3 /home/cloudy/project/app/scrapers/adaptive_bot.py &")

    b_strat1.cmd("python3 /home/cloudy/project/app/scrapers/strategy_rotating_bot.py &")
    b_strat2.cmd("python3 /home/cloudy/project/app/scrapers/strategy_rotating_bot.py &")

    b_rand1.cmd("python3 /home/cloudy/project/app/scrapers/randomizer_bot.py &")
    b_rand2.cmd("python3 /home/cloudy/project/app/scrapers/randomizer_bot.py &")

    b_fast1.cmd("python3 /home/cloudy/project/app/scrapers/fast_repeater_bot.py &")
    b_enum1.cmd("python3 /home/cloudy/project/app/scrapers/enumerator_bot.py &")

    print("Started individual scraper bots")

    # Cluster A
    for bot in [A_rand1, A_rand2, A_rand3, A_rand4]:
        bot.cmd("python3 /home/cloudy/project/app/scrapers/randomizer_bot.py &")
    for bot in [A_fast1, A_fast2, A_fast3, A_fast4]:
        bot.cmd("python3 /home/cloudy/project/app/scrapers/fast_repeater_bot.py &")
    for bot in [A_enum1, A_enum2, A_enum3, A_enum4]:
        bot.cmd("python3 /home/cloudy/project/app/scrapers/enumerator_bot.py &")

    # Cluster B
    for bot in [B_rand1, B_rand2, B_rand3, B_rand4]:
        bot.cmd("python3 /home/cloudy/project/app/scrapers/randomizer_bot.py &")
    for bot in [B_fast1, B_fast2, B_fast3, B_fast4]:
        bot.cmd("python3 /home/cloudy/project/app/scrapers/fast_repeater_bot.py &")
    for bot in [B_enum1, B_enum2, B_enum3, B_enum4]:
        bot.cmd("python3 /home/cloudy/project/app/scrapers/enumerator_bot.py &")

    # Cluster C
    for bot in [C_rand1, C_rand2, C_rand3, C_rand4]:
        bot.cmd("python3 /home/cloudy/project/app/scrapers/randomizer_bot.py &")
    for bot in [C_fast1, C_fast2, C_fast3, C_fast4]:
        bot.cmd("python3 /home/cloudy/project/app/scrapers/fast_repeater_bot.py &")
    for bot in [C_enum1, C_enum2, C_enum3, C_enum4]:
        bot.cmd("python3 /home/cloudy/project/app/scrapers/enumerator_bot.py &")

    print("Started all cluster bots\n")

    CLI(net)
    net.stop()


if __name__ == "__main__":
    build_topology()
