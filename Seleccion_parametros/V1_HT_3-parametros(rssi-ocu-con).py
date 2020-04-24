#!/usr/bin/env python
# coding: utf-8

# # Hoeffding Tree or Very Fast Decision Tree
# 
# https://scikit-multiflow.github.io/scikit-multiflow/index.html
# 
# https://scikit-multiflow.github.io/scikit-multiflow/_autosummary/skmultiflow.trees.HoeffdingTree.html#skmultiflow.trees.HoeffdingTree

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')
get_ipython().run_line_magic('matplotlib', 'inline')
#from skmultiflow.meta import AdaptiveRandomForest

from skmultiflow.trees import HoeffdingTree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn import metrics
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd



X = pd.read_csv('dataset_seleccion_parametros.csv')
y = X['associatedTo']
X = X.drop('associatedTo', axis=1)
X = X.drop('station', axis=1)

X = X.drop('dis1', axis=1)
X = X.drop('dis2', axis=1)
X = X.drop('dis3', axis=1)
X = X.drop('dis4', axis=1)
X = X.drop('pow1', axis=1)
X = X.drop('pow2', axis=1)
X = X.drop('pow3', axis=1)
X = X.drop('pow4', axis=1)

X.head()


# In[2]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=1)

X_train, X_test, y_train, y_test = X_train.to_numpy(), X_test.to_numpy(), y_train.to_numpy(), y_test.to_numpy()

print(type(X_train))
#print(type(X_train.to_numpy()))


# ### Entrenar el clasificador (modelo)

# In[21]:


clasificador = HoeffdingTree()
print(clasificador.get_info())

print("start training")
clasificador.fit(X_train,y_train, classes=None, sample_weight=None)
print("end training")


# # Graficas Paper

# In[4]:


dataset = pd.read_csv('dataset_seleccion_parametros.csv')

dataset.shape


# In[5]:


dataset.head()


# In[6]:


#dataset = dataset.drop('associatedTo', axis=1)
dataset = dataset.drop('station', axis=1)
dataset = dataset.drop('dis1', axis=1)
dataset = dataset.drop('dis2', axis=1)
dataset = dataset.drop('dis3', axis=1)
dataset = dataset.drop('dis4', axis=1)
dataset = dataset.drop('pow1', axis=1)
dataset = dataset.drop('pow2', axis=1)
dataset = dataset.drop('pow3', axis=1)
dataset = dataset.drop('pow4', axis=1)
#X = X.drop('dist', axis=1)
dataset.head()


# In[7]:


dataset_copy = dataset


# In[8]:


clasificador_final = clasificador


# ### 50% del dataset

# In[9]:


dataset_copy50 = dataset_copy.sample(frac=0.5, random_state=1)

print(dataset_copy.shape)
print(dataset_copy50.shape)

X_50 = dataset_copy50.drop('associatedTo', axis=1)
y_50 = dataset_copy50['associatedTo']

print(X_50.shape)
print(y_50.shape)

X50_train, X50_test, y50_train, y50_test = train_test_split(X_50,y_50,test_size=0.2, random_state=1)

X50_train, X50_test, y50_train, y50_test = X50_train.to_numpy(), X50_test.to_numpy(), y50_train.to_numpy(), y50_test.to_numpy()

#X_train, X_test, y_train, y_test = X_train.to_numpy(), X_test.to_numpy(), y_train.to_numpy(), y_test.to_numpy()

print('X_train:',X50_train.shape)
print('X_test:',X50_test.shape)
print('y_train:',y50_train.shape)
print('y_test:',y50_test.shape)

#clasificador_final = RandomForestClassifier(n_estimators=26, max_depth=20, random_state=0, oob_score=True)

print("start training")
clasificador_final.fit(X50_train,y50_train)
print("end training")

print("start prediction")
predict50_final = clasificador_final.predict(X50_test)
print("end prediction")

