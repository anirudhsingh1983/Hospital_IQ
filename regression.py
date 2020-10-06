# -*- coding: utf-8 -*-
"""
Created on 04 Oct 2020  

@author: Anirudh Singh 
@version: 1.0 
"""

# Imports 
import pandas as pd
pd.options.mode.chained_assignment = None
import functools, requests
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Constants 
CONSTANTS = {"URL":'https://bitbucket.org/!api/2.0/snippets/patientroute/eaXpKj/2d820cd34758161cafb395e8550f1cba2bab4273/files/b_data.json',
             'test_size':0.2,
             'seed':0}

def read_from_API(constants):
    """
    Reads data JSON from API 
    
    Args: 
        constants (dictionary): Dictionary of constants and their values 
        
    Returns:
        dataframe: Returns the data of JSON in dataframe format. If the data pull from API was unsuccessful, an empty dataframe is returned.  
        bool: Returns a flag to indicate if the data fetch from API was successul or not. True indicates success and False indicates failure.  
    """
    
    # Read data from API 
    read_success = True 
    data = pd.DataFrame()
    
    try:
        data_json = requests.get(constants['URL']).json()
        # Flatten the dictionary values to a list 
        json_values_in_list = functools.reduce(lambda x,y:x+y,data_json.values())
        # Convert the flattened dictionary values (in the list) to a dataframe 
        data = pd.DataFrame(json_values_in_list)

    except:
        read_success = False
        print("API fetch unsuccessful. Further execution of program terminated.")
        
    return(data,read_success)
    

def target_encoder(data,column='service_id',target='surgeries_this_month',encoding_type='mean'):
    """
    Transform a selected column of the dataframe to its target encoding based on the 'target' argument. 
    
    Args: 
        data (dataframe): Dataframe containing data  
        column (string): A string containing the name of the column to be transformed 
        target (string): A string containing the name of the target column  
        encoding_type (string): String representing encoding function to be used for label encoding 
         
    Returns:
        dataframe: Dataframe containing the transformed column (with rest of the data remaining same)
        dictionary: Encodings in python dictionary object 
    """
    # Generate encodings for each value of column 
    data_group_by_column = data.groupby([column])[target].agg([encoding_type])
    target_encoding_mappping = data_group_by_column[encoding_type].to_dict()
    
    # Apply encodings to the column of the dataframe
    data[column] = data[column].map(target_encoding_mappping)
    
    return(data,target_encoding_mappping)


def regression(data,formula='surgeries_this_month ~ age_in_yrs + service_id + surgeries_last_month'):
    """
    Trains a linear regression model on data based on the argument 'formula' 
    
    Args: 
        data (dataframe): Dataframe containing data to be used for linear regression model 
        formula (string): A string containing formula indicating dependent and independent variables for the linear regression model 
                            Default value is: 'surgeries_this_month ~ age_in_yrs + service_id + surgeries_last_month'
    Returns:
        statsmodels.regression.linear_model.RegressionResultsWrapper: Trained model object   
    """
    # Fit the linear regression model 
    model = smf.ols(formula=formula, data=data).fit()
    
    return(model)



def outlier_detection(d,column):
    """
    Transform a selected column of the dataframe to its target encoding based on the 'target' argument. 
    
    Args: 
        d (dataframe): Dataframe containing data  
        column (string): A string containing the name of the column to be checked for outliers
         
    Returns:
        bool: flag indicating if at least one outlier was found
        dataframe: Dataframe with outliers removed 
    """
    # Calculate inter-quantile range, upper & lower bounds as per box plot outlier detection logic 
    iqr = d[column].quantile(0.75) - d[column].quantile(0.25)
    ub = d[column].quantile(0.75) + 1.5*iqr
    lb = d[column].quantile(0.25) - 1.5*iqr
    
    # Identify if any outliers found
    if d.loc[(d[column] < lb)|(d[column] > ub)].shape[0] > 0:
        outlier_present = True 
        # Filter out outliers 
        d = d.loc[(d[column] >= lb)&(d[column] <= ub)]
    else:
        outlier_present = False 
    
    return(outlier_present,d)


    

def main():
    """
    The main driver function of the module to execute the model development job 
    Args: None
    Returns: None
    """
    # Read data from API into a dataframe 
    data,read_success = read_from_API(constants=CONSTANTS)
    if read_success == True: 
        # Split data into train and test sets 
        data_train, data_test = train_test_split(data,test_size=CONSTANTS['test_size'], random_state=CONSTANTS['seed'],shuffle=True)

        # Apply target encoding to service_id
        data_train, target_encoding_mappping = target_encoder(data_train,column='service_id',target='surgeries_this_month',encoding_type='mean')
        data_test['service_id'] = data_test['service_id'].map(target_encoding_mappping)

        # Check if there is any outlier to be removed before fitting the model. In this case, there was nothing found. If outliers would be found, we would remove them. 
        if sum([outlier_detection(data_train,col)[0] for col in data_train.columns[[0,3,4,5]]]) == 0:
            print("No outliers found. Proceeding without any data elimination from train set. \n\n")

        # Train a linear regression model from data in dataframe 
        model = regression(data_train,formula='surgeries_this_month ~ age_in_yrs + service_id + surgeries_last_month')

        # Print model summary 
        print(model.summary())

        # Calculate and print RMSE 
        print("RMSE on test set is: ",str(metrics.mean_squared_error(model.predict(data_test),data_test['surgeries_this_month'])))



# Execute main()
if __name__ == "__main__":
    main()


