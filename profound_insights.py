import streamlit as st
import pandas as pd
import plotly.express as px
from db_utils import fetch_data

def show_profound_insights():
    st.title("🧠 Profound Insights")

    query_map = {
        "Yearly Breakdown of Stops and Arrests by Country": """
           WITH stop_stats AS (
                SELECT 
                    country_name,
                    EXTRACT(YEAR FROM timestamp) AS year,
                    COUNT(*) AS total_stops,
                    SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests
                FROM traffic_stops
                GROUP BY country_name, EXTRACT(YEAR FROM timestamp)
            )
            SELECT 
                country_name,
                year,
                total_stops,
                total_arrests,
                ROUND(CASE 
                    WHEN total_stops > 0 THEN (total_arrests * 100.0 / total_stops)
                    ELSE 0
                END, 2) AS arrest_rate_percent
            FROM stop_stats
            ORDER BY year, country_name;
        """,

        "Driver Violation Trends Based on Age and Race": """
            SELECT 
                driver_race,
                violation,
                CASE 
                    WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
                    WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
                    ELSE '60+'
                END AS age_group,
                COUNT(*) AS count
            FROM traffic_stops
            GROUP BY driver_race, violation, age_group
            ORDER BY count DESC
        """,

        "Time Period Analysis of Stops (Year, Month, Hour)": """
            SELECT 
                YEAR(timestamp) AS year,
                MONTH(timestamp) AS month,
                HOUR(timestamp) AS hour,
                COUNT(*) AS total_stops
            FROM traffic_stops
            GROUP BY YEAR(timestamp), MONTH(timestamp), HOUR(timestamp)
            ORDER BY year, month, hour
        """,

        "Violations with High Search and Arrest Rates": """
            WITH violation_summary AS (
                SELECT 
                    violation,
                    COUNT(*) AS total,
                    SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) AS searches,
                    SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS arrests
                FROM traffic_stops
                GROUP BY violation
            )
            SELECT 
                violation,
                total,
                searches,
                arrests,
                ROUND((searches * 100.0 / total), 2) AS search_rate_percent,
                ROUND((arrests * 100.0 / total), 2) AS arrest_rate_percent
            FROM violation_summary
            ORDER BY arrest_rate_percent DESC
        """,

        "Driver Demographics by Country (Age, Gender, and Race)": """
            SELECT 
                country_name,
                driver_gender,
                driver_race,
                AVG(driver_age) AS avg_age,
                COUNT(*) AS total_drivers
            FROM traffic_stops
            GROUP BY country_name, driver_gender, driver_race
            ORDER BY country_name, total_drivers DESC
        """,

        "Top 5 Violations with Highest Arrest Rates": """
            WITH violation_stats AS (
                SELECT 
                    violation,
                    COUNT(*) AS total,
                    SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS arrests
                FROM traffic_stops
                GROUP BY violation
            )
            SELECT 
                violation,
                total,
                arrests,
                ROUND((arrests * 100.0 / total), 2) AS arrest_rate_percent
            FROM violation_stats
            ORDER BY arrest_rate_percent DESC
            LIMIT 5
        """
    }

    selected_query = st.selectbox("Select an Insight to Explore", list(query_map.keys()))

    if st.button("Run Query"):
        query = query_map[selected_query]
        result = fetch_data(query)

        if not result.empty:
            st.subheader("📊 Query Output")
            st.dataframe(result)

            st.markdown("---")
            st.subheader("📈 Visualization")

            if selected_query == "Yearly Breakdown of Stops and Arrests by Country":
                fig = px.bar(result, x="year", y="total_stops", color="country_name", barmode="group",
                             title="Total Stops per Year by Country")
                fig.update_layout(yaxis_range=[21000, 22000])
                st.plotly_chart(fig)

                filtered_result = result.dropna(subset=["arrest_rate_percent"])

                if not filtered_result.empty:
                    filtered_result["year"] = filtered_result["year"].astype(str)

                    fig2 = px.bar(
                        filtered_result,
                        x="arrest_rate_percent",
                        y="year",
                        color="country_name",
                        orientation="h",
                        barmode="group",
                        title="Arrest Rate (%) Over Years by Country"
                    )
                    fig2.update_layout(xaxis_range=[48, 51])
                    st.plotly_chart(fig2)


            elif selected_query == "Driver Violation Trends Based on Age and Race":
                fig = px.sunburst(result, path=['driver_race', 'age_group', 'violation'], values='count',
                                  title="Violation Trends by Age and Race", width=800, height=800)
                st.plotly_chart(fig)

            elif selected_query == "Time Period Analysis of Stops (Year, Month, Hour)":
                fig = px.line(result, x="hour", y="total_stops", color="month",
                              title="Stops by Hour of the Day, Colored by Month")
                st.plotly_chart(fig)

            elif selected_query == "Violations with High Search and Arrest Rates":
                fig = px.scatter(result, x="search_rate_percent", y="arrest_rate_percent", size="total",
                                 color="violation", hover_name="violation",
                                 title="Search Rate vs Arrest Rate by Violation")
                st.plotly_chart(fig)

            elif selected_query == "Driver Demographics by Country (Age, Gender, and Race)":
                fig = px.bar(result, x="country_name", y="total_drivers", color="driver_race",
                             facet_col="driver_gender", title="Driver Demographics by Country")
                st.plotly_chart(fig)

            elif selected_query == "Top 5 Violations with Highest Arrest Rates":
                fig = px.bar(result, x="violation", y="arrest_rate_percent", color="violation",
                             title="Top 5 Violations with Highest Arrest Rates")
                fig.update_layout(yaxis_range=[48, 51])
                st.plotly_chart(fig)
        else:
            st.warning("No results found.")
