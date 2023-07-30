# Food Price Forecasting for Essential Items in Jordan

## Overview
This project focuses on the analysis and prediction of food prices for essential items in Jordan, utilizing data from the World Food Programme. The ARIMA and SARIMAX models are employed for time series forecasting to predict future prices for commodities, with Bread (pita) being the main focus.

## Documentation

### Data Selection
A dataset from the World Food Programme organization was chosen, providing food prices in Jordan and its governorates.

### Feature Extraction
- The commodity feature showed the highest score.
- Calculated the average price for each commodity.
- Final dataset contains three features: date, commodity, and price.

### Data Preparation
- Chose Bread (pita) as the target commodity.
- Split the data into 80% training and 20% testing sets.
- A figure is plotted to visualize training and testing data.

### ARIMA Model
ARIMA (Autoregressive Integrated Moving Average) was used for forecasting, with challenges including:
- Stationarity checks using the adfuller test.
- Transforming the data to achieve stationarity through differencing.
- Determining model order (p,d,q) using ACF and PACF plots.
- Best model found was ARIMA(0,1,0) with pmdarima.

### Model Performance
- Applied ARIMA to predict prices.
- Calculated RMSE to evaluate performance.

### Future Price Forecasting
- Forecasted future prices monthly for the next year using ARIMA and SARIMAX.
- Visualized forecasted data.

### Deployment
- Utilized Jupyter Widgets for interactive browser controls.
- Deployed using Tkinter GUI, allowing users to input date and commodity to get price predictions.

## Technologies Used
- Python
- ARIMA
- SARIMAX
- pmdarima
- Tkinter

## Contributors
- Marwa Amayreh
- Osama Alzamel
- Ammar Abid Aldaim

