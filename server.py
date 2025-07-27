# This code is for demonstration purposes on your local machine.
# You would need to install Flask: pip install Flask
from flask import Flask, request, jsonify
from datetime import datetime
import random
import json

# Assume fill_and_submit_itr_form is defined in a separate module or here for simplicity
# This is a placeholder for the actual tool logic you provided earlier
def fill_and_submit_itr_form_mock(itr_form_type: str, user_data: dict, pan: str) -> dict:
    # Simulate the logic of your tool
    # For a real server, you'd put the actual fill_and_submit_itr_form logic here
    
    errors = []
    warnings = []
    
    # Basic PAN validation
    pan_from_data = user_data.get("personalInfo", {}).get("pan")
    if not pan_from_data or len(pan_from_data) != 10 or not pan_from_data.isalnum():
        errors.append("PAN must be a 10-character alphanumeric string and present in personalInfo.pan.")
    if pan_from_data != pan:
        errors.append("Provided PAN does not match the PAN in user_data.personalInfo.pan.")

    # Simulate success or failure based on some conditions
    # For example, if 'invalid' is in the pan, make it fail
    if "INVALID" in pan.upper():
        errors.append("Simulated error: Invalid PAN detected for demo purposes.")

    # Simulate ITR1 business income error
    total_business_income_44AD = user_data.get("form3CD", {}).get("partAPL", {}).get("persumptiveInc44AD", {}).get("totPersumptiveInc44AD", 0)
    total_business_income_44ADA = user_data.get("form3CD", {}).get("partAPL", {}).get("persumptiveInc44ADA", {}).get("totPersumptiveInc44ADA", 0)
    if itr_form_type == 'ITR1' and (total_business_income_44AD > 0 or total_business_income_44ADA > 0):
        errors.append("ITR1 is not suitable for business income. Consider ITR3 or ITR4.")

    if errors:
        return {
            'acknowledgement_number': None,
            'submission_status': 'failed',
            'submission_date': datetime.now().isoformat(),
            'verification_required': False,
            'errors': errors,
            'warnings': warnings
        }
    else:
        current_year = datetime.now().year
        acknowledgement_suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        acknowledgement_number = f"ITR-V-{current_year}-{acknowledgement_suffix}"
        return {
            'acknowledgement_number': acknowledgement_number,
            'submission_status': 'success',
            'submission_date': datetime.now().isoformat(),
            'verification_required': True,
            'itr_form_type': itr_form_type,
            'pan': pan,
            'gross_total_income': user_data.get("insights", {}).get("cumulativeSalary", {}).get("salary", 0), # Simplified
            'total_tax_paid': 50000, # Simplified
            'errors': [],
            'warnings': ["Simulated warning: Remember to check all fields for accuracy."],
            'next_steps': [
                "Download ITR-V acknowledgement",
                "Complete e-verification within 120 days",
                "Keep all supporting documents for 6 years",
                "Check refund status using acknowledgement number"
            ]
        }

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "e-filing-mock-server"}), 200

@app.route('/file_itr', methods=['POST'])
def file_itr():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request must be JSON"}), 400

    itr_form_type = data.get('itr_form_type')
    user_data = data.get('user_data')
    pan = data.get('pan')

    if not all([itr_form_type, user_data, pan]):
        return jsonify({"error": "Missing required fields: itr_form_type, user_data, pan"}), 400

    try:
        # Call your mock function that simulates the tool's logic
        result = fill_and_submit_itr_form_mock(itr_form_type, user_data, pan)
        if result['submission_status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 400 # Or 200 with status: failed, depending on API design
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

if __name__ == '__main__':
    # Run the server on localhost:5000
    # You can change the port if needed
    app.run(debug=True, port=5000)