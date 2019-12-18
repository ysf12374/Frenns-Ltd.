# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 22:24:45 2019

@author: Yousuf
"""
frenns='FRN100000570'
reg='04378201'
namez='BP P.L.C'
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
  database = "vkingsol_frennsdevelopment"
)

df=pd.read_sql('select syncinvoice_id,amount, vat_amount, outstanding_amount,paid from syncinvoice', con=mysql)
x=pd.read_sql('select amount, vat_amount, outstanding_amount from syncinvoice', con=mysql)
df_out=df['paid']
syncid=df['syncinvoice_id']
df1=df['amount'].values.astype('float32')
df2=df['vat_amount'].values.astype('float32')    
df3=df['outstanding_amount'].values.astype('float32')    
df_no_plot=df['syncinvoice_id'].values.astype(int)
#df_out=[1 for i in df_out if i =='true']     +
X=x.values.astype('float32')

for i in range(0,len(df_out)):
    if df_out[i]=='true':
        df_out.at[i]=1      
    elif df_out[i]=='false':
        df_out.at[i]=0
    else:
        df_out.at[i]=2
Y=df_out.values.astype(int)
## import the necessary packages
#from sklearn.preprocessing import LabelBinarizer
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import classification_report
#from keras.models import Sequential
#from keras.layers.core import Dense
#from keras.optimizers import SGD
#from imutils import paths
#import matplotlib.pyplot as plt
#import numpy as np
#import argparse
#import random

#validation_size = 0.11
#seed=7
#X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
#scoring = 'accuracy'
#models = []
#models.append(('LR', LogisticRegression()))
##lb = LabelBinarizer()
##Y_train = lb.fit_transform(Y_train)
##Y_validation = lb.transform(Y_validation)
##
##
### define the 3072-1024-512-3 architecture using Keras
##model = Sequential()
##model.add(Dense(256, input_dim=3, init='uniform', activation='sigmoid'))
###model.add(Dense(512, input_dim=3, init='normal', activation="sigmoid"))
###model.add(Dense(10, activation="sigmoid"))
##model.add(Dense(64, activation="sigmoid"))
###model.add(Dense(32, activation="relu"))
##model.add(Dense(3, activation="softmax"))
##
### initialize our initial learning rate and # of epochs to train for
##INIT_LR = 0.01
##EPOCHS = 10
### Compile model
##model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
### Fit the model
##H = model.fit(X_train, Y_train, validation_data=(X_validation, Y_validation),epochs=EPOCHS, batch_size=32)
###H=model.fit(X_train, Y_train, epochs=15, batch_size=10,  verbose=3)
###predictions = model.predict(X_validation[0])
##scores = model.evaluate(X_validation, Y_validation)
##print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
### calculate predictions
##
### evaluate the network
##print("[INFO] evaluating network...")
##predictions = model.predict(X_validation, batch_size=32)
###print(classification_report(Y_validation.argmax(axis=1),
###	predictions.argmax(axis=1), target_names=lb.classes_))
##
### plot the training loss and accuracy
##N = np.arange(0, EPOCHS)
##plt.style.use("ggplot")
##plt.figure()
##plt.plot(N, H.history["loss"], label="train_loss")
##plt.plot(N, H.history["val_loss"], label="val_loss")
##plt.plot(N, H.history["acc"], label="train_acc")
##plt.plot(N, H.history["val_acc"], label="val_acc")
##plt.title("Training Loss and Accuracy (Simple NN)")
##plt.xlabel("Epoch #")
##plt.ylabel("Loss/Accuracy")
##plt.legend()
##plt.savefig("plot.png")
## compile the model using SGD as our optimizer and categorical
## cross-entropy loss (you'll want to use binary_crossentropy
## for 2-class classification)
#
#models.append(('KNN', KNeighborsClassifier()))
##models.append(('SVM', SVC(kernel='linear', C=0.01)))
#results = []
#names = []
#
#for name, model in models:
#	kfold = model_selection.KFold(n_splits=10, random_state=seed)
#	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
#	results.append(cv_results)
#	names.append(name)
#	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
#	print(msg)
#lr = KNeighborsClassifier()
#lr.fit(X_train, Y_train)
#X_validation=X_validation[0:1,:]
#Y_validation=Y_validation[0]
##X_validation=np.transpose(X_validation)
#predictions = lr.predict(X_validation)
#print('LogisticRegression')
#print(accuracy_score(Y_validation, predictions))
#print(confusion_matrix(Y_validation, predictions))

for i in syncid:
    j=str(i)
    data=pd.read_sql('select frenns_id,name,paid from syncinvoice where syncinvoice_id="'+j+'"', con=mysql)
    frens=data['frenns_id'].values.astype(str)
    frens=max(frens)
    namz=data['name'].values.astype(str)
    namz=max(namz)
    dcsn=data['paid']
    if dcsn[0]=='true':
        dcsn=1
        dcs='yes'
    elif dcsn[0]=='false':
        dcsn=0
        dcs='no'
    else:
        dcsn=0
        dcs='no'
    records=[str(frens),str(namz),str(dcsn),str(dcs)]
    sql="INSERT INTO ML(frenns_id,name,class,decision) VALUES (%s,%s,%s,%s)" #         
    cursor=mysql.cursor()
    cursor.execute(sql,records)
    mysql.commit()
    print("Record Inserted into table")
cursor.close()    
mysql.commit()
mysql.close()
#from sklearn.cluster import KMeans
#from matplotlib import style
#import matplotlib.pyplot as plt
#X=np.array([df1,df2,df3])
#
#X=X.transpose()
#kmeans = KMeans(n_clusters=8)
#kmeans.fit(X)
#
#centroids = kmeans.cluster_centers_
#labels = kmeans.labels_
#
#print(centroids)
#print(labels)       
#colors = ["g.","r.","c.","y.",".b",".m",".k",".w"]
#
#labels_plot=labels.astype(int)
##for i in range(0,len(X)):
##    print("coordinate:",X[i], "label:", labels[i])
##    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)
##
##plt.scatter(centroids[:, 0],centroids[:, 1], marker = "x", s=150, linewidths = 5, zorder = 10)
##
##
##pdd=df[[0]]
#
#
#labels=pd.DataFrame(labels)
#report=pd.concat([df_no,labels],axis=1)
#for i in range(0,len(X)):
#    plt.plot(df_no_plot[i], labels_plot[i], colors[labels_plot[i]], markersize = 10)
#plt.show()
#ff=pd.read_sql('select company_name from syncfinancialanalysis where company_name = "' + namez + '" and frenns_id = "' + frenns + '"', con=mysql)# 
#updatesql=ff['company_name']
#df=df.groupby('frenns_id').mean()
#updsql=updatesql.as_matrix()
#df=df.values.flatten()
## set the matplotlib backend so figures can be saved in the background
#import matplotlib
#matplotlib.use("Agg")
#

#import pickle
#import cv2
#import os
#
#(trainX, testX, trainY, testY) = train_test_split(data,
#	labels, test_size=0.25, random_state=42)

###########################################################################################################
####### These are mysql queries to select the columns from clearsight_development table  ##################
###########################################################################################################

#df = pd.read_sql('select * from company_ann_reports where CompanyNumber = "' + reg + '"', con=mysql)
#llf=pd.read_sql('select Result from fraud_analysis where CompanyNumber="' + reg + '"', con=mysql)
#
#pp=pd.read_sql('select CompanyNumber from ML where CompanyNumber ="' + reg + '"', con=mysql)
#try:
#    updatesql=pp['CompanyNumber']
#    updsql=len(updatesql)
#except:
#    updsql=0;
#
#df=df.drop(['URL','NAME','CompanyNumber','YEAR'],axis=1)
#df1=df.mean().transpose()#.reset_index().drop(['index'],axis=1)
#
##mycursor=mysql.cursor()
#records=[str(df1['work_cap']),str(df1['COS']),str(df1['curr_ass']),str(df1['fix_ass']),str(df1['tot_ass']),str(df1['depr_amort']),str(df1['PPE']),str(df1['SGA']),str(df1['Long_term_d']),str(df1['curr_lia']),str(df1['inc_tax']),str(df1['cash']),str(df1['sales']),str(df1['pnl_before_tax']),str(df1['pnl_after_tax']),str(df1['grossprofit']),str(llf['Result'].iloc[0])]
#if updsql==0:
#    sql = "INSERT INTO ML(CompanyNumber, NAME,creditrating, creditscore,creditlimit,revenue) VALUES(%s,%s,%s,%s,%s,%s)"#,combinedcreditscore,combinedpurchasescore)
#    mycursor.execute(sql,records)
#    mysql.commit()
#    mycursor.close()
#    print(records)
#    #mysql.close()
#else:
#    sql="UPDATE ML SET creditrating=%s,creditscore=%s,creditlimit=%s,revenue=%s  WHERE CompanyNumber='" + reg + "'" #,combinedcreditscore=%s,combinedpurchasescore=%s                                        
#    mycursor.execute(sql,recds)
#    mysql.commit()
#    mycursor.close()
#    print(recds)
#    mysql.close()
#mycursor.close()
#mysql.close()
