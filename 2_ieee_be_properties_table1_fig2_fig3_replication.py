# -*- coding: utf-8 -*-
"""2_IEEE_BE_Properties_Table1_Fig2_Fig3_Replication.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fUId0xy6HVabp2A8YAQvqLwtOsmNSPH_

# *Mansilla, R., Smith, G., Smith A. and Goulding, J. "Bundle entropy as an optimized measure of consumers' systematic product choice combinations in mass transactional data". In 2022 IEEE International Conference on Big Data (IEEE Big Data 2022), Osaka, Japan.*
-----

# **Code and replication of the methodology of the desired properties of Bundle entropy on DUNNHUMBY data set**

* Assumes a running postgres database with hostname: \<hostname\>, database: \<database\>
* Assumes the open real-world dataset [The complete journey data from dunnhumby](https://www.dunnhumby.com/source-files/) has been loaded into the database in a table called `transaction_data` in postgres.

## 1) Connect to database & Import Python libraries
"""

# Import libraries
import numpy as np
import pandas as pd
from getpass import getpass
import matplotlib.pyplot as plt
import matplotlib
from pylab import rcParams
import seaborn as sns
import matplotlib.lines as lines
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Commented out IPython magic to ensure Python compatibility.
# Connect to database
# %config Completer.use_jedi = False
# %reload_ext sql

# %sql {f"postgresql://<username>:{getpass()}@<hostname>/<database>"}

"""# SQL

### 2) SQL code to create tables using the 2,500 customers
"""

# Commented out IPython magic to ensure Python compatibility.
# %%sql
# --======================================================================  
# --============= DUNMHUMBY CODE TO COMPUTE ENTROPIES ====================
# --======================================================================
# -- Dunnhumby trasnaction_data has data 711 days (around to years).
# 
# --==================================
# --============= First ==============
# --==================================
# CREATE TABLE rm.transaction_data_filtered AS (
#   SELECT household_key, basket_id, day, product_id, quantity, sales_value 
# 	FROM public.transaction_data)
# 
# --==================================
# --============= Second ============= # customers with at least 1 purchase a month
# --==================================
# CREATE TABLE rm.trans_data_cust_21_purch AS (
#   SELECT *
#   FROM rm.transaction_data_filtered
#   WHERE household_key IS NOT null
#   AND household_key IN (SELECT b.household_key 
#                         FROM (SELECT a.household_key, count(distinct a.basket_id) as total_baskets
#                               FROM rm.transaction_data_filtered a
#                               GROUP BY 1) b
#                               WHERE b.total_baskets >= 21)
#   ORDER BY household_key);
# 
# --==================================
# --============= Third ==============
# --==================================
# CREATE TABLE rm.trans_data_8_customers AS (
#   SELECT household_key, basket_id,product_id
#   FROM rm.trans_data_cust_21_purch
#   WHERE household_key IN(1,2,3,4,5,6,7,8))

"""# PYTHON

### 3) FIGURE 2 of our paper
Figure 2 depicts the scores received for each examined metric (BE, IE, BLE, amd BRE) when systematic bundles were added to the purchases of three random households.

#### Original table (3 households)
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# sql_or_bundle_5 = """SELECT household_key, 
#                           round(bev3_norm(basket_id::TEXT, product_id::TEXT),2) as BE,
#                           round(norm_entropy(product_id::TEXT),2) as IE,
#                           round(joint_entropy(basket_id::TEXT, product_id::TEXT),2) as BLE,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.10 ),2) as BRE10,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.24 ),2) as BRE24,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.70 ),2) as BRE70
#                       FROM rm.trans_data_8_customers
#                       WHERE household_key in (1,2,4)
#                       GROUP BY 1
#                       ORDER BY 1
#                     """
# df_orig_bundle_5 = %sql {sql_or_bundle_5}
# df_orig_bundle_5 = df_orig_bundle_5.DataFrame()
# 
# #-- Convert multiple columns
# df_orig_bundle_5 = df_orig_bundle_5.astype(float)

"""#### Adding random bundle to the original table"""

#-- Main table to which random bundles will be added
sql_c1_to_c8 = """SELECT household_key, basket_id,product_id
            FROM rm.trans_data_8_customers
            ORDER BY 2
                """
