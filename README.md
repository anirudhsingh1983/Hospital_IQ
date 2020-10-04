# Hospital IQ Assignment solution 

## 1. How to run the script?
To run the script, please use the following command on command line.
"python regression.py"

The dependencies to run the scrip are as follows. 
* Libraries: 
  * pandas
  * functools
  * requests
  * statsmodels
  * sklearn 
* Access to internet to read from API 


## 2. Things to do prior to fitting the regression model if Hospital IQ didn't assure clean data.
The actions to clean data would depend upon what are the quality issues in the data. Assuming all common data issues would be present in data, the following actions would be required: 
1. Check for missing values in the data. 
2. Identify the right approach to fill missing values. It could be one of the following: 
  * Functional (based on domain expertise or understanding of data)
  * Imputation by mean/median/etc. 
  * Imputation using KNN
  * Imputation using MICE 
  * Imputation by predictive model like randomforest, etc.
3. Identify the illegitimate values in the data and impute them either by one of the methodologies listed in last point. 
4. Identify outliers and either remove them or rectify their values. I checked it in the code anyways and found no outliers as per the boxplot approach. 
5. I would also make sure the data sample is representative of the population in order to ensure the model doesn't learn to overemphasize on a particular set of cases.

## 3. How did you decide on the covariates in your model?
There was a set of 5 variables to choose from: 'age_in_yrs','hospital_id','last_name','service_id','surgeries_last_month'. 

An important POINT to note is that multivariate normality is the requirement of the a linear regression model. All the abovementioned 5 variables together are not multivariate normal. Also, none of the individual variable is normally distributed. The normality was tested using Shapiro test (scipy.stats.shapiro). So, ideally, linear regression should not be fitted on the model. I didnt check the other requirements (multi-collinearity, homoscedasticity, etc.) of linear regression model as the first condition is breached anyways). 

But, I proceeded with selecting some of the variables as linear regression is the requirement of the assignment. The decision on each of the variable is described as follows. 
* age_in_yrs: It is being used in the model. 
* hospital_id: It has same values throughout the data. So, it contains no informartion value. Hence, it was not used. 
* last_name: It is a string and cannot be used in linear regression. Any transformation of string to numerical values (e.g., target encoding, etc.) was avoided because the last name of a surgeon is not a stable field. For predictions, a new value of last name can will render the model useless. 
* service_id: It is a categorical field (even though the values are numbers). Without functional knowledge, it looks to be nominal and not ordinal. Hence, a target encoding was used for it. A model was tried by using the service_id as numerical field (treating it as an ordinal variable) but it had lower performance on test set.
* surgeries_last_month: It is being used in the model. 


## 4. What is your interpretation of the coefficients of the variables in your model?
* Coefficient of 'age_in_yrs' = 0.1201. This is very small (closer to 0 than 1). This is also expected, given the low correlation between 'age_in_yrs' and 'surgeries_this_month'. So, age doesnt have much impact on number of surgeries per month. 
* Coefficient of 'service_id' = 0.8944. Though, service_id was encoded using target encoding. Hence, a positive coefficient was expected. This variable doesn't have normal distribution and hence is not quite suited for linear regression. However, I have kept it in the model, else we would run out of variables to use. In this case, if the surgeon does the type of surgery that has higher average average of 'surgeries_this_month, the number of expected surgeries will be higher. 
* Coefficient of 'surgeries_last_month' = 1.2026. This value indicates that the higher the number of surgeries in last month, the higher the number of surgeries expected in 'this' month. This variable doesn't have normal distribution too and hence is not quite suited for linear regression. However, I have kept it in the model, else we would run out of variables to use. 


## 5. How well does this model fit the data overall?
The model fits fine as the adjusted R square is fairly high (0.943).However, the stability of model over time or on a different set of data would be a question as the data violates the assumptions of linear regression. 


## 6. What is the output of RegressionResults.summary? (Nothing other than the raw output of that method is needed.)
                             OLS Regression Results                             
|Dep. Variable:     surgeries_this_month   |R-squared:                       0.944|
|----|-----|

|Model:                              OLS   |Adj. R-squared:                  0.943|
|----|-----|

| | | | | 
|----|-----|----|-----|
|Method:|                   Least Squares   |F-statistic:|                     870.3|
|Date:                  |Sun, 04 Oct 2020   |Prob (F-statistic):           |3.77e-97|
|Time:                          |12:22:42   |Log-Likelihood:                |-710.67|
|No. Observations:                   |160   |AIC:                             |1429.|
|Df Residuals:                       |156   |BIC:                             |1442.|
|Df Model:                             |3   |                                 |     |
|Covariance Type:              |nonrobust   |                                 |     |

| | | | | | | | 
|----|-----|----|-----|-----|----|-----|
|                           |coef    |std err          |t      |P>t       |[0.025      |0.975]|
|Intercept             |-142.3748     |13.763    |-10.344     | 0.000     |-169.562    |-115.188|
|age_in_yrs             |  0.1201     | 0.155    | 0.772      | 0.441     |-0.187      | 0.427|
|service_id              | 0.8944     | 0.072    | 12.455     | 0.000     | 0.753      |1.036|
|surgeries_last_month     |1.2026     | 0.025    | 48.769     | 0.000     | 1.154      | 1.251|

| | | | | 
|----|-----|----|-----|
|Omnibus:                       | 3.153   |Durbin-Watson:                |   2.006|
|Prob(Omnibus):                 | 0.207   |Jarque-Bera (JB):             |   2.936|
|Skew:                          |-0.260   |Prob(JB):                     |   0.230|
|Kurtosis:                      | 2.587   |Cond. No.                     |1.81e+03|
 
