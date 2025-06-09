import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Предполагается, что у вас уже загружен датафрейм df
df = pd.read_csv(r'train.csv', sep=';')
df = df.reset_index(drop=True)

st.title("Анализ подписок на депозит — Поведение и влияние факторов")

# Добавим колонку с возрастными группами
bins = [17, 25, 35, 45, 55, 100]
labels = ['18-25', '26-35', '36-45', '46-55', '56+']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)

# 1. Подписки на депозит по возрастным группам
st.header("Подписки на депозит по возрастным группам")
age_group_data = df.groupby(['age_group', 'y'], as_index=False)['age'].count().rename(columns={'age': 'Count'})

age_group_data['Percent'] = age_group_data.groupby('age_group')['Count'].transform(lambda x: round(100 * x / x.sum(), 1))

fig_age = px.bar(
    age_group_data,
    x='age_group',
    y='Percent',  # здесь — процент вместо количества
    color='y',
    barmode='group',
    text='Percent',  # это подписи
    labels={'y': 'Подписка на депозит', 'age_group': 'Возрастная группа'}
)
st.plotly_chart(fig_age, use_container_width=True)
st.markdown("""
- Самые активные группы — 18-25 и 26-35 лет.

- С возрастом склонность подписываться снижается.

- Клиенты 46+ лет менее склонны к подписке, возможно, из-за других финансовых приоритетов.
""")

# 2. Влияние ипотечного (housing) и персонального (loan) кредитов на подписки
st.header("Влияние ипотечного и персонального кредитов на подписки")
loan_data = df.groupby(['housing', 'loan', 'y'], as_index=False)['age'].count().rename(columns={'age': 'Count'})

fig_loan = px.bar(loan_data, x='housing', y='Count', color='y', barmode='group',
                  facet_col='loan', category_orders={"housing": ['no', 'yes'], "loan": ['no', 'yes']},
                  labels={'housing':'Ипотечный кредит', 'loan':'Персональный кредит', 'y':'Подписка'})
st.plotly_chart(fig_loan, use_container_width=True)

st.markdown("""
- Клиенты без ипотечного и персонального кредита более склонны подписываться.

- Наличие кредита уменьшает гибкость и возможности для вложений.
""")

# 3. Влияние баланса на подписку (boxplot)
st.header("Влияние баланса на подписку")
fig_balance = px.box(df, x='y', y='balance', points='all', color='y',
                     labels={'y': 'Подписка на депозит', 'balance': 'Баланс счета'},
                     title="Распределение баланса по подписке")
st.plotly_chart(fig_balance, use_container_width=True)
st.markdown("""- Средний баланс у клиентов с подпиской значительно выше.
- Подтверждает гипотезу: чем больше средств, тем выше вероятность вклада""")

# 4. Влияние длительности звонка на подписку (duration)
st.header("Влияние длительности последнего контакта")
fig_duration = px.box(df, x='y', y='duration', points='all', color='y',
                      labels={'y': 'Подписка на депозит', 'duration': 'Длительность последнего звонка (сек)'},
                      title="Длительность последнего контакта и подписка")
st.plotly_chart(fig_duration, use_container_width=True)
st.markdown("""
- Чем дольше длился звонок, тем выше шанс подписки.

- Длительность — явный индикатор интереса клиента.
""")

# 5. Влияние дня месяца последнего контакта
st.header("Влияние дня последнего контакта")
fig_day = px.box(df, x='y', y='day', points='all', color='y',
                 labels={'y': 'Подписка на депозит', 'day': 'День месяца последнего контакта'},
                 title="День последнего контакта и подписка")
st.plotly_chart(fig_day, use_container_width=True)
st.markdown("""- День месяца не оказывает заметного влияния на решение о подписке.

- Нет устойчивой зависимости между датой звонка и подпиской.""")

# 6. Кросс-таблицы и тепловые карты
st.header("Тепловые карты: пересечение профессии и семейного положения с подписками")

# job vs marital с подпиской
job_marital = pd.crosstab(index=df['job'], columns=[df['marital'], df['y']], normalize='index') * 100
job_marital = job_marital.reset_index()

fig_heatmap = px.imshow(job_marital.set_index('job').values,
                        labels=dict(x="Статус + Подписка", y="Профессия", color="% от профессии"),
                        x=job_marital.columns[1:], y=job_marital['job'],
                        color_continuous_scale='Viridis')
st.plotly_chart(fig_heatmap, use_container_width=True)
st.markdown("""
- Некоторые профессии более склонны к подписке, особенно в сочетании с семейным положением.

- Например, у married management подписка выше, чем у student single.
""")

# Можно добавить фильтры, чтобы выбирать возраст, наличие кредитов, диапазон баланса и смотреть изменение подписок

st.sidebar.header("Фильтры")
age_filter = st.sidebar.multiselect("Возрастные группы", options=labels, default=labels)
housing_filter = st.sidebar.multiselect("Ипотечный кредит", options=['yes', 'no'], default=['yes', 'no'])
loan_filter = st.sidebar.multiselect("Персональный кредит", options=['yes', 'no'], default=['yes', 'no'])
deposit_filter = st.sidebar.selectbox("Подписка на депозит", options=['все', 'да', 'нет'], index=0)

df_filtered = df[df['age_group'].isin(age_filter) & 
                 df['housing'].isin(housing_filter) & 
                 df['loan'].isin(loan_filter)]

if deposit_filter != 'все':
    y_val = 'yes' if deposit_filter == 'да' else 'no'
    df_filtered = df_filtered[df_filtered['y'] == y_val]

st.markdown(f"**Отфильтровано записей: {len(df_filtered)}**")

# Повторим, например, график подписок по возрастным группам для отфильтрованных данных
age_group_data_f = df_filtered.groupby(['age_group', 'y'], as_index=False)['age'].count().rename(columns={'age': 'Count'})
age_group_data_f['Percent'] = age_group_data_f.groupby('age_group')['Count'].transform(lambda x: round(100 * x / x.sum(), 1))

fig_age_f = px.bar(age_group_data_f, x='age_group', y='Percent', color='y', barmode='group', text='Percent')
st.plotly_chart(fig_age_f, use_container_width=True)


st.markdown("""
#### Выводы 
            
- Основные драйверы подписки — возраст, баланс и длительность звонка.

- Наличие кредитов и профессия также важны, но второстепенно.

""")
