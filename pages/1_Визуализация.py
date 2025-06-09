import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
fig = make_subplots(rows=1, cols=3)


# Загрузи данные
df = pd.read_csv(r'train.csv', sep=';')

# ctgrs = [col.value_counts().reset_index() for col in df.columns]

arr = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing',
       'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays',
       'previous', 'poutcome', 'y']

df_marital_counts = df['marital'].value_counts().reset_index()
df_marital_counts.columns = ['Marital-Status', 'Count']
df_education_counts = df['education'].value_counts().reset_index()
df_education_counts.columns = ['Education', 'Count']
df_default_counts = df['default'].value_counts().reset_index()
df_default_counts.columns = ['Default', 'Count']
df_loan_counts = df['loan'].value_counts().reset_index()
df_loan_counts.columns = ['Loan', 'Count']
df_housing_counts = df['housing'].value_counts().reset_index()
df_housing_counts.columns = ['Housing', 'Count']
df_poutcome_counts = df['poutcome'].value_counts().reset_index()
df_poutcome_counts.columns = ['Poutcome', 'Count']
df_previous_counts = df['previous'].value_counts().reset_index()
df_previous_counts.columns = ['Previous', 'Count']
df_contact_counts = df['contact'].value_counts().reset_index()
df_contact_counts.columns = ['Contact', 'Count']
df_month_counts = df['month'].value_counts().reset_index()
df_month_counts.columns = ['Month', 'Count']


st.title("📊 Маркетинговый анализ банка")

# Sidebar - выбор анализа
analysis_type = st.sidebar.selectbox(
    "Выберите тип анализа:",
    [
        "Распределение по возрасту",
        "Анализ по типу работы",
        "Семейное положение",
        "Образование",
        "Кредиты & займы",
        "Тип контакта",
        "Месяц контакта",
        "Результат предыдущей кампании",
        "Влияние предыдущих кампаний",
        "Средний баланс по профессиям",
        "Подписки на депозит по месяцам",
        "Распределение возраста по образованию",
        "Распределение возраста по семейному положению",
        "Роль ипотечного и персонального кредита в подписках",
        "Подписки по возрастным группам",
        "Распределение housing, personal loan и default",
        "Баланс и подписки на депозит",
        "Длительность звонка и подписки",
        "Heatmap профессия vs семейное положение"
        # "Term Deposits vs Previous Campaign Outcome",
        # "Deposits by Month",
    ]
)

