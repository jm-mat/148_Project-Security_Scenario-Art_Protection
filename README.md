# 148_Project-Security_Scenario-Art_Protection
Project to simulate bot and scraping behavior for a mock art sharing website. on the HTTP level. Will implement some defense mechanisms that focuses on bot detection and rate limiting. Effectiveness of defense mechanisms will be evaluated in the report.

Installation and Running Instructions(Ubuntu 24.01): (Implementation only confirmed working on Native OS Linux Installations)

1) Run these commands to install all required packages:

sudo apt update && sudo apt upgrade -y

sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-seaborn \
    python3-pandas \
    python3-matplotlib \
    python3-flask \
    python3-numpy \
    python3-scipy \
    python3-networkx \
    mininet \
    openvswitch-switch \
    git \
    build-essential

2) Add POX Controller used with Mininet(topology.py and topology2.py)

cd ~
git clone https://github.com/noxrepo/pox.git

3) Run POX Controller in a separate terminal

./pox/pox.py forwarding.l2_learning

4) Open another terminal to run topology files in mininet/ (topology.py or topology2.py(automatically runs flask app and scripts in the background))
   
sudo python3 topology.py

or

sudo python3 topology2.py

5)Open flask server in browser

http://10.0.0.1:5001/                  #<- homepage 
http://10.0.0.1:5001/admin/dashboard   #<- Dashboard for live traffic monitoring

6) Run traffic analyzer in flask_app/logs/ (combines all logs in the folder and generates tables and graphs)

python3 analyze_logs.py



