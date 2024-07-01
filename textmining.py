import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

# Load CSV files
raw_df = pd.read_csv('/Users/sanguri/sesac/visualization/raw_극성사전.csv')
tone_rate_df = pd.read_csv('/Users/sanguri/sesac/visualization/어조금리분석.csv')
hawk_df = pd.read_csv("/Users/sanguri/sesac/visualization/hawk2.csv")
dove_df = pd.read_csv("/Users/sanguri/sesac/visualization/dove2.csv")
call_report_url_df = pd.read_csv('/Users/sanguri/sesac/visualization/call_reports_url.csv')
call_news_df = pd.read_csv('/Users/sanguri/sesac/visualization/call_news.csv')

# Convert 'date' columns to datetime
tone_rate_df['date'] = pd.to_datetime(tone_rate_df['date'], format='%Y-%m-%d')
call_report_url_df['date'] = pd.to_datetime(call_report_url_df['date'])
call_news_df['date'] = pd.to_datetime(call_news_df['date'])

# Streamlit page title
st.title('논문 프로젝트 페이지')

# Category visualization
st.header('카테고리 별 데이터 시각화')
categories = raw_df['category'].unique()
st.write(f"카테고리 유니크 값: {', '.join(categories)}")

# Plotly chart for category distribution
fig = px.histogram(raw_df, x='category', color='category', title='Category Distribution')
st.plotly_chart(fig, use_container_width=True)

# Scatter plot for doc_tone and base_rate correlation over time
st.header('날짜 흐름에 따른 doc_tone과 base_rate의 상관관계 산점도')
st.scatter_chart(tone_rate_df, x='doc_tone', y='base_rate', color='date', 
                 x_label='doc_tone', y_label='base_rate', use_container_width=True)

# Min-Max normalization
scaler = MinMaxScaler()
tone_rate_df[['doc_tone', 'base_rate']] = scaler.fit_transform(tone_rate_df[['doc_tone', 'base_rate']])

# Line chart for doc_tone and base_rate over time
st.header('날짜 흐름에 따른 doc_tone과 base_rate 선 그래프')
tone_rate_df = tone_rate_df.sort_values(by='date')
tone_rate_df.set_index('date', inplace=True)
st.line_chart(tone_rate_df[['doc_tone', 'base_rate']], x_label='Date', y_label='Value', use_container_width=True)

# Hawkish dictionary filter
st.subheader("Hawkish Dictionary")
min_hawk_score = hawk_df["polarity_score"].min()
max_hawk_score = hawk_df["polarity_score"].max()
hawk_score_range = st.slider("확인하고 싶은 극성점수의 범주를 설정하세요.:", min_value=min_hawk_score, max_value=max_hawk_score, value=(min_hawk_score, max_hawk_score), step=0.1)
filtered_hawk_df = hawk_df[(hawk_df["polarity_score"] >= hawk_score_range[0]) & (hawk_df["polarity_score"] <= hawk_score_range[1])]

if not filtered_hawk_df.empty:
    st.subheader(f"극성점수가 {hawk_score_range[0]}과 {hawk_score_range[1]} 사이에 있는 단어는 다음과 같습니다.")
    st.write(filtered_hawk_df)
else:
    st.subheader("선택된 범주 내의 극성점수에 해당하는 단어가 없습니다.")

# Dovish dictionary filter
st.subheader("Dovish Dictionary")
min_dove_score = dove_df["polarity_score"].min()
max_dove_score = dove_df["polarity_score"].max()
dove_score_range = st.slider("확인하고 싶은 극성점수의 범주를 설정하세요.:", min_value=min_dove_score, max_value=max_dove_score, value=(min_dove_score, max_dove_score), step=0.1)
filtered_dove_df = dove_df[(dove_df["polarity_score"] >= dove_score_range[0]) & (dove_df["polarity_score"] <= dove_score_range[1])]

if not filtered_dove_df.empty:
    st.subheader(f"극성점수가 {dove_score_range[0]}과 {dove_score_range[1]} 사이에 있는 단어는 다음과 같습니다.")
    st.write(filtered_dove_df)
else:
    st.subheader("선택된 범주 내의 극성점수에 해당하는 단어가 없습니다.")

# Call report URL section
st.header('콜금리 그래프')
st.line_chart(call_report_url_df.set_index('date')['call_rate'])

min_date_report = st.date_input("채권분석보고서 조회 시작일", value=pd.to_datetime("2024-06-01").date(), key="min_date_report", format="YYYY-MM-DD")
max_date_report = st.date_input("채권분석보고서 조회 종료일", value=pd.to_datetime("2024-06-30").date(), key="max_date_report", format="YYYY-MM-DD")

min_date_report = pd.to_datetime(min_date_report)
max_date_report = pd.to_datetime(max_date_report)
filtered_report_url_df = call_report_url_df[(call_report_url_df['date'] >= min_date_report) & (call_report_url_df['date'] <= max_date_report)]
st.write("조회된 채권분석보고서", filtered_report_url_df)

# Call news section
min_date_news = st.date_input("뉴스 조회 시작일", value=pd.to_datetime("2024-03-01").date(), key="min_date_news", format="YYYY-MM-DD")
max_date_news = st.date_input("뉴스 조회 종료일", value=pd.to_datetime("2024-03-31").date(), key="max_date_news", format="YYYY-MM-DD")

min_date_news = pd.to_datetime(min_date_news)
max_date_news = pd.to_datetime(max_date_news)
filtered_call_news_df = call_news_df[(call_news_df['date'] >= min_date_news) & (call_news_df['date'] <= max_date_news)]
st.write("조회된 뉴스", filtered_call_news_df)
