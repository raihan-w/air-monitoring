import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_antd_components as sac
import streamlit_shadcn_ui as ui

main_data = pd.read_csv('dashboard/main_data.csv')

st.title("Air Quality Analysis Dashboard")

st.markdown(
    """
    ## **Introduction to the Dashboard**
    Welcome to the Air Quality Dashboard!  This interactive tool allows you to explore air quality data from 12 monitoring stations. You can analyze air quality trends and the factors that influence pollution levels over time and their relationship with various environmental factors.
    """
)
# Membuat tabs
tabs_selection = sac.tabs([
    sac.TabsItem(label="Overview", icon="house-fill"),
    sac.TabsItem(label="Analytics", icon="bar-chart-fill"),
    sac.TabsItem(label="Conclusion", icon="book-fill"),
],index=0, variant="outline", color="pink", use_container_width=True)

# Tab Overview
if tabs_selection == 'Overview':
    st.markdown(
        """
        ### **Analysis Questions** 
        1. Bagaimana tren polutan (PM2.5, PM10, SO2, NO2, CO, dan O3) berubah dari tahun ke tahun?
        2. Bagaimana perubahan tingkat polutan pada jam-jam tertentu?
        3. Apakah ada korelasi antar polutan (PM2.5, PM10, SO2, NO2, CO, dan O3)?
        4. Apakah curah hujan mempengaruhi konsentrasi polutan terutama PM2.5 dan PM10?
        """)

    st.markdown(
        """
        ### **Variable Description**
        Berikut adalah deskripsi dari variabel yang terdapat pada dataset:
    
        - **Year**: Tahun pengambilan data
        - **Month**: Bulan pengambilan data
        - **Day**: Hari pengambilan data
        - **Hour**: Jam pengambilan data
        - **PM2.5**: Konsentrasi PM2.5 (µg/m³)
        - **PM10**: Konsentrasi PM10 (µg/m³)
        - **SO2**: Konsentrasi SO2 (µg/m³)
        - **NO2**: Konsentrasi NO2 (µg/m³)
        - **CO**: Konsentrasi CO (µg/m³)
        - **O3**: Konsentrasi O3 (µg/m³)
        - **TEMP**: Suhu udara (°C)
        - **PRESSURE**: Tekanan udara (hPa)
        - **DEWP**: Suhu titik embun (°C)
        - **RAIN**: Curah hujan (mm)
        - **wd**: Arah angin
        - **WSPM**: Kecepatan angin (m/s)
        - **station**: Nama stasiun pemantauan kualitas udara
        """
    )

    st.write("### **Dataset Preview**")
    stations = main_data['station'].unique()
    
    selected_station = st.selectbox('Select a Station', stations)

    filtered_data = main_data[main_data['station'] == selected_station]
    filtered_data = filtered_data.drop(columns=['No', 'year', 'month', 'day', 'hour', 'station', 'datetime'])

    # columns = filtered_data.columns.tolist()
    # selected_columns = []
    # for column in columns:
    #     if st.checkbox(f"Show {column}", value=True):  # Default value is True, meaning all columns are shown
    #         selected_columns.append(column)

    # filtered_data = filtered_data[selected_columns]

    st.write(f"Preview for station: {selected_station}")
    ui.table(data=filtered_data.head(5))
    

