# Hotel Booking Cancellation Prediction using Machine Learning

This project predicts whether a hotel booking is likely to be cancelled using machine learning techniques. The notebook covers data exploration, preprocessing, feature engineering, class imbalance handling, model training, hyperparameter tuning, and final prediction logic.

## Project Overview

Hotel booking cancellations can affect hotel revenue, room planning, and customer management. This project uses historical hotel booking data to build a classification model that predicts booking cancellation status.

## Features

- Data loading and initial exploration
- Missing value handling
- Duplicate removal
- Outlier detection and removal
- Feature engineering
- Categorical encoding
- Feature scaling
- Class imbalance handling using SMOTENC
- Baseline model comparison
- Hyperparameter tuning
- Final model evaluation
- Feature importance analysis
- Simple user-input prediction flow

## Machine Learning Models Used

The notebook compares several classification models, including:

- Logistic Regression
- Linear Support Vector Classifier
- Random Forest Classifier
- HistGradientBoosting Classifier

The stronger models are further tuned using randomized search.

## Tech Stack

- Python
- Jupyter Notebook
- pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Imbalanced-learn
- SciPy

## Dataset

This project included a dataset named:

```text
hotel_bookings.csv
or downloaded via :
https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand/data
```

## How to Run
Open the notebook:

```bash
jupyter notebook notebooks/hotel_booking_cancellation_prediction.ipynb
```

4. Add the dataset file `hotel_bookings.csv` and run the notebook cells from top to bottom.

## Results

The notebook evaluates models using metrics such as:

- Accuracy
- AUC
- Recall
- F1-score

Update this section with your final model performance after running the notebook.

Example:

```text
Best Model: HistGradientBoosting Classifier
Accuracy: 0.84
AUC: 0.90
Recall: 0.68
F1-score: 0.70
```
