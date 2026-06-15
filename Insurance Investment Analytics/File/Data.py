import pandas as pd
import random
from datetime import datetime, timedelta

# Set random seed for consistent data regeneration
random.seed(42)

# Factual U.S. Census Bureau Regions and States Mapping
US_DATA = {
    'Northeast': ['New York', 'Pennsylvania', 'New Jersey', 'Massachusetts', 'Connecticut', 'New Hampshire', 'Rhode Island', 'Maine', 'Vermont'],
    'Midwest': ['Illinois', 'Ohio', 'Michigan', 'Indiana', 'Wisconsin', 'Minnesota', 'Missouri', 'Iowa', 'Kansas', 'Nebraska', 'South Dakota', 'North Dakota'],
    'South': ['Texas', 'Florida', 'Georgia', 'North Carolina', 'Virginia', 'Tennessee', 'Maryland', 'South Carolina', 'Alabama', 'Kentucky', 'Louisiana', 'Oklahoma', 'Arkansas', 'Mississippi', 'West Virginia', 'Delaware'],
    'West': ['California', 'Washington', 'Arizona', 'Colorado', 'Oregon', 'Utah', 'Nevada', 'New Mexico', 'Idaho', 'Hawaii', 'Montana', 'Alaska', 'Wyoming']
}

# Invert dictionary for easy lookup during structural state selections
STATE_TO_REGION = {state: region for region, states in US_DATA.items() for state in states}
ALL_STATES = list(STATE_TO_REGION.keys())

# Define business variables aligned to structured profiles
LOCATIONS = ['Urban', 'Rural']
CONSTRUCTIONS = ['Frame', 'Fire Resist', 'Masonry']
BUSINESS_TYPES = {
    'Retail': {'min_inv': 300000, 'max_inv': 2500000},
    'Apartment': {'min_inv': 1500000, 'max_inv': 15000000},
    'Farming': {'min_inv': 100000, 'max_inv': 1200000},
    'Hospitality': {'min_inv': 2000000, 'max_inv': 18000000},
    'Office Bldg': {'min_inv': 1000000, 'max_inv': 12000000},
    'Medical': {'min_inv': 3000000, 'max_inv': 20000000},
    'Other': {'min_inv': 500000, 'max_inv': 5000000}
}

def generate_insurance_dataset(num_rows=500):
    data_list = []
    
    # Generate sequential unique policy codes starting at 100001
    start_policy = 100001
    
    # Date generation range around the 2021 timeframe from the image
    start_date = datetime(2021, 1, 1)
    
    for i in range(num_rows):
        policy = start_policy + i
        
        # Expiry: Spread randomly across a year
        random_days = random.randint(0, 365)
        expiry_date = (start_date + timedelta(days=random_days)).strftime('%e-%b-%y').strip()
        
        # Factual Geographic Layout
        state = random.choice(ALL_STATES)
        region = STATE_TO_REGION[state]
        location = random.choice(LOCATIONS)
        
        # Adjust business selection based on location constraints for realism
        if location == 'Rural':
            business_type = random.choices(['Farming', 'Retail', 'Other'], weights=[0.70, 0.20, 0.10])[0]
            construction = random.choices(['Frame', 'Masonry'], weights=[0.75, 0.25])[0]
        else: # Urban
            business_type = random.choice([b for b in BUSINESS_TYPES.keys() if b != 'Farming'])
            construction = random.choices(['Masonry', 'Fire Resist', 'Frame'], weights=[0.45, 0.35, 0.20])[0]
            
        # Realistic business financial ranges using distribution settings
        inv_range = BUSINESS_TYPES[business_type]
        investment = random.randint(inv_range['min_inv'], inv_range['max_inv'])
        
        # Contextual risk flags based on regional geography logic
        # Example: West Coast/Mountain has higher earthquake risks; Coastal South/Midwest has flood risks
        if region in ['West']:
            earthquake = random.choices(['Y', 'N'], weights=[0.40, 0.60])[0]
            flood = random.choices(['Y', 'N'], weights=[0.10, 0.90])[0]
        elif region in ['South', 'Midwest']:
            earthquake = random.choices(['Y', 'N'], weights=[0.05, 0.95])[0]
            flood = random.choices(['Y', 'N'], weights=[0.35, 0.65])[0]
        else: # Northeast
            earthquake = random.choices(['Y', 'N'], weights=[0.05, 0.95])[0]
            flood = random.choices(['Y', 'N'], weights=[0.20, 0.80])[0]
            
        # Risk Ratings generated between 1.0 and 10.0
        rating = round(random.uniform(1.0, 10.0), 1)
        
        # Match data mapping layout from target image
        row = {
            'Policy': policy,
            'Expiry': expiry_date,
            'Location': location,
            'State': state,
            'Region': region,
            'Investment': investment,
            'Construction': construction,
            'BusinessType': business_type,
            'Earthquake': earthquake,
            'Flood': flood,
            'Rating': rating
        }
        data_list.append(row)
        
    return pd.DataFrame(data_list)

# Generate and save the file
df = generate_insurance_dataset(1000)
df.to_csv('US_Insurance_Analytics_Data.csv', index=False)

print("Successfully generated 'US_Insurance_Analytics_Data.csv' with 500 rows of factual geographical attributes!")