import os
from flask import Flask, request, jsonify
import joblib
from waitress import serve
from sklearn.preprocessing import OrdinalEncoder
from flask import Flask

# Create a new Flask app
app = Flask(__name__)

# Load the model once when the application starts
model = joblib.load('test.pkl')

# Helper function for loan prediction
def loan_prediction(loan_amnt, term, int_rate, grade, sub_grade, emp_title, emp_length, home_ownership, annual_inc, verification_status,
       purpose, dti, earliest_cr_line, open_acc, pub_rec,
       revol_bal, revol_util, total_acc, initial_list_status,
       application_type, mort_acc, pub_rec_bankruptcies, zip_code):
    """
    Given the customer information and loan information
    predict if the customer will default/loan will be charged off
    """

    # Construct the 2D matrix of values that .predict is expecting
    X = [[loan_amnt, term, int_rate, grade, sub_grade, emp_title, emp_length, home_ownership, annual_inc, 
          verification_status, purpose, dti, earliest_cr_line, open_acc, pub_rec, revol_bal, 
          revol_util, total_acc, initial_list_status, application_type, mort_acc, pub_rec_bankruptcies, zip_code]]

    # Get a list of predictions and select only 1st
    predictions = model.predict(X)
    prediction = int(predictions[0])

    return {"Predicted Loan Status": prediction}

# Defining routes
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
    <p>Feel free to adjust the values of the borrower's information.</p>
    <p>The API will respond with the predicted loan status.</p>
    """

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the request data from the user in JSON format
        request_json = request.get_json()

        # Initialize the OrdinalEncoder
        od = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)

        # Assuming you need to transform certain columns, extract relevant data
        # Example: If 'term', 'grade', and other columns need encoding
        columns_to_encode = ['term', 'grade', 'sub_grade', 'emp_title', 'home_ownership', 'verification_status', 'purpose', 'application_type', 'initial_list_status']
        
        # Extract the columns you need to encode and apply OrdinalEncoder
        data_to_encode = [request_json[column] for column in columns_to_encode if column in request_json]
        encoded_data = od.fit_transform([data_to_encode])  # Transform the extracted data

        # Now replace the original columns with the encoded ones in the request_json
        for i, column in enumerate(columns_to_encode):
            if column in request_json:
                request_json[column] = encoded_data[0][i]  # Replace with encoded value

        # Send the transformed data to the loan_prediction function
        result = loan_prediction(**request_json)

        # Return the result as a JSON response
        return jsonify(result)
    except Exception as e:
        # Return an error message as JSON
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Use waitress to serve the app
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Use waitress to serve the app
    serve(app, host='0.0.0.0', port=port)