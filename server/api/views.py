from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import StockPredictionSerializer
from  rest_framework import status
from  rest_framework.response import Response
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from django.conf import settings
from .utils import save_plot
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from sklearn.metrics import mean_squared_error, r2_score

class StockPredictionAPIView(APIView):
    def post(self, request):
        serializer = StockPredictionSerializer(data=request.data)
        if serializer.is_valid():
            ticker = serializer.validated_data['ticker']

            #fetch the data from yfinance
            current_date = datetime.now()
            start_date = datetime(current_date.year-10, current_date.month, current_date.day)
            end_date = current_date
            dataFrame = yf.download(ticker, start_date, end_date)
            print(dataFrame)
            if dataFrame.empty:
                return Response({'error': 'No Data found for the given ticker.', 'status': status.HTTP_404_NOT_FOUND})
            dataFrame = dataFrame.reset_index()
            print(dataFrame)

            #Generate Basic plots
            plt.switch_backend('AGG')
                #Non-interactive backends (like Agg) just render the plot into an image in memory/file
                #What is "Agg" specifically?
                #Agg stands for Anti-Grain Geometry — a library for rendering high-quality raster (pixel-based) images. It draws the figure directly to a .png, .jpg, or similar image file, but it can't open a window to show it live.

            plt.figure(figsize=(12, 5))
            plt.plot(dataFrame.Close, label='Closing')
            plt.title(f'Closing price of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()

            # Save the plot to the file
            plot_img_path = f'{ticker}_plot.png' 
            #with f O/p: AAPL_plot.png || without f o/p: {ticker}_plot.png

            plot_img = save_plot(plot_img_path)

            # 100 days moving average
            ma100 = dataFrame.Close.rolling(100).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(dataFrame.Close, label='Closing')
            plt.plot(ma100, 'r', label='100 DMA')
            plt.title(f'100 Days of Moving Average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_img_path = f'{ticker}_100_dma.png' 
            plot_100_dma = save_plot(plot_img_path)

            # 200 days moving average
            ma200 = dataFrame.Close.rolling(200).mean()
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(dataFrame.Close, label='Closing')
            plt.plot(ma100, 'r', label='100 DMA')
            plt.plot(ma200, 'g', label='200 DMA')
            plt.title(f'200 Days of Moving Average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_img_path = f'{ticker}_200_dma.png' 
            plot_200_dma = save_plot(plot_img_path)

            # Splitting data into training and testing datasets
            dataTraining = pd.DataFrame(dataFrame.Close[0:int(len(dataFrame)*0.7)])
            dataTesting = pd.DataFrame(dataFrame.Close[int(len(dataFrame)*0.7): int(len(dataFrame))])

            # Scaling down the data between 0 & 1
            scaler = MinMaxScaler(feature_range=(0,1))

            # Load ML model
            model = load_model('Resources/stock_prediction_model.keras')

            #Preparing Test Data
            past_100_days = dataTraining.tail(100)
            final_df = pd.concat([past_100_days, dataTesting], ignore_index=True)
            input_data = scaler.fit_transform(final_df)

            x_test = []
            y_test = []
            for i in range(100, input_data.shape[0]):
                x_test.append(input_data[i-100: i])
                y_test.append(input_data[i, 0])

            x_test, y_test = np.array(x_test), np.array(y_test)

            # Making Predictions
            y_predicted = model.predict(x_test)

            # Revert the scaled prices to origin price
            y_predicted = scaler.inverse_transform(y_predicted.reshape(-1, 1)).flatten() # -1, 1 means get all rows from the data
            y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten() 

            # Plot the final predictions
            plt.switch_backend('AGG')
            plt.figure(figsize=(12, 5))
            plt.plot(y_test,'b', label='Original Price')
            plt.plot(y_predicted, 'r', label='Predicted Price')
            plt.title(f'Final Prediction of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_img_path = f'{ticker}_final_prediction.png' 
            plot_prediction = save_plot(plot_img_path)

            # Model Evaluation 
            # Mean Squared Error (MSE) - To check wheather model is predicted correct or wrong?
            mse = mean_squared_error(y_test, y_predicted)

            # Root Mean Squared Error (RMSE)
            rmse = np.sqrt(mse)

            # R-Squared
            r2 = r2_score(y_test, y_predicted) # r square should be in between 0 & 1 and if  it is near means our prediction is very good

            return Response({
                'status': 'Success', 
                'plot_img': plot_img, 
                'plot_100_dma': plot_100_dma,
                'plot_200_dma' : plot_200_dma,
                'plot_prediction' : plot_prediction,
                'mse' : mse,
                'rmse' : rmse,
                'r2' : r2
            })