import app_1
import app_2
import app_3
import view
import streamlit as st


PAGES = {
    "Board of directors room": app_1,
    "CEO room": app_2,
    "Meeting room": app_3,
    "Logging and tracking":view
}
st.sidebar.title('NAVIGATION')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()