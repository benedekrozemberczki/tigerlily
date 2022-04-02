"""Tool to compute Personalized PageRank based embeddings."""

from typing import Callable

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from sklearn.decomposition import NMF


class EmbeddingMachine:
    """Tool to compute Personalized PageRank based embeddings."""

    def __init__(self, seed: int = 42, dimensions: int = 128, max_iter: int = 20):
        """Set  the default hyperparameters of the embeddings.

        :param seed: The random seed for factorization.
        :param dimensions: The number of embedding dimensions.
        :param max_iter: The number of iterations.
        """
        self.seed = seed
        self.dimensions = dimensions
        self.max_iter = max_iter

    def _generate_mappings(self, pagerank_scores):
        node_1_mapping = {node: i for i, node in enumerate(set(pagerank_scores["node_1"].values.tolist()))}
        node_2_mapping = {node: i for i, node in enumerate(set(pagerank_scores["node_2"].values.tolist()))}
        pagerank_scores["node_1_num"] = pagerank_scores["node_1"].map(lambda x: node_1_mapping[x])
        pagerank_scores["node_2_num"] = pagerank_scores["node_2"].map(lambda x: node_2_mapping[x])
        mat = coo_matrix(
            (pagerank_scores["score"], (pagerank_scores["node_1_num"], pagerank_scores["node_2_num"])),
            shape=(len(node_1_mapping), len(node_2_mapping)),
        )

        return pagerank_scores, mat

    def fit(self, pagerank_scores: pd.DataFrame) -> pd.DataFrame:
        """Train an embedding model.

        :param pagerank_scores: A dataframe of the top-k personalized PageRank scores.
        :returns: A node embedding for each source.
        """
        assert "node_1" in pagerank_scores
        assert "node_2" in pagerank_scores
        assert "score" in pagerank_scores
        pagerank_scores, pagerank_mat = self._generate_mappings(pagerank_scores)

        model = NMF(
            n_components=self.dimensions,
            max_iter=self.max_iter,
            random_state=self.seed,
        )

        raw_embedding = model.fit_transform(pagerank_mat)
        raw_embedding = (raw_embedding - raw_embedding.mean(0)) / raw_embedding.std(0)
        embedding = pd.DataFrame(raw_embedding, columns=["emb_" + str(i) for i in range(self.dimensions)])
        pagerank_scores = (
            pagerank_scores[["node_1", "node_1_num"]].drop_duplicates(ignore_index=True).sort_values("node_1_num")
        )
        embedding = pd.concat([pagerank_scores, embedding], axis=1)
        del embedding["node_1_num"]
        self.embedding = embedding.rename(columns={"node_1": "node_id"})
        return self.embedding

    def create_features(
        self, target: pd.DataFrame, feature_definition: Callable[[np.ndarray, np.ndarray], np.ndarray]
    ) -> np.ndarray:
        """Calculate the edge features based on node embeddings.

        :param target: A dataframe of drug-drug interactions.
        :param feature_definition: A Tigerlily edge feature computation function.
        :returns: Drug pair features for each edge.
        """
        self.embedding = self.embedding.set_index("node_id")

        drug_features_left = target[["drug_1"]].rename(columns={"drug_1": "node_id"})
        drug_features_left = drug_features_left.set_index("node_id").join(self.embedding)
        drug_features_left = np.array(drug_features_left.reset_index(drop=True))

        drug_features_right = target[["drug_2"]].rename(columns={"drug_2": "node_id"})
        drug_features_right = drug_features_right.set_index("node_id").join(self.embedding)
        drug_features_right = np.array(drug_features_right.reset_index(drop=True))

        drug_pair_features = feature_definition(drug_features_left, drug_features_right)
        self.embedding = self.embedding.reset_index()
        return drug_pair_features
