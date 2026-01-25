import streamlit as st
import pandas as pd
import numpy as np
import ai_engine  # Aapnu Brain
from datetime import datetime
import time 
from fpdf import FPDF 
import base64

# ---------------- CONFIGURATION ----------------
st.set_page_config(
    page_title="MSME Squad",
    page_icon="🏭",
    layout="wide"
)

# ---------------- 🌐 TRANSLATION DICTIONARY ----------------
translations = {
    "English": {
        "nav_overview": "📊 Executive Overview",
        "nav_maint": "🛠 Predictive Maintenance",
        "nav_inv": "📦 Smart Inventory",
        "nav_energy": "⚡ Energy Optimizer",
        "nav_quality": "🔍 Quality Control",
        "title": "🏭 Factory Command Center",
        "subtitle": "Real-time Operational Intelligence & Financial Risk Analysis",
        "upload_header": "📂 UPLOAD DATASETS (Maintenance, Inventory, Energy)",
        "hero_eff": "🏭 Overall Efficiency",
        "hero_risk": "💰 Estimated Risk Cost",
        "hero_alerts": "🚨 Active Alerts",
        "hero_production": "📦 Production Target",
        "chat_placeholder": "Ask about factory...",
        "btn_download": "📥 Download Report",
        "btn_refresh": "🔄 Refresh",
        "stat_vib": "⚙️ Avg Vibration",
        "stat_top_prod": "🔥 Top Product",
        "stat_peak": "⚡ Peak Load",
        "stat_roi": "🌱 Carbon ROI Potential",
        "ai_center": "🤖 AI Decision Center (Prioritized Actions)",
        "chat_title": "💬 AI Assistant",
        
        # Insights Messages
        "insight_wait": "ℹ️ Upload data files above to generate AI Decisions.",
        "insight_maint_risk": "🔴 **URGENT:** Maintenance needed for **{count} machines**. Estimated risk: {cost}",
        "insight_maint_ok": "🟢 **Maintenance:** All machines healthy.",
        "insight_prod": "📦 **Production:** Prioritize **'{prod}'** batch.",
        "insight_energy_waste": "⚡ **Profit Opportunity:** Fix {hours} hours of waste. Earn {rev} in Carbon Credits.",
        "insight_energy_ok": "✅ **Energy:** Consumption is optimized.",

        # Chatbot Messages
        "bot_nodata": "⚠️ Please upload data in 'Executive Overview' first.",
        "bot_risk_high": "⚠️ ALERT: {count} Machines are Critical! Check immediately.",
        "bot_risk_ok": "✅ All Machines are healthy. No issues.",
        "bot_prod": "📦 Forecast: {total} Units. Top Product: {top}.",
        "bot_energy_waste": "⚡ WARNING: {count} Hours of high waste detected.",
        "bot_energy_ok": "🌱 Energy consumption is efficient.",
        "bot_confused": "Sorry, I didn't understand. Try 'Status', 'Risk' or 'Profit'."
    },
    "Gujarati": {
        "nav_overview": "📊 મુખ્ય ડેશબોર્ડ",
        "nav_maint": "🛠 મશીન મેન્ટેનન્સ",
        "nav_inv": "📦 સ્માર્ટ ઇન્વેન્ટરી",
        "nav_energy": "⚡ એનર્જી સેવર",
        "nav_quality": "🔍 ક્વોલિટી ચેક",
        "title": "🏭 ફેક્ટરી કમાન્ડ સેન્ટર",
        "subtitle": "રીયલ-ટાઇમ ફેક્ટરી એનાલિટિક્સ અને જોખમ વિશ્લેષણ",
        "upload_header": "📂 ડેટા અપલોડ કરો (મશીન, સ્ટોક, વીજળી)",
        "hero_eff": "🏭 કુલ કાર્યક્ષમતા",
        "hero_risk": "💰 અંદાજિત નુકસાન",
        "hero_alerts": "🚨 એક્ટિવ એલર્ટ",
        "hero_production": "📦 ઉત્પાદન લક્ષ્ય (ટાર્ગેટ)",
        "chat_placeholder": "ફેક્ટરી વિશે પૂછો...",
        "btn_download": "📥 રિપોર્ટ ડાઉનલોડ કરો",
        "btn_refresh": "🔄 રીફ્રેશ કરો",
        "stat_vib": "⚙️ સરેરાશ વાઇબ્રેશન",
        "stat_top_prod": "🔥 મુખ્ય પ્રોડક્ટ",
        "stat_peak": "⚡ મહત્તમ લોડ",
        "stat_roi": "🌱 કાર્બન ક્રેડિટ કમાણી",
        "ai_center": "🤖 AI નિર્ણય કેન્દ્ર (મહત્વપૂર્ણ)",
        "chat_title": "💬 ફેક્ટરી આસિસ્ટન્ટ",

        # Insights Messages
        "insight_wait": "ℹ️ AI નિર્ણયો જોવા માટે ઉપર ડેટા અપલોડ કરો.",
        "insight_maint_risk": "🔴 **તાત્કાલિક:** **{count} મશીનો** રિપેરિંગ માંગે છે. અંદાજિત જોખમ: {cost}",
        "insight_maint_ok": "🟢 **મેન્ટેનન્સ:** બધા મશીન એકદમ બરાબર છે.",
        "insight_prod": "📦 **ઉત્પાદન:** **'{prod}'** બેચને પ્રાથમિકતા આપો.",
        "insight_energy_waste": "⚡ **નફાની તક:** {hours} કલાકનો બગાડ અટકાવો. કાર્બન ક્રેડિટ્સમાં {rev} કમાઓ.",
        "insight_energy_ok": "✅ **એનર્જી:** વીજળીનો વપરાશ યોગ્ય છે.",

        # Chatbot Messages
        "bot_nodata": "⚠️ કૃપા કરીને પહેલા ડેટા અપલોડ કરો.",
        "bot_risk_high": "⚠️ ચેતવણી: {count} મશીન ક્રિટિકલ કન્ડિશનમાં છે! તાત્કાલિક તપાસો.",
        "bot_risk_ok": "✅ બધા મશીન એકદમ બરાબર છે. કોઈ ચિંતા નથી.",
        "bot_prod": "📦 અનુમાન: {total} યુનિટ્સ. મુખ્ય પ્રોડક્ટ: {top}.",
        "bot_energy_waste": "⚡ ચેતવણી: {count} કલાક પાવર વેસ્ટ (બગાડ) પકડાયો છે.",
        "bot_energy_ok": "🌱 વીજળીનો વપરાશ એકદમ કાર્યક્ષમ છે.",
        "bot_confused": "માફ કરજો, હું સમજ્યો નહીં. 'જોખમ', 'ઉત્પાદન' કે 'નફો' વિશે પૂછો."
    },
    "Hindi": {
        "nav_overview": "📊 मुख्य डैशबोर्ड",
        "nav_maint": "🛠 प्रिडिक्टिव मेंटेनेंस",
        "nav_inv": "📦 स्मार्ट इन्वेंट्री",
        "nav_energy": "⚡ ऊर्जा अनुकूलक",
        "nav_quality": "🔍 गुणवत्ता नियंत्रण",
        "title": "🏭 फैक्ट्री कमांड सेंटर",
        "subtitle": "रियल-टाइम ऑपरेशनल इंटेलिजेंस और जोखिम विश्लेषण",
        "upload_header": "📂 डेटा अपलोड करें (रखरखाव, इन्वेंट्री, ऊर्जा)",
        "hero_eff": "🏭 कुल दक्षता",
        "hero_risk": "💰 अनुमानित जोखिम लागत",
        "hero_alerts": "🚨 सक्रिय अलर्ट",
        "hero_production": "📦 उत्पादन लक्ष्य",
        "chat_placeholder": "फैक्ट्री के बारे में पूछें...",
        "btn_download": "📥 रिपोर्ट डाउनलोड करें",
        "btn_refresh": "🔄 रिफ्रेश",
        "stat_vib": "⚙️ औसत कंपन",
        "stat_top_prod": "🔥 शीर्ष उत्पाद",
        "stat_peak": "⚡ पीक लोड",
        "stat_roi": "🌱 कार्बन क्रेडिट आय",
        "ai_center": "🤖 AI निर्णय केंद्र (प्राथमिकता)",
        "chat_title": "💬 एआई सहायक",

        # Insights Messages
        "insight_wait": "ℹ️ AI निर्णय देखने के लिए डेटा अपलोड करें.",
        "insight_maint_risk": "🔴 **तत्काल:** **{count} मशीनों** को मरम्मत की आवश्यकता है. जोखिम: {cost}",
        "insight_maint_ok": "🟢 **रखरखाव:** सभी मशीनें ठीक हैं.",
        "insight_prod": "📦 **उत्पादन:** **'{prod}'** बैच को प्राथमिकता दें.",
        "insight_energy_waste": "⚡ **लाभ का अवसर:** {hours} घंटे की बर्बादी रोकें. कार्बन क्रेडिट में {rev} कमाएं.",
        "insight_energy_ok": "✅ **ऊर्जा:** खपत अनुकूलित है.",

        # Chatbot Messages
        "bot_nodata": "⚠️ कृपया पहले डेटा अपलोड करें.",
        "bot_risk_high": "⚠️ चेतावनी: {count} मशीनें खराब स्थिति में हैं! तुरंत जांचें.",
        "bot_risk_ok": "✅ सभी मशीनें ठीक काम कर रही हैं.",
        "bot_prod": "📦 अनुमान: {total} यूनिट्स. मुख्य उत्पाद: {top}.",
        "bot_energy_waste": "⚡ चेतावनी: {count} घंटे बिजली की बर्बादी पाई गई है.",
        "bot_energy_ok": "🌱 ऊर्जा की खपत सही है.",
        "bot_confused": "क्षमा करें, मैं समझा नहीं. 'जोखिम', 'उत्पादन' या 'लाभ' के बारे में पूछें."
    }
}

