# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 00:42:54 2019

@author: yousuf
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.layers import fully_connected
from keras.datasets import mnist
from keras.layers import Input, Dense
from keras.models import Model
from keras.preprocessing import image
import numpy as np
# import pandas as pd
#import cv2,os,sys
#from sklearn.feature_extraction.text import CountVectorizer
#imagepath="/home/yousuf/Downloads/fraud_detection_document/pdf_images/bill_0.jpg"
#training_folder="/home/yousuf/Downloads/fraud_detection_document/pdf_images/training/"
#ldir=os.listdir(training_folder)
#vectorizer = CountVectorizer()
#from sklearn.feature_extraction.text import HashingVectorizer
#vectorizer = HashingVectorizer(n_features=20)
#vector = vectorizer.transform(text)

import numpy as np
import pandas as pd
import mysql.connector
import config
mysql = mysql.connector.connect(
  host=config.HOST,
  user=config.USER,
  passwd=config.PSWD,
  database = config.FRENNS_NAME5
  )
df = pd.read_sql('select syncinvoice_id, frenns_id, unique_frenns_id, syncsupplier_id, type, issue_date, due_date, collection_date, creation_date, last_updated, name, address, postcode, city,  contact_person,  email, invoice_number, currency, amount, vat_amount, outstanding_amount, paid, pay_date, invoiceId, customerId, updateId from syncinvoice ORDER BY syncinvoice_id asc', index_col=None,con=mysql)#.drop(['update_at','flags'],axis=1)#.drop([0],axis=0)
for i in range(0,len(df['syncinvoice_id'])):
    df.at[i,'label']=1 if df.loc[i,'paid']=='true' else 0
df1 = pd.read_sql('select syncinvoice_id, frenns_id, unique_frenns_id, syncsupplier_id, type, issue_date, due_date, collection_date, creation_date, last_updated, name, address, postcode, city,  contact_person,  email, invoice_number, currency, amount, vat_amount, outstanding_amount, paid, pay_date, invoiceId, customerId, updateId from syncinvoice ORDER BY syncinvoice_id desc LIMIT 1', index_col=None,con=mysql)#.drop(['update_at','flags'],axis=1)#.drop([0],axis=0)
for i in range(0,len(df1['syncinvoice_id'])):
    df1.at[i,'label']=1 if df1.loc[i,'paid']=='true' else 0
#print(df.head)
categorical_attr_names=['frenns_id','unique_frenns_id','paid','type','name', 'address', 'postcode', 'city', 'contact_person', 'email','invoice_number', 'currency','invoiceId', 'customerId', 'updateId','pay_date','issue_date', 'due_date', 'collection_date', 'creation_date', 'last_updated']
#ori_dataset_numeric_attr=df.drop(categorical_attr_names,axis=1)
numeric_attr_names = ['syncinvoice_id', 'syncsupplier_id', 'amount', 'vat_amount', 'outstanding_amount']
numeric_attr = df[numeric_attr_names] + 1e-7
numeric_attr = numeric_attr.apply(np.log)
ori_dataset_numeric_attr = (numeric_attr - numeric_attr.min()) / (numeric_attr.max() - numeric_attr.min())
#print(ori_dataset_numeric_attr.shape,ori_dataset_numeric_attr.head(10))
ori_dataset_categ_transformed = pd.get_dummies(df[categorical_attr_names])
#print(ori_dataset_categ_transformed.shape)
ori_subset_transformed = pd.concat([ori_dataset_categ_transformed, ori_dataset_numeric_attr], axis = 1)
#print(ori_subset_transformed.head(10))
test=ori_subset_transformed[-1:]
kkk=ori_subset_transformed.iloc[-1]

numeric_attr1 = df1[numeric_attr_names] + 1e-7
numeric_attr1 = numeric_attr1.apply(np.log)
ori_dataset_numeric_attr1 = (numeric_attr1 - numeric_attr1.min()) / (numeric_attr1.max() - numeric_attr1.min())
#print(ori_dataset_numeric_attr.shape,ori_dataset_numeric_attr.head(10))
ori_dataset_categ_transformed1 = pd.get_dummies(df1[categorical_attr_names])
#print(ori_dataset_categ_transformed.shape)
ori_subset_transformed1 = pd.concat([ori_dataset_categ_transformed1, ori_dataset_numeric_attr1], axis = 1)

ori_dataset_numeric_attr=pd.concat([ori_dataset_numeric_attr, df['label']], axis = 1)




