import math
import streamlit as st

# Set Konfigurasi Halaman
st.set_page_config(
    page_title="Smart Farming Engine - Integrated System",
    page_icon="🌱",
    layout="wide"
)

# ==========================================
# ZUHRI FORMALISM ENGINES
# ==========================================
class ZuhriPillarIII:
    """Engine Pilar III: Irigasi, Mikroklimat & Pemantauan Rutin"""
    def __init__(self, pi_eff: float = 3.141592653589793):
        self.pi_eff = pi_eff

    def calculate_daily_flux(self, temp_c: float, rh_percent: float, 
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

    def predict_yield(self, lai: float, flux_data: dict, land_area_m2: float) -> dict:
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


class ZuhriPillarII:
    """Engine Pilar II: Pengendalian Hama & Penyakit Geometris"""
    def __init__(self, pi_eff: float = 3.141592653589793):
        self.pi_eff = pi_eff

    def calculate_efficacy(self, base_dose: float, surface_tension: float, 
                           vpd_kpa: float, spray_pressure_bar: float) -> dict:
        penetration_factor = (spray_pressure_bar * math.log(self.pi_eff + 1)) / (surface_tension + 0.1)
        efficacy_boost = (penetration_factor * self.pi_eff) / (vpd_kpa + 0.5)
        effective_dose = base_dose * (1 / (1 + math.exp(-efficacy_boost / 10)))

        return {
            "penetration_factor": round(penetration_factor, 3),
            "efficacy_boost_percent": round(efficacy_boost * 100, 2),
            "optimized_dose_ml_per_l": round(effective_dose, 2)
        }

    def calculate_spore_disruption(self, humidity_rh: float, temp_c: float, 
                                  spore_density_index: float) -> dict:
        fungal_risk = (humidity_rh * temp_c * spore_density_index) / (self.pi_eff * 100)
        disruption_freq_khz = (fungal_risk * self.pi_eff * 12.5)
        radiation_duration_min = (fungal_risk / self.pi_eff) * 15

        return {
            "fungal_risk_index": round(fungal_risk, 2),
            "disruption_frequency_khz": round(disruption_freq_khz, 2),
            "recommended_duration_min": round(min(radiation_duration_min, 120.0), 1)
        }

# ==========================================
# STREAMLIT UI & NAVIGATION
# ==========================================
st.sidebar.title("🎮 Navigasi Modul")
modul_pilihan = st.sidebar.radio(
    "Pilih Pilar Operasional:",
    ["Pilar III: Irigasi & Pemantauan Rutin", "Pilar II: Proteksi Hama & Patogen"]
)

st.sidebar.markdown("---")

# ------------------------------------------
# MODUL 1: PILAR III
# ------------------------------------------
if modul_pilihan == "Pilar III: Irigasi & Pemantauan Rutin":
    st.title("🌱 Smart Farming Engine: Pilar III")
    st.caption("Daily Routine Flux Variable Monitor & Real-Time Yield Predictive Algorithm (π_eff)")

    st.sidebar.header("⚙️ Input Parameter Lahan")
    suhu = st.sidebar.number_input("Suhu Udara (°C)", value=29.5, step=0.5)
    kelembapan = st.sidebar.number_input("Kelembapan Udara (RH %)", value=75.0, step=1.0)
    radiasi = st.sidebar.number_input("Radiasi Surya (MJ/m²/hari)", value=18.5, step=0.5)
    ec_tanah = st.sidebar.number_input("EC Tanah (mS/cm)", value=1.8, step=0.1)
    lai = st.sidebar.number_input("Leaf Area Index (LAI)", value=3.2, step=0.1)
    luas_lahan = st.sidebar.number_input("Luas Lahan (m²)", value=1000.0, step=50.0)

    engine_p3 = ZuhriPillarIII()
    flux_data = engine_p3.calculate_daily_flux(suhu, kelembapan, radiasi, ec_tanah)
    yield_data = engine_p3.predict_yield(lai, flux_data, luas_lahan)

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

# ------------------------------------------
# MODUL 2: PILAR II
# ------------------------------------------
else:
    st.title("🛡️ Smart Farming Engine: Pilar II")
    st.caption("Bio-Pesticide Efficacy Amplifier & Fungal Spore Resonance Disruptor (π_eff)")

    st.sidebar.header("⚙️ Input Parameter Proteksi")
    st.sidebar.subheader("1. Aplikasi Semprot")
    dosis_basis = st.sidebar.number_input("Dosis Standard (ml/L)", value=2.0, step=0.1)
    tegangan_permukaan = st.sidebar.number_input("Tegangan Permukaan (mN/m)", value=32.0, step=1.0)
    tekanan_bar = st.sidebar.number_input("Tekanan Pompa Sanchin (Bar)", value=25.0, step=1.0)

    st.sidebar.subheader("2. Lingkungan & Patogen")
    vpd_input = st.sidebar.number_input("VPD Lahan (kPa)", value=1.031, step=0.1)
    rh_input = st.sidebar.number_input("Kelembapan Udara (RH %)", value=75.0, step=1.0)
    temp_input = st.sidebar.number_input("Suhu Udara (°C)", value=29.5, step=0.5)
    spore_index = st.sidebar.number_input("Indeks Kepadatan Spora (1-10)", value=4.5, step=0.5)

    engine_p2 = ZuhriPillarII()
    efficacy_data = engine_p2.calculate_efficacy(dosis_basis, tegangan_permukaan, vpd_input, tekanan_bar)
    spore_data = engine_p2.calculate_spore_disruption(rh_input, temp_input, spore_index)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧪 Amplifikasi Bio-Pestisida")
        st.metric("Dosis Optimal Terkalibrasi", f"{efficacy_data['optimized_dose_ml_per_l']} ml/L")
        st.metric("Amplifikasi Efikasi", f"{efficacy_data['efficacy_boost_percent']} %")
        st.metric("Faktor Penetrasi Kutikula", efficacy_data["penetration_factor"])

    with col2:
        st.subheader("🔬 Resonansi Pemutus Spora Jamur")
        st.metric("Indeks Risiko Jamur", spore_data["fungal_risk_index"])
        st.metric("Frekuensi Disruptif Target", f"{spore_data['disruption_frequency_khz']} kHz")
        st.metric("Rekomendasi Durasi Radiasi", f"{spore_data['recommended_duration_min']} Menit")

    st.markdown("---")
    if spore_data["fungal_risk_index"] > 3.0:
        st.warning("⚠️ **Peringatan Risiko Jamur Tinggi:** Diperlukan aktivasi pemancar frekuensi atau penyemprotan protektif segera.")
    else:
        st.success("✅ **Kondisi Aman:** Risiko infeksi spora patogen berada dalam batas ambang toleransi aman.")
