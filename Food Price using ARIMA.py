# -*- coding: utf-8 -*-
"""Final final edit .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RCcpepWU06XN3ttyAkEYAK-CxxwONpCy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error

data=pd.read_csv('jordan_food_price.csv')

# Group by date and commodity and calculate mean price
national_prices = data.groupby(['date', 'commodity'])['price'].mean().reset_index()

# Convert 'date' column to datetime format and set it as index
national_prices['date'] = pd.to_datetime(national_prices['date'])
national_prices.set_index('date', inplace=True)

national_prices.head()

national_prices.describe()

print(national_prices.columns)

# Get unique commodities
commodities = national_prices['commodity'].unique()
commodities

import matplotlib.pyplot as plt
# Select data for 'Bread (pita)'
commodity_name = 'Bread (pita)'
commodity_data = national_prices[national_prices['commodity'] == commodity_name]

# Sort the data by date
commodity_data_sort = commodity_data.sort_index()

# Determine the split point for 80% of the data
split_point = int(len(commodity_data) * 0.8)

# Split the data into training and testing sets
train_data = commodity_data[:split_point]
test_data = commodity_data[split_point:]

train_data.head(), test_data.head()

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(train_data.index, train_data['price'], label='Training data')
plt.plot(test_data.index, test_data['price'], label='Testing data')
plt.title(f'ARIMA Model - {commodity_data} Prices')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

from statsmodels.tsa.stattools import adfuller

def adfuller_test(price):
    result = adfuller(price)
    labels = ['ADF Test Statistic', 'p-value', '#Lags Used', 'Number of Observations']
    for value, label in zip(result, labels):
        print(label + ' : ' + str(value))

    if result[1] <= 0.05:
        print("Strong evidence against the null hypothesis (Ho). Reject the null hypothesis. Data is stationary.")
    else:
        print("Weak evidence against the null hypothesis. Indicating it is non-stationary.")

adfuller_test(train_data['price'])

train_data['price'] = pd.to_numeric(train_data['price'], errors='coerce')

differenced_data = train_data['price'].diff(periods=1).dropna()
adfuller_test(differenced_data )

acf_original=plot_acf(train_data ['price'])
pacf_original=plot_pacf(train_data ['price'])

import pmdarima as pm

# Automatically select the best ARIMA model
model = pm.auto_arima(train_data['price'], seasonal=False, trace=True)

# Print model summary
print(model.summary())

# Make predictions
predictions = model.predict(n_periods=len(test_data))

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(test_data['price'], predictions))
print(f"Root Mean Squared Error (RMSE): {rmse}")

from statsmodels.tsa.arima.model import ARIMA

# Fit an ARIMA model
model = ARIMA(train_data['price'], order=(0,1,0))
model_fit = model.fit()

# Make predictions
predictions = model_fit.predict(start=len(train_data), end=len(train_data) + len(test_data) - 1, dynamic=False)

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(test_data['price'], predictions))

# Plot actual vs predicted prices
plt.figure(figsize=(12, 6))
plt.plot(test_data.index, predictions, label='Predicted prices')
plt.plot(test_data.index, test_data['price'], label='Actual prices')
plt.title(f'ARIMA Model - {commodity_name} Prices - Predictions')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

rmse

predictions

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(test_data['price'], predictions))
print(f"Root Mean Squared Error (RMSE): {rmse}")

monthly_prices = commodity_data.resample('M').mean()
model = sm.tsa.ARIMA(monthly_prices['price'], order=(0,1,0))
results = model.fit()
print(results.summary())

forecast = results.get_forecast(steps=12)
forecasted_values = forecast.predicted_mean
forecasted_values

plt.plot(monthly_prices.index, monthly_prices['price'], label='Actual')
plt.plot(forecasted_values.index, forecasted_values, label='Forecast')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('ARIMA Forecast')
plt.legend()
plt.show()

from statsmodels.tsa.statespace.sarimax import SARIMAX
# Fit the SARIMAX model
model = SARIMAX(commodity_data['price'], order=(1,0,0), seasonal_order=(2,1,1,12))
model_fit = model.fit(disp=0)

# Make forecast for the next 12 months
forecast = model_fit.predict(start=len(commodity_data), end=len(commodity_data)+11)

# Print the forecast
print(forecast)

# Plot the actual prices
plt.plot(commodity_data.index, commodity_data['price'], label='Actual Prices')

# Plot the forecasted prices
forecast_index = pd.date_range(start=commodity_data.index[-1], periods=13, freq='M')[1:]  # Generate index for forecasted period
plt.plot(forecast_index, forecast, label='Forecasted Prices')

# Set labels and title
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Forecasted Prices')
plt.legend()

# Show the plot
plt.show()

"""# For Deployment"""

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import ipywidgets as widgets
from IPython.display import display

