

def ae(ids):
    # try:
        import numpy as np
        import pandas as pd
        #import matplotlib.pyplot as plt
        #import tensorflow as tf
        #from tensorflow.examples.tutorials.mnist import input_data
        #from tensorflow.contrib.layers import fully_connected
        #from keras.datasets import mnist
        #from keras.layers import Input, Dense
        #from keras.models import Model
        #from keras.preprocessing import image
        #import numpy as np
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
        #df1 = pd.read_sql('select syncinvoice_id, frenns_id, unique_frenns_id, syncsupplier_id, type, issue_date, due_date, collection_date, creation_date, last_updated, name, address, postcode, city,  contact_person,  email, invoice_number, currency, amount, vat_amount, outstanding_amount, paid, pay_date, invoiceId, customerId, updateId from syncinvoice ORDER BY syncinvoice_id desc LIMIT 1', index_col=None,con=mysql)#.drop(['update_at','flags'],axis=1)#.drop([0],axis=0)
        df = pd.read_sql('select bs_call,bs_put,syncinvoice_id, frenns_id, unique_frenns_id, syncsupplier_id, type, issue_date, due_date, collection_date, creation_date, last_updated, name, address, postcode, city,  contact_person,  email, invoice_number, currency, amount, vat_amount, outstanding_amount, paid, pay_date, invoiceId, customerId, updateId from syncinvoice ORDER BY syncinvoice_id asc', index_col=None,con=mysql)#.drop(['update_at','flags'],axis=1)#.drop([0],axis=0)
        
        #for i in range(0,len(df1['syncinvoice_id'])):
        #    df1.at[i,'label']=1 if df1.loc[i,'paid']=='true' else 0
        #print(df.head)
        #categorical_attr_names=['frenns_id','unique_frenns_id','paid','type','name', 'address', 'postcode', 'city', 'contact_person', 'email','invoice_number', 'currency','invoiceId', 'customerId', 'updateId','pay_date','issue_date', 'due_date', 'collection_date', 'creation_date', 'last_updated']
        ##ori_dataset_numeric_attr=df.drop(categorical_attr_names,axis=1)
        #numeric_attr_names = ['syncinvoice_id', 'syncsupplier_id', 'amount', 'vat_amount', 'outstanding_amount']
        #
        #numeric_attr1 = df1[numeric_attr_names] + 1e-7
        #numeric_attr1 = numeric_attr1.apply(np.log)
        #ori_dataset_numeric_attr1 = (numeric_attr1 - numeric_attr1.min()) / (numeric_attr1.max() - numeric_attr1.min())
        #
        #
        #
        #X1=np.array(ori_dataset_numeric_attr1.drop(['syncinvoice_id','syncsupplier_id'],axis=1))
        #y1=np.array(df1['label'])
        
        categorical_attr_names=['frenns_id','unique_frenns_id','paid','type','name', 'address', 'postcode', 'city', 'contact_person', 'email','invoice_number', 'currency','invoiceId', 'customerId', 'updateId','pay_date','issue_date', 'due_date', 'collection_date', 'creation_date', 'last_updated']
        #ori_dataset_numeric_attr=df.drop(categorical_attr_names,axis=1)
        numeric_attr_names = ['syncinvoice_id', 'syncsupplier_id', 'amount', 'vat_amount', 'outstanding_amount','bs_call','bs_put']
        numeric_attr = df[numeric_attr_names].astype('float32') + 1e-7
        numeric_attr = numeric_attr.apply(np.log)
        ori_dataset_numeric_attr = (numeric_attr - numeric_attr.min()) / (numeric_attr.max() - numeric_attr.min())
        #print(ori_dataset_numeric_attr.shape,ori_dataset_numeric_attr.head(10))
        ori_dataset_categ_transformed = pd.get_dummies(df[categorical_attr_names])
        #print(ori_dataset_categ_transformed.shape)
        ori_subset_transformed = pd.concat([ori_dataset_categ_transformed, ori_dataset_numeric_attr], axis = 1)
        #print(ori_subset_transformed.head(10))
        length=len(ori_subset_transformed)
        ids=int(ids)-1
        ids=int(ids)
        if length>int(ids):
            ids=length-int(ids)+1
        else:
            ids=1    
        test=ori_subset_transformed[-ids:]
        kkk=ori_subset_transformed.iloc[-ids]
        test=np.array(test)
        #numeric_attr1 = df1[numeric_attr_names] + 1e-7
        #numeric_attr1 = numeric_attr1.apply(np.log)
        #ori_dataset_numeric_attr1 = (numeric_attr1 - numeric_attr1.min()) / (numeric_attr1.max() - numeric_attr1.min())
        ##print(ori_dataset_numeric_attr.shape,ori_dataset_numeric_attr.head(10))
        #ori_dataset_categ_transformed1 = pd.get_dummies(df1[categorical_attr_names])
        ##print(ori_dataset_categ_transformed.shape)
        #ori_subset_transformed1 = pd.concat([ori_dataset_categ_transformed1, ori_dataset_numeric_attr1], axis = 1)
        #
        #ori_dataset_numeric_attr=pd.concat([ori_dataset_numeric_attr, df['label']], axis = 1)
        #
        
        
        
        
        
        #model_json=model.to_json()
        #with open("model.json","w") as json_file:
        #    json_file.write(model_json)
        #model.save_weights("model.h5")
        
        from keras.models import model_from_json
        json_file=open("model.json","r")
        loaded_model_json=json_file.read()
        json_file.close()
        loaded_model=model_from_json(loaded_model_json)
        loaded_model.load_weights("model.h5")
        loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        
        # make class predictions with the model
        predictions = loaded_model.predict(test)
        
        #from sklearn.metrics import confusion_matrix
        #matrix=confusion_matrix(y1,predictions)
        #print(y1,predictions)
        #input_img= Input(shape=(3916,))
        #encoded = Dense(units=1024, activation='relu')(input_img)
        #encoded = Dense(units=512, activation='relu')(encoded)
        #encoded = Dense(units=256, activation='relu')(encoded)
        #encoded = Dense(units=128, activation='relu')(encoded)
        #encoded = Dense(units=64, activation='relu')(encoded)
        #encoded = Dense(units=32, activation='relu')(encoded)
        #encoded = Dense(units=1, activation='sigmoid')(encoded)
        ##decoded = Dense(units=32, activation='relu')(encoded)
        ##decoded = Dense(units=64, activation='relu')(decoded)
        ##decoded = Dense(units=128, activation='relu')(decoded)
        ##decoded = Dense(units=256, activation='relu')(decoded)
        ##decoded = Dense(units=512, activation='relu')(decoded)
        ##decoded = Dense(units=1024, activation='relu')(decoded)
        ##decoded = Dense(units=3916, activation='sigmoid')(decoded)
        #autoencoder=Model(input_img, encoded)
        ##encoder = Model(input_img, encoded)
        ##autoencoder.summary()
        ##encoder.summary()
        #autoencoder.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        #autoencoder.fit(X_train, y_train,
        #                epochs=10,
        #                batch_size=32,
        #                shuffle=True,
        #                validation_data=(X_test, y_test))
        ##encoded_imgs = encoder.predict(X_test)
        ##print(encoded_imgs)
        #predicted = autoencoder.predict(X_test)
        
        # print(test.shape, predictions.shape)
        compare=np.allclose(test, predictions,rtol=0.4,atol=0.4,equal_nan=True)#rtol=0.2,atol=0.2,
        same=[]
        from tqdm import tqdm
        for i in tqdm(range(0,test.shape[0])):
            for j in range(0,test.shape[1]):
                diff=abs(test[i,j]-predictions[i,j])
                if diff<0.1:
                    same.append(diff)     
        score=len(same)
        total_size=test.shape[0]*test.shape[1]
        absolute=float(abs(total_size-score))
        deviation=(absolute/total_size+0.00001)*100
        # average=(total_size+score)/2.00
    #    print(absolute,average)
        # percentage_deviation=(absolute/average+0.001)*100
        # print(deviation)
        if deviation<27:
            compare=True
        else:
            compare=False
        mysql.close()
        return deviation,compare
    # except Exception as e:
    #     compare="Error in loading Autoencoder"
    #     # mysql.close()
    #     return e
        
# ae(10)

