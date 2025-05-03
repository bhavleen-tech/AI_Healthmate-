import pandas as pd
from imblearn.over_sampling import SMOTE, RandomOverSampler # type: ignore
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier # type: ignore
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_selection import RFE
print("all libraries loaded")

# Load dataset
file_path = "Disease_symptom_and_patient_profile_dataset.csv"
df = pd.read_csv(file_path)

# Handle missing values
df = df.ffill()

# Ensure 'Disease' column is all strings
df['Disease'] = df['Disease'].astype(str)

# Encode categorical features into numerical values
label_encoders = {}
for col in df.columns:
    if df[col].dtype == 'object' and col != 'Disease':
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le  # Store encoder for inverse transformation if needed

# Define features (X) and target (y)
X = df.drop(columns=["Disease", "Outcome Variable"])  # Remove target & redundant columns
y = df["Disease"]

# Handle rare diseases (merge categories with <3 occurrences)
disease_counts = y.value_counts()
rare_diseases = disease_counts[disease_counts < 3].index
y = y.replace(rare_diseases, "Other")

# Encode the updated target variable
disease_encoder = LabelEncoder()
y = disease_encoder.fit_transform(y)

# Apply SMOTE with k_neighbors adjusted or use RandomOverSampler if needed
try:
    smote = SMOTE(k_neighbors=min(3, y.min()), random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
except ValueError:
    ros = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = ros.fit_resample(X, y)

# Split dataset into training & testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Feature Selection with Recursive Feature Elimination (RFE)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rfe = RFE(rf_model, n_features_to_select=10)
X_train = rfe.fit_transform(X_train, y_train)
X_test = rfe.transform(X_test)

# Hyperparameter tuning for Random Forest

# Train XGBoost model
xgb_model = XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=7, eval_metric='mlogloss')
xgb_model.fit(X_train, y_train)

# Train LightGBM model
lgb_model = LGBMClassifier(n_estimators=300, learning_rate=0.05, max_depth=7)
lgb_model.fit(X_train, y_train)


# Predictions using XGBoost
y_pred_xgb = xgb_model.predict(X_test)

# Predictions using LightGBM
y_pred_lgb = lgb_model.predict(X_test)

accuracy_xgb = accuracy_score(y_test, y_pred_xgb)
accuracy_lgb = accuracy_score(y_test, y_pred_lgb)

print(f"XGBoost Accuracy: {accuracy_xgb * 100:.2f}%")
print(f"LightGBM Accuracy: {accuracy_lgb * 100:.2f}%")


print("\nXGBoost Classification Report:\n", classification_report(y_test, y_pred_xgb))
print("\nLightGBM Classification Report:\n", classification_report(y_test, y_pred_lgb))

import pickle
with open("disease_prediction_model.pkl", "wb") as model_file:
    pickle.dump(lgb_model, model_file)

with open("label_encoders.pkl", "wb") as le_file:
    pickle.dump(label_encoders, le_file)

with open("disease_encoder.pkl", "wb") as de_file:
    pickle.dump(disease_encoder, de_file)
print("model uploaded")