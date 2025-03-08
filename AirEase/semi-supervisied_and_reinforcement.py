# Import necessary libraries for adaptive and semi-supervised learning
from sklearn.ensemble import RandomForestClassifier
from sklearn.semi_supervised import SelfTrainingClassifier

# Generate partially labeled synthetic dataset (semi-supervised learning)
num_labeled = int(0.5 * num_samples)  # 50% labeled data
num_unlabeled = num_samples - num_labeled  # Remaining are unlabeled

# Create a mask: -1 indicates unlabeled data
labels = np.copy(user_activations)
labels[num_labeled:] = -1  # Mark 50% of the dataset as unlabeled

# Train an adaptive learning model using RandomForest inside a semi-supervised Self-Training classifier
base_model = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
semi_supervised_model = SelfTrainingClassifier(base_model, threshold=0.8)

# Fit the model using partially labeled data
semi_supervised_model.fit(X, labels)

# Predict and evaluate on labeled test data
y_pred_semi = semi_supervised_model.predict(X_test[:num_labeled])
semi_supervised_accuracy = accuracy_score(y_test[:num_labeled], y_pred_semi)

# Save the semi-supervised model
joblib.dump(semi_supervised_model, "semi_supervised_adaptive_airflow_model.pkl")

# Display new accuracy
semi_supervised_accuracy
