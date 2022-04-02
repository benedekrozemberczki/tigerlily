"""Tests for tigerlily."""

from re import L
import unittest


class TestPipeline(unittest.TestCase):
    """Test tigerlily."""

    @classmethod
    def setUpClass(cls):
        cls.dataset = ExampleDataset()
        cls.edges = cls.dataset.read_pagerank()
        cls.target = cls.dataset.read_target()
        cls.pagerank_scores = cls.dataset.read_pagerank()

    def test_embedding(self):

        print(self.edges)
        assert 2 == 2
