## So you want to choose a model:

### Explanation:
Let's just resign ourselves to _not_ doing this. 

#### Linear/logistic regression:
What you want to do:
- recover beta coefficients such that you can say a one-unit change in volume of traffic results in a 0.45% increase in number of accidents

What you need:
- domain knowledge to the extent that you can write a linear combination of variables that are well-measured, independent of each other and the error term, and complete
- no endogeneity:
	- omitted variables: when sunny days causes both increase in traffic and accidents (via glare) and it's not in your model
	- reverse causality: more accidents actually causes more traffic (maybe due to backups along the route)
	- data that is not missing in a systematic way
Defending your model on these grounds is really difficult and generally not what you need to do anyway, in practical terms.

### Prediction: Quantities

#### Linear regression:
Luckily, you can still use linear regression with relaxed assumptions to make a good prediction if you don't care about the coefficients on the independent variables. Then you can just throw in all the features you think of because multicollinearity doesn't affect the overall model fit.

**Your data looks like**:
- At least ~20 observations per X
- No outliers

**Returns**: interpretable!
- An actual quantity estimate (e.g. number of car crashes)
- beta coefficients for each independent variable that can be broadly interpreted for direction and magnitude of effect (confidence in this depends on how good your model is)
- p-values

**Improving fit**:
- Stepwise regression, aka adding and subtracting features until you get a nice R-squared, is extremely frowned upon in academia but is apparently okay in the real world. You can use the likelihood-ratio test with each predictor to build your model based on their contributions.
- Try multinomial transformations of your features
- Try adding interaction terms (x2**x3) if you think some features behave differently at different levels of other features (e.g. traffic is extra likely to lead to car crashes when the weather's bad)
- L2 regularization, aka Ridge, will help you stabilize your model if there is a lot of multicollinearity

_Reduce_: 
- L1 regularization, aka Lasso, will help you drop variables that don't have a large effect (this biases the model, so do NOT interpret).
	- grid search an alpha term that sets the level of your penalty: higher lambda = sparser model (**linear_model.Lasso(alpha = _)**)

**Caveats**:
- In statsmodels, don't forget to make an intercept (**sm.add_constant()**). SM returns a lot of good things like coefficients and confidence intervals but the score function is _not_ an accuracy score, so you'll have to compute your own.


### Prediction: Classes

### Linear
Generally if you think your classes are separable via linear boundary (a line, an ellipse, a parabola), you should pick one of these because they are faster and easier to train. If you can draw a linear boundary, choosing something like knn won't add much value. However, these are not a good choice if you think you will have multidimensional clusters of labels that are overlap. Try these first.

#### Logistic regression: 

_A lot of machine learning resources put logistic regression in with classification algorithms, but it's not really that because you are actually looking at the response of Y to changes in your Xs (it's not just that a combination of Xs places the Y in a given category)._

**Your data looks like**:
- Few features
- Not a lot of missing data, no outliers
- Okay: some noise (more robust to noise than NB, for example)
- Multicollinearity: no

**You want**:
- Scalable, easy to update model; probability estimates

**Returns**: interpretable!
- Change in logit for Y given one-unit change in predictor; this can be transformed to an odds ratio for interpretability or into a prediction based on some cutoff of the odds
- beta coefficients for each independent variable 

**Improving fit**:
_Reduce_: 
- Lasso regularization
- Random forest/SVM can give a ranking of variables by importance that you can then stick in your regression to see how their effect

**Caveats**:
- May not converge with a lot of multicollinearity in Xs - reduce first
- Drop one of the dummies (your base case, aka if I only include 'summer', 'fall', and 'spring', my model captures the effect of changing to another season from winter as the baseline): **pd.get_dummies(drop_first=True)**

#### Naive Bayes: 

**Your data looks like**:
- Okay: smaller training set, lots of features, missing data
- Multicollinearity: no
- _Especially_: text data

**You want**:
- Simple, fast, scalable, avoid overfit

**Caveats**:
- Sensitive to class imbalance, so change your priors, e.g. use a uniform
- NB assumes independence of features and in practice is fairly robust to violations of this but it can still create problems. Either change priors to penalize highly dependent features or change predictor threshold to reflect this (e.g. 'San Francisco' is counted twice for each 'Boston' even though they appear with the same frequency, so either deprecate 'San' or only classify as SF at a threshold of 0.66). 
- Use a pseduocount to avoid zero-frequency problems when a particular label-feature combination doesn't appear in your dataset

#### SVM:

**Your data looks like**:
- Okay: many features, partial/weak label information
- Multicollinearity: okay
- _Especially_: text

**You want**:
- High accuracy, avoid overfit; you don't mind inefficient training & non-interpretability

**Returns**:
- You can get SVM to return probabilities, but it will be slow: **SVC(probability = True)**

**Improving fit**:
- SVM can automatically balance classes for you: **SVC(class_weight='balanced')**
- Adjust soft margin cost function (penalty of error term), C: larger = more support vectors --> overrfit (**SCV(C = _)**)
- If not linearly separable: kernel choice ('linear', 'poly', 'rbf', etc.)
- For rbf, poly, and sigmoid kernels: gamma term defines influence of each training example; high gamma = overfit

#### K-means clustering:

**Your data looks like**:
- Few features
- Little missing data, little noise, no outliers
- Multicollinearity: okay

**You want**:
- fast, **unsupervised** predictions

**Improving fit**:
- Change k number of clusters (which is essentially changing the size of the clusters) - k-means is super-sensitive to this: **KMeans(n_clusters = _)**
- Starting points (seeds/centroids) of each of the clusters - sklearn will try a number (**n_init**) for you
- Weight features by importance in preprocessing because kmeans just uses Euclidean distances 

**Caveats**:
- BIG assumptions: spherical clusters, all variables have same variance, all clusters are about the same size
- Will return clusters even if there aren't any actual clusters!
- Clusters have hard boundaries; there's no softness allowance like in SVM
- Variables must be scaled
- Similar to knn, you have to figure out how to compute similarity for categorical variables; how you do this can affect the results

### Non-linear
#### Random forest

**Your data looks like**:
- Okay: large amounts of data, lots of features, outliers, lots of categorical variables
- Multicollinearity: okay

**You want**:
- Fast, scalable (but you'll still have to grow the forest each time you change the model)

**Improving fit**:
- try different information criterion: **RandomForestClassifier(criterion='gini'|'entropy')**
_Reduce_:
- Limit tree depth: **max_depth**
- Limit number of variables that are used to build each leaf (usually the square root of the number of features): **max_features**
- Limit splits: **min_samples_split**, **min_samples_leaf**

**Caveats**:
- Prone to overfit: prune as above
- Balance your classes: **class_weight = 'balanced'** will do the inverse proportional for you
- If using for feature selection, rf is biased toward features with lots of categories and will arbitrarily choose between multicollinear features (so don't interpret)

#### K-nearest neighbors: 

**Your data looks like**:
- Few features
- Little missing data, little noise
- Multicollinearity: no
- _Especially_: features are geographic/make sense as distances

**You want**:
- Fast training, but slow to compute (all training is in memory)

**Improving fit**:
- change k number of neighbors: smaller = more prone to overfit, but larger is hard to run (and pointless; as k approaches n, the prediction converges to the baseline mean guess); **KNeighborsClassifier(n_neighbors = _)**
- change weighting of points, e.g. by distance to penalize further away neighbors: **KNeighborsClassifer(weights = 'distance')** - default is uniform
- change distance function (based on continuous/binary/categorical variables)

**Caveats**:
- Sensitive to class imbalance
- Remember to normalize/standardize your continuous features and encode categorical variables 

