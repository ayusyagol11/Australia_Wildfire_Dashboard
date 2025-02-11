# 🌏 Australia Wildfire Dashboard

![Dashboard Screenshot](https://via.placeholder.com/800x400) *(Replace with an actual screenshot of your dashboard)*

Welcome to the **Australia Wildfire Dashboard**! This interactive web application provides insights into historical wildfire data across different regions of Australia. Built with **Dash** and **Plotly**, the dashboard allows users to explore wildfire trends, analyze fire intensity, and visualize key metrics over time.

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

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/australia-wildfire-dashboard.git
   cd australia-wildfire-dashboard
