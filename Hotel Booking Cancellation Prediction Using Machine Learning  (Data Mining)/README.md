# Hotel Booking Cancellation Prediction using Machine Learning

A machine learning-based hotel booking cancellation prediction system with an interactive Streamlit dashboard for business intelligence and cancellation risk analysis.

---

## Project Overview

This project predicts whether a hotel booking is likely to be cancelled using machine learning techniques. The system analyzes booking-related features such as lead time, ADR (Average Daily Rate), special requests, room types, market segment, and parking requirements to estimate cancellation probability.

The project also includes an interactive Streamlit dashboard for:
- Business analytics
- Cancellation risk prediction
- Revenue management insights
- Operational decision support

---

## Features

### Machine Learning Pipeline
- Data preprocessing and cleaning
- Feature engineering
- Missing value handling
- Outlier detection
- Categorical encoding
- Feature scaling
- Class imbalance handling using SMOTENC
- Model comparison and evaluation
- Hyperparameter tuning

### Interactive Dashboard
- KPI visualization
- Cancellation analytics
- Business intelligence graphs
- Real-time cancellation prediction
- Revenue management recommendations

### Prediction Outputs
The system classifies bookings into:
- Low Risk
- Moderate Risk
- High Risk

and provides recommended operational actions for hotel management.

---

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Imbalanced-learn
- Joblib

---

## Machine Learning Models

The project evaluates multiple classification models including:

- Logistic Regression
- Linear Support Vector Classifier (LinearSVC)
- Random Forest Classifier
- HistGradientBoosting Classifier

---

## Dataset

This project uses the **Hotel Booking Demand** dataset.

Dataset file:
```text
hotel_bookings.csv
```

Dataset source:  
https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand/data

After downloading, place the dataset inside the project folder.

---

## Project Structure

```text
hotel-booking-cancellation-prediction/
│
├── application.py
├── application_bundle.pkl
├── Code.ipynb
├── hotel_bookings.csv
├── README.md
└── screenshots/
```

---

## Dashboard Preview

Add screenshots of your dashboard inside the `screenshots/` folder.

Suggested screenshots:
- KPI dashboard
- Prediction result page
- Business intelligence graphs

---

## How to Run

### Run the Streamlit application

```bash
streamlit run application.py
```

---

## Prediction Features

The prediction system uses:
- Lead Time
- ADR (Average Daily Rate)
- Market Segment
- Room Types
- Special Requests
- Parking Requirements
- Arrival Week Information

to estimate booking cancellation probability.

---

## Business Intelligence Insights

The dashboard provides:
- Cancellation rate analysis
- Lead time vs ADR analysis
- Guest engagement analysis
- Revenue management recommendations

---

## License

This project is for educational and academic purposes.