df_c1_to_c8 = %sql {sql_c1_to_c8}
df_c1_to_c8 = df_c1_to_c8.DataFrame()

#### ADD RANDOM BUNDLES to import to postgres ####

# Empty dataframe
random_concat_1_to_8 = pd.DataFrame(columns=['household_key','basket_id','product_id'])

# dataframe with random items
rd_items = pd.DataFrame(data={'household_key':[1]*100000,'basket_id':[2]*100000,'product_id':list(range(-100001, -1))})

#-- definition to add rows of random items per basket_id
def add_bundle(x):
    #-- get "rd_bundle_items" random products from "rd_items"
    rd_bundle_items = 40
    global rd_items 
    random_bundle = rd_items.iloc[:rd_bundle_items]
    rd_items = rd_items.iloc[rd_bundle_items:]

    #-- for loop to replace sample household_key & basket_id with the household_key & basket_id on the current customer 
    for row in range(rd_bundle_items):
        random_bundle.iloc[row,0] = x.iloc[0,0]#row 0, column 0
        random_bundle.iloc[row,1] = x.iloc[0,1]#row 0, column 1
        
    #-- add all items (rows) to the original table
    return x.append(random_bundle)

for cust in range(1,7):    
    #-- for each customer apply to all of the original table the 'add_bundle' function per basket_id  
    df_random_bundle = df_c1_to_c8[df_c1_to_c8['household_key']==cust].groupby('basket_id').apply(add_bundle).reset_index(drop=True)

    #-- Update random_concat_1_to_8 with df_random_bundle
    random_concat_1_to_8 = pd.concat([df_random_bundle,  random_concat_1_to_8])

# Commented out IPython magic to ensure Python compatibility.
#-- Upload dataframe into database
# %sql --persist random_concat_1_to_8

# Commented out IPython magic to ensure Python compatibility.
# %%time
# #-- Compute all measures for the first 5 customers for plotting purposes
# sql_rd_bundle = """SELECT household_key, 
#                           round(bev3_norm(basket_id::TEXT, product_id::TEXT),2) as BE,
#                           round(norm_entropy(product_id::TEXT),2) as IE,
#                           round(joint_entropy(basket_id::TEXT, product_id::TEXT),2) as BLE,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.10 ),2) as BRE10,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.24 ),2) as BRE24,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.70 ),2) as BRE70
#                       FROM public.random_concat_1_to_8
#                       WHERE household_key in (1,2,4)
#                       GROUP BY 1
#                       ORDER BY 1
#                     """
# df_rd_bundle_5 = %sql {sql_rd_bundle}
# df_rd_bundle_5 = df_rd_bundle_5.DataFrame()
# 
# #-- Convert multiple columns
# df_rd_bundle_5 = df_rd_bundle_5.astype(float)

"""#### Adding systematic bundle to the original table"""

#### ADD SYSTEMATIC BUNDLES to import to PGADMIN####

syst_concat_1_to_8 = pd.DataFrame(columns=['household_key','basket_id','product_id'])

#-- definition to add rows of random items per basket_id
def add_bundle(x):
    #-- for loop to replace sample household_key & basket_id with the household_key & basket_id on the current customer 
    for row in range(syst_bundle_items):
        syst_bundle.iloc[row,0] = x.iloc[0,0]#row 0, column 0
        syst_bundle.iloc[row,1] = x.iloc[0,1]#row 0, column 1
        
    #-- add all items (rows) to the original table
    return x.append(syst_bundle)

#-- get a random(s) products from the original table
syst_bundle_items = 10
syst_bundle = df_c1_to_c8.sample(n=syst_bundle_items)
syst_bundle.product_id = syst_bundle.product_id*-1

for cust in range(1,7):    
    #-- for each customer apply to all of the original table the 'add_bundle' function per basket_id  
    df_syst_bundle = df_c1_to_c8[df_c1_to_c8['household_key']==cust].groupby('basket_id').apply(add_bundle).reset_index(drop=True)

    #-- Append df_concat to c1_with_rd_items
    syst_concat_1_to_8 = pd.concat([df_syst_bundle,  syst_concat_1_to_8])

