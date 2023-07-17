import React, { useState } from 'react';
import axios from 'axios';
import './Dashboard.css';
import StockChart from './StockChart';

const Dashboard = () => {
  const [loading, setLoading] = useState(false);
  const [stockData, setStockData] = useState({ date: [], price: [] },);
  const [trainStartDate, setTrainStartDate] = useState('');
  const [trainEndDate, setTrainEndDate] = useState('');
  const [symbolInput, setSymbolInput] = useState('');
  const [testStartDate, setTestStartDate] = useState('');
  const [testEndDate, setTestEndDate] = useState('');
  const [trainingCompleted, setPostTrainContent] = useState(false);
  const [predictionCompleted, setPostTestContent] = useState(false);

  const TrainModel = async () => {
    try {
      setLoading(true);
      setPostTrainContent(false);
      const response = await axios.post('http://127.0.0.1:5000/train', {
        symbol: symbolInput,
        start_date: trainStartDate,
        end_date: trainEndDate,
      });
      setPostTrainContent(true);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const runAlgorithm = async () => {
    try {
      setLoading(true);
      setPostTestContent(false);
      const response = await axios.post('http://127.0.0.1:5000/predict', {
        symbol: symbolInput,
        start_date: testStartDate,
        end_date: testEndDate,
      });
      setStockData(response.data);
      setPostTestContent(true);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleTestEdDateChange = (event) => {
    setTestEndDate(event.target.value);
  };

  const handleTestStDateChange = (event) => {
    setTestStartDate(event.target.value);
  };

  const handleTrainStDateChange = (event) => {
    setTrainStartDate(event.target.value);
  };

  const handleTrainEdDateChange = (event) => {
    setTrainEndDate(event.target.value);
  };

  const handleSymbolChange = (event) => {
    setSymbolInput(event.target.value);
  };

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Anomaly Detection Dashboard</h1>
      <div className="dashboard-buttons">
        <div className="dashboard-row">
          <div>
            <label >Symbol:</label>
            <input type="text" value={symbolInput} onChange={handleSymbolChange} />
          </div>
        </div>
        <br />
        <div className="dashboard-row">
          <div>
            <label>Start Date:</label>
            <input type="text" value={trainStartDate} onChange={handleTrainStDateChange} />
          </div>
          <div>
            <label>End Date:</label>
            <input type="text" value={trainEndDate} onChange={handleTrainEdDateChange} />
          </div>
          <button disabled={loading} onClick={TrainModel} className="dashboard-button">
            Train Model
          </button>
          {trainingCompleted && (
            <div style={{ margin: 10 }}>
              <label>Model training is Completed!</label>
            </div>
          )}
        </div>
        <br />
        <div className="dashboard-row">
          <div>
            <label>Start Date:</label>
            <input type="text" value={testStartDate} onChange={handleTestStDateChange} />
          </div>
          <div>
            <label>End Date:</label>
            <input type="text" value={testEndDate} onChange={handleTestEdDateChange} />
          </div>
          <button disabled={loading} onClick={runAlgorithm} className="dashboard-button">
            Predict Anomaly
          </button>
          {predictionCompleted && (
            <div style={{ margin: 10 }}>
              <label>Model prediction is Completed!</label>
            </div>
          )}
        </div>
      </div>
      <div>
        <h1>Stock Chart</h1>
        <StockChart stockData={stockData} />
      </div>
      {loading && <p>Loading...</p>}
    </div>

  );
};

export default Dashboard;
