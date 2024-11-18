# Predicting Loan Defaults: Data Analysis, Model Development, and Business Insights
---
![image](image/test.png)

This project aims to develop a predictive model that identifies loan applicants who are likely to default on their loans. By analyzing historical data and applicant profiles, the model will help the lending company assess risk and make informed decisions regarding loan approvals, adjustments, or denials.

## Probelem Statement
---

The problem at hand is to develop a predictive model that can accurately determine the likelihood of loan defaults based on the profiles of loan applicants. The lending company faces two main risks when approving loans: rejecting a creditworthy applicant results in lost business, while approving a high-risk applicant may lead to financial loss. The goal is to analyze historical loan application data to identify patterns and relationships between applicant characteristics (such as income, loan amount, interest rate, and credit history) and the likelihood of default. By building a reliable model, the company can make more informed decisions, such as denying loans, adjusting loan terms, or setting higher interest rates for riskier applicants, ultimately improving its financial performance and reducing defaults.

### Project objectives
- Conduct a thorough exploratory analysis of the loan application data to identify patterns, trends, and correlations between applicant features and loan default risk.
- Select and compare different machine learning models to predict loan defaults.
- Provide actionable recommendations to the Lending Company based on model insights.
- Develop an API to handle request and respond with predicted loan status of the applicant.

### Metrics Of Success

While specific benchmarks can vary by organization and context, a recall rate of 70-80% is often considered acceptable for high-risk applications like loan default prediction. This ensures that the majority of potential defaulters are identified, reducing financial risk.

Therefore for this project we aim to achieve a recall score of above 70% so that we have a model that meets the industry standards.

## Dataset

The dataset comprises historical loan application records of 396,030 borrowers, including various features that describe the applicants' profiles and the outcomes of their loan applications. 

Key features include financial attributes (e.g., annual income, total credit revolving balance, debt-to-income ratio, loan amount), demographic information (e.g., age, employment length, home ownership status), and loan characteristics (e.g., interest rate, loan term, loan purpose). 

The target variable is the loan status, which indicates whether the applicant fully paid the loan, is currently repaying (current), or defaulted (charged-off). 
Additionally, the dataset also contain features such as the month the borrower's earliest reported credit line was opened, the number of open credit lines, and public records indicating past delinquencies.

# Using the API

To make predictions using the API created in this project, please send a HTTP `POST` request  to the `/predict` endpoint with the following JSON structure:

```json
{
        "loan_amnt": 8000,
        "term": '36 months',
        "int_rate": 11.8,
        "grade": 'B',
        "sub_grade":'B5',
        "home_ownership": 'MORTGAGE',
        "annual_inc": 90000,
        "verification_status": 'Not Verified',
        "purpose": 'credit_card',
        "dti": 22.05,
        "earliest_cr_line": 2004,
        "open_acc": 17,
        "pub_rec": 0,
        "revol_bal": 20131,
        "revol_util": 53.01,
        "total_acc": 27,
        "initial_list_status": 'f',
        "application_type': 'INDIVIDUAL',
        "mort_acc": 3,
        "pub_rec_bankruptcies": 0,
        "zip_code": 05113
        
    }
```

```python
import requests
response = requests.post(
    url="https://loan-prediction-api-9f068a1898db.herokuapp.com/predict",
    json={
        "loan_amnt": 8000,
        "term": '36 months',
        "int_rate": 11.8,
        "grade": 'B',
        "sub_grade":'B5',
        "emp_title": 'consultant',
        "emp_length": '3 years',
        "home_ownership": 'MORTGAGE',
        "annual_inc": 90000,
        "verification_status": 'Not Verified',
        "purpose": 'credit_card',
        "dti": 22.05,
        "earliest_cr_line": 2004,
        "open_acc": 17,
        "pub_rec": 0,
        "revol_bal": 20131,
        "revol_util": 53.01,
        "total_acc": 27,
        "initial_list_status": 'f',
        "application_type": 'INDIVIDUAL',
        "mort_acc": 3,
        "pub_rec_bankruptcies": 0,
        "zip_code": '05113'
        
    }
)
response.json()
```