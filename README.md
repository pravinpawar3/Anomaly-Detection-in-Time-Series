# Alpha Detector: Steep Bull/Bear Trends (Anomaly) Detection in Stock Prices using LSTM-based Autoencoder

This project implements anomaly detection in stock price data using an LSTM-based Autoencoder model. The system is designed to be deployed with a **React Dashboard** on the frontend and a **Flask** API backend. It identifies unusual price movements (anomalies) in real-time and displays them on an interactive web dashboard.

![image](https://github.com/user-attachments/assets/4221b882-f5dc-4d62-9065-b818d164dece)

<img width="1472" alt="Anomaly" src="https://github.com/pravinpawar3/Anomaly-Detection-in-Time-Series/assets/23742943/8357adfd-5ec3-4654-b041-3ef47b746631">

<img width="950" alt="Screenshot 2023-01-19 at 5 40 52 PM" src="https://user-images.githubusercontent.com/23742943/213578357-db5b000c-2305-4470-b27c-2806a9605c2a.png">


---

## Project Structure

- **Backend (Flask)**: Handles data processing, training the LSTM model, and providing API endpoints for anomaly detection.
- **Frontend (React)**: Displays the detected anomalies and allows users to visualize stock price movements.
- **Autoencoder Model**: Uses an LSTM Autoencoder for anomaly detection, trained on historical stock price data.

---

## Prerequisites

Before running this project, make sure you have the following installed on your machine:

- Python 3.8+: Required for running the Flask backend and training the model.
- Node.js: Needed to run the React frontend.
- React: A JavaScript library for building the user interface.
- pip: Python package manager to install Python dependencies.
- npm: Node package manager to install frontend dependencies.

Installation Links:
- Download Python: https://www.python.org/downloads/
- Download Node.js: https://nodejs.org/

---

## Backend Setup (Flask)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/stock-price-anomaly-detection.git
   cd stock-price-anomaly-detection
   ```

2. **Install Python dependencies:**

   Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Flask API:**

   The Flask app runs an API that interacts with the trained LSTM Autoencoder model to detect anomalies. You can modify the `flask_app.py` file for custom routes or other configurations.

4. **Start the Flask app:**

   Navigate to the backend directory and run the Flask server:

   ```bash
   python Flask.py
   ```

   The Flask server should now be running on `http://localhost:5000`.

## Frontend Setup (React)

5. **Install React dependencies:**

   Navigate to the `frontend` directory and install the required React dependencies:

   ```bash
   cd src
   npm install
   ```

6. **Start the React development server:**

   Run the following command to start the React app:

   ```bash
   npm start
   ```

   The React app should now be accessible at `http://localhost:3000`.

---

## Model Explanation

### LSTM-based Autoencoder

The core of the anomaly detection process uses an LSTM (Long Short-Term Memory) Autoencoder. This model is designed to reconstruct the input stock price time series data. When an anomaly occurs, the reconstruction error will be significantly higher than usual, indicating that the data point is an anomaly.

- **Autoencoder Architecture**: 
    - Encoder: LSTM layers that capture the temporal patterns of stock price data.
    - Decoder: LSTM layers that reconstruct the input sequence.
    - The reconstruction error is used to flag anomalies.

- **Modelling**:
    - Historical stock price data from Yahoo Finance is used to train the LSTM Autoencoder, allowing the model to learn patterns in stock prices and detect anomalies in the test set by identifying deviations from these patterns.
---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

