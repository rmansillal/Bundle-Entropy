<h1 align="center">Bundle entropy as an optimized measure of consumers' systematic product choice combinations in mass transactional data</h1>

<h3 align="center">Bundle Entropy is introduced in:</h3>

<p align="center">Mansilla, R., Smith, G., Smith A. and Goulding, J. "Bundle entropy as an optimized measure of consumers' systematic product choice combinations in mass transactional data". In 2022 IEEE International Conference on Big Data (IEEE Big Data 2022), Osaka, Japan.</p>


## Code to replicate the results from our IEEE Big Data paper


### A. Postgres Aggregate Functions


* #### *Bundle Entropy (BE)* 

  The proposed Bundle Entropy (formula 9 in the paper) is implemented as a custom postgres aggregrate function. The implementation to copy and paste into psql can be found in: [https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe](https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe?usp=sharing)


* #### *Basket Revealed Entropy (BRE)* 

  BRE method (formula 3 in the paper) is from:
  * *Guidotti, R., Coscia, M., Pedreschi, D. & Pennacchioli, D. (2015), ‘Behavioral entropy and profitability in retail’, Proceedings of the 2015 IEEE International Conference on Data Science and Advanced Analytics, DSAA 2015 pp. 1–10* 

  BRE is implemented as a custom postgres aggregrate function. The implementation to copy and paste into psql can be found in: [https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe](https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe?usp=sharing)


* #### *Item Level Entropy (IE)*

  The Standard Entropy method (formula 1 in the paper) is from:

  * *Shannon, C. (1948), ‘A Mathematical Theory of Communication’, The Bell System Technical Jour-
nal 28(3), 379–423*. 

  Standard Entropy is implemented as a custom postgres aggregrate function. The implementation to copy and paste into psql can be found in: [https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe](https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe?usp=sharing)


* #### *Basket Level Entropy (BLE)*

  BLE (formula 2 in the paper) is implemented as a custom postgres aggregrate function. The implementation to copy and paste into psql can be found in ( it requires the previous code to be run to define **basket_tuple** and **_state_bundle_entropy**): [https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe](https://colab.research.google.com/drive/1zBE4DpumMtQKRk3yYY2QOiGS7WUnVSEe?usp=sharing)


### B. Replication of the methodology on synthetic data

* #### Replication of FIGURE 1

Figure 1 illustrate some synthetic examples (the purchasing patterns of five customers ) motivating the need for a new measure. The implementation of the synthetic examples to copy and paste into psql can be found in: [https://colab.research.google.com/drive/1MJG7mA8_KXuzHZZ24FGZNbejaSvAYQzG](https://colab.research.google.com/drive/1MJG7mA8_KXuzHZZ24FGZNbejaSvAYQzG?usp=sharing)

<p align="center"><b> Figure 1: Examples motivating the need for a new measure</b></p>
<p align="center"> <img width="550" src="https://user-images.githubusercontent.com/43341262/188644292-634da6b6-bafb-4360-919a-e560acc78aec.png" alt="Figure 1" /> </p>


### C. Replication of the methodology of the desired properties of *Bundle entropy*

Quasi-synthetic data were used to evaluate the desired properties that we consider essential for a measure that aims to measure the predictability of systematic basket composition at an individual level. The implementation in SQL and Python to replicate Table 2, Figure 1 and 2 of our paper can be found in: [https://colab.research.google.com/drive/14BUnWsX1yq1xTK3MFjIB3qVI3xWpseGD](https://colab.research.google.com/drive/14BUnWsX1yq1xTK3MFjIB3qVI3xWpseGD?usp=sharing)

<p align="center"><b> Table 2: tatistic for property 1</b></p>
<p align="center"> <img width="300" src="https://user-images.githubusercontent.com/43341262/187892000-4ce1391f-3def-4ed1-8fc4-b5dc9c075088.png" alt="Table 2" /> </p>

<p align="center"><b> Figure 1: P1: adding systematic vs unsystematic bundles</b></p>
<p align="center"> <img width="450" src="https://user-images.githubusercontent.com/43341262/187892133-f6afdfdf-f9c7-4145-828e-b433aaf3b566.png" alt="Figure 1" /> </p>

<p align="center"><b> Figure 2: omparing measures by increasing the size of systematic bundles added to all baskets.</b></p>
<p align="center"> <img width="350" src="https://user-images.githubusercontent.com/43341262/187892202-153687a1-629d-482d-a99f-41bfdfa45719.png" alt="Figure 2" /> </p>


### D. Replication of the methodology of the case study (Dunnhumby data set)

Our paper tested *Bundle entropy* on Dunnhumby open source data set called "The complete journey", which contains grocery purchases at a household level over two years from 2,500 frequent shoppers. *Bundle entropy* is also tested on a second large transactional dataset of loyalty card holders from a large UK grocery retailer. However, the dataset is unavailable for public release.

Dunnhumby data set (the complete journey) can be downloaded from: [https://www.dunnhumby.com/source-files/](https://www.dunnhumby.com/source-files/)

The implementation in SQL and Python to replicate all the results of the case study (Figure 3a, 4, and Table 3) can be found in: [https://colab.research.google.com/drive/1woNGSpYD6jR3JCaDxqlX8dknUHgQfwrF](https://colab.research.google.com/drive/1woNGSpYD6jR3JCaDxqlX8dknUHgQfwrF?usp=sharing)

<p align="center"><b> Figure 3a: Kendall Tau Rank Agreement (Mean Rank Difference) </b></p>
<p align="center"> <img width="350" src="https://user-images.githubusercontent.com/43341262/187929401-3e82e523-a454-4d7b-88eb-2cfac5d3c364.png" alt="Figure 3a" /> </p>

<p align="center"><b> Figure 4: Percentage of shared households (systematic, standard, and unsystematic) between measures</b></p>
<p align="center"> <img width="850" src="https://user-images.githubusercontent.com/43341262/187928920-f85b192b-cb84-4db9-9e2f-3810e5eac85a.png" alt="Figure 4" /> </p>

<p align="center"><b> Table 3: Spending and visiting patterns per measure</b></p>
<p align="center"> <img width="800" src="https://user-images.githubusercontent.com/43341262/187927592-5211aa44-7a34-48d9-9451-71a7f5335948.png" alt="Table 3" /> </p>


## E. Python and libraries versions used

<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="28"/> </a> *3.6.9* 

<a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="28"/> </a> *1.1.5* 

<a href="https://numpy.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/numpy/numpy-original.svg" alt="numpy" width="40" height="28"/> </a> *1.19.5* 

<a href="https://matplotlib.org/" target="_blank" rel="noreferrer"> <img src="https://user-images.githubusercontent.com/43341262/188117265-1c162daf-f86c-4bcf-89e6-04faa8482558.svg" alt="matplotlib" width="80" height="17"/> </a> *3.1.1*

<a href="https://seaborn.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://user-images.githubusercontent.com/43341262/188117310-a42f837d-fd35-4927-8d2b-a6dc39f402b9.svg" alt="seaborn" width="80" height="17"/> </a> *0.11.1* 



