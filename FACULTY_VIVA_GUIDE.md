# EcoScale AI: Faculty Presentation & Viva Defense Guide

---

## 1. Executive Summary & Project Abstract

### What is EcoScale AI?
**EcoScale AI** is an autonomous, cloud-native **Carbon Intelligence and Infrastructure Orchestration Platform**. It bridges the gap between **sustainable software engineering (Green Cloud Computing)** and **autonomous DevOps / Infrastructure as Code (IaC)**.

### The Problem It Solves
1. **The Digital Carbon Blindspot:** Modern developers and students rarely understand the environmental cost of their daily hardware usage, heavy model training, and continuous cloud deployments.
2. **Static vs. Elastic Infrastructure:** Traditional cloud deployments run idle servers, consuming constant baseline electricity ($P_{\text{idle}}$) and inflating Power Usage Effectiveness (PUE) losses.
3. **Regulatory Non-Compliance:** Modern ESG (Environmental, Social, and Governance) compliance mandates rigorous accounting of **Scope 2 (Operational emissions)** and **Scope 3 (Embodied hardware manufacturing emissions)** under the GHG Protocol.

### The EcoScale Solution
EcoScale calculates fine-grained carbon footprints using **enterprise Thoughtworks Cloud Carbon Footprint (CCF)** equations, while an **Autonomous AI Agent** monitors host telemetry, dynamically scales live Docker microservice containers up or down, and reroutes traffic across global regions based on real-time grid carbon intensity.

---

## 2. System Architecture & Tech Stack

```
                          ┌──────────────────────────────────────────────┐
                          │         CLIENT BROWSER (PORT 8501)           │
                          │   EcoScale Dark Nature Frosted Glass UI      │
                          └──────────────────────┬───────────────────────┘
                                                 │
                                                 ▼
                          ┌──────────────────────────────────────────────┐
                          │         STREAMLIT APPLICATION (app.py)        │
                          │   • Security Gateway (Admin RBAC)            │
                          │   • CCF Enterprise Mathematical Engine       │
                          │   • Autonomous Scaling Daemon (psutil)       │
                          │   • AI Time-Series Forecaster (Scikit-Learn) │
                          │   • PyDeck 3D Geospatial Visualizer          │
                          └───────┬───────────────────────────────┬──────┘
                                  │                               │
            Docker Engine Control │ (IaC Subprocess)              │ REST API (JSON)
                                  ▼                               ▼
      ┌────────────────────────────────────────┐     ┌──────────────────────────────┐
      │          DOCKER DAEMON / DinD          │     │     NODE.JS / EXPRESS API    │
      │  ┌──────────────┐   ┌──────────────┐   │     │  (Running in active node)    │
      │  │ node-1 (5001)│   │ node-2 (5002)│   │◄────┤  POST /api/history           │
      │  └──────────────┘   └──────────────┘   │     │  GET  /api/history/:username │
      │  ┌──────────────┐   ┌──────────────┐   │     └──────────────┬───────────────┘
      │  │ node-3 (5003)│   │ node-dr (DR) │   │                    │
      │  └──────────────┘   └──────────────┘   │                    │ Mongoose ODM
      └────────────────────────────────────────┘                    ▼
                                                     ┌──────────────────────────────┐
                                                     │     MONGODB ATLAS CLOUD      │
                                                     │  Collection: 'histories'     │
                                                     │  (Emissions, PUE, Energy)    │
                                                     └──────────────────────────────┘
```

### Complete Technology Stack Table

| Layer | Technology | Role / Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit 1.62+, Custom CSS (`style.css`), Plotly Express/GO, PyDeck | Frosted glassmorphic interface, interactive 3D geospatial arc globe, dual-trace forecasting charts |
| **Host Telemetry** | `psutil` (Python System & Process Utilities) | Real-time physical CPU load sampling, RAM utilization monitoring |
| **Orchestration / IaC** | Docker Engine, Docker-in-Docker (DinD), `subprocess` | Programmatic container provisioning (`node-1` to `node-5`), port routing, Chaos Monkey disruption, self-healing DR |
| **Calculation Engine** | Thoughtworks CCF + GHG Protocol Scope 2 & 3 | Dynamic power curve, PUE multipliers, cradle-to-gate hardware amortization |
| **Machine Learning** | Random Forest Regressor (`joblib`), Ordinary Least Squares (`sklearn.linear_model.LinearRegression`) | Supervised emission estimation and continuous-time fractional time-series projection |
| **Backend API** | Node.js 20, Express 5, CORS, Dotenv | Microservice layer inside Docker containers handling persistence and historical queries |
| **Database** | MongoDB Atlas (Cloud M0 Cluster), Mongoose 9 ODM | Persistent storage of emission metrics, energy consumption, and timestamps |
| **Cloud Hosting** | GitHub Codespaces / FCMCompute (OpenStack) | Containerized cloud VM hosting with public port forwarding (Port 8501) |

