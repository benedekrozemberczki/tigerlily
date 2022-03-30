"""BLA"""

import json
import requests
import pandas as pd
import pyTigerGraph as tg
from typing import List
from tqdm.notebook import tqdm

class PersonalizedPageRankMachine:
    
    def __init__(self, host: str, graphname: str, secret: str, password:str):
        self._host = host
        self._graphname = graphname
        self._secret = secret
        self._password = password
        
    def connect(self):
        token_getter = tg.TigerGraphConnection(host=self._host,
                                               graphname=self._graphname)
        
        token = token_getter.getToken(self._secret, "12000")[0]

        self.connection = tg.TigerGraphConnection(host=self._host,
                                                  graphname=self._graphname,
                                                  password=self._password,
                                                  apiToken=token)
        
    def purge_graph(self):
        self.connection.delVertices("drug")
        self.connection.delVertices("gene")
        
    def upload_relationship(self, edges, source:str, target: str, edge_type: str="interacts"):
        sub_edges = edges[(edges["type_1"] == source) & (edges["type_2"] == target)]
        sub_edges = [(edge[0], edge[1], {}) for edge in sub_edges[["node_1","node_2"]].values.tolist()]
        self.connection.upsertEdges(source, edge_type, target, sub_edges)
        
    def upload_graph(self, new_graph: bool, edges: pd.DataFrame):
        assert "type_1" in edges.columns and "type_2" in edges.columns
        assert "node_1" in edges.columns and "node_2" in edges.columns
        self.purge_graph()
        self.upload_relationship(edges, "drug", "gene", "interacts")
        self.upload_relationship(edges, "gene", "gene", "interacts")
        self.upload_relationship(edges, "gene", "drug", "interacts")
        
    def install_query(self, url: str):
        script = requests.get(url).text
        script = script.replace("CREATE QUERY", "CREATE OR REPLACE QUERY")
        self.connection.gsql(script)
        self.connection.gsql("INSTALL QUERY ALL")
        
    def personalized_pagerank(self,
                                  node_id: str,
                                  node_type: str="drug",
                                  edge_type: str="interacts",
                                  print_accum: bool=True,
                                  damping: float=0.5,
                                  iterations: int=100,
                                  top_k: int=100):
        
        parameters = dict()
        parameters["source"] = [{"type":node_type,"id":node_id}]
        parameters["e_type"] = "interacts"
        parameters["print_accum"]  = print_accum
        parameters["damping"] = damping
        parameters["iter"]  = iterations
        parameters["top_k"] = top_k
        query = "RUN QUERY tg_pagerank_pers("+json.dumps(parameters)+")"
        response = self.connection.gsql(query)
        response = json.loads(response)
        return response
    
    def get_personalized_pagerank(self,
                                  node_ids: List,
                                  edge_type: str="interacts",
                                  print_accum: bool=True,
                                  damping: float=0.5,
                                  iterations: int=100,
                                  top_k: int=100):
        all_scores = []
        for node_id in tqdm(node_ids):
            scores = self.personalized_pagerank(node_id["v_id"],
                                                    node_id["v_type"],
                                                    edge_type,
                                                    print_accum,
                                                    damping,
                                                    iterations,
                                                    top_k)
            scores = scores["results"][0]["top_scores"]
            scores = [[node_id["v_id"], edge["vertex_id"], edge["score"]] for edge in scores]
            scores = pd.DataFrame(scores, columns=["node_1","node_2","score"])
            all_scores.append(scores)
    
        all_scores = pd.concat(all_scores)
        return all_scores