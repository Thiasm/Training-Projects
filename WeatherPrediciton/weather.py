import pandas as pd # type: ignore
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error

def createPredictions(predictors, coreData, reg):

# Prepare the data to train the Regression Model
    train = coreData.loc[:"2020-12-31"] # Assign "train" all the data from the start until end of 2020
    test = coreData.loc["2021-01-01":] # Assign "test" all the data from start of 2021 until now
    reg.fit(train[predictors], train["TARGET"]) # Train the Regression Model to predict the next TMAX value with real past values 

# Generate the predictions 
    predictions = reg.predict(test[predictors]) # Generate TMAX predictions for the "test"
    error = mean_absolute_error(test["TARGET"], predictions) # ?

# Prepare data for visualisation
    combined = pd.concat([test["TARGET"], pd.Series(predictions, index=test.index)], axis=1) # Concat real and predicted TMAX values in a Dataframe
    combined.columns=["actual", "predictions"] # Rename the columns for better visibility
    return error, combined


def mainFunction():
    
# Setup Data
    data = pd.read_csv("weatherData.csv", index_col="DATE") # Read data and set index to Date
    coreData = data[["PRCP", "SNOW", "SNWD", "TMAX", "TMIN"]].copy() # Select most valuable data to work with
    
# Remove useless values
    # print(coreData.apply(pd.isnull).sum() / coreData.shape[0]) # Find the colums with the more empty values
    # print(coreData["SNOW"].value_counts()) # Get the diferent values of Snow to figure out if it's worthit to keep it
    # print(coreData["SNWD"].value_counts()) # Get the diferent values of Snow to figure out if it's worthit to keep it
    del coreData["SNOW"]
    del coreData["SNWD"]

# Replace NULL values with theoritical values
    # print(coreData[pd.isnull(coreData['PRCP'])])
    # print(coreData["PRCP"].value_counts())
    coreData["PRCP"] = coreData["PRCP"].fillna(0) # Replace the Null values with 0
    coreData = coreData.ffill() # Replace all the null values with previous not null value
    
# Convert Data Format to improve the visibility
    coreData.index = pd.to_datetime(coreData.index) # Convert litteral date in date Object
    coreData[['TMAX', "TMIN"]] = coreData[['TMAX', "TMIN"]].sub(32).mul(5).div(9) # Convert F° to C° in TMAX and TMIN
    
# Prepare Data
    coreData["TARGET"] = coreData.shift(-1)["TMAX"] # Create in Target a list with all the TMAX values shifted with 1 rank less 
    coreData = coreData.iloc[:-1].copy() # Delete the last row of the list (to remove the Null value on target crated by the shift)

# Create new values for the model
    coreData["mobileMonthAverage"] = coreData["TMAX"].rolling(30).mean() # Generate a mobile month average tmax value
    coreData["monthDayMax"] = coreData.apply(lambda row: row["mobileMonthAverage"] / row["TMAX"] if row["TMAX"] != 0 else 0, axis=1) # Generate a MonthAverage/Tmax value
    coreData["maxMin"] = coreData.apply(lambda row: row["TMAX"] / row["TMIN"] if row["TMIN"] != 0 else 0, axis=1)  # Generate a Tmax/Tmin value
    
# Fix not usable values    
    coreData = coreData.dropna() # Now remove rows with NaN

# Create more new values for the model
    monthAverage = coreData['TMAX'].groupby(coreData.index.month).apply(lambda x: x.expanding(1).mean()) # Generate an expanding TMAX average per month
    monthAverage = monthAverage.reset_index(level=0, drop=True) # Remove Index
    coreData['monthAverage'] = monthAverage.copy() # Remove Index

    yearAverage = coreData['TMAX'].groupby(coreData.index.day_of_year).apply(lambda x: x.expanding(1).mean()) # Generate an expanding TMAX average per year
    yearAverage = yearAverage.reset_index(level=0, drop=True) # Remove Index
    coreData['yearAverage'] = monthAverage.copy() # Remove Index
    
# Display the prediction
    reg = Ridge(alpha=.1) # Init Regression model    
    predictors = ["PRCP", 'TMAX', 'TMIN', 'mobileMonthAverage', 'monthDayMax', 'maxMin', 'monthAverage', 'yearAverage'] # Indicate the values to use for the next TMAX prediction
    error, combined = createPredictions(predictors, coreData, reg)
    print(error) # Indicate the absolute error average
    combined.plot()
    plt.show() # Display the results

# Analyse the quality
    print(reg.coef_)
    print(coreData.corr()['TARGET'])
    combined['diff'] = (combined['actual'] - combined['predictions']).abs()
    print(combined.sort_values("diff", ascending=False).head())

    return

if __name__ == "__main__":
    mainFunction()