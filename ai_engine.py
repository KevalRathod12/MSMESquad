import joblib
import pandas as pd
import numpy as np
from PIL import Image

# ---------------------------------------------------------
# 1. LOAD SAVED MODELS (Magaj Jagado)
# ---------------------------------------------------------
print("⚙️ Loading AI Models...")

try:
    model_maint = joblib.load('models/maintenance_model.pkl')
    model_inv = joblib.load('models/inventory_model.pkl')
    features_inv = joblib.load('models/inventory_features.pkl') # Columns yaad rakhva
    model_energy = joblib.load('models/energy_model.pkl')
    high_energy_cluster = joblib.load('models/energy_high_cluster.pkl')
    model_quality = joblib.load('models/quality_model.pkl')
    print("✅ All AI Models Loaded Successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    print("Please run 'train_models.py' first.")

# ---------------------------------------------------------
# 2. DEFINE INTELLIGENT FUNCTIONS (Aa functions App ma vaparsu)
# ---------------------------------------------------------

def analyze_machine_health(vibration, temperature):
    """
    Input: Machine Sensor Data
    Output: 'Risk' or 'Normal' status
    """
    # Model ne jevu input joiye tevu banavu padse (2D array)
    input_data = [[vibration, temperature]]
    prediction = model_maint.predict(input_data)
    
    if prediction[0] == 1:
        return "⚠️ CRITICAL RISK: High probability of breakdown!"
    else:
        return "✅ Machine Health is Optimal."

def forecast_demand(day_of_year, month, is_weekend, product_id):
    """
    Input: Date details & Product ID
    Output: Predicted Sales Quantity
    """
    # Empty dataframe banavo jema badhi columns hoy
    input_df = pd.DataFrame(columns=features_inv)
    
    # Ek row add karo (0 values sathe)
    input_df.loc[0] = 0
    
    # Values set karo
    input_df['Day_Num'] = day_of_year
    input_df['Month'] = month
    input_df['Is_Weekend'] = 1 if is_weekend else 0
    
    # Product ID wali column ne 1 karo (One-Hot Encoding logic)
    prod_col = f"Product_ID_{product_id}"
    if prod_col in input_df.columns:
        input_df[prod_col] = 1
        
    # Prediction karo
    predicted_qty = model_inv.predict(input_df)[0]
    return int(predicted_qty)

def detect_energy_waste(kwh_usage):
    """
    Input: Electricity Usage (kWh)
    Output: Is it High or Normal?
    """
    # Cluster predict karo
    cluster = model_energy.predict([[kwh_usage]])[0]
    
    if cluster == high_energy_cluster:
        return "⚠️ High Energy Consumption Detected (Potential Waste)"
    else:
        return "✅ Energy Usage is within Efficient Range"

def check_product_quality(image_file):
    """
    Input: Uploaded Image File
    Output: 'Defective' or 'Good'
    """
    # Image process karo (resize & grey)
    img = Image.open(image_file).convert('L').resize((64, 64))
    img_array = np.array(img).flatten().reshape(1, -1)
    
    prediction = model_quality.predict(img_array)
    
    if prediction[0] == 1:
        return "❌ Defect Detected"
    else:
        return "✅ Quality Passed"