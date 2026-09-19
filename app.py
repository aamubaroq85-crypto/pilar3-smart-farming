import math
import streamlit as st

st.set_page_config(
    page_title="Smart Farming Engine - Integrated System",
    page_icon="🌱",
    layout="wide"
)

# ==========================================
# ZUHRI FORMALISM ENGINES (PILLAR I - IV)
# ==========================================

class ZuhriPillarI:
    def __init__(self, pi_eff: float = 3.141592653589793):
        self.pi_eff = pi_eff

    def calculate_humic_synthesis(self, organic_matter_pct: float, soil_ph: float, moisture_pct: float) -> dict:
        ph_resonance = math.exp(-abs(soil_ph - 7.0) / self.pi_eff)
        humic_synth_rate = (organic_matter_pct * (moisture_pct / 100.0) * self.pi_eff) * ph_resonance
        pore_stability_index = (humic_synth_rate * soil_ph) / self.pi_eff
        return {
            "ph_resonance_factor": round(ph_resonance, 4),
            "humic_synthesis_rate_kg_ha": round(humic_synth_rate, 2),
            "pore_stability_index": round(pore_stability_index, 2)
        }

    def calculate_nutrient_availability(self, npk_input_kg: float, ec_tanah: float, moisture_pct: float) -> dict:
        ionic_solubility = (ec_tanah * (moisture_pct / 100.0) * self.pi_eff)
        effective_npk_absorbed = npk_input_kg * (1 - math.exp(-ionic_solubility / 5.0))
        absorption_efficiency = (effective_npk_absorbed / npk_input_kg) * 100 if npk_input_kg > 0 else 0.0
        return {
            "ionic_solubility_index": round(ionic_solubility, 3),
            "effective_npk_absorbed_kg": round(effective_npk_absorbed, 2),
            "absorption_efficiency_pct": round(absorption_efficiency, 2)
        }

class ZuhriPillarII:
    def __init__(self, pi_eff: float = 3.141592653589793):
        self.pi_eff = pi_eff

    def calculate_efficacy(self, base_dose: float, surface_tension: float, vpd_kpa: float, spray_pressure_bar: float) -> dict:
        penetration_factor = (spray_pressure_bar * math.log(self.pi_eff + 1)) / (surface_tension + 0.1)
        efficacy_boost = (penetration_factor * self.pi_eff) / (vpd_kpa + 0.5)
        effective_dose = base_dose * (1 / (1 + math.exp(-efficacy_boost / 10)))
        return {
            "penetration_factor": round(penetration_factor, 3),
            "efficacy_boost_percent": round(efficacy_boost * 100, 2),
            "optimized_dose_ml_per_l": round(effective_dose, 2)
        }

    def calculate_spore_disruption(self, humidity_rh: float, temp_c: float, spore_density_index: float) -> dict:
        fungal_risk = (humidity_rh * temp_c * spore_density_index) / (self.pi_eff * 100)
        disruption_freq_khz = (fungal_risk * self.pi_eff * 12.5)
        radiation_duration_min = (fungal_risk / self.pi_eff) * 15
        return {
            "fungal_risk_index": round(fungal_risk, 2),
            "disruption_frequency_khz": round(disruption_freq_khz, 2),
            "recommended_duration_min": round(min(radiation_duration_min, 120.0), 1)
        }

class ZuhriPillarIII:
    def __init__(self, pi_eff: float = 3.141592653589793):
        self.pi_eff = pi_eff

    def calculate_daily_flux(self, temp_c: float, rh_percent: float, solar_rad: float, soil_ec: float) -> dict:
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

