# config.py

class Config:
    # PostgreSQL database configuration
    DB_CONFIG = {
    'host': 'localhost',
    'database': 'sharepoint',
    'user': 'postgres',
    'password': 'Mkw@naz1',
}

    # Power BI configuration
    POWERBI_CONFIG = {
        'url': 'your_powerbi_report_url',
        'embed_token': 'your_powerbi_embed_token',
    }

    # Streamlit configuration
    STREAMLIT_CONFIG = {
        'host': 'localhost',  # Replace with your Streamlit host
        'port': 5432,         # Replace with your Streamlit port
    }

    # API keys
    API_KEY = 'your_api_key'
    SECRET_KEY = '2b7bJcDuB_VwANuW-oRKjMpzLFN7y51aiESkDITvxvY'