# Tab Analytics
elif tabs_selection == 'Analytics':

    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

    analytic_segment = sac.segmented(
        items=[
            sac.SegmentedItem(label='Trends'),
            sac.SegmentedItem(label='Hourly'),
            sac.SegmentedItem(label='Correlations'),
            sac.SegmentedItem(label='Rain Impact'),
        ], label='Select the Analysis Focus', align='center', size='sm', divider=False, use_container_width=True
    )
    
    if analytic_segment == 'Trends':
        st.subheader("Trends in Pollutants over Time")
        st.write("Understand how pollutant levels have evolved over the years, identifying any significant upward or downward trends.")

        groupByYear = main_data.groupby('year')[pollutants].mean().reset_index()

        plt.figure(figsize=(14,10))
        for i, pollutant in enumerate(pollutants):
            plt.subplot(3, 2, i + 1) 
            sns.lineplot(x='year', y=pollutant, data=groupByYear)
            plt.title(f'Trend of {pollutant}')
            plt.xlabel('Year')
            plt.ylabel(f'Average Concentration ({pollutant})')
            plt.grid(True)
            plt.xticks(groupByYear['year'], rotation=45)
            plt.tight_layout()
        
        st.pyplot(plt)
        with st.expander('Show explanation'):
            st.markdown(
                """
                - PM2.5 dan PM10 mengalami peningkatan dari tahun 2013 hingga 2014, namun sempat mengalami penurunan dari tahun 2014 hinnga 2016. Pada tahun 2017 konsentasi polutan mengalami peningkatan yang cukup signifikan.
                - SO2 dan NO2 menunjukkan tren yang lebih fluktuatif, dengan sedikit peningkatan pada tahun 2014 kemudian mengalami penurunan secara bertahap hingga 2016. Tetapi terjadi peningkatan pada tahun 2017.
                - CO menunjukkan fluktuasi dengan sedikit penurunan pada tahun 2016, namun terjadi kenaikan signifikan pada 2017.
                - O3 mengalami peningkatan secara bertahap dari tahun 2013 hingga 2015, namun mengalami penurunan signifikan pada tahun 2017.
                """
            )

        st.subheader("Trends in Pollutants Over Time by Station")

        groupByStationYear = main_data.groupby(by=['station', 'year'])[pollutants].mean().reset_index()

        stations = groupByStationYear['station'].unique()
        selected_station = st.selectbox('Select a Station:', stations)

        filtered_data = groupByStationYear[groupByStationYear['station'] == selected_station]
        filtered_data = filtered_data.drop(columns=['station'])

        st.write(f"Average Pollutants for station: {selected_station}")
        ui.table(filtered_data)


    elif analytic_segment == 'Hourly':
        st.subheader("Hourly Variations in Pollutants")
        st.write("Examine daily variations in pollutant concentrations to determine whether certain hours of the day exhibit higher pollution levels. This is important for identifying peak pollution times.")

        groupByHour = main_data.groupby('hour')[pollutants].mean().reset_index()

        plt.figure(figsize=(14,10))
        for i, pollutant in enumerate(pollutants):
            plt.subplot(3, 2, i + 1) 
            sns.lineplot(x='hour', y=pollutant, data=groupByHour)
            plt.title(f'Trend of {pollutant} per Hour')
            plt.xlabel('Hour')
            plt.ylabel(f'Average Concentration ({pollutant})')
            plt.xticks(range(0, 24, 2)) # Menampilkan setiap jam  dengan interval 2 jam
            plt.grid(True)
            plt.tight_layout()
        
        st.pyplot(plt)
        with st.expander('Show explanation', expanded=True):
            st.markdown(
                """
                - PM2.5 dan PM10 menunjukkan penurunan yang signifikan selama malam hingga pagi hari (dari pukul 00:00 hingga sekitar pukul 6:00). Namun, setelah pukul 6:00 nilai keduanya mulai meningkat mencapai puncaknya pada malam hari (sekitar pukul 20:00–23:00).
                - SO2 mengalami penurunan selama malam dan pagi hari (dari pukul 00:00 hingga sekitar pukul 6:00). Namun, setelah pukul 6:00 konsentrasinya menignkat hingga puncaknya pada pukul 11:00 dan mulai menurun pada pukul 12:00 hingga 18:00.
                - NO2 menunjukan kosentrasi tinggi pada jam-jam awal pagi (pukul 00:00–6:00), mengalami sedikit peningkatan pada jam 08:00 dan turun sepanjang siang. Konsentrasi NO2 mengalami peningkatan pada sore hingga malam hari (puncaknya pada pukul 22:00).
                - CO menunjukan kosentrasi tinggi menjelang pagi (pukul 01:00–4:00), mengalami sedikit peningkatan pada pagi hari (pukul 05:00 hingga 08:00) dan turun sepanjang siang (pukul09:00 hingga 16:00). Konsentrasi CO kembali mengalami peningkatan pada sore hingga malam hari(16:00 hingga 23:00).
                - Konsentrasi O3 mengalami peningkatan pada pagi hingga sore hari (puncaknya sekitar pukul 15:00–16:00) kemudian penurunan hingga malam hari.
                """
            )

    elif analytic_segment == 'Correlations':
        st.subheader("Correlation between Pollutants")
        st.write("Analyze how different pollutants are correlated with each other. For instance, PM2.5 and CO might show a strong correlation.")

        correlation_matrix = main_data[pollutants].corr()

        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Correlation Heatmap of Pollutants')
        st.pyplot(plt)
        with st.expander('Show explanation', expanded=True):
            st.markdown(
                """
                - PM2.5 dan PM10 menunjukan korelasi yang sangat kuat (0.88), hal ini mengindikasikan bahwa PM2.5 dan PM10 cenderung meningkat dan menurun bersamaan
                - PM2.5 dan CO menunjukan korelasi positif yang tinggi (0.79), hal ini mengindikasikan bahwa konsentrasi PM2.5 dan CO sering berfluktuasi bersamaan
                - PM2.5 dan NO2 menunjukan korelasi positif yang cukup tinggi (0.67), hal ini mengindikasikan bahwa PM2.5 dan NO2 ering berfluktuasi bersamaan
                - PM10 dan SO2 memiliki korelasi sebesar 0.46, menunjukan bahwa kedua polutan ini seing berhubungan.
                - PM10 dan CO menunjukan korelasi positif yang tinggi (0.70), hal ini mengindikasikan bahwa konsentrasi PM10 dan CO sering berfluktuasi bersamaan
                - PM10 dan NO2 menunjukan korelasi yang cukup tinggi (0.65), hal ini mengindikasikan bahwa konsentrasi PM10 dan CO sering berfluktuasi bersamaan
                - O3 memiliki korelasi negatif pada sebagian besar polutan, hal ini menunjukan meskipun terdapat korelasi dengan polutan sebagian besar O3 tidak terpengaruh langsung oleh polutan lain
                """
            )


    elif analytic_segment == 'Rain Impact':
        st.subheader("Impact of Rainfall on Pollutants")
        st.write("Examine whether rainfall has a significant effect on pollutants such as PM2.5 and PM10.")
        
        rain_pollutant_matrix = main_data[['RAIN'] + pollutants].corr()

        plt.figure(figsize=(8, 6))
        sns.heatmap(rain_pollutant_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Correlation Heatmap: Rainfall and Pollutants')
        st.pyplot(plt)
        with st.expander('Show explanation', expanded=True):
            st.markdown(
                """
                Secara umum korelasi antara curah hujan (RAIN) dan polutan sangat lemah (mendekati 0), hal ini menunjukan bahwa hujan tidak memiliki pengaruh signifikan terhadap konsentrasi sebagian besar polutan. Scatter plot mungkin tidak perlu dilakukan untuk melihat hubungan langsung antara curah hujan dan konsentrasi polutan terutama PM2.5 dan PM10.
                """
            )
        
        plt.figure(figsize=(12, 6))

        # Membuat scatterplot antara Rainfall dan PM2.5
        plt.subplot(1, 2, 1)
        sns.scatterplot(x=main_data['RAIN'], y=main_data['PM2.5'])
        plt.title('Rainfall vs PM2.5') 
        plt.xlabel('Rainfall (mm)') 
        plt.ylabel('PM2.5 (µg/m³)') 
        plt.grid(True)

        # Membuat scatterplot antara Rainfall dan PM10
        plt.subplot(1, 2, 2)  
        sns.scatterplot(x=main_data['RAIN'], y=main_data['PM10'])
        plt.title('Rainfall vs PM10')
        plt.xlabel('Rainfall (mm)')
        plt.ylabel('PM10 (µg/m³)')
        plt.grid(True)

        plt.tight_layout()
        st.pyplot(plt)
        with st.expander('Show explanation'):
            st.markdown(
                """
                Konsentrasi PM2.5 dan PM10 saat curah hujan rendah cenderug lebih tinggi, dibandingkan ketika curah hujan meningkat konsentrasi PM2.5 dan PM10 cenderung menurun.
                """
            )

elif tabs_selection == 'Conclusion':
    
    
    st.markdown(
        """
        ### **Conclusion**
        Dari analisis data yang telah dilakukan terhadap dataset Air Quality, disimpulkan bahwa:
        1. Bagaimana tren polutan (PM2.5, PM10, SO2, NO2, CO, dan O3) berubah dari tahun ke tahun?
            - Pada periode 2014 hingga 2016, konsentrasi polutan seperti PM2.5, PM10, SO2, dan NO2 menurun signifikan, namun pada 2017 terjadi lonjakan polutan. Sementara itu, konsentrasi Ozone (O3) mencapai puncaknya pada 2015 dan turun drastis pada 2017.
        2. Bagaimana perubahan tingkat polutan pada jam-jam tertentu?
            - Analisis berdasarkan waktu menunjukkan fluktuasi konsentrasi polutan sepanjang hari. PM2.5 dan PM10 menurun signifikan pada malam hingga pagi (00:00–08:00), kemudian meningkat menjelang sore dan puncaknya terjadi sekitar pukul 20:00–23:00,
            - SO2 turun pada malam hingga pagi (00:00–06:00) dan kemudian naik hingga puncaknya pada pukul 11:00, sebelum turun lagi pada siang hari (12:00–18:00).
            - NO2 dan CO turun pada pagi hingga sore (08:00–16:00) dan kemudian melonjak pada malam hari (22:00–23:00).
            - O3, berbeda dengan polutan lainnya, meningkat pada pagi hingga sore (terutama pukul 15:00–16:00), lalu menurun pada malam hari.
        3. Apakah ada korelasi antar polutan (PM2.5, PM10, SO2, NO2, CO, dan O3)?
            - Analisis korelasi antar polutan menunjukkan bahwa PM2.5 dan PM10 sangat terkait dengan polutan lain seperti CO dan NO2. Artinya saat konsentrasi PM2.5 dan PM10 meningkat, CO dan NO2 juga cenderung meningkat. Sebaliknya, O3 memiliki pola yang lebih independen dan tidak terpengaruh langsung oleh polutan lain.
        4. Apakah curah hujan mempengaruhi konsentrasi polutan terutama PM2.5 dan PM10?
            - Analisis menunjukkan bahwa hubungan antara curah hujan (RAIN) dan konsentrasi polutan relatif lemah. Hujan tidak secara langsung mempengaruhi konsentrasi PM2.5 dan PM10. Namun, saat curah hujan rendah PM2.5 dan PM10 cenderung lebih tinggi. Sebaliknya, saat hujan meningkat, konsentrasi kedua polutan ini cenderung menurun.
        """
    )
    