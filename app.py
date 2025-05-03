import streamlit as st
from predict import predict_salary

# Set page configuration for full width and reduced padding
st.set_page_config(layout="wide", page_title="Fair Wage Predictor")

# Custom CSS to reduce padding
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            padding-left: 4rem;
            padding-right: 4rem;
        }
        [data-testid="stSidebar"] {
            display: none;
        }
        .st-emotion-cache-1y4p8pa {
            width: 100%;
            padding: 1rem 1rem 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

st.title('CMPSC 497 - Capitalism 2 Final Project')
st.subheader('Fair Wage Predictor for Software Engineering Jobs in the US')

# Create two columns with adjusted spacing
col1, col2 = st.columns([2, 3], gap="medium")

# --- Left Column: Overview ---
with col1:
    # st.header("🌟 Key Points")
    st.write(
        'This is a web application that predicts the fair wage for Software Engineering jobs in the US '
        'based on various factors such as years of experience, location, job title, and company. '
        'The model is trained on a dataset of salaries from Glassdoor data for Software Engineers from Salesforce, Uber, Stripe, and Atlassian, '
        'across cities San Francisco, Seattle, Chicago, and New York. '
    )

    st.write(
        'Fill out the form to the right to get a prediction of your fair wage! '
    )

    st.markdown("""
    **Predict fair salaries using:**
    - 🎯 Years of experience
    - 📍 Location (SF, NYC, Chicago, Seattle)
    - 🏢 Company (Salesforce, Uber, Stripe, Atlassian)
    - 💼 Job title *(only software engineer for now)*
    """) 
    
    
    st.info("""
    💡 **Tip:** For best results:
    - Use exact job titles
    - Use base salary (not total comp)
    - Select nearest major city
    """)

    st.warning("""
    **Please note:**
    - Prototype system (expect error)
    - Limited to US software engineering jobs
    - Anonymous data (Glassdoor)
    - Updated Apr 2025
    """)

# --- Right Column: Form ---
with col2:
    with st.form(key='salary_form'):
        years_exp = st.number_input('Years of Experience', min_value=0, step=1)
        location = st.selectbox('Location', ['San Francisco', 'Seattle', 'Chicago', 'New York'])
        job_title = st.selectbox('Job Title', ['Software Engineer'])  # Can add more titles later
        company = st.selectbox('Company', ['Salesforce', 'Uber', 'Stripe', 'Atlassian'])
        current_salary = st.text_input('Current Salary (USD) (optional)', placeholder="Leave blank if not applicable")
        submit = st.form_submit_button(label='Submit')

    # --- Handle Submission ---
    if submit:
        # Validate current_salary if it's not empty
        if current_salary.strip():
            try:
                current_salary_value = float(current_salary)
            except ValueError:
                st.error("Please enter a valid number for current salary, or leave it blank.")
                st.stop()
        else:
            current_salary_value = None

        # Make the prediction
        try:
            predicted_salary, defaults = predict_salary(
                company=company,
                city=location,
                years_experience=years_exp,
                job_title=job_title
            )

            st.success("Prediction successful!")
            # --- Salary Fairness Check ---
            if current_salary_value is not None:
                diff = current_salary_value - predicted_salary
                percent_diff = (diff / predicted_salary) * 100

                if abs(percent_diff) <= 10:
                    st.markdown("### ✅ **Your salary is within a fair range of the predicted value.**")
                elif percent_diff > 10:
                    st.markdown(f"### 📈 **Your salary of ${current_salary_value:,.2f} is above the predicted fair wage. Congrats!**")
                else:
                    st.markdown(f"### 📉 **Your salary of ${current_salary_value:,.2f} is below the predicted fair wage. You may want to negotiate or investigate further.**")

            st.markdown(f"### 🎯 Predicted Fair Salary: **${predicted_salary:,.2f}**")

        except Exception as e:
            st.error(f"Prediction failed: {e}")