if analysis_type == "Распределение по возрасту":
    st.header("Распределение возраста клиентов с разбивкой по подписке на вклад")
    fig = px.histogram(
        df,
        x="age",
        color="y",  # разбивка по подписке yes/no
        nbins=30,
        barmode='overlay',
        opacity=0.7,
        color_discrete_map={"yes": "limegreen", "no": "lightgray"},
        labels={'y': 'Подписка на вклад'},
        category_orders={"y": ["no", "yes"]},
    )

    mean_age = df["age"].mean()
    fig.add_vline(
        x=mean_age,
        line_dash="dash",
        line_color="black",
        annotation_text=f"Средний возраст: {round(mean_age, 2)}",
        annotation_position="top right"
    )

    fig.update_layout(
        legend_title_text='Подписка',
        legend=dict(
            y=0.95,
            x=0.75,
            bgcolor='rgba(255,255,255,0.7)',
            bordercolor='Black',
            borderwidth=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    **Insight 📊:**  
    - Средний возраст клиентов: **{round(mean_age, 2)}** лет.  
    - Наибольшая активность подписки наблюдается у клиентов от 30 до 55 лет.
    - Клиенты младше 30 и старше 60 реже подписываются.
    - Молодые люди более осторожны с долгосрочными вкладами.
    """)

elif analysis_type == "Анализ по типу работы":
    st.header("Распределение клиентов по типу работы")

    # Подсчет количества по типу работы и подписке
    job_subscribe_counts = df.groupby(
        ['job', 'y']).size().reset_index(name='Count')

    # Построение графика с разбивкой по подписке (y)
    fig = px.bar(
        job_subscribe_counts,
        x='job',
        y='Count',
        color='y',
        barmode='group',
        text='Count',
        color_discrete_map={"yes": "limegreen", "no": "lightgray"},
        category_orders={"y": ["no", "yes"]},
        labels={'y': 'Подписка на вклад', 'job': 'Тип работы'},
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title='Тип работы',
        yaxis_title='Количество клиентов',
        legend_title_text='Подписка на вклад',
        legend=dict(
            y=0.95,
            x=0.75,
            bgcolor='rgba(255,255,255,0.7)',
            bordercolor='Black',
            borderwidth=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insight 📊:**  
    - Больше всего клиентов в категориях blue-collar и management.
    - Высокая доля подписавшихся в management, technician и entrepreneur.
    - Группы с низкой активностью: student и housemaid.
    - Стоит обратить внимание на профессии с высокой подпиской — там потенциал для роста.
    """)

elif analysis_type == "Семейное положение":
    st.header("Анализ семейного положения клиентов")

    # Подсчет количества по семейному положению
    df_marital_counts = df['marital'].value_counts().reset_index()
    df_marital_counts.columns = ['Marital Status', 'Count']

    # Круговая диаграмма с дыркой (donut)
    fig = px.pie(
        df_marital_counts,
        names='Marital Status',
        values='Count',
        hole=0.5,
        color_discrete_sequence=['HotPink', 'LightSeaGreen', 'SlateBlue'],
    )
    fig.update_traces(
        marker=dict(line=dict(color='#000000', width=1.4)),
        textposition='outside',
        textinfo='percent+label'
    )
    st.plotly_chart(fig, use_container_width=True)

    total_clients = df.shape[0]
    married_pct = (df_marital_counts.loc[df_marital_counts['Marital Status']
                   == 'married', 'Count'].values[0] / total_clients) * 100
    single_pct = (df_marital_counts.loc[df_marital_counts['Marital Status']
                  == 'single', 'Count'].values[0] / total_clients) * 100
    divorced_pct = (df_marital_counts.loc[df_marital_counts['Marital Status']
                    == 'divorced', 'Count'].values[0] / total_clients) * 100

    st.markdown(f"""
    **Insight 📊:**  
    - Основная группа — married (~60%).
    - Подписки на депозит чуть выше у single и divorced.
    - Семейное положение может быть косвенным индикатором финансовой гибкости.
    """)

elif analysis_type == "Образование":
    st.header("Анализ образования клиентов")

    # Подсчет количества клиентов по уровню образования
    df_education_counts = df['education'].value_counts().reset_index()
    df_education_counts.columns = ['Education', 'Count']

    col1, col2 = st.columns(2)

    with col1:
        # Столбчатая диаграмма
        fig_bar = px.bar(
            df_education_counts,
            x='Education',
            y='Count',
            color='Education',
            text='Count',
            template='plotly_white',
            title='Распределение клиентов по уровню образования'
        )
        fig_bar.update_traces(marker=dict(
            line=dict(color='#000000', width=1.4)))
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Круговая диаграмма (donut)
        fig_pie = px.pie(
            df_education_counts,
            names='Education',
            values='Count',
            hole=0.5,
            template='plotly_white',
            title='Процентное распределение уровней образования'
        )
        fig_pie.update_traces(marker=dict(line=dict(color='#000000', width=1.4)),
                              textposition='outside', textinfo='percent+label')
        # fig_pie.update_layout(title_x=0.5)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Подсчет процентов для инсайтов
    total_clients = df.shape[0]
    primary_pct = (df_education_counts.loc[df_education_counts['Education'] == 'primary', 'Count'].values[0] /
                   total_clients) * 100 if 'primary' in df_education_counts['Education'].values else 0
    secondary_pct = (df_education_counts.loc[df_education_counts['Education'] == 'secondary', 'Count'].values[0] /
                     total_clients) * 100 if 'secondary' in df_education_counts['Education'].values else 0
    tertiary_pct = (df_education_counts.loc[df_education_counts['Education'] == 'tertiary', 'Count'].values[0] /
                    total_clients) * 100 if 'tertiary' in df_education_counts['Education'].values else 0
    unknown_pct = (df_education_counts.loc[df_education_counts['Education'] == 'unknown', 'Count'].values[0] /
                   total_clients) * 100 if 'unknown' in df_education_counts['Education'].values else 0

    st.markdown(f"""
    **Insight 📊:**  
    - Большинство клиентов — secondary (среднее образование).
    - Наибольший процент подписавшихся среди tertiary (высшее образование).
    - Ключевое замечание: высокий уровень образования → более высокая склонность к долгосрочным вкладам.
    """)

elif analysis_type == "Кредиты & займы":
    # st.header("Анализ кредитов и займов клиентов")

    # Подсчет значений для default, housing и loan
    df_default_counts = df['default'].value_counts()
    df_housing_counts = df['housing'].value_counts()
    df_loan_counts = df['loan'].value_counts()

    # Создаем три круговые диаграммы на одном холсте
    fig = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
                        subplot_titles=('Кредит в дефолте', 'Ипотечный кредит', 'Персональный кредит'))

    fig.add_trace(go.Pie(
        labels=df_default_counts.index,
        values=df_default_counts.values,
        hole=0.6,
        marker_colors=['Crimson', 'ForestGreen'],
        showlegend=False
    ), row=1, col=1)

    fig.add_trace(go.Pie(
        labels=df_housing_counts.index,
        values=df_housing_counts.values,
        hole=0.6,
        marker_colors=['Crimson', 'ForestGreen'],
        showlegend=False
    ), row=1, col=2)

    fig.add_trace(go.Pie(
        labels=df_loan_counts.index,
        values=df_loan_counts.values,
        hole=0.6,
        marker_colors=['Crimson', 'ForestGreen'],
        showlegend=True
    ), row=1, col=3)

    fig.update_layout(
        title_text='Анализ кредитов и займов',
        title_x=0.5,
        template='simple_white',
        showlegend=True
    )

    fig.update_traces(hoverinfo='value',textinfo='percent+label',textposition='inside', marker=dict(line=dict(width=0.003)))

    st.plotly_chart(fig, use_container_width=True)

    # Инсайты
    st.markdown("""
    **Insight 📊:**  
    - Большинство клиентов не имеют housing loan и personal loan.
    - Те, кто имеет кредиты, подписываются реже.
    - Это может говорить о том, что кредиты отнимают финансовую гибкость.
    """)

