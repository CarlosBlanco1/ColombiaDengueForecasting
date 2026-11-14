from services.prediction_service import predict_dengue_cases_for_department
from services.week_service import compute_date_range, fetch_2m_temp_precip_date_range
from fastapi import APIRouter, HTTPException
import pandas as pd

valid_department_codes = [
        "05",
        "08",
        "13",
        "15",
        "17",
        "18",
        "19",
        "20",
        "23",
        "25",
        "27",
        "41",
        "44",
        "47",
        "50",
        "52",
        "54",
        "63",
        "66",
        "68",
        "70",
        "73",
        "76",
        "81",
        "85",
        "86",
        "91",
        "94",
        "95",
        "97",
        "99",
    ]

router = APIRouter()

@router.get("/department-prediction/{department_id}")
async def predict_department_cases(department_id: str):

    if department_id not in valid_department_codes:
        raise HTTPException(code=404, detail="no department found for given ID")
    
    num_cases = predict_dengue_cases_for_department(department_id)

    return num_cases