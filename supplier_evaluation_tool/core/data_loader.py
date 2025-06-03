import pandas as pd

def load_data(uploaded_file):
    try:
        data = pd.read_csv(uploaded_file)
        return data
    except Exception as e:
        raise ValueError(f"Error loading dataset: {str(e)}")