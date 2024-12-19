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

    return render_template('test.html', dropdown_options=dropdown_options)

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

if __name__ == "__main__":
    app.run(debug=True)
