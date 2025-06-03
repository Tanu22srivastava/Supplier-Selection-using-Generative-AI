import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def get_column_type(series):
    """Detect column type and return an appropriate description"""
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    elif pd.api.types.is_bool_dtype(series):
        return "boolean"
    elif len(series.unique()) <= 10:  
        return "categorical"
    else:
        return "text"  

def get_unique_values(series):
    unique_vals = series.dropna().unique()
    if len(unique_vals) > 30: 
        return unique_vals[:30].tolist(), True  
    return unique_vals.tolist(), False

def analyze_dataset_columns(data):
    column_info = {}
    for col in data.columns:
        col_type = get_column_type(data[col])
        info = {
            'type': col_type,
        }
        if col_type == 'numeric':
            info['min'] = float(data[col].min()) if not pd.isna(data[col].min()) else 0
            info['max'] = float(data[col].max()) if not pd.isna(data[col].max()) else 0
            info['mean'] = float(data[col].mean()) if not pd.isna(data[col].mean()) else 0
        elif col_type in ['categorical', 'boolean']:
            info['unique_values'], info['truncated'] = get_unique_values(data[col])
        column_info[col] = info
    return column_info

def preprocess_data(data):
    if 'Label' in data.columns:
        X = data.drop('Label', axis=1)
        y = data['Label']
    else:
        X = data.copy()
        y = None

    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))

    X = X.fillna(X.mean(numeric_only=True))

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y, X.columns.tolist()