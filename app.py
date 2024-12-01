# Flask is the overall web framework
from flask import Flask, request
# joblib is used to unpickle the model
import joblib
# json is used to prepare the result
import json

# create new flask app here
app = Flask(__name__)

# helper function here

def loan_prediction(loan_amnt, term, int_rate, grade, sub_grade, emp_title, emp_length,
                    home_ownership, annual_inc, verification_status,purpose, dti, 
                    earliest_cr_line, open_acc, pub_rec, revol_bal, revol_util, total_acc, 
                    initial_list_status, application_type, mort_acc, pub_rec_bankruptcies, zip_code):
    """
    Given the customer information and loan information
    predict if the customer will default/loan will be charged off
    """

    # Load the model from the file
    with open("model.pkl", "rb") as f:
        model = joblib.load(f)

    # Construct the 2D matrix of values that .predict is expecting
    X = [[loan_amnt, term, int_rate, grade, sub_grade, emp_title, emp_length, home_ownership, annual_inc, 
          verification_status, purpose, dti, earliest_cr_line, open_acc, pub_rec,revol_bal, 
          revol_util, total_acc, initial_list_status,application_type, mort_acc,pub_rec_bankruptcies, zip_code]]

    # Get a list of predictions and select only 1st
    predictions = model.predict(X)
    prediction = int(predictions[0])

    return {"Predicted Loan Status": prediction}


# defining routes here
@app.route('/', methods=['GET'])
def index():
    return """
    <h1>API Documentation</h1>
    <p>Welcome to the Loan Status Prediction API!</p>
    <p>To make a prediction, send a POST request to the <code>/predict</code> endpoint with the following JSON structure:</p>
    <pre>
    {
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
    </pre>
    <p> Feel free to adjust the values of the borrowers information.<p>
    <p>The API will respond with the predicted loan status where 1 is default and 0 non-default</p>
    """


@app.route('/predict', methods=['POST'])
def predict():
    # Get the request data from the user in JSON format
    request_json = request.get_json()

    # We are expecting the request to look like this:
    # Send it to our prediction function using ** to unpack the arguments
    result = loan_prediction(**request_json)

    # Return the result as a string with JSON format
    return json.dumps(result)