"""
import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('ggplot')
plt.hist([predict50_final,y50_test])
plt.show()
"""

y50_pred = predict50_final

print('Score:', clasificador_final.score(X50_test, y50_test))
print('')  
print('Mean Absolute Error:', metrics.mean_absolute_error(y50_test, y50_pred))  
print('')  
print('Mean Squared Error:', metrics.mean_squared_error(y50_test, y50_pred))  
print('')  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y50_test, y50_pred))) 
print('')  
print('----Confusion_matrix----')
print(confusion_matrix(y50_test,y50_pred))  
print('')  

print('----Classification_report----')  
print(classification_report(y50_test,y50_pred)) 
print('')  

print('----Accuracy_score----')  
print(accuracy_score(y50_test, y50_pred))  


# In[ ]:





# ### 60%

# In[10]:


dataset_copy60 = dataset_copy.sample(frac=0.6, random_state=1)

print(dataset_copy.shape)
print(dataset_copy60.shape)

X_60 = dataset_copy60.drop('associatedTo', axis=1)
y_60 = dataset_copy60['associatedTo']

print(X_60.shape)
print(y_60.shape)

X60_train, X60_test, y60_train, y60_test = train_test_split(X_60,y_60,test_size=0.2, random_state=1)

X60_train, X60_test, y60_train, y60_test = X60_train.to_numpy(), X60_test.to_numpy(), y60_train.to_numpy(), y60_test.to_numpy()

print('X_train:',X60_train.shape)
print('X_test:',X60_test.shape)
print('y_train:',y60_train.shape)
print('y_test:',y60_test.shape)

print("start training")
clasificador_final.fit(X60_train,y60_train)
print("end training")

print("start prediction")
predict60_final = clasificador_final.predict(X60_test)
print("end prediction")



"""
import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('ggplot')
plt.hist([predict60_final,y60_test])
plt.show()
"""

y60_pred = predict60_final

print('Score:', clasificador_final.score(X60_test, y60_test))
print('')  
print('Mean Absolute Error:', metrics.mean_absolute_error(y60_test, y60_pred))  
print('')  
print('Mean Squared Error:', metrics.mean_squared_error(y60_test, y60_pred))  
print('')  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y60_test, y60_pred))) 
print('')  
print('----Confusion_matrix----')
print(confusion_matrix(y60_test,y60_pred))  
print('')  

print('----Classification_report----')  
print(classification_report(y60_test,y60_pred)) 
print('')  

print('----Accuracy_score----')  
print(accuracy_score(y60_test, y60_pred)) 


# In[ ]:





# ### 70%

# In[11]:


dataset_copy70 = dataset_copy.sample(frac=0.7, random_state=1)

print(dataset_copy.shape)
print(dataset_copy70.shape)

X_70 = dataset_copy70.drop('associatedTo', axis=1)
y_70 = dataset_copy70['associatedTo']

print(X_70.shape)
print(y_70.shape)

X70_train, X70_test, y70_train, y70_test = train_test_split(X_70,y_70,test_size=0.8, random_state=1)
X70_train, X70_test, y70_train, y70_test = X70_train.to_numpy(), X70_test.to_numpy(), y70_train.to_numpy(), y70_test.to_numpy()


print('X_train:',X70_train.shape)
print('X_test:',X70_test.shape)
print('y_train:',y70_train.shape)
print('y_test:',y70_test.shape)


print("start training")
clasificador_final.fit(X70_train,y70_train)
print("end training")

print("start prediction")
predict70_final = clasificador_final.predict(X70_test)
print("end prediction")



"""
import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('ggplot')
plt.hist([predict70_final,y70_test])
plt.show()
"""

y70_pred = predict70_final

print('Score:', clasificador_final.score(X70_test, y70_test))
print('')  
print('Mean Absolute Error:', metrics.mean_absolute_error(y70_test, y70_pred))  
print('')  
print('Mean Squared Error:', metrics.mean_squared_error(y70_test, y70_pred))  
print('')  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y70_test, y70_pred))) 
print('')  
print('----Confusion_matrix----')
print(confusion_matrix(y70_test,y70_pred))  
print('')  

