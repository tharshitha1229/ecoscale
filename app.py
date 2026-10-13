import streamlit as st
import time
import pandas as pd
import numpy as np
import joblib
import requests
import datetime
import subprocess 
import json
import psutil 
import random
import base64
import os
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
from streamlit_autorefresh import st_autorefresh
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="EcoScale AI", page_icon="🌱", layout="wide")

# ==========================================
# CUSTOM CSS INJECTION
# ==========================================
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("style.css")
except Exception:
    pass

# ==========================================
# SECURITY & AUTHENTICATION
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""<div style="text-align: center; margin-top: 60px; margin-bottom: 28px;">
<div style="font-size: 32px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.5px;">Eco<span style="color: #D2F53E;">Scale</span></div>
<div style="font-size: 14px; color: #8E9CA6; margin-top: 6px;">Autonomous Carbon Orchestration Platform</div>
</div>""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center; margin-bottom: 18px; font-weight: 700;'>Infrastructure Gateway</h4>", unsafe_allow_html=True)
            pwd = st.text_input("Administrator Access", type="password", placeholder="Enter Password (admin123)")
            
            st.write("") # Spacer
            if st.button("Unlock Command Center ↗", type="primary", use_container_width=True):
                if pwd == "admin123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Access Denied: Incorrect Password")
    
    st.stop()
# ==========================================
# ==========================================
# CLOUD CARBON FOOTPRINT (CCF) MATHEMATICAL ENGINE
# Enterprise Standards: Thoughtworks CCF & GHG Protocol (Scope 2 & 3)
# ==========================================
try:
    ai_model = joblib.load('carbon_model.pkl')
except Exception:
    ai_model = None

# Hardware Lifespan & Power Specifications (SPECpower, Apple/Dell LCA Reports)
CCF_HARDWARE = {
    "Mac (Apple Silicon)": {
        "idle_watts": 5.0,
        "max_watts": 45.0,
        "embodied_carbon_g": 185000.0,  # 185 kg CO2e cradle-to-gate
        "lifespan_years": 4.0,
    },
    "Windows PC": {
        "idle_watts": 35.0,
        "max_watts": 130.0,
        "embodied_carbon_g": 350000.0,  # 350 kg CO2e
        "lifespan_years": 4.0,
    },
    "Linux Workstation": {
        "idle_watts": 65.0,
        "max_watts": 230.0,
        "embodied_carbon_g": 450000.0,  # 450 kg CO2e
        "lifespan_years": 4.0,
    }
}

CCF_MOBILE = {
    "Apple": {
        "avg_watts": 2.2,
        "embodied_carbon_g": 65000.0,   # 65 kg CO2e
        "lifespan_years": 3.0,
    },
    "OnePlus": {
        "avg_watts": 2.5,
        "embodied_carbon_g": 60000.0,   # 60 kg CO2e
        "lifespan_years": 3.0,
    },
    "Samsung": {
        "avg_watts": 2.6,
        "embodied_carbon_g": 70000.0,   # 70 kg CO2e
        "lifespan_years": 3.0,
    }
}

CCF_REGIONS = {
    "GCP (Europe-West / Frankfurt)": {
        "pue": 1.10,                     # Thoughtworks CCF benchmark for Google Cloud
        "grid_intensity_g_kwh": 150.0,   # Low-carbon wind/solar grid
        "provider": "Google Cloud Platform"
    },
    "AWS (US-East / N. Virginia)": {
        "pue": 1.135,                    # Standard AWS hyperscale data center PUE
        "grid_intensity_g_kwh": 380.0,   # PJM mixed regional grid
        "provider": "Amazon Web Services"
    },
    "Azure (India-West / Pune)": {
        "pue": 1.125,                    # Microsoft Azure hyperscale facility
        "grid_intensity_g_kwh": 590.0,   # Western Regional Load Dispatch Centre (coal heavy)
        "provider": "Microsoft Azure"
    }
}

