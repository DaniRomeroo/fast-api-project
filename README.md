# 📈 Stock & Social Interest Analysis
Distributed Computing – Project 02 

A web-based data aggregation and analysis platform that combines **financial market data** with **social interest signals** to provide exploratory insights on stock behavior.  
The system integrates multiple public APIs, stores historical data in MongoDB and exposes analytical results through a RESTful API and a role-based web interface.

---
## 🚀 Features

- Integration of **multiple public APIs**:
  - **TwelveData** – historical stock prices
  - **ApeWisdom** – social interest metrics (mentions & votes)
- Asynchronous **ETL pipelines** with logging and history
- **Cross-source analysis** combining financial and social data
- Rule-based analytical summaries (non-predictive)
- **JWT authentication** with role-based access control
- **User dashboard** for stock analysis and visualization
- **Admin dashboard** for user management, ETL execution and monitoring
- Interactive charts using **Chart.js**

---
## 🏗️ System Architecture (Overview)

**Frontend**
- HTML, CSS (TailwindCSS), JavaScript
- Role-based views (User / Admin)
- Chart.js for data visualization

**Backend**
- FastAPI
- JWT authentication (OAuth2 Bearer)
- Modular architecture:
  - Authentication
  - ETL & ingestion
  - Analysis logic
  - API layer

**Database**
- MongoDB Atlas

**External APIs**
- TwelveData
- ApeWisdom

---
## ⚙️ Setup Instructions
### 1️⃣ Clone the repository

```bash
git clone <repository_url>
cd <project_folder>
```
### 2️⃣ Clone the repository

```bash
pip install -r requirements.txt
```
### 3️⃣ Configure environment variables
Create a `.env` file in the project root (see template below).
```bash
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>/<database>
DB_NAME=db_name
SECRET_KEY=your_secret_key

TWELVEDATA_KEY=your_twelvedata_api_key
```
### 4️⃣ Run the application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
### 5️⃣ Access the application
Service	URL: http://localhost:8000
