from .game import Game
from queue import SimpleQueue

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

    def bfs(self, year: int, seed: int = -1, team: str = None) -> list[tuple]:
        """
        Returns farthest instance for a team or seed within a given year. More effective to use BFS than DFS since we're searching top-down (higher -> lower round)
        :return: [tuple(year, max_round)] | use list b/c there may be ties
        """

        if team is not None:

            def team_search(node: Game) -> tuple:
                # find Node where given team won the game
                winner = node.get_winner().name
                if team == winner:
                    print(f" ***Found matching node: {year} ---{node.get_game_summary()}---")
                    try:  # try casting round -> int
                        max_round = int(node.tourney_round)
                    except ValueError:
                        max_round = 100  # 100 is default, indicating some win somewhere
                    return max_round
                return 1000  # none result

            return year, self.championship.breadth_first_search(SimpleQueue(), set(), team_search)

        elif seed != -1:

            def seed_search(node: Game) -> tuple:
                winner = node.get_winner().seed
                if (winner != -1) and (seed == winner):
                    print(f" ***Found matching node: {year} ---{node.get_game_summary()}---")
                    try:
                        max_round = int(node.tourney_round)
                    except ValueError:
                        max_round = 100  # 100 is default, indicating some win somewhere
                    return max_round
                return 1000  # none result

            return year, self.championship.breadth_first_search(SimpleQueue(), set(), seed_search)