import pandas as pd
import re

path = "data/poker/"
file = "Ancha II-2.50-5-USD-NoLimitHoldem-PokerStars-1-7-2023.txt"

text = open(path +
            file, "r").read()

# split text by three enter keys
text = text.split("\n\n\n")

# function that takes in one or more regex 
# strings, concatenates them, and adds the 
# result to a non-capturing group and gives 
# the group a quantifier of 0 or 1, then 
# returns the result
def optional(*args):
    return "(?:" + "".join(args) + ")?"

# regex for parsing hand history
rx_hand_num = r"PokerStars Hand #(\d+)"
rx_stakes = r":  Hold'em No Limit \((\W\d.\d+/\W\d.\d+ \w+)\)"
rx_date = r" - (\d+\/\d+\/\d+ \d+:\d+:\d+ \w+)"
rx_table = r"\nTable '(.+)' "
rx_max_players = r"(\d+)-max "
rx_button = r"Seat #(\d) is the button"
rx_players = r"((?:\n.* \(.\d+.\d+ in chips\)){1,9})"
rx_start = r"((?:\n.*)+)\n\*\*\* HOLE CARDS \*\*\*"
rx_preflop_action = r"((?:\n[^\*].*)+)"
rx_flop = r"\n\*\*\* FLOP \*\*\* (\[.*\])"
rx_turn = r"\n\*\*\* TURN \*\*\* (\[.*\])"
rx_river = r"\n\*\*\* RIVER \*\*\* (\[.*\])"
rx_summary = r"\n\*\*\* SUMMARY \*\*\*((?:\n.*)+)"

rx_action = r"((?:\n[^\*].*)+)"

rx_river_optional = optional(rx_river, rx_action)
rx_turn_and_river_optional = optional(rx_turn, rx_action, rx_river_optional)
rx_flop_turn_and_river_optional = optional(rx_flop, rx_action, rx_turn_and_river_optional)

# combine regex
pattern = rx_hand_num + rx_stakes + rx_date + rx_table + rx_max_players + rx_button + rx_players + rx_start + rx_preflop_action + rx_flop_turn_and_river_optional + rx_summary

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

# parse preflop column
rx_limped = r"(?:.*[^(raises)]\n){0,}.*raises (.\d+.?\d{0,2}) to (.\d+.?\d{0,2})\n(?:.*\n){0,}.*(?:raises (.\d+.?\d{0,2}) to (.\d+.?\d{0,2}))"
df['pf_raise'] = df.preflop.str.extract(rx_limped)[0]
df['pf_3b'] = df.preflop.str.extract(rx_limped)[2]

print(df.head())