#-- save systematiccs csv 
syst_concat_1_to_8.to_csv(f'syst_bundles_c1_to_c10.csv', index=False) #con esto cree una tabla en postgres manualmente y subi esta data manualmente tb

# Commented out IPython magic to ensure Python compatibility.
#-- Upload dataframe into database
# %sql --persist syst_concat_1_to_8

# Commented out IPython magic to ensure Python compatibility.
# %%time
# #-- Compute all measures for the first 5 customers for plotting purposes
# sql_syst_bundle = """SELECT household_key, 
#                           round(bev3_norm(basket_id::TEXT, product_id::TEXT),2) as BE,
#                           round(norm_entropy(product_id::TEXT),2) as IE,
#                           round(joint_entropy(basket_id::TEXT, product_id::TEXT),2) as BLE,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.10 ),2) as BRE10,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.24 ),2) as BRE24,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.70 ),2) as BRE70
#                       FROM public.syst_concat_1_to_8
#                       WHERE household_key in (1,2,4)
#                       GROUP BY 1
#                       ORDER BY 1
#                     """
# df_syst_bundle_5 = %sql {sql_syst_bundle}
# df_syst_bundle_5 = df_syst_bundle_5.DataFrame()
# 
# #-- Convert multiple columns
# df_syst_bundle_5 = df_syst_bundle_5.astype(float)

df_syst_bundle_5.describe()

"""##### Normalized Version"""

def lollipop_plot_norm(c,r,measure,df):
  # Reorder it following the values of the first value:
  ordered_df = df.sort_values(by='household')
  my_range=range(1,len(df.index)+1)

  # Build the lollipop plot
  axes[c][r].vlines(x=my_range, ymin=ordered_df['original'], ymax=ordered_df['systematic'], color='grey', alpha=0.5,ls=':')
  axes[c][r].scatter(my_range, ordered_df['systematic'], color='tomato', alpha=0.8 , label='syst',s=60)
  axes[c][r].scatter(my_range, ordered_df['original'],  color='black', alpha=0.8, label='orig',s=40,marker='x')
  
  # Add title and axis names
  axes[c][r].tick_params(axis='both', which='major', labelsize=12)
  axes[c][r].set_ylim([-0.1, 1.22])
  axes[c][r].set_xlim([0.5,3.5])
  axes[c][r].text(2,1.12,measure, horizontalalignment='center',fontsize=12,fontweight="bold")

#-- NORMALIZED
nr_rows = 2
nr_cols = 3

fig, axes = plt.subplots(nr_rows, nr_cols, figsize=(6,5),sharey='row',sharex='col')

lollipop_plot_norm(0,0,'Bundle Ent.',be) 
lollipop_plot_norm(0,1,'Item Entropy',ie)
lollipop_plot_norm(0,2,'BLE',ble)
lollipop_plot_norm(1,0,'BRE10',bre10)
lollipop_plot_norm(1,1,'BRE24',bre24)
lollipop_plot_norm(1,2,'BRE70',bre70)

plt.tight_layout()  
axes[0,2].legend(fontsize=12,ncol=3,bbox_to_anchor=(1.0,-1.2),frameon=False,labelspacing=0.01,handlelength=0.03, handletextpad=0.4,columnspacing=0.8)
plt.text(-2.8,-0.4,'Household ID', horizontalalignment='center',fontsize=13)
plt.text(-7.3,1,'Measure Value', horizontalalignment='center',fontsize=13, rotation='vertical')
#plt.text(-2,2.8,'(Normalized using bev3_norm)', horizontalalignment='center',fontsize=13)
plt.show()

"""### 4) TABLE 1 of our paper

Table 1 illustrates the percentage of households that accords to property 0 and 1 for all measures and the percentage of households that each measures considered as fully predictable.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# #-- Main table
# sql_all_cust = """SELECT household_key, basket_id,product_id
#             FROM rm.trans_data_cust_21_purch
#             ORDER BY basket_id 
#                 """
# df_all_cust = %sql {sql_all_cust}
# df_all_cust = df_all_cust.DataFrame()

