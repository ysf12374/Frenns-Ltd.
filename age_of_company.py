import numpy as np
import pandas as pd
import mysql.connector
import pandas as pd
from sklearn import model_selection
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import matplotlib.pyplot as plt
mysql = mysql.connector.connect(
  host="144.76.137.232",
  user="vkingsolextadmin",
  passwd="~O3o3y4h",
  database = "clearsight_development"
)
def company_age(cn):
    df1=pd.read_sql("select DATEDIFF(CURDATE(), STR_TO_DATE(IncorporationDate, '%d/%m/%Y')) AS days from company_data where CompanyNumber="+str(cn), con=mysql)
    return df1['days'].values[0]
from tqdm import tqdm
mycursor=mysql.cursor()
df=pd.read_sql("select distinct CompanyNumber from company_data", con=mysql)
for i in tqdm(range(2280,len(df['CompanyNumber']))):
    mycursor.execute("SELECT company_age FROM company_analysis WHERE CompanyNumber='"+str(df.loc[i,'CompanyNumber'])+"' ")
    ids=mycursor.fetchall()
    if ids:
        sql_update_query = "UPDATE company_analysis set company_age = '"+str(company_age(df.loc[i,'CompanyNumber']))+"' where CompanyNumber = '"+str(df.loc[i,'CompanyNumber'])+"'"
        mycursor.execute(sql_update_query)
        mysql.commit()
mycursor.close()
mysql.close()