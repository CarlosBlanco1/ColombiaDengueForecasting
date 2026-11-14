from api.services.data_processing_service import process_data_generate_df
from api.services.week_service import compute_date_range, fetch_2m_temp_precip_date_range
from celery_app import app
import pandas as pd

@app.task(bind=True, max_retries=3, default_retry_delay=10)
def fetch_data_process_and_save():

    start_date, end_date = compute_date_range(pd.Timestamp.now())

    fetch_2m_temp_precip_date_range(start_date, end_date)

    df = process_data_generate_df()

