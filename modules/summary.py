# path: modules/summary.py
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import datetime

def _to_stops_df(error_data):
    """Eski 'Hata Türü' verilerini 'Duruş Türü' şemasına çevir."""
    df = pd.DataFrame(error_data) if error_data else pd.DataFrame()
    if df.empty:
        return pd.DataFrame(columns=["Duruş Türü","Süre (sn)","Açıklama"])
    df = df.copy()
    if "Duruş Türü" not in df.columns and "Hata Türü" in df.columns:
        df["Duruş Türü"] = df["Hata Türü"]
    if "Süre (sn)" not in df.columns:
        df["Süre (sn)"] = 0
    if "Açıklama" not in df.columns:
        df["Açıklama"] = ""
    return df[["Duruş Türü","Süre (sn)","Açıklama"]]

def calculate_summary(error_data, start_time, end_time, produced_beds, unit_time, break_time):
    df = _to_stops_df(error_data)

    total_etud_minutes = (
        datetime.datetime.combine(datetime.date.today(), end_time)
        - datetime.datetime.combine(datetime.date.today(), start_time)
    ).total_seconds() / 60
    total_etud_minutes = round(total_etud_minutes - float(break_time or 0), 2)

    if total_etud_minutes <= 0:
        st.error("Etüt süresi geçersiz. Lütfen başlangıç, bitiş ve mola değerlerini kontrol edin.")
        st.stop()

    total_planned_sec   = float(df.loc[df["Duruş Türü"] == "Planlı",   "Süre (sn)"].sum()) if not df.empty else 0.0
    total_unplanned_sec = float(df.loc[df["Duruş Türü"] == "Plansız", "Süre (sn)"].sum()) if not df.empty else 0.0
    total_errors_sec    = total_planned_sec + total_unplanned_sec

    # Planlanan üretim = (Etüt Süresi - Planlı duruş) / CT
    planned_available_minutes = max(total_etud_minutes - (total_planned_sec / 60.0), 0)
    planned_production = (planned_available_minutes / float(unit_time)) if float(unit_time) > 0 else 0

    # Net çalışma: planlı + plansız düş
    net_seconds = max(total_etud_minutes * 60 - total_errors_sec, 0)
    utilization = (net_seconds / (total_etud_minutes * 60)) * 100 if total_etud_minutes > 0 else 0
    performance = (float(produced_beds) / planned_production * 100) if planned_production > 0 else 0

    summary_df = pd.DataFrame({
        "Etüt Süresi (dk)": [round(total_etud_minutes, 2)],
        "Toplam Planlı Süre (sn)": [round(total_planned_sec, 2)],
        "Toplam Plansız Süre (sn)": [round(total_unplanned_sec, 2)],
        "Toplam Duruş Süresi (sn)": [round(total_errors_sec, 2)],
        "Kapasite Kullanımı (%)": [round(utilization, 2)],
        "Gerçekleşen Üretim (adet)": [int(produced_beds)],
        "Planlanan Üretim (adet)": [round(planned_production, 2)],
        "Gerçekleşme Oranı (%)": [round(performance, 2)],
    })
    return summary_df

def render_summary_table(summary_df: pd.DataFrame):
    planli_dk  = round(float(summary_df.loc[0,'Toplam Planlı Süre (sn)']) / 60, 2)
    plansiz_dk = round(float(summary_df.loc[0,'Toplam Plansız Süre (sn)']) / 60, 2)
    hatali_dk  = round(float(summary_df.loc[0,'Toplam Hatalı Süre (sn)']) / 60, 2)

    st.markdown(f"### ⏱️ Toplam Etüt Süresi: **{summary_df.loc[0,'Etüt Süresi (dk)']} dakika**")
    c1, c2, c3 = st.columns(3)
    c1.metric("🟡 Planlı Duruş", f"{planli_dk} dk")
    c2.metric("🔴 Plansız Duruş", f"{plansiz_dk} dk")
    c3.metric("📈 Kapasite Kullanımı", f"{summary_df.loc[0,'Kapasite Kullanımı (%)']} %")

    df_dk = summary_df.copy()
    df_dk["Toplam Planlı Süre (dk)"]  = planli_dk
    df_dk["Toplam Plansız Süre (dk)"] = plansiz_dk
    df_dk["Toplam Hatalı Süre (dk)"]  = hatali_dk
    df_dk.drop(columns=["Toplam Planlı Süre (sn)","Toplam Plansız Süre (sn)","Toplam Hatalı Süre (sn)"], inplace=True)

    st.markdown("### 📋 Detaylı Tablo")
    st.dataframe(df_dk)

def render_summary_charts(error_data, summary_df: pd.DataFrame):
    df = _to_stops_df(error_data)
    if not df.empty:
        st.subheader("📊 Duruş Türlerine Göre Dağılım (Pie)")
        pie_data = df.groupby("Duruş Türü")["Süre (sn)"].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

        st.subheader("📈 Planlı Duruşlar (dk)")
        planned_bar = (df[df["Duruş Türü"] == "Planlı"].groupby("Açıklama")["Süre (sn)"].sum() / 60).round(2).sort_values(ascending=False)
        if not planned_bar.empty:
            st.bar_chart(planned_bar)

        st.subheader("📉 Plansız Duruşlar (dk)")
        unplanned_bar = (df[df["Duruş Türü"] == "Plansız"].groupby("Açıklama")["Süre (sn)"].sum() / 60).round(2).sort_values(ascending=False)
        if not unplanned_bar.empty:
            st.bar_chart(unplanned_bar)

    st.subheader("🏁 Planlanan vs Gerçekleşen Üretim")
    planned = float(summary_df.loc[0,"Planlanan Üretim (adet)"])
    actual  = float(summary_df.loc[0,"Gerçekleşen Üretim (adet)"])
    st.bar_chart(pd.DataFrame({"Üretim":[planned, actual]}, index=["Planlanan","Gerçekleşen"]))

