import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error


# Load your dataset
excel_file = r'C:\Users\yagmur\Desktop\TR-GNP.xlsx'
data = pd.read_excel(excel_file, names=['Year', 'GNP', 'iGNPi'])

# Assuming you have a 'year' column and a 'gnp' column
year_column = 'Year'
gnp_column = 'GNP'

# Sort the data by year for better visualization
data.sort_values(by=year_column, inplace=True)

# Calculate the six-month moving average
data['six_month_avg'] = data[gnp_column].rolling(window=6).mean().shift(1)
# Filter data for the period 2015 to 2022
filtered_data = data[(data['Year'] >= 2015) & (data['Year'] <= 2022)].copy()

# Calculate the arithmetic average of observations from 2000 to 2014 (inclusive) and divide by 15
start_year = 2000
end_year = 2014

sum_values = 0
count_values = 0

for year in range(start_year, end_year + 1):
    values_for_year = data[data['Year'] == year][gnp_column].values
    if len(values_for_year) > 0:
        sum_values += values_for_year[0]
        count_values += 1

init_value = sum_values / 15 if count_values > 0 else 0

# Set the initial value for 2015
data.loc[data['Year'] == 2015, 'exp_smoothed'] = init_value

# Function for simple exponential smoothing
def simple_exponential_smoothing(series, alpha, init_value):
    result = [init_value]  # Set the initial value directly
    for t in range(1, len(series)):
        result.append(alpha * series.iloc[t-1] + (1 - alpha) * result[t-1])
    return result

#User input
alpha = float(input("Enter the value of alpha (between 0 and 1): "))

# Apply simple exponential smoothing to the GNP column starting from 2015
data.loc[data['Year'] >= 2015, 'exp_smoothed'] = simple_exponential_smoothing(
    data[data['Year'] >= 2015][gnp_column], alpha, init_value
)

# Filter data for the period 2015 to 2022
filtered_data = data[(data['Year'] >= 2015) & (data['Year'] <= 2022)].copy()

# Print the DataFrame with the exponential smoothing
print(filtered_data[[year_column, gnp_column, 'exp_smoothed']])

# Print the DataFrame with the six-month moving average
print(filtered_data[["Year","GNP", 'six_month_avg']])

#plot the graphs
plt.figure(figsize=(10, 6))
plt.plot(filtered_data[year_column], filtered_data[gnp_column], label='Actual Values')
plt.plot(filtered_data[year_column], filtered_data['six_month_avg'], label='Six-Month Moving Average')
plt.plot(filtered_data[year_column], filtered_data['exp_smoothed'], label=f'Exponential Smoothing Forecast (alpha={alpha})', color='green', linestyle='-.')
plt.xlabel('Year')
plt.ylabel('GNP')
plt.title('Actual GNP - Six-Month Moving Average - Simple Exponential Smoothing for 2015-2022')
plt.show()


# Calculate percentage increase for both methods
filtered_data['Percentage_Increase_ES'] = (filtered_data['exp_smoothed'] - filtered_data['GNP']) / filtered_data['GNP'] * 100
filtered_data['Percentage_Increase_Six_Year'] = (filtered_data['six_month_avg'] - filtered_data['GNP']) / filtered_data['GNP'] * 100

print(filtered_data['Percentage_Increase_ES'])
print(filtered_data['Percentage_Increase_Six_Year'])

# Convert Percentage Increase to GNP itself
filtered_data['Adjusted_Forecast_ES'] = filtered_data['GNP'] + (filtered_data['GNP'] * filtered_data['Percentage_Increase_ES'] / 100)
filtered_data['Adjusted_Forecast_Six_Year'] = filtered_data['GNP'] + (filtered_data['GNP'] * filtered_data['Percentage_Increase_Six_Year'] / 100)

#plot the percentage increase graphs for both Moving Average and Exponential Smoothing
plt.figure(figsize=(10, 6))
plt.plot(filtered_data['Year'], filtered_data['Percentage_Increase_ES'], label='Exponential Smoothing')
plt.plot(filtered_data['Year'], filtered_data['Percentage_Increase_Six_Year'], label='Six-Month Moving Average')
plt.xlabel('Year')
plt.ylabel('Percentage Error')
plt.title('Percentage Error for Exponential Smoothing and Six-Month Moving Average')
plt.legend()
plt.show()

# MAD and MSE calculation for moving average
mad_ma = mean_absolute_error(filtered_data['GNP'], filtered_data['Adjusted_Forecast_Six_Year'])
mse_ma = mean_squared_error(filtered_data['GNP'], filtered_data['Adjusted_Forecast_Six_Year'])

# MAD and MSE calculation for exponential smoothing
mad_es = mean_absolute_error(filtered_data['GNP'], filtered_data['Adjusted_Forecast_ES'])
mse_es = mean_squared_error(filtered_data['GNP'], filtered_data['Adjusted_Forecast_ES'])

print(f'MA MAD: {mad_ma}, MA MSE: {mse_ma}')
print(f'ES MAD: {mad_es}, ES MSE: {mse_es}')