"""#### Original table (all households)"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# sql_or_bundle = """SELECT household_key, 
#                           round(bev3_norm2(basket_id::TEXT, product_id::TEXT),2) as BE_norn2
#                       FROM rm.trans_data_cust_21_purch
#                       GROUP BY 1
#                       ORDER BY 1
#                     """
# df_or_bundle = %sql {sql_or_bundle}
# df_or_bundle = df_or_bundle.DataFrame()
# 
# #-- Convert multiple columns
# households_bev3_norm2 = df_or_bundle.astype(float)
#

# Commented out IPython magic to ensure Python compatibility.
# %sql --persist households_bev3_norm2

# Commented out IPython magic to ensure Python compatibility.
# %%time
# sql_or_bundle = """SELECT household_key, 
#                           round(bev3_norm(basket_id::TEXT, product_id::TEXT),2) as BE,
#                           round(norm_entropy(product_id::TEXT),2) as IE,
#                           round(joint_entropy(basket_id::TEXT, product_id::TEXT),2) as BLE,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.10 ),2) as BRE10,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.24 ),2) as BRE24,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.70 ),2) as BRE70
#                       FROM rm.trans_data_cust_21_purch
#                       GROUP BY 1
#                       ORDER BY 1
#                     """
# df_or_bundle = %sql {sql_or_bundle}
# df_or_bundle = df_or_bundle.DataFrame()
# 
# #-- Convert multiple columns
# df_or_bundle = df_or_bundle.astype(float)

"""#### With random bundles"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# #### ADD RANDOM BUNDLES to each consumer's basket and import to PGADMIN####
# 
# # Empty dataframe
# random_concat_all_cust = pd.DataFrame(columns=['household_key','basket_id','product_id'])
# 
# # dataframe with random items
# rd_items = pd.DataFrame(data={'household_key':[1]*10000000,'basket_id':[2]*10000000,'product_id':list(range(-10000001, -1))})
# 
# #-- definition to add rows of random items per basket_id
# def add_bundle(x):
#     #-- get "rd_bundle_items" random products from "rd_items"
#     rd_bundle_items = 10
#     global rd_items 
#     random_bundle = rd_items.iloc[:rd_bundle_items]
#     rd_items = rd_items.iloc[rd_bundle_items:]
# 
#     #-- for loop to replace sample household_key & basket_id with the household_key & basket_id on the current customer 
#     for row in range(rd_bundle_items):
#         random_bundle.iloc[row,0] = x.iloc[0,0]#row 0, column 0
#         random_bundle.iloc[row,1] = x.iloc[0,1]#row 0, column 1
#         
#     #-- add all items (rows) to the original table
#     return x.append(random_bundle)
# 
# for cust in list(df_all_cust.household_key.unique()):
#     #-- for each customer apply to all of the original table the 'add_bundle' function per basket_id  
#     df_random_bundle = df_all_cust[df_all_cust['household_key']==cust].groupby('basket_id').apply(add_bundle).reset_index(drop=True)
# 
#     #-- Append df_concat to c1_with_rd_items
#     random_concat_all_cust = pd.concat([df_random_bundle,  random_concat_all_cust])

# Commented out IPython magic to ensure Python compatibility.
# %%time
# # UPload dataframe into database
# %sql --persist random_concat_all_cust

# Commented out IPython magic to ensure Python compatibility.
# %%time
# sql_rd_bundle = """SELECT household_key, 
#                           round(bev3_norm(basket_id::TEXT, product_id::TEXT),2) as BE,
#                           round(norm_entropy(product_id::TEXT),2) as IE,
#                           round(joint_entropy(basket_id::TEXT, product_id::TEXT),2) as BLE,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.10 ),2) as BRE10,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.24 ),2) as BRE24,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.70 ),2) as BRE70
#                       FROM public.random_concat_all_cust
#                       GROUP BY 1
#                       ORDER BY 1
#                     """
# df_rd_bundle = %sql {sql_rd_bundle}
# df_rd_bundle = df_rd_bundle.DataFrame()
# 
# #-- Convert multiple columns
# df_rd_bundle = df_rd_bundle.astype(float) #HERE

