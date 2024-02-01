from bs4 import BeautifulSoup
import requests
import pandas as pd

# Create valorant ranks list
general_ranks_list = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ascendant", "Immortal"]
ranks_list = [f"{rank} {num}" for rank in general_ranks_list for num in range(1, 4)]
ranks_list.append("Radiant")

# Get url valorant agents statistics all rank
all_url = []
for i in range(3, 28):
    url = f"https://blitz.gg/valorant/stats/agents?sortBy=pickRate&type=general&sortDirection=DESC&mode=competitive&rank={i}&act=e7act3"
    all_url.append(url)

# Get data from each url
for i in range(len(all_url)):
    destination = requests.get(all_url[i])
    soup = BeautifulSoup(destination.content, 'html.parser')

    # Create variable for save data in class
    # Agent
    all_agents_raw = soup.find_all(class_ = "⚡a45ddda9 column col-1 ⚡904d395 sticky")
    all_agents = []

    for agent in all_agents_raw:
        all_agents.append(agent.text)

    # KDA
    all_kda_raw = soup.find_all(class_ = "⚡8a7d61c3")
    all_kda = []

    for kda in all_kda_raw:
        all_kda.append(kda.text)

    all_kill = []
    all_death = []
    all_assist = []

    for kda in all_kda:
        kda = kda.split(" / ")
        all_kill.append(kda[0])
        all_death.append(kda[1])
        all_assist.append(kda[2])

    # K/D
    all_kd_raw = soup.find_all(class_ = "⚡a3efd15e column col-2 ⚡904d395")
    all_kd = []

    for kd in all_kd_raw:
        all_kd.append(kd.text)

    # Win%
    all_win_raw = soup.find_all(class_ = "⚡a3efd15e column col-4 ⚡904d395")
    all_win = []

    for win in all_win_raw:
        all_win.append(win.text)

    # Pick%
    all_pick_raw = soup.find_all(class_ = "⚡a3efd15e column col-5 ⚡904d395")
    all_pick = []

    for pick in all_pick_raw:
        all_pick.append(pick.text)

    # Avg.Score
    all_score_raw = soup.find_all(class_ = "⚡a3efd15e column col-6 ⚡904d395")
    all_score = []

    for score in all_score_raw:
        all_score.append(score.text)

    # Mathces
    all_matches_raw = soup.find_all(class_ = "⚡a3efd15e column col-7 ⚡904d395")
    all_matches = []

    for match in all_matches_raw:
        all_matches.append(match.text)


    # Create DataFrame
    dataframe = pd.DataFrame({
        "Agent": all_agents,
        "Kill": all_kill,
        "Death": all_death,
        "Assist": all_assist,
        "K/D": all_kd,
        "Win%": all_win,
        "Pick%": all_pick,
        "Avg. Score": all_score,
        "Matches": all_matches
    })

    # Convert data type
    # Remove " " and convert string to float
    dataframe["Kill"] = dataframe.apply(lambda m: float(m["Kill"][1:-1]), axis = 1)
    dataframe["Death"] = dataframe.apply(lambda m: float(m["Death"][1:-1]), axis = 1)
    dataframe["Assist"] = dataframe.apply(lambda m: float(m["Assist"][1:-1]), axis = 1)

    # Convert string to float
    dataframe["K/D"] = dataframe["K/D"].astype(float)
    dataframe["Avg. Score"] = dataframe["Avg. Score"].astype(float)

    # Remove "%" and convert string to float
    dataframe["Pick%"] = dataframe.apply(lambda m: float(m["Pick%"][:-1]), axis = 1)
    dataframe["Win%"] = dataframe.apply(lambda m: float(m["Win%"][:-1]), axis = 1)

    # Remove "," and convert string to int
    dataframe["Matches"] = dataframe.apply(lambda x: x["Matches"].replace(",",""), axis = 1)
    dataframe["Matches"] = dataframe["Matches"].astype(int)

    # DataFrame to CSV
    dataframe.to_csv(f"./agents_data/rank {ranks_list[i]}.csv", header = True, index = False)