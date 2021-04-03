import json, re

pkmn_file_name = "pkmn_changes.txt"
base_stats_token = "Base Stats (Complete):"
type_token = "Type (Complete):"
separator = "==================="
stats_regex = r"(?P<hp>\d*) HP \/ (?P<at>\d*) Atk \/ (?P<df>\d*) Def \/ (?P<sa>\d*) SAtk \/ (?P<sd>\d*) SDef \/ (?P<sp>\d*) Spd \/ \d* BST"

final_json = {}

def from_match(groups):
    gname = ["hp", "at", "df", "sa", "sd", "sp"]
    return {k:int(v) for (k, v) in zip(gname, groups)}

def treat_separated_list(sep_list):
    pkmn_names = [x.split(" - ")[1].strip() for x in sep_list[1:-1:2]]
    for n, name in enumerate(pkmn_names):
        data = sep_list[(n + 1) * 2]
        changes = {}
        if base_stats_token in data:
            stats_pos = data.split(base_stats_token)[1].split("New")[1].split("\n")[0].strip() 
            m = re.match(stats_regex, stats_pos)
            changes.update({"bs": from_match(m.groups())})
        if type_token in data:
            type_pos = data.split(type_token)[1].split("New")[1].split("\n")[0].strip() 
            types = [x.strip() for x in type_pos.split(" / ")]
            changes.update({"types": types})
        if not changes == {}:
            final_json.update({name: changes})

with open(pkmn_file_name) as pkmn_file:
    treat_separated_list(pkmn_file.read().split(separator))

s = json.dumps(final_json, indent=2)
print(s.replace("\"", "'"))
