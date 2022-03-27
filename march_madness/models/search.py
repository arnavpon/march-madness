import json
import os
from pprint import pprint
from collections import OrderedDict

from march_madness.models.game import *
from march_madness.models.graph import Graph
from ..helpers import string_formatting as sf

# convert this into tree structure for search by Game, organized by year
# standardize titles so we can query by round

def load_all_data() -> OrderedDict:
    """
    Constructs game dictionaries for each tournament year
    Format { game : { round : [Game] } }
    :return: ordered dict
    """
    games_by_year = OrderedDict()
    for year in range(1939, 2020):
        data = load_data_for_year(year)
        if data is not None:
            games_by_year[year] = data
        else:
            print(f"[load_all_data] No data for year {year}")
    # print(f"\n[games_by_year] Year {year}:")
    # pprint(games_by_year)
    return games_by_year


def load_data_for_year(year: int) -> OrderedDict:
    """
    Formats HTML elements into Game objects, then
      constructs graph of all tournament years and all games played
    :param year: int | year of tournament
    :return: dict | { round : [Game] }
    """
    # print(f"\n\n[load_data_for_year] Year {year}")
    path = os.path.join(os.getcwd(), f"./march_madness/data/bracket_{year}.jl")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        games = OrderedDict()
        games_raw = json.load(f)
        for tourney_round, game_data in games_raw.items():
            tr = format_round_2(list(games.keys()))
            # print(f"Round (Level): {tr}")
            game_data_1 = [g for g in game_data if "\n\t\t\t" not in g]
            game_data_2 = [re.sub(r"<.*?>", "", g) for g in game_data_1]
            game_data_3 = [g.replace("\u00a0", " ") for g in game_data_2]
            game_data_4 = [g.replace("&amp;", "&") for g in game_data_3]
            game_data_5 = [g.split("|")[0].strip() for g in game_data_4]
            game_data_6 = [re.sub(r"^.*?No\.", "No.", g) for g in game_data_5]
            game_data_7 = [re.sub(r" \([\d]?OT\)$", "", g) for g in game_data_6]
            gms = [Game(game, tourney_round) for game in game_data_7]
            if tr in games:  # update
                existing = games[tr]
                for gm in gms:
                    existing.append(gm)
                games[tr] = existing
            else:  # add
                games[tr] = gms
        return games


def generate_graph_for_year(games: dict, year: int) -> Graph:
    """
    Returns all nodes for a given level of the Graph | 0 -> leaf, 1 -> after leaf, ...
    :param games: dict of all games
    :param year: int | tournament year
    :return: Graph for year
    """

    # print(f"\n\n[generate_graph_for_year] Year {year}")
    final_game = trawl_graph(-1, OrderedDict(), games[year])
    return Graph(year, final_game)


def is_node_leaf(level: int, node: Game, nodes_below_level: OrderedDict) -> bool:
    """
    Checks if the node is a leaf
     - Answers the question: "Did one of the teams playing in the current game have to win a game at an earlier level?" If not, it is a leaf.
    :param level: int | level in graph of node
    :param node: Game
    :param nodes_below_level: dict of all games at LOWER levels than "level"
    :return: true if leaf, false if not
    """

    # print(f"\n[leaf_node_check] Level {level} | Game: {node.get_game_summary()}")
    t1 = node.team1.name
    t2 = node.team2.name
    if level == 0:  # lowest level guaranteed to be leaves
        # print("**leaf**")
        return True
    else:
        winners = set()
        for i in range(0, level):  # get ALL winners at any level below this one
            nds = nodes_below_level[i]
            for nd in nds:
                winners.add(nd.get_winner().name)
        if (t1 not in winners) and (t2 not in winners):
            # print("**leaf**")
            return True
        # print("--node--")
    return False


def get_child_nodes(node: Game, nodes_below: OrderedDict) -> set[Game]:
    """
    For a given non-leaf node, finds the child nodes in the below levels
     - Note: a child node determines one of the teams playing the current Game
     - Note: children are not guaranteed to be exactly 1 level down, but they must be at a lower level
    :param node: game for which we want to find children
    :param nodes_below: games that happened earlier in tournament
    :return: set of child nodes (Game objects)
    """

    # print("  looking for children...")
    children = set()
    t1 = node.team1.name
    t2 = node.team2.name
    keys = list(nodes_below.keys())
    level_below = keys[-1]  # start with last key in list
    for game in nodes_below[level_below]:
        # print(f"  game:  {game.get_game_summary()}")
        if t1 == game.get_winner().name or t2 == game.get_winner().name:
            # print(f"\tfound child:    {game.get_game_summary()}")
            children.add(game)

    if len(children) == 0:  # some games have only 1 child (1 team played qualifier)
        # print(f"Didn't find children, step down a level...")
        if len(keys) > 1:  # more than 1 key remaining
            cp = nodes_below.copy()
            del(cp[level_below])
            return get_child_nodes(node, cp)
        else:
            # print("Error: no levels remaining!")
            pass
    return children


