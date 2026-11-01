"""
Loan Portfolio Risk Analysis
Run: python analyze_loans.py
Creates synthetic loan data, risk summaries and charts in outputs/.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def make_loans(n=1500, seed=42):
    rng = np.random.default_rng(seed)
    grades = np.array(["A", "B", "C", "D", "E"])
    purposes = np.array(["Education", "Medical", "Home", "Business", "Personal"])
    grade = rng.choice(grades, n, p=[.18, .28, .27, .17, .10])
    income = rng.normal(650000, 220000, n).clip(120000, 1800000).round()
    amount = rng.integers(30000, 700001, n)
    purpose = rng.choice(purposes, n)
    # Illustrative synthetic probability; not a credit-scoring model.
    grade_risk = pd.Series(grade).map({"A":.04,"B":.07,"C":.12,"D":.20,"E":.30}).to_numpy()
    income_adjustment = np.where(income < 350000, .06, 0)
    amount_adjustment = np.where(amount > 450000, .03, 0)
    probability = np.clip(grade_risk + income_adjustment + amount_adjustment, .01, .75)
    default = rng.binomial(1, probability)
    return pd.DataFrame({
        "loan_id": np.arange(50001, 50001+n),
        "loan_grade": grade,
        "annual_income": income,
        "loan_amount": amount,
        "purpose": purpose,
        "default": default
    })

def main():
    df = make_loans()
    df.to_csv(OUT / "loan_data.csv", index=False)

    overall_rate = df["default"].mean() * 100
    by_grade = (df.groupby("loan_grade", as_index=False)
                  .agg(loan_count=("loan_id", "count"),
                       default_rate=("default", "mean"),
                       average_loan_amount=("loan_amount", "mean")))
    by_grade["default_rate_pct"] = (by_grade.pop("default_rate") * 100).round(2)
    by_purpose = (df.groupby("purpose", as_index=False)
                    .agg(loan_count=("loan_id", "count"),
                         default_rate=("default", "mean")))
    by_purpose["default_rate_pct"] = (by_purpose.pop("default_rate") * 100).round(2)

    by_grade.to_csv(OUT / "risk_by_grade.csv", index=False)
    by_purpose.to_csv(OUT / "risk_by_purpose.csv", index=False)

    print(f"Total loans: {len(df)}")
    print(f"Overall default rate: {overall_rate:.2f}%")
    print("\nRisk by loan grade:\n", by_grade.to_string(index=False))
    print("\nRisk by loan purpose:\n", by_purpose.to_string(index=False))

    plt.figure(figsize=(7, 4))
    plt.bar(by_grade["loan_grade"], by_grade["default_rate_pct"])
    plt.title("Synthetic Default Rate by Loan Grade")
    plt.xlabel("Loan grade"); plt.ylabel("Default rate (%)")
    plt.tight_layout()
    plt.savefig(OUT / "default_rate_by_grade.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 4))
    plt.bar(by_purpose["purpose"], by_purpose["default_rate_pct"])
    plt.title("Synthetic Default Rate by Loan Purpose")
    plt.xlabel("Purpose"); plt.ylabel("Default rate (%)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "default_rate_by_purpose.png", dpi=160)
    plt.close()

if __name__ == "__main__":
    main()
