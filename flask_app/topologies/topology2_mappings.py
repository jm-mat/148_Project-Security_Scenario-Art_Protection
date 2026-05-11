# Topology 2 — Large‑Scale 50‑Node Simulation

SCRAPER_NAMES = {}

# Humans (6 total — 2 copies of each)
human_ips = {
    "10.0.0.2": "CasualHuman-1",
    "10.0.0.3": "CasualHuman-2",

    "10.0.0.4": "MultiHuman-1",
    "10.0.0.5": "MultiHuman-2",

    "10.0.0.6": "ExpertHuman-1",
    "10.0.0.7": "ExpertHuman-2",
}

SCRAPER_NAMES.update(human_ips)

# Individual Bots (8 total)
individual_bots = {
    "10.0.0.8":  "AdaptiveBot-1",
    "10.0.0.9":  "AdaptiveBot-2",

    "10.0.0.10": "StrategicBot-1",
    "10.0.0.11": "StrategicBot-2",

    "10.0.0.12": "RandomWalkerBot-1",
    "10.0.0.13": "RandomWalkerBot-2",

    "10.0.0.14": "FastRepeaterBot-1",
    "10.0.0.15": "EnumeratorBot-1",
}

SCRAPER_NAMES.update(individual_bots)

# Cluster A — 12 bots (4× Randomizer, 4× FastRepeater, 4× Enumerator)
clusterA_random = ["10.0.0.20", "10.0.0.21", "10.0.0.22", "10.0.0.23"]
clusterA_fast   = ["10.0.0.24", "10.0.0.25", "10.0.0.26", "10.0.0.27"]
clusterA_enum   = ["10.0.0.28", "10.0.0.29", "10.0.0.30", "10.0.0.31"]

for i, ip in enumerate(clusterA_random, start=1):
    SCRAPER_NAMES[ip] = f"ClusterA-Randomizer-{i}"

for i, ip in enumerate(clusterA_fast, start=1):
    SCRAPER_NAMES[ip] = f"ClusterA-FastRepeater-{i}"

for i, ip in enumerate(clusterA_enum, start=1):
    SCRAPER_NAMES[ip] = f"ClusterA-Enumerator-{i}"

clusterA = clusterA_random + clusterA_fast + clusterA_enum

# Cluster B — same pattern
clusterB_random = ["10.0.0.32", "10.0.0.33", "10.0.0.34", "10.0.0.35"]
clusterB_fast   = ["10.0.0.36", "10.0.0.37", "10.0.0.38", "10.0.0.39"]
clusterB_enum   = ["10.0.0.40", "10.0.0.41", "10.0.0.42", "10.0.0.43"]

for i, ip in enumerate(clusterB_random, start=1):
    SCRAPER_NAMES[ip] = f"ClusterB-Randomizer-{i}"

for i, ip in enumerate(clusterB_fast, start=1):
    SCRAPER_NAMES[ip] = f"ClusterB-FastRepeater-{i}"

for i, ip in enumerate(clusterB_enum, start=1):
    SCRAPER_NAMES[ip] = f"ClusterB-Enumerator-{i}"

clusterB = clusterB_random + clusterB_fast + clusterB_enum


# Cluster C — same pattern
clusterC_random = ["10.0.0.44", "10.0.0.45", "10.0.0.46", "10.0.0.47"]
clusterC_fast   = ["10.0.0.48", "10.0.0.49", "10.0.0.50", "10.0.0.51"]
clusterC_enum   = ["10.0.0.52", "10.0.0.53", "10.0.0.54", "10.0.0.55"]

for i, ip in enumerate(clusterC_random, start=1):
    SCRAPER_NAMES[ip] = f"ClusterC-Randomizer-{i}"

for i, ip in enumerate(clusterC_fast, start=1):
    SCRAPER_NAMES[ip] = f"ClusterC-FastRepeater-{i}"

for i, ip in enumerate(clusterC_enum, start=1):
    SCRAPER_NAMES[ip] = f"ClusterC-Enumerator-{i}"

clusterC = clusterC_random + clusterC_fast + clusterC_enum

# Cluster definitions for dashboard aggregation
BOT_CLUSTERS = {
    "ClusterA": clusterA,
    "ClusterB": clusterB,
    "ClusterC": clusterC,
}

