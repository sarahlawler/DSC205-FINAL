
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Data Visualization Job Filter')
st.header("An app created by Sarah Lawler and Kat Reynosa")

dataset = 'https://raw.githubusercontent.com/sarahlawler/DSC205/refs/heads/main/DataScience_salaries_2024.csv'
df = pd.read_csv(dataset)

df.dropna(inplace=True)
# show data
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(df)

# use slider to find min and max
st.markdown('---')
minSalary, maxSalary = st.slider('Select desired salary range:',
                                 min_value = int(df['salary_in_usd'].min()),
                                 max_value = int(df['salary_in_usd'].max()),
                                 value = (int(df['salary_in_usd'].min()), int(df['salary_in_usd'].max())),
                                 step=1000)
st.write(f'You set {minSalary} as your minimum salary and {maxSalary} as your maximum salary.')


# connect location to company location

countries = st.multiselect('Select countries to filter jobs:',
                                    options = df['company_location'].unique(),
                                    default = [])

#filter by salary and job
filtered = df.loc[(df['salary_in_usd'] >= minSalary) & (df['salary_in_usd'] <= maxSalary)]

# filter by location and salary

if countries:
    filtered = filtered[filtered['company_location'].isin(countries)]
                                

# save choice
choice = st.selectbox('Select plot to visualize salaries:',
                      ('Histogram - Filtered by Salary and Country',
                       'Pie Chart - Job Distribution by Country',
                       'Line Plot - Salary Through Time'))
if choice == 'Histogram - Filtered by Salary and Country':
    for country in countries:
        country_data = filtered[filtered['company_location'] == country]
        plt.figure(figsize=(8,5))
        sns.histplot(country_data['salary_in_usd'], kde = True, bins='auto', color='blue')
        plt.title(f'Salary Distribution in {country}')
        plt.xlabel('Salary (USD)')
        plt.ylabel('Frequency')
        st.pyplot(plt)
        plt.close()
if choice == 'Pie Chart - Job Distribution by Country':
    if countries:
        filtered = filtered[filtered['company_location'].isin(countries)]
    country_count = filtered['company_location'].value_counts()
    plt.figure(figsize=(8,5))
    plt.pie(country_count, labels=country_count.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    plt.title('Job Distribution by Country')
    st.pyplot(plt)
    plt.close()
    
if choice == 'Line Plot - Salary Through Time':
    filtered = df.loc[(df['salary_in_usd'] >= minSalary) & (df['salary_in_usd'] <= maxSalary)]
    df['work_year'] = pd.to_numeric(df['work_year'], errors = 'coerce')
    if countries:
        
        filtered = filtered.loc[filtered['company_location'].isin(countries)]
        salaryOverTime = filtered.groupby(['work_year', 'company_location'])['salary_in_usd'].mean().reset_index()

        plt.figure(figsize=(8,5))
        sns.lineplot(data=salaryOverTime, x='work_year', y='salary_in_usd', hue='company_location', marker='o')
        plt.title('Average Salary Trend Over Time')
        plt.xlabel('Date')
        plt.ylabel('Average Salary (USD)')
        st.pyplot(plt)
        plt.close()
        
        
    
