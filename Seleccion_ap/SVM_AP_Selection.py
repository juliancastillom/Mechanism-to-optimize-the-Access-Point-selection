#!/usr/bin/env python
# coding: utf-8

# # PROYECTO AP_Selection SVM

# ## Se usa algoritmo de Clasificación SVMs (Support vector machines) 
# 
# Son un conjunto de métodos de aprendizaje supervisado que se utilizan para la clasificación, regresión y detección de valores atípicos. (https://scikit-learn.org/stable/modules/svm.html)

# In[1]:


import numpy as np
import pandas as pd


# # Cargar dataset y limpiar datos

# In[3]:


X = pd.read_csv('dataset_seleccion_ap.csv')


# In[4]:


X.shape


# In[5]:


X.head()


# In[6]:


#available = ((X !=0) & (X.notnull()))
available = ((X.notnull()))


# In[7]:


available.apply(pd.Series.value_counts)


# In[8]:


available.all(axis=1).value_counts()


# In[9]:


mask = available['associatedTo']


# In[10]:


X = X[mask]


# In[11]:


X.shape


# In[12]:


y = X['associatedTo']


# In[13]:


X = X.drop('associatedTo', axis=1)
X = X.drop('station', axis=1)
#X = X.drop('dist', axis=1)
X.head()


# In[14]:


from sklearn.model_selection import train_test_split


# In[15]:


#X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=10000)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=1)


# In[16]:



#from sklearn.preprocessing import StandardScaler
#sc = StandardScaler()
#X_train = sc.fit_transform(X_train)
#X_test = sc.transform(X_test)


# In[17]:


print(len(X))
print(len(X_train))
print(len(X_test))
print(len(y))
print(len(y_train))
print(len(y_test))


# In[18]:


from sklearn import svm
clasificador = svm.SVC(kernel='rbf', C=1, gamma=1, coef0=10.0)


# In[19]:


clasificador


# In[20]:


clasificador.fit(X_train,y_train)


# In[21]:


predict = clasificador.predict(X_test)


# In[22]:


predict.shape


# In[23]:


y_test.shape


# In[24]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('ggplot')
plt.hist([predict,y_test])


# In[25]:


clasificador.score(X_test, y_test)


# # Clasificador basico

# In[26]:


#clasificador = svm.SVC(kernel='rbf', C=1, gamma=1)
#clasificador = svm.SVC()
#clasificador = svm.SVC(kernel='rbf', C=1, gamma=1, coef0=10.0)
#clasificador = svm.SVC(kernel='linear', C = 1.0)
#clasificador = svm.SVC(gamma=0.001, C=100)
#clasificador = svm.SVC(kernel='poly', degree=3)
#clasificador = svm.SVC(kernel='poly', degree = 2, C = 1.0, coef0 = 1)
clasificador_svm = svm.SVC(kernel='rbf', C=1, gamma=1, coef0=10.0)


# In[27]:


clasificador_svm.fit(X_train,y_train)

predict = clasificador_svm.predict(X_test)
print("\nScore: " + str(clasificador.score(X_test, y_test)))
#print(clasificador.feature_importances_)


# In[28]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('ggplot')
plt.hist([predict,y_test])


# # Grafico de ajuste SVM

# In[29]:


# Grafico de ajuste del árbol de decisión
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = (16,9)
train_prec =  []
eval_prec = []
max_deep_list = list(range(1, 200, 5))
kernel_list=['rbf', 'linear', 'poly']

for k in kernel_list:
    print(k)
    clasificador_svm = svm.SVC(kernel=k, C=1, gamma=1, coef0=10.0)
    #DecisionTreeClassifier(criterion='entropy', max_depth=deep)
    clasificador_svm.fit(X_train, y_train)
    train_prec.append(clasificador_svm.score(X_train, y_train))
    eval_prec.append(clasificador_svm.score(X_test, y_test))


# In[30]:


print(train_prec)
print(eval_prec)


# In[31]:


plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('ggplot')
plt.plot(kernel_list,train_prec, color='r', label='entrenamiento')
plt.plot(kernel_list,eval_prec, color='b', label='evaluacion')
plt.title('Grafico de ajuste arbol de decision')
plt.legend()
plt.ylabel('precision')
plt.xlabel('Kernel')
plt.show()


# # Clasificador según los mejores parámetros

# In[32]:


clasificador_final = svm.SVC(kernel='rbf', C=1, gamma=1, coef0=10.0)

clasificador_final.fit(X_train,y_train)

predict_final = clasificador_final.predict(X_test)

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = (16,9)
plt.style.use('ggplot')
plt.hist([predict_final,y_test])
plt.show()


print(clasificador_final.score(X_test, y_test))


