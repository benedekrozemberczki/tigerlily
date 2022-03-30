"""BLA"""

import numpy as np

def hadamard_operator(embedding_left, embedding_right):
    return embedding_left * embedding_right

def difference_operator(embedding_left, embedding_right):
    return embedding_left - embedding_right

def l1_norm_operator(embedding_left, embedding_right):
    return np.abs(embedding_left - embedding_right)

def l2_norm_operator(embedding_left, embedding_right):
    return np.square(embedding_left - embedding_right)

def concatenation_operator(embedding_left, embedding_right):
    return np.concat([embedding_left, embedding_right],axis=1)
