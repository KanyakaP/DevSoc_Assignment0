import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(
    'https://raw.githubusercontent.com/cronan03/DevSoc_AI-ML/main/train_processed_splitted.csv')
print(df.head())
print(df.columns)
print(df.describe())
numeric_df = df.select_dtypes(include='number')
df_encoded = pd.get_dummies(df, columns=['Utilities'])
numeric_features = df_encoded.select_dtypes(include='number')
train_min = numeric_features.min()
train_max = numeric_features.max()
df_normalized = (numeric_features - numeric_features.min()) / \
    (numeric_features.max() - numeric_features.min())
X = df_normalized.drop(columns=['SalePrice']).values
Y = df_normalized['SalePrice'].values

N, D = X.shape


rng = np.random.default_rng(seed=42)
w = rng.standard_normal(D)
b = rng.standard_normal()

y_pred_A = X.dot(w) + b

mse_A = np.mean((y_pred_A - Y)**2)

plt.figure(figsize=(6, 6))
plt.scatter(Y, y_pred_A, alpha=0.5)
plt.xlabel("Actual SalePrice")
plt.ylabel("Predicted SalePrice")
plt.title("Actual vs Predicted SalePrice")

plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--', lw=2)
plt.show()


def mse_loss(y_pred, y_true):
    loss = np.mean((y_pred - y_true) ** 2)
    return loss


N, D = X.shape
w = np.random.randn(D)
b = np.random.randn()


learning_rate = 0.01
epochs = 1000


for epoch in range(epochs):

    y_pred = X.dot(w) + b

    loss = np.mean((y_pred - Y) ** 2)

    dw = (2/N) * X.T.dot(y_pred - Y)
    db = (2/N) * np.sum(y_pred - Y)

    w -= learning_rate * dw
    b -= learning_rate * db

    if epoch % 100 == 0:
        print(f"Epoch {epoch}: Loss = {loss:.4f}")

print("\nFinal weights:", w[:5], "...")  # show first few weights
print("Final bias:", b)
plt.figure(figsize=(6, 6))
plt.scatter(Y, X.dot(w)+b, alpha=0.5, color='green')
plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--')
plt.xlabel("Actual SalePrice")
plt.ylabel("Predicted SalePrice")
plt.title("Trained Model: Actual vs Predicted")
plt.show()
df_test = pd.read_csv(
    'https://raw.githubusercontent.com/cronan03/DevSoc_AI-ML/main/test_processed_splitted.csv'
)

df_test = pd.get_dummies(df_test, columns=['Utilities'], dtype='int32')

train_features = df_encoded.drop(columns=['SalePrice'])

for col in train_features.columns:
    if col not in df_test.columns:
        df_test[col] = 0

df_test = df_test[train_features.columns]

df_test_normalized = (df_test - train_min.drop('SalePrice')) / (
    train_max.drop('SalePrice') - train_min.drop('SalePrice')
)
X_test = df_test_normalized.values.astype(float)
y_pred_test = X_test.dot(w) + b
saleprice_min = train_min['SalePrice']
saleprice_max = train_max['SalePrice']
y_pred_original = y_pred_test * (saleprice_max - saleprice_min) + saleprice_min
