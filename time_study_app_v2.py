import os
import streamlit as st
import datetime
from PIL import Image

from modules.layout_v2 import render_etud_info_v2
from modules.errors import render_error_inputs
from modules.summary import calculate_summary, render_summary_table, render_summary_charts
from modules.storage import save_data, load_data
from modules.data_manager import export_current_session_to_excel, export_pretty_report

# Sayfa ayarları
st.set_page_config(page_title="Zaman Etüdü V2", layout="wide")
st.title("🕒 Zaman Etüdü Uygulaması - Form Bilgili Versiyon")

# Şirket logosu (opsiyonel)
logo = None
try:
    logo = Image.open("logo.png")
except Exception:
    pass

col1, col2 = st.columns([6, 1])
with col2:
    if logo:
        st.image(logo, width=130)

# Başlangıç state
if "error_data" not in st.session_state:
    st.session_state["error_data"] = []

# Etüt bilgileri
etud_info = render_etud_info_v2()
if etud_info is None:
    st.warning("Lütfen tüm etüt bilgilerini eksiksiz giriniz.")
    st.stop()

(operator, machine, etud_date, vardiya,
 start_time, end_time, initial_count, final_count,
 unit_time, break_time) = etud_info

produced_beds = max(0, final_count - initial_count)
if final_count < initial_count:
    st.warning("Etüt Sonrası sayım, Etüt Öncesi'nden küçük görünüyor. Üretim adedi 0 olarak alındı.")

# Bilgileri göster
st.info(f"👤 Operatör: {operator} | 🏭 Makine: {machine} | 📅 Tarih: {etud_date} | 🕒 Vardiya: {vardiya}")

# Hata girişi
st.subheader("🔧 Duruş Giriş Alanı")
render_error_inputs()

# Özet
st.subheader("📊 Özet Tablo ve Üretim Verileri")
df_summary = calculate_summary(
    error_data=st.session_state["error_data"],
    start_time=start_time,
    end_time=end_time,
    produced_beds=produced_beds,
    unit_time=unit_time,
    break_time=break_time
)
render_summary_table(df_summary)
render_summary_charts(st.session_state["error_data"], df_summary)


# --- Excel çıktı 1: Ham tablo ---
if st.button("📤 Excel'e Aktar (Ham Tablo)", key="export_raw"):
    excel_path = export_current_session_to_excel(etud_info, st.session_state["error_data"])
    if excel_path:
        with open(excel_path, "rb") as f:
            st.download_button("📥 Excel Dosyasını İndir", f, file_name=os.path.basename(excel_path), key="dl_raw")

# --- Excel çıktı 2: Tek sayfa rapor ---
if st.button("🧾 Tek Sayfa Raporu Oluştur (Excel)", key="export_pretty"):
    try:
        out_path = os.path.join("excel_raporlar", f"etut_raporu_pretty_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        export_pretty_report(etud_info, st.session_state["error_data"], df_summary, out_path)
        st.session_state["pretty_report_path"] = out_path
        st.success("Rapor hazır. Aşağıdan indirebilirsiniz.")
    except ImportError as e:
        st.error(str(e))

if "pretty_report_path" in st.session_state:
    with open(st.session_state["pretty_report_path"], "rb") as f:
        st.download_button("📥 Raporu İndir (Excel)", f,
                           file_name=os.path.basename(st.session_state["pretty_report_path"]),
                           key="dl_pretty")
