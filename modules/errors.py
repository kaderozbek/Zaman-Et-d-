# path: modules/errors.py
import streamlit as st

def render_error_inputs():
    if "error_data" not in st.session_state:
        st.session_state["error_data"] = []

    st.markdown("### ➕ Yeni Duruş Ekle")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        durus_turu = st.selectbox("Duruş Türü", ["Planlı", "Plansız"], key="type_input")
    with col2:
        sure = st.number_input("Süre (saniye)", min_value=0, key="duration_input")
    with col3:
        aciklama = st.text_input("Duruş Açıklaması", key="desc_input")
    with col4:
        if st.button("Duruş Ekle"):
            if durus_turu and sure >= 0 and aciklama:
                st.session_state["error_data"].append({
                    "Duruş Türü": durus_turu,   # <- yeni ad
                    "Süre (sn)": sure,
                    "Açıklama": aciklama
                })
                st.success("Duruş eklendi.")
                st.rerun()
            else:
                st.error("Lütfen tüm alanları doldurun.")

    if st.session_state["error_data"]:
        st.markdown("### 📋 Duruş Kayıtları")
        for i, row in enumerate(st.session_state["error_data"]):
            # geriye dönük uyumluluk: eski "Hata Türü" ismi varsa oku
            tur = row.get("Duruş Türü", row.get("Hata Türü", "—"))
            col1, col2, col3, col4 = st.columns([2, 2, 4, 1])
            col1.write(f"Tür: {tur}")
            col2.write(f"Süre: {row.get('Süre (sn)',0)} sn")
            col3.write(f"Açıklama: {row.get('Açıklama','—')}")
            if col4.button("❌", key=f"delete_{i}"):
                st.session_state["error_data"].pop(i)
                st.rerun()
