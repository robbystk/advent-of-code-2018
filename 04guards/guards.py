import sys
import re
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pattern = re.compile("^\\[([0-9]{4}-[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9])\\] (.*)$")

def datetime_from_entry(s):
    datetime_format = "%Y-%m-%d %H:%M"
    return datetime.datetime.strptime(pattern.match(s).group(1), datetime_format)

def data_from_entry(s):
    return pattern.match(s).group(2)

def parse_data(s):
    pass

with open(sys.argv[1]) as f:
    sequence = []
    for line in f:
        line = line.strip()
        ts = datetime_from_entry(line)
        data = data_from_entry(line)
        sequence.append([ts, data])

frame = pd.DataFrame(sequence, columns=['Datetime', 'Event'])

sorted_indices = frame['Datetime'].argsort()
sorted_frame = frame.take(sorted_indices).reindex()

guard_pattern = re.compile("^Guard #([0-9]+) begins shift$")
wake_pattern = re.compile("wakes up")
sleep_pattern = re.compile("falls asleep")

sleep_frequency = {}

def add_sleep(cg, start, current_time):
    # print(f"adding sleep from {start} to {current_time} for guard #{current_guard}")
    if cg not in sleep_frequency:
        sleep_frequency[cg] = np.zeros(60, dtype=np.int32)
    sleep_frequency[cg][(start.minute):(current_time.minute+1)] += 1

asleep = False
sleep_time = None

for index, dt, event in sorted_frame.itertuples():
    guard_match = guard_pattern.match(event)
    if guard_match:
        if asleep:
            add_sleep(current_guard, sleep_time, dt)
        current_guard = int(guard_match.group(1))
        asleep = False
        # print(f"guard #{current_guard} begins shift at {dt:%H:%M}")
    elif wake_pattern.match(event):
        if asleep:
            add_sleep(current_guard, sleep_time, dt)
        asleep = False
        sleep_time = None
        # print(f"guard #{current_guard} wakes up at {dt:%H:%M}")
    elif sleep_pattern.match(event):
        asleep = True
        sleep_time = dt
        # print(f"guard #{current_guard} falls asleep at {dt:%H:%M}")
    else:
        print("could not parse line", file=sys.stderr)
        break

def print_sleep_record(sleep_record):
    for g in sleep_record:
        print(f"guard #{g}:\t", end='')
        for f in sleep_record[g]:
            print(f"{f}", end='')
        print("")

# print_sleep_record(sleep_frequency)

heatmap = []
guards = []
for g in sleep_frequency:
    guards.append(g)
    heatmap.append(sleep_frequency[g])

plt.plot(np.array(heatmap).T)
# plt.show()

most_sleep = 0
sleepiest_guard = None

for g in sleep_frequency:
    total_sleep = sleep_frequency[g].sum()
    if total_sleep > most_sleep:
        most_sleep = total_sleep
        sleepiest_guard = g

sleepiest_minute = np.argmax(sleep_frequency[sleepiest_guard])

print(f"sleepiest guard: {sleepiest_guard}")
print(f"sleepiest minute: {sleepiest_minute}")
print(f"answer: {sleepiest_guard * sleepiest_minute}")
