import streamlit as st
import pandas as pd
import zipfile
import os
import seaborn as sns
sns.set_theme(style='dark')

st.set_page_config(
    page_title="Bike Sharing Data Analysis Dashboard",
    page_icon=":bike:")

st.title(':bike: Bike Sharing Data Analysis Dashboard :bike:')

st.write("""Bike-sharing systems have revolutionized urban mobility by offering a flexible, 
            eco-friendly, and health-conscious mode of transportation. These systems, 
            which automate the rental and return process, have proliferated worldwide, 
            with over 500 programs and more than half a million bicycles in operation. 
            The data generated by these systems is not only voluminous but also rich in detail, 
            recording every ride's duration, departure, and arrival positions, 
            effectively turning the bike-sharing network into a vast sensor array for urban mobility.
            """)

st.write("""The dataset we will explore pertains to the Capital Bikeshare system in Washington D.C., 
            covering the years 2011 and 2012. This data has been meticulously aggregated on both 
            hourly and daily bases, incorporating vital weather information to provide a comprehensive 
            view of the factors influencing bike rentals. The primary goal of visualizing this dataset 
            is to uncover patterns and insights that can inform better management and expansion of bike-sharing services.
            """)

# Time Series Analysis
def time_series_analysis():
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])

    daily_share = hour_data.groupby("dteday")["Rental Count"].sum()
    month_share = day_data.groupby("mnth")["Rental Count"].sum()
    season_share = day_data.groupby("season")["Rental Count"].sum()

    tab1, tab2, tab3 = st.tabs(["Daily", "Monthly", "Seasonal"])

    with tab1:
        # Add/Remove functionality
        selected_date_str = st.text_input("Want to change value? Select Date (YYYY-MM-DD)")

        if selected_date_str:
            try:
                selected_date = pd.to_datetime(selected_date_str)
                # Filter data for the selected date
                date_data = hour_data.loc[hour_data['dteday'] == selected_date]

                if not date_data.empty:
                    # Display data for the selected date
                    st.write(f"Data for {selected_date_str}")
                    existing_cnt = date_data.iloc[0]['cnt']  # Get existing cnt value
                    st.write(f"Existing cnt: {existing_cnt}")
                    st.dataframe(date_data)

                    # Input for new cnt value
                    new_cnt_value = st.text_input("Enter New cnt Value")

                    if st.button("Update cnt"):
                        if new_cnt_value:
                            try:
                                # Convert input to integer
                                value = int(new_cnt_value)

                                # Update cnt value in the DataFrame
                                date_data.loc[date_data.index[0], 'cnt'] = value
                                st.success(f"cnt value updated for {selected_date_str} to {value}")

                                # Update main hour_data (assuming it's a copy)
                                hour_data.loc[hour_data['dteday'] == selected_date, 'cnt'] = value

                            except ValueError:
                                st.error("Invalid input. Please enter an integer.")
                        else:
                            st.error("Please enter a new cnt value.")
                    else:
                        st.warning(f"No data found for {selected_date_str}")
            except ValueError:
                st.error("Invalid date format. Please enter YYYY-MM-DD.")

        # Save the updated data (consider error handling for saving)
        hour_data.to_csv("hour.csv", index=False)
        st.markdown("<p style='text-align: center; color: white;'>Line Chart</p>", unsafe_allow_html=True)
        st.line_chart(daily_share)

    with tab2:
        st.markdown("<p style='text-align: center; color: white;'>Bar Chart</p>", unsafe_allow_html=True)
        st.bar_chart(month_share)

    with tab3:
        st.markdown("<p style='text-align: center; color: white;'>Bar Chart</p>", unsafe_allow_html=True)
        st.bar_chart(season_share)
        with st.expander("Detailed Explanation"):
            st.write(
                """ Season (1=springer, 2=summer, 3=fall, 4=winter)
                """
            )

def weather_impact_analysis():
    scatter_data = day_data.rename(columns={'temp':'Temperature', 'hum':'Humidity'})
    tab1, tab2 = st.tabs(["Temperature", "Humidity"])

    with tab1:
        st.markdown("<p style='text-align: center; color: white;'>Scatter Plot</p>", unsafe_allow_html=True)
        st.scatter_chart(scatter_data, x="Temperature", y="Rental Count")
        with st.expander("Detailed Explanation"):
            st.write(
                """ Temperature is Normalized in Celsius. The values are divided to 41 (max)
                """
            )

    with tab2:
        st.markdown("<p style='text-align: center; color: white;'>Scatter Plot</p>", unsafe_allow_html=True)
        st.scatter_chart(scatter_data, x="Humidity", y="Rental Count")
        with st.expander("Detailed Explanation"):
            st.write(
                """ Humidity is normalized. The values are divided to 100 (max)
                """
            )
    
def show_all():
    col = st.columns((2,2), gap='medium')
    with col[0]:
        st.subheader("Time Series")
        time_series_analysis()
    with col[1]:
        st.subheader("Weather Impact")
        weather_impact_analysis()

uploaded_file = st.file_uploader("Choose Bike Sharing Dataset")

if uploaded_file is not None:
    filename, file_extension = os.path.splitext(uploaded_file.name)
    if (file_extension == ".zip") is True:
        st.success("File type is ZIP")
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall()
    else:
        st.error('File type is not ZIP')
    

    day_data = pd.read_csv("day.csv")
    hour_data = pd.read_csv("hour.csv")

    day_data = day_data.rename(columns={'cnt':'Rental Count'})
    hour_data = hour_data.rename(columns={'cnt':'Rental Count'})

    vis_list = ["Time Series Analysis", "Weather Impact Analysis", "Show All Visualization"]
    selected_vis = st.selectbox('Select a Type of Visualization', vis_list)

    if selected_vis == "Time Series Analysis":
        time_series_analysis()
    elif selected_vis == "Weather Impact Analysis":
        weather_impact_analysis()
    elif selected_vis == "Show All Visualization":
        show_all()
