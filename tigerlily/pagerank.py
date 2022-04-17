"""Personalized PageRank computation with TigerGraph."""

import json
import typing
from typing import Dict, List

import pandas as pd
import pyTigerGraph as tg  # noqa: N813
import requests
from tqdm.notebook import tqdm


class PersonalizedPageRankMachine:
    """Define a drug-protein graph and compute the Personalized PageRank of nodes."""

    def __init__(self, host: str, graphname: str, username: str, secret: str, password: str):
        """Set up a Personalized PageRank computation machine.

        :param host: Address of the TigerGraph host.
        :param graphname: Name of the Graph used for analytics.
        :param username: The username for the grapgh
        :param secret: The secret generated in TigerGraph Studio.
        :param password: The password of the user.
        """
        self._host = host
        self._graphname = graphname
        self._username = username
        self._secret = secret
        self._password = password

    def connect(self):
        """Connect to the host with the authentication details."""
        token_getter = tg.TigerGraphConnection(host=self._host, graphname=self._graphname)

        token = token_getter.getToken(self._secret, "12000")[0]

        self.connection = tg.TigerGraphConnection(
            host=self._host, graphname=self._graphname, username=self._username, password=self._password, apiToken=token
        )

    def _purge_graph(self):
        """Delete the ecisting drug and gene type nodes."""
        self.connection.delVertices("drug")
        self.connection.delVertices("gene")

    def _upload_relationship(self, edges: pd.DataFrame, source: str, target: str, edge_type: str = "interacts"):
        """Given an edge dataframe uploading the edges corresponding to specific source and target types.

        :param edges: Edges dataframe of interest.
        :param source: Source node type.
        :param target: Target node type.
        :param edge_type: The type of edges.
        """
        sub_edges = edges[(edges["type_1"] == source) & (edges["type_2"] == target)]
        sub_edges = [(edge[0], edge[1], {}) for edge in sub_edges[["node_1", "node_2"]].values.tolist()]
        self.connection.upsertEdges(source, edge_type, target, sub_edges)

    def upload_graph(self, new_graph: bool, edges: pd.DataFrame):
        """
        Uploadthe edges from a dataframe using the PyTigerGraph connection.

        :param new_graph: Decision about deleting the existing nodes in the graph.
        :param edges: The dataframe with the edges between drugs and proteins.
        """
        assert "type_1" in edges.columns and "type_2" in edges.columns
        assert "node_1" in edges.columns and "node_2" in edges.columns
        if new_graph:
            self._purge_graph()
        self._upload_relationship(edges, "drug", "gene", "interacts")
        self._upload_relationship(edges, "gene", "gene", "interacts")
        self._upload_relationship(edges, "gene", "drug", "interacts")

    def install_query(
        self,
        url: str = "https://raw.githubusercontent.com/tigergraph/gsql-graph-algorithms/master/algorithms/Centrality/pagerank/personalized/multi_source/tg_pagerank_pers.gsql",  # noqa:E501
    ):
        """Install a query on the host.

        :param url: A url to the query string.
        """
        script = requests.get(url).text
        script = script.replace("CREATE QUERY", "CREATE OR REPLACE QUERY")
        self.connection.gsql(script)
        self.connection.gsql("INSTALL QUERY ALL")

    @typing.no_type_check
    def personalized_pagerank(
        self,
        node_id: str,
        node_type: str = "drug",
        edge_type: str = "interacts",
        print_accum: bool = True,
        damping: float = 0.85,
        iterations: int = 20,
        top_k: int = 40,
    ) -> Dict:
        """Compute the pagerank for a specific node.

        :param node_id: Identifier of the node of interest.
        :param node_type: Type of the node.
        :param edge_type: Type of the edge.
        :param print_accum: Accumulation flag.
        :param damping: Non return probability.
        :param iterations: Number of steps per walk.
        :param top_k: Number of closest neighbors to return for the query.
        :returns: Personalized PageRank nodes for a specific node in the Graph.
        """
        params = {}
        params["source"] = [{"type": node_type, "id": node_id}]
        params["e_type"] = edge_type
        params["print_accum"] = print_accum
        params["damping"] = damping
        params["iter"] = iterations
        params["top_k"] = top_k
        query = "RUN QUERY tg_pagerank_pers(" + json.dumps(params) + ")"
        response = self.connection.gsql(query)
        response = json.loads(response)
        return response

    def get_personalized_pagerank(
        self,
        node_ids: List,
        edge_type: str = "interacts",
        print_accum: bool = True,
        damping: float = 0.5,
        iterations: int = 100,
        top_k: int = 100,
    ) -> pd.DataFrame:
        """
        Compute the pruned Personalized PageRank for a list of nodes.

        :param node_ids: Identifiers of the nodes of interest.
        :param edge_type: Type of the node.
        :param print_accum: Accumulation flag.
        :param damping: Non return probability.
        :param iterations: Number of steps per walk.
        :param top_k: Number of closest neighbors to return for the query.
        :returns: A table of node pairs with PageRank scores.
        """
        all_scores = []
        for node_id in tqdm(node_ids):
            scores = self.personalized_pagerank(
                node_id["v_id"], node_id["v_type"], edge_type, print_accum, damping, iterations, top_k
            )
            scores = scores["results"][0]["top_scores"]
            scores = [[node_id["v_id"], edge["vertex_id"], edge["score"]] for edge in scores]
            scores = pd.DataFrame(scores, columns=["node_1", "node_2", "score"])
            all_scores.append(scores)

        all_scores = pd.concat(all_scores)
        return all_scores
