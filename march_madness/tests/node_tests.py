import unittest
from ..models.search import *

class NodeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.gby = load_all_data()
        cls.full_graph = construct_graphs(cls.gby)

    def test_1939(self):
        graph = self.full_graph[1939].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Oregon")
        self.assertEqual(loser, "Ohio State")

    def test_1940(self):
        graph = self.full_graph[1940].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Indiana")
        self.assertEqual(loser, "Kansas")

    def test_1941(self):
        graph = self.full_graph[1941].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Wisconsin")
        self.assertEqual(loser, "Washington State")

    def test_1945(self):
        graph = self.full_graph[1945].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Oklahoma A&M")
        self.assertEqual(loser, "NYU")

    def test_1948(self):
        graph = self.full_graph[1948].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Kentucky")
        self.assertEqual(loser, "Baylor")

    def test_1952(self):
        graph = self.full_graph[1952].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Kansas")
        self.assertEqual(loser, "St. John's")

    def test_1958(self):
        graph = self.full_graph[1958].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Kentucky")
        self.assertEqual(loser, "Seattle")

    def test_1963(self):
        graph = self.full_graph[1963].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Loyola Chicago")
        self.assertEqual(loser, "Cincinnati")

    def test_1964(self):
        graph = self.full_graph[1964].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "UCLA")
        self.assertEqual(loser, "Duke")

    def test_1969(self):
        graph = self.full_graph[1969].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "UCLA")
        self.assertEqual(loser, "Purdue")

    def test_1972(self):
        graph = self.full_graph[1972].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "UCLA")
        self.assertEqual(loser, "Florida State")

    def test_1978(self):
        graph = self.full_graph[1978].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Kentucky")
        self.assertEqual(loser, "Duke")

    def test_1982(self):
        graph = self.full_graph[1982].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "North Carolina")
        self.assertEqual(loser, "Georgetown")

    def test_1988(self):
        graph = self.full_graph[1988].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Kansas")
        self.assertEqual(loser, "Oklahoma")

    def test_1992(self):
        graph = self.full_graph[1992].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Duke")
        self.assertEqual(loser, "Michigan")

    def test_1998(self):
        graph = self.full_graph[1998].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Kentucky")
        self.assertEqual(loser, "Utah")

    def test_2002(self):
        graph = self.full_graph[2002].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Maryland")
        self.assertEqual(loser, "Indiana")

    def test_2008(self):
        graph = self.full_graph[2008].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Kansas")
        self.assertEqual(loser, "Memphis")

    def test_2012(self):
        graph = self.full_graph[2012].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Kentucky")
        self.assertEqual(loser, "Kansas")

    def test_2018(self):
        graph = self.full_graph[2018].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Villanova")
        self.assertEqual(loser, "Michigan")

    def test_2019(self):
        graph = self.full_graph[2019].championship
        winner = graph.get_winner().name
        loser = graph.get_loser().name
        self.assertEqual(winner, "Virginia")
        self.assertEqual(loser, "Texas Tech")


if __name__ == "__main__":
    unittest.main()