"""#### With systematic bundles"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# #### ADD SYSTEMATIC BUNDLES to import to PGADMIN####
# 
# syst_concat_all_cust = pd.DataFrame(columns=['household_key','basket_id','product_id'])
# 
# #-- definition to add rows of random items per basket_id
# def add_bundle(x):
#     #-- for loop to replace sample household_key & basket_id with the household_key & basket_id on the current customer 
#     for row in range(syst_bundle_items):
#         syst_bundle.iloc[row,0] = x.iloc[0,0]#row 0, column 0
#         syst_bundle.iloc[row,1] = x.iloc[0,1]#row 0, column 1
#         
#     #-- add all items (rows) to the original table
#     return x.append(syst_bundle)
# 
# #-- get a random(s) products from the original table
# syst_bundle_items = 10
# syst_bundle = df_all_cust[df_all_cust['product_id']>=1].sample(n=syst_bundle_items)
# syst_bundle.product_id = syst_bundle.product_id*-1
# 
# for cust in list(df_all_cust.household_key.unique()):   
#     #-- for each customer apply to all of the original table the 'add_bundle' function per basket_id  
#     df_syst_bundle = df_all_cust[df_all_cust['household_key']==cust].groupby('basket_id').apply(add_bundle).reset_index(drop=True)
# 
#     #-- Append df_concat to c1_with_rd_items
#     syst_concat_all_cust = pd.concat([df_syst_bundle,  syst_concat_all_cust])

# Commented out IPython magic to ensure Python compatibility.
# %sql --persist syst_concat_all_cust

# Commented out IPython magic to ensure Python compatibility.
# %%time
# sql_syst_bundle = """SELECT household_key, 
#                           round(bev3_norm(basket_id::TEXT, product_id::TEXT),2) as BE,
#                           round(norm_entropy(product_id::TEXT),2) as IE,
#                           round(joint_entropy(basket_id::TEXT, product_id::TEXT),2) as BLE,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.10 ),2) as BRE10,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.24 ),2) as BRE24,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.70 ),2) as BRE70
#                       FROM public.syst_concat_all_cust
#                       GROUP BY 1
#                       ORDER BY 1
#                       LIMIT 1100
#                     """
# df_syst_bundle_1 = %sql {sql_syst_bundle}
# df_syst_bundle_1 = df_syst_bundle_1.DataFrame()
# 
# #-- Convert multiple columns
# df_syst_bundle_1 = df_syst_bundle_1.astype(float) #HERE
#

# Commented out IPython magic to ensure Python compatibility.
# %%time
# sql_syst_bundle_2 = """SELECT household_key, 
#                           round(bev3_norm(basket_id::TEXT, product_id::TEXT),2) as BE,
#                           round(norm_entropy(product_id::TEXT),2) as IE,
#                           round(joint_entropy(basket_id::TEXT, product_id::TEXT),2) as BLE,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.10 ),2) as BRE10,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.24 ),2) as BRE24,
#                           round(bre(basket_id::TEXT, product_id::TEXT,0.70 ),2) as BRE70
#                       FROM public.syst_concat_all_cust
#                       GROUP BY 1
#                       ORDER BY 1 desc
#                       LIMIT 1113 
#                     """
# df_syst_bundle_2 = %sql {sql_syst_bundle_2}
# df_syst_bundle_2 = df_syst_bundle_2.DataFrame()
# 
# #-- Convert multiple columns
# df_syst_bundle_2 = df_syst_bundle_2.astype(float)

# Concat both df with systematic bundles added 
df_syst_bundle = pd.concat([df_syst_bundle_1,  df_syst_bundle_2])

"""#### Join tables"""

df_or_bundle['bundle'] = 'original'
df_rd_bundle['bundle'] = 'random'
df_syst_bundle['bundle'] = 'systematic'

rd_syst_concat= pd.concat([df_rd_bundle[['household_key','bundle','be','ie','ble','bre10','bre24','bre70']],  df_syst_bundle[['household_key','bundle','be','ie','ble','bre10','bre24','bre70']]])
rd_syst_orig_concat= pd.concat([df_or_bundle[['household_key','bundle','be','ie','ble','bre10','bre24','bre70']],  rd_syst_concat])
rd_syst_orig_concat_2213_norm = rd_syst_orig_concat.copy()

rd_syst_orig_concat_2213_norm2 = rd_syst_orig_concat_2213_norm.copy()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# %sql --persist rd_syst_orig_concat_2213_norm2

"""#### Replicate Table 1 """

