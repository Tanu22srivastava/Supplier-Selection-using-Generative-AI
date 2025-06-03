import streamlit as st
def render_header():
    st.markdown("<h1 class='main-header'>Supplier Evaluation & Ranking System</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <p class="info-text">
        This application helps you evaluate and rank suppliers based on your chosen criteria or using AI-powered clustering techniques.
        Upload your supplier dataset (CSV) to get started.
        </p>
    </div>
    """, unsafe_allow_html=True)