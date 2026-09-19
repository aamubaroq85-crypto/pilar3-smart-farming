import math
import streamlit as st

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Pilar II - Pest & Pathogen Engine",
    page_icon="🛡️",
    layout="wide"
)

class ZuhriPillarIIEngine:
    """
    Engine Pilar II: Pengendalian Hama & Penyakit Geometris
    Berbasis Zuhri Formalism Constant (\pi_eff)
    """
    def __init__(self, pi_eff: float = 3.141592653589793):
        self.pi_eff = pi_eff

    def calculate_pesticide_efficacy(self, base_dose: float, surface_tension: float, 
                                     vpd_kpa: float, spray_pressure_bar: float) -> dict:
        """
        2. Bio-Pesticide Efficacy Amplifier (30)
        Mengkalkulasi efikasi penetrasi dan amplifikasi dosis aplikasi semprot.
        """
        # Faktor Penetrasi Vaskular berdasarkan VPD dan Tekanan Semprot
        penetration_factor = (spray_pressure_bar * math.log(self.pi_eff + 1)) / (surface_tension + 0.1)
        
        # Amplifikasi Efikasi Efektif (E_eff)
        efficacy_boost = (penetration_factor * self.pi_eff) / (vpd_kpa + 0.5)
        
        # Dosis Optimal Efektif (Mencegah pemborosan bahan aktif)
        effective_dose = base_dose * (1 / (1 + math.exp(-efficacy_boost / 10)))

        return {
            "penetration_factor": round(penetration_factor, 3),
            "efficacy_boost_percent": round(efficacy_boost * 100, 2),
            "optimized_dose_ml_per_l": round(effective_dose, 2)
        }

    def calculate_spore_disruption(self, humidity_rh: float, temp_c: float, 
                                  spore_density_index: float) -> dict:
        """
        1. Fungal Spore Resonance Disruptor (26)
        Memprediksi risiko spora jamur dan kalkulasi frekuensi gelombang pemutus dinding kitin.
        """
        # Indeks Risiko Inveksi Jamur (Fungal Risk Index)
        fungal_risk = (humidity_rh * temp_c * spore_density_index) / (self.pi_eff * 100)
        
        # Kalkulasi Frekuensi Resonansi Disruptif (kHz) untuk melumpuhkan spora
        disruption_freq_khz = (fungal_risk * self.pi_eff * 12.5)
        
        # Durasi Radiasi Resonansi Ideal (Menit)
        radiation_duration_min = (fungal_risk / self.pi_eff) * 15

        return {
            "fungal_risk_index": round(fungal_risk, 2),
            "disruption_frequency_khz": round(disruption_freq_khz, 2),
            "recommended_duration_min": round(min(radiation_duration_min, 120.0), 1)
        }

# UI Streamlit
st.title("🛡️ Smart Farming Engine: Pilar II")
st.caption("Bio-Pesticide Efficacy Amplifier & Fungal Spore Resonance Disruptor (π_eff)")

# Sidebar Parameter Input
st.sidebar.header("⚙️ Input Parameter Proteksi Lahan")

st.sidebar.subheader("1. Parameters Aplikasi Semprot")
dosis_basis = st.sidebar.number_input("Dosis Standard Bahan (ml/L)", value=2.0, step=0.1)
tegangan_permukaan = st.sidebar.number_input("Tegangan Permukaan (mN/m)", value=32.0, step=1.0)
tekanan_bar = st.sidebar.number_input("Tekanan Pompa Sanchin (Bar)", value=25.0, step=1.0)

st.sidebar.subheader("2. Parameters Lingkungan & Patogen")
vpd_input = st.sidebar.number_input("VPD Lahan (kPa)", value=1.031, step=0.1)
rh_input = st.sidebar.number_input("Kelembapan Udara (RH %)", value=75.0, step=1.0)
temp_input = st.sidebar.number_input("Suhu Udara (°C)", value=29.5, step=0.5)
spore_index = st.sidebar.number_input("Indeks Kepadatan Spora (1-10)", value=4.5, step=0.5)

engine = ZuhriPillarIIEngine()

# Kalkulasi Data
efficacy_data = engine.calculate_pesticide_efficacy(dosis_basis, tegangan_permukaan, vpd_input, tekanan_bar)
spore_data = engine.calculate_spore_disruption(rh_input, temp_input, spore_index)

# Tampilan Hasil Output
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧪 Amplifikasi Bio-Pestisisda")
    st.metric("Dosis Optimal Terkalibrasi", f"{efficacy_data['optimized_dose_ml_per_l']} ml/L")
    st.metric("Amplifikasi Efikasi", f"{efficacy_data['efficacy_boost_percent']} %")
    st.metric("Faktor Penetrasi Kutikula", efficacy_data["penetration_factor"])

with col2:
    st.subheader("🔬 Resonansi Pemutus Spora Jamur")
    st.metric("Indeks Risiko Jamur", spore_data["fungal_risk_index"])
    st.metric("Frekuensi Disruptif Target", f"{spore_data['disruption_frequency_khz']} kHz")
    st.metric("Rekomendasi Durasi Radiasi", f"{spore_data['recommended_duration_min']} Menit")

# Status Alert
st.markdown("---")
if spore_data["fungal_risk_index"] > 3.0:
    st.warning("⚠️ **Peringatan Risiko Jamur Tinggi:** Diperlukan aktivasi pemancar frekuensi atau penyemprotan protektif segera setelah hujan/kondisi embun pekat.")
else:
    st.success("✅ **Kondisi Aman:** Risiko infeksi spora patogen berada dalam batas ambang toleransi aman.")