print('----Classification_report----')  
print(classification_report(y70_test,y70_pred)) 
print('')  

print('----Accuracy_score----')  
print(accuracy_score(y70_test, y70_pred)) 


# In[ ]:





# ### 80%

# In[12]:


dataset_copy80 = dataset_copy.sample(frac=0.8, random_state=1)

print(dataset_copy.shape)
print(dataset_copy80.shape)

X_80 = dataset_copy80.drop('associatedTo', axis=1)
y_80 = dataset_copy80['associatedTo']

print(X_80.shape)
print(y_80.shape)

X80_train, X80_test, y80_train, y80_test = train_test_split(X_80,y_80,test_size=0.8, random_state=1)
X80_train, X80_test, y80_train, y80_test = X80_train.to_numpy(), X80_test.to_numpy(), y80_train.to_numpy(), y80_test.to_numpy()

print('X_train:',X80_train.shape)
print('X_test:',X80_test.shape)
print('y_train:',y80_train.shape)
print('y_test:',y80_test.shape)


print("start training")
clasificador_final.fit(X80_train,y80_train)
print("end training")

print("start prediction")
predict80_final = clasificador_final.predict(X80_test)
print("end prediction")



"""
import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('ggplot')
plt.hist([predict80_final,y80_test])
plt.show()
"""

y80_pred = predict80_final

print('Score:', clasificador_final.score(X80_test, y80_test))
print('')  
print('Mean Absolute Error:', metrics.mean_absolute_error(y80_test, y80_pred))  
print('')  
print('Mean Squared Error:', metrics.mean_squared_error(y80_test, y80_pred))  
print('')  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y80_test, y80_pred))) 
print('')  
print('----Confusion_matrix----')
print(confusion_matrix(y80_test,y80_pred))  
print('')  

print('----Classification_report----')  
print(classification_report(y80_test,y80_pred)) 
print('')  

print('----Accuracy_score----')  
print(accuracy_score(y80_test, y80_pred)) 


# In[ ]:





# ### 90%

# In[13]:


dataset_copy90 = dataset_copy.sample(frac=0.9, random_state=1)

print(dataset_copy.shape)
print(dataset_copy90.shape)

X_90 = dataset_copy90.drop('associatedTo', axis=1)
y_90 = dataset_copy90['associatedTo']

print(X_90.shape)
print(y_90.shape)

X90_train, X90_test, y90_train, y90_test = train_test_split(X_90,y_90,test_size=0.8, random_state=1)
X90_train, X90_test, y90_train, y90_test = X90_train.to_numpy(), X90_test.to_numpy(), y90_train.to_numpy(), y90_test.to_numpy()

print('X_train:',X90_train.shape)
print('X_test:',X90_test.shape)
print('y_train:',y90_train.shape)
print('y_test:',y90_test.shape)

print("start training")
clasificador_final.fit(X90_train,y90_train)
print("end training")

print("start prediction")
predict90_final = clasificador_final.predict(X90_test)
print("end prediction")




"""
import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('ggplot')
plt.hist([predict90_final,y90_test])
plt.show()
"""

y90_pred = predict90_final

print('Score:', clasificador_final.score(X90_test, y90_test))
print('')  
print('Mean Absolute Error:', metrics.mean_absolute_error(y90_test, y90_pred))  
print('')  
print('Mean Squared Error:', metrics.mean_squared_error(y90_test, y90_pred))  
print('')  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y90_test, y90_pred))) 
print('')  
print('----Confusion_matrix----')
print(confusion_matrix(y90_test,y90_pred))  
print('')  

print('----Classification_report----')  
print(classification_report(y90_test,y90_pred)) 
print('')  

print('----Accuracy_score----')  
print(accuracy_score(y90_test, y90_pred)) 