elif analysis_type == "Тип контакта":
    st.header("Тип контакта с клиентами")
    
    # Подсчет количества каждого типа контакта
    df_contact_counts = df["contact"].value_counts().reset_index()
    df_contact_counts.columns = ["Contact", "Count"]
    
    # Круговая диаграмма
    fig = px.pie(
        df_contact_counts,
        names="Contact",
        values="Count",
        hole=0.5,
        template="simple_white",
        color_discrete_sequence=["#FF6347", "#00BFFF", "#32CD32"]
    )
    fig.update_traces(
        marker=dict(line=dict(color='#000000', width=1.4)),
        textposition='outside',
        textinfo='percent+label'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Insight 📊:**  
    - Два основных канала: cellular и telephone.
    - Подписка выше у клиентов, которых контактировали через cellular — более персонализированный и удобный контакт.
    """)

elif analysis_type == "Месяц контакта":
    st.header("Месяц последнего контакта")
    
    # Подсчет количества контактов по месяцам
    df_month_counts = df["month"].value_counts().reset_index()
    df_month_counts.columns = ["Month", "Count"]
    
    # Бар-чарт для количества контактов
    fig = px.bar(
        df_month_counts.sort_values(by="Month"),
        x="Month",
        y="Count",
        color="Month",
        text="Count",
        template="simple_white",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(marker=dict(line=dict(color="#000000", width=1.2)))
    
    st.plotly_chart(fig, use_container_width=True)    
    st.markdown("""
    **Insight 📊:**  
    - Наибольшее количество контактов — в may и jul.
    - Подписка выше в зимне-весенние месяцы (mar, apr) — возможно, клиенты активнее готовят финансовую подушку в это время.
    """)

elif analysis_type == "Результат предыдущей кампании":
    st.header("Результат предыдущей маркетинговой кампании")
    
    # Подсчет количества по результатам предыдущей кампании
    df_poutcome_counts = df["poutcome"].value_counts().reset_index()
    df_poutcome_counts.columns = ["Poutcome", "Count"]
    
    col1, col2 = st.columns(2)
    with col1:
        # Бар-чарт
        fig_bar = px.bar(
            df_poutcome_counts,
            x="Poutcome",
            y="Count",
            color="Poutcome",
            text="Count",
            template="simple_white",
            color_discrete_sequence=["grey", "red", "blue", "green"]
        )
        fig_bar.update_traces(marker=dict(line=dict(color="#000000", width=1.2)))
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        # Пай-чарт
        fig_pie = px.pie(
            df_poutcome_counts,
            names="Poutcome",
            values="Count",
            hole=0.5,
            template="simple_white",
            color_discrete_sequence=["grey", "red", "blue", "green"]
        )
        fig_pie.update_traces(marker=dict(line=dict(color="#000000", width=1.4)),
                              textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("""
    **Insight 📊:**  
    - Большинство клиентов ранее не контактировались или отказались (nonexistent, failure).
    - Те, у кого предыдущая кампания была success, с высокой вероятностью подписываются вновь.
    """)

elif analysis_type == "Влияние предыдущих кампаний":
    st.header("Влияние предыдущих кампаний")
    
    # Подготовка данных
    st.markdown("""
    - **previous**: Количество предыдущих контактов перед текущей кампанией.
    - **pdays**: Количество дней, прошедших с последнего контакта (или -1, если не связывались).
    """)
    
    # Гистограмма previous
    fig_previous = px.histogram(
        df, x="previous",
        nbins=20, color_discrete_sequence=["Teal"],
        title="<b>Распределение количества предыдущих контактов"
    )
    fig_previous.update_layout(title_x=0.5)
    st.plotly_chart(fig_previous, use_container_width=True)
    
    # Гистограмма pdays (исключаем -1)
    fig_pdays = px.histogram(
        df[df["pdays"] != -1],
        x="pdays",
        nbins=20, color_discrete_sequence=["SlateBlue"],
        title="<b>Количество дней с последнего контакта (pdays)"
    )
    fig_pdays.update_layout(title_x=0.5)
    st.plotly_chart(fig_pdays, use_container_width=True)
    
    # Insight
    st.markdown("""
    **Insight 📊:**  
    - Положительная история взаимодействия (успех ранее) → более высокая подписка.
    - Отрицательный опыт в прошлом мешает повторной подписке.
    """)

elif analysis_type == "Средний баланс по профессиям":
    st.header("Средний баланс по профессиям")
    
    # Группировка данных
    avg_balance_by_job = df.groupby('job', as_index=False)['balance'].mean()
    avg_balance_by_job['balance'] = avg_balance_by_job['balance'].round(1)
    
    # Сортировка по среднему балансу
    avg_balance_by_job = avg_balance_by_job.sort_values(by='balance', ascending=False)
    
    # Визуализация
    fig = px.bar(
        avg_balance_by_job,
        x='job',
        y='balance',
        text='balance',
        color='job',
        template='ggplot2',
        title='<b>Средний баланс по типу работы</b>'
    )
    fig.update_traces(marker=dict(line=dict(color='#000000', width=1.2)))
    fig.update_layout(title_x=0.5, showlegend=False, xaxis_title='Тип работы', yaxis_title='Средний баланс')
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight
    st.markdown("""
    **Insight 📊:**  
    - Наибольший средний баланс у management и self-employed.
    - Низкий баланс у blue-collar и housemaid.
    - Баланс — важный фактор при принятии решения о подписке.
    """)

elif analysis_type == "Распределение возраста по семейному положению":
    st.header("Распределение возраста по семейному положению")
    
    fig = px.box(
        df,
        x='marital',
        y='age',
        color='marital',
        template='simple_white',
        color_discrete_sequence=['HotPink', 'LightSeaGreen', 'SlateBlue']
    )
    
    st.plotly_chart(fig, use_container_width=True)    
    # Insight
    st.markdown("""
    **Insight 📊:**  
    - Married — более старшие клиенты.
    - Single — чаще молодые.
    - Интересно, что у divorced медианный возраст чуть выше.
    """)

elif analysis_type == "Распределение возраста по образованию":
    st.header("Распределение возраста по образованию")
    
    fig = px.box(
        df,
        x='education',
        y='age',
        color='education',
        template='simple_white',
        title='<b>Распределение возраста по уровню образования</b>'
    )
    
    fig.update_layout(title_x=0.5, legend_title_text="<b>Образование")
    st.plotly_chart(fig, use_container_width=True)
    
    # Insight
    st.markdown("""
    **Insight 📊:**  
    - Более молодые — в группе secondary.
    - Старшие — чаще в primary.
    - Высшее образование распространено у возрастной группы 30-50 лет.
    """)

elif analysis_type == "Подписки на депозит по месяцам":
    st.header("Подписки на депозит по месяцам")

    # Подготовка данных
    deposits_by_month = df.groupby(['month', 'y'], as_index=False)['age'].count().rename(columns={'age': 'Count'})
    deposits_by_month['percent'] = round(deposits_by_month['Count'] * 100 / deposits_by_month.groupby('month')['Count'].transform('sum'), 1)
    deposits_by_month['percent'] = deposits_by_month['percent'].apply(lambda x: f'{x}%')

    # График
    fig = px.bar(
        deposits_by_month,
        x='month',
        y='Count',
        text='percent',
        color='y',
        barmode='group',
        template='simple_white',
        color_discrete_sequence=['MediumPurple', 'YellowGreen']
    )
    fig.update_layout(
        title_x=0.5,
        showlegend=True,
        legend_title_text="Deposit",
        title_text='<b style="color:black; font-size:100%;">Подписки на депозит по месяцам'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Insight
    st.markdown("""
    **Insight📊:**  
    - Подписки выше в mar, apr, jun.
    - Менее активно подписываются в конце года.
    """)

elif analysis_type == "Роль ипотечного и персонального кредита в подписках":
    st.header("Роль housing/personal loan в подписках на депозит")
    
    # Housing loan
    a = df.groupby(['housing', 'y'], as_index=False).size().rename(columns={'size':'Count'})
    fig1 = px.bar(
        a, x='housing', y='Count', color='y', barmode='group',
        title="<b>Housing Loan vs Deposits</b>", template='simple_white',
        color_discrete_sequence=['MediumPurple', 'YellowGreen']
    )
    
    # Personal loan
    b = df.groupby(['loan', 'y'], as_index=False).size().rename(columns={'size':'Count'})
    fig2 = px.bar(
        b, x='loan', y='Count', color='y', barmode='group',
        title="<b>Personal Loan vs Deposits</b>", template='simple_white',
        color_discrete_sequence=['MediumPurple', 'YellowGreen']
    )
    
    col1, col2 = st.columns(2)
    with col1: st.plotly_chart(fig1, use_container_width=True)
    with col2: st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("""
    **Insight📊:**
    - Клиенты без кредитов housing/personal чаще подписываются.
    - Наличие кредита снижает вероятность вклада — высокая долговая нагрузка.
    """)

elif analysis_type == "Подписки по возрастным группам":
    st.header("Подписки на депозит по возрастным группам")
    
    # Создаём колонку age_group
    df['age_group'] = pd.cut(df['age'], bins=[18, 25, 35, 45, 55, 100],
                              labels=['18-25', '26-35', '36-45', '46-55', '56+'])
    
    # Группировка
    a = df.groupby(['age_group', 'y'], as_index=False).size().rename(columns={'size':'Count'})
    
    fig = px.bar(
        a, x='age_group', y='Count', color='y', barmode='group',
        template='simple_white', color_discrete_sequence=['MediumPurple', 'YellowGreen']
    )
    
    fig.update_layout(title_x=0.5, title_text="<b>Deposits by Age Group")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Insight📊:**  
    - Группа 26-35 и 36-45 — лидеры по подпискам.
    - Молодые (до 25) и старшие (56+) — минимальная активность.
    """)

