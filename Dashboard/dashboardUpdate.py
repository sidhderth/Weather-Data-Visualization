import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
import os
import datetime
import monthylyCSVMaker

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Enphase Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded")

averageOrNot = "Hourly"

st.sidebar.markdown("<h2 style='text-align: center; color: white;'>☀️Enphase Dashboard☀️</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
selectWeatherMonth = st.sidebar.selectbox("Select Weather Month", months)

formatMonth = [f"{months.index(selectWeatherMonth) + 1:02}"][0]
weatherFilePath = os.path.join('Weather', 'Daily', f"{formatMonth}-{str(datetime.date.today())[0:4]}")

averageWeatherButton = st.sidebar.button("Average", type="primary")

if (averageWeatherButton):
    selectedWheatherFile = monthylyCSVMaker.fileAverage(weatherFilePath)
    selectedWheatherFile.monthlyAverageMaker()
    
    averageOrNot = "Average"

weatherFiles = [files for files in os.listdir(weatherFilePath) if files.endswith('.csv')]

selectedWeatherFile = st.sidebar.selectbox("Select Weather File: ", weatherFiles)

enphaseFilePath = 'Enphase'
enphaseFiles = [f for f in os.listdir(enphaseFilePath) if f.endswith('.csv')]
selectedEnphaseFile = st.sidebar.selectbox("Select Enphase File: ", enphaseFiles)

col = st.columns((3, 6, 8), gap='small')

with col[0]:
    def createMetricContainer(title, value, unit):
        return f"""
        <div style='background-color: rgba(25, 25, 25, 0.8); border: 2px solid #444; 
        border-radius: 10px; padding: 10px; margin-bottom: 10px; 
        display: flex; flex-direction: column; justify-content: center; align-items: center; 
        text-align: center; width: 125px; height: 125px; color: #f0f0f0; box-sizing: border-box;'>
            <h5 style='margin: 0; font-size: 12px; width: 100%; text-align: center;'> {title} </h5>
            <h6 style='margin: 0; font-size: 24px; width: 100%; text-align: center;'> {value} {unit}</h6>
        </div>
        """

    st.markdown(createMetricContainer("Power Imported", "0", "W"), unsafe_allow_html=True)
    st.markdown(createMetricContainer("Power Produced", "0", "W"), unsafe_allow_html=True)
    st.markdown(createMetricContainer("Power Consumed", "0", "W"), unsafe_allow_html=True)
    st.markdown(createMetricContainer("Power Exported", "0", "W"), unsafe_allow_html=True)
    st.markdown(createMetricContainer("Houses Powered", "0", None), unsafe_allow_html=True)
    st.markdown(createMetricContainer("CO2 Removed", "0", "LBS"), unsafe_allow_html=True)

st.markdown(
    """
    <style>
    h4 {
        margin-bottom: -100px;  /* Reduce the bottom margin of the title */
    }
    .plotly-chart {
        margin-top: -100px;  /* Reduce the top margin of the charts */
    }
    </style>
    """, 
    unsafe_allow_html=True
)

with col[1]:
    st.markdown("<h4 style='text-align: center; color: white;'>Enphase Data</h2>", unsafe_allow_html=True)

with col[2]:    
    st.markdown(f"<h4 style='text-align: center; color: white;'>{averageOrNot} Weather Data</h2>", unsafe_allow_html=True)
    df = pd.read_csv(os.path.join(weatherFilePath, selectedWeatherFile), encoding="ISO-8859-1")
    nestedCollum = st.columns((8, 8), gap = 'small')

    with nestedCollum[0]:
        timeX = pd.to_datetime(df['datetime'])
        solarIrradianceY = df['solarIrradiance']
        solarEnergyY = df['solarEnergy']

        figSolarIrradiance = px.line(
            x = timeX,
            y = solarIrradianceY,
            title = "Solar Irradiance",
            labels = {'x': 'Date', 'y': 'Solar Irradiance (W/m²)'}
        )
        figSolarIrradiance.update_traces(line_color='red', mode='lines+markers')
        figSolarIrradiance.update_layout(
            xaxis_tickangle=-45, 
            width=450, 
            height=400,
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            font_color='white',  # Text color
            title_font_color='white'
        )
        st.plotly_chart(figSolarIrradiance)
        
        figSolarEnergy = px.line(
            x = timeX,
            y = solarEnergyY,
            title = "Solar Energy",
            labels = {'x': 'Date', 'y': 'Solar Energy (MJ/m²)'}
        )
        figSolarEnergy.update_traces(line_color='blue', mode='lines+markers')
        figSolarEnergy.update_layout(
            xaxis_tickangle=-45, 
            width=450, 
            height=400,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font_color='white',
            title_font_color='white'
        )
        st.plotly_chart(figSolarEnergy)

    with nestedCollum[1]:
        timeX = pd.to_datetime(df['datetime'])  
        uvIndexY = df['uvIndex']  
        cloudCoverY = df['cloudCover']  

        figCloudCover = px.line(
            x = timeX,
            y = cloudCoverY,
            title = "Cloud Cover",
            labels = {'x': 'Date', 'y': 'Cloud Cover (%)'}
        )
        figCloudCover.update_traces(line_color='green', mode='lines+markers')
        figCloudCover.update_layout(
            xaxis_tickangle=-45, 
            width=450, 
            height=400,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font_color='white',
            title_font_color='white'
        )
        st.plotly_chart(figCloudCover)
        
        figUVIndex = px.line(
            x = timeX,
            y = uvIndexY,
            title = "UV Index",
            labels = {'x': 'Date', 'y': 'UV Index'}
        )
        figUVIndex.update_traces(line_color='orange', mode='lines+markers')
        figUVIndex.update_layout(
            xaxis_tickangle=-45, 
            width=550, 
            height=400,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font_color='white',
            title_font_color='white'
        )
        st.plotly_chart(figUVIndex)
