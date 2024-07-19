import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def get_country_data(country):
    base_url = f"https://disease.sh/v3/covid-19/countries/{country}"
    response = requests.get(base_url)
    return response.json()

def get_historical_data(country):
    base_url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=30"
    response = requests.get(base_url)
    return response.json()

def main():
    st.title("COVID-19 Statistics Tracker")

    # User input for country
    country = st.text_input("Enter a country name (e.g., USA, India):", "USA")

    if st.button("Get COVID-19 Statistics"):
        country_data = get_country_data(country)
        historical_data = get_historical_data(country)

        if "country" in country_data:
            # Current statistics
            st.subheader(f"Current COVID-19 Statistics in {country_data['country']}")
            st.write(f"Total Cases: {country_data['cases']}")
            st.write(f"Total Deaths: {country_data['deaths']}")
            st.write(f"Total Recovered: {country_data['recovered']}")
            st.write(f"Active Cases: {country_data['active']}")
            st.write(f"Critical Cases: {country_data['critical']}")

            # Historical data
            st.subheader("30-Day COVID-19 Cases Trend")
            timeline = historical_data['timeline']
            cases = timeline['cases']
            deaths = timeline['deaths']
            recovered = timeline['recovered']
            
            # Prepare data for chart
            df = pd.DataFrame({
                'Date': pd.to_datetime(list(cases.keys())),
                'Cases': list(cases.values()),
                'Deaths': list(deaths.values()),
                'Recovered': list(recovered.values())
            })
            df.set_index('Date', inplace=True)

            # Display cases trend
            fig = px.line(df, x=df.index, y=['Cases', 'Deaths', 'Recovered'], 
                          title=f'30-Day COVID-19 Trend in {country_data["country"]}')
            fig.update_xaxes(title_text='Date')
            fig.update_yaxes(title_text='Count')
            st.plotly_chart(fig)

        else:
            st.error("Country not found. Please check the name and try again.")

if __name__ == "__main__":
    main()
