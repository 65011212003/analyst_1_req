"""
Machine Learning & AI Examples
Demonstrates: Scikit-learn, data preprocessing, model training, evaluation
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

class EmployeeMLAnalyzer:
    """
    Machine Learning examples for employee data analysis
    Demonstrates: Classification, Regression, Model Evaluation
    """
    
    def __init__(self):
        self.data = None
        self.models = {}
        self.scalers = {}
    
    def create_sample_dataset(self):
        """Create synthetic employee dataset for ML"""
        np.random.seed(42)
        n_samples = 500
        
        # Generate features
        years_experience = np.random.randint(0, 25, n_samples)
        education_level = np.random.choice(['Bachelor', 'Master', 'PhD'], n_samples, p=[0.6, 0.3, 0.1])
        performance_score = np.random.uniform(2.5, 5.0, n_samples)
        projects_completed = np.random.randint(0, 50, n_samples)
        department = np.random.choice(['IT', 'HR', 'Finance', 'Marketing'], n_samples)
        
        # Target: Salary (regression)
        # Formula: base salary + experience bonus + performance bonus + education bonus
        base_salary = 50000
        salary = (
            base_salary +
            (years_experience * 3000) +
            (performance_score * 5000) +
            (projects_completed * 500) +
            np.random.normal(0, 5000, n_samples)  # Random variation
        )
        
        # Additional binary features
        high_performer = performance_score > 4.0
        promoted = (years_experience > 5) & (performance_score > 4.0)
        
        # Target: Attrition (classification)
        # Employees more likely to leave if low salary relative to experience
        attrition_probability = 1 / (1 + np.exp((salary - 70000 - years_experience * 2000) / 10000))
        attrition = np.random.random(n_samples) < attrition_probability
        
        self.data = pd.DataFrame({
            'years_experience': years_experience,
            'education': education_level,
            'performance_score': performance_score,
            'projects_completed': projects_completed,
            'department': department,
            'salary': salary,
            'high_performer': high_performer,
            'promoted': promoted,
            'attrition': attrition
        })
        
        print(f"✓ Created dataset with {len(self.data)} employees")
        print(f"\nDataset Preview:")
        print(self.data.head())
        print(f"\nDataset Info:")
        print(self.data.describe())
        
        return self.data
    
    def regression_example(self):
        """
        Regression Example: Predict employee salary
        Demonstrates: Feature engineering, model training, evaluation
        """
        print("\n" + "=" * 60)
        print("REGRESSION: Predicting Employee Salary")
        print("=" * 60)
        
        # Prepare features
        # Encode categorical variables
        le_education = LabelEncoder()
        le_department = LabelEncoder()
        
        X = self.data.copy()
        X['education_encoded'] = le_education.fit_transform(X['education'])
        X['department_encoded'] = le_department.fit_transform(X['department'])
        
        # Select features for model
        feature_columns = ['years_experience', 'education_encoded', 'performance_score', 
                          'projects_completed', 'department_encoded']
        X = X[feature_columns]
        y = self.data['salary']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print("\n1. Linear Regression")
        print("-" * 40)
        
        # Train Linear Regression
        lr_model = LinearRegression()
        lr_model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred_lr = lr_model.predict(X_test_scaled)
        
        # Evaluation
        mse_lr = mean_squared_error(y_test, y_pred_lr)
        r2_lr = r2_score(y_test, y_pred_lr)
        
        print(f"Mean Squared Error: ${mse_lr:,.2f}")
        print(f"R² Score: {r2_lr:.4f}")
        print(f"Root Mean Squared Error: ${np.sqrt(mse_lr):,.2f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_columns,
            'coefficient': lr_model.coef_
        }).sort_values('coefficient', ascending=False)
        
        print(f"\nFeature Coefficients:")
        print(feature_importance)
        
        print("\n2. Random Forest Regression")
        print("-" * 40)
        
        # Train Random Forest
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_reg = GradientBoostingRegressor(n_estimators=100, random_state=42)
        rf_reg.fit(X_train, y_train)
        
        # Predictions
        y_pred_rf = rf_reg.predict(X_test)
        
        # Evaluation
        mse_rf = mean_squared_error(y_test, y_pred_rf)
        r2_rf = r2_score(y_test, y_pred_rf)
        
        print(f"Mean Squared Error: ${mse_rf:,.2f}")
        print(f"R² Score: {r2_rf:.4f}")
        print(f"Root Mean Squared Error: ${np.sqrt(mse_rf):,.2f}")
        
        # Feature importance
        feature_importance_rf = pd.DataFrame({
            'feature': feature_columns,
            'importance': rf_reg.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\nFeature Importance:")
        print(feature_importance_rf)
        
        # Save models
        self.models['salary_predictor_lr'] = lr_model
        self.models['salary_predictor_rf'] = rf_reg
        self.scalers['salary_scaler'] = scaler
        
        return lr_model, rf_reg
    
    def classification_example(self):
        """
        Classification Example: Predict employee attrition
        Demonstrates: Binary classification, model comparison
        """
        print("\n" + "=" * 60)
        print("CLASSIFICATION: Predicting Employee Attrition")
        print("=" * 60)
        
        # Prepare features
        le_education = LabelEncoder()
        le_department = LabelEncoder()
        
        X = self.data.copy()
        X['education_encoded'] = le_education.fit_transform(X['education'])
        X['department_encoded'] = le_department.fit_transform(X['department'])
        
        feature_columns = ['years_experience', 'education_encoded', 'performance_score', 
                          'projects_completed', 'salary', 'department_encoded']
        X = X[feature_columns]
        y = self.data['attrition'].astype(int)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print(f"\nDataset: {len(X_train)} training, {len(X_test)} test samples")
        print(f"Attrition rate: {y.mean():.2%}")
        
        models = {
            'Logistic Regression': LogisticRegression(random_state=42),
            'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=5),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
        }
        
        for name, model in models.items():
            print(f"\n{name}")
            print("-" * 40)
            
            # Train
            model.fit(X_train_scaled, y_train)
            
            # Predict
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
            
            # Evaluate
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"Accuracy: {accuracy:.4f}")
            print(f"\nClassification Report:")
            print(classification_report(y_test, y_pred, target_names=['Stay', 'Leave']))
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
            print(f"Cross-validation scores: {cv_scores}")
            print(f"Average CV score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
            
            # Save best model
            if name == 'Random Forest':
                self.models['attrition_predictor'] = model
                self.scalers['attrition_scaler'] = scaler
        
        return models
    
    def predict_new_employee(self, employee_data):
        """
        Predict salary and attrition for a new employee
        Demonstrates: Using trained models for predictions
        """
        print("\n" + "=" * 60)
        print("PREDICTION: New Employee Analysis")
        print("=" * 60)
        
        print(f"\nEmployee Data:")
        for key, value in employee_data.items():
            print(f"  {key}: {value}")
        
        # Encode categorical variables
        education_map = {'Bachelor': 0, 'Master': 1, 'PhD': 2}
        department_map = {'IT': 0, 'HR': 1, 'Finance': 2, 'Marketing': 3}
        
        # Prepare features for salary prediction
        features_salary = np.array([[
            employee_data['years_experience'],
            education_map[employee_data['education']],
            employee_data['performance_score'],
            employee_data['projects_completed'],
            department_map[employee_data['department']]
        ]])
        
        # Scale features
        features_salary_scaled = self.scalers['salary_scaler'].transform(features_salary)
        
        # Predict salary
        predicted_salary_lr = self.models['salary_predictor_lr'].predict(features_salary_scaled)[0]
        predicted_salary_rf = self.models['salary_predictor_rf'].predict(features_salary)[0]
        
        print(f"\n📊 Salary Predictions:")
        print(f"  Linear Regression: ${predicted_salary_lr:,.2f}")
        print(f"  Random Forest: ${predicted_salary_rf:,.2f}")
        print(f"  Average Prediction: ${(predicted_salary_lr + predicted_salary_rf) / 2:,.2f}")
        
        # Prepare features for attrition prediction (includes salary)
        features_attrition = np.array([[
            employee_data['years_experience'],
            education_map[employee_data['education']],
            employee_data['performance_score'],
            employee_data['projects_completed'],
            predicted_salary_rf,  # Use predicted salary
            department_map[employee_data['department']]
        ]])
        
        features_attrition_scaled = self.scalers['attrition_scaler'].transform(features_attrition)
        
        # Predict attrition
        attrition_prob = self.models['attrition_predictor'].predict_proba(features_attrition_scaled)[0, 1]
        attrition_prediction = self.models['attrition_predictor'].predict(features_attrition_scaled)[0]
        
        print(f"\n🎯 Attrition Risk:")
        print(f"  Probability of leaving: {attrition_prob:.2%}")
        print(f"  Prediction: {'HIGH RISK' if attrition_prediction == 1 else 'LOW RISK'}")
        
        if attrition_prob > 0.7:
            print(f"  ⚠️ Recommendation: Implement retention strategies")
        elif attrition_prob > 0.4:
            print(f"  ⚠️ Recommendation: Monitor employee satisfaction")
        else:
            print(f"  ✓ Recommendation: Continue current engagement")

def demonstrate_ml_pipeline():
    """Complete machine learning pipeline demonstration"""
    print("\n" + "=" * 60)
    print("MACHINE LEARNING & AI DEMONSTRATION")
    print("Employee Analytics with Scikit-learn")
    print("=" * 60)
    
    analyzer = EmployeeMLAnalyzer()
    
    # Step 1: Create dataset
    analyzer.create_sample_dataset()
    
    # Step 2: Regression example
    analyzer.regression_example()
    
    # Step 3: Classification example
    analyzer.classification_example()
    
    # Step 4: Predict for new employee
    new_employee = {
        'years_experience': 7,
        'education': 'Master',
        'performance_score': 4.2,
        'projects_completed': 25,
        'department': 'IT'
    }
    
    analyzer.predict_new_employee(new_employee)
    
    print("\n" + "=" * 60)
    print("✓ Machine Learning demonstration completed!")
    print("=" * 60)

if __name__ == "__main__":
    demonstrate_ml_pipeline()
