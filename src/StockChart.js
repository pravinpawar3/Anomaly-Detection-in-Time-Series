import React from 'react';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

const StockChart = ({ stockData }) => {
  // Extract the necessary data for the chart
  const labels = stockData.actualtimeStamp || [];
  const prices = stockData.actualValues || [];
  const anomalytimeStamp = stockData.anomalytimeStamp || [];

  // Create the data array for the "Anomaly Detected" dataset
  const anomalyData = [];
  for (let i = 0; i < labels.length; i++) {
    if (anomalytimeStamp.includes(labels[i])) {
      anomalyData.push(prices[i]);
    } else {
      anomalyData.push(null);
    }
  }

  // Chart configuration
  const chartData = {
    labels: labels,
    datasets: [
      {
        label: 'Stock Price',
        data: prices,
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
      {
        label: 'Anomaly Detected',
        data: anomalyData,
        borderColor: 'red',
        pointStyle: 'circle',
        pointRadius: 5,
        pointBackgroundColor: 'red',
        fill: false,
      },
    ],
  };

  const chartOptions = {
    scales: {
      x: {
        type: 'category',
      },
    },
  };
  
  return <Line data={chartData} options={chartOptions} />;
};

export default StockChart;
