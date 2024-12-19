from flask import Flask, request, render_template, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # Load dropdown options for the form (optional)
        with open("dropdown.pkl", "rb") as f:
            dropdown_options = joblib.load(f)
    except Exception as e:
        dropdown_options = {}
        print(f"Error loading dropdown options: {e}")

    return render_template('home.html', dropdown_options=dropdown_options)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect form data
        form_data = request.get_json()  # Assuming data is sent as JSON via fetch
        feature_names = ['loan_amnt', 'term', 'int_rate', 'grade', 'sub_grade', 'emp_title', 'emp_length',
                         'home_ownership', 'annual_inc', 'verification_status', 'purpose', 'dti',
                         'earliest_cr_line', 'open_acc', 'pub_rec', 'revol_bal', 'revol_util',
                         'total_acc', 'initial_list_status', 'application_type', 'mort_acc',
                         'pub_rec_bankruptcies', 'zip_code']
        
        # Convert form data to DataFrame
        input_data = pd.DataFrame([form_data], columns=feature_names)
        
        # Load the trained model
        with open('model.pkl', 'rb') as f:
            model = joblib.load(f)
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        return jsonify({'prediction': int(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api-documentation', methods=['GET'])
def index():
    return """
    <h1>API Documentation</h1>
    <p>Welcome to the Loan Status Prediction API!</p>
    <p>To make a prediction, send a POST request to the <code>/api</code> endpoint with the following JSON structure:</p>
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
if __name__ == "__main__":
    app.run(debug=True)