# In[ ]:





# ### 100%

# In[14]:


dataset_copy100 = dataset_copy.sample(frac=1, random_state=1)

print(dataset_copy.shape)
print(dataset_copy100.shape)

X_100 = dataset_copy100.drop('associatedTo', axis=1)
y_100 = dataset_copy100['associatedTo']

print(X_100.shape)
print(y_100.shape)

X100_train, X100_test, y100_train, y100_test = train_test_split(X_100,y_100,test_size=0.8, random_state=1)
X100_train, X100_test, y100_train, y100_test = X100_train.to_numpy(), X100_test.to_numpy(), y100_train.to_numpy(), y100_test.to_numpy()

print('X_train:',X100_train.shape)
print('X_test:',X100_test.shape)
print('y_train:',y100_train.shape)
print('y_test:',y100_test.shape)


print("start training")
clasificador_final.fit(X100_train,y100_train)
print("end training")

print("start prediction")
predict100_final = clasificador_final.predict(X100_test)
print("end prediction")




"""
import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('ggplot')
plt.hist([predict100_final,y100_test])
plt.show()
"""

y100_pred = predict100_final

print('Score:', clasificador_final.score(X100_test, y100_test))
print('')  
print('Mean Absolute Error:', metrics.mean_absolute_error(y100_test, y100_pred))  
print('')  
print('Mean Squared Error:', metrics.mean_squared_error(y100_test, y100_pred))  
print('')  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y100_test, y100_pred))) 
print('')  
print('----Confusion_matrix----')
print(confusion_matrix(y100_test,y100_pred))  
print('')  

print('----Classification_report----')  
print(classification_report(y100_test,y100_pred)) 
print('')  

print('----Accuracy_score----')  
print(accuracy_score(y100_test, y100_pred)) 

print('score, Mean Absolute Error, Mean Squared Error, Root Mean Squared Error', 'Accuracy_score')
print(clasificador_final.score(X100_test, y100_test), 
      metrics.mean_absolute_error(y100_test, y100_pred),  
      metrics.mean_squared_error(y100_test, y100_pred), 
      np.sqrt(metrics.mean_squared_error(y100_test, y100_pred)), 
      accuracy_score(y100_test, y100_pred))


# In[ ]:





# ### Graficos y Datos

# In[15]:



print(clasificador_final.get_info())

print('size, score, Mean Absolute Error, Mean Squared Error, Root Mean Squared Error, Accuracy_score')
print("50%", clasificador_final.score(X50_test, y50_test), metrics.mean_absolute_error(y50_test, y50_pred),  metrics.mean_squared_error(y50_test, y50_pred), np.sqrt(metrics.mean_squared_error(y50_test, y50_pred)), accuracy_score(y50_test, y50_pred))
print("60%", clasificador_final.score(X60_test, y60_test), metrics.mean_absolute_error(y60_test, y60_pred),  metrics.mean_squared_error(y60_test, y60_pred), np.sqrt(metrics.mean_squared_error(y60_test, y60_pred)), accuracy_score(y60_test, y60_pred))
print("70%", clasificador_final.score(X70_test, y70_test), metrics.mean_absolute_error(y70_test, y70_pred),  metrics.mean_squared_error(y70_test, y70_pred), np.sqrt(metrics.mean_squared_error(y70_test, y70_pred)), accuracy_score(y70_test, y70_pred))
print("80%", clasificador_final.score(X80_test, y80_test), metrics.mean_absolute_error(y80_test, y80_pred),  metrics.mean_squared_error(y80_test, y80_pred), np.sqrt(metrics.mean_squared_error(y80_test, y80_pred)), accuracy_score(y80_test, y80_pred))
print("90%", clasificador_final.score(X90_test, y90_test), metrics.mean_absolute_error(y90_test, y90_pred),  metrics.mean_squared_error(y90_test, y90_pred), np.sqrt(metrics.mean_squared_error(y90_test, y90_pred)), accuracy_score(y90_test, y90_pred))
print("100%", clasificador_final.score(X100_test, y100_test), metrics.mean_absolute_error(y100_test, y100_pred),  metrics.mean_squared_error(y100_test, y100_pred), np.sqrt(metrics.mean_squared_error(y100_test, y100_pred)), accuracy_score(y100_test, y100_pred))


