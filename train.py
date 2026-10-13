import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# 1. Generate a Synthetic Dataset (1,000 simulated users)
np.random.seed(42)
num_samples = 1000

# Randomize user habits (hours per day)
coding = np.random.randint(0, 13, num_samples)
streaming = np.random.randint(0, 11, num_samples)
heavy = np.random.randint(0, 9, num_samples)

# Hardware power efficiency weights
# e.g., Mac (Apple Silicon) = 1.0 (highly efficient), Windows PC = 1.5 (consumes more power)
pc_weight = np.random.choice([1.0, 1.5, 1.2], num_samples)
# e.g., OnePlus 12 / iPhone = 1.0, Older/larger batteries = 1.1
mobile_weight = np.random.choice([1.0, 1.0, 1.1], num_samples)

# Calculate target emissions using authentic Cloud Carbon Footprint (CCF) methodology:
# Operational: Energy (kWh) * PUE * Grid Intensity (g/kWh)
# Embodied: Manufacturing Carbon * (Usage Hours / Lifespan Hours)

# 1. Operational Power (Watts)
# Coding: ~25% utilization; Heavy: ~85% utilization; Mobile: ~2.5W average
pc_idle = pc_weight * 15.0
pc_max = pc_weight * 70.0
coding_watts = pc_idle + 0.25 * (pc_max - pc_idle)
heavy_watts = pc_idle + 0.85 * (pc_max - pc_idle)
mobile_watts = mobile_weight * 2.5

pc_coding_kwh = (coding_watts * coding) / 1000.0
pc_heavy_kwh = (heavy_watts * heavy) / 1000.0
mobile_streaming_kwh = (mobile_watts * streaming) / 1000.0

total_kwh = pc_coding_kwh + pc_heavy_kwh + mobile_streaming_kwh
pue = 1.12 # Cloud & datacenter average PUE
grid_intensity = 400.0 # gCO2e per kWh average

operational_emissions = total_kwh * pue * grid_intensity

# 2. Embodied Emissions (Scope 3 GHG Protocol)
# PC lifespan: 35,040 hrs (4 yrs); Mobile: 26,280 hrs (3 yrs)
pc_embodied_total = pc_weight * 220000.0 # g CO2e cradle-to-gate
mobile_embodied_total = mobile_weight * 65000.0

pc_usage_hours = coding + heavy
mobile_usage_hours = streaming

embodied_emissions = (pc_embodied_total * (pc_usage_hours / 35040.0)) + (mobile_embodied_total * (mobile_usage_hours / 26280.0))

# Total CCF Carbon Emissions (gCO2e)
emissions = operational_emissions + embodied_emissions + np.random.normal(5, 2, num_samples)

# Build the DataFrame
df = pd.DataFrame({
    'coding_hours': coding,
    'streaming_hours': streaming,
    'heavy_hours': heavy,
    'pc_weight': pc_weight,
    'mobile_weight': mobile_weight,
    'carbon_emission': emissions
})

# 2. Train the Random Forest AI Model
X = df[['coding_hours', 'streaming_hours', 'heavy_hours', 'pc_weight', 'mobile_weight']]
y = df['carbon_emission']

print("Training Random Forest Regressor...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 3. Export the trained model
joblib.dump(model, 'carbon_model.pkl')
print("✅ AI Model successfully trained and saved as 'carbon_model.pkl'!")