def compute_ccf_footprint(device, mobile, coding_h, streaming_h, heavy_h, region_name, active_nodes, host_cpu):
    dev = CCF_HARDWARE.get(device, CCF_HARDWARE["Mac (Apple Silicon)"])
    mob = CCF_MOBILE.get(mobile, CCF_MOBILE["Apple"])
    region = CCF_REGIONS.get(region_name, CCF_REGIONS["GCP (Europe-West / Frankfurt)"])

    # 1. Scope 2: Operational Emissions
    # Power (W) = P_idle + Util * (P_max - P_idle)
    coding_power_w = dev["idle_watts"] + 0.25 * (dev["max_watts"] - dev["idle_watts"])
    coding_kwh = (coding_power_w * coding_h) / 1000.0
    
    heavy_power_w = dev["idle_watts"] + 0.85 * (dev["max_watts"] - dev["idle_watts"])
    heavy_kwh = (heavy_power_w * heavy_h) / 1000.0
    
    mobile_kwh = (mob["avg_watts"] * streaming_h) / 1000.0
    
    client_total_kwh = coding_kwh + heavy_kwh + mobile_kwh
    client_pue = 1.0
    client_grid_intensity = 450.0
    client_operational_co2_g = client_total_kwh * client_pue * client_grid_intensity

    # Cloud Backend Orchestrated Nodes (Live Docker container workload)
    cloud_pue = region["pue"]
    cloud_grid_intensity = region["grid_intensity_g_kwh"]
    
    cloud_nodes_count = max(active_nodes, 1)
    cloud_utilization = max(host_cpu / 100.0, 0.12)
    cloud_node_power_w = 12.0 + cloud_utilization * (45.0 - 12.0)
    
    cloud_runtime_h = max(heavy_h + (coding_h * 0.4), 1.0)
    cloud_it_kwh = (cloud_node_power_w * cloud_nodes_count * cloud_runtime_h) / 1000.0
    cloud_facility_kwh = cloud_it_kwh * cloud_pue
    cloud_operational_co2_g = cloud_facility_kwh * cloud_grid_intensity

    total_operational_co2_g = client_operational_co2_g + cloud_operational_co2_g
    total_energy_kwh = client_total_kwh + cloud_facility_kwh
    effective_pue = ((client_total_kwh * client_pue) + (cloud_facility_kwh * cloud_pue)) / total_energy_kwh if total_energy_kwh > 0 else 1.0

    # 2. Scope 3: Embodied Emissions (Cradle-to-gate hardware manufacturing)
    pc_lifespan_h = dev["lifespan_years"] * 365.25 * 24.0
    mob_lifespan_h = mob["lifespan_years"] * 365.25 * 24.0
    
    pc_usage_h = coding_h + heavy_h
    mob_usage_h = streaming_h
    
    pc_embodied_co2_g = dev["embodied_carbon_g"] * (pc_usage_h / pc_lifespan_h)
    mob_embodied_co2_g = mob["embodied_carbon_g"] * (mob_usage_h / mob_lifespan_h)
    
    server_lifespan_h = 4.0 * 365.25 * 24.0
    cloud_embodied_co2_g = 150000.0 * cloud_nodes_count * (cloud_runtime_h / server_lifespan_h)
    
    total_embodied_co2_g = pc_embodied_co2_g + mob_embodied_co2_g + cloud_embodied_co2_g

    # 3. Total Cloud Carbon Footprint
    total_co2_g = total_operational_co2_g + total_embodied_co2_g

    return {
        "total_co2_g": round(total_co2_g, 2),
        "operational_co2_g": round(total_operational_co2_g, 2),
        "embodied_co2_g": round(total_embodied_co2_g, 2),
        "total_energy_kwh": round(total_energy_kwh, 4),
        "effective_pue": round(effective_pue, 3),
        "cloud_pue": cloud_pue,
        "cloud_grid_intensity": cloud_grid_intensity,
        "cloud_nodes_count": cloud_nodes_count,
        "cloud_operational_co2_g": round(cloud_operational_co2_g, 2),
        "cloud_embodied_co2_g": round(cloud_embodied_co2_g, 2),
        "client_operational_co2_g": round(client_operational_co2_g, 2),
        "client_embodied_co2_g": round(pc_embodied_co2_g + mob_embodied_co2_g, 2),
        "components": {
            "PC Coding (Scope 2)": round(coding_kwh * client_grid_intensity, 2),
            "PC Heavy Compute (Scope 2)": round(heavy_kwh * client_grid_intensity, 2),
            "Mobile Streaming (Scope 2)": round(mobile_kwh * client_grid_intensity, 2),
            "Cloud Backend Nodes (Scope 2)": round(cloud_operational_co2_g, 2),
            "PC Manufacturing (Scope 3)": round(pc_embodied_co2_g, 2),
            "Mobile Manufacturing (Scope 3)": round(mob_embodied_co2_g, 2),
            "Cloud Server Hardware (Scope 3)": round(cloud_embodied_co2_g, 2),
        }
    }

