import pandas as pd
import numpy as np
from sklearn.utils import shuffle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report
import pickle
print(os.listdir("../media")[0])
data = pd.read_csv('../media/' + os.listdir("../media")[0])
new_data = data[data['proto'] == "DNS"]
new_data = new_data.dropna(subset=['subproto'])
new_data['proto'], new_data['subproto'] = new_data['subproto'], new_data['proto']
data = data.loc[data['proto'] != 'DNS']
data = data.append(new_data)
data = shuffle(data)
drop_protos = ["Unknown", "Unencryped_Jabber", "NTP", "Apple", "AppleiTunes"]
replace_protos = [("SSL_No_Cert", "SSL")]
data = data[~data["proto"].isin(drop_protos)]
for old_proto, new_proto in replace_protos:
    data = data.replace(old_proto, new_proto)
proto_clusters = [data[data["proto"] == proto] for proto in data["proto"].unique()]
train_clusters = []
test_clusters = []
for cluster in proto_clusters:
    np.random.seed(42)
    cluster = cluster.iloc[np.random.permutation(len(cluster))]
    split_index = len(cluster) // 3
    train_clusters.append(cluster.iloc[:split_index])
    test_clusters.append(cluster.iloc[split_index:])
train_data = pd.concat(train_clusters)
test_data = pd.concat(test_clusters)
scaler = StandardScaler()
X_train = scaler.fit_transform(train_data.drop(["proto", "subproto"], axis=1))
X_test = scaler.transform(test_data.drop(["proto", "subproto"], axis=1))

labeler = LabelEncoder()
y_train = labeler.fit_transform(train_data["proto"])
y_test = labeler.transform(test_data["proto"])

X = scaler.fit_transform(train_data.drop(["proto", "subproto"], axis=1))
y = labeler.fit_transform(train_data["proto"])

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
list_final = []
for i in range(1, len(X_test)):
    a = labeler.inverse_transform(model.predict(X_test[i:i + 1]))
    list_final.append([data[i:i + 1]['proto'].tolist()[0], data[i:i + 1]['client_bytes'].tolist()[0],
                       data[i:i + 1]['server_bytes'].tolist()[0], data[i:i + 1]['client_payload'].tolist()[0],
                       data[i:i + 1]['is_tcp'].tolist()[0]])
    # l.append(data[i:i+1]['client_bytes'].tolist()[0])
    # l.append(data[i:i+1]['server_bytes'].tolist()[0])
    # l.append(data[i:i+1]['client_payload'].tolist()[0])
    # l.append(data[i:i+1]['is_tcp'].tolist()[0])
print(list_final)