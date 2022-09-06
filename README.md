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

Quasi-synthetic data were used to evaluate the desired properties that we consider essential for a measure that aims to measure the predictability of systematic basket composition at an individual level. The implementation in SQL and Python to replicate Table 1, Figure 2 and 3 of our paper can be found in: [https://colab.research.google.com/drive/1fUId0xy6HVabp2A8YAQvqLwtOsmNSPH](https://colab.research.google.com/drive/1fUId0xy6HVabp2A8YAQvqLwtOsmNSPH_?usp=sharing)

* #### Replication of TABLE 1

Table 1 illustrates the percentage of households that accords to property 0 and 1 for all measures and the percentage of households that each measures considered as fully predictable.

<p align="center"><b> Table 1: Measures vs. Properties 0 & 1 and the percentage
of households considered as fully predictable</b></p>
<p align="center"> <img width="450" src="https://user-images.githubusercontent.com/43341262/188661423-c914ae1d-55a1-4d68-8738-7d1f561552ac.png" alt="Table 1" /> </p>

* #### Replication of FIGURE 2

Figure 2 depicts the scores received for each examined metric (BE, IE, BLE, amd BRE) when systematic bundles were added to the purchases of three random households. 

<p align="center"><b> Figure 2: Examples of three household’s scores for the evaluated measures when adding systematic bundles to their purchases</b></p>
<p align="center"> <img width="400" src="https://user-images.githubusercontent.com/43341262/188662488-60a4ce09-dc11-4c09-8435-051673d78a9b.png" alt="Figure 2" /> </p>

* #### Replication of FIGURE 3

Figure 3 depicts the empirical performance of the measures for property 2 by randomly picking all of the baskets from a random sample of 1,000 households and gradually building systematic bundles of varying sizes (from one to 10 items) to each household's baskets. 

<p align="center"><b> Figure 3: Comparing measures by increasing the size of systematic bundles added to all baskets.</b></p>
<p align="center"> <img width="400" src="https://user-images.githubusercontent.com/43341262/188662838-87df191b-663c-400e-8153-93ac48fd7f40.png" alt="Figure 3" /> </p>


### D. Replication of the methodology of the case study (Dunnhumby data set)

Our paper tested *Bundle entropy* on Dunnhumby open source data set called "The complete journey", which contains grocery purchases at a household level over two years from 2,500 frequent shoppers. *Bundle entropy* is also tested on a second large transactional dataset of loyalty card holders from a large UK grocery retailer. However, the dataset is unavailable for public release.

Dunnhumby data set (the complete journey) can be downloaded from: [https://www.dunnhumby.com/source-files/](https://www.dunnhumby.com/source-files/)

The implementation in SQL and Python to replicate all the results of the case study (Figure 4a and Table 2) can be found in: [https://colab.research.google.com/drive/1woNGSpYD6jR3JCaDxqlX8dknUHgQfwrF](https://colab.research.google.com/drive/1woNGSpYD6jR3JCaDxqlX8dknUHgQfwrF?usp=sharing)

* #### Replication of FIGURE 4a

Figure 4 displays the Mean Rank Difference between the likelihood of a pair of households (consumers) being in the same rank order according to both measurements and the likelihood of the pairs being in different rank orders.

<p align="center"><b> Figure 4a: Kendall Tau Rank Agreement (Mean Rank Difference) of relative household/customer predictability for pairs of measures </b></p>
<p align="center"> <img width="350" src="https://user-images.githubusercontent.com/43341262/188725072-8b0dc32f-b37d-42a7-8865-754d7bad07ff.png" alt="Figure 4a" /> </p>

* #### Replication of TABLE 2

Table 2 shows the Pearson Correlation for all measures under exploration, as well as the average basket expenditure and number of visits. Furthermore, the association of the measures with another performance indicator important to the fast-moving consumer goods market - an individual's average monthly spend (an indication of potential lifetime value)
 
<p align="center"><b> Table 2: Pearson Correlation between the measures and spending and visiting factors.</b></p>
<p align="center"> <img width="500" src="https://user-images.githubusercontent.com/43341262/188726154-fb9d69f1-c56f-4524-9630-19ef63c98be2.png" alt="Table 3" /> </p>


## E. Python and libraries versions used

<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="28"/> </a> *3.6.9* 

<a href="https://pandas.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="28"/> </a> *1.1.5* 

<a href="https://numpy.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/numpy/numpy-original.svg" alt="numpy" width="40" height="28"/> </a> *1.19.5* 

<a href="https://matplotlib.org/" target="_blank" rel="noreferrer"> <img src="https://user-images.githubusercontent.com/43341262/188117265-1c162daf-f86c-4bcf-89e6-04faa8482558.svg" alt="matplotlib" width="80" height="17"/> </a> *3.1.1*

<a href="https://seaborn.pydata.org/" target="_blank" rel="noreferrer"> <img src="https://user-images.githubusercontent.com/43341262/188117310-a42f837d-fd35-4927-8d2b-a6dc39f402b9.svg" alt="seaborn" width="80" height="17"/> </a> *0.11.1* 