---

## 3. The 4 Functional Modules (Tab-by-Tab Breakdown)

### 🔒 Security Gateway
* **Mechanism:** Blocks access until administrator credentials (`admin123`) are authenticated.
* **Faculty Value:** Demonstrates enterprise Role-Based Access Control (RBAC) and prevents unauthorized manipulation of live cloud infrastructure.

### Tab 1: ⚡ Personal CCF Engine
* **Input Parameters:** Hardware Profile (Mac, Windows, Linux; Mobile: Apple, OnePlus, Samsung), Datacenter Choice (GCP Frankfurt, AWS Virginia, Azure Pune), Daily Habits (Coding hours, Streaming hours, Heavy compute / ML hours).
* **Autonomous Provisioning:** When the user clicks **Calculate Footprint**:
  1. Inspects active Docker containers. If zero nodes exist, boots `node-1` on Port 5001.
  2. If a heavy computational workload is detected ($\ge 2$ hrs heavy compute or $\ge 6$ hrs coding), the AI agent dynamically scales up an additional dedicated worker instance (`node-2`, `node-3`, etc.) on port `5000 + n`.
  3. Executes the full CCF mathematical model.
  4. Routes payload to the newly provisioned container over HTTP REST, persisting the record to MongoDB.
* **Advisory Engine:** Evaluates Cloud Economics:
  * Heavy workload $\rightarrow$ Routed to **Dedicated VM** ($0.15/hr, zero cold start latency).
  * Light workload $\rightarrow$ Routed to **Serverless Function (AWS Lambda)** ($0.0001 per invocation, event-driven).
* **Visualizations:**
  * 4 Executive KPI Cards (Total Carbon, Scope 2 Operational, Scope 3 Embodied %, Energy in kWh).
  * Scope 2 vs Scope 3 Donut Chart.
  * Subsystem Carbon Impact Horizontal Bar Chart.
  * Mathematical Derivation Expander with LaTeX formulas.

### Tab 2: ☁️ Command Center (Live Cloud Orchestrator)
* **Live Topology Table:** Real-time query of `docker ps` displaying active node names, container IDs, running status, and port bindings.
* **True Auto-Scaling Daemon (Kubernetes HPA Mode):**
  * Powered by `streamlit-autorefresh` (3000ms polling interval).
  * Samples `psutil.cpu_percent()`.
  * **Scale-Up Rule:** If physical CPU load exceeds **60%** and active nodes $< 5$, provisions a new container.
  * **Scale-Down Rule:** If CPU load drops below **20%** and active nodes $> 1$, gracefully terminates the highest-numbered container to conserve energy.
* **Chaos Engineering & Self-Healing Disaster Recovery:**
  * Simulates Netflix's **Chaos Monkey**: picks an active container at random and forcefully kills it (`docker rm -f`).
  * **Self-Healing Agent:** Detects the sudden failure, issues an alert, and autonomously spins up a Disaster Recovery node (`<target>-dr`) on a new port, proving High Availability (HA) and Zero Data Loss.

### Tab 3: 🗄️ Historical Forecasts & Time-Series AI
* **User Search:** Queries MongoDB Atlas via backend GET endpoint for past records of a student/user ID.
* **Continuous Time-Series Engine:**
  * Solves the 0-variance collapse problem by measuring fractional days: $\Delta t = \frac{\text{seconds}}{86400}$.
  * Trains a `LinearRegression` model to project a 7-day trajectory.
  * Enforces physical non-negative constraints (emissions cannot drop below device idle baseline).
* **AI Uncertainty Corridor:**
  * Plots a shaded $\pm\sigma$ standard error corridor that widens over the 7-day horizon to represent model uncertainty.
  * Renders a continuous, seamless dashed projection directly anchored to the latest verified data point.
