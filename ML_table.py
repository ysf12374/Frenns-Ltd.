# -*- coding: utf-8 -*-
"""
Created on Wed May 01 23:28:18 2019

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
  host="144.76.137.232",#"localhost",
  user="vkingsol_demo",
  passwd="gUj3z5?9",
  database = "vkingsol_frennsdevelopment"
  )
df=pd.read_sql('select amount,vat_amount,outstanding_amount,paid from syncinvoice', con=mysql)
x=pd.read_sql('select amount, vat_amount, outstanding_amount from syncinvoice', con=mysql)
frn=pd.read_sql('select frenns_id from syncinvoice', con=mysql)
df.paid=df.paid.replace([''],1)
df.paid=df.paid.replace(['false'],0)
df.paid=df.paid.replace(['true'],1)
X=df.iloc[:,:3]
Y=df.iloc[:,3]
F=frn.iloc[:,:1]
validation_size = 0.11
seed=7
#X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
#scoring = 'accuracy'
#models = []
#models.append(('LR', LogisticRegression()))
#models.append(('KNN', KNeighborsClassifier(n_neighbors=5)))
#models.append(('SVM', SVC(kernel='linear', C=0.01)))
#results = []
#names = []
#for name, model in models:
#	kfold = model_selection.KFold(n_splits=10, random_state=seed)
#	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
#	results.append(cv_results)
#	names.append(name)
#	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
##	print(msg)
#svc = SVC()
#svc.fit(X_train, Y_train)
#predictions = svc.predict(X_validation)
#print('Support Vector Machine')
#print(accuracy_score(Y_validation, predictions))
#print(confusion_matrix(Y_validation, predictions))

x1=df.iloc[1:2,:3]
#pr=svc.predict(x1)
L=X.loc[1,'amount']


#from keras.models import Sequential
#from keras.layers import Dense

#df.paid=df.paid.replace([''],1)
#df.paid=df.paid.replace(['false'],0)
#X=df.iloc[:,:3]
#from keras.utils import to_categorical
#one-hot encode target column
#Y = to_categorical(df.iloc[:,3])

#vcheck that target column has been converted
#train_y_2[0:5]
#Y=df.iloc[:,3]
#
#
##create model
#model_2 = Sequential()
#
##get number of columns in training data
#n_cols_2 = train_X_2.shape[1]
#
##add layers to model
#model_2.add(Dense(250, activation='relu', input_shape=(n_cols_2,)))
#model_2.add(Dense(250, activation='relu'))
#model_2.add(Dense(250, activation='relu'))
#model_2.add(Dense(2, activation='softmax'))
#
#model_2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#model_2.fit(X_2, target, epochs=30, validation_split=0.2, callbacks=[early_stopping_monitor])

#for i in range(0,len(X)):
#    mycursor=mysql.cursor()
#    rec=[str(i+1),str(F.loc[i,'frenns_id']),str(X.loc[i,'amount']),str(X.loc[i,'vat_amount']),str(X.loc[i,'outstanding_amount']),str(Y.iloc[i]),'yes' if Y.iloc[i]==1 else 'no']
#    uu=pd.read_sql('select amount from ML where id={0}'.format(i+1), con=mysql)
#    try:
#        upd=uu['amount']
#    except:
#        upd=0
#    if len(upd)==0:
#        sql="INSERT INTO ML(id, frenns_id, amount, vat_amount, outstanding_amount, class,decision) VALUES (%s,%s,%s,%s,%s,%s,%s)";mycursor.execute(sql,rec);mysql.commit()
#mycursor.close()
#mysql.commit()
#mysql.close()

#inx={'amount':[1],'vat_amount':[2],'outstanding_amount':[3],'paid':[0]}
#inp=pd.DataFrame(data=inx)
#
#ml=pd.read_sql('select frenns_id from ML', con=mysql)
#j=0
for i in range(0,len(X)):
    mycursor=mysql.cursor()
#    rec=[str(i+1),str(F.loc[i,'frenns_id']),str(X.loc[i,'amount']),str(X.loc[i,'vat_amount']),str(X.loc[i,'outstanding_amount']),str(Y.iloc[i]),'yes' if Y.iloc[i]==1 else 'no']
    uu=pd.read_sql('select amount from ML where id={0}'.format(i+1), con=mysql)
    try:
        upd=uu['amount']
    except:
        upd=0
    
    benford1=pd.read_sql('select value from syncfraudanalysis where area="Benfords law 1st digit" and frenns_id="{0}"'.format(F.loc[i,'frenns_id']), con=mysql)
    benford2=pd.read_sql('select value from syncfraudanalysis where area="Benfords law 2nd digit" and frenns_id="{0}"'.format(F.loc[i,'frenns_id']), con=mysql)
    beneish=pd.read_sql('select value from syncfraudanalysis where area="Beneish-M Score" and frenns_id="{0}"'.format(F.loc[i,'frenns_id']), con=mysql)
    zscore=pd.read_sql('select value from syncfraudanalysis where area="Z Score" and frenns_id="{0}"'.format(F.loc[i,'frenns_id']), con=mysql)
    benford1=benford1.mean().values
    benford2=benford2.mean().values
    try:
        beneish=beneish.mean().values
    except:
        beneish=0
    zscore=zscore.mean().values
    if beneish<=-2.22:
        scorebeneish=2
    else:
        scorebeneish=0
    if benford1>=15:
        scorebrad1=0
    else:
        scorebrad1=1
    if benford2>=15:
        scorebrad2=0
    else:
        scorebrad2=1
    if zscore<=2:
        scorez=1
    else:
        scorez=0
#    import clearsight_final
#    clearsight=clearsight_final.regnum()
    credit=pd.read_sql('select avg(creditscore) as creditscore,avg(purchasescore) as purchasescore from syncfinancialanalysis where frenns_id="{0}"'.format(F.loc[i,'frenns_id']), con=mysql)
    Credit_Score=credit.creditscore.values
    
    Purchase_Score=credit.purchasescore.values

    if 1<Credit_Score<=470:
        CreditRating=0;
    elif 471<=Credit_Score<=519:
        CreditRating=1;
    elif 520<=Credit_Score<=568:
        CreditRating=2;
    elif 569<=Credit_Score<=617:
        CreditRating=3;
    elif 618<=Credit_Score<=666:
        CreditRating=4;
    elif 667<=Credit_Score<=715:
        CreditRating=5;
    elif 716<=Credit_Score<=764:
        CreditRating=6;
    elif 765<=Credit_Score<=813:
        CreditRating=7;
    else:
        CreditRating=0
    if 1<Purchase_Score<=300:
        PurchaseRating=0;
    elif 301<=Purchase_Score<=335:
        PurchaseRating=1;
    elif 336<=Purchase_Score<=371:
        PurchaseRating=2;
    elif 372<=Purchase_Score<=406:
        PurchaseRating=3;
    elif 407<=Purchase_Score<=441:
        PurchaseRating=4;
    elif 442<=Purchase_Score<=477:
        PurchaseRating=5;
    elif 478<=Purchase_Score<=512:
        PurchaseRating=6;
    elif 513<=Purchase_Score<=548:
        PurchaseRating=7;
    else:
        PurchaseRating=0 
    score=scorebeneish+scorebrad1+scorebrad2+scorez+CreditRating+PurchaseRating+Y.iloc[i]
#    print(scorebeneish,scorebrad1,scorebrad2,scorez,CreditRating,PurchaseRating,Y.iloc[i])
    if 0<=score<=8:
        cls=0
    else:
        cls=1
    
    rec=[str(i+1),str(F.loc[i,'frenns_id']),str(X.loc[i,'amount']),str(X.loc[i,'vat_amount']),str(X.loc[i,'outstanding_amount']),str(cls),'yes' if cls==1 else 'no',str(score)]

    if len(upd)==0:
        sql="INSERT INTO ML(id, frenns_id, amount, vat_amount, outstanding_amount, class,decision,score) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)";mycursor.execute(sql,rec);mysql.commit()

mycursor.close()
mysql.close()


