import streamlit as st
import pandas as pd
from db_utils import fetch_data

def show_add_log():
    st.title("📝 Add New Police Log")

    # Fetch the traffic stop data
    data = fetch_data("SELECT * FROM traffic_stops")

    # Main form for input
    with st.form("new_log_form"):
        stop_date = st.date_input("Stop Date")
        stop_time = st.time_input("Stop Time")
        county_name = st.text_input("County Name")
        driver_gender = st.selectbox("Driver Gender", ["Male", "Female"])
        driver_age = st.number_input("Driver Age", min_value=16, max_value=100, value=27)
        driver_race = st.text_input("Driver Race")
        search_conducted = st.selectbox("Was a Search Conducted?", ["0", "1"])
        search_type = st.text_input("Search Type")  # Added Search Type input
        drugs_related_stop = st.selectbox("Was it Drug Related?", ["0", "1"])
        stop_duration = st.selectbox("Stop Duration", data['stop_duration'].dropna().unique())
        vehicle_number = st.text_input("Vehicle Number")

        submitted = st.form_submit_button("Submit")

    # Process the prediction after form is submitted
    if submitted:
        # Ensure the data is in the correct format for comparison
        search_conducted_int = int(search_conducted)
        drugs_related_stop_int = int(drugs_related_stop)

        if driver_gender == "Male":
            driver_gender_match = "M"
        elif driver_gender == "Female":
            driver_gender_match = "F"
        
        filtered_data = data[
            (data['driver_gender'].str.lower() == driver_gender_match.lower()) &
            (data['driver_age'] == driver_age) &
            (data['search_conducted'] == search_conducted_int) &
            (data['stop_duration'].str.lower() == stop_duration.lower()) &
            (data['drugs_related_stop'] == drugs_related_stop_int)
        ]
        
        # Use mode of matching data
        if not filtered_data.empty:
            predicted_outcome = filtered_data['stop_outcome'].mode()[0]
            predicted_violation = filtered_data['violation'].mode()[0]
        else:
            predicted_outcome = "warning"
            predicted_violation = "speeding"
        
        # Show success message
        try:
            st.toast("✅ Prediction complete. See summary below.", icon="🔍")
        except AttributeError:
            st.success("✅ Prediction complete. See summary below.")
        
        # Display prediction results
        with st.expander("🚔 **View Prediction Summary**", expanded=False):
            st.markdown(f"**Violation:** {predicted_violation}")
            st.markdown(f"**Stop Outcome:** {predicted_outcome}")
            
            summary_1 = (
                f"On {stop_date.strftime('%B %d, %Y')} at {stop_time.strftime('%I:%M %p')}, "
                f"a {driver_age}-year-old {driver_gender} driver was stopped in {county_name}. "
                f"During the stop, {'a search was conducted of type ' + search_type if search_conducted_int and search_type else 'no search was conducted'}. "
                f"The stop {'was drug-related' if drugs_related_stop_int else 'was not drug-related'}."
            )

            summary_2 = (
                f"The stop lasted approximately **{stop_duration.lower()}**. "
                f"The vehicle involved was registered as **{vehicle_number}**."
            )
            st.markdown("---")
            st.markdown("📝 **Log Summary:**")
            st.write(summary_1)
            st.write(summary_2)

