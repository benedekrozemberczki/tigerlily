"""Edge feature computation from node features."""

import numpy as np


def hadamard_operator(embedding_left: np.ndarray, embedding_right: np.ndarray) -> np.ndarray:
    """Caclulate the Hadamard operator based edge features.

    :param embedding_left: Left hand side node features.
    :param embedding_right: Right hand side node features.
    :returns: The edge features.
    """
    edge_features = embedding_left * embedding_right
    return edge_features


def difference_operator(embedding_left: np.ndarray, embedding_right: np.ndarray) -> np.ndarray:
    """Caclulate the difference operator based edge features.

    :param embedding_left: Left hand side node features.
    :param embedding_right: Right hand side node features.
    :returns: The edge features.
    """
    edge_features = embedding_left - embedding_right
    return edge_features


def l1_norm_operator(embedding_left: np.ndarray, embedding_right: np.ndarray) -> np.ndarray:
    """Caclulate the L1 norm operator based edge features.

    :param embedding_left: Left hand side node features.
    :param embedding_right: Right hand side node features.
    :returns: The edge features.
    """
    edge_features = np.abs(embedding_left - embedding_right)
    return edge_features


def l2_norm_operator(embedding_left: np.ndarray, embedding_right: np.ndarray) -> np.ndarray:
    """Caclulate the L2 norm operator based edge features.

    :param embedding_left: Left hand side node features.
    :param embedding_right: Right hand side node features.
    :returns: The edge features.
    """
    edge_features = np.square(embedding_left - embedding_right)
    return edge_features


def concatenation_operator(embedding_left: np.ndarray, embedding_right: np.ndarray) -> np.ndarray:
    """Caclulate the concatenation operator based edge features.

    :param embedding_left: Left hand side node features.
    :param embedding_right: Right hand side node features.
    :returns: The edge features.
    """
    edge_features = np.concatenate([embedding_left, embedding_right], axis=1)
    return edge_features
