import streamlit as st
from dashboard import show_dashboard
from profound_insights import show_profound_insights
from fundamental_insights import show_fundamental_insights
from add_log import show_add_log

st.set_page_config(
    page_title="SecureCheck",
    page_icon="https://i.postimg.cc/G2tPstTQ/SCK-Thumb.png",
    layout="wide"
)

# Sidebar Logo
st.sidebar.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="https://i.postimg.cc/59Yb7j9h/SCK-Icon1.png" width="190" height="120">
    </div>
    """,
    unsafe_allow_html=True
)

selected_page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "💡 Fundamental Insights", "🧠 Profound Insights", "📝 Add New Police Log"]
)

# Routing Logic
if selected_page == "🏠 Home":
    show_dashboard()
elif selected_page == "💡 Fundamental Insights":
    show_fundamental_insights()
elif selected_page == "🧠 Profound Insights":
    show_profound_insights()
elif selected_page == "📝 Add New Police Log":
    show_add_log()
