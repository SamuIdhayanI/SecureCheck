import streamlit as st
import plotly.express as px
from db_utils import fetch_data

def show_fundamental_insights():
    st.title("💡 Fundamental Insights")

    # Define categories and questions
    category_map = {
        "🚗 Vehicle-Based": [
            "What are the top 10 vehicles involved in drug-related stops?",
            "Which vehicles were most frequently searched?"
        ],
        "🧍 Demographic-Based": [
            "Which driver age group had the highest arrest rate?",
            "What is the gender distribution of drivers stopped in each country?",
            "Which race and gender combination has the highest search rate?"
        ],
        "🕒 Time & Duration Based": [
        "What time of day sees the most traffic stops?",
        "What is the average stop duration for different violations?",
        "Are stops during the night more likely to lead to arrests?"
        ],
        "⚖️ Violation-Based": [
            "Which violations are most associated with searches or arrests?",
            "Which violations are most common among younger drivers (<25)?",
            "Is there a violation that rarely results in search or arrest?"
        ],
        "🌍 Location-Based": [
            "Which countries report the highest rate of drug-related stops?",
            "What is the arrest rate by country and violation?",
            "Which country has the most stops with search conducted?"
        ]
    }

    # Define queries
    query_map = {
        "What are the top 10 vehicles involved in drug-related stops?":
            """
            SELECT vehicle_number, COUNT(*) AS stop_count
            FROM traffic_stops
            WHERE drugs_related_stop = 1 AND vehicle_number IS NOT NULL AND vehicle_number != ''
            GROUP BY vehicle_number
            ORDER BY stop_count DESC
            LIMIT 10
            """,

        "Which vehicles were most frequently searched?":
            """
            SELECT vehicle_number, COUNT(*) AS search_count
            FROM traffic_stops
            WHERE search_conducted = 1 AND vehicle_number IS NOT NULL AND vehicle_number != ''
            GROUP BY vehicle_number
            ORDER BY search_count DESC
            LIMIT 10
            """,

        "Which driver age group had the highest arrest rate?":
            """
            SELECT 
                CASE 
                    WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN driver_age BETWEEN 36 AND 45 THEN '36-45'
                    WHEN driver_age BETWEEN 46 AND 60 THEN '46-60'
                    ELSE '60+' 
                END AS age_group,
                ROUND(SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate
            FROM traffic_stops
            WHERE driver_age IS NOT NULL
            GROUP BY age_group
            ORDER BY arrest_rate DESC
            """,

        "What is the gender distribution of drivers stopped in each country?":
            """
            SELECT country_name, driver_gender, COUNT(*) AS count
            FROM traffic_stops
            GROUP BY country_name, driver_gender
            ORDER BY country_name, driver_gender
            """,

        "Which race and gender combination has the highest search rate?":
            """
            SELECT driver_race, driver_gender,
                   ROUND(SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS search_rate
            FROM traffic_stops
            GROUP BY driver_race, driver_gender
            ORDER BY search_rate DESC
            LIMIT 5
            """,
        "What time of day sees the most traffic stops?": """
            SELECT 
                CASE 
                    WHEN CAST(LEFT(stop_time, 2) AS UNSIGNED) BETWEEN 6 AND 11 THEN 'Morning'
                    WHEN CAST(LEFT(stop_time, 2) AS UNSIGNED) BETWEEN 12 AND 17 THEN 'Afternoon'
                    WHEN CAST(LEFT(stop_time, 2) AS UNSIGNED) BETWEEN 18 AND 21 THEN 'Evening'
                    ELSE 'Night'
                END AS time_of_day,
                COUNT(*) AS stop_count
            FROM traffic_stops
            GROUP BY time_of_day
            ORDER BY stop_count DESC
        """,

        "What is the average stop duration for different violations?": """
            SELECT violation,
                ROUND(AVG(
                    CASE stop_duration
                        WHEN '0-15 Min' THEN 7.5
                        WHEN '16-30 Min' THEN 23
                        WHEN '30+ Min' THEN 40
                    END
                ), 2) AS avg_duration_min
            FROM traffic_stops
            GROUP BY violation
            ORDER BY avg_duration_min DESC
        """,

        "Are stops during the night more likely to lead to arrests?": """
            SELECT time_segment,
                ROUND(SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate
            FROM (
                SELECT *,
                    CASE 
                        WHEN CAST(LEFT(stop_time, 2) AS UNSIGNED) BETWEEN 22 AND 23 
                                OR CAST(LEFT(stop_time, 2) AS UNSIGNED) BETWEEN 0 AND 5 THEN 'Night'
                        ELSE 'Day'
                    END AS time_segment
                FROM traffic_stops
            ) AS sub
            GROUP BY time_segment
        """,

        "Which violations are most associated with searches or arrests?": """
            SELECT violation,
                ROUND(SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS search_rate,
                ROUND(SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate
            FROM traffic_stops
            GROUP BY violation
            ORDER BY search_rate DESC
        """,

        "Which violations are most common among younger drivers (<25)?": """
            SELECT violation, COUNT(*) AS count
            FROM traffic_stops
            WHERE driver_age < 25
            GROUP BY violation
            ORDER BY count DESC
        """,

        "Is there a violation that rarely results in search or arrest?": """
            SELECT violation,
                ROUND(SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS search_rate,
                ROUND(SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate
            FROM traffic_stops
            GROUP BY violation
            HAVING search_rate < 50 AND arrest_rate < 50
            ORDER BY violation
        """,

        "Which countries report the highest rate of drug-related stops?": """
            SELECT country_name,
                ROUND(SUM(CASE WHEN drugs_related_stop = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS drug_stop_rate
            FROM traffic_stops
            GROUP BY country_name
            ORDER BY drug_stop_rate DESC
        """,

        "What is the arrest rate by country and violation?": """
            SELECT country_name, violation,
                ROUND(SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS arrest_rate
            FROM traffic_stops
            GROUP BY country_name, violation
            ORDER BY country_name, arrest_rate DESC
        """,

        "Which country has the most stops with search conducted?": """
            SELECT country_name, COUNT(*) AS search_count
            FROM traffic_stops
            WHERE search_conducted = 1
            GROUP BY country_name
            ORDER BY search_count DESC
        """

    }

    # UI - Category and question selection
    category = st.selectbox("Select Category", list(category_map.keys()))
    selected_question = st.selectbox("Select a Question", category_map[category])

    # Run query on button click
    if st.button("Run Query"):
        query = query_map[selected_question]
        result = fetch_data(query)

        if result.empty:
            st.warning("No results found.")
            return

        # Display result table
        if selected_question in [
            "What are the top 10 vehicles involved in drug-related stops?",
            "Which vehicles were most frequently searched?"
        ]:
            st.subheader("📊 Query Output")
            st.dataframe(result[['vehicle_number']])
        else:
            st.subheader("📊 Query Output")
            st.dataframe(result)

        st.markdown("---")
        st.subheader("📈 Visualization")
        if selected_question == "What are the top 10 vehicles involved in drug-related stops?":
            fig = px.bar(result, x='vehicle_number', y='stop_count',
                         title='Top 10 Vehicles in Drug-Related Stops',
                         labels={'vehicle_number': 'Vehicle', 'stop_count': 'Number of Stops'})
            fig.update_layout(xaxis_title="Vehicle", yaxis_title="Stops")
            st.plotly_chart(fig)

        elif selected_question == "Which vehicles were most frequently searched?":
            fig = px.bar(result, x='vehicle_number', y='search_count',
                         title='Most Frequently Searched Vehicles',
                         labels={'vehicle_number': 'Vehicle', 'search_count': 'Search Count'})
            fig.update_layout(xaxis_title="Vehicle", yaxis_title="Searches")
            st.plotly_chart(fig)

        elif selected_question == "Which driver age group had the highest arrest rate?":
            fig = px.bar(result, x='age_group', y='arrest_rate',
                         title='Arrest Rate by Driver Age Group',
                         labels={'age_group': 'Age Group', 'arrest_rate': 'Arrest Rate (%)'})
            fig.update_layout(yaxis_range=[45, 55])
            st.plotly_chart(fig)

        elif selected_question == "What is the gender distribution of drivers stopped in each country?":
            fig = px.bar(result, x='country_name', y='count', color='driver_gender',
                         barmode='group', title='Gender Distribution of Drivers by Country',
                         labels={'country_name': 'Country', 'count': 'Count'})
            fig.update_layout(yaxis_range=[10000, 12000])
            st.plotly_chart(fig)

        elif selected_question == "Which race and gender combination has the highest search rate?":
            fig = px.bar(result, x='driver_race', y='search_rate', color='driver_gender',
                         title='Top Race-Gender Combinations by Search Rate',
                         labels={'driver_race': 'Race', 'search_rate': 'Search Rate (%)'})
            fig.update_layout(yaxis_range=[45, 55])
            st.plotly_chart(fig)
        
        elif selected_question == "What time of day sees the most traffic stops?":
            fig = px.pie(result, names='time_of_day', values='stop_count',
                        title='Traffic Stops by Time of Day',
                        hole=0.4)
            st.plotly_chart(fig)

        elif selected_question == "What is the average stop duration for different violations?":
            fig = px.bar(result, x='violation', y='avg_duration_min',
                         title='Average Stop Duration by Violation',
                         labels={'violation': 'Violation', 'avg_duration_min': 'Avg Duration (min)'})
            fig.update_layout(yaxis_range=[23, 24])
            st.plotly_chart(fig)

        elif selected_question == "Are stops during the night more likely to lead to arrests?":
            fig = px.pie(result, names='time_segment', values='arrest_rate',
                        title='Arrest Rate: Night vs Day',
                        hole=0.4)
            st.plotly_chart(fig)
        
        elif selected_question == "Which violations are most associated with searches or arrests?":
            melted = result.melt(id_vars='violation', value_vars=['search_rate', 'arrest_rate'],
                                var_name='Metric', value_name='Rate')
            fig = px.bar(melted, x='violation', y='Rate', color='Metric', barmode='group',
                        title='Search and Arrest Rates by Violation',
                        labels={'violation': 'Violation', 'Rate': 'Rate (%)'})
            fig.update_layout(yaxis_range=[48, 51])
            st.plotly_chart(fig)

        elif selected_question == "Which violations are most common among younger drivers (<25)?":
            fig = px.pie(result, names='violation', values='count',
                        title='Violations Among Drivers Under 25',
                        hole=0.4)
            st.plotly_chart(fig)

        elif selected_question == "Which countries report the highest rate of drug-related stops?":
            fig = px.bar(result, x='country_name', y='drug_stop_rate',
                         title='Drug-Related Stop Rate by Country',
                         labels={'country_name': 'Country', 'drug_stop_rate': 'Rate (%)'})
            fig.update_layout(yaxis_range=[49, 51])
            st.plotly_chart(fig)

        elif selected_question == "What is the arrest rate by country and violation?":
            fig = px.bar(result, x='violation', y='arrest_rate',
                         color='country_name', barmode='group',
                         title='Arrest Rate by Country and Violation',
                         labels={'violation': 'Violation', 'arrest_rate': 'Arrest Rate (%)'})
            fig.update_layout(yaxis_range=[49, 51])
            st.plotly_chart(fig)

        elif selected_question == "Which country has the most stops with search conducted?":
            fig = px.pie(result, names='country_name', values='search_count',
                        title='Search-Conducted Stops by Country',
                        hole=0.4)
            st.plotly_chart(fig)
