Tutorial
========



.. contents:: Contents
    :local:

Creating and populating a Graph
------------------------------------

As a first step the basic TigerLily tools are imported and we load the example dataset which integrated DrugBankDDI and the BioSNAP datasets. We create a ``PersonalizedPageRankMachine`` and connect to the host with the Graph. The settings of this machine should be changed with the appropriate user credentials and details; a secret can be obtained in the TigerGraph Graph Studio. We install the default Personalized PageRank query and upload the edges of the example dataset used in our demonstrations. This graph has drug and protein nodes, drug-protein and protein-protein interactions. Our goal is to predict the drug-drug interactions

.. code-block:: python

    from tigerlily.dataset import ExampleDataset
    from tigerlily.embedding import EmbeddingMachine
    from tigerlily.operator import hadamard_operator
    from tigerlily.pagerank import PersonalizedPageRankMachine

    dataset = ExampleDataset()

    edges = dataset.read_edges()
    target = dataset.read_target()

    machine = PersonalizedPageRankMachine(host="host_name",
                                          graphname="graph_name",
                                          secret="secret_value",
                                          password="password_value")
                           
    machine.connect()
    machine.install_query()

    machine.upload_graph(new_graph=True, edges=edges)



Upstream Model Training
-----------------------


.. code-block:: python

    import numpy as np



Downstream Model Training and Scoring
-------------------------------------


.. code-block:: python

    import numpy as np
