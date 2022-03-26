import re
from queue import SimpleQueue


def format_round(rd: str) -> int:
    rd_lower = rd.lower()
    # print(f"[format_round] Round: {rd_lower}")
    if (rd_lower == "first four") or (rd_lower == "opening round"):
        return "100"  # marker for preliminary round
    elif "64" in rd_lower:
        return "64"
    elif "32" in rd_lower:
        return "32"
    elif rd_lower == "sweet 16":
        return "16"
    elif rd_lower == "elite eight":
        return "8"
    elif "final four" in rd_lower:
        return "4"
    elif "national championship" in rd_lower:
        return "2"
    elif "national semifinals" in rd_lower:
        return "4"
    elif "regional finals" in rd_lower:
        return "8"
    elif "regional semifinals" in rd_lower:
        return "16"
    else:
        return rd_lower


def format_round_2(current_keys: list[int]) -> int:
    """
    Simply formats round in order from 0 up
    :param current_keys: list of current keys in games dict
    :return: next key
    """
    if len(current_keys) == 0:
        return 0
    return current_keys[-1] + 1


class Game(object):
    children = set()  # child nodes of this game (games where teams were determined)

    def get_is_championship(self):
        return self._is_championship

    def set_is_championship(self, new_value: bool):
        self._is_championship = new_value
        self.tourney_round = "2"  # update tourney round to match

    is_championship = property(get_is_championship, set_is_championship)  # marks whether node is championship game

    def get_team_names(self):
        return map(lambda t: t.name, self.teams)
    team_names = property(get_team_names)

    def get_team1(self):
        return self.teams[0]
    team1 = property(get_team1)

    def get_team2(self):
        return self.teams[1]
    team2 = property(get_team2)

    def get_winner(self):
        # compute winner based on scores
        winner = self.team1 if self.team1.score > self.team2.score else self.team2
        return winner

    def get_loser(self):
        # compute winner based on scores
        loser = self.team2 if self.team1.score > self.team2.score else self.team1
        return loser

    def get_game_summary(self):
        winner = self.get_winner()
        loser = self.get_loser()
        return_string = f"*Round of "
        if self.tourney_round == "-1":
            return_string += "PRELIMS"
        elif self.is_championship:
            return_string += "2"
        else:
            return_string += f"{self.tourney_round.upper()}"
        return_string += "* \t "
        if winner.seed != -1:
            return_string += f"({winner.seed}) {winner.name}"
        else:
            return_string += f"{winner.name}"
        return_string += " beat "
        if loser.seed != -1:
            return_string += f"({loser.seed}) {loser.name}"
        else:
            return_string += f"{loser.name}"
        return_string += f" {winner.score} - {loser.score}"
        return return_string

    def print_game_summary(self):
        print(self.get_game_summary())

    def is_leaf(self):
        # leaf has no child nodes
        return len(self.children) == 0

    def __init__(self, html: str, tourney_round: str):
        if "," in html:
            teams = [Team(team.strip()) for team in html.split(",")]
        else:  # error, no comma in input
            # print(f"[Game] improper input format...{html}")
            i = list(re.finditer("No.", html))[1].start()
            t1 = html[:i-1].strip()
            t2 = html[i:].strip()
            teams = [Team(t1), Team(t2)]
        self.teams = teams
        self.tourney_round = format_round(tourney_round)
        self._is_championship = False
        # print(f"[Team 1] {teams[0].name} vs. [Team 2] {teams[1].name}\n")

    def is_node(self, team_1: str, team_2: str):
        """
        Returns true if the two teams provided match
        :param team_1: name of team 1
        :param team_2: name of team 2
        :return: true if both provided teams are the teams in this game
        """
        names = [self.team1.name, self.team2.name]
        return team_1 in names and team_2 in names

    def show_levels_breadth_first(self, q: SimpleQueue, explored: set):
        """
        Breadth First Search through graph
        :param q: queue containing game objects to search
        :param explored: set containing explored objects
        :return: concatenated str displaying full graph
        """

        q.put(self)  # add this node to queue to start
        graph_string = ""
        while q.qsize() > 0:  # iterate until queue is empty
            # print(f"[bfs] Queue length: {q.qsize()} | Explored: {explored}")
            next_item = q.get()
            if next_item not in explored:
                next_item.print_game_summary()  # print summary
                graph_string += f"{next_item.get_game_summary()}\n"
                explored.add(next_item)  # label route as explored after printing
                if len(next_item.children) > 0:  # stop after getting to leaf
                    for child in next_item.children:
                        if child not in explored:
                            q.put(child)
                            # print(f"  added CHILD of '{self.get_game_summary()}' -> q")
        return graph_string

    def breadth_first_search(self, q: SimpleQueue, explored: set, comp) -> int:
        """
        Breadth First Search through graph
        :param q: queue containing game objects to search
        :param explored: set containing explored objects
        :param comp: lambda used to check for seed or name
        :return: int | highest matching tournament round
        """

        q.put(self)  # add this node to queue to start
        best_round = 1000  # 1000 means no wins in tournament at any level
        while q.qsize() > 0:  # iterate until queue is empty
            # print(f"[bfs] Queue length: {q.qsize()} | Explored: {explored}")
            next_item = q.get()
            if next_item not in explored:
                # print(f"Searching node ---'{self.get_game_summary()}'---")
                res = comp(next_item)  # apply lambda
                if res < best_round:
                    # print(f"Result: {res}")
                    return res
                explored.add(next_item)  # label route as explored after printing
                if len(next_item.children) > 0:  # stop after getting to leaf
                    for child in next_item.children:
                        if child not in explored:
                            q.put(child)
        return best_round


class Team(object):
    """
    Representation for a team within a game
    Example input format: No. 16 North Dakota State 78
    """
    def __init__(self, html: str):
        # print(f"Input: '{html}'")
        score_match = re.search(r"(\d+)$", html)  # last numerical instance
        seed_match = re.search(r"(\d+)[A-Z]? ", html)  # first numerical instance
        self.score = 0 if score_match is None else int(score_match.group(0))
        if seed_match is not None:
            # some seeds have a letter at the end (e.g. 2Q), so get the number portion
            numeric_value = re.search(r"(\d+)", seed_match.group(0)).group(0)
            self.seed = int(numeric_value)
        else:
            self.seed = -1
        start_i = 0 if seed_match is None else seed_match.end()
        end_i = len(html) if score_match is None else score_match.start()-1
        self.name = html[start_i:end_i]  # name is between seed & score
        # print(f"Name: '{self.name}' | Score: {self.score} | Seed: {self.seed}")