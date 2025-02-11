# 🌏 Australia Wildfire Dashboard
Welcome to the **Australia Wildfire Dashboard**! This interactive web application provides insights into historical wildfire data across different regions of Australia. Built with **Dash** and **Plotly**, the dashboard allows users to explore wildfire trends, analyze fire intensity, and visualize key metrics over time.
<img src="https://github.com/ayusyagol11/Wildfire_Australia/blob/main/SC/SCR-20250212-glvg.png" alt="Dashboard Screenshot" width="800" height="Auto">

---

## 🚀 Features

- **Interactive Filters**:
  - Select a **region** (e.g., New South Wales, Queensland).
  - Choose a **year** to analyze wildfire data.
  
- **Visualizations**:
  - **Pie Chart**: Monthly average estimated fire area.
  - **Bar Chart**: Monthly average count of fire pixels.
  - **Line Chart**: Mean fire brightness over time.
  - **Scatter Plot**: Relationship between fire radiative power and brightness.


- **Insights**:
  - Identify months with the largest fire areas.
  - Track fire intensity and frequency over time.
  - Explore correlations between fire brightness and radiative power.

---

## 📊 Dataset

The dashboard uses the **Historical Wildfires Dataset**, which includes the following key columns:

| Column Name                     | Description                                      |
|---------------------------------|--------------------------------------------------|
| `Region`                        | Australian region where the fire occurred.       |
| `Date`                          | Date of the fire event.                          |
| `Estimated_fire_area`           | Estimated area affected by the fire (in hectares).|
| `Mean_estimated_fire_brightness`| Average brightness of the fire.                  |
| `Mean_estimated_fire_radiative_power` | Average radiative power of the fire.        |
| `Count`                         | Number of fire pixels detected.                  |

---

## 📈 Visualisations
1. Monthly Average Estimated Fire Area (Pie Chart)
Shows the distribution of fire area by month.
Helps identify months with the largest fire areas.
![Monthly average estimated fire area](https://github.com/ayusyagol11/Wildfire_Australia/blob/main/SC/SCR-20250212-gijd.png)

2. Monthly Average Count of Fire Pixels (Bar Chart)
Displays the frequency of fire pixels by month.
Indicates how often fires occurred in each month.
![Average Count of Pixels for Presumed Vegetation Fires](https://github.com/ayusyagol11/Wildfire_Australia/blob/main/SC/SCR-20250212-gild.png)

3. Mean Fire Brightness Over Time (Line Chart)
Tracks the average fire brightness over time.
Higher values indicate more intense fires.
![Mean fire brightness over time](https://github.com/ayusyagol11/Wildfire_Australia/blob/main/SC/SCR-20250212-gimk.png)

4. Fire Radiative Power vs. Brightness (Scatter Plot)
Explores the relationship between fire radiative power and brightness.
Larger and darker points represent fires with higher area and count.
![Relationship between fire radiative power and brightness](https://github.com/ayusyagol11/Wildfire_Australia/blob/main/SC/SCR-20250212-gino.png)

---

## 🛠️ Technologies Used
Python: Core programming language.

- **Dash**: Framework for building interactive web applications.

- **Plotly**: Library for creating interactive visualizations.

- **Pandas**: Data manipulation and analysis.

- **HTML/CSS**: Styling and layout of the dashboard.

---

## 📧 Contact
For questions or feedback, feel free to reach out:
**Email: mailto:aayushyagol11@gmail.com
GitHub: [ayusyagol11](https://github.com/ayusyagol11)
LinkedIn: [Aayush Yagol](https://www.linkedin.com/in/aayush-yagol-046874145/)
