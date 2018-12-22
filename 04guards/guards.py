import sys
import re
import datetime
import pandas as pd

pattern = re.compile("^\\[([0-9]{4}-[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9])\\] (.*)$")

def datetime_from_entry(s):
    datetime_format = "%Y-%m-%d %H:%M"
    return datetime.datetime.strptime(pattern.match(s).group(1), datetime_format)

def data_from_entry(s):
    return pattern.match(s).group(2)

def time(s):
    return s[12:17]

with open(sys.argv[1]) as f:
    current_guard = None
    current_date = None
    sequence = [(datetime_from_entry(line.strip()),
        data_from_entry(line.strip())) for line in f]

frame = pd.DataFrame(sequence)

print(frame.head())
