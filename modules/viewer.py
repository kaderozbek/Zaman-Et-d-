import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def render_summary_charts(error_data):
    """Hata verilerini grafiksel olarak görselleştirir."""
    if not error_data:
        st.info("Henüz hata verisi yok.")
        return

    # Hata verilerini DataFrame'e dönüştür
    df = pd.DataFrame(error_data)

    # Hata Türlerine Göre Dağılım (Pie Chart)
    st.subheader("📊 Hata Türlerine Göre Dağılım (Pie Chart)")
    pie_data = df.groupby("Hata Türü")["Süre (sn)"].sum()

    # Pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Daire şeklinde göster
    st.pyplot(fig1)

    # Hatalara Göre Süre Dağılımı (Bar Chart)
    st.subheader("📈 Hatalara Göre Süre Dağılımı (Bar Chart)")
    bar_data = df.groupby("Açıklama")["Süre (sn)"].sum().sort_values(ascending=False)

    # Bar chart
    st.bar_chart(bar_data)

def render_error_summary_table(error_data):
    """Hata verilerini özet tablo şeklinde gösterir."""
    if not error_data:
        st.info("Henüz hata verisi yok.")
        return

    df = pd.DataFrame(error_data)
    st.subheader("Hata Verilerinin Özeti")
    st.dataframe(df)  # Hata verilerini bir tablo şeklinde gösterir

