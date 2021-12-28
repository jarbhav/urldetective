import pandas as pd 
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score

urldata = pd.read_csv("lotofdata.csv")


#Predictor Variables
#x = urldata[['hostname_length',
       #'path_length', 'fd_length', 'tld_length', 'count-', 'count@', 'count?',
       #'count%', 'count.', 'count=', 'count-http','count-https', 'count-www', 'count-digits']]
x = urldata[['short_url', 'use_of_ip', 'count-', 'count@', 'count?', 'count%', 'count.', 'count=', 'count-http', 'count-https', 'count-www', 'count-digits', 'count-letters', 'count_dir', 'url_length', 'hostname_length', 'path_length', 'fd_length', 'tld_length']]


#Target Variable
y = urldata['label']



#Splitting the data into Training and Testing
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.3, random_state=42)

#Random Forest
rfc = RandomForestClassifier()
rfc.fit(x_train, y_train)

rfc_predictions = rfc.predict(x_test)
accuracy_score(y_test, rfc_predictions)
print(confusion_matrix(y_test,rfc_predictions))

pickle.dump(rfc, open('RFCmodelfin.pkl', 'wb'))