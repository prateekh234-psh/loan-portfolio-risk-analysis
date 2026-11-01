# Loan Portfolio Risk Analysis

A beginner-friendly Python project exploring patterns in a **synthetic** loan portfolio.

## Questions explored
- What is the overall default rate in the generated sample?
- How does default rate vary across loan grades?
- How does default rate vary by loan purpose?
- How do average loan amounts differ by grade?

## Run
```bash
python -m pip install -r requirements.txt
python analyze_loans.py
```

The script creates `outputs/` containing the synthetic data, summary CSVs and charts.

## Important limitations
- All records are synthetic; no real borrower information is used.
- This is descriptive analysis, not a lending decision or validated credit-risk model.
- The generated relationships are illustrative and must not be interpreted as real-world default probabilities.

