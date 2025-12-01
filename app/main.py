from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoanFeatures(BaseModel):
    loan_amount: float
    days_past_due: int
    score: int

def rule_based_pd(score: int, dpd: int) -> float:
    # trivial baseline logic for day 1 demo
    pd = 0.10 # base PD
    if score >= 700:
        pd -= 0.05
    elif score >= 650:
        pd -= 0.03
    else:
        pd += 0.05

    if dpd > 30:
        pd += 0.10

    return max(0.001, round(pd, 3))

@app.post("/explain/pd")
def explain_pd(features: LoanFeatures):
    pd_val = rule_based_pd(features.score, features.days_past_due)
    explanation = (
        f"Score={features.score} and DPD={features.days_past_due} "
        f"imply PD={pd_val}. If DPD > 30, risk escaltes."
    )

    return {
        "pd_estimates": pd_val,
        "explanation": explanation
    }