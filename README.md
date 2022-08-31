# Bundle entropy as an optimized measure of consumers’ systematic product choice combinations


#### **Bundle Entropy is introduced in:**
*Mansilla, R., Smith, G., Smith A. and Goulding, J. "Bundle entropy as an optimized measure of
consumers’ systematic product choice combinations". In 2022 IEEE International Conference on Big Data (IEEE Big Data 2022), Osaka, Japan.*


## Code to replicate the results from our IEEE Big Data paper


### A. Postgres Aggregate Functions


#### 1. The proposed *Bundle Entropy* 

Bundle Entropy (formula 9 in the paper) is implemented as a custom postgres aggregrate function. The implementation to copy and paste into psql can be found in: [https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe](https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe?usp=sharing)


#### 2. *Basket Revealed Entropy (BRE)* 

BRE method (formula 3 in the paper) is from:
* *Guidotti, R., Coscia, M., Pedreschi, D. & Pennacchioli, D. (2015), ‘Behavioral entropy and profitability in retail’, Proceedings of the 2015 IEEE International Conference on Data Science and Advanced Analytics, DSAA 2015 pp. 1–10* 

BRE is implemented as a custom postgres aggregrate function. The implementation to copy and paste into psql can be found in: [https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe](https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe?usp=sharing)


#### 3. *Standard Entropy*

The Standard Entropy method (formula 1 in the paper) is from:

* *Shannon, C. (1948), ‘A Mathematical Theory of Communication’, The Bell System Technical Jour-
nal 28(3), 379–423*. 

Standard Entropy is implemented as a custom postgres aggregrate function. The implementation to copy and paste into psql can be found in: [https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe](https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe?usp=sharing)


#### 4. *Basket Level Entropy (BLE)*

BLE (formula 1 in the paper) is implemented as a custom postgres aggregrate function. The implementation to copy and paste into psql can be found in ( it requires the previous code to be run to define **basket_tuple** and **_state_bundle_entropy**): [https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe](https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe?usp=sharing)

### B. Replication of the methodology on synthetic data

Synthetic data (toy examples) represents the grocery purchase history of 11 customers. This table exemplifies that our proposed measure meets all the desired properties described in our paper. The implementation of the synthetic table to copy and paste into psql can be found in: [https://colab.research.google.com/drive/1ikmgT0AN7INBczu-s4yVqsfIfvFt491z](https://colab.research.google.com/drive/1ikmgT0AN7INBczu-s4yVqsfIfvFt491z?usp=sharing)


### C. Replication of the methodology of the desired properties of *Bundle entropy*


### D. Replication of the methodology of the case study (Dunnhumby data set)

Our paper tested *Bundle entropy* on Dunnhumby open source data set called "The complete journey", which contains grocery purchases at a household level over two years from 2,500 frequent shoppers. The Dunnhumby dataset contain records of `what', `how much', `where', and `when' each transaction with transactions linked to a customer via their loyalty card. *Bundle entropy* is also tested on a second large transactional dataset of loyalty card holders from a large UK grocery retailer. However, the dataset is unavailable for public release.

Dunnhumby data set (the complete journey) can be downloaded from: [https://www.dunnhumby.com/source-files/](https://www.dunnhumby.com/source-files/)

The implementation in SQL and Python to replicate these results can be found in: [https://colab.research.google.com/drive/14BUnWsX1yq1xTK3MFjIB3qVI3xWpseGD](https://colab.research.google.com/drive/14BUnWsX1yq1xTK3MFjIB3qVI3xWpseGD?usp=sharing)