class ZuhriPillarIV:
    def __init__(self, pi_eff: float = 3.141592653589793):
        self.pi_eff = pi_eff

    def calculate_yield_matrix(self, total_harvest_kg: float, price_per_kg: float) -> dict:
        grade_a_pct = (1 - math.exp(-self.pi_eff)) * 100
        grade_a_kg = total_harvest_kg * (grade_a_pct / 100.0)
        gross_revenue = total_harvest_kg * price_per_kg
        return {
            "grade_a_percentage": round(grade_a_pct, 2),
            "grade_a_kg": round(grade_a_kg, 2),
            "gross_revenue_rp": gross_revenue
        }

    def route_distribution(self, gross_revenue: float, tabarot_pct: float) -> dict:
        # Dana Sosial & Bantuan TABAROT
        tabarot_fund = gross_revenue * (tabarot_pct / 100.0)
        remaining = gross_revenue - tabarot_fund
        
        # Flux Balancer: 40% Reinvestasi Lahan, 60% Perencanaan Rumah Tangga
        farm_reinvestment = remaining * 0.40
        household_planning = remaining * 0.60
        
        return {
            "tabarot_fund_rp": tabarot_fund,
            "household_planning_rp": household_planning,
            "farm_reinvestment_rp": farm_reinvestment
        }

# ==========================================
# STREAMLIT UI & NAVIGATION
# ==========================================

st.sidebar.title("🎮 Navigasi Modul")
modul_pilihan = st.sidebar.radio(
    "Pilih Pilar Operasional:",
    [
        "Pilar III: Irigasi & Pemantauan Rutin", 
        "Pilar II: Proteksi Hama & Patogen",
        "Pilar I: Manajemen Tanah & Nutrisi",
        "Pilar IV: Logistik & Distribusi"
    ]
)

st.sidebar.markdown("---")

if modul_pilihan == "Pilar III: Irigasi & Pemantauan Rutin":
    st.title("🌱 Smart Farming Engine: Pilar III")
    st.sidebar.header("⚙️ Input Parameter Lahan")
    suhu = st.sidebar.number_input("Suhu Udara (°C)", value=29.5, step=0.5)
    kelembapan = st.sidebar.number_input("Kelembapan Udara (RH %)", value=75.0, step=1.0)
    radiasi = st.sidebar.number_input("Radiasi Surya (MJ/m²/hari)", value=18.5, step=0.5)
    ec_tanah = st.sidebar.number_input("EC Tanah (mS/cm)", value=1.8, step=0.1)
    lai = st.sidebar.number_input("LAI", value=3.2, step=0.1)
    luas_lahan = st.sidebar.number_input("Luas Lahan (m²)", value=1000.0, step=50.0)

    engine = ZuhriPillarIII()
    flux = engine.calculate_daily_flux(suhu, kelembapan, radiasi, ec_tanah)
    yield_est = engine.predict_yield(lai, flux, luas_lahan)

    c1, c2 = st.columns(2)
    c1.metric("VPD (kPa)", flux["vpd_kpa"])
    c1.metric("Fluks Transpirasi", flux["phi_transpiration"])
    c2.metric("Estimasi Panen (Kg)", f"{yield_est['total_predicted_yield_kg']:,}")
    c2.metric("Faktor Stres (ΔE)", yield_est["stress_correction_factor"])

elif modul_pilihan == "Pilar II: Proteksi Hama & Patogen":
    st.title("🛡️ Smart Farming Engine: Pilar II")
    st.sidebar.subheader("Input Semprot & Patogen")
    dosis = st.sidebar.number_input("Dosis (ml/L)", value=2.0)
    tegangan = st.sidebar.number_input("Tegangan (mN/m)", value=32.0)
    tekanan = st.sidebar.number_input("Tekanan (Bar)", value=25.0)
    vpd = st.sidebar.number_input("VPD Lahan", value=1.031)
    rh = st.sidebar.number_input("RH (%)", value=75.0)
    temp = st.sidebar.number_input("Suhu (°C)", value=29.5)
    spora = st.sidebar.number_input("Indeks Spora", value=4.5)

    engine = ZuhriPillarII()
    eff = engine.calculate_efficacy(dosis, tegangan, vpd, tekanan)
    disrupt = engine.calculate_spore_disruption(rh, temp, spora)

    c1, c2 = st.columns(2)
    c1.metric("Dosis Optimal", f"{eff['optimized_dose_ml_per_l']} ml/L")
    c2.metric("Frekuensi Disruptif", f"{disrupt['disruption_frequency_khz']} kHz")
    c2.metric("Indeks Risiko Jamur", disrupt["fungal_risk_index"])