elif analysis_type == "Распределение housing, personal loan и default":
    st.header("Housing, Personal Loan и Credit in Default")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig1 = px.pie(
            df, names='housing', title='Housing Loan', hole=0.5,
            color_discrete_sequence=['LightSeaGreen', 'HotPink']
        )
        fig1.update_traces(marker=dict(line=dict(color='#000', width=1.2)), textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.pie(
            df, names='loan', title='Personal Loan', hole=0.5,
            color_discrete_sequence=['SlateBlue', 'Orange']
        )
        fig2.update_traces(marker=dict(line=dict(color='#000', width=1.2)), textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)
    
    with col3:
        fig3 = px.pie(
            df, names='default', title='Credit in Default', hole=0.5,
            color_discrete_sequence=['MediumPurple', 'YellowGreen']
        )
        fig3.update_traces(marker=dict(line=dict(color='#000', width=1.2)), textinfo='percent+label')
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("""
    **Insight📊:**  
    - Большинство клиентов не имеют housing или personal loan.
    - Очень мало клиентов с default — показатель надежной базы.
    """)

elif analysis_type == "Баланс и подписки на депозит":
    st.header("Balance vs Подписки на депозит")
    
    fig = px.box(
        df, x='y', y='balance', color='y', template='simple_white',
        color_discrete_sequence=['MediumPurple', 'YellowGreen']
    )
    fig.update_layout(title_x=0.5, title_text="<b>Balance vs Deposit Subscription</b>")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Insight📊:**  
    - Высокий баланс → выше вероятность подписки.
    - Те, кто не подписывается, обычно имеют более низкий баланс.
    """)

elif analysis_type == "Длительность звонка и подписки":
    st.header("Длительность звонка и подписки")
    
    fig = px.box(
        df, x='y', y='duration', color='y', template='simple_white',
        color_discrete_sequence=['MediumPurple', 'YellowGreen']
    )
    fig.update_layout(title_x=0.5, title_text="<b>Duration of Call vs Deposit Subscription</b>")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Insight📊:**  
    - Длительные звонки (дольше 300 секунд) → выше шанс подписки.
    - Короткие звонки чаще приводят к отказу.
    """)

elif analysis_type == "Heatmap профессия vs семейное положение":
    st.header("Взаимосвязь профессии и семейного положения")
    
    crosstab = pd.crosstab(df['job'], df['marital'])
    
    fig = px.imshow(
        crosstab, text_auto=True, color_continuous_scale='Viridis',
        title="<b>Heatmap: Job vs Marital Status"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Insight📊:**  
    - Чётко видно, что management и technician — лидеры среди married.
    - blue-collar больше среди married, single — чаще student.
    """)




