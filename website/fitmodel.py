#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[57]:


df = pd.read_csv("D:/Kavya/kjc/6thsem/project/final/website/fitfact.csv", header=0, parse_dates=[0])


df.bool_of_active[(df.bool_of_active==500)]=1


X = df.drop(["Stress_level","date"],axis=1)
X


# In[71]:


y = df["Stress_level"]


# ## Test Train Split

# In[72]:


from sklearn.model_selection import train_test_split


# In[73]:


X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=0)


# In[74]:


X_train.head()


# In[75]:


from sklearn import tree
regtree = tree.DecisionTreeRegressor(max_depth = 5)


# In[76]:


regtree.fit(X_train, y_train)


# In[78]:


y_train_pred = regtree.predict(X_train)
y_test_pred = regtree.predict(X_test)


# ## Performance

# In[79]:


from sklearn.metrics import mean_squared_error, r2_score


# In[80]:


mean_squared_error(y_test, y_test_pred)


# In[81]:


r2_score(y_train, y_train_pred)


# In[82]:


r2_score(y_test, y_test_pred)

# In[84]:






# In[87]:


from sklearn.ensemble import RandomForestRegressor


# In[88]:


rf_reg = RandomForestRegressor(n_estimators=1000, n_jobs=-1 ,random_state=0)


# In[90]:


rf_reg.fit(X_train, y_train)


# In[91]:


mean_squared_error(y_test, rf_reg.predict(X_test))


# In[93]:


r2_score(y_test, rf_reg.predict(X_test))


# ## Gridsearch

# In[137]:


from sklearn.model_selection import GridSearchCV


# In[161]:


rf_reg = RandomForestRegressor(n_estimators=1000,random_state=0, oob_score=True)


# In[162]:


params_grid = {"max_features" : [2,3,4,5,6,7,8,9,10,15],
              "min_samples_split": [2, 3, 4, 5, 7, 8, 10]
              }


# In[163]:


grid_search = GridSearchCV(rf_reg, params_grid,
                           n_jobs=-1, scoring='r2')


# In[164]:


grid_search.fit(X_train, y_train)


# In[165]:


grid_search.best_params_


# In[166]:


cvrf_reg = grid_search.best_estimator_


# In[167]:


r2_score(y_test, cvrf_reg.predict(X_test))


# In[171]:


r2_score(y_train, cvrf_reg.predict(X_train))


# In[172]:


import pickle
pickle.dump(cvrf_reg, open('model.pkl','wb'))

model = pickle.load(open('model.pkl','rb'))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




