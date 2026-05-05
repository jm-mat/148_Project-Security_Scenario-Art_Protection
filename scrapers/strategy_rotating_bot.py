# strategy rotating bot(repeater, enumerator and randomizer)
import requests
import random
import time

BASE = "http://127.0.0.1:5000"

STRATEGIES = ["fast", "enum", "random"]
PAGES = ["/", "/api/artworks"] + \
        [f"/artwork/{i}" for i in range(1, 10+1)] + \
        [f"/api/artwork/{i}" for i in range(1, 10+1)]

# per-instance randomness
time.sleep(random.uniform(0.5, 4.0))
SPEED = random.uniform(0.5, 1.5)

# fast repeater behavior
def do_fast():
    page = random.choice(PAGES)
    return page, random.uniform(0.05, 0.2)
# enumerator behavior
def do_enum(counter):
    page = f"/api/artwork/{counter}"
    return page, random.uniform(0.3, 0.8)
# randomizer behavior
def do_random():
    page = random.choice(PAGES)
    return page, random.expovariate(1.2)

counter = random.randint(1, 5)

# random behavior for each iteration 
for i in range(200):
    strat = random.choice(STRATEGIES)

    if strat == "fast":
        page, delay = do_fast()
    elif strat == "enum":
        page, delay = do_enum(counter)
        counter = counter + 1 if counter < 10 else 1
    else:
        page, delay = do_random()

    delay *= SPEED

    r = requests.get(BASE + page)
    print(f"[ROTATE:{strat}] {i}: GET {page} => {r.status_code} (delay {delay:.2f}s)")

    time.sleep(delay)
