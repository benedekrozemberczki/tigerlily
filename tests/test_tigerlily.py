"""Tests for tigerlily."""

import unittest

from tigerlily.dataset import ExampleDataset
from tigerlily.embedding import EmbeddingMachine
from tigerlily.operator import (
    concatenation_operator,
    difference_operator,
    hadamard_operator,
    l1_norm_operator,
    l2_norm_operator,
)
from tigerlily.pagerank import PersonalizedPageRankMachine


class TestPipeline(unittest.TestCase):
    """Test tigerlily."""

    @classmethod
    def setUpClass(cls):
        """Download dataset."""
        cls.dataset = ExampleDataset()
        cls.edges = cls.dataset.read_pagerank()
        cls.target = cls.dataset.read_target()
        cls.pagerank_scores = cls.dataset.read_pagerank()

    def test_embedding(self):
        """Test Embeddings."""
        embedding_machine = EmbeddingMachine()
        scores = embedding_machine.fit(self.pagerank_scores)
        assert scores.shape[1] == 129

    def test_pagerank(self):
        """Test PageRank."""
        pr = PersonalizedPageRankMachine("host", "graph", "user", "secret", "pass")
        assert pr._host == "host"

    def test_operators(self):
        """Test operators."""
        embedding_machine = EmbeddingMachine()
        embedding_machine.fit(self.pagerank_scores)

        drug_pair_features = embedding_machine.create_features(self.target, concatenation_operator)
        assert drug_pair_features.shape[1] == 256

        drug_pair_features = embedding_machine.create_features(self.target, hadamard_operator)
        assert drug_pair_features.shape[1] == 128

        drug_pair_features = embedding_machine.create_features(self.target, difference_operator)
        assert drug_pair_features.shape[1] == 128

        drug_pair_features = embedding_machine.create_features(self.target, l1_norm_operator)
        assert drug_pair_features.shape[1] == 128

        drug_pair_features = embedding_machine.create_features(self.target, l2_norm_operator)
        assert drug_pair_features.shape[1] == 128

    def test_data(self):
        """Test the dataset."""
        self.dataset = ExampleDataset()

        edges = self.dataset.read_edges()
        assert edges.shape == (816683, 4)

        target = self.dataset.read_target()
        assert target.shape == (187850, 3)

        pagerank_scores = self.dataset.read_pagerank()
        assert pagerank_scores.shape == (54110, 3)