# In[ ]:





# ### confusion_matrix plots

# In[16]:


from sklearn.utils.multiclass import unique_labels
plt.rcParams['figure.figsize'] = (17,12)
plt.style.use('ggplot')
class_names = np.array(['AP1','AP2','AP3','AP4']) 

cmap=plt.cm.Blues
# Compute confusion matrix
cm_50 = confusion_matrix(y50_test, y50_pred)
cm_60 = confusion_matrix(y60_test, y60_pred)
cm_70 = confusion_matrix(y70_test, y70_pred)
cm_80 = confusion_matrix(y80_test, y80_pred)

cm_90 = confusion_matrix(y90_test, y90_pred)
cm_100 = confusion_matrix(y100_test, y100_pred)
# Only use the labels that appear in the data
print(cm_50)
print(cm_60)
print(cm_70)
print(cm_80)
print(cm_90)
print(cm_100)

f, ax = plt.subplots(2, 3)
ax1 = ax[0, 0]
ax2 = ax[0, 1]
ax3 = ax[0, 2]
ax4 = ax[1, 0]
ax5 = ax[1, 1]
ax6 = ax[1, 2]

im = ax1.imshow(cm_50, interpolation='nearest', cmap=cmap)
# We want to show all ticks...
ax1.set(xticks=np.arange(cm_50.shape[1]),
       yticks=np.arange(cm_50.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='50%',
       ylabel='True label',
       xlabel='Predicted label')

# Rotate the tick labels and set their alignment.
plt.setp(ax1.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_50.max() / 2.
for i in range(cm_50.shape[0]):
    for j in range(cm_50.shape[1]):
        ax1.text(j, i, format(cm_50[i, j], fmt),
                ha="center", va="center",
                color="white" if cm_50[i, j] > thresh else "black")
        
#------------------------
im = ax2.imshow(cm_60, interpolation='nearest', cmap=cmap)

# We want to show all ticks...
ax2.set(xticks=np.arange(cm_60.shape[1]),
       yticks=np.arange(cm_60.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='60%',
       ylabel='True label',
       xlabel='Predicted label')

# Rotate the tick labels and set their alignment.
plt.setp(ax2.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_60.max() / 2.
for i in range(cm_60.shape[0]):
    for j in range(cm_60.shape[1]):
        ax2.text(j, i, format(cm_60[i, j], fmt),
                ha="center", va="center",
                color="white" if cm_60[i, j] > thresh else "black")
#------------------------
im = ax3.imshow(cm_70, interpolation='nearest', cmap=cmap)

# We want to show all ticks...
ax3.set(xticks=np.arange(cm_70.shape[1]),
       yticks=np.arange(cm_70.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='70%',
       ylabel='True label',
       xlabel='Predicted label')

# Rotate the tick labels and set their alignment.
plt.setp(ax3.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_70.max() / 2.
for i in range(cm_70.shape[0]):
    for j in range(cm_70.shape[1]):
        ax3.text(j, i, format(cm_70[i, j], fmt),
                ha="center", va="center",
                color="white" if cm_70[i, j] > thresh else "black")

        
#------------------------
im = ax4.imshow(cm_80, interpolation='nearest', cmap=cmap)
# We want to show all ticks...
ax4.set(xticks=np.arange(cm_80.shape[1]),
       yticks=np.arange(cm_80.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='80%',
       ylabel='True label',
       xlabel='Predicted label')

# Rotate the tick labels and set their alignment.
plt.setp(ax4.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_80.max() / 2.
for i in range(cm_80.shape[0]):
    for j in range(cm_80.shape[1]):
        ax4.text(j, i, format(cm_80[i, j], fmt),
                ha="center", va="center",
                color="white" if cm_80[i, j] > thresh else "black")
#------------------------
im = ax5.imshow(cm_90, interpolation='nearest', cmap=cmap)
# We want to show all ticks...
ax5.set(xticks=np.arange(cm_90.shape[1]),
       yticks=np.arange(cm_90.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='90%',
       ylabel='True label',
       xlabel='Predicted label')

# Rotate the tick labels and set their alignment.
plt.setp(ax5.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_90.max() / 2.
for i in range(cm_90.shape[0]):
    for j in range(cm_90.shape[1]):
        ax5.text(j, i, format(cm_90[i, j], fmt),
                ha="center", va="center",
                color="white" if cm_90[i, j] > thresh else "black")

#------------------------
im = ax6.imshow(cm_100, interpolation='nearest', cmap=cmap)
# We want to show all ticks...
ax6.set(xticks=np.arange(cm_100.shape[1]),
       yticks=np.arange(cm_100.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='100%',
       ylabel='True label',
       xlabel='Predicted label')

# Rotate the tick labels and set their alignment.
plt.setp(ax6.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_100.max() / 2.
for i in range(cm_100.shape[0]):
    for j in range(cm_100.shape[1]):
        ax6.text(j, i, format(cm_100[i, j], fmt),
                ha="center", va="center",
                color="white" if cm_100[i, j] > thresh else "black")
        
f.tight_layout()


# In[ ]:





# ### confusion_matrix 70, 80, 90, 100 % del dataset

# In[17]:


from sklearn.utils.multiclass import unique_labels
plt.rcParams['figure.figsize'] = (16,14)
#plt.rcParams['figure.figsize'] = (26,24)
plt.style.use('ggplot')
class_names = np.array(['AP1','AP2','AP3','AP4']) 

cmap=plt.cm.Blues
# Compute confusion matrix
cm_50 = confusion_matrix(y50_test, y50_pred)
cm_60 = confusion_matrix(y60_test, y60_pred)
cm_70 = confusion_matrix(y70_test, y70_pred)
cm_80 = confusion_matrix(y80_test, y80_pred)

cm_90 = confusion_matrix(y90_test, y90_pred)
cm_100 = confusion_matrix(y100_test, y100_pred)
# Only use the labels that appear in the data

print(cm_70)
print(cm_80)
print(cm_90)
print(cm_100)

f, ax = plt.subplots(2, 2)
ax3 = ax[0, 0]
ax4 = ax[0, 1]
ax5 = ax[1, 0]
ax6 = ax[1, 1]


#im = ax1.imshow(cm, interpolation='nearest', cmap=cmap)
#ax1.figure.colorbar(im, ax=ax)
    
#------------------------
im = ax3.imshow(cm_70, interpolation='nearest', cmap=cmap)

# We want to show all ticks...
ax3.set(xticks=np.arange(cm_70.shape[1]),
       yticks=np.arange(cm_70.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='70%',
       ylabel='True label',
       xlabel='Predicted label')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Rotate the tick labels and set their alignment.
plt.setp(ax3.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_70.max() / 2.
for i in range(cm_70.shape[0]):
    for j in range(cm_70.shape[1]):
        ax3.text(j, i, format(cm_70[i, j], fmt),
                ha="center", va="center",fontsize=12,
                color="white" if cm_70[i, j] > thresh else "black")

        
#------------------------
im = ax4.imshow(cm_80, interpolation='nearest', cmap=cmap)
# We want to show all ticks...
ax4.set(xticks=np.arange(cm_80.shape[1]),
       yticks=np.arange(cm_80.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='80%',
       ylabel=('True label'),
       xlabel='Predicted label')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Rotate the tick labels and set their alignment.
plt.setp(ax4.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_80.max() / 2.
for i in range(cm_80.shape[0]):
    for j in range(cm_80.shape[1]):
        ax4.text(j, i, format(cm_80[i, j], fmt),
                ha="center", va="center",fontsize=12,
                color="white" if cm_80[i, j] > thresh else "black")
#------------------------
im = ax5.imshow(cm_90, interpolation='nearest', cmap=cmap)
# We want to show all ticks...
ax5.set(xticks=np.arange(cm_90.shape[1]),
       yticks=np.arange(cm_90.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='90%',
       ylabel='True label',
       xlabel='Predicted label')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Rotate the tick labels and set their alignment.
plt.setp(ax5.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_90.max() / 2.
for i in range(cm_90.shape[0]):
    for j in range(cm_90.shape[1]):
        ax5.text(j, i, format(cm_90[i, j], fmt),
                ha="center", va="center",fontsize=12,
                color="white" if cm_90[i, j] > thresh else "black")

#------------------------
#------------------------
im = ax6.imshow(cm_100[1:, 1:], interpolation='nearest', cmap=cmap)
# We want to show all ticks...
ax6.set(xticks=np.arange(cm_100.shape[1]-1),
       yticks=np.arange(cm_100.shape[0]-1),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='100%',
       ylabel='True label',
       xlabel='Predicted label')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Rotate the tick labels and set their alignment.
plt.setp(ax6.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
#ax6.xaxis.label.set_color('red')
#ax6.tick_params(axis='x', colors='red')


# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_100.max() / 2.
for i in range(cm_100.shape[0]-1):
    for j in range(cm_100.shape[1]-1):
        ax6.text(j, i, format(cm_100[i+1, j+1], fmt),
                ha="center", va="center",fontsize=12,
                color="white" if cm_100[i+1, j+1] > thresh else "black")

plt.suptitle('HT', x = 0.5, y = 1.1, fontsize=18)   
f.tight_layout()


# In[ ]:





# In[18]:


from sklearn.utils.multiclass import unique_labels
plt.rcParams['figure.figsize'] = (16,14)
#plt.rcParams['figure.figsize'] = (26,24)
plt.style.use('ggplot')
class_names = np.array(['AP1','AP2','AP3','AP4']) 

cmap=plt.cm.Greys
# Compute confusion matrix
cm_50 = confusion_matrix(y50_test, y50_pred)
cm_60 = confusion_matrix(y60_test, y60_pred)
cm_70 = confusion_matrix(y70_test, y70_pred)
cm_80 = confusion_matrix(y80_test, y80_pred)

cm_90 = confusion_matrix(y90_test, y90_pred)
cm_100 = confusion_matrix(y100_test, y100_pred)
# Only use the labels that appear in the data

print(cm_70)
print(cm_80)
print(cm_90)
print(cm_100)

f, ax = plt.subplots(2, 2)
ax3 = ax[0, 0]
ax4 = ax[0, 1]
ax5 = ax[1, 0]
ax6 = ax[1, 1]


#im = ax1.imshow(cm, interpolation='nearest', cmap=cmap)
#ax1.figure.colorbar(im, ax=ax)
    
#------------------------
im = ax3.imshow(cm_70, interpolation='nearest', cmap=cmap)

# We want to show all ticks...
ax3.set(xticks=np.arange(cm_70.shape[1]),
       yticks=np.arange(cm_70.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='70%',
       ylabel='True label',
       xlabel='Predicted label')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Rotate the tick labels and set their alignment.
plt.setp(ax3.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
ax3.grid(True, color='0.9')
ax3.spines['bottom'].set_color('0.8')
ax3.spines['top'].set_color('0.8')
ax3.spines['left'].set_color('0.8')
ax3.spines['right'].set_color('0.8')
# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_70.max() / 2.
for i in range(cm_70.shape[0]):
    for j in range(cm_70.shape[1]):
        ax3.text(j, i, format(cm_70[i, j], fmt),
                ha="center", va="center",fontsize=12,
                color="white" if cm_70[i, j] > thresh else "black")
        


        
#------------------------
im = ax4.imshow(cm_80, interpolation='nearest', cmap=cmap)
# We want to show all ticks...
ax4.set(xticks=np.arange(cm_80.shape[1]),
       yticks=np.arange(cm_80.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='80%',
       ylabel=('True label'),
       xlabel='Predicted label')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Rotate the tick labels and set their alignment.
plt.setp(ax4.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

ax4.grid(True, color='0.9')
ax4.spines['bottom'].set_color('0.8')
ax4.spines['top'].set_color('0.8')
ax4.spines['left'].set_color('0.8')
ax4.spines['right'].set_color('0.8')

# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_80.max() / 2.
for i in range(cm_80.shape[0]):
    for j in range(cm_80.shape[1]):
        ax4.text(j, i, format(cm_80[i, j], fmt),
                ha="center", va="center",fontsize=12,
                color="white" if cm_80[i, j] > thresh else "black")


#------------------------
im = ax5.imshow(cm_90, interpolation='nearest', cmap=cmap)
# We want to show all ticks...
ax5.set(xticks=np.arange(cm_90.shape[1]),
       yticks=np.arange(cm_90.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='90%',
       ylabel='True label',
       xlabel='Predicted label')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Rotate the tick labels and set their alignment.
plt.setp(ax5.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
ax5.grid(True, color='0.9')
ax5.spines['bottom'].set_color('0.8')
ax5.spines['top'].set_color('0.8')
ax5.spines['left'].set_color('0.8')
ax5.spines['right'].set_color('0.8')
# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_90.max() / 2.
for i in range(cm_90.shape[0]):
    for j in range(cm_90.shape[1]):
        ax5.text(j, i, format(cm_90[i, j], fmt),
                ha="center", va="center",fontsize=12,
                color="white" if cm_90[i, j] > thresh else "black")
        


#------------------------
#------------------------
im = ax6.imshow(cm_100[1:, 1:], interpolation='nearest', cmap=cmap)
# We want to show all ticks...
ax6.set(xticks=np.arange(cm_100.shape[1]-1),
       yticks=np.arange(cm_100.shape[0]-1),
       # ... and label them with the respective list entries
       xticklabels=class_names, yticklabels=class_names,
       title='100%',
       ylabel='True label',
       xlabel='Predicted label')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Rotate the tick labels and set their alignment.
plt.setp(ax6.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
ax6.grid(True, color='0.9')
ax6.spines['bottom'].set_color('0.8')
ax6.spines['top'].set_color('0.8')
ax6.spines['left'].set_color('0.8')
ax6.spines['right'].set_color('0.8')
#ax6.xaxis.label.set_color('red')
#ax6.tick_params(axis='x', colors='red')


# Loop over data dimensions and create text annotations.
fmt = 'd'
thresh = cm_100.max() / 2.
for i in range(cm_100.shape[0]-1):
    for j in range(cm_100.shape[1]-1):
        ax6.text(j, i, format(cm_100[i+1, j+1], fmt),
                ha="center", va="center",fontsize=12,
                color="white" if cm_100[i+1, j+1] > thresh else "black")

plt.suptitle('HT', x = 0.5, y = 1.1, fontsize=18)
f.tight_layout()


# In[ ]:





# ### Compute the Matthews correlation coefficient (MCC)
# 
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.matthews_corrcoef.html

# In[20]:


from sklearn.metrics import matthews_corrcoef

mcc_70 = matthews_corrcoef(y70_test, y70_pred)
mcc_80 = matthews_corrcoef(y80_test, y80_pred)
mcc_90 = matthews_corrcoef(y90_test, y90_pred)
mcc_100 = matthews_corrcoef(y100_test, y100_pred)

print(mcc_70, mcc_80, mcc_90, mcc_100)