def trawl_graph(level: int, nodes: OrderedDict, remaining_nodes: OrderedDict) -> Game:
    """
    Starts from leaves & trawls up graph recursively till championship
    :param level: int | current level of recursion, 0 -> leaf
    :param nodes: ordered dict | games in order of round, w/ children set
    :param remaining_nodes: ordered dict | games w/o children set yet
    :return: Game | returns single game, with children assigned appropriately
    """

    current = [node for node_ls in nodes.values() for node in node_ls]
    remaining = [node for node_ls in remaining_nodes.values() for node in node_ls]
    # print(f"\n[trawl_graph] Level {level} | # Current Nodes: {len(current)} | # Nodes Remaining: {len(remaining)}")
    remaining_levels = list(remaining_nodes.keys())
    # print(f"{remaining_levels} remaining levels to trawl...")
    while len(remaining_levels) > 0:  # there remain levels to be trawled
        next_level = remaining_levels[0]
        formatted_nodes = list()
        for node in remaining_nodes[next_level]:
            if not is_node_leaf(next_level, node, nodes):
                # if node is not a leaf, add children to current node before recursion
                node.children = get_child_nodes(node, nodes)
            formatted_nodes.append(node)
        nodes[next_level] = formatted_nodes  # assign formatted nodes to dict
        del (remaining_nodes[next_level])  # remove nodes from remaining
        return trawl_graph(next_level, nodes, remaining_nodes)

    return get_championship(nodes)  # stopping condition - return top-level game


def all_games_in_tournament(games: OrderedDict) -> list[Game]:
    """
    Generates flat list of all games
    :param games: all games
    :return:
    """
    flat_games = []
    for key, val in games.items():
        for game in val:
            flat_games.append(game)
    return flat_games


def get_championship(nodes: OrderedDict) -> Game:
    """
    Sets children & returns championship Game object
     - Note: NOT guaranteed that championship is final game or only game on level
    :param nodes: full dict of all games in order, w/ children set
    :return: championship Game object
    """

    # print("\n[get_championship]")
    for lvl in list(nodes.keys())[::-1]:  # traverse node dict in reverse order
        # print(f"Level {lvl}")

        for gm in all_games_in_tournament(nodes):
            if gm.tourney_round == "2":
                # check if any game is marked w/ "2" round -> championship
                node_cp = nodes.copy()
                del (node_cp[lvl])
                gm.children = get_child_nodes(gm, node_cp)
                gm.is_championship = True
                # print(f"!!! CHAMPION - {gm.get_game_summary()} !!!   *by round num*")
                return gm

        if len(nodes[lvl]) == 1:
            gm = nodes[lvl].pop()
            if not gm.is_leaf():
                # only 1 NON-leaf game in round -> championship
                node_cp = nodes.copy()
                del(node_cp[lvl])
                gm.children = get_child_nodes(gm, node_cp)
                gm.is_championship = True
                # print(f"!!! CHAMPION - {gm.get_game_summary()} !!!   *lone leaf*")
                return gm

        winners = list()
        for node in nodes[lvl]:
            if node.is_leaf():  # leaf this high up must be 3rd place game
                # print(" third place game")
                break
            winner = node.get_winner().name
            if winner not in winners:
                winners.append(winner)
            else:  # 2nd occurrence of winner -> championship
                nodes_cp = nodes[lvl].copy()
                nodes_cp.remove(node)  # remove this node from node list
                dict_cp = nodes.copy()  # copy full node dict
                dict_cp[lvl] = nodes_cp  # replace level w/ modified node ls
                node.children = get_child_nodes(node, dict_cp)
                node.is_championship = True
                # print(f"!!! CHAMPION - {node.get_game_summary()} !!!   *twice winner*")
                return node  # championship game is one where winner is not in list of losers
    print("ERROR - no champ found :(")