# Commented out IPython magic to ensure Python compatibility.
# %%time
# # Compute the percentage of cases where the original score is in between the random and systematic score.The "between" function is inclusive.
# sql_p1 = """
#         SELECT 
#           ROUND(cast(SUM(be) as decimal(10,2)) / cast(COUNT(*) as decimal(10,2)),3) AS be,
#           ROUND(cast(SUM(ie) as decimal(10,2)) / cast(COUNT(*) as decimal(10,2)),3) AS ie,
#           ROUND(cast(SUM(ble) as decimal(10,2)) / cast(COUNT(*) as decimal(10,2)),3) AS ble,
#           ROUND(cast(SUM(bre10) as decimal(10,2)) / cast(COUNT(*) as decimal(10,2)),3) AS bre10,
#           ROUND(cast(SUM(bre24) as decimal(10,2)) / cast(COUNT(*) as decimal(10,2)),3) AS bre24,
#           ROUND(cast(SUM(bre70) as decimal(10,2)) / cast(COUNT(*) as decimal(10,2)),3) AS bre70
#         FROM (
#           SELECT 
#           (SUM(CASE WHEN bundle = 'original' THEN be ELSE 0 END) > SUM(CASE WHEN bundle = 'systematic' THEN be ELSE 0 END))::INT as be,
#           (SUM(CASE WHEN bundle = 'original' THEN e ELSE 0 END) > SUM(CASE WHEN bundle = 'systematic' THEN e ELSE 0 END))::INT as ie,
#           (SUM(CASE WHEN bundle = 'original' THEN je ELSE 0 END) > SUM(CASE WHEN bundle = 'systematic' THEN je ELSE 0 END))::INT as ble,
#           (SUM(CASE WHEN bundle = 'original' THEN bre10 ELSE 0 END) > SUM(CASE WHEN bundle = 'systematic' THEN bre10 ELSE 0 END) )::INT as bre10,
#           (SUM(CASE WHEN bundle = 'original' THEN bre24 ELSE 0 END) > SUM(CASE WHEN bundle = 'systematic' THEN bre24 ELSE 0 END) )::INT as bre24,
#           (SUM(CASE WHEN bundle = 'original' THEN bre70 ELSE 0 END) > SUM(CASE WHEN bundle = 'systematic' THEN bre70 ELSE 0 END) )::INT as bre70
#           FROM rd_syst_orig_concat_2213_norm2
#           GROUP BY household_key
#             ) x ;
#           """
# df_p1 = %sql {sql_p1}
# df_p1 = df_p1.DataFrame()
# 
# df_p1.head()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# sql_p1_0 = """
#         SELECT 
#           *
#         FROM rd_syst_orig_concat_2213_norm2
#           """
# df_2213 = %sql {sql_p1_0}
# df_2213 = df_2213.DataFrame()

# percentage of households that end up with 0 
measures = ['be','be2','ie','ble','bre10','bre24','bre70']
percent_of_0 = [round((len(df_2213[(df_2213['bundle']=='systematic')&(df_2213[measure]==0.0)])/2213),3) for measure in measures]
percent_of_0

"""### 5) FIGURE 3 of our paper

Evaluate PROPERTY 2 on 1,000 households due to computational cost.
"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# #-- Main table with 1,000 households
# sql_p2 = """SELECT household_key, basket_id,product_id
#            FROM rm.trans_data_cust_21_purch
#            WHERE household_key IN (SELECT DISTINCT household_key
#                                     FROM rm.trans_data_cust_21_purch
#                                     ORDER BY 1
#                                     LIMIT 1000) 
#            ORDER BY basket_id 
#                 """
# df_p2 = %sql {sql_p2}
# df_p2 = df_p2.DataFrame()
# 
# # Convert multiple columns
# df_p2 = df_p2.astype(float)
# df_p2.head()