# Step 1: Load the data
data = pd.read_csv('jordan_food_price.csv')

# Step 2: Preprocess the data
# Group by date and commodity and calculate mean price
national_prices = data.groupby(['date', 'commodity'])['price'].mean().reset_index()
# Convert 'date' column to datetime format and set it as index
national_prices['date'] = pd.to_datetime(national_prices['date'])
national_prices.set_index('date', inplace=True)

# Step 3: Train an ARIMA model for each commodity
# Get unique commodities
commodities = national_prices['commodity'].unique()
# Dictionary to store the models
models = {}
for commodity in commodities:
    # Select data for this commodity
    commodity_data = national_prices[national_prices['commodity'] == commodity]
    # Fit an ARIMA model
    model = ARIMA(commodity_data['price'], order=(0, 1, 0))
    model_fit = model.fit()
    # Store the model in the dictionary
    models[commodity] = model_fit

# Step 4: Create an interactive interface for making predictions
# Create widgets
date_picker = widgets.DatePicker(description='Pick a Date')
commodity_dropdown = widgets.Dropdown(options=commodities, description='Commodity')
# Display widgets
display(date_picker)
display(commodity_dropdown)

# Define a button to generate the prediction
# Define a button to generate the prediction
# Define a button to generate the prediction
# Define a button to generate the prediction
def on_button_clicked(b):
    # Get the selected date and commodity
    date = date_picker.value
    commodity = commodity_dropdown.value
    # Get the model for this commodity
    model = models[commodity]
    # Get the original data for this commodity
    commodity_data = national_prices[national_prices['commodity'] == commodity]['price']
    # Check if the date is in the range of the training data
    if date in commodity_data.index:
        # Make a prediction
        prediction = model.predict(start=date, end=date)
        print(f'Predicted price for {commodity} on {date}: {prediction}')
    else:
        # Generate a forecast
        steps = (date - commodity_data.index[-1].date()).days
        forecast = model.get_forecast(steps=steps)
        prediction = forecast.predicted_mean.iloc[-1]
        print(f'Forecasted price for {commodity} on {date}: {prediction}')

        # Create a date range for the forecast
        forecast_dates = pd.date_range(start=commodity_data.index[-1].date() + pd.Timedelta(days=1), periods=steps, freq='D')
        # Create a new Series with the correct dates as the index
        forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_dates)

    # Plot the last 30 data points
    commodity_data[-30:].plot(label='observed')
    # Plot the forecast
    forecast_series.plot(label='forecast')
    plt.legend()
    plt.show()

button = widgets.Button(description='Predict Price')
button.on_click(on_button_clicked)
display(button)

date_picker = widgets.DatePicker(description='Pick a Date')
commodity_dropdown = widgets.Dropdown(options=commodities, description='Commodity')
# Display widgets
display(date_picker)
display(commodity_dropdown)
# Define a button to generate the prediction
def on_button_clicked(b):
    # Get the selected date and commodity
    date = date_picker.value
    commodity = commodity_dropdown.value
    # Get the model for this commodity
    model = models[commodity]
    # Check if the date is in the range of the training data
    if date in model.data.row_labels.date:
        # Make a prediction
        prediction = model.predict(start=date, end=date)
    else:
        # Generate a forecast
        steps = (date - model.data.row_labels[-1].date()).days
        forecast = model.get_forecast(steps=steps)
        prediction = forecast.predicted_mean.iloc[-1]
    print(f'Predicted price for {commodity} on {date}: {prediction}')

