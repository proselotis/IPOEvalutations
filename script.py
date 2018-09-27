import pandas_datareader.data as web
import datetime as dt
from sklearn.linear_model import LinearRegression
import numpy as np 
import pandas as pd 
from dateutil.relativedelta import relativedelta

def forwardStepWise(data, response, variables):
    model = LinearRegression()
    y = response

    vars_remaining = variables
    
    vars_in_model = []
    last_err = -np.inf

    for _ in range(len(vars_remaining)):
        scores = []
        for var in vars_remaining:
            candidate_vars = vars_in_model + [var]
            X = data[candidate_vars]
            scores.append(cross_val_score(model, X, y, cv=10, scoring="neg_mean_squared_error").mean())

        i = np.argmax(scores)

        if scores[i] <= last_err:
            print(scores[i])
            break
        else:
            last_err = scores[i]
            var_to_add = vars_remaining[i]
            vars_in_model.append(var_to_add)
            del vars_remaining[i]
            print(vars_in_model, scores[i])
            
    return (model, vars_in_model)
    
def backwardRegression(data, response, variables):
    model = LinearRegression()
    y = response


    vars_remaining = []
    vars_in_model = variables

    last_error = cross_val_score(model, data[vars_in_model], response, cv=10, scoring = "neg_mean_squared_error").error()
    for _ in range(len(vars_in_model)):
        scores = []
        for var in vars_in_model:
            candidate_vars = copy.copy(vars_in_model)
            candidate_cars.remove(var)
            X = data[candidate_vars]
            scores.append(
                cross_val_score(model, X, response, cv=10, scoring = "neg_mean_squared_error").mean())

            i = np.argmax(scores)
            if scores[1] <= last_error:
                break
            else:
                last_error = scores[i]
                del vars_in_model[i]
    print(vars_in_model)

def dayCheck(startYear,startMonth,startDay):
   while(True):
      try: 
         testDate = dt.datetime(startYear,startMonth,startDay)
         return testDate
      except ValueError:
         startDay = 1 
         startMonth = startMonth + 1
         if startMonth == 13:
            startMonth = 1 
            startYear = startYear + 1 

def simpleIPODate(symbol):
   try:
      return web.DataReader(symbol, 'iex', dt.datetime.now() - relativedelta(years=5), dt.datetime.now()).iloc[0].name
   except TypeError:
      return ""
   except KeyError:
      sys.exit("This is not a stock on the market")
def findIPODate(symbol,startYear):
   startMonth = 1
   startDay = 2 
   testDate = dayCheck(startYear,startMonth,startDay)
   while(True):
      try:
         f = web.DataReader(symbol, 'morningstar', testDate, testDate + dt.timedelta(days = 1))
         startYear = testDate.year - 1
         break
      except TypeError:
         startYear = testDate.year + 1
         testDate = dayCheck(startYear,startMonth,startDay)
         startYear = testDate.year
         startMonth = testDate.month
         startDay = testDate.day
   testDate = dt.datetime(startYear,startMonth,startDay)
   while(True):
      try:
         f = web.DataReader(symbol, 'morningstar', testDate, testDate + dt.timedelta(days = 1))
         startMonth = testDate.month - 1
         break
      except TypeError:
         startMonth = testDate.month + 1
         testDate = dayCheck(startYear,startMonth,startDay)
         startYear = testDate.year
         startMonth = testDate.month
         startDay = testDate.day
   testDate = dt.datetime(startYear,startMonth,startDay)
   while(True):
      try:
         f = web.DataReader(symbol, 'morningstar', testDate, testDate )
         return testDate
      except TypeError:
         startDay = testDate.day + 1
         testDate = dayCheck(startYear,startMonth,startDay)
         startYear = testDate.year
         startMonth = testDate.month
         startDay = testDate.day