"""#### Add systematic bundles to each consumer's basket"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# df_p2_with_syst_bundle_100 = pd.DataFrame(columns=['household_key','basket_id','product_id','items_added'])
# 
# #-- definition to add rows of items per basket_id
# def add_row(x):
#     #-- for loop to replace sample basket_id with the basket_id on the current group 
#     for row in range(items):
#         syst_bundle.iloc[row,0] = x.iloc[0,0]#row 0, column 0
#         syst_bundle.iloc[row,1] = x.iloc[0,1]#row 0, column 1
#     #-- add all items (rows) to df_syst
#     return x.append(syst_bundle)
# 
# #-- for loop to vary the numer of systematic items added to all of the original table 
# for items in range(1,11):
#     #-- get a syst(s) products from the original table, df_p2[df_p2['product_id']>=1] is to make shure we are not sample a negative number
#     syst_bundle = df_p2[df_p2['product_id']>=1].sample(n=items)
#     syst_bundle.product_id = syst_bundle.product_id*-1
# 
#     #-- apply to all of the original table the 'add_row' function per basket_id group 
#     df_syst = df_p2.groupby(['household_key','basket_id']).apply(add_row).reset_index(drop=True)
#      
#     #-- Add a column for number of items added
#     df_syst['items_added'] = items
# 
#     #-- Append df_syst to df_p2_with_syst_bundle
#     df_p2_with_syst_bundle_100 = pd.concat([df_syst,  df_p2_with_syst_bundle_100])
# 
# #-- save systematiccs csv 
# df_p2_with_syst_bundle_100.to_csv(f'df_p2_with_syst_bundle_100.csv', index=False)
# df_p2.to_csv(f'df_p2_original.csv', index=False)

df_p2_with_syst_bundle_1000 = pd.read_csv('df_p2_with_syst_bundle_100.csv')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# #-- Push dataframe into datbase (pgadmin)
# %sql --persist df_p2_with_syst_bundle_1000

"""#### Compute all measures per systematic bundle size (1 to 10)"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# #-- Empty dataframe 
# df_p2_added_items_norm = pd.DataFrame(columns=['household_key','items_added','be','be2','ie','ble','bre10','bre24','bre70'])
# 
# for item in range(1,11):
# 
#     sql_per_items = """SELECT household_key,
#                               items_added,
#                               round(bev3_norm(basket_id::TEXT, product_id::TEXT),2) as BE,
#                               round(norm_entropy(product_id::TEXT),2) as IE,
#                               round(joint_entropy(basket_id::TEXT, product_id::TEXT),2) as BLE,
#                               round(bre(basket_id::TEXT, product_id::TEXT,0.10 ),2) as BRE10,
#                               round(bre(basket_id::TEXT, product_id::TEXT,0.24 ),2) as BRE24,
#                               round(bre(basket_id::TEXT, product_id::TEXT,0.70 ),2) as BRE70
#                       FROM public.df_p2_with_syst_bundle_1000
#                       WHERE items_added = {}
#                       GROUP BY 1,2
#                       ORDER BY 1
#                     """.format(item)
#     df_per_items = %sql {sql_per_items}
#     df_per_items = df_per_items.DataFrame()
# 
#     #-- concat df_per_items entropies for each item group with df_p2_added_items
#     df_p2_added_items_norm = pd.concat([df_p2_added_items_norm,df_per_items])
# 
# #-- save systematiccs csv 
# df_p2_added_items_norm.to_csv(f'df_p2_added_items_1000_norm.csv', index=False)
# df_p2_added_items_norm = pd.read_csv('df_p2_added_items_1000_norm.csv')

#-- Convert multiple columns
df_p2_added_items_norm = df_p2_added_items_norm.astype(float)

df_to_plot = df_p2_added_items_norm.groupby(by='items_added').mean().reset_index()
df_to_plot.describe()

"""#### Lineplot for Property 2"""

plt.rcParams["figure.figsize"] = (9,7)

#-- NORMALIZED potential support for P2
df_to_plot.plot(x='items_added',y=['be','ie','ble','bre10','bre24','bre70'], kind='line',linewidth=3,marker= 'o', color=['lightseagreen','khaki','thistle','lightcoral','steelblue','sandybrown'])
    

plt.ylabel('Measure Value',fontsize=22)
plt.xlabel('Size of the added systematic bundle',fontsize=22)
plt.xticks(fontsize=22)
plt.ylim(-0.1,1.3)
plt.xlim(1,10)
plt.yticks(fontsize=22)
plt.legend(['BE','IE','BLE','BRE10','BRE24','BRE70'],fontsize=16, loc='upper right',frameon=True,  ncol=3)
plt.tight_layout()
#plt.title('Normalized - bev3_norm')
plt.show()