import streamlit as st
from db_utils import fetch_data

def show_dashboard():
    # Inject custom CSS and Font Awesome
    st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        .about-card {
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            padding: 25px;
            background-color: #ffffff;
            margin-bottom: 30px;
        }
        .about-card h3 {
            margin-top: 0;
            color: #1f4e79;
        }
        .about-card p {
            font-size: 16px;
            line-height: 1.6;
            color: #333;
            margin-bottom: 0;
        }

        .metrics-bg {
            background-image: url('https://i.postimg.cc/tCR98MPX/metrices-bg.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 12px;
            padding: 40px 30px;
            margin-bottom: 40px;
            color: white;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            text-align: center;
        }

        @media (max-width: 768px) {
            .metrics-grid {
                grid-template-columns: 1fr;
            }
        }

        .metric-box {
            background-color: rgba(0, 0, 0, 0.5);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }

        .metric-icon {
            font-size: 36px;
            margin-bottom: 10px;
            color: white;
        }

        .metric-label {
            font-size: 18px;
            font-weight: bold;
        }

        .metric-value {
            font-size: 28px;
            font-weight: bold;
            margin-top: 10px;
            color: #ffd700;
        }
    </style>
    """, unsafe_allow_html=True)


    st.title("SecureCheck: Digital Police Check Post Registry")

    # About Card
    st.markdown("""
        <div class="about-card">
            <h3>📣 About SecureCheck</h3>
            <p>This project is designed to enhance the efficiency and security of police check posts 
            through a centralized, SQL-based database system. Currently, manual logging and inefficient 
            database management hinder effective vehicle tracking and security operations. Our solution 
            provides real-time logging of vehicles and personnel, enabling swift identification of suspect 
            vehicles through automated SQL queries. A Python-powered dashboard offers real-time insights and alerts, 
            ensuring proactive monitoring of check post activities. With advanced data analytics, the system not only 
            streamlines daily operations but also facilitates crime pattern analysis, improving overall security measures. 
            This centralized database integrates seamlessly across multiple locations, optimizing the performance 
            and coordination of check posts.</p>
        </div>
    """, unsafe_allow_html=True)

    # Fetch data
    query = "SELECT * FROM traffic_stops"
    data = fetch_data(query)

    # Prepare metrics
    total_stops = data.shape[0]
    total_arrests = data[data['stop_outcome'].str.contains("Arrest", case=False, na=False)].shape[0]
    tickets_issued = data[data['stop_outcome'].str.contains("Ticket", case=False, na=False)].shape[0]
    search_conducted = data[data['search_conducted'] == 1].shape[0]

    # Metrics section with icons
    st.markdown(f"""
        <div class="metrics-bg">
            <div class="metrics-grid">
                <div class="metric-box">
                    <div class="metric-icon"><i class="fa-solid fa-car-on"></i></div>
                    <div class="metric-value">{total_stops}</div>
                    <div class="metric-label">Police Stops</div>
                </div>
                <div class="metric-box">
                    <div class="metric-icon"><i class="fa-solid fa-user-shield"></i></div>
                    <div class="metric-value">{search_conducted}</div>
                    <div class="metric-label">Searches Conducted</div>
                </div>
                <div class="metric-box">
                    <div class="metric-icon"><i class="fa-solid fa-handcuffs"></i></div>
                    <div class="metric-value">{total_arrests}</div>
                    <div class="metric-label">Arrests</div>
                </div>
                <div class="metric-box">
                    <div class="metric-icon"><i class="fa-solid fa-ticket"></i></div>
                    <div class="metric-value">{tickets_issued}</div>
                    <div class="metric-label">Tickets Issued</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Data Table
    st.markdown("---")
    st.header("🗂️ Logs Preview")
    if data.empty:
        st.warning("No data available in the table.")
    else:
        st.dataframe(data, use_container_width=True)