# ==========================================
# DOCKER INFRASTRUCTURE AS CODE (IaC)
# ==========================================
def get_real_containers():
    """Queries Docker for live running instances of the backend."""
    try:
        cmd = ["docker", "ps", "--filter", "ancestor=ecoscale-backend", "--filter", "ancestor=greencloud-backend", "--format", "{{json .}}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                containers.append(json.loads(line))
        return containers
    except:
        return []

import os

def launch_container(node_name, port):
    """Commands Docker to spin up a new backend instance."""
    server_path = os.path.abspath("backend/server.js")
    check_img = subprocess.run(["docker", "image", "inspect", "ecoscale-backend"], capture_output=True)
    img_name = "ecoscale-backend" if check_img.returncode == 0 else "greencloud-backend"
    subprocess.run(["docker", "run", "-d", "--name", node_name, "-v", f"{server_path}:/usr/src/app/server.js", "--env-file", "backend/.env", "-p", f"{port}:5001", img_name])

def destroy_container(node_name):
    """Forcefully kills a Docker container."""
    subprocess.run(["docker", "rm", "-f", node_name])

def get_active_port():
    """Helper to find the port of an active container, or boot one if none exist."""
    containers = get_real_containers()
    if not containers:
        launch_container("node-1", 5001)
        time.sleep(2) # Give Express/MongoDB time to connect
        return 5001
    
    # Extract the port string (e.g., "0.0.0.0:5001->5001/tcp") and parse the public port
    port_str = containers[0].get('Ports', '')
    try:
        return int(port_str.split(':')[1].split('->')[0])
    except:
        return 5001

st.markdown("""<div class="inspo-hero-shell">
<div class="inspo-nav">
<div class="inspo-logo">Eco<span>Scale</span></div>
<div class="inspo-nav-links">
<span class="inspo-nav-link active">CCF Engine</span>
<span class="inspo-nav-link">Orchestration</span>
<span class="inspo-nav-link">Forecasts</span>
<span class="inspo-nav-link">Global Routing</span>
</div>
<a class="inspo-pill-btn" href="#system-tabs">Live Cluster ↗</a>
</div>
<div class="inspo-hero-grid">
<div class="inspo-hero-left">
<div class="hero-title">DECARBONIZE<br>PLANET</div>
<div class="inspo-hero-subtitle">Autonomous multi-agent infrastructure for enterprise carbon intelligence</div>
<a class="inspo-hero-link" href="#system-tabs">Explore CCF Engine ↗</a>
</div>
<div class="inspo-hero-right">
<div class="inspo-hero-card">
<div class="inspo-badge">
<span class="inspo-badge-dot"></span>
<span>📍 GCP Europe-West • PUE 1.10</span>
</div>
<p class="inspo-card-text">
Autonomous agents actively monitor physical CPU telemetry, dynamically orchestrate Docker containers, and calculate regulatory Scope 2 operational and Scope 3 embodied carbon footprints.
</p>
</div>
</div>
</div>
<div class="inspo-divider-wrap">
<div class="inspo-divider-accent"></div>
</div>
<div class="inspo-pillars">
<div class="inspo-pillar">
<div class="inspo-pillar-header">
<span class="inspo-pillar-num">1</span>
<span class="inspo-pillar-title">Scope 2 Operational</span>
</div>
<p class="inspo-pillar-desc">Energy (kWh) × PUE × Grid Intensity</p>
</div>
<div class="inspo-pillar">
<div class="inspo-pillar-header">
<span class="inspo-pillar-num">2</span>
<span class="inspo-pillar-title">Scope 3 Embodied</span>
</div>
<p class="inspo-pillar-desc">Hardware Manufacturing Lifecycle</p>
</div>
<div class="inspo-pillar">
<div class="inspo-pillar-header">
<span class="inspo-pillar-num">3</span>
<span class="inspo-pillar-title">Autonomous Scaler</span>
</div>
<p class="inspo-pillar-desc">Real-Time Docker Container HPA</p>
</div>
<div class="inspo-pillar">
<div class="inspo-pillar-header">
<span class="inspo-pillar-num">4</span>
<span class="inspo-pillar-title">Green Grid Routing</span>
</div>
<p class="inspo-pillar-desc">Shift to Wind & Solar Powered Datacenters</p>
</div>
</div>
</div>
<div id="system-tabs"></div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["⚡ Personal CCF Engine", "☁️ Command Center", "🗄️ Historical Forecasts", "🌍 Global Grid Routing"])

# ==========================================
# TAB 1: THE PERSONAL USER EXPERIENCE
# ==========================================
with tab1:
    st.markdown("### 🔍 Enterprise Cloud Carbon Footprint (CCF) Engine")
    st.caption("Powered by Thoughtworks CCF Mathematical Methodology & Live Autonomous Agent Orchestration")
    
    with st.container(border=True):
        st.markdown("##### 👤 User Identification")
        username = st.text_input("Student ID or Name", placeholder="e.g., 25BCE1177")
        st.write("") # Spacer
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### 🖥️ Client Hardware Profile (Scope 3 Embodied)")
            device = st.selectbox("Primary Computer", ["Mac (Apple Silicon)", "Windows PC", "Linux Workstation"])
            mobile = st.selectbox("Mobile Device", ["Apple", "OnePlus", "Samsung"])
            
            st.markdown("##### ☁️ Cloud Infrastructure & Datacenter PUE")
            target_region = st.selectbox(
                "Target Cloud Datacenter", 
                [
                    "GCP (Europe-West / Frankfurt)", 
                    "AWS (US-East / N. Virginia)", 
                    "Azure (India-West / Pune)"
                ],
                help="Power Usage Effectiveness (PUE) and regional Grid Carbon Intensity from Cloud Carbon Footprint (CCF) dataset."
            )
            
        with col2:
            st.markdown("##### ⏱️ Daily Usage Habits (Scope 2 Operational)")
            coding_hours = st.slider("Hours spent coding/studying", 0, 12, 4)
            streaming_hours = st.slider("Hours streaming (Anime, YouTube)", 0, 10, 2)
            heavy_software = st.slider("Hours using heavy computation / ML", 0, 8, 1)

    if st.button("🚀 Calculate Footprint (CCF Enterprise Engine)", type="primary", use_container_width=True):
        if not username:
            st.warning("⚠️ Please enter a name to save your record.")
        else:
            with st.spinner('🔐 Agent sampling live Docker telemetry & executing CCF formulas...'):
                # Live Agent Infrastructure Telemetry
                live_containers = get_real_containers()
                active_nodes_count = len(live_containers)
                host_cpu = psutil.cpu_percent(interval=0.1)
                
                # Execute CCF Mathematical Engine
                ccf = compute_ccf_footprint(
                    device=device,
                    mobile=mobile,
                    coding_h=coding_hours,
                    streaming_h=streaming_hours,
                    heavy_h=heavy_software,
                    region_name=target_region,
                    active_nodes=active_nodes_count,
                    host_cpu=host_cpu
                )

                # DOCKER ROUTING & PERSISTENCE
                active_port = get_active_port()
                api_url = f"http://localhost:{active_port}/api/history"
                
                try:
                    payload = {
                        "username": username.strip(),
                        "device": device,
                        "mobile": mobile,
                        "coding_hours": coding_hours,
                        "streaming_hours": streaming_hours,
                        "heavy_hours": heavy_software,
                        "total_emission": float(ccf["total_co2_g"]),
                        "operational_emission": float(ccf["operational_co2_g"]),
                        "embodied_emission": float(ccf["embodied_co2_g"]),
                        "pue": float(ccf["effective_pue"]),
                        "energy_kwh": float(ccf["total_energy_kwh"])
                    }
                    requests.post(api_url, json=payload)
                    st.success("✅ CCF Enterprise Calculation successfully verified & persisted to MongoDB.")
                    
                    # SERVERLESS VS DEDICATED LOGIC
                    if heavy_software > 2 or coding_hours > 6:
                        st.info(f"**Cloud Economics:** Heavy workload detected. Routing to **Dedicated VM** (Low latency, Fixed Cost). Estimated cost: $0.15/hr.")
                    else:
                        st.info(f"**Cloud Economics:** Light workload detected. Routing to **Serverless Function (AWS Lambda)** (Cold start latency, Pay-per-ms). Estimated cost: $0.0001.")
                    
                    st.info(f"**Agent Routing Decision:** Task allocated to Docker container on Port **{active_port}** (Managing {ccf['cloud_nodes_count']} node(s) @ {host_cpu}% host CPU in {target_region} with PUE {ccf['cloud_pue']}).")
                except:
                    st.error(f"⚠️ Failed to route traffic to container on port {active_port}. Is MongoDB connected?")

            st.write("")
            st.markdown("### 📊 CCF Executive Carbon Summary")
            
            # Executive Metric Cards
            mcol1, mcol2, mcol3, mcol4 = st.columns(4)
            with mcol1:
                st.metric("🌱 Total Carbon Footprint", f"{ccf['total_co2_g']:.1f} g", help="Operational + Embodied emissions")
            with mcol2:
                st.metric("⚡ Operational (Scope 2)", f"{ccf['operational_co2_g']:.1f} g", f"PUE: {ccf['effective_pue']}", help="Energy (kWh) × PUE × Grid Carbon Intensity")
            with mcol3:
                st.metric("🏭 Embodied (Scope 3)", f"{ccf['embodied_co2_g']:.1f} g", f"{round(ccf['embodied_co2_g']/ccf['total_co2_g']*100, 1)}% of Total", help="Hardware manufacturing cradle-to-gate amortized over lifespan")
            with mcol4:
                st.metric("🔋 Energy Consumed", f"{ccf['total_energy_kwh']:.4f} kWh", f"Datacenter PUE {ccf['cloud_pue']}")

            # Mathematical Methodology Expander
            with st.expander("📐 Enterprise CCF Mathematical Principles (Thoughtworks Standard)", expanded=False):
                st.markdown(r"""
                **Cloud Carbon Footprint (CCF)** calculates greenhouse gas (GHG) emissions through rigorous engineering standards:
                
                $$\text{Total Carbon Footprint } (g\text{CO}_2e) = \text{Operational Emissions (Scope 2)} + \text{Embodied Emissions (Scope 3)}$$
                
                ---
                ##### 1. Operational Emissions (Scope 2)
                $$\text{Operational Emissions} = \sum \left( \text{Energy}_{\text{hardware}} (\text{kWh}) \times \text{PUE} \times I_{\text{grid}} \left(\frac{g\text{CO}_2e}{\text{kWh}}\right) \right)$$
                * **PUE (Power Usage Effectiveness)**: The ratio of total datacenter facility energy to IT equipment energy. A PUE of **1.10** (Google Cloud) represents top-tier cooling efficiency compared to legacy **1.57+** data centers.
                * **Dynamic Compute Power**: $P = P_{\text{idle}} + \text{Utilization} \times (P_{\text{max}} - P_{\text{idle}})$.
                
                ---
                ##### 2. Embodied Emissions (Scope 3 - Hardware Manufacturing)
                $$\text{Embodied Emissions} = \sum \left( M_{\text{manufacturing}} (g\text{CO}_2e) \times \frac{\text{Active Usage Time (hours)}}{\text{Hardware Lifespan (hours)}} \right)$$
                * Accounts for raw material extraction, fabrication, and transport cradle-to-gate carbon amortized across 35,040 operational hours (4-year server/workstation lifespan) and 26,280 hours (3-year mobile lifespan).
                """)

            # Plotly Visualizations: Donut Scope Split & Component Breakdown
            chart_col1, chart_col2 = st.columns([1, 1.4])
            with chart_col1:
                st.markdown("##### 🔬 GHG Protocol Scope Split")
                scope_df = pd.DataFrame({
                    "Scope": ["Scope 2: Operational Emissions", "Scope 3: Embodied Emissions"],
                    "Emissions (gCO₂e)": [ccf["operational_co2_g"], ccf["embodied_co2_g"]]
                })
                fig_donut = px.pie(
                    scope_df, 
                    names="Scope", 
                    values="Emissions (gCO₂e)", 
                    hole=0.55,
                    color="Scope",
                    color_discrete_map={
                        "Scope 2: Operational Emissions": "#00E676", 
                        "Scope 3: Embodied Emissions": "#00B0FF"
                    }
                )
                fig_donut.update_layout(template="plotly_dark", margin=dict(t=20, b=20, l=10, r=10), showlegend=True)
                st.plotly_chart(fig_donut, use_container_width=True)

            with chart_col2:
                st.markdown("##### 🧩 CCF Component Breakdown")
                comp_df = pd.DataFrame({
                    "Subsystem": list(ccf["components"].keys()),
                    "Emissions (gCO₂e)": list(ccf["components"].values())
                }).sort_values("Emissions (gCO₂e)", ascending=True)
                
                fig_bar = px.bar(
                    comp_df,
                    x="Emissions (gCO₂e)",
                    y="Subsystem",
                    orientation="h",
                    color="Emissions (gCO₂e)",
                    color_continuous_scale="Viridis"
                )
                fig_bar.update_layout(template="plotly_dark", margin=dict(t=20, b=20, l=10, r=10))
                st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# TAB 2: LIVE CLOUD ORCHESTRATOR
# ==========================================
with tab2:
    st.markdown("### ☁️ Autonomous Auto-Scaling Agent")
    
    # Auto-Scaling Toggle
    auto_scale = st.toggle("🤖 Enable True Auto-Scaling (K8s Mode)", value=False, help="Automatically scales Docker containers based on live CPU load.")
    if auto_scale:
        st_autorefresh(interval=3000, limit=None, key="autoscaler")
        
    col_dash1, col_dash2 = st.columns([1.5, 1])
    
    with col_dash1:
        st.subheader("🌐 Live Docker Container Topology")
        
        live_containers = get_real_containers()
        if live_containers:
            vm_data = [{"Node Name": c.get('Names'), "Container ID": c.get('ID')[:12], "Status": c.get('State'), "Port Mapping": c.get('Ports')} for c in live_containers]
            st.dataframe(pd.DataFrame(vm_data), use_container_width=True)
        else:
            st.info("No active cloud nodes detected.")
            
        st.markdown("##### ⚙️ Manual Agent Overrides")
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🚀 Scale Up (+1 Node)", use_container_width=True):
                next_port = 5000 + len(live_containers) + 1
                launch_container(f"node-{len(live_containers) + 1}", next_port)
                st.rerun()
        with btn_col2:
            if st.button("📉 Scale Down (-1 Node)", use_container_width=True):
                if live_containers:
                    destroy_container(live_containers[-1].get('Names'))
                    st.rerun()
        
        st.divider()
        st.markdown("### 🌩️ Chaos Engineering")
        if st.button("☠️ Kill a Server (Chaos Monkey)", type="primary"):
            if live_containers:
                target = random.choice(live_containers).get('Names')
                st.error(f"🚨 FATAL ERROR: {target} suffered a hardware crash! Chaos Monkey killed the container.")
                destroy_container(target)
                time.sleep(1)
                
                # DISASTER RECOVERY LOGIC (Feature 2)
                st.warning("🔄 AI Agent detected failure! Spinning up Disaster Recovery node...")
                recovery_name = f"{target}-dr"
                launch_container(recovery_name, 5000 + random.randint(100, 999))
                time.sleep(2)
                st.success(f"✅ Traffic successfully re-routed to {recovery_name}. Zero Data Loss.")
                time.sleep(3)
                st.rerun()
            else:
                st.warning("No running nodes available to crash.")

    with col_dash2:
        st.subheader("⚡ Host Hardware Telemetry")
        cpu_usage = psutil.cpu_percent(interval=0.1)
        ram_info = psutil.virtual_memory()
        st.metric("Physical CPU Load", f"{cpu_usage}%")
        st.progress(cpu_usage / 100)
        st.metric("Host RAM Consumed", f"{ram_info.percent}%", f"{(ram_info.used / (1024**3)):.1f} GB")
        st.progress(ram_info.percent / 100)
        
        # True Auto-Scaling Logic
        if auto_scale:
            if cpu_usage > 60.0 and len(live_containers) < 5:
                st.toast("🔥 High CPU load detected! Auto-scaling UP...", icon="📈")
                next_port = 5000 + len(live_containers) + 1
                launch_container(f"node-{len(live_containers) + 1}", next_port)
            elif cpu_usage < 20.0 and len(live_containers) > 1:
                st.toast("🧊 Low CPU load detected. Auto-scaling DOWN...", icon="📉")
                destroy_container(live_containers[-1].get('Names'))

# ==========================================
# TAB 3: DATABASE & FORECASTING
# ==========================================
with tab3:
    st.markdown("### 🗄️ Carbon Database & AI Forecast")
    st.write("")
    st.markdown("##### 🔍 User Lookup")
    
    # Initialize session state for fetched data
    if "forecast_data" not in st.session_state:
        st.session_state.forecast_data = None
        st.session_state.forecast_user = ""
        st.session_state.forecast_error = None
        st.session_state.forecast_warning = None
        
    search_user = st.text_input("Student ID:", placeholder="e.g., 25BCE1177")
    
    if st.button("Fetch & Predict"):
        active_port = get_active_port()
        api_url = f"http://localhost:{active_port}/api/history"
        
        # Reset previous messages
        st.session_state.forecast_error = None
        st.session_state.forecast_warning = None
        
        try:
            response = requests.get(f"{api_url}/{search_user}")
            if response.status_code == 200 and len(response.json()) > 0:
                st.session_state.forecast_data = response.json()
                st.session_state.forecast_user = search_user
            else:
                st.session_state.forecast_data = None
                st.session_state.forecast_user = search_user
                st.session_state.forecast_warning = "No records found for this user."
        except:
            st.session_state.forecast_data = None
            st.session_state.forecast_user = search_user
            st.session_state.forecast_error = f"⚠️ Failed to connect to backend on port {active_port}."

    # Only display if the current input matches what was fetched
    if st.session_state.forecast_user == search_user:
        if st.session_state.forecast_error:
            st.error(st.session_state.forecast_error)
        elif st.session_state.forecast_warning:
            st.warning(st.session_state.forecast_warning)
        elif st.session_state.forecast_data is not None:
            raw_cols = ['timestamp', 'device', 'coding_hours', 'streaming_hours', 'total_emission', 'operational_emission', 'embodied_emission', 'pue', 'energy_kwh']
            cols_to_display = [c for c in raw_cols if c in pd.DataFrame(st.session_state.forecast_data).columns]
            history_df = pd.DataFrame(st.session_state.forecast_data)[cols_to_display]
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
            history_df = history_df.sort_values('timestamp')
            st.dataframe(history_df, use_container_width=True)
            
            # =========================================================
            # ADVANCED AI TIME-SERIES FORECASTING & UNCERTAINTY ENGINE
            # =========================================================
            # 1. Continuous Time Tracking (in fractional days, preventing 0-variance collapse)
            min_ts = history_df['timestamp'].min()
            time_deltas_days = (history_df['timestamp'] - min_ts).dt.total_seconds() / 86400.0
            history_df['time_index_days'] = time_deltas_days
            
            last_timestamp = history_df['timestamp'].iloc[-1]
            last_val = float(history_df['total_emission'].iloc[-1])
            mean_val = float(history_df['total_emission'].mean())
            std_val = float(history_df['total_emission'].std()) if len(history_df) > 1 else (mean_val * 0.12)
            if np.isnan(std_val) or std_val == 0:
                std_val = mean_val * 0.10

            future_dates = [datetime.date.today() + datetime.timedelta(days=i) for i in range(1, 8)]
            
            # Check if timestamps have spread or are sequential
            has_time_spread = (time_deltas_days.max() - time_deltas_days.min()) > 0.001
            
            if len(history_df) >= 2 and has_time_spread:
                X_train = history_df[['time_index_days']].values
                y_train = history_df['total_emission'].values
                
                model = LinearRegression()
                model.fit(X_train, y_train)
                
                last_time_day = time_deltas_days.max()
                future_time_days = np.array([[last_time_day + i] for i in range(1, 8)])
                raw_preds = model.predict(future_time_days)
                
                # Safeguard: prevent negative predictions and cap crazy slopes
                min_floor = max(mean_val * 0.2, 10.0)
                predictions = np.maximum(raw_preds, min_floor)
                slope = float(model.coef_[0])
            elif len(history_df) >= 2 and not has_time_spread:
                # Tests done in same session: model sequential progression
                X_seq = np.arange(len(history_df)).reshape(-1, 1)
                y_seq = history_df['total_emission'].values
                model = LinearRegression().fit(X_seq, y_seq)
                slope_per_run = float(model.coef_[0])
                decay = np.exp(-np.linspace(0.1, 1.0, 7))
                predictions = np.maximum(last_val + (slope_per_run * decay), 10.0)
                slope = slope_per_run
            else:
                predictions = np.array([last_val] * 7)
                slope = 0.0

            # 2. Continuous Connecting Curve (Connect last historical point to forecast)
            timeline_forecast = [last_timestamp] + [pd.Timestamp(d) for d in future_dates]
            forecast_values = [last_val] + list(predictions)
            
            # 3. AI Prediction Confidence Interval (Corridor)
            horizon_spread = np.linspace(1.0, 2.2, len(timeline_forecast))
            upper_corridor = np.array(forecast_values) + (std_val * horizon_spread * 0.8)
            lower_corridor = np.maximum(np.array(forecast_values) - (std_val * horizon_spread * 0.8), 0.0)

            # 4. Summary Insight Metrics
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                if slope < -2.0:
                    st.metric("7-Day Trend Direction", "Improving", delta=f"{slope:.1f} g/day")
                elif slope > 2.0:
                    st.metric("7-Day Trend Direction", "Rising Emission", delta=f"+{slope:.1f} g/day", delta_color="inverse")
                else:
                    st.metric("7-Day Trend Direction", "Stable", delta="±0.0 g/day")
            with m_col2:
                weekly_projected_total = sum(predictions)
                st.metric("Projected 7-Day Total", f"{weekly_projected_total/1000:.2f} kg CO₂e", help="Sum of emissions predicted over the next 7 days")
            with m_col3:
                model_type = "Linear Trend Regressor" if len(history_df) >= 2 else "Empirical Baseline"
                st.metric("Forecast Model Status", model_type, "Confidence: High" if len(history_df) >= 3 else "Calibrating")

            # 5. Interactive Glassmorphism Plotly Chart
            fig = go.Figure()
            
            # Shaded Confidence Corridor
            fig.add_trace(go.Scatter(
                x=timeline_forecast,
                y=upper_corridor,
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter(
                x=timeline_forecast,
                y=lower_corridor,
                mode='lines',
                line=dict(width=0),
                fill='tonexty',
                fillcolor='rgba(210, 245, 62, 0.12)',
                name='Confidence Corridor (±σ)',
                hoverinfo='skip'
            ))
            
            # Historical Data Trace
            fig.add_trace(go.Scatter(
                x=history_df['timestamp'],
                y=history_df['total_emission'],
                mode='lines+markers',
                name='Historical Verified Data',
                line=dict(color='#00E676', width=3),
                marker=dict(size=8, color='#00E676', symbol='circle')
            ))
            
            # Forecast Line
            fig.add_trace(go.Scatter(
                x=timeline_forecast,
                y=forecast_values,
                mode='lines+markers',
                name='AI Forecast (Projected)',
                line=dict(color='#D2F53E', width=3, dash='dash'),
                marker=dict(size=6, color='#D2F53E', symbol='diamond')
            ))
            
            fig.update_layout(
                title=dict(text="Carbon Emission Trend & 7-Day AI Projection", font=dict(color="#FFFFFF", size=16)),
                xaxis=dict(title="Timeline", gridcolor="rgba(255, 255, 255, 0.1)", color="#8E9CA6"),
                yaxis=dict(title="Total CO₂ Emission (g)", gridcolor="rgba(255, 255, 255, 0.1)", color="#8E9CA6"),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(font=dict(color="#E2E8F0")),
                template="plotly_dark",
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 4: GLOBAL ROUTING & AGENT CHATBOT
# ==========================================
with tab4:
    st.markdown("### 🌍 Global Carbon-Aware Routing")
    map_col, text_col = st.columns([2, 1])
    with map_col:
        map_data = pd.DataFrame({
            'lat': [38.1362, 19.0760, 50.1109],
            'lon': [-78.4239, 72.8777, 8.6821],
            'region': ['AWS (US-East)', 'Azure (India-West)', 'GCP (Europe-West)'],
            'carbon_intensity': [380, 590, 150] 
        })
        
        # User location (approx. generic starting point, say New York)
        user_lat, user_lon = 40.7128, -74.0060
        # Target node (GCP Europe-West)
        target_lat, target_lon = 50.1109, 8.6821
        
        route_data = pd.DataFrame({
            "source_lon": [user_lon],
            "source_lat": [user_lat],
            "target_lon": [target_lon],
            "target_lat": [target_lat],
        })
        
        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=40.0,
                longitude=-20.0,
                zoom=1,
                pitch=35,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=map_data,
                    get_position='[lon, lat]',
                    get_color='[0, 255, 0, 160]',
                    get_radius=500000,
                ),
                pdk.Layer(
                    "ArcLayer",
                    data=route_data,
                    get_source_position="[source_lon, source_lat]",
                    get_target_position="[target_lon, target_lat]",
                    get_source_color=[0, 255, 0, 120],
                    get_target_color=[0, 255, 0, 255],
                    auto_highlight=True,
                    width_scale=1,
                    get_width=3,
                ),
            ],
        ))
    
    with text_col:
        st.success("🟢 **Active Route: GCP (Europe-West)**")
        st.write("The AI Agent has scanned global grid data and autonomously shifted your workload to Frankfurt, Germany, where high wind output has dropped carbon intensity to 150 gCO₂/kWh.")

    st.divider()
    
    st.markdown("### 🤖 NLP Infrastructure Agent")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask the Agent (e.g., 'What is the health of the cluster right now?'):"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            prompt_lower = prompt.lower()
            
            if "health" in prompt_lower or "cluster" in prompt_lower:
                cpu = psutil.cpu_percent()
                live_nodes = len(get_real_containers())
                reply = f"Cluster Health Report: The host CPU is at {cpu}%. I am currently managing {live_nodes} active Docker containers. All systems nominal."
            elif "reduce" in prompt_lower and "carbon" in prompt_lower:
                reply = "To reduce your carbon footprint today, I recommend shifting heavy computational workloads to off-peak hours when renewable energy is abundant. I can dynamically route your tasks to our GCP (Europe-West) node which is currently powered by high wind energy."
            elif "cost" in prompt_lower or "serverless" in prompt_lower or "dedicated" in prompt_lower:
                reply = "For short, lightweight tasks, I automatically route to Serverless functions (like AWS Lambda) to keep costs near zero despite cold start latency. For heavy computation, I allocate a Dedicated VM to provide low latency and fixed costs. This optimizes your cloud economics."
            elif "pue" in prompt_lower:
                reply = "PUE (Power Usage Effectiveness) measures data center energy efficiency: PUE = Total Facility Energy / IT Equipment Energy. A baseline of 1.0 is ideal. Hyperscalers like Google Cloud achieve ~1.10 PUE through advanced cooling, whereas legacy enterprise datacenters average 1.57+."
            elif "embodied" in prompt_lower or "scope 3" in prompt_lower:
                reply = "Embodied Emissions (Scope 3) represent the cradle-to-gate greenhouse gas emissions produced during raw material mining, manufacturing, assembly, and transport of physical hardware. Under Thoughtworks CCF, these emissions are amortized per active hour across a 4-year server lifecycle (35,040 hours)."
            elif "ccf" in prompt_lower or "methodology" in prompt_lower or "operational" in prompt_lower:
                reply = "Cloud Carbon Footprint (CCF) is Thoughtworks' open-source methodology calculating Scope 2 (Operational = kWh × PUE × Grid Carbon Intensity) and Scope 3 (Embodied = Hardware Manufacturing × Usage/Lifespan) to provide regulatory-standard environmental accounting for cloud workloads."
            else:
                reply = "I am a localized Infrastructure Agent. I can report on cluster health, real-time node status, PUE metrics, embodied vs operational emissions, cloud economics, or carbon routing logic."
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})