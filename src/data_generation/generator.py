import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

class LoanDataGenerator:
    def __init__(self, num_loans: int = 10000):
        self.num_loans = num_loans
        self.faker = Faker()
        Faker.seed(42)
        np.random.seed(42)
        
    def generate_origination_data(self) -> pd.DataFrame:
        """Generates static origination (application) data for loans."""
        data = []
        for i in range(1, self.num_loans + 1):
            loan_id = f"LI{i:06d}"
            origination_date = self.faker.date_between(start_date='-3y', end_date='-1y')
            origination_month = origination_date.strftime('%Y-%m')
            loan_amount = round(np.random.uniform(5000, 50000), 2)
            
            # Additional realistic risk factors
            credit_score = int(np.random.normal(680, 50))
            credit_score = max(300, min(850, credit_score)) # Bound between 300 and 850
            annual_income = round(np.random.uniform(40000, 150000), 2)
            
            # Simple fraud logic: high loan, low income, low credit score has higher fraud chance
            is_fraud = 1 if (loan_amount > 40000 and annual_income < 50000) or (credit_score < 550 and random.random() > 0.7) else 0

            data.append({
                'LoanId': loan_id,
                'OriginationMonth': origination_month,
                'LoanAmount': loan_amount,
                'City': self.faker.city(),
                'State': self.faker.state_abbr(),
                'JobArea': self.faker.job(),
                'AnnualIncome': annual_income,
                'CreditScore': credit_score,
                'IsFraud': is_fraud
            })
            
        return pd.DataFrame(data)

    def generate_performance_data(self, origination_df: pd.DataFrame) -> pd.DataFrame:
        """Generates monthly performance (time-series) data for each loan."""
        performance_data = []
        
        for _, row in origination_df.iterrows():

            loan_id = row['LoanId']
            loan_amount = row['LoanAmount']
            start_date = datetime.strptime(row['OriginationMonth'], '%Y-%m')
            
            principal_balance = loan_amount
            monthly_payment = loan_amount / 24 # Simplified straight-line amortization
            
            delinquent_flag = 0
            delinquent_days = 0
            
            for month_on_books in range(1, 25): # 24 months maximum
                current_month_date = start_date + relativedelta(months=month_on_books)
                current_month_str = current_month_date.strftime('%Y-%m')
                
                # Prepayment Logic (5% chance of early payoff)
                prepay_flag = 1 if random.random() < 0.05 and principal_balance > 0 else 0
                if prepay_flag:
                    ending_balance = 0.0
                else:
                    ending_balance = max(0.0, principal_balance - monthly_payment)
                
                # Delinquency Logic (Injecting randomness based on previous state)
                if random.random() < 0.10: # 10% chance to miss a payment
                    delinquent_days += 30
                    delinquent_flag = 1
                elif delinquent_days > 0 and random.random() < 0.5: # 50% chance to catch up
                    delinquent_days = 0
                    delinquent_flag = 0
                    
                performance_data.append({
                    'LoanId': loan_id,
                    'PerformanceMonth': current_month_str,
                    'MonthOnBooks': month_on_books,
                    'PrincipalBalance': round(principal_balance, 2),
                    'EndingBalance': round(ending_balance, 2),
                    'DelinquentDays': delinquent_days,
                    'DelinquentFlag': delinquent_flag,
                    'PrepayFlag': prepay_flag
                })
                
                principal_balance = ending_balance
                
                # Stop generating future months if the loan is fully paid off
                if principal_balance == 0:
                    break
                    
        return pd.DataFrame(performance_data)
    

    def generate_and_save(self, raw_data_path: str):
        """Orchestrates generation and saves to CSV."""
        
        print("Generating Origination Data...")
        origination_df = self.generate_origination_data()
        
        print("Generating Performance Data...")
        performance_df = self.generate_performance_data(origination_df)
        
        origination_df.to_csv(f"{raw_data_path}/origination_data.csv", index=False)
        performance_df.to_csv(f"{raw_data_path}/performance_data.csv", index=False)
        print(f"Data successfully saved to {raw_data_path}!")