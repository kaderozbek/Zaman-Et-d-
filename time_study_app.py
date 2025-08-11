import streamlit as st
from modules.layout import render_etud_info
from modules.errors import render_error_inputs
from modules.summary import calculate_summary, render_summary_table

st.set_page_config(page_title="Zaman Etüdü", layout="wide")
st.title("🕒 Zaman Etüdü Uygulaması")

if "error_data" not in st.session_state:
    st.session_state["error_data"] = []

etud_info = render_etud_info()

if etud_info is None:
    st.warning("Etüt saatlerini seçmeden devam edemezsiniz.")
    st.stop()

# 👇 BURASI YANLIŞSA HATA VERİR – ama bu hali doğru
start_time, end_time, initial_count, final_count, unit_time = etud_info

st.subheader("🔧 Hata Giriş Alanı")
render_error_inputs()

st.subheader("📊 Özet Tablo ve Üretim Verileri")
df_summary = calculate_summary(
    error_data=st.session_state["error_data"],
    start_time=start_time,
    end_time=end_time,
    produced_beds=(final_count - initial_count)/unit_time,
    unit_time=unit_time
)

render_summary_table(df_summary)