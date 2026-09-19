import math
import streamlit as st

# Set Konfigurasi Halaman
st.set_page_config(
    page_title="Pilar III - Flux & Yield Engine",
    page_icon="🌱",
    layout="wide"
)

class ZuhriPillarIIIEngine:
    def __init__(self, pi_eff: float = 3.141592653589793):
        self.pi_eff = pi_eff

    def calculate_daily_flux_variables(self, temp_c: float, rh_percent: float, 
                                     solar_rad: float, soil_ec: float) -> dict:
        rh_ratio = rh_percent / 100.0
        vps = 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
        vpa = vps * rh_ratio
        vpd = vps - vpa

        phi_trans = (solar_rad * vpd * self.pi_eff) / (rh_ratio + 0.1)
        v_xylem = (phi_trans * 0.75) / self.pi_eff
        v_phloem = (solar_rad * 0.25) * self.pi_eff
        vascular_ratio = v_xylem / (v_phloem if v_phloem != 0 else 1.0)
        s_soil = (soil_ec * temp_c) / self.pi_eff

        return {
            "vpd_kpa": round(vpd, 3),
            "phi_transpiration": round(phi_trans, 2),
            "vascular_ratio": round(vascular_ratio, 3),
            "soil_entropy_index": round(s_soil, 2)
        }

    def predict_yield_realtime(self, lai: float, flux_data: dict, 
                              land_area_m2: float) -> dict:
        phi_trans = flux_data.get("phi_transpiration", 0.0)
        s_soil = flux_data.get("soil_entropy_index", 0.0)

        lai_eff = lai * math.log(self.pi_eff + 1)
        k_harvest = (lai_eff * phi_trans) / (self.pi_eff ** 2)
        delta_e = math.exp(-s_soil / (self.pi_eff * 10))

        yield_per_m2 = (k_harvest * delta_e) * 0.15
        total_yield_kg = yield_per_m2 * land_area_m2

        return {
            "effective_lai": round(lai_eff, 2),
            "harvest_index_k": round(k_harvest, 4),
            "stress_correction_factor": round(delta_e, 4),
            "predicted_yield_per_m2_kg": round(yield_per_m2, 3),
            "total_predicted_yield_kg": round(total_yield_kg, 2)
        }

# UI Streamlit
st.title("🌱 Smart Farming Engine: Pilar III")
st.caption("Daily Routine Flux Variable Monitor & Real-Time Yield Predictive Algorithm (π_eff)")

# Sidebar Parameter Input
st.sidebar.header("⚙️ Input Parameter Lahan")
suhu = st.sidebar.number_input("Suhu Udara (°C)", value=29.5, step=0.5)
kelembapan = st.sidebar.number_input("Kelembapan Udara (RH %)", value=75.0, step=1.0)
radiasi = st.sidebar.number_input("Radiasi Surya (MJ/m²/hari)", value=18.5, step=0.5)
ec_tanah = st.sidebar.number_input("EC Tanah (mS/cm)", value=1.8, step=0.1)
lai = st.sidebar.number_input("Leaf Area Index (LAI)", value=3.2, step=0.1)
luas_lahan = st.sidebar.number_input("Luas Lahan (m²)", value=1000.0, step=50.0)

engine = ZuhriPillarIIIEngine()

# Kalkulasi
flux_data = engine.calculate_daily_flux_variables(suhu, kelembapan, radiasi, ec_tanah)
yield_data = engine.predict_yield_realtime(lai, flux_data, luas_lahan)

# Tampilan Hasil
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Fluks Harian (Monitor)")
    st.metric("VPD (kPa)", flux_data["vpd_kpa"])
    st.metric("Fluks Transpirasi (Φ_trans)", flux_data["phi_transpiration"])
    st.metric("Rasio Vaskular (Xylem/Phloem)", flux_data["vascular_ratio"])
    st.metric("Indeks Entropi Tanah", flux_data["soil_entropy_index"])

with col2:
    st.subheader("📈 Prediksi Panen (Real-Time)")
    st.metric("Total Estimasi Panen (Kg)", f"{yield_data['total_predicted_yield_kg']:,} kg")
    st.metric("Estimasi per m²", f"{yield_data['predicted_yield_per_m2_kg']} kg/m²")
    st.metric("LAI Efektif", yield_data["effective_lai"])
    st.metric("Faktor Koreksi Stres (ΔE)", yield_data["stress_correction_factor"])
