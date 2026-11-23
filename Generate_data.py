import csv
from datetime import datetime, timedelta
import os
import random
from faker import Faker

fake = Faker()

# Project Configuration
TOTAL_DAYS_TO_SIMULATE = 5
CLAIMS_PER_DAY = 500
OUTPUT_DIR = "../daily_claims_exports"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Master Setup
PLANS = ["Bronze_HighDeductible", "Silver_PPO", "Gold_HMO", "Platinum_POS"]
PROVIDERS = ["Apex Care Clinic", "St. Jude General Hospital", "Metro Health Medical Center", "Trinity Health Memorial",
             "Pinecrest Community Hospital"]
DIAGNOSIS_CODES = ["J45.909", "E11.9", "I10", "M25.56", "Z00.00", "R07.9"]
PROCEDURES = {"99283": 1200.00, "36415": 45.00, "99213": 150.00, "27447": 22000.00, "74177": 1800.00}


def generate_daily_batch(target_date):
    """Generates a list of claims simulating transactions for a specific day."""
    batch_data = []

    for _ in range(CLAIMS_PER_DAY):
        # Service date matches the transactional target run date
        date_of_service = target_date
        # Submission date runs a few days late (or way past SLA windows)
        submitted_date = date_of_service + timedelta(days=random.choice([2, 5, 12, 105]))

        proc_code = random.choice(list(PROCEDURES.keys()))
        base_cost = PROCEDURES[proc_code]
        # Introduce pricing variance/gouging rules
        billed_amount = round(base_cost * random.choice([1.0, 1.05, 0.95, 4.5]), 2)

        batch_data.append({
            "CLAIM_ID": f"{random.choice(['E', '8', '7', '0'])}{fake.hexify(text='^^^^^^^-^^^^')}".upper(),
            "PATIENT_ID": f"PT{random.randint(100000, 999999)}",
            "POLICY_NUMBER": f"POL{random.randint(10000000, 99999999)}",
            "INSURANCE_PLAN": random.choice(PLANS),
            "PROVIDER_NAME": random.choice(PROVIDERS),
            "DIAGNOSIS_CODE": random.choice(DIAGNOSIS_CODES),
            "PROCEDURE_CODE": proc_code,
            "CHARGE_AMOUNT": billed_amount,
            "DATE_OF_SERVICE": date_of_service.strftime("%Y-%m-%d"),
            "SUBMITTED_DATE": submitted_date.strftime("%Y-%m-%d")
        })

    return batch_data


def main():
    # Set a baseline timeline start window (mimicking late Oct 2026)
    base_date = datetime(2026, 10, 21)

    print(f"🚀 Starting simulation to generate {TOTAL_DAYS_TO_SIMULATE} distinct sequential daily files...")

    for day in range(TOTAL_DAYS_TO_SIMULATE):
        current_run_date = base_date + timedelta(days=day)
        date_str = current_run_date.strftime("%Y%m%d")
        filename = os.path.join(OUTPUT_DIR, f"raw_claims_{date_str}.csv")

        # Generate transactions for this specific day
        daily_records = generate_daily_batch(current_run_date)

        # Write out to daily files
        fieldnames = ["CLAIM_ID", "PATIENT_ID", "POLICY_NUMBER", "INSURANCE_PLAN", "PROVIDER_NAME", "DIAGNOSIS_CODE",
                      "PROCEDURE_CODE", "CHARGE_AMOUNT", "DATE_OF_SERVICE", "SUBMITTED_DATE"]
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(daily_records)

        print(f"💾 Created: {filename} ({len(daily_records)} transactions written)")

    print(f"\n🎉 Success! Check the '{OUTPUT_DIR}' directory in your PyCharm sidebar.")


if __name__ == "__main__":
    main()
