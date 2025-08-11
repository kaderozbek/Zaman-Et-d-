import streamlit as st

def render_etud_info():
    st.subheader("🕐 Etüt Bilgileri")

    start_time = st.time_input("Etüt Başlangıç Saati", key="start_time")
    end_time = st.time_input("Etüt Bitiş Saati", key="end_time")

    initial_count = st.number_input("Etüt Öncesi Yatak Sayısı", min_value=0, key="initial_count")
    final_count = st.number_input("Etüt Sonrası Yatak Sayısı", min_value=0, key="final_count")

    unit_time = st.number_input("Bir Yatak Oluşma Süresi (dakika)", min_value=0.1, key="unit_time")

    if start_time >= end_time:
        st.error("Bitiş saati, başlangıç saatinden sonra olmalıdır.")
        return None

    return start_time, end_time, initial_count, final_count, unit_time
