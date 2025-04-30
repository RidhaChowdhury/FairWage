import joblib
import pandas as pd

def predict_salary(company=None, city=None, years_experience=None, job_title=None):
    """
    Predict salary using XGBoost's native categorical handling.
    All parameters are optional - uses median/mode defaults when omitted.
    
    Args:
        company (str, optional): Company name
        city (str, optional): City
        years_experience (float, optional): Years of experience
        job_title (str, optional): Job title
    
    Returns:
        tuple: (predicted_salary, used_defaults_dict)
    """
    # Load model artifacts
    try:
        artifacts = joblib.load('salary_predictor.pkl')
        model = artifacts['model']
        categorical_columns = artifacts['categorical_columns']
        feature_order = artifacts['feature_order']
        categories = artifacts['categories']
    except FileNotFoundError:
        raise FileNotFoundError("Model files not found. Please train the model first.")

    # Prepare input with defaults
    input_data = {
        'Company': [company] if company is not None else [categories['Company'][0]],
        'City': [city] if city is not None else [categories['City'][0]],
        'Years of Experience': [years_experience] if years_experience is not None else [artifacts.get('median_experience', 3.0)],
        'Job Title': [job_title] if job_title is not None else [categories['Job Title'][0]]
    }
    
    # Track which defaults were used
    used_defaults = {
        'company': company is None,
        'city': city is None,
        'years_experience': years_experience is None,
        'job_title': job_title is None
    }

    # Create DataFrame with correct feature order
    df = pd.DataFrame(input_data, columns=feature_order)
    
    # Convert to categorical
    for col in categorical_columns:
        df[col] = pd.Categorical(
            df[col],
            categories=categories[col]
        )
    
    # Make prediction
    prediction = model.predict(df)
    
    return round(float(prediction[0]), 2), used_defaults

if __name__ == "__main__":
    # Example usage
    salary, defaults = predict_salary(
        company="Salesforce",
        city="San Francisco",
        years_experience=3.5,
        job_title="Software Engineer"
    )
    
    print(f"Predicted salary: ${salary:,.2f}")
    if any(defaults.values()):
        print("Defaults used:", {k:v for k,v in defaults.items() if v})