import streamlit as st
import pandas as pd


df = pd.read_csv(r'train.csv', sep=';')

bins = [17, 25, 35, 45, 55, 100]
labels = ['18-25', '26-35', '36-45', '46-55', '56+']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)

total_clients = df.shape[0]
subscribed = df[df["y"]=="yes"].shape[0]
not_subscribed = df[df["y"]=="no"].shape[0]

subscribed_pct = round(100 * subscribed / total_clients, 1)
not_subscribed_pct = round(100 * not_subscribed / total_clients, 1)

avg_age = round(df["age"].mean(), 1)
avg_balance = round(df["balance"].mean(), 1)
avg_duration = round(df["duration"].mean(), 1)

housing_yes = df[df["housing"]=="yes"].shape[0]
housing_pct = round(100 * housing_yes / total_clients, 1)

loan_yes = df[df["loan"]=="yes"].shape[0]
loan_pct = round(100 * loan_yes / total_clients, 1)

default_yes = df[df["default"]=="yes"].shape[0]
default_pct = round(100 * default_yes / total_clients, 1)

age_group_counts = df.groupby("age_group")["age"].count()
most_populous_group = age_group_counts.idxmax()
least_populous_group = age_group_counts.idxmin()

median_balance = round(df["balance"].median(), 1)
median_age = round(df["age"].median(), 1)

st.title("📊 Анализ ключевых метрик")

# 1️⃣ Общее количество клиентов
st.header("1️⃣ Общее количество клиентов в датасете")
col1, col2, col3 = st.columns(3)
col1.metric("Всего клиентов", f"{total_clients}")
col2.metric("Подписались на депозит", f"{subscribed} ({subscribed_pct}%)")
col3.metric("Не подписались", f"{not_subscribed} ({not_subscribed_pct}%)")

st.markdown("---")

# 2️⃣ Средние показатели
st.header("2️⃣ Средние показатели")
col1, col2, col3 = st.columns(3)
col1.metric("Средний возраст", f"{avg_age} лет")
col2.metric("Средний баланс", f"{avg_balance}")
col3.metric("Средняя длительность звонка", f"{avg_duration} сек")

st.markdown("---")

# 3️⃣ Кредиты
st.header("3️⃣ Кредиты")
col1, col2, col3 = st.columns(3)
col1.metric("Ипотека", f"{housing_yes} ({housing_pct}%)")
col2.metric("Персональный кредит", f"{loan_yes} ({loan_pct}%)")
col3.metric("Дефолты", f"{default_yes} ({default_pct}%)")

st.markdown("---")

# 4️⃣ Возрастные группы
st.header("4️⃣ Возрастные группы")
col1, col2 = st.columns(2)
col1.metric("Самая многочисленная", most_populous_group)
col2.metric("Наименее многочисленная", least_populous_group)

