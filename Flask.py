from flask import Flask, request, jsonify
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras.layers import Dense, LSTM, Dropout, RepeatVector, TimeDistributed
import numpy as np
import pandas as pd
import yfinance as yf
import pickle
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 

model = None
threshold = 0

def load_data(stock_symbol, start_date, end_date):
    # Fetch stock data from Yahoo Finance API
    stock_data = yf.download(stock_symbol, start_date, end_date)
    data = []
    data.append([str(x.date()) for x in stock_data['Close'].index])
    data.append(stock_data['Close'].values)
    return data

def sequence_data(X,ts):
    # Generate batch of sequence data
    X_seq, y_seq = [], []
    for i in range(len(X)-ts):
        X_seq.append(X.iloc[i:(i+ts)].values)
        y_seq.append(X.iloc[i+ts])
    return np.array(X_seq), np.array(y_seq)

def createModel(x, y):
    # Create auto-regressive model using LSTM layers
    model = Sequential()
    model.add(LSTM(128, input_shape=(x,y)))
    model.add(Dropout(rate=0.5))
    model.add(RepeatVector(x))
    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(rate=0.5))
    model.add(TimeDistributed(Dense(y)))
    model.compile(optimizer='adam', loss='mae')
    return model

@app.route('/train', methods=['POST'])
def train():
    global model
    global threshold
    # Get the input values from the request
    data = request.get_json()
    symbol = data.get('symbol')
    start_date = data.get('start_date')
    end_date = data.get('end_date')


    # Use the input values in your code
    data = load_data(symbol, start_date, end_date)
    #data =  load_data('GME', '2002-04-04', '2017-12-31')
    
    train_data = pd.DataFrame({'timeStamp':data[0], 'closePrices':data[1]})

    # Scale the input sequence
    scaler = StandardScaler()
    scaler = scaler.fit(train_data[['closePrices']])
    train_data['closePrices'] = scaler.transform(train_data[['closePrices']])
    X_train, y_train = sequence_data(train_data[['closePrices']], 60)
    
    # Build and train model
    model = createModel(X_train.shape[1],1)
    his = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2,
                callbacks=[keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, mode='min')], shuffle=False)
    
    # Save the trained model and any other necessary artifacts
    model.save('anomaly_detection_model.h5')
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    X_train_pred = model.predict(X_train, verbose=0)
    train_loss = np.mean(np.abs(X_train_pred - X_train), axis=1)
    threshold = np.max(train_loss+0.5)
    return jsonify({'message': 'Model trained successfully'})

def getAccuracy(anomaly_start_date, anomaly_end_date, result_df):
    result_df['True Anomaly'] = False  # Initialize the 'true anomaly' column

    # Set 'true anomaly' values for the desired date range
    result_df.loc[(result_df['timeStamp'] >= anomaly_start_date) & (result_df['timeStamp'] <= anomaly_end_date), 'True Anomaly'] = True
    # Assuming 'result_df' has been created as mentioned earlier
    true_anomalies = result_df[result_df['True Anomaly']]
    predicted_anomalies = result_df[result_df['Anomaly']]

    # Calculate the number of correctly predicted anomalies
    correctly_predicted = len(predicted_anomalies[predicted_anomalies['True Anomaly']])

    # Calculate the total number of actual anomalies
    total_actual_anomalies = min(1, len(true_anomalies))

    # Calculate the accuracy
    accuracy = min(1,correctly_predicted / total_actual_anomalies)

    return accuracy

@app.route('/predict', methods=['POST'])
def predict():
    global model
    global threshold
    # Get the input values from the request
    data = request.get_json()
    symbol = data.get('symbol')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    # Use the input values in your code
    input_data = load_data(symbol, start_date, end_date)
    #input_data = load_data('GME', '2018-01-03', '2021-04-28')

    # Load the trained model
    if model is None:
        model = load_model('anomaly_detection_model.h5')

    # Perform data preprocessing and model prediction here
    test_data = pd.DataFrame({'timeStamp':input_data[0], 'closePrices':input_data[1]})

    # Scale the input sequence
    scaler = StandardScaler()
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    test_data['closePrices_scale'] = scaler.transform(test_data[['closePrices']])
    X_test, y_test= sequence_data(test_data[['closePrices_scale']], 60)

    # Perform prediction
    X_test_pred = model.predict(X_test, verbose=0)
    anomaly_scores = np.mean(np.abs(X_test_pred-X_test), axis=1)
    
    result_df = pd.DataFrame(test_data[60:])
    result_df['Anomaly'] = anomaly_scores > threshold
    result_df['Close'] = test_data[60:].closePrices
    anomalies_df = result_df.loc[result_df.Anomaly]
    
    trueAnomaly = data.get('true_anomaly')
    anomaly_start_date = data.get('anomaly_start_date')
    anomaly_end_date = data.get('anomaly_end_date')
    
    accuracy = 'NA'
    if trueAnomaly:
        accuracy = getAccuracy(anomaly_start_date, anomaly_end_date, result_df)

    return jsonify({ 
     'actualValues': result_df.Close.astype(int).tolist(),
     'anomalytimeStamp': anomalies_df.timeStamp.tolist(),
     'actualtimeStamp': result_df.timeStamp.tolist(),
     'accuracy': accuracy})

@app.route('/display', methods=['GET'])
def display():
    return "Welcome!"

if __name__ == '__main__':
    # For debug
    app.run(debug=False)
