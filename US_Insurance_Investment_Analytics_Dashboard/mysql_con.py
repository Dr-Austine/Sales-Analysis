import pandas as pd
import os

def view_all_data():
    """
    Bypasses MySQL completely and loads the customer data directly 
    from the local CSV file structure for fast cloud deployment.
    """
    # 1. Track down the absolute path to your file structure
    current_dir = os.path.dirname(US_Insurance_Investment_Analytics_Dashboard/data/customers.csv)
    
    # 2. Match the exact location: data/customers.csv relative to your folder
    csv_path = os.path.join(current_dir, "data", "customers.csv")
    
    try:
        # 3. Read the CSV file using Pandas
        df = pd.read_csv(csv_path)
        
        # 4. Convert it back to a raw rows matrix list so Main.py's 
        # pd.DataFrame(result, columns=[...]) construction functions perfectly.
        return df.values.tolist()
        
    except FileNotFoundError:
        # Fallback safety warning if the folder layout doesn't match on GitHub
        print(f"Error: Could not locate data file at {csv_path}")
        return []

