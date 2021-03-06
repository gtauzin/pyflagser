"""Testing for the python API of the C++ flagser `.flag` file I/O."""

import pytest
import os

import numpy as np
from numpy.testing import assert_almost_equal

from pyflagser import load_unweighted_flag, load_weighted_flag, \
    save_weighted_flag
from pyflagser._utils import _extract_unweighted_graph, \
    _extract_weighted_graph


def test_unweighted_fmt(flag_file):
    adjacency_matrix = load_unweighted_flag(flag_file, fmt='coo')
    vertices_coo, edges_coo = _extract_unweighted_graph(adjacency_matrix)
    adjacency_matrix = load_unweighted_flag(flag_file, fmt='dense')
    vertices_dense, edges_dense = _extract_unweighted_graph(adjacency_matrix)
    assert_almost_equal(vertices_coo, vertices_dense)
    assert_almost_equal(edges_coo, edges_dense)


@pytest.mark.parametrize('max_edge_length', [0.1, 0.5, np.inf])
def test_weighted(flag_file, max_edge_length):
    adjacency_matrix = load_weighted_flag(flag_file)
    vertices_a, edges_a = _extract_weighted_graph(adjacency_matrix,
                                                  max_edge_length)
    fname_temp = os.path.split(flag_file)[1]
    save_weighted_flag(fname_temp, adjacency_matrix)
    adjacency_matrix = load_weighted_flag(fname_temp)
    vertices_b, edges_b = _extract_weighted_graph(adjacency_matrix,
                                                  max_edge_length)
    os.remove(fname_temp)
    assert_almost_equal(vertices_a, vertices_a)
    assert_almost_equal(edges_b, edges_b)
