## This file contains a few generalized functions for making
## running machine learning for SETs more streamlined
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split

## Funtion for getting dataframe to only node magnitude and pulse width
def df_cleanup(df):
    df.sort_values(by=['Node'], inplace=True)

    # # Label Encoder is used to encode Nodes (strings) into values between 0 and 
    # # n_classes - 1
    le = preprocessing.LabelEncoder()
    le.fit(df["Node"])
    df["Node"] = le.transform(df["Node"])

    new_df = df.drop(["Bias 1", "Bias 2", "Number of Transients", "Deposited_Q"], axis=1)

    new_df['Magnitude'] = new_df['Magnitude'].astype(float, errors='raise')
    new_df['Pulse Width'] = new_df['Pulse Width'].astype(float, errors='raise')
    
    return new_df


## Function for Printing Column of Coorelation Matrix
def print_corr(dataframe, column):
    print(dataframe.corr()[column] )


## Function for splitting up testing and training material
## and splitting node to be classified from the rest
def training_split(dataframe, column, test_size, random_state):
    
    X = dataframe.drop(column, axis=1)
    y = dataframe[column]

    ## Convert datafram to array
    X = X.to_numpy()
    y = y.to_numpy()
    # print(y)
    # print(le.inverse_transform(y))

    ## Scale values
    X = preprocessing.scale(X)

    

    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.25, random_state=1234)
    
    return  (X, y, X_train, X_test, y_train, y_test)


## kNN Model Initialization and Run
def kNN_initialization(n_neighbors, X_train, y_train, X_test, y_test):
    

    ## Initialize knn model with arbitrary n_neighbors (k) value
    # Maybe use unsupervised version?
    knn = KNeighborsClassifier(n_neighbors)

    ## Fit kNN
    knn.fit(X_train, y_train)

    ## predict y_test value using fitted mode
    y_pred = knn.predict(X_test)
    #plot_confusion_matrix(knn, X_test, y_test)

    ## Print accuracy of kNN
    print("Initial kNN Accuracy:",metrics.accuracy_score(y_test, y_pred))
    return knn


## kNN Model Optimization using GridSearchCV
def gridSearchCV_Optimization(largest_n_neighbors, X_train, y_train, X_test, y_test):
    from sklearn.model_selection import GridSearchCV
    parameters = {"n_neighbors": range(1, largest_n_neighbors),
        "weights": ["uniform", "distance"]}
    gridsearch = GridSearchCV(KNeighborsClassifier(), parameters)
    gridsearch.fit(X_train, y_train)
    print(gridsearch.best_params_)
    test_preds_grid = gridsearch.predict(X_test)
    print("Optimized Accuracy:",metrics.accuracy_score(y_test, test_preds_grid))
    return gridsearch
