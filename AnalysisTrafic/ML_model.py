import pandas as pd
import numpy as np
from sklearn.utils import shuffle
import os
from matplotlib import pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report
import pickle
def get_data():
    data = pd.read_csv('./media/' + os.listdir("./media")[0])
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

    with open('/home/stas/PycharmProjects/pythonProject/TLS/AnalysisTrafic/ML_model/ML_get_data.pkl', 'rb') as f:
        model = pickle.load(f)
    list_final = []
    for i in range(1, len(X_test)):
        a = labeler.inverse_transform(model.predict(X_test[i:i + 1]))
        list_final.append([data[i:i + 1]['proto'].tolist()[0], data[i:i + 1]['client_bytes'].tolist()[0],
                           data[i:i + 1]['server_bytes'].tolist()[0], data[i:i + 1]['client_payload'].tolist()[0],
                           data[i:i + 1]['is_tcp'].tolist()[0]])
    l = []
    n = []
    for proto in train_data["proto"].unique():
        l.append(len(train_data[train_data["proto"] == proto]))
        n.append(proto.ljust(20).replace(' ', ''))
    explode = (0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01)
    colors = sns.color_palette("crest")
    fig = plt.figure(figsize=(10, 10))
    patches, texts = plt.pie(l, colors=colors, explode=explode)
    plt.legend(patches, labels=n, loc="best")
    plt.savefig('/home/stas/PycharmProjects/pythonProject/TLS/TLS/static/AnalysisTrafic/images/circle.png')

    l = train_data['client_packets'].sum()
    n = train_data['server_packets'].sum()

    data = [l, n]
    names = ['Пакеты со стороны клиента', 'Пакеты со стороны сервера']

    plt.figure()

    xvals = names
    yvals = data
    colors = sns.color_palette("crest")
    position = np.arange(len(xvals))
    mybars = plt.bar(position, yvals, align='center', linewidth=0, color=colors)
    plt.xticks(position, xvals)

    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')

    for bari in mybars:
        height = bari.get_height()
        plt.gca().text(bari.get_x() + bari.get_width() / 2, bari.get_height() - 0.2, str(int(height)),
                       ha='center', color='black', fontsize=11)
    plt.savefig('/home/stas/PycharmProjects/pythonProject/TLS/TLS/static/AnalysisTrafic/images/column.png')

    return list_final