import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('19-08-2025/PJME_hourly.csv')

# Conversione Datetime
df["Datetime"] = pd.to_datetime(df["Datetime"])
df["date"] = df["Datetime"].dt.date
df["week"] = df["Datetime"].dt.isocalendar().week
df["year"] = df["Datetime"].dt.year

#  Media giornaliera 
daily_means = df.groupby("date")["PJME_MW"].transform("mean")
df["consumo_giornaliero"] = pd.Series(
    pd.Categorical(
        ["alto consumo" if val else "basso consumo" for val in (df["PJME_MW"] >= daily_means)]
    )
)

# Media settimanale 
weekly_means = df.groupby(["year", "week"])["PJME_MW"].transform("mean")
df["consumo_settimanale"] = pd.Series(
    pd.Categorical(
        ["alto consumo" if val else "basso consumo" for val in (df["PJME_MW"] >= weekly_means)]
    )
)

print(df.head(10))


# Lineplot giornaliero 
giorno = "2002-12-31"
subset = df[df["date"] == pd.to_datetime(giorno).date()]

plt.figure(figsize=(14,6))
sns.lineplot(data=subset, x="Datetime", y="PJME_MW", 
             hue="consumo_giornaliero", 
             palette={"alto consumo":"red", "basso consumo":"blue"}, linewidth=2)
plt.title(f"Andamento consumo orario - {giorno}")
plt.ylabel("MW")
plt.xlabel("Ora")
plt.show()

# Boxplot per ora del giorno 
df["hour"] = df["Datetime"].dt.hour

plt.figure(figsize=(14,6))
sns.boxplot(data=df, x="hour", y="PJME_MW", palette="Set3")
plt.title("Distribuzione consumi per ora del giorno")
plt.ylabel("MW")
plt.xlabel("Ora del giorno")
plt.show()


df["hour"] = df["Datetime"].dt.hour
df["weekday"] = df["Datetime"].dt.day_name()  

order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# media dei consumi per ogni (giorno, ora)
pivot_table = df.pivot_table(index="weekday", columns="hour", values="PJME_MW", aggfunc="mean")
pivot_table = pivot_table.reindex(order)  # riordina i giorni

# Plot heatmap
plt.figure(figsize=(14,6))
sns.heatmap(pivot_table, cmap="coolwarm", annot=False, cbar_kws={'label': 'Consumo medio (MW)'})
plt.title("Heatmap settimanale dei consumi orari")
plt.xlabel("Ora del giorno")
plt.ylabel("Giorno della settimana")
plt.show()