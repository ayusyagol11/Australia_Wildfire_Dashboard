
# 🌏 Australia Wildfire Dashboard
Welcome to the **Australia Wildfire Dashboard**! This interactive web application provides insights into historical wildfire data across different regions of Australia. Built with **Dash** and **Plotly**, the dashboard allows users to explore wildfire trends, analyze fire intensity, and visualise key metrics over time.

![Australian Wildfire Dashboard](https://github.com/ayusyagol11/Wildfire_Australia/blob/main/SC/SCR-20250421-iaaz.png)

---

## 🚀 Features

- **Interactive Filters**:
  - Select a **region** (e.g., New South Wales, Queensland).
  - Choose a **year** to analyse wildfire data.
  
- **Visualisations**:
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
**1. Monthly Average Estimated Fire Area (Pie Chart)**
Shows the distribution of fire area by month.
Helps identify months with the largest fire areas.

<img src="https://github.com/ayusyagol11/Wildfire_Australia/blob/main/SC/SCR-20250421-iczt.png" alt="Monthly average estimated fire area" width="600" height="Auto">

**2. Monthly Average Count of Fire Pixels (Bar Chart)**
Displays the frequency of fire pixels by month.
Indicates how often fires occurred in each month.

<img src="https://github.com/ayusyagol11/Wildfire_Australia/blob/main/SC/SCR-20250421-idcc.png" alt="Average Count of Pixels for Presumed Vegetation Fires" width="600" height="Auto">

**3. Mean Fire Brightness Over Time (Line Chart)**
Tracks the average fire brightness over time.
Higher values indicate more intense fires.

<img src="https://github.com/ayusyagol11/Wildfire_Australia/blob/main/SC/SCR-20250421-iddi.png" alt="Mean fire brightness over time" width="600" height="Auto">

**4. Fire Radiative Power vs. Brightness (Scatter Plot)**
Explores the relationship between fire radiative power and brightness.
Larger and darker points represent fires with higher area and count.

<img src="https://github.com/ayusyagol11/Wildfire_Australia/blob/main/SC/SCR-20250421-idem.png" alt="Relationship between fire radiative power and brightness" width="600" height="Auto">

---

## 🛠️ Technologies Used
Python: Core programming language.

- **Dash**: Framework for building interactive web applications.

- **Plotly**: Library for creating interactive visualisations.

- **Pandas**: Data manipulation and analysis.

- **HTML/CSS**: Styling and layout of the dashboard.

---

## 📧 Contact
For questions or feedback, feel free to reach out:
- **Email**: mailto:aayushyagol11@gmail.com
- **GitHub**: [ayusyagol11](https://github.com/ayusyagol11)
- **LinkedIn**: [Aayush Yagol](https://www.linkedin.com/in/aayush-yagol-046874145/)
