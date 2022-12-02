# Importation des packages
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Importation des données
DTrain = pd.read_csv("all_e.csv", delimiter=",", na_filter = False)
DTrain = DTrain.drop(DTrain.columns[0], axis = 1)
DTrainWithoutPrice = DTrain.drop(columns = ['price'])
DTrainWithoutPrice.drop(list(DTrainWithoutPrice.filter(regex = 'model')), axis = 1, inplace = True)
DTrainWithoutPrice.drop(list(DTrainWithoutPrice.filter(regex = 'brand')), axis = 1, inplace = True) 

X = DTrainWithoutPrice[0:15000]
Y = DTrain.price[0:15000]

DTrainWithoutPrice.head()
Y.head()

model_tree = DecisionTreeRegressor(criterion='mae', max_depth=8, max_leaf_nodes=80, min_samples_leaf=100)

model_tree.fit(X, Y)

# Affichage de l'arbre dans un graphique
plt.figure(figsize=(80,80)) # Permet de faire un super grand affichage comme ça on peut zoomer dessus
tree.plot_tree(model_tree,feature_names=list(X.columns))
plt.show

# Affichage de l'arbre sous forme textuelle
from sklearn.tree import export_text
print(export_text(model_tree, feature_names=list(X.columns)))
