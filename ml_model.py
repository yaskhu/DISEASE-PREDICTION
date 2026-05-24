import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
import os

# Create models folder if not exists
os.makedirs('models', exist_ok=True)

# LOAD DATA
# Download from Kaggle: heart disease dataset
df = pd.read_csv('data/heart.csv')

# Check data
print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Missing values: {df.isnull().sum().sum()}")

# Separate features and target
X = df.drop('target', axis=1)  # All except target column
y = df['target']  # Target: 0 = no disease, 1 = disease

print(f"Classes: {y.value_counts().to_dict()}")

# TRAIN/TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# SCALE FEATURES (Important for RF but doesn't hurt)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# TRAIN MODEL with GridSearch for hyperparameter tuning
print("\n🔄 Training model...")
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5],
}

rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(rf, param_grid, cv=5, n_jobs=-1, verbose=1)
grid_search.fit(X_train_scaled, y_train)

best_model = grid_search.best_estimator_
print(f"✅ Best params: {grid_search.best_params_}")

# EVALUATE
train_acc = best_model.score(X_train_scaled, y_train)
test_acc = best_model.score(X_test_scaled, y_test)

print(f"\n📊 Training Accuracy: {train_acc:.4f}")
print(f"📊 Testing Accuracy: {test_acc:.4f}")

# FEATURE IMPORTANCE
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': best_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🎯 Top 5 Important Features:")
print(feature_importance.head())

# SAVE MODEL & SCALER
joblib.dump(best_model, 'models/disease_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(X.columns.tolist(), 'models/feature_names.pkl')

print("\n✅ Model saved to models/disease_model.pkl")
print("✅ Scaler saved to models/scaler.pkl")