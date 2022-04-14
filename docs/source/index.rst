:github_url: https://github.com/benedekrozemberczki/tigerlily

TigerLily Documentation
=======================

TigerLily is a TigerGraph based system designed to solve the drug interaction prediction task. In this machine learning task we want to predict whether two drugs have an adverse interaction. Our framework allows to solve this highly relevant real world problem using graph mining techniques in these steps:

- (a) Using PyTigergraph we create a heterogeneous biological graph of drugs and proteins.
- (b) We calculate the personalized PageRank scores of drug nodes in the TigerGraph Cloud.
- (c) We embed the nodes using sparse non-negative matrix factorization of the personalized PageRank matrix.
- (d) Using the node embeddings we train a gradient boosting based drug interaction predictor.

If you would use TigerLily please cite our work:

.. code-block:: latex


     >@misc{tigerlily2022,
       author = {Benedek Rozemberczki},
       title = {TigerLily: Finding drug interactions insilico with the Graph},
       year = {2022},
       publisher = {GitHub},
       journal = {GitHub repository},
       howpublished = {\url{https://github.com/benedekrozemberczki/tigerlily}},
     }

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Package Reference

   modules/root


.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Notes


   notes/installation
   notes/tutorial
   notes/resources


