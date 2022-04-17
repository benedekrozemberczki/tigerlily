Tutorial
========



.. contents:: Contents
    :local:

Creating and Populating a Graph
------------------------------------

As a first step, the basic TigerLily tools are imported and we load the example dataset which integrated DrugBankDDI and the BioSNAP datasets. We create a ``PersonalizedPageRankMachine`` and connect to the host with the Graph. The settings of this machine should be changed with the appropriate user credentials and details; a secret can be obtained in the TigerGraph Graph Studio. We install the default Personalized PageRank query and upload the edges of the example dataset used in our demonstrations. This graph has drug and protein nodes, and drug-protein and protein-protein interactions. Our goal is to predict the drug-drug interactions

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
                                          username="user_name",
                                          secret="secret_value",
                                          password="password_value")
                           
    machine.connect()
    machine.install_query()

    machine.upload_graph(new_graph=True, edges=edges)



Computing the Approximate Personalized PageRank Vectors
---------------------------------------------------------------------

We are only interested in describing the neighbourhood of drug nodes in the biological graph. Because of this we only retrieve the neighbourhood of the drugs - for each drug we retrieve those nodes (top-k closest neighbors) which are the closest based on the Personalized PageRank scores. We are going to learn the drug embeddings based on these scores.

.. code-block:: python

    drug_node_ids = machine.connection.getVertices("drug")

    pagerank_scores = machine.get_personalized_pagerank(drug_node_ids)



Learning the Drug Embeddings and Drug Pair Feature Generation
-------------------------------------------------------------

We create an embedding machine that creates drug node representations. The embedding machine instance has a random seed, a dimensions hyperparameter (this sets the number of factors), and a maximal iteration count for the factorization. An embedding is learned from the Personalized PageRank scores and using the drug features we create drug pair features.


.. code-block:: python

    embedding_machine = EmbeddingMachine(seed=42,
                                         dimensions=32,
                                         max_iter=100)

    embedding = embedding_machine.fit(pagerank_scores)

    drug_pair_features = embedding_machine.create_features(target, hadamard_operator)


Predicting Drug Interactions and Inference
-------------------------------------------------------------

We load a gradient boosting-based classifier, an evaluation metric for binary classification, and a function to create train-test splits. We create a train and test portion of the drug pairs using 80% of the pairs for training. A gradient boosted tree model is trained, score the model on the test set. We compute an AUROC score on the test portion of the dataset and print it out.


.. code-block:: python

    from lightgbm import LGBMClassifier
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(drug_pair_features,
                                                        target,
                                                        train_size=0.8,
                                                        random_state=42)

    model = LGBMClassifier(learning_rate=0.01,
                           n_estimators=100)

    model.fit(X_train,y_train["label"])

    predicted_label = model.predict_proba(X_test)

    auroc_score_value = roc_auc_score(y_test["label"], predicted_label[:,1])

    print(f'AUROC score: {auroc_score_value :.4f}')