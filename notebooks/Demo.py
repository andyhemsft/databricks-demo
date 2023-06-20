# Databricks notebook source
# MAGIC %md # Training machine learning models on tabular data: an end-to-end example
# MAGIC
# MAGIC This tutorial covers the following steps:
# MAGIC - Import data from your local machine into the Databricks File System (DBFS)
# MAGIC - Visualize the data using Seaborn and matplotlib
# MAGIC - Run a parallel hyperparameter sweep to train machine learning models on the dataset
# MAGIC - Explore the results of the hyperparameter sweep with MLflow
# MAGIC - Register the best performing model in MLflow
# MAGIC - Apply the registered model to another dataset using a Spark UDF
# MAGIC - Set up model serving for low-latency requests
# MAGIC
# MAGIC In this example, you build a model to predict the quality of Portugese "Vinho Verde" wine based on the wine's physicochemical properties. 
# MAGIC
# MAGIC The example uses a dataset from the UCI Machine Learning Repository, presented in [*Modeling wine preferences by data mining from physicochemical properties*](https://www.sciencedirect.com/science/article/pii/S0167923609001377?via%3Dihub) [Cortez et al., 2009].
# MAGIC
# MAGIC ## Requirements
# MAGIC This notebook requires Databricks Runtime for Machine Learning.  
# MAGIC If you are using Databricks Runtime 7.3 LTS ML or below, you must update the CloudPickle library. To do that, uncomment and run the `%pip install` command in Cmd 2. 

# COMMAND ----------

# This command is only required if you are using a cluster running DBR 7.3 LTS ML or below. 
#%pip install --upgrade cloudpickle

# COMMAND ----------

# MAGIC %md ## Import data
# MAGIC   
# MAGIC In this section, you download a dataset from the web and upload it to Databricks File System (DBFS).
# MAGIC
# MAGIC 1. Navigate to https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/ and download both `winequality-red.csv` and `winequality-white.csv` to your local machine.
# MAGIC
# MAGIC 1. From this Databricks notebook, select **File > Upload data to DBFS...**, and drag these files to the drag-and-drop target to upload them to the Databricks File System (DBFS). 
# MAGIC
# MAGIC     **Note**: if you don't have the **File > Upload data to DBFS...** option, you can load the dataset from the Databricks example datasets. Uncomment and run the last two lines in the following cell.
# MAGIC
# MAGIC 1. Click **Next**. Auto-generated code to load the data appears. Under **Access Files from Notebooks**, select the **pandas** tab. Click **Copy** to copy the example code, and then click **Done**. 
# MAGIC
# MAGIC 1. Create a new cell, then paste in the sample code. It will look similar to the code shown in the following cell. Make these changes:
# MAGIC   - Pass `sep=';'` to `pd.read_csv`
# MAGIC   - Change the variable names from `df1` and `df2` to `white_wine` and `red_wine`, as shown in the following cell.

# COMMAND ----------

# If you have the File > Upload Data menu option, follow the instructions in the previous cell to upload the data from your local machine.
# The generated code, including the required edits described in the previous cell, is shown here for reference.

import pandas as pd

# In the following lines, replace <username> with your username.
# white_wine = pd.read_csv("/dbfs/FileStore/shared_uploads/<username>/winequality_white.csv", sep=';')
# red_wine = pd.read_csv("/dbfs/FileStore/shared_uploads/<username>/winequality_red.csv", sep=';')

# If you do not have the File > Upload Data menu option, uncomment and run these lines to load the dataset.

white_wine = pd.read_csv("/dbfs/databricks-datasets/wine-quality/winequality-white.csv", sep=";")
red_wine = pd.read_csv("/dbfs/databricks-datasets/wine-quality/winequality-red.csv", sep=";")

# COMMAND ----------

# MAGIC %md Merge the two DataFrames into a single dataset, with a new binary feature "is_red" that indicates whether the wine is red or white.

# COMMAND ----------

red_wine['is_red'] = 1
white_wine['is_red'] = 0

data = pd.concat([red_wine, white_wine], axis=0)

# Remove spaces from column names
data.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)

# COMMAND ----------

data.head()
