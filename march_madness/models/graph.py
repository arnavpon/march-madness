from queue import SimpleQueue
from .game import Game, Team
from ..helpers import string_formatting as sf

class Graph(object):

    """
    A graph maps a given tournament year against the games played in that year
    The "game_structure" is a single Game object
     - the children of the initial object contain the other nodes
    """

    def __init__(self, year: int, championship: Game):
        self.year = year
        self.championship = championship

    def show(self) -> str:
        print(f"\n\n[show_graph] Year {self.year}")
        return self.championship.show_levels_breadth_first(SimpleQueue(), set())  # ***

    def bfs(self, year: int, seed: int = -1, team: str = None) -> tuple:
        """
        Returns farthest instance for a team or seed within a given year. More effective to use BFS than DFS since we're searching top-down (higher -> lower round)
        :return: tuple( year: int, best_result: tuple(round_number, team_name) )
        """

        if team is not None:

            def team_search(node: Game) -> tuple:
                """
                Searches for nodes where the specified Team won the game
                :param node: in game graph
                :return: tuple(round: int, None)
                """

                winner = node.get_winner().name
                if sf.format_string_for_comparison(team) == sf.format_string_for_comparison(winner):
                    print(f" ***Found matching node: {year} ---{node.get_game_summary()}---")
                    try:  # try casting round -> int
                        max_round = int(node.tourney_round)
                    except ValueError:
                        max_round = Team.RESULT_WIN_UNKNOWN_ROUND  # 100 is default
                    return max_round, None
                return Team.RESULT_NO_WINS, None  # none result

            return year, self.championship.breadth_first_search(SimpleQueue(), set(), team_search)

        elif seed != -1:

            def seed_search(node: Game) -> tuple:
                """
                Searches for nodes where the specified seed WON the game
                :param node: in game graph
                :return: tuple(round: int, team: str)
                """
                winner = node.get_winner()
                if (winner.seed != -1) and (seed == winner.seed):
                    print(f" ***Found matching node: {year} ---{node.get_game_summary()}---")
                    try:
                        max_round = int(node.tourney_round)
                    except ValueError:
                        max_round = Team.RESULT_WIN_UNKNOWN_ROUND
                    return max_round, winner.name  # return team for that seed
                return Team.RESULT_NO_WINS, ""  # no win result - don't return team

            return year, self.championship.breadth_first_search(SimpleQueue(), set(), seed_search)