button = widgets.Button(description='Predict Price')
button.on_click(on_button_clicked)
display(button)

"""# Using Tkinter GUI"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
# Create the root window
root = tk.Tk()

# Create a StringVar to hold the date
date_var = tk.StringVar()
# Create a date entry field
date_entry = ttk.Entry(root, textvariable=date_var)
date_entry.pack()

# Create a StringVar to hold the commodity
commodity_var = tk.StringVar()
# Create a dropdown menu for the commodity
commodity_dropdown = ttk.Combobox(root, textvariable=commodity_var, values=list(models.keys()))
commodity_dropdown.pack()



def predict_price():
    # Get the selected date and commodity
    date_str = date_var.get()
    date = datetime.strptime(date_str, '%Y-%m-%d').date()  # convert string to date
    commodity = commodity_var.get()
    # Get the model for this commodity
    model = models[commodity]
    # Check if the date is in the range of the training data
    if date in model.data.row_labels.date:
        # Make a prediction
        prediction = model.predict(start=date, end=date)
    else:
        # Generate a forecast
        steps = (date - model.data.row_labels[-1].date()).days
        forecast = model.get_forecast(steps=steps)
        prediction = forecast.predicted_mean.iloc[-1]
    print(f'Forecasted price for {commodity} on {date}: {prediction}')

# Create a button to generate the prediction
predict_button = ttk.Button(root, text="Predict Price", command=predict_price)
predict_button.pack()

root.mainloop()

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import pandas as pd

# Create the root window
root = tk.Tk()

# Create a StringVar to hold the date
date_var = tk.StringVar()
# Create a label and an entry field for the date
date_label = ttk.Label(root, text="Write the date (yyyy-mm-dd):")
date_label.pack()
date_entry = ttk.Entry(root, textvariable=date_var)
date_entry.pack()

# Create a StringVar to hold the commodity
commodity_var = tk.StringVar()
# Create a label and a dropdown menu for the commodity
commodity_label = ttk.Label(root, text="Commodity Type:")
commodity_label.pack()
commodity_dropdown = ttk.Combobox(root, textvariable=commodity_var, values=list(models.keys()))
commodity_dropdown.pack()
# Create a button to generate the prediction
predict_button = ttk.Button(root, text="Predict Price", command=predict_price)
predict_button.pack()
# Create a Text widget to display the output
output_text = tk.Text(root)
output_text.pack()

# Create a figure and a canvas to display the figure
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Define a function to generate the prediction
def predict_price():
    # Clear the figure
    fig.clear()

    # Get the selected date and commodity
    date_str = date_var.get()
    date = datetime.strptime(date_str, '%Y-%m-%d').date()  # convert string to date
    commodity = commodity_var.get()
    # Get the model for this commodity
    model = models[commodity]
    # Get the original data for this commodity
    commodity_data = national_prices[national_prices['commodity'] == commodity]['price']

    # Check if the date is in the range of the training data
    if date in model.data.row_labels.date:
        # Make a prediction
        prediction = model.predict(start=date, end=date)
        output_text.insert(tk.END, f'Predicted price for {commodity} on {date}: {prediction}\n')
    else:
        # Generate a forecast
        steps = (date - commodity_data.index[-1].date()).days
        forecast = model.get_forecast(steps=steps)
        prediction = forecast.predicted_mean.iloc[-1]
        output_text.insert(tk.END, f'Forecasted price for {commodity} on {date}: {prediction}\n')

        # Create a date range for the forecast
        forecast_dates = pd.date_range(start=commodity_data.index[-1] + pd.Timedelta(days=1), periods=steps, freq='D')
        # Create a new Series with the correct dates as the index
        forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_dates)

        # Plot the last 30 data points
        ax = fig.add_subplot(111)
        ax.plot(commodity_data[-30:], label='observed')
        # Plot the forecast
        ax.plot(forecast_series, label='forecast')
        ax.legend()

        # Redraw the canvas
        canvas.draw()



root.mainloop()

