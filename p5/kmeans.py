import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('data.txt')

X = data[["INCOME","SPEND"]]

#number of clusters
K=4
centroids = (X.sample(n=K))
diff = 1
j=0

while diff!=0:
    XD=X
    i=1
    for index1,row_c in centroids.iterrows():
        ED=[]
        for index2,row_d in XD.iterrows():
            d1=(row_c["SPEND"]-row_d["SPEND"])**2
            d2=(row_c["INCOME"]-row_d["INCOME"])**2
            d=np.sqrt(d1+d2)
            ED.append(d)
        X[i]=ED
        i=i+1
    C=[]
    for index,row in X.iterrows():
        min_dist=row[1]
        pos=1
        for i in range(K):
            if row[i+1] < min_dist:
                min_dist = row[i+1]
                pos=i+1
        C.append(pos)
    X["Cluster"]=C
    Centroids_new = X.groupby(["Cluster"]).mean()[["INCOME","SPEND"]]
    if j == 0:
        diff=1
        j=j+1
    else:
        diff = (Centroids_new['INCOME'] - centroids['INCOME']).sum() + (Centroids_new['SPEND'] - centroids['SPEND']).sum()
        print(diff.sum())
    centroids = X.groupby(["Cluster"]).mean()[["INCOME", "SPEND"]]

color=['blue','green','cyan','red']
for k in range(K):
    data=X[X["Cluster"]==k+1]
    plt.scatter(data["SPEND"],data["INCOME"],c=color[k])

# this plot the centroids
# plt.scatter(centroids["SPEND"], centroids["INCOME"], c='black')

plt.xlabel('Spend')
plt.ylabel('Income')
plt.show()