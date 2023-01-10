import pandas as pd
import re
from IPython.display import display

path = "data/poker/"
file = "Ancha II-2.50-5-USD-NoLimitHoldem-PokerStars-1-7-2023.txt"

text = open(path +
            file, "r").read()

# split text by three enter keys
text = text.split("\n\n\n")

# regex for parsing hand history
rx_hand_num = r"PokerStars Hand #(\d+)"
rx_stakes = r":  Hold'em No Limit \((\W\d.\d+/\W\d.\d+ \w+)\)"
rx_date = r" - (\d+\/\d+\/\d+ \d+:\d+:\d+ \w+)"
rx_table = r"\nTable '(.+)' "
rx_max_players = r"(\d+)-max "
rx_button = r"Seat #(\d) is the button"
rx_players = r"((?:\n.* \(.\d+.\d+ in chips\)){1,9})"
rx_start = r"((?:\n.*)+)\n\*\*\* HOLE CARDS \*\*\*"
rx_preflop_action = r"((?:\n.*)+)"
rx_flop = r"\n\*\*\* FLOP \*\*\* (\[.*\])"
rx_flop_action = r"(?:((?:\n.*)+)\n\*\*\* TURN \*\*\*"
rx_turn = r" (\[.*\]))?"
rx_turn_action = r"((?:\n.*)+)\n\*\*\* RIVER \*\*\*"
rx_river = r" (\[.*\])"
rx_river_action = r"((?:\n.*)+)\n\*\*\* SUMMARY \*\*\*"
rx_summary = r"((?:\n.*)+)"

# combine regex
pattern = rx_hand_num + rx_stakes + rx_date + rx_table + rx_max_players + rx_button + rx_players + rx_start + rx_preflop_action + rx_flop + rx_flop_action + rx_turn + rx_turn_action + rx_river + rx_river_action + rx_summary

# compile regex
hand_history_regex = re.compile(pattern)

# create lists to store data
hand_num = []
stakes = []
date = []
table = []
max_players = []
button = []
players = []
start = []
preflop_action = []
flop = []
flop_action = []
turn = []
turn_action = []
river = []
river_action = []
summary = []

starting_fields = [hand_num, stakes, date, table, max_players, button, players, start, preflop_action, flop, flop_action, turn, turn_action, river, river_action, summary]

for i in range(len(text)):
    mo = hand_history_regex.search(text[i])
    if mo:
        for j in range(len(starting_fields)):
            starting_fields[j].append(mo.group(j+1))

df = pd.DataFrame({
    "hand_num": hand_num,
    "stakes": stakes,
    "date": date,
    "table": table,
    "max_players": max_players,
    "button": button,
    "players": players,
    "start": start,
    "preflop": preflop_action,
    "flop": flop,
    "flop_action": flop_action,
    "turn": turn,
    "turn_action": turn_action,
    "river": river,
    "river_action": river_action,
    "summary": summary
})

# print the first 5 rows of the dataframe
display(df.head())

print(pattern)