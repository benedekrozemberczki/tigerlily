"""A class to read the DrugBankDDI Dataset."""

import io

import pandas as pd
from six.moves import urllib


class ExampleDataset:
    """Class to read the DrugBank DDI Dataset Integrated with BioSNAP."""

    def __init__(
        self,
        base_url: str = "https://raw.githubusercontent.com/benedekrozemberczki/datasets/master/tigerlily_example_data/",
    ):
        """Create the dataset loader.

        :param base_url: The folder with the CSV files.
        """
        self.base_url = base_url

    def _read_table(self, name: str):
        """Read the edges.

        :param name: Name of the csv file.
        :returns: The table with data.
        """
        path = self.base_url + name
        bytes = urllib.request.urlopen(path).read()
        data = pd.read_csv(io.BytesIO(bytes), encoding="utf8", sep=",")
        return data

    def read_edges(self):
        """Read the edges.

        :returns: The protein-drug graph edges dataframe.
        """
        edges = self._read_table("edges.csv")
        return edges

    def read_target(self):
        """Read the target.

        :returns: The drug interaction target dataframe.
        """
        edges = self._read_table("target.csv")
        return edges

    def read_pagerank(self):
        """Read the precomputed PageRank scores for the graph.

        :returns: The PageRank scores.
        """
        pagerank_scores = self._read_table("pagerank_scores.csv")
        return pagerank_scores
