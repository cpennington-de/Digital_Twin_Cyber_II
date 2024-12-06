import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Step 1: Load the data
csv_file = '/Users/colinpennington/Documents/GitHub/Digital_Twin_Cyber_II/Digital Twin HW2/DTClassifier/dataset_full.csv'
data = pd.read_csv(csv_file)

# Step 2: Define dependent (y) and independent variables (X)
y = data['phishing']  # Replace with your target column name
X = data.drop(columns=['phishing'])  # Drop the target column from your independent variables

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 4: Initialize the model and perform RFE with a limit of 10 variables
model = LinearRegression()

# RFE: Recursive Feature Elimination with a set number of features
rfe = RFE(estimator=model, n_features_to_select=10)
rfe.fit(X_train, y_train)

# Step 5: Identify the selected features
selected_features = X.columns[rfe.support_]
print(f"Selected features: {list(selected_features)}")

# Step 6: Evaluate the final model
model.fit(X_train[selected_features], y_train)
r2_train = model.score(X_train[selected_features], y_train)
r2_test = model.score(X_test[selected_features], y_test)

print(f"R-squared on training set: {r2_train}")
print(f"R-squared on test set: {r2_test}")

# Step 7: Interpret feature importance
feature_importance = pd.DataFrame({
    'Feature': selected_features,
    'Coefficient': model.coef_
}).sort_values(by='Coefficient', key=abs, ascending=False)

print(feature_importance)
