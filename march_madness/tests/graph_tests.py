import unittest

from ..models.search import *

class NodeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.gby = load_all_data()
        cls.full_graph = construct_graphs(cls.gby)

    def test_search_rutgers(self):
        years, max_round = search(self.full_graph, team="Rutgers")
        self.assertEqual(max_round, 8)
        self.assertEqual(len(years), 1)
        for year in years:
            self.assertIn(year, set([1976]))

    def test_search_duke(self):
        years, max_round = search(self.full_graph, team="Duke")
        self.assertEqual(max_round, 2)
        self.assertEqual(len(years), 5)
        for year in years:
            self.assertIn(year, set([1991, 1992, 2001, 2010, 2015]))

    def test_search_unc(self):
        years, max_round = search(self.full_graph, team="North Carolina")
        self.assertEqual(max_round, 2)
        self.assertEqual(len(years), 6)
        for year in years:
            self.assertIn(year, set([1957, 1982, 1993, 2005, 2009, 2017]))

    def test_search_4seed(self):
        years, max_round = search(self.full_graph, seed=4)
        self.assertEqual(max_round, 2)
        self.assertEqual(len(years), 1)
        for year in years:
            self.assertIn(year, set([1997]))

    def test_search_8seed(self):
        years, max_round = search(self.full_graph, seed=8)
        self.assertEqual(max_round, 2)
        self.assertEqual(len(years), 1)
        for year in years:
            self.assertIn(year, set([1985]))

    def test_search_15seed(self):
        years, max_round = search(self.full_graph, seed=15)
        self.assertEqual(max_round, 32)
        self.assertEqual(len(years), 1)
        for year in years:
            self.assertIn(year, set([2013]))

    def test_search_16seed(self):
        years, max_round = search(self.full_graph, seed=16)
        self.assertEqual(max_round, 64)
        self.assertEqual(len(years), 1)
        for year in years:
            self.assertIn(year, set([2018]))

    def test_search_noteam(self):
        years, max_round = search(self.full_graph, team="unknown")
        self.assertEqual(max_round, 1000)
        self.assertEqual(len(years), 2019-1939+1)

    def test_1939(self):
        graph = self.full_graph[1939].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 Oregon beat Ohio State 46 - 33")

    def test_1940(self):
        graph = self.full_graph[1940].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 Indiana beat Kansas 60 - 42")

    def test_1950(self):
        graph = self.full_graph[1950].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 CCNY beat Bradley 71 - 68")

    def test_1960(self):
        graph = self.full_graph[1960].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 Ohio State beat California 75 - 55")

    def test_1970(self):
        graph = self.full_graph[1970].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 UCLA beat Jacksonville 80 - 69")

    def test_1980(self):
        graph = self.full_graph[1980].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 (2) Louisville beat (8) UCLA 59 - 54")

    def test_1990(self):
        graph = self.full_graph[1990].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 (1) UNLV beat (3) Duke 103 - 73")

    def test_2000(self):
        graph = self.full_graph[2000].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 (1) Michigan State beat (5) Florida 89 - 76")

    def test_2009(self):
        graph = self.full_graph[2009].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 (1) North Carolina beat (2) Michigan State 89 - 72")

    def test_2010(self):
        graph = self.full_graph[2010].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 (1) Duke beat (5) Butler 61 - 59")

    def test_2011(self):
        graph = self.full_graph[2011].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 (3) UConn beat (8) Butler 53 - 41")

    def test_2019(self):
        graph = self.full_graph[2019].show()
        self.assertEqual(graph.split("\n")[0], "*Round of 2* 	 (1) Virginia beat (3) Texas Tech 85 - 77")

if __name__ == "__main__":
    unittest.main()