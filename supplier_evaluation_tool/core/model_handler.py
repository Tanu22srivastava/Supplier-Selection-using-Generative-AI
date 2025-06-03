from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
import pandas as pd

def train_model(X, y):
    if y is not None:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test)
        predictions = model.predict(X)
        prediction_probs = model.predict_proba(X)[:, 1] if len(model.classes_) > 1 else predictions
        
        return predictions, prediction_probs, accuracy
    else:
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(X)
        return clusters, clusters, None

def apply_filters_to_data(data, filter_conditions):
    filtered_data = data.copy()
    for column, filter_info in filter_conditions.items():
        filter_type = filter_info['type']
        if filter_type == 'numeric':
            min_val = filter_info.get('min')
            max_val = filter_info.get('max')
            if min_val is not None:
                filtered_data = filtered_data[filtered_data[column] >= min_val]
            if max_val is not None:
                filtered_data = filtered_data[filtered_data[column] <= max_val]
        elif filter_type == 'categorical' or filter_type == 'boolean':
            selected_values = filter_info.get('values', [])
            if selected_values:
                filtered_data = filtered_data[filtered_data[column].isin(selected_values)]
        elif filter_type == 'text':
            search_text = filter_info.get('search', '')
            if search_text:
                filtered_data = filtered_data[filtered_data[column].astype(str).str.contains(search_text, case=False, na=False)]
    return filtered_data

def rank_suppliers(data, filter_conditions, predictions=None, prediction_probs=None, selected_criteria=None, sort_directions=None):
    filtered_data = apply_filters_to_data(data, filter_conditions) if filter_conditions else data.copy()
    
    if len(filtered_data) == 0:
        return None, "No suppliers match all selected filters. Please adjust your criteria."
    
    if selected_criteria:
        try:
            ranked_data = filtered_data.sort_values(by=selected_criteria, ascending=sort_directions)
        except KeyError as e:
            return None, f"Error: {e}. One or more columns do not exist in the dataset."
    else:
        if prediction_probs is not None:
            score_mapping = dict(zip(data.index, prediction_probs))
            filtered_data['Supplier_Score'] = filtered_data.index.map(score_mapping)
        else:
            score_mapping = dict(zip(data.index, predictions)) if predictions is not None else {}
            filtered_data['Supplier_Score'] = filtered_data.index.map(score_mapping)
        
        ranked_data = filtered_data.sort_values(by='Supplier_Score', ascending=False)
    
    return ranked_data, None