# 🎨 CUSTOM CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div.stButton > button {
        background-color: #2e86de; color: white; border-radius: 8px; font-weight: bold;
    }
    .upload-box {
        border: 2px dashed #2e86de; padding: 10px; border-radius: 10px; background-color: #ffffff; text-align: center;
    }
    .risk-high { background-color: #ffe6e6; color: #cc0000; padding: 10px; border-radius: 5px; border-left: 5px solid #cc0000; }
    .risk-ok { background-color: #e6fffa; color: #006644; padding: 10px; border-radius: 5px; border-left: 5px solid #006644; }
    </style>
    """, unsafe_allow_html=True)

# ---------------- SESSION STATE INIT ----------------
if 'maint_data' not in st.session_state: st.session_state['maint_data'] = None
if 'inv_data' not in st.session_state: st.session_state['inv_data'] = None
if 'energy_data' not in st.session_state: st.session_state['energy_data'] = None

# Chat History Init
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your Factory AI. Example: Risk , Production , Energy..."}]

# ---------------- HELPER: PDF GENERATOR ----------------
def create_pdf_report(efficiency, risk_cost, alerts, production_target, maint_status, top_prod, peak_load, carbon_roi):
    risk_cost = str(risk_cost).replace("₹", "Rs. ")
    carbon_roi = str(carbon_roi).replace("₹", "Rs. ")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Factory AI Daily Report", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="1. Executive Summary", ln=True, align='L')
    pdf.set_font("Arial", size=11)
    pdf.cell(100, 10, txt=f"Efficiency: {efficiency}", ln=False)
    pdf.cell(100, 10, txt=f"Risk Cost: {risk_cost}", ln=True)
    pdf.cell(100, 10, txt=f"Alerts: {alerts}", ln=False)
    pdf.cell(100, 10, txt=f"Target: {production_target}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="2. Details", ln=True, align='L')
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt=f"- Maintenance: {maint_status}", ln=True)
    pdf.cell(200, 10, txt=f"- Top Product: {top_prod}", ln=True)
    pdf.cell(200, 10, txt=f"- Peak Load: {peak_load} kW", ln=True)
    pdf.cell(200, 10, txt=f"- Carbon ROI: {carbon_roi}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="3. AI Action Plan", ln=True, align='L')
    pdf.set_font("Arial", size=11)
    if alerts > 0:
        pdf.set_text_color(194, 24, 7)
        pdf.multi_cell(0, 10, txt="URGENT: Critical risks detected in Machinery/Energy. Immediate inspection required.")
    else:
        pdf.set_text_color(0, 100, 0)
        pdf.multi_cell(0, 10, txt="Operations are running smoothly. Focus on optimizing inventory for the top product.")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, txt="Generated by MSME Squad", align='C')
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# ---------------- HELPER: SMART CHATBOT LOGIC ----------------
def get_bot_response(user_query, current_lang_dict):
    query = user_query.lower()
    t = current_lang_dict
    
    keywords_risk = ["risk", "machine", "maintenance", "health", "status", "જોખમ", "મશીન", "ખરાબ", "खराब", "जोखिम"]
    keywords_prod = ["production", "inventory", "stock", "demand", "forecast", "ઉત્પાદન", "સ્ટોક", "उत्पादन"]
    keywords_energy = ["energy", "waste", "carbon", "cost", "bill", "પાવર", "વીજળી", "બિલ", "બગાડ", "बिजली"]
    keywords_hello = ["hi", "hello", "help", "kem cho", "namaste", "કેમ છો", "नमस्ते"]

    if any(x in query for x in keywords_risk):
        if st.session_state['maint_data'] is None: return t["bot_nodata"]
        df = st.session_state['maint_data']
        risk_count = df[df['AI_Diagnosis'] == "🔴 CRITICAL"].shape[0]
        return t["bot_risk_high"].format(count=risk_count) if risk_count > 0 else t["bot_risk_ok"]

    elif any(x in query for x in keywords_prod):
        if st.session_state['inv_data'] is None: return t["bot_nodata"]
        total = st.session_state['inv_data']['AI_Predicted_Demand'].sum()
        top_prod = "N/A"
        if not st.session_state['inv_data'].empty:
            top_prod = st.session_state['inv_data'].groupby('Product_ID')['AI_Predicted_Demand'].sum().idxmax()
        return t["bot_prod"].format(total=total, top=top_prod)

    elif any(x in query for x in keywords_energy):
        if st.session_state['energy_data'] is None: return t["bot_nodata"]
        df = st.session_state['energy_data']
        waste_count = df[df['AI_Status'] == "⚠️ HIGH"].shape[0]
        return t["bot_energy_waste"].format(count=waste_count) if waste_count > 0 else t["bot_energy_ok"]

    elif any(x in query for x in keywords_hello):
        return t["bot_intro"]

    else:
        return t["bot_confused"]

# ---------------- SIDEBAR (CHATBOT IS BACK HERE) ----------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3061/3061341.png", width=150)
st.sidebar.title("🏭 MSME Squad")

st.sidebar.markdown("---")

selected_lang = st.sidebar.selectbox("Languages", ["English", "Gujarati", "Hindi"])
t = translations[selected_lang]

st.sidebar.markdown("---")

menu = st.sidebar.radio("Modules:", [t["nav_overview"], t["nav_maint"], t["nav_inv"], t["nav_energy"], t["nav_quality"]])

st.sidebar.markdown("---")

# --- CHATBOT RESTORED IN SIDEBAR ---
with st.sidebar.expander("💬 MSME AI Assistant", expanded=True):
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt := st.chat_input(t["chat_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = get_bot_response(prompt, t)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)


# ---------------- 1. EXECUTIVE OVERVIEW (MAIN PAGE) ----------------
# Use t[] for comparison so it works in any language
if menu == t["nav_overview"]:
        
        # Header
        c_head1, c_head2 = st.columns([2, 1])
        with c_head1:
            st.title(t["title"])
            st.markdown(f"**{t['subtitle']}**")
        
        # Upload Section
        with st.expander(t["upload_header"], expanded=True):
            col_u1, col_u2, col_u3 = st.columns(3)
            
            # Maintenance
            with col_u1:
                st.markdown("### 🛠 Maintenance")
                file_m = st.file_uploader("Upload `test_maintenance.csv`", type=['csv'], key="u1")
                if file_m:
                    df = pd.read_csv(file_m)
                    results = []
                    critical_count = 0
                    for index, row in df.iterrows():
                        status = ai_engine.analyze_machine_health(row['Vibration'], row['Temperature'])
                        if "RISK" in status:
                            results.append("🔴 CRITICAL")
                            critical_count += 1
                        else:
                            results.append("🟢 OK")
                    df['AI_Diagnosis'] = results
                    st.session_state['maint_data'] = df
                    if critical_count > 0: st.toast(f"🚨 ALERT: {critical_count} Machines Critical!", icon="🔥")
                    else: st.toast("✅ Maintenance Normal.", icon="🛠")
                    st.success(f"✅ Loaded {len(df)} Machines")

            # Inventory
            with col_u2:
                st.markdown("### 📦 Inventory")
                file_i = st.file_uploader("Upload `test_inventory_plan.csv`", type=['csv'], key="u2")
                if file_i:
                    df = pd.read_csv(file_i)
                    df['Date'] = pd.to_datetime(df['Date'])
                    predictions = []
                    for index, row in df.iterrows():
                        d = row['Date']
                        pid = row['Product_ID']
                        pred = ai_engine.forecast_demand(d.dayofyear, d.month, (d.weekday() >= 5), pid)
                        predictions.append(pred)
                    df['AI_Predicted_Demand'] = predictions
                    st.session_state['inv_data'] = df
                    st.success(f"✅ Generated Forecast")

            # Energy
            with col_u3:
                st.markdown("### ⚡ Energy")
                file_e = st.file_uploader("Upload `test_energy.csv`", type=['csv'], key="u3")
                if file_e:
                    df = pd.read_csv(file_e)
                    e_status = []
                    waste_count = 0
                    for index, row in df.iterrows():
                        status = ai_engine.detect_energy_waste(row['kWh_Usage'])
                        if "High" in status:
                            e_status.append("⚠️ HIGH")
                            waste_count += 1
                        else:
                            e_status.append("✅ NORMAL")
                    df['AI_Status'] = e_status
                    st.session_state['energy_data'] = df
                    if waste_count > 0: st.toast(f"⚡ WARNING: {waste_count} Hours Waste!", icon="⚡")
                    st.success(f"✅ Analyzed Usage")

        st.markdown("---")

        # Metrics Calculation
        risk_count = 0
        energy_waste_count = 0
        eff_maint = 100
        eff_energy = 100
        estimated_loss = 0
        carbon_revenue = 0 
        avg_vib = 0
        top_prod_name = "-"
        peak_load = 0
        carbon_footprint = 0
        
        COST_PER_BREAKDOWN = 25000
        COST_PER_ENERGY_WASTE = 1000
        CREDIT_PRICE_PER_TON = 2000
        
        if st.session_state['maint_data'] is not None:
            df_m = st.session_state['maint_data']
            total_m = len(df_m)
            risk_count = df_m[df_m['AI_Diagnosis'] == "🔴 CRITICAL"].shape[0]
            if total_m > 0:
                eff_maint = round(((total_m - risk_count) / total_m) * 100)
                avg_vib = round(df_m['Vibration'].mean(), 2)
            estimated_loss += (risk_count * COST_PER_BREAKDOWN)

        if st.session_state['energy_data'] is not None:
            df_e = st.session_state['energy_data']
            total_e = len(df_e)
            energy_waste_count = df_e[df_e['AI_Status'] == "⚠️ HIGH"].shape[0]
            if total_e > 0:
                eff_energy = round(((total_e - energy_waste_count) / total_e) * 100)
                peak_load = df_e['kWh_Usage'].max()
                total_kwh = df_e['kWh_Usage'].sum()
                carbon_footprint = round(total_kwh * 0.85, 1)
                saved_kwh_potential = energy_waste_count * 50
                saved_co2_tons = (saved_kwh_potential * 0.85) / 1000
                carbon_revenue = round(saved_co2_tons * CREDIT_PRICE_PER_TON)
            estimated_loss += (energy_waste_count * COST_PER_ENERGY_WASTE)
            
        if st.session_state['inv_data'] is not None:
            df_i = st.session_state['inv_data']
            top_prod_name = df_i.groupby('Product_ID')['AI_Predicted_Demand'].sum().idxmax()
        
        final_efficiency_val = round((eff_maint + eff_energy) / 2) if (st.session_state['maint_data'] is not None or st.session_state['energy_data'] is not None) else 0
        final_efficiency = f"{final_efficiency_val}%" if final_efficiency_val > 0 else "Waiting..."
        eff_delta = "normal" if final_efficiency_val >= 90 else ("off" if final_efficiency_val >= 75 else "inverse")
        loss_display = f"Rs. {estimated_loss:,}"
        total_alerts = risk_count + energy_waste_count
        prod_target = f"{st.session_state['inv_data']['AI_Predicted_Demand'].sum()} Units" if st.session_state['inv_data'] is not None else "-"
        
        # Download Button Logic
        with c_head2:
            st.write("") 
            if st.button(t["btn_refresh"]): st.rerun()
            if final_efficiency_val > 0:
                pdf_bytes = create_pdf_report(
                    final_efficiency, loss_display, total_alerts, prod_target, 
                    f"{risk_count} Risks", top_prod_name, peak_load, f"Rs. {carbon_revenue}"
                )
                st.download_button(
                    label=t["btn_download"],
                    data=pdf_bytes,
                    file_name=f"Factory_Report_{datetime.now().strftime('%Y-%m-%d')}.pdf",
                    mime="application/pdf"
                )

        # Display Metrics (With Translations)
        st.subheader("🚀 Operational Health & Risk Monitor")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric(t["hero_eff"], final_efficiency, "Plant Score", delta_color=eff_delta)
        with col2: st.metric(t["hero_risk"], loss_display.replace("Rs.", "₹"), "Potential Loss", delta_color="inverse")
        with col3: st.metric(t["hero_alerts"], total_alerts, "Requires Action", delta_color="inverse")
        with col4: st.metric(t["hero_production"], prod_target, "AI Forecast")

        st.write("") 

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric(t["stat_vib"], f"{avg_vib} mm/s" if avg_vib > 0 else "-", "Health")
        with c2: st.metric(t["stat_top_prod"], top_prod_name, "Demand")
        with c3: st.metric(t["stat_peak"], f"{peak_load} kW" if peak_load > 0 else "-", "Stress", delta_color="inverse")
        with c4: st.metric(t["stat_roi"], f"₹{carbon_revenue}" if carbon_revenue > 0 else "-", "Earnings", delta_color="normal")

        st.markdown("---")
        

        # --- 🤖 AI DECISION CENTER (Replace this specific block only) ---
        st.markdown("---")
        st.subheader(t["ai_center"]) # <-- Header ગુજરાતીમાં આવશે
        insight_found = False
        
        # 1. Maintenance Logic (Fixed)
        if st.session_state['maint_data'] is not None:
            insight_found = True
            if risk_count > 0:
                # English text hatavi ne t["..."] mukyu
                cost_str = f"₹{risk_count*COST_PER_BREAKDOWN:,}"
                st.error(t["insight_maint_risk"].format(count=risk_count, cost=cost_str))
            else:
                st.success(t["insight_maint_ok"]) # <-- AA CHANGE KARYU

        # 2. Inventory Logic (Fixed)
        if st.session_state['inv_data'] is not None:
            insight_found = True
            st.info(t["insight_prod"].format(prod=top_prod_name)) # <-- AA CHANGE KARYU

        # 3. Energy Logic (Fixed)
        if st.session_state['energy_data'] is not None:
            insight_found = True
            if energy_waste_count > 0:
                rev_str = f"₹{carbon_revenue}"
                st.warning(t["insight_energy_waste"].format(hours=energy_waste_count, rev=rev_str)) # <-- AA CHANGE KARYU
            else:
                st.success(t["insight_energy_ok"]) # <-- AA CHANGE KARYU

        if not insight_found: 
            st.info(t["insight_wait"])

    # ---------------- 2. PREDICTIVE MAINTENANCE ----------------
elif menu == t["nav_maint"]:
        st.title(t["nav_maint"])
        
        if st.session_state['maint_data'] is None:
            st.warning("⚠️ No Data Found. Please go to **Executive Overview** and upload 'test_maintenance.csv'.")
        else:
            df = st.session_state['maint_data']
            risky_df = df[df['AI_Diagnosis'] == "🔴 CRITICAL"]
            if not risky_df.empty:
                st.markdown(f'<div class="risk-high">🚨 <b>CRITICAL ALERT:</b> Found {len(risky_df)} machines at high risk.</div>', unsafe_allow_html=True)
                st.dataframe(risky_df)
            else:
                st.markdown('<div class="risk-ok">✅ All machines are operating within safe parameters.</div>', unsafe_allow_html=True)
            st.markdown("---")
            st.subheader("📋 Full Sensor Log Analysis")
            st.dataframe(df.style.applymap(lambda v: 'color: red; font-weight: bold;' if v == '🔴 CRITICAL' else 'color: green;', subset=['AI_Diagnosis']))


    # ---------------- 3. SMART INVENTORY ----------------
elif menu == t["nav_inv"]:
        st.title(t["nav_inv"])
        
        if st.session_state['inv_data'] is None:
            st.warning("⚠️ No Data Found. Please go to **Executive Overview** and upload 'test_inventory_plan.csv'.")
        else:
            df = st.session_state['inv_data']
            total = df['AI_Predicted_Demand'].sum()
            st.success(f"📈 Total Production Requirement: **{total} Units**")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📊 Product-wise Breakdown")
                st.bar_chart(df.groupby('Product_ID')['AI_Predicted_Demand'].sum())
            with col2:
                st.subheader("📅 Daily Trend")
                st.line_chart(df.groupby('Date')['AI_Predicted_Demand'].sum())
            st.dataframe(df)


    # ---------------- 4. ENERGY OPTIMIZER ----------------
elif menu == t["nav_energy"]:
        st.title(t["nav_energy"])
        
        if st.session_state['energy_data'] is None:
            st.warning("⚠️ No Data Found. Please go to **Executive Overview** and upload 'test_energy.csv'.")
        else:
            df = st.session_state['energy_data']
            waste_df = df[df['AI_Status'] == "⚠️ HIGH"]
            c1, c2 = st.columns(2)
            c1.metric("Total Consumption", f"{df['kWh_Usage'].sum()} kWh")
            c2.metric("Inefficient Hours", len(waste_df), delta_color="inverse")
            st.markdown("---")
            if not waste_df.empty:
                st.error("🔥 **High Consumption Alert:**")
                st.table(waste_df)
            st.subheader("📈 Hourly Load Profile")
            st.area_chart(df.set_index('Hour')['kWh_Usage'])


    # ---------------- 5. QUALITY CONTROL ----------------
elif menu == t["nav_quality"]:
        st.header(t["nav_quality"])
        st.info("Note: Image Analysis is done one-by-one (Visual Inspection).")
        
        file = st.file_uploader("Upload Image", type=['jpg','png'])
        if file:
            col1, col2 = st.columns(2)
            with col1:
                st.image(file, caption="Uploaded Photo", width=300)
            with col2:
                st.write("Analyzing...")
                result = ai_engine.check_product_quality(file)
                if "Defect" in result:
                    st.error(f"🚨 {result}")
                else:
                    st.success(f"✅ {result}")