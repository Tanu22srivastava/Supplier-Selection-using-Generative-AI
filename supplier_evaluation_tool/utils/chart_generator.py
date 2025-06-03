import matplotlib.pyplot as plt
import pandas as pd
def generate_chart(data, selected_criteria=None, top_n=10):
    """Generate a comparison chart of the top N suppliers"""
    data_to_plot = data.head(top_n).copy()
    
    # Find an ID column to use for labels
    id_columns = ['Supplier_ID', 'SupplierID', 'ID', 'supplier_id']
    id_col = None
    for col in id_columns:
        if col in data_to_plot.columns:
            id_col = col
            break
    
    if id_col:
        labels = data_to_plot[id_col].astype(str).tolist()
    else:
        labels = [f"Supplier {i+1}" for i in range(len(data_to_plot))]
    
    # Truncate long labels
    labels = [str(label)[:10] + '...' if len(str(label)) > 10 else str(label) for label in labels]
    
    x_positions = list(range(len(labels)))
    
    if selected_criteria and len(selected_criteria) > 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Filter criteria to only include numeric columns present in the data
        valid_criteria = [c for c in selected_criteria if c in data_to_plot.columns and 
                         pd.api.types.is_numeric_dtype(data_to_plot[c])]
        
        if not valid_criteria:
            # If no valid numeric criteria, find some numeric columns to plot
            numeric_cols = data_to_plot.select_dtypes(include=['int64', 'float64']).columns.tolist()
            cols_to_exclude = ['Supplier_Score', 'index', 'Label']
            valid_criteria = [col for col in numeric_cols if col not in cols_to_exclude][:3]
        
        bar_width = 0.8 / len(valid_criteria) if len(valid_criteria) > 0 else 0.8
        
        for i, criterion in enumerate(valid_criteria):
            values = data_to_plot[criterion].values
            offset = i * bar_width - (len(valid_criteria) - 1) * bar_width / 2
            bar_positions = [pos + offset for pos in x_positions]
            ax.bar(bar_positions, values, width=bar_width, label=criterion)
        
        plt.title('Supplier Comparison Based on Selected Criteria', fontsize=14, pad=20)
        plt.xlabel('Suppliers', fontsize=12, labelpad=10)
        plt.ylabel('Value', fontsize=12, labelpad=10)
        plt.legend(fontsize=10, loc='best')
        plt.xticks(x_positions, labels, rotation=45, ha='right', fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout(pad=3.0)
        return fig
    
    else:
        try:
            if 'Supplier_Score' in data_to_plot.columns:
                fig, ax = plt.subplots(figsize=(12, 6))
                values = data_to_plot['Supplier_Score'].values
                ax.bar(x_positions, values, color='cornflowerblue')
                plt.title('Supplier Comparison: Model Score', fontsize=14, pad=20)
                plt.xlabel('Suppliers', fontsize=12, labelpad=10)
                plt.ylabel('Score', fontsize=12, labelpad=10)
                plt.xticks(x_positions, labels, rotation=45, ha='right', fontsize=10)
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.tight_layout(pad=3.0)
                return fig
            
            numeric_cols = data_to_plot.select_dtypes(include=['int64', 'float64']).columns.tolist()
            cols_to_exclude = ['Supplier_Score', 'index', 'Label']
            plot_cols = [col for col in numeric_cols if col not in cols_to_exclude]
            
            if not plot_cols:
                plot_cols = [col for col in data_to_plot.columns if col not in cols_to_exclude]
            
            if len(plot_cols) > 0:
                best_chart_col = plot_cols[0]
                
                if len(plot_cols) > 1:
                    best_variance = data_to_plot[plot_cols[0]].var()
                    for col in plot_cols[1:]:
                        if data_to_plot[col].var() > best_variance:
                            best_variance = data_to_plot[col].var()
                            best_chart_col = col
                
                fig, ax = plt.subplots(figsize=(12, 6))
                values = data_to_plot[best_chart_col].values
                ax.bar(x_positions, values, color='cornflowerblue')
                plt.title(f'Supplier Comparison: {best_chart_col}', fontsize=14, pad=20)
                plt.xlabel('Suppliers', fontsize=12, labelpad=10)
                plt.ylabel(best_chart_col, fontsize=12, labelpad=10)
                plt.xticks(x_positions, labels, rotation=45, ha='right', fontsize=10)
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.tight_layout(pad=3.0)
                return fig
            
            else:
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.bar(x_positions, [1] * len(x_positions))
                plt.title('Supplier Comparison', fontsize=14)
                plt.xlabel('Suppliers', fontsize=12)
                plt.xticks(x_positions, labels, rotation=45)
                plt.tight_layout()
                return fig
        
        except Exception as e:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(x_positions, [1] * len(x_positions))
            plt.title('Supplier Comparison (Error in data processing)', fontsize=14)
            plt.xlabel('Suppliers', fontsize=12)
            plt.xticks(x_positions, labels, rotation=45)
            plt.tight_layout()
            return fig