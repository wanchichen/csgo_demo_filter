import os
import pandas as pd
import shutil
import argparse
import copy

parser = argparse.ArgumentParser()

parser.add_argument('--players', nargs='*', default=["shox"])
parser.add_argument('--stats', nargs='*', default=["4K", "5K", "1v3 won", "1v4 won", "1v5 won", "Knife"])
parser.add_argument('--demo_folder', default="C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\replays")
parser.add_argument('--copy_demos', default='False', type=str)

args = parser.parse_args()

PLAYERS = args.players
INTERESTING_STATS = ["Name"] + args.stats
DEMO_FOLDER = args.demo_folder

excel_files = os.listdir()
out_df = pd.DataFrame()

for excel_file in excel_files:
    if(excel_file.find(".xlsx") > 0):
        player_stats = pd.read_excel(excel_file, sheet_name=1, engine="openpyxl", header=0)
        kills = pd.read_excel(excel_file, sheet_name=3, engine="openpyxl", header=0)

        for player in PLAYERS:

            keep_player_stat = False
            player_in_game = player_stats.index[player_stats['Name'] == player].tolist() 

            if(len(player_in_game) > 0):
                player_index = player_in_game[0]
                filter_stats = copy.deepcopy(INTERESTING_STATS)
                filter_stats.remove("Knife")
                stat_matrix = player_stats[filter_stats].iloc[player_index]

                player_kills = kills[kills['Killer'] == player]
                player_got_knife_kill = player_kills.index[player_kills['Weapon'] == 'Knife'].tolist() 
                if (len(player_got_knife_kill) > 0):
                    keep_player_stat = True
                    stat_matrix["Knife"] = True

                for stat in INTERESTING_STATS:
                    if (stat != "Name" and stat != "Knife"):
                        if (stat_matrix[stat] > 0):
                            keep_player_stat = True
                            break

                if (keep_player_stat == True):
                    stat_matrix["Match"] = f'{excel_file.split("-export.xlsx")[0]}.dem'
                    out_df = out_df.append(stat_matrix)

out_df.to_csv("summary.csv", index=False, columns=["Match"]+INTERESTING_STATS)

matches_to_save = out_df['Match'].unique()
try:
    os.mkdir("demos")
except:
    pass

if (args.copy_demos != 'False'):
    for match in matches_to_save:
        src = f"{DEMO_FOLDER}\\{match}"
        dest = f"demos\\{match}"
        shutil.copyfile(src, dest)