* **Executive Metrics:** Displays 7-day slope direction (Improving vs. Rising), projected weekly total in kg $CO_2e$, and model confidence status.

### Tab 4: 🌍 Global Grid Routing & NLP Agent
* **3D Geospatial PyDeck Visualization:** Renders regional nodes across AWS (US-East), Azure (India-West), and GCP (Europe-West) with animated green arcs indicating traffic routing.
* **Carbon-Aware Routing Logic:** Reroutes traffic to GCP Frankfurt where high wind power output yields the lowest grid carbon intensity ($150 \text{ gCO}_2e/\text{kWh}$).
* **NLP Infrastructure Agent:** Conversational chatbot that answers queries about real-time CPU telemetry, container count, PUE definitions, Scope 2 vs Scope 3 differences, and Cloud Economics.

---

## 4. The Core Mathematics (What to Write on the Whiteboard)

If your faculty asks: *"What exact mathematical equations did you implement?"*, present these three equations:

### Equation 1: Total Cloud Carbon Footprint
$$\text{Total Footprint } (g\text{CO}_2e) = \text{Operational Emissions (Scope 2)} + \text{Embodied Emissions (Scope 3)}$$

---

### Equation 2: Scope 2 Operational Emissions (Energy & Grid)
$$\text{Operational Emissions} = \sum \Big( \text{Energy}_{\text{hardware}} (\text{kWh}) \times \text{PUE} \times I_{\text{grid}} \Big)$$

Where:
1. **Dynamic Power Consumption (Watts):**
   $$P(\text{util}) = P_{\text{idle}} + \text{Utilization} \times (P_{\text{max}} - P_{\text{idle}})$$
   * Coding/Study utilization is modeled at **25%**.
   * Heavy computation / ML training is modeled at **85%**.
2. **Energy Calculation (kWh):**
   $$\text{Energy} (\text{kWh}) = \frac{P(\text{util}) \times \text{Active Hours}}{1000}$$
3. **PUE (Power Usage Effectiveness):**
   $$\text{PUE} = \frac{\text{Total Facility Energy Consumed}}{\text{IT Equipment Energy Consumed}}$$
   * GCP Frankfurt: $\text{PUE} = 1.10$ | $I_{\text{grid}} = 150 \text{ gCO}_2e/\text{kWh}$
   * AWS Virginia: $\text{PUE} = 1.135$ | $I_{\text{grid}} = 380 \text{ gCO}_2e/\text{kWh}$
   * Azure Pune: $\text{PUE} = 1.125$ | $I_{\text{grid}} = 590 \text{ gCO}_2e/\text{kWh}$

---

### Equation 3: Scope 3 Embodied Emissions (Manufacturing Lifecycle)
$$\text{Embodied Emissions} = \sum \left( M_{\text{manufacturing}} \times \frac{\text{Active Usage Time (hours)}}{\text{Hardware Lifespan (hours)}} \right)$$

* **Amortization Standard:**
  * Laptops / Workstations / Servers: 4-year lifespan ($35,040\text{ hours}$).
  * Mobile Devices: 3-year lifespan ($26,280\text{ hours}$).
* **Cradle-to-gate Manufacturing Carbon ($M_{\text{manufacturing}}$):**
  * Apple Silicon Mac: $185,000 \text{ g } (185\text{ kg } CO_2e)$
  * Windows PC: $350,000 \text{ g } (350\text{ kg } CO_2e)$
  * Linux Workstation: $450,000 \text{ g } (450\text{ kg } CO_2e)$
  * Cloud Server Slice: $150,000 \text{ g } (150\text{ kg } CO_2e)$

---

## 5. Top 10 Faculty Viva Questions & Perfect Answers

#### Q1: "How does your Python code actually control Docker containers?"
> **Answer:** "In `app.py`, the system communicates with the host Docker daemon via Python's `subprocess` module. We execute commands like `docker ps`, `docker run -d`, and `docker rm -f`. To avoid naming collisions and stopped-container errors, our container manager automatically removes existing instances with `docker rm -f <name>` before launching. In cloud environments like GitHub Codespaces, this runs via Docker-in-Docker (DinD) enabled in `.devcontainer/devcontainer.json`."

