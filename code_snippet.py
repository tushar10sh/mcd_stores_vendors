#code snippets for abhishek

import googlemaps
from datetime import datetime
import pandas as pdb
import numpy as np
import json

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()
import csv

full_store_data = pd.read_excel("/home/tushar/Downloads/ALL_Store_Address.xlsx")
full_store_data['Full_Address'] = full_store_data['Address'] + ", " + full_store_data['City'] + ", " + full_store_data['State'] + ", India"
maps = googlemaps.Client(key='AIzaSyCBL_aZWLXwiSsHxYD2dftcRrxt3wzvKGI')

for i in range(len(full_store_data['Full_Address'])):
    res = maps.geocode(full_store_data['Full_Address'][i])
     full_store_data['Latitude'][i] = res[0]['geometry']['location']['lat']
     full_store_data['Longitude'][i] = res[0]['geometry']['location']['lng']


full_store_data.to_excel('/home/tushar/Downloads/ALL_Store_Address_withLatLon.xlsx')
features = { 'type': 'FeatureCollection', 'features': [] }


for i in range(len(full_store_data['Full_Address'])):
     features['features'].append( { 'geometry': { "type": "Point", "coordinates": [ full_store_data['Longitude'][i], full_store_data['Latitude'][i] ] }, "type": "Feature", "properties": { "popupContent": "<p> <strong>Address</strong> " + full_store_data['Full_Address'][i] +  "<br/>  <strong> Idx: </strong>" + str(i) + "  <br/> <strong> Demand: </strong> " + str(full_store_data['Demand'][i] ) + "</p>", "demand": full_store_data['Demand'][i], "cluster_label": full_store_data['Cluster'][i] }, "id": i } )


with open("/home/tushar/Downloads/All_store_features.geojson", "w") as f:
    json.dump(features, f)


X=full_store_data.loc[:,['Full_Address','Latitude','Longitude']]
Y_axis = full_store_data[['Latitude']]
X_axis = full_store_data[['Longitude']]
K_clusters = range(1,10)
kmeans = [KMeans(n_clusters=i) for i in K_clusters]
score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]

plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.plot(K_clusters, score)

kmeans = KMeans(n_clusters = 6, init ='k-means++')
kmeans.fit(X[X.columns[1:3]]) # Compute k-means clustering.
X['cluster_label'] = kmeans.fit_predict(X[X.columns[1:3]])
centers = kmeans.cluster_centers_ # Coordinates of cluster centers.
labels = kmeans.predict(X[X.columns[1:3]]) # Labels of each point
print(centers)