#image=cv2.imread(imagepath)
#gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#gray1=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY).astype('float32')/255.0
#variance=gray.var()
#print(gray.shape)
#(X_train, _), (X_test, _) = mnist.load_data()
#train_image = []
#from tqdm import tqdm
#for i in tqdm(range(1,len(ldir)+1)):
#    imagepath=training_folder+str(i)+'.jpg'
#    image1=cv2.imread(imagepath)
#    gray=cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
#    dim=(50,50)
#    gray = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA) 
##    img = image.load_img(training_folder+str(i)+'.jpg', target_size=(1000,1000,1), grayscale=False)
##    img1 = image.load_img(training_folder+str(i)+'.jpg', target_size=(1000,1000,1), grayscale=False)
##    img = image.img_to_array(gray)
#    img = gray.astype('float32').flatten()/255.0
#    train_image.append(img)
#class array():
#    def __init__(self,df):
#        self.array=np.array(df)
#
#X=array(ori_subset_transformed)
#print(X.array)


X1=np.array(ori_dataset_numeric_attr1.drop(['syncinvoice_id','syncsupplier_id'],axis=1))
#X = np.array(ori_dataset_numeric_attr.drop(['syncinvoice_id','syncsupplier_id'],axis=1))
X=np.array(ori_subset_transformed)
y=np.array(df['label'])
#y1=np.array(df1['label'])
from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(X, random_state=42, test_size=0.2)
#print(X_train.shape,X_test.shape)#


#from keras.models import Sequential
#model = Sequential()
#model.add(Dense(1024, input_dim=3, activation='relu'))
#model.add(Dense(512, activation='relu'))
#model.add(Dense(256, activation='relu'))
#model.add(Dense(128,activation='relu'))
#model.add(Dense(64, activation='relu'))
#model.add(Dense(32, activation='relu'))
#model.add(Dense(64, activation='relu'))
#model.add(Dense(128, activation='relu'))
#model.add(Dense(256, activation='relu'))
#model.add(Dense(512, activation='relu'))
#model.add(Dense(1024, activation='relu'))
#model.add(Dense(3, activation='sigmoid'))
#
#
#
#model1 = Sequential()
#model1.add(Dense(1024, input_dim=3, activation='relu'))
#model1.add(Dense(512, activation='relu'))
#model1.add(Dense(256, activation='relu'))
#model1.add(Dense(128,activation='relu'))
#model1.add(Dense(64, activation='relu'))
#model1.add(Dense(32, activation='relu'))



#model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit the keras model on the dataset
#model.fit(X_train, X_train, epochs=20, batch_size=32, verbose=1)
# make class predictions with the model
#predictions = model1.predict_classes(X_test)
#predicted = model.predict_classes(X_test)
#from sklearn.metrics import confusion_matrix
#matrix=confusion_matrix(X_test,predictions)
#print(X_test.shape,predicted.shape,predicted)
#scores=model.evaluate(X_test,X_test,verbose=1)
#print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))
#print("....................................../n")
#print(scores)



#model_json=model.to_json()
#with open("model.json","w") as json_file:
#    json_file.write(model_json)
#model.save_weights("model.h5")




#from keras.models import model_from_json
#json_file=open("model.json","r")
#loaded_model_json=json_file.read()
#json_file.close()
#loaded_model=model_from_json(loaded_model_json)
#loaded_model.load_weights("model.h5")
#loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


input_img= Input(shape=(len(kkk),))
encoded = Dense(units=1024, activation='relu')(input_img)
encoded = Dense(units=512, activation='relu')(encoded)
encoded = Dense(units=256, activation='relu')(encoded)
encoded = Dense(units=128, activation='relu')(encoded)
encoded = Dense(units=64, activation='relu')(encoded)
encoded = Dense(units=32, activation='relu')(encoded)
decoded = Dense(units=64, activation='relu')(encoded)
decoded = Dense(units=128, activation='relu')(decoded)
decoded = Dense(units=256, activation='relu')(decoded)
decoded = Dense(units=512, activation='relu')(decoded)
decoded = Dense(units=1024, activation='relu')(decoded)
decoded = Dense(units=len(kkk), activation='sigmoid')(decoded)
##decoded = Dense(units=3, activation='sigmoid')(decoded)
autoencoder=Model(input_img, decoded)
encoder = Model(input_img, encoded)
#autoencoder.summary()
#encoder.summary()

autoencoder.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
autoencoder.fit(X_train, X_train,
                epochs=20,
                batch_size=256,
                shuffle=True,
                validation_data=(X_test, X_test))
encoded_imgs = encoder.predict(X_test)
#print(encoded_imgs)
predicted = autoencoder.predict(X_test)
model_json=autoencoder.to_json()
with open("model.json","w") as json_file:
    json_file.write(model_json)
autoencoder.save_weights("model.h5")

#compare=np.allclose(X_test, predicted,rtol=0.1,atol=0.2,equal_nan=True)#rtol=0.2,atol=0.2
#print(compare)
#print(X_test.shape,predicted.shape,predicted)
print(predicted.shape)
mysql.close()



