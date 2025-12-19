# train.py (Run this FIRST)
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from xgboost import XGBRegressor 
from sklearn.metrics import mean_squared_error

def train():
    print("🚀 Starting Training Factory...")
    
    df = pd.read_csv('AB_NYC_2019.csv')
    
    df = df.drop(columns=['name', 'host_id', 'neighbourhood'], errors='ignore')
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
    df = df[(df['price'] < 500) & (df['price'] > 0)] # Remove outliers

    target = 'price'
    numeric_features = [
        'minimum_nights', 'number_of_reviews', 'reviews_per_month', 
        'calculated_host_listings_count', 'availability_365', 
        'latitude', 'longitude'
    ]
    categorical_features = ['neighbourhood_group', 'room_type']

    X = df[numeric_features + categorical_features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', XGBRegressor(random_state=42, objective='reg:squarederror'))
    ])

    param_grid = {
        'model__n_estimators': [50, 100, 150, 200],
        'model__learning_rate': [0.01, 0.05, 0.1],
        'model__max_depth': [3, 4, 6, 7, 8]
    }

    print("🔧 Tuning Hyperparameters (this might take a minute)...")
    search = GridSearchCV(
        pipeline, 
        param_grid, 
        cv=3, 
        scoring='neg_root_mean_squared_error',
        n_jobs=-1
    )
    search.fit(X_train, y_train)

    best_model = search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    
    print(f"✅ Training Complete!")
    print(f"🏆 Best RMSE: ${rmse:.2f}")

    joblib.dump(best_model, 'airbnb_best_model.joblib')
    print("💾 Model saved to 'airbnb_best_model.joblib'")

if __name__ == "__main__":
    train()