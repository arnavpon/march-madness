import unittest
from ..models.game import Team

class NodeTestCase(unittest.TestCase):

    def test_alphanumeric_input(self):
        html = 'No. 1L Indiana 63'
        team = Team(html)
        self.assertEqual(team.name, "Indiana")
        self.assertEqual(team.seed, 1)
        self.assertEqual(team.score, 63)

    def test_standard_input(self):
        html = 'No. 6 Rutgers 64'
        team = Team(html)
        self.assertEqual(team.name, "Rutgers")
        self.assertEqual(team.seed, 6)
        self.assertEqual(team.score, 64)

    def test_truncated_input(self):
        html = 'Santa Clara 73'
        team = Team(html)
        self.assertEqual(team.name, "Santa Clara")
        self.assertEqual(team.seed, -1)
        self.assertEqual(team.score, 73)


if __name__ == "__main__":
    unittest.main()