def construct_graphs(games_by_year: OrderedDict) -> dict:
    """
    Starting from the dict containing { round : games }, constructs Graph of tournament structure for the year
     - each node is a Game (top node is championship)
     - each child of a node is the previous Game played by the teams in the current Game
     - leaf: a game where the two teams in it did NOT win to get into that game
    :param games_by_year: dict w/ all games indexed by year
    :return: dict | key = year, value = Graph
    """

    graph = dict()
    for year in games_by_year.keys():
        graph[year] = generate_graph_for_year(games_by_year, year)
    return graph


def search(full_graph: dict, team: str = None, seed: int = -1) -> dict:
    """
    Searches and returns the farthest a team or seed has advanced
    :param full_graph: key = year, value = Graph
    :param team: str | team name to search on
    :param seed: int | seed number to search on
    :return: dict(best_result_by_round: <object>) | 1000: no wins, 100: unnumbered rounds
    """

    print("\n\n[search] Starting full graph search...")
    if team is not None:
        return search_for_team(full_graph, team)
    elif seed != -1:
        return search_for_seed(full_graph, seed)


def search_for_team(full_graph: dict, team: str) -> dict:
    """
    Searches through full graph for best results by given TEAM
    :param full_graph:
    :param team: str | name
    :return: dict(best_result_by_round: [year])
    """

    print(f"[search] Searching graph for team '{team}'...")
    results = dict()
    for year in full_graph.keys():
        _, result_tuple = full_graph[year].bfs(year, team=team)
        result, team_name = result_tuple
        if result in results.keys():  # result was achieved in previous year
            existing_years = results[result]
            existing_years.append(year)  # add to END of list to preserve order
            results[result] = existing_years
        else:  # new result type
            results[result] = [year]

    print("\n")
    sorted_keys = sorted(results.keys())  # sort low -> high (best -> worst finishes)
    counter = 0
    for round_number in sorted_keys:
        years = results[round_number]
        formatted_round = format_round_number(round_number, len(sorted_keys))
        if formatted_round != "":  # ignore empty result, continue loop
            y = [f"{yr}" for yr in years]
            if counter == 0:
                print(f"Best result for '{sf.format_string_for_display(team)}' is win in <{formatted_round}> in {', '.join(y)}")
            else:
                print(f"Other results: win in <{formatted_round}> in {', '.join(y)}")
        counter += 1
    return results


def search_for_seed(full_graph: dict, seed: int) -> dict:
    """
    Searches through full graph for best results by given SEED
    :param full_graph
    :param seed: int | number of desired seed to search
    :return: dict(best_result_by_round: team: [year])  -differs from "team search" result
    """

    print(f"[search] Searching graph for seed #{seed}...")
    results = dict()
    for year in full_graph.keys():
        _, result_tuple = full_graph[year].bfs(year, seed=seed)
        result, team_name = result_tuple
        if result in results.keys():  # result was achieved in previous year
            years_by_team = results[result]  # dict(team: year)
            if team_name in years_by_team:  # team already exists
                results_for_team = years_by_team[team_name]
                results_for_team.append(year)
                years_by_team[team_name] = results_for_team  # add year to list
            else:  # new team
                years_by_team[team_name] = [year]  # create list
            results[result] = years_by_team
        else:  # new result type
            results[result] = {team_name: [year]}

    print(f"\nBest results for a #{seed} Seed:")
    sorted_keys = sorted(results.keys())  # sort low -> high (best -> worst finishes)
    if len(sorted_keys) == 1:
        print("Never won a March Madness game")
    else:
        for round_number in sorted_keys:
            format_round = format_round_number(round_number, len(years_by_team.keys()))
            if format_round != "":
                print(f"  Win in <{format_round}>")
                years_by_team = results[round_number]  # { team_name: [years] }
                for team, years in years_by_team.items():
                    y = [f"{yr}" for yr in years]
                    print(f"    Team '{sf.format_string_for_display(team)}' in {', '.join(y)}")
    return results


def format_round_number(r: int, n_keys: int) -> str:
    """
    Returns formatted string based on input 'best round' result
    :param r: round as int
    :param n_keys: number of keys in results dict (reflects # of unique tourney results)
    :return: round as str
    """

    if r == Team.RESULT_NO_WINS:  # no wins anywhere
        if n_keys > 1:  # team has won a tournament game in 1 year
            return ""  # pass in loop
        return "never won a March Madness game"
    elif r == Team.RESULT_WIN_UNKNOWN_ROUND:  # win in unmarked round
        return "PRELIMINARY Round"
    elif r == 2:
        return "CHAMPIONSHIP"
    else:
        return f"Round of {r}"