# In[ ]:





# # Ejemplo Curvas de aprendizaje
# 
# ### responde que tanto mejora el algoritmo al introducir mas datos

# In[33]:


# Ejemplo Curvas de aprendizaje
#from sklearn.learning_curve import learning_curve
from sklearn.model_selection import learning_curve

arbol2 = clasificador_final

train_sizes, train_scores, test_scores = learning_curve(estimator=arbol2,
                        X=X_train, y=y_train, 
                        train_sizes=np.linspace(0.1, 1.0, 10), cv=10,
                        n_jobs=-1)

train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)


# In[34]:


# graficando las curvas
plt.plot(train_sizes, train_mean, color='r', marker='o', markersize=5,
         label='entrenamiento')
plt.fill_between(train_sizes, train_mean + train_std, 
                 train_mean - train_std, alpha=0.15, color='r')
plt.plot(train_sizes, test_mean, color='b', linestyle='--', 
         marker='s', markersize=5, label='evaluacion')
plt.fill_between(train_sizes, test_mean + test_std, 
                 test_mean - test_std, alpha=0.15, color='b')
plt.grid()
plt.title('Curva de aprendizaje')
plt.legend(loc='upper right')
plt.xlabel('Cant de ejemplos de entrenamiento')
plt.ylabel('Precision')
plt.show()


# # Metodos de evaluacion del modelo

# In[35]:


y_pred = predict_final


# In[36]:


#Saber que tan bueno es el metodo
# error cuadratico medio
# entre mas bajo es el valor es mejor el modelo
from sklearn.metrics import mean_squared_error
mean_squared_error(y_test, y_pred)


# In[37]:


#Matriz de confusion
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm


# In[38]:


#precision: cuenta cuantos salen buenos y cuantos salen malos
from sklearn.metrics import precision_score
precision_score(y_test, y_pred, average='macro')


# In[39]:


precision_score(y_test, y_pred, average='micro')


# In[40]:


#-----
clasificador_final.score(X_test, y_test)


# In[41]:


from sklearn import metrics

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))  


# In[42]:


from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(y_test,y_pred))  
print(classification_report(y_test,y_pred))  
print(accuracy_score(y_test, y_pred))  


# In[43]:


# hay que tener en cuenta precision y recall para elegir el algoritmo/modelo
X.head()


# In[ ]:





# ### Curva ROC
# 

# In[44]:


#https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
#http://www.hrc.es/bioest/roc_1.html

from sklearn.metrics import roc_curve, auc
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import label_binarize
#from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt

y_train_3 = label_binarize(y_train, classes=[1,2,3,4])
y_test_3 = label_binarize(y_test, classes=[1,2,3,4])
#X_train_3 = label_binarize(X_train, classes=[1,2,3,4])
#X_test_3 = label_binarize(X_test, classes=[1,2,3,4])
n_classes = 4

# shuffle and split training and test sets
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

# classifier
#clf = OneVsRestClassifier(LinearSVC(random_state=0))
#y_score = clf.fit(X_train, y_train).decision_function(X_test)

y_score_3 = clasificador_final.fit(X_train, y_train).decision_function(X_test)

#y_score_3 = clasificador_final.fit(X_train, y_train)
#y_score_3 = clasificador_final.predict_proba(X_test)

# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test_3[:, i], y_score_3[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
    #print fpr[i]
    #print tpr[i]
    #print("-----------------------------------")


# In[45]:


# Plot of a ROC curve for a specific class

plt.figure()
for i in range(n_classes):
    plt.plot(fpr[i], tpr[i], label='ROC curve - AP %s, (area = %0.2f)' %(i+1, roc_auc[i]))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([-0.01, 1.01])
    plt.ylim([-0.01, 1.04])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve AP')
    plt.legend(loc="lower right")
plt.show()


# In[46]:


fpr


# ###  ESTADISTICAS Y GRAFICAS PAPER

# In[47]:


dataset = pd.read_csv('dataset_seleccion_ap.csv')
dataset.shape


# In[48]:


#dataset = dataset.drop('associatedTo', axis=1)
dataset = dataset.drop('station', axis=1)
#X = X.drop('dist', axis=1)
dataset.head()


# In[49]:


dataset_copy = dataset
clasificador_final = svm.SVC(kernel='rbf', C=1, gamma=1, coef0=10.0)


# ### 50% del dataset

# In[50]:


dataset_copy50 = dataset_copy.sample(frac=0.5, random_state=1)

print(dataset_copy.shape)
print(dataset_copy50.shape)

X_50 = dataset_copy50.drop('associatedTo', axis=1)
y_50 = dataset_copy50['associatedTo']

print(X_50.shape)
print(y_50.shape)

X50_train, X50_test, y50_train, y50_test = train_test_split(X_50,y_50,test_size=0.2, random_state=1)

print('X_train:',X50_train.shape)
print('X_test:',X50_test.shape)
print('y_train:',y50_train.shape)
print('y_test:',y50_test.shape)

#clasificador_final = svm.SVC(kernel='rbf', C=1, gamma=1, coef0=10.0)

#clasificador_final = RandomForestClassifier(n_estimators=26, max_depth=20, random_state=0, oob_score=True)

clasificador_final.fit(X50_train,y50_train)

predict50_final = clasificador_final.predict(X50_test)

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


# ### 60%

# In[51]:


dataset_copy60 = dataset_copy.sample(frac=0.6, random_state=1)

print(dataset_copy.shape)
print(dataset_copy60.shape)

X_60 = dataset_copy60.drop('associatedTo', axis=1)
y_60 = dataset_copy60['associatedTo']

print(X_60.shape)
print(y_60.shape)

X60_train, X60_test, y60_train, y60_test = train_test_split(X_60,y_60,test_size=0.2, random_state=1)

print('X_train:',X60_train.shape)
print('X_test:',X60_test.shape)
print('y_train:',y60_train.shape)
print('y_test:',y60_test.shape)

#clasificador_final = RandomForestClassifier(n_estimators=26, max_depth=20, random_state=0, oob_score=True)

clasificador_final.fit(X60_train,y60_train)

predict60_final = clasificador_final.predict(X60_test)

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


# ### 70%

# In[52]:


dataset_copy70 = dataset_copy.sample(frac=0.7, random_state=1)

print(dataset_copy.shape)
print(dataset_copy70.shape)

X_70 = dataset_copy70.drop('associatedTo', axis=1)
y_70 = dataset_copy70['associatedTo']

print(X_70.shape)
print(y_70.shape)

X70_train, X70_test, y70_train, y70_test = train_test_split(X_70,y_70,test_size=0.8, random_state=1)

print('X_train:',X70_train.shape)
print('X_test:',X70_test.shape)
print('y_train:',y70_train.shape)
print('y_test:',y70_test.shape)

#clasificador_final = RandomForestClassifier(n_estimators=26, max_depth=20, random_state=0, oob_score=True)

clasificador_final.fit(X70_train,y70_train)

predict70_final = clasificador_final.predict(X70_test)

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


# ### 80%

# In[53]:


dataset_copy80 = dataset_copy.sample(frac=0.8, random_state=1)

print(dataset_copy.shape)
print(dataset_copy80.shape)

X_80 = dataset_copy80.drop('associatedTo', axis=1)
y_80 = dataset_copy80['associatedTo']

print(X_80.shape)
print(y_80.shape)

X80_train, X80_test, y80_train, y80_test = train_test_split(X_80,y_80,test_size=0.8, random_state=1)

print('X_train:',X80_train.shape)
print('X_test:',X80_test.shape)
print('y_train:',y80_train.shape)
print('y_test:',y80_test.shape)

#clasificador_final = RandomForestClassifier(n_estimators=26, max_depth=20, random_state=0, oob_score=True)

clasificador_final.fit(X80_train,y80_train)

predict80_final = clasificador_final.predict(X80_test)

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


# ### 90%

# In[54]:


dataset_copy90 = dataset_copy.sample(frac=0.9, random_state=1)

print(dataset_copy.shape)
print(dataset_copy90.shape)

X_90 = dataset_copy90.drop('associatedTo', axis=1)
y_90 = dataset_copy90['associatedTo']

print(X_90.shape)
print(y_90.shape)

X90_train, X90_test, y90_train, y90_test = train_test_split(X_90,y_90,test_size=0.8, random_state=1)

print('X_train:',X90_train.shape)
print('X_test:',X90_test.shape)
print('y_train:',y90_train.shape)
print('y_test:',y90_test.shape)

#clasificador_final = RandomForestClassifier(n_estimators=26, max_depth=20, random_state=0, oob_score=True)

clasificador_final.fit(X90_train,y90_train)

predict90_final = clasificador_final.predict(X90_test)

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


# ### 100%

# In[55]:


dataset_copy100 = dataset_copy.sample(frac=1, random_state=1)

print(dataset_copy.shape)
print(dataset_copy100.shape)

X_100 = dataset_copy100.drop('associatedTo', axis=1)
y_100 = dataset_copy100['associatedTo']

print(X_100.shape)
print(y_100.shape)

X100_train, X100_test, y100_train, y100_test = train_test_split(X_100,y_100,test_size=0.8, random_state=1)

