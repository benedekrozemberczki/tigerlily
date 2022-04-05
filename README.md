[pypi-image]: https://badge.fury.io/py/tigerlily.svg
[pypi-url]: https://pypi.python.org/pypi/tigerlily
[size-image]: https://img.shields.io/github/repo-size/benedekrozemberczki/tigerlily.svg
[size-url]: https://github.com/benedekrozemberczki/tigerlily/archive/main.zip
[build-image]: https://github.com/benedekrozemberczki/tigerlily/workflows/CI/badge.svg
[build-url]: https://github.com/benedekrozemberczki/tigerlily/actions?query=workflow%3ACI
[docs-image]: https://readthedocs.org/projects/tigerlily/badge/?version=latest
[docs-url]: https://tigerlily.readthedocs.io/en/latest/?badge=latest
[coverage-image]: https://codecov.io/gh/benedekrozemberczki/tigerlily/branch/main/graph/badge.svg
[coverage-url]: https://codecov.io/github/benedekrozemberczki/tigerlily?branch=main


[![PyPI Version][pypi-image]][pypi-url]
[![Docs Status][docs-image]][docs-url]
[![Code Coverage][coverage-image]][coverage-url]
[![Build Status][build-image]][build-url]


<p align="center">
  <img width="100%" src="https://github.com/benedekrozemberczki/tigerlily/blob/main/images/tigerlily_logo.jpg?sanitize=true" />
</p>





--------------------------------------------------------------------------------

### **Drug Interaction Prediction with Tigerlily**

**[Documentation](https://tigerlily.readthedocs.io)** | **[Example Notebook](https://github.com/benedekrozemberczki/tigerlily/blob/main/example_notebook.ipynb)** 



**Tigerlily** is a [TigerGraph](https://www.tigergraph.com/) based system designed to solve the [drug interaction prediction task](https://arxiv.org/abs/2111.02916). In this machine learning task we want to predict whether two drugs have an adverse interaction. Our framework allows to solve this **[highly relevant real world problem](https://www.newscientist.com/article/2143486-side-effects-kill-thousands-but-our-data-on-them-is-flawed/)** using graph mining techniques in these steps: 

- **(a)** Using [PyTigergraph](https://github.com/pyTigerGraph/pyTigerGraph) we create a heterogeneous biological graph of drugs and proteins.
- **(b)** We calculate the [personalized PageRank](https://github.com/tigergraph/gsql-graph-algorithms/blob/master/algorithms/Centrality/pagerank/personalized/multi_source/tg_pagerank_pers.gsql) scores of drug nodes in the [TigerGraph Cloud](https://tgcloud.io/).
- **(c)** We embed the nodes using [sparse non-negative matrix factorization](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html) of the personalized PageRank matrix.
- **(d)** Using the node embeddings we train a [gradient boosting](https://lightgbm.readthedocs.io/en/latest/) based drug interaction predictor.

<p align="center">
  <img width="90%" src="https://github.com/benedekrozemberczki/tigerlily/blob/main/images/pair_scoring.jpg?sanitize=true" />
</p>

--------------------------------------------------------------------------------


### (A) **Creating and populating a Graph**

The API of `tigerlily` ....

```python
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
```


### (B) **Computing the Approximate Personalized PageRank vectors**

```python
drug_node_ids = machine.connection.getVertices("drug")

pagerank_scores = machine.get_personalized_pagerank(drug_node_ids)
```
### (C) Learning the Drug Embeddings and Drug Pair Feature Generation


```python
embedding_machine = EmbeddingMachine(seed=42,
                                     dimensions=32,
                                     max_iter=100)

embedding = embedding_machine.fit(pagerank_scores)

drug_pair_features = embedding_machine.create_features(target, concatenation_operator)
```
### (D) Learning to Predict Drug Interactions and Inference

```python
X_train, X_test, y_train, y_test = train_test_split(X=drug_pair_features,
                                                    y=target,
                                                    train_size=0.8,
                                                    random_state=42)

model = LGBMClassifier(learning_rate=0.01,
                       n_estimators=100)

model.fit(X_train,y_train["label"])

predicted_label = model.predict_proba(X_test)

auroc_score_value = roc_auc_score(y_test["label"], predicted_label[:,1])

print(f'AUROC score: {auroc_score_value :.4f}')
```

Head over to our [documentation](https://tigerlily.readthedocs.io) to find out more about installation and a full API reference.
For a quick start, check out the [example notebook](https://github.com/benedekrozemberczki/tigerlily/blob/main/example_notebook.ipynb). If you notice anything unexpected, please open an [issue](github.com/benedekrozemberczki/tigerlily/issues).


--------------------------------------------------------------------------------

**Citing**


If you find *Tigerlily* useful in your research, please consider adding the following citation:

```bibtex
@misc{tigerlily2022,
  author = {Benedek Rozemberczki},
  title = {TigerLily: Finding drug interactions insilico with the Graph},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/benedekrozemberczki/tigerlily}},
}
```

--------------------------------------------------------------------------------

**Installation**

To install tigerlily, simply run:

```sh
pip install tigerlily
```

**Running tests**

Running tests requires that you run:

```
$ tox -e py
```
--------------------------------------------------------------------------------

**License**

- [Apache 2.0 License](https://github.com/benedekrozemberczki/tigerlily/blob/main/LICENSE)