#### Q2: "What is the difference between Scope 1, Scope 2, and Scope 3 emissions in your project?"
> **Answer:** "Under the GHG Protocol:
> * **Scope 1:** Direct emissions from sources owned or controlled by the company (e.g., burning diesel in backup datacenter generators).
> * **Scope 2:** Indirect emissions from the consumption of purchased electricity. In EcoScale, this is our **Operational Emissions**, calculated as energy consumed multiplied by PUE and regional grid carbon intensity ($gCO_2e/kWh$).
> * **Scope 3:** Indirect supply chain emissions. In EcoScale, this is our **Embodied Emissions**, covering the extraction, manufacturing, and transport of computing hardware amortized over its operational lifespan."

#### Q3: "What is PUE and why does it matter in cloud computing?"
> **Answer:** "PUE stands for Power Usage Effectiveness. It is the ratio of total facility power (cooling, lighting, power distribution losses) to the actual power delivered to the computing IT equipment: $\text{PUE} = \frac{\text{Total Facility Power}}{\text{IT Equipment Power}}$. A theoretical baseline of 1.0 represents 100% efficiency. Legacy data centers operate around 1.57, whereas modern hyperscalers like Google achieve ~1.10 through liquid cooling and AI-driven thermal optimization."

#### Q4: "Why did you use Linear Regression for forecasting instead of ARIMA or LSTM?"
> **Answer:** "For individual user sessions with 5 to 50 historical datapoints, deep learning models like LSTM suffer from severe overfitting, and ARIMA requires stationary, strictly periodic time-series. We implemented Ordinary Least Squares (OLS) with fractional time indexing ($\Delta t = \text{seconds}/86400$) combined with a statistical confidence corridor ($\pm\sigma$) and an empirical non-negative baseline floor. This provides stable, interpretable trendlines without vanishing gradients or cold-start errors."

#### Q5: "Is the auto-scaling real or simulated?"
> **Answer:** "The scaling is **100% real and programmatic**. The application inspects the host's physical CPU metrics using `psutil`. When load exceeds 60% or when a heavy workload is submitted, the code physically issues a `docker run` command to spin up a new container (`node-2`, `node-3`, etc.) listening on ports 5002, 5003, and maps real HTTP network traffic to it."

#### Q6: "What happens when Chaos Monkey kills a container? How does disaster recovery work?"
> **Answer:** "When Chaos Monkey executes, it selects a live container at random and kills it forcefully via `docker rm -f`. The agent detects the failure and triggers self-healing logic: it dynamically provisions a disaster recovery container named `<target>-dr` on a fresh port and reroutes traffic with zero downtime, proving fault tolerance and High Availability."

#### Q7: "How is MongoDB connected and how do containers share data?"
> **Answer:** "Each container runs our Express microservice (`backend/server.js`) connected to a shared MongoDB Atlas cloud cluster via `MONGO_URI`. Because the database is hosted centrally in the cloud rather than locally in the container, any container node can read or write history records independently."

#### Q8: "What is Carbon-Aware Routing?"
> **Answer:** "Carbon-aware routing is an optimization strategy where computational workloads are routed to geographic datacenters powered by low-carbon energy sources at that specific time. In Tab 4, we demonstrate shifting workloads from fossil-heavy grids (like India-West at $590 \text{ gCO}_2e/\text{kWh}$) to renewable-rich grids (like GCP Frankfurt at $150 \text{ gCO}_2e/\text{kWh}$ powered by wind)."

#### Q9: "Why does heavy compute cost more in emissions than streaming?"
> **Answer:** "Streaming is network-intensive and runs on a power-efficient mobile chip consuming ~2.5W. Heavy compute / machine learning utilizes GPU and CPU cores at ~85% load, driving workstation power draw up to 130W–230W. Over multiple hours, this produces significantly higher kilowatt-hour consumption and resulting carbon emissions."

#### Q10: "How is your project structured for production deployment?"
> **Answer:** "The project is container-ready. We provide:
> 1. A multi-stage `Dockerfile` for the Node.js backend microservice.
> 2. A `.devcontainer/devcontainer.json` for 1-click cloud deployment in GitHub Codespaces with Docker-in-Docker.
> 3. An automated Bash script `setup_fcmcompute.sh` that provisions persistent `systemd` background services on OpenStack / FCMCompute VMs."