print('X_train:',X100_train.shape)
print('X_test:',X100_test.shape)
print('y_train:',y100_train.shape)
print('y_test:',y100_test.shape)

#clasificador_final = RandomForestClassifier(n_estimators=26, max_depth=20, random_state=0, oob_score=True)

clasificador_final.fit(X100_train,y100_train)

predict100_final = clasificador_final.predict(X100_test)

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


# ### Graficos y Datos

# In[56]:



print('size, score, Mean Absolute Error, Mean Squared Error, Root Mean Squared Error, Accuracy_score')
print("50%", clasificador_final.score(X50_test, y50_test), metrics.mean_absolute_error(y50_test, y50_pred),  metrics.mean_squared_error(y50_test, y50_pred), np.sqrt(metrics.mean_squared_error(y50_test, y50_pred)), accuracy_score(y50_test, y50_pred))
print("60%", clasificador_final.score(X60_test, y60_test), metrics.mean_absolute_error(y60_test, y60_pred),  metrics.mean_squared_error(y60_test, y60_pred), np.sqrt(metrics.mean_squared_error(y60_test, y60_pred)), accuracy_score(y60_test, y60_pred))
print("70%", clasificador_final.score(X70_test, y70_test), metrics.mean_absolute_error(y70_test, y70_pred),  metrics.mean_squared_error(y70_test, y70_pred), np.sqrt(metrics.mean_squared_error(y70_test, y70_pred)), accuracy_score(y70_test, y70_pred))
print("80%", clasificador_final.score(X80_test, y80_test), metrics.mean_absolute_error(y80_test, y80_pred),  metrics.mean_squared_error(y80_test, y80_pred), np.sqrt(metrics.mean_squared_error(y80_test, y80_pred)), accuracy_score(y80_test, y80_pred))
print("90%", clasificador_final.score(X90_test, y90_test), metrics.mean_absolute_error(y90_test, y90_pred),  metrics.mean_squared_error(y90_test, y90_pred), np.sqrt(metrics.mean_squared_error(y90_test, y90_pred)), accuracy_score(y90_test, y90_pred))
print("100%", clasificador_final.score(X100_test, y100_test), metrics.mean_absolute_error(y100_test, y100_pred),  metrics.mean_squared_error(y100_test, y100_pred), np.sqrt(metrics.mean_squared_error(y100_test, y100_pred)), accuracy_score(y100_test, y100_pred))


# In[ ]:





# ### confusion_matrix plots

# In[57]:


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

fig, ax = plt.subplots(2, 3)
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
        
fig.tight_layout()


# In[ ]:





# ### confusion_matrix 70, 80, 90, 100 % del dataset

# In[58]:


from sklearn.utils.multiclass import unique_labels
plt.rcParams['figure.figsize'] = (16,14)
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


im = ax1.imshow(cm, interpolation='nearest', cmap=cmap)
ax1.figure.colorbar(im, ax=ax)
    
    
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
        
fig.tight_layout()


# In[ ]:





# ### Compute the Matthews correlation coefficient (MCC)
# 
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.matthews_corrcoef.html

# In[59]:


from sklearn.metrics import matthews_corrcoef

mcc_70 = matthews_corrcoef(y70_test, y70_pred)
mcc_80 = matthews_corrcoef(y80_test, y80_pred)
mcc_90 = matthews_corrcoef(y90_test, y90_pred)
mcc_100 = matthews_corrcoef(y100_test, y100_pred)

print(mcc_70, mcc_80, mcc_90, mcc_100)


# In[ ]:





# In[60]:


from sklearn.metrics import f1_score
f1_macro = f1_score(y100_test, y100_pred, average='macro')
f1_micro = f1_score(y100_test, y100_pred, average='micro')
f1_weighted = f1_score(y100_test, y100_pred, average='weighted')
f1_none = f1_score(y100_test, y100_pred, average=None)

print(f1_macro, f1_micro, f1_weighted, f1_none)


# In[61]:


from sklearn.metrics import precision_score
ps_macro = precision_score(y100_test, y100_pred, average='macro')
ps_micro = precision_score(y100_test, y100_pred, average='micro')
ps_weighted = precision_score(y100_test, y100_pred, average='weighted')
ps_none = precision_score(y100_test, y100_pred, average=None)

print(ps_macro, ps_micro, ps_weighted, ps_none)


# In[62]:


from sklearn.metrics import recall_score
rec_macro = recall_score(y100_test, y100_pred, average='macro')
rec_micro = recall_score(y100_test, y100_pred, average='micro')
rec_weighted = recall_score(y100_test, y100_pred, average='weighted')
rec_none = recall_score(y100_test, y100_pred, average=None)

print(rec_macro, rec_micro, rec_weighted, rec_none)