elif modul_pilihan == "Pilar I: Manajemen Tanah & Nutrisi":
    st.title("🪨 Smart Farming Engine: Pilar I")
    st.sidebar.subheader("Input Tanah & Nutrisi")
    organik = st.sidebar.number_input("Bahan Organik (%)", value=4.5)
    ph = st.sidebar.number_input("pH Tanah", value=6.2)
    air = st.sidebar.number_input("Kadar Air (%)", value=55.0)
    npk = st.sidebar.number_input("Input NPK (kg/ha)", value=150.0)
    ec = st.sidebar.number_input("EC Tanah (mS/cm)", value=1.8)

    engine = ZuhriPillarI()
    humic = engine.calculate_humic_synthesis(organik, ph, air)
    nutrisi = engine.calculate_nutrient_availability(npk, ec, air)

    c1, c2 = st.columns(2)
    c1.metric("Laju Sintesis Humat", f"{humic['humic_synthesis_rate_kg_ha']} kg/ha/hari")
    c1.metric("Resonansi pH", humic["ph_resonance_factor"])
    c2.metric("Efisiensi Serapan NPK", f"{nutrisi['absorption_efficiency_pct']} %")

else:
    st.title("📦 Smart Farming Engine: Pilar IV")
    st.caption("Monthly Yield Calculation Matrix & Community Yield Distribution Router")

    st.sidebar.header("⚙️ Input Panen & Harga")
    total_panen = st.sidebar.number_input("Total Panen Bulanan (Kg)", value=850.0, step=10.0)
    harga_pasar = st.sidebar.number_input("Harga Pasar Aktual (Rp/Kg)", value=35000.0, step=1000.0)
    st.sidebar.markdown("---")
    st.sidebar.header("🤝 Alokasi Distribusi")
    persen_tabarot = st.sidebar.slider("Alokasi Kas/Bantuan TABAROT (%)", min_value=0.0, max_value=50.0, value=15.0, step=1.0)

    engine_p4 = ZuhriPillarIV()
    matrix = engine_p4.calculate_yield_matrix(total_panen, harga_pasar)
    dist = engine_p4.route_distribution(matrix["gross_revenue_rp"], persen_tabarot)

    st.subheader("📊 Hasil Panen & Valuasi Ekonomi")
    col1, col2, col3 = st.columns(3)
    col1.metric("Kualitas Grade A (%)", f"{matrix['grade_a_percentage']} %")
    col2.metric("Estimasi Grade A (Kg)", f"{matrix['grade_a_kg']} Kg")
    col3.metric("Gross Revenue (Kotor)", f"Rp {matrix['gross_revenue_rp']:,.0f}")

    st.markdown("---")
    st.subheader("⚖️ Alokasi Distribusi (Flux Balancer)")
    c1, c2, c3 = st.columns(3)
    
    c1.info("🛠️ **Reinvestasi Lahan**")
    c1.write(f"**Rp {dist['farm_reinvestment_rp']:,.0f}**")
    c1.caption("Pembelian input, paranet, maintenance Sanchin & Cultivator.")

    c2.success("🏠 **Perencanaan Rumah Tangga**")
    c2.write(f"**Rp {dist['household_planning_rp']:,.0f}**")
    c2.caption("Manajemen keuangan keluarga & tabungan pendidikan anak.")

    c3.warning("🤝 **Kas TABAROT**")
    c3.write(f"**Rp {dist['tabarot_fund_rp']:,.0f}**")
    c3.caption("Dana bantuan darurat, sosial & kegiatan relawan pemuda.")
