import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("19-08-2025/es_2/data/AirQualityUCI.csv", sep=";", decimal=",", low_memory=False)

# colonne non utili ai fini dell'analisi
df.drop(['Unnamed: 15', 'Unnamed: 16'], axis=1, inplace=True)

# Sostituisco i valori -200 con NaN e rimuovo le righe contenenti NaN
df = df.replace(-200, np.nan).dropna()

# Parsing corretto della colonna datetime (gg/mm/aaaa + HH.MM.SS)
df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H.%M.%S", errors="coerce")
df = df.dropna(subset=["Datetime"])


df["date"] = df["Datetime"].dt.date
df["hour"] = df["Datetime"].dt.hour
df["dayofweek"] = df["Datetime"].dt.dayofweek  # 0 = lunedì
df["week"] = df["Datetime"].dt.isocalendar().week
df["month"] = df["Datetime"].dt.month


pollutant = "NO2(GT)"  

# Calcolo soglia giornaliera: mediana (più robusta della media)
daily_median = df.groupby("date")[pollutant].transform("median")

# Target binario: 1=scarsa qualità, 0=buona qualità
df["target"] = (df[pollutant] > daily_median).astype(int)

features = ["hour", "dayofweek", "month"]
X = df[features]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

#random forest 
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

#valutazione
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=["Buona qualità", "Scarsa qualità"]))

# Matrice di confusione
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Buona", "Scarsa"],
            yticklabels=["Buona", "Scarsa"])
plt.title("Matrice di confusione")
plt.ylabel("Valori reali")
plt.xlabel("Predetti")
plt.show()

