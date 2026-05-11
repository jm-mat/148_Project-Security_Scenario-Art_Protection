import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import importlib

# Path to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Logs are in the same folder as this script
LOG_DIR = SCRIPT_DIR

# Add the parent of flask_app to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
sys.path.append(PROJECT_ROOT)

def detect_topology(filename):
    name = filename.lower()
    if "topology1" in name:
        return "topology1_mappings"
    if "topology2" in name:
        return "topology2_mappings"
    return None

def load_logs():
    rows = []
    print("LOG_DIR =", LOG_DIR)
    print("FILES:", os.listdir(LOG_DIR))

    for filename in os.listdir(LOG_DIR):
        if not filename.endswith(".log"):
            continue
        # Detect topology
        topology_name = detect_topology(filename)
        if topology_name:
            topo = importlib.import_module(f"flask_app.topologies.{topology_name}")
            SCRAPER_NAMES = topo.SCRAPER_NAMES
        else:
            SCRAPER_NAMES = {}

        with open(os.path.join(LOG_DIR, filename)) as f:
            for line in f:
                # Only JSON lines contain "{"
                if "{" not in line:
                    continue

                try:
                    # Split timestamp and JSON
                    ts_str, json_part = line.split("{", 1)
                    ts_str = ts_str.strip()
                    # Parse timestamp with milliseconds
                    ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S,%f")
                    # Parse JSON
                    data = json.loads("{" + json_part)
                    # Add metadata
                    data["timestamp"] = ts
                    data["logfile"] = filename
                    data["scraper_type"] = SCRAPER_NAMES.get(data["ip"], "Unknown")

                    rows.append(data)

                except Exception as e:
                    print("Parse error:", e)
                    print("Line:", line)

    return pd.DataFrame(rows)


df = load_logs()
print(df.head())

# Requests per IP
ip_table = df["ip"].value_counts()
print("\n=== Requests per IP ===")
print(ip_table)

plt.figure(figsize=(10,5))
sns.countplot(y=df["ip"], order=df["ip"].value_counts().index)
plt.title("Requests per IP")
plt.tight_layout()
plt.savefig("1_requests_per_ip.png")

# Requests per Endpoint
endpoint_table = df["path"].value_counts()
print("\n=== Requests per Endpoint ===")
print(endpoint_table)

plt.figure(figsize=(10,5))
sns.countplot(y=df["path"], order=df["path"].value_counts().index)
plt.title("Requests per Endpoint")
plt.tight_layout()
plt.savefig("2_requests_per_endpoint.png")

# Status Code Distribution
status_table = df["status"].value_counts()
print("\n=== Status Codes ===")
print(status_table)

plt.figure(figsize=(6,4))
sns.countplot(x=df["status"])
plt.title("Status Code Distribution")
plt.tight_layout()
plt.savefig("3_status_codes.png")

# Flagged vs Non-Flagged
flag_table = df["flagged"].value_counts()
print("\n=== Flagged Requests ===")
print(flag_table)

plt.figure(figsize=(6,4))
sns.countplot(x=df["flagged"])
plt.title("Flagged vs Non-Flagged Requests")
plt.tight_layout()
plt.savefig("4_flagged.png")

# Requests Over Time (RPS)
df_sorted = df.sort_values("timestamp")
df_sorted["count"] = 1
df_time = df_sorted.set_index("timestamp").resample("1s").count()

plt.figure(figsize=(12,4))
plt.plot(df_time.index, df_time["count"])
plt.title("Requests Per Second")
plt.tight_layout()
plt.savefig("5_rps.png")

# Requests per Scraper Type
scraper_table = df["scraper_type"].value_counts()
print("\n=== Requests per Scraper Type ===")
print(scraper_table)

# Wrap long scraper names so they don't overlap
df["scraper_type_wrapped"] = df["scraper_type"].apply(
    lambda x: "\n".join([x[i:i+25] for i in range(0, len(x), 25)])
)

plt.figure(figsize=(14, 8))  # bigger figure
sns.countplot(
    y=df["scraper_type_wrapped"],
    order=df["scraper_type_wrapped"].value_counts().index
)
plt.title("Requests per Scraper Type")
plt.tight_layout()
plt.savefig("6_scraper_types.png")


# Time-to-Mitigation (TTM) — by Scraper Type
ttm_rows = []

for scraper, group in df.groupby("scraper_type"):
    group = group.sort_values("timestamp")

    first_seen = group["timestamp"].iloc[0]

    blocked = group[group["status"] == 403]
    if blocked.empty:
        continue

    first_block = blocked["timestamp"].iloc[0]
    ttm = (first_block - first_seen).total_seconds()

    ttm_rows.append({"scraper_type": scraper, "ttm_seconds": ttm})

ttm_df = pd.DataFrame(ttm_rows)
print("\n=== Time to Mitigation (TTM) by Scraper Type ===")
print(ttm_df)

# Wrap long scraper names for readability
ttm_df["scraper_type_wrapped"] = ttm_df["scraper_type"].apply(
    lambda x: "\n".join([x[i:i+25] for i in range(0, len(x), 25)])
)

plt.figure(figsize=(14, 8))
sns.barplot(data=ttm_df, x="ttm_seconds", y="scraper_type_wrapped")
plt.title("Time to Mitigation (Seconds) by Scraper Type")
plt.tight_layout()
plt.savefig("7_ttm.png")

print("\nGraphs saved:")
print(" - 1_requests_per_ip.png")
print(" - 2_requests_per_endpoint.png")
print(" - 3_status_codes.png")
print(" - 4_flagged.png")
print(" - 5_rps.png")
print(" - 6_scraper_types.png")
print(" - 7_ttm.png")

