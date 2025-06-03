import streamlit as st

# Import modules from your organized structure
from ui.header import render_header
from ui.sidebar import render_sidebar
from core.data_loader import load_data
from core.data_preprocessor import preprocess_data
from core.model_handler import train_model, rank_suppliers
from utils.chart_generator import generate_chart
from utils.report_generator import generate_supplier_report
from utils.pdf_exporter import create_pdf

if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'ranked_data' not in st.session_state:
    st.session_state['ranked_data'] = None
if 'report' not in st.session_state:
    st.session_state['report'] = None
if 'chart_fig' not in st.session_state:
    st.session_state['chart_fig'] = None
if 'criteria_selected' not in st.session_state:
    st.session_state['criteria_selected'] = []
if 'column_info' not in st.session_state:
    st.session_state['column_info'] = {}
if 'filter_conditions' not in st.session_state:
    st.session_state['filter_conditions'] = {}
if 'has_label' not in st.session_state:
    st.session_state['has_label'] = False

render_header()

render_sidebar()

st.markdown("<h2 class='sub-header'>Step 1: Upload Supplier Data</h2>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your supplier dataset (CSV)", type="csv")

if uploaded_file is not None:
    try:
        data = load_data(uploaded_file)
        st.session_state['data'] = data
        st.session_state['has_label'] = 'Label' in data.columns

        from core.data_preprocessor import analyze_dataset_columns
        st.session_state['column_info'] = analyze_dataset_columns(data)

        st.success(f"✅ Dataset loaded successfully! ({data.shape[0]} rows, {data.shape[1]} columns)")
        if st.session_state['has_label']:
            st.info("📋 Supervised dataset detected with 'Label' column. Will use supervised learning approach.")

        with st.expander("Data Preview"):
            st.dataframe(data.head())
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<p class='info-text'><b>Column Types:</b></p>", unsafe_allow_html=True)
                st.write(data.dtypes)
            with col2:
                st.markdown("<p class='info-text'><b>Summary Statistics:</b></p>", unsafe_allow_html=True)
                st.write(data.describe().round(2))

    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")


if st.session_state['data'] is not None:
    st.markdown("<h2 class='sub-header'>Step 2: Select Ranking Method</h2>", unsafe_allow_html=True)
    ranking_method = st.radio(
        "How would you like to rank suppliers?",
        ["Use AI-powered evaluation", "Select specific criteria"]
    )

    selected_criteria = []
    sort_directions = []

    if ranking_method == "Select specific criteria":
        criteria_options = st.multiselect(
            "Select criteria to rank suppliers:",
            options=st.session_state['data'].columns.tolist(),
            help="Choose the attributes that matter most to you."
        )
        st.session_state['criteria_selected'] = criteria_options

        if criteria_options:
            st.markdown("<p class='info-text'>Configure ranking parameters for each criterion:</p>", unsafe_allow_html=True)
            for criterion in criteria_options:
                col_info = st.session_state['column_info'].get(criterion, {})
                col_type = col_info.get('type', 'text')

                with st.container():
                    st.markdown(f"<div class='filter-section'>", unsafe_allow_html=True)
                    st.markdown(f"<span class='highlight'>{criterion}</span> ({col_type})", unsafe_allow_html=True)

                    if col_type == 'numeric':
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            sort_dir = st.radio(
                                f"Sort direction for {criterion}",
                                ["Ascending", "Descending"],
                                key=f"sort_{criterion}",
                                horizontal=True
                            )
                            sort_directions.append(True if sort_dir == "Ascending" else False)

                        with st.expander("Add filter (optional)"):
                            min_val = col_info.get('min', 0)
                            max_val = col_info.get('max', 100)
                            filter_min, filter_max = st.slider(
                                f"Filter range for {criterion}",
                                min_value=float(min_val),
                                max_value=float(max_val),
                                value=(float(min_val), float(max_val)),
                                step=(max_val - min_val) / 100 if max_val > min_val else 0.1,
                                key=f"slider_{criterion}"
                            )
                            if filter_min > min_val or filter_max < max_val:
                                st.session_state['filter_conditions'][criterion] = {
                                    'type': 'numeric',
                                    'min': filter_min,
                                    'max': filter_max
                                }
                            else:
                                st.session_state['filter_conditions'].pop(criterion, None)

                    elif col_type in ['categorical', 'boolean']:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            sort_dir = st.radio(
                                f"Sort direction for {criterion}",
                                ["Ascending", "Descending"],
                                key=f"sort_{criterion}",
                                horizontal=True
                            )
                            sort_directions.append(True if sort_dir == "Ascending" else False)

                        with st.expander("Add filter (optional)"):
                            unique_values = col_info.get('unique_values', [])
                            is_truncated = col_info.get('truncated', False)
                            selected_values = st.multiselect(
                                f"Select values to include for {criterion}" + (" (showing first 30 only)" if is_truncated else ""),
                                options=unique_values,
                                default=unique_values,
                                key=f"filter_{criterion}"
                            )
                            if len(selected_values) < len(unique_values):
                                st.session_state['filter_conditions'][criterion] = {
                                    'type': col_type,
                                    'values': selected_values
                                }
                            else:
                                st.session_state['filter_conditions'].pop(criterion, None)

                    else:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            sort_dir = st.radio(
                                f"Sort direction for {criterion}",
                                ["Ascending", "Descending"],
                                key=f"sort_{criterion}",
                                horizontal=True
                            )
                            sort_directions.append(True if sort_dir == "Ascending" else False)

                        with st.expander("Add filter (optional)"):
                            search_text = st.text_input(
                                f"Search text in {criterion}",
                                key=f"search_{criterion}"
                            )
                            if search_text:
                                st.session_state['filter_conditions'][criterion] = {
                                    'type': 'text',
                                    'search': search_text
                                }
                            else:
                                st.session_state['filter_conditions'].pop(criterion, None)

                    st.markdown("</div>", unsafe_allow_html=True)

            selected_criteria = criteria_options

    elif st.session_state['has_label']:
        st.info("Using the supervised model to predict and rank suppliers based on their probability of being a good supplier (Label = 1).")

    if st.session_state['filter_conditions']:
        st.markdown("<h2 class='sub-header'>Active Filters</h2>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        for col, filter_info in st.session_state['filter_conditions'].items():
            filter_type = filter_info.get('type')
            if filter_type == 'numeric':
                st.markdown(f"• {col}: Between {filter_info.get('min')} and {filter_info.get('max')}")
            elif filter_type in ['categorical', 'boolean']:
                st.markdown(f"• {col}: {', '.join(str(v) for v in filter_info.get('values', []))}")
            elif filter_type == 'text':
                st.markdown(f"• {col}: Contains '{filter_info.get('search')}'")
        st.markdown("</div>")
        if st.button("Clear All Filters"):
            st.session_state['filter_conditions'] = {}

    st.markdown("<h2 class='sub-header'>Step 3: Process and Rank Suppliers</h2>", unsafe_allow_html=True)
    if st.button("Process and Rank Suppliers", type="primary"):
        with st.spinner("Processing data and ranking suppliers..."):
            try:
                X, y, feature_names = preprocess_data(st.session_state['data'])
                predictions, prediction_probs, accuracy = train_model(X, y)

                if st.session_state['has_label'] and accuracy is not None:
                    st.metric("Model Accuracy", f"{accuracy * 100:.2f}%")

                ranked_data, error = rank_suppliers(
                    st.session_state['data'],
                    st.session_state['filter_conditions'],
                    predictions,
                    prediction_probs,
                    selected_criteria,
                    sort_directions
                )

                if error:
                    st.error(error)
                else:
                    st.session_state['ranked_data'] = ranked_data
                    st.session_state['chart_fig'] = generate_chart(ranked_data, selected_criteria, top_n=10)
                    st.success("✅ Suppliers ranked successfully!")

            except Exception as e:
                st.error(f"Error during processing: {e}")

    if st.session_state['ranked_data'] is not None:
        st.markdown("<h2 class='sub-header'>Step 4: Results and Report</h2>", unsafe_allow_html=True)
        st.markdown("<p class='info-text'><b>Top Ranked Suppliers:</b></p>", unsafe_allow_html=True)

        if 'Supplier_Score' in st.session_state['ranked_data'].columns and st.session_state['has_label']:
            st.info("The 'Supplier_Score' column represents the probability of the supplier being a good match (Label = 1). Higher scores indicate better suppliers.")

        st.dataframe(st.session_state['ranked_data'].head(10))
        csv_data = st.session_state['ranked_data'].to_csv(index=False)
        st.download_button(
            label="Download Complete Rankings (CSV)",
            data=csv_data,
            file_name="ranked_suppliers.csv",
            mime="text/csv",
        )

        if st.session_state['chart_fig']:
            st.markdown("<p class='info-text'><b>Supplier Comparison Chart:</b></p>", unsafe_allow_html=True)
            st.pyplot(st.session_state['chart_fig'])

        if st.button("Generate AI-Powered Supplier Report"):
            with st.spinner("Generating detailed report..."):
                try:
                    st.session_state['report'] = generate_supplier_report(
                        st.session_state['ranked_data'],
                        selected_criteria if selected_criteria else None,
                        top_n=3
                    )
                except Exception as e:
                    st.error(f"Error generating report: {e}")

        if st.session_state['report']:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='sub-header'>AI Supplier Evaluation Report</p>", unsafe_allow_html=True)
            st.markdown(st.session_state['report'])
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("Generate PDF Report"):
                with st.spinner("Creating PDF report..."):
                    pdf_buffer = create_pdf(
                        st.session_state['report'],
                        selected_criteria if selected_criteria else None,
                        st.session_state['chart_fig']
                    )
                    if pdf_buffer:
                        st.download_button(
                            label="Download PDF Report",
                            data=pdf_buffer,
                            file_name="supplier_evaluation_report.pdf",
                            mime="application/pdf",
                        )

else:
    st.info("👆 Please upload your supplier dataset (CSV) to get started.")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280; font-size: 0.8rem;'>Supplier Evaluation & Ranking System © 2025</p>", unsafe_allow_html=True)