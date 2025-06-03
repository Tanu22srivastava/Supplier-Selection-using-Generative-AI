import streamlit as st
def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 class='sub-header'>Settings</h2>", unsafe_allow_html=True)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<h3 class='sub-header'>About</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p class='info-text'>This tool helps you:</p>
        <ul class='info-text'>
            <li>Analyze supplier data</li>
            <li>Rank suppliers based on your criteria</li>
            <li>Generate AI-powered reports</li>
            <li>Export results and visualizations</li>
        </ul>
        """, unsafe_allow_html=True)