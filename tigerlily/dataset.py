
"""A class to read the DrugBankDDI Dataset."""

import io
import urllib
import pandas as pd


class ExampleDataset:
    """Class to read the DrugBank DDI Dataset Integrated with BioSNAP."""
    def __init__(self, base_url: str="https://raw.githubusercontent.com/benedekrozemberczki/datasets/master/tigerlily_example_data/"):
        self.base_url = base_url


    def _read_table(self, name: str):
        """Method to read the edges.
        Args:
            name (str): Name of the csv file.
    
        Returns:
            data (pd.DataFrame): The table with data.
        """
        path = self.base_url + name
        bytes = urllib.request.urlopen(path).read()
        data = pd.read_csv(io.BytesIO(bytes), encoding="utf8", sep=",")
        return data

    def read_edges(self):
        """Method to read the edges.

        Returns:
            edges (pd.DataFrame): The protei-drug graph edges dataframe.
        """
        edges = self._read_table("edges.csv")
        return edges

    def read_target(self):
        """Method to read the target.

        Returns:
            target (pd.DataFrame): The drug interaction target dataframe.
        """
        edges = self._read_table("target.csv")
        return edges

    def read_pagerank(self):
        """Method to read the precomputed PageRank scores for the graph.

        Returns:
            pagerank_scores (pd.DataFrame): The PageRank scores.
        """
        pagerank_scores = self._read_table("pagerank_scores.csv")
        return pagerank_scores