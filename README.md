# Camera Health Check Repair Dashboard

This is a Streamlit dashboard for managing camera health check and repair data.

## Features
- Admin and viewer login roles
- Add, edit, delete camera records (Admin only)
- Import Excel files to append records
- Filter and search camera data
- Black & orange themed UI
- Uses `repairs.csv` as backend

## Installation
1. Clone the repository:
```
git clone https://github.com/YOUR_USERNAME/camera-repair-dashboard.git
cd camera-repair-dashboard
```
2. Install requirements:
```
pip install -r requirements.txt
```
3. Run the app:
```
streamlit run app.py
```

## Default Login Credentials
- Admin: admin / admin123
- Viewer: viewer / viewer123

> Update credentials in `app.py` if needed.
