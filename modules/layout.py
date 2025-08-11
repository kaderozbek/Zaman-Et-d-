

import streamlit as st
import datetime

def render_etud_info_v2():
    st.subheader("🕐 Etüt Bilgileri")

    operator = st.text_input("Operatör Adı")
    machine = st.text_input("Makine Adı / Numarası")
    etud_date = st.date_input("Etüt Tarihi", value=datetime.date.today())
    vardiya = st.selectbox("Vardiya", ["1. Vardiya", "2. Vardiya",])

    start_time = st.time_input("Etüt Başlangıç Saati")
    end_time = st.time_input("Etüt Bitiş Saati")
    initial_count = st.number_input("Etüt Öncesi Yatak Sayısı", min_value=0)
    final_count = st.number_input("Etüt Sonrası Yatak Sayısı", min_value=0)
    unit_time = st.number_input("Bir Yatak Oluşma Süresi (dakika)", min_value=0.1)

    if start_time >= end_time:
        st.error("Bitiş saati, başlangıç saatinden sonra olmalıdır.")
        return None

    return operator, machine, etud_date, vardiya, start_time, end_time, initial_count, final_count, unit_time
