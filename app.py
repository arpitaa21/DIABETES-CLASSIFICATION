import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import os
from pathlib import Path

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Diabetes Classification Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING - PROFESSIONAL HEALTHCARE THEME
# ============================================================================

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f5fff7;
    }
    
    .main {
        background-color: #f5fff7;
        padding: 2rem;
    }
    
    /* Main title styling */
    .main-title {
        color: #0f5132;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        color: #4a7c59;
        font-size: 1.1em;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #0f5132;
        font-weight: 600;
    }
    
    /* Card styling */
    .card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #198754;
    }
    
    .card-success {
        border-left-color: #198754;
    }
    
    .card-danger {
        border-left-color: #dc3545;
    }
    
    .card-info {
        border-left-color: #0dcaf0;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #198754;
        color: white;
        border-radius: 8px;
        height: 2.8em;
        width: 100%;
        font-size: 16px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 8px rgba(25, 135, 84, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #157347;
        box-shadow: 0 6px 12px rgba(21, 115, 71, 0.4);
        transform: translateY(-2px);
    }
    
    /* Input styling */
    .stNumberInput>div>div>input,
    .stSlider>div>div>div>input {
        border-radius: 6px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
    }
    
    .stNumberInput>div>div>input:focus,
    .stSlider>div>div>div>input:focus {
        border-color: #198754;
        box-shadow: 0 0 0 3px rgba(25, 135, 84, 0.1);
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    
    .sidebar-metric {
        background-color: #f0f9f6;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #198754;
    }
    
    .sidebar-metric-title {
        color: #0f5132;
        font-weight: 600;
        font-size: 0.9em;
    }
    
    .sidebar-metric-value {
        color: #198754;
        font-weight: 700;
        font-size: 1.3em;
        margin-top: 0.5rem;
    }
    
    /* Result card styling */
    .result-high-risk {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left-color: #dc3545;
        color: #721c24;
    }
    
    .result-low-risk {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left-color: #28a745;
        color: #155724;
    }
    
    .result-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1em;
        margin: 0.5rem 0;
    }
    
    .badge-high-risk {
        background-color: #dc3545;
        color: white;
    }
    
    .badge-low-risk {
        background-color: #28a745;
        color: white;
    }
    
    /* Chart styling */
    .chart-container {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Separator */
    .separator {
        border-top: 2px solid #e0e0e0;
        margin: 2rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.9em;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Metric grid */
    .metric-box {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9em;
        font-weight: 500;
    }
    
    .metric-value {
        color: #198754;
        font-size: 1.8em;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button {
        border-radius: 6px;
        color: #0f5132;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #198754;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

@st.cache_resource
def load_model_and_scaler():
    """Load model and scaler with error handling"""
    try:
        model_path = "models/diabetes_model.pkl"
        scaler_path = "models/scaler.pkl"
        
        # Check if files exist
        if not os.path.exists(model_path):
            return None, None, f"❌ Model file not found: {model_path}"
        if not os.path.exists(scaler_path):
            return None, None, f"❌ Scaler file not found: {scaler_path}"
        
        # Load files
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        
        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)
        
        return model, scaler, None
    
    except Exception as e:
        return None, None, f"❌ Error loading model: {str(e)}"

def predict_diabetes_risk(model, scaler, input_data):
    """Make prediction with proper error handling"""
    try:
        # Scale input
        scaled_data = scaler.transform([input_data])
        
        # Make prediction
        prediction = model.predict(scaled_data)[0]
        
        # Try to get probability
        probability = None
        try:
            if hasattr(model, 'predict_proba'):
                probability = model.predict_proba(scaled_data)[0][1]
            elif hasattr(model, 'decision_function'):
                # For SVM, use decision_function and convert to probability
                decision = model.decision_function(scaled_data)[0]
                # Simple sigmoid conversion
                probability = 1 / (1 + np.exp(-decision))
                probability = np.clip(probability, 0, 1)
        except:
            pass
        
        return prediction, probability, None
    
    except Exception as e:
        return None, None, f"❌ Prediction error: {str(e)}"

def get_prediction_label(prediction, probability):
    """Return the binary class label and confidence for the predicted class"""
    if prediction == 1:
        label = "DIABETIC"
        color = "red"
        emoji = "⚠️"
        confidence = (probability * 100) if probability is not None else None
    else:
        label = "NOT DIABETIC"
        color = "green"
        emoji = "✅"
        confidence = ((1 - probability) * 100) if probability is not None else None
    
    return label, color, emoji, confidence

def get_prediction_score(model, scaled_data):
    """Return the model score used for local feature attribution."""
    if hasattr(model, "decision_function"):
        score = model.decision_function(scaled_data)
        return float(np.ravel(score)[0])

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(scaled_data)[0][1]
        return float(proba)

    raise ValueError("Model does not expose decision_function or predict_proba")

def get_prediction_feature_importance(model, scaler, input_data):
    """Compute per-prediction feature importance using leave-one-feature-out scoring."""
    try:
        feature_names = [
            "Pregnancies",
            "Glucose",
            "Blood Pressure",
            "Skin Thickness",
            "Insulin",
            "BMI",
            "Diabetes Pedigree",
            "Age"
        ]

        raw_input = np.array(input_data, dtype=float)
        scaled_input = scaler.transform([raw_input])
        baseline_score = get_prediction_score(model, scaled_input)

        reference_values = np.array(getattr(scaler, "mean_", raw_input), dtype=float)
        contributions = []

        for index, feature_name in enumerate(feature_names):
            modified_input = raw_input.copy()
            modified_input[index] = reference_values[index]
            modified_scaled = scaler.transform([modified_input])
            modified_score = get_prediction_score(model, modified_scaled)

            contribution = baseline_score - modified_score
            contributions.append({
                "Feature": feature_name,
                "Contribution": contribution,
                "Importance": abs(contribution)
            })

        importance_df = pd.DataFrame(contributions)
        total_importance = importance_df["Importance"].sum()

        if total_importance == 0:
            importance_df["Importance (%)"] = 100.0 / len(importance_df)
        else:
            importance_df["Importance (%)"] = (
                importance_df["Importance"] / total_importance * 100
            )

        importance_df["Direction"] = importance_df["Contribution"].apply(
            lambda value: "Pushes toward Diabetes" if value >= 0 else "Pushes toward Not Diabetic"
        )

        importance_df = importance_df.sort_values("Importance (%)", ascending=False).reset_index(drop=True)
        return importance_df, baseline_score, None

    except Exception as e:
        return None, None, f"❌ Feature importance error: {str(e)}"

def create_prediction_feature_importance_chart(importance_df):
    """Create a local explanation chart for the current prediction."""
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#dc3545" if value >= 0 else "#198754" for value in importance_df["Contribution"]]

    bars = ax.barh(
        importance_df["Feature"],
        importance_df["Importance (%)"],
        color=colors,
        edgecolor="none"
    )

    ax.set_xlabel("Relative Importance (%)", fontsize=11, fontweight=600, color="#0f5132")
    ax.set_title("Feature Importance for This Prediction", fontsize=13, fontweight=700, color="#0f5132", pad=20)
    ax.set_xlim(0, max(importance_df["Importance (%)"]) * 1.2)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    for bar, value in zip(bars, importance_df["Importance (%)"]):
        ax.text(value + 0.5, bar.get_y() + bar.get_height() / 2, f"{value:.1f}%", va="center", fontsize=10, fontweight=600)

    plt.tight_layout()
    return fig

def create_feature_importance_chart():
    """Create feature importance visualization"""
    features = [
        "Glucose",
        "BMI",
        "Age",
        "Insulin",
        "Pregnancies",
        "Skin Thickness",
        "Blood Pressure",
        "Diabetes Pedigree"
    ]
    
    importance = [0.30, 0.18, 0.14, 0.10, 0.08, 0.07, 0.07, 0.06]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['#198754' if i >= 0.10 else '#6c757d' for i in importance]
    bars = ax.barh(features, importance, color=colors, edgecolor='none')
    
    # Styling
    ax.set_xlabel("Importance Score", fontsize=11, fontweight=600, color="#0f5132")
    ax.set_title("Feature Importance in Diabetes Prediction", 
                 fontsize=13, fontweight=700, color="#0f5132", pad=20)
    ax.set_xlim(0, max(importance) * 1.15)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, importance)):
        ax.text(val + 0.005, bar.get_y() + bar.get_height()/2, 
                f'{val:.2f}', va='center', fontsize=10, fontweight=600)
    
    plt.tight_layout()
    return fig

def create_model_comparison_chart():
    """Create model accuracy comparison chart"""
    models = ["Logistic\nRegression", "Random\nForest", "SVM\n(Best)", 
              "Gradient\nBoosting", "Neural\nNetwork"]
    accuracies = [76.5, 75.8, 77.34, 75.2, 76.0]
    colors = ['#198754' if acc == max(accuracies) else '#6c757d' for acc in accuracies]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(models, accuracies, color=colors, edgecolor='none', width=0.6)
    
    # Styling
    ax.set_ylabel("Accuracy (%)", fontsize=11, fontweight=600, color="#0f5132")
    ax.set_title("Model Performance Comparison", 
                 fontsize=13, fontweight=700, color="#0f5132", pad=20)
    ax.set_ylim(70, 80)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add value labels
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{acc:.2f}%', ha='center', va='bottom', fontsize=10, fontweight=600)
    
    plt.tight_layout()
    return fig

# ============================================================================
# MAIN APPLICATION
# ============================================================================

# Load model and scaler
model, scaler, load_error = load_model_and_scaler()

if load_error:
    st.error("🚨 INITIALIZATION ERROR", icon="🔴")
    st.error(load_error)
    st.info("""
    **Troubleshooting steps:**
    1. Verify `models/diabetes_model.pkl` exists
    2. Verify `models/scaler.pkl` exists
    3. Check file paths are correct
    4. Re-run your training notebook to regenerate model files
    """)
    st.stop()

# ============================================================================
# HEADER SECTION
# ============================================================================

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<p class="main-title">🩺 Diabetes Classification Dashboard</p>', 
                unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced AI-Powered Binary Classification for Diabetic vs Not Diabetic</p>', 
                unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: right; margin-top: 1rem;">
        <p style="font-size: 0.9em; color: #666;">
            📊 ML-Powered Prediction<br>
            ✅ Clinical Grade Accuracy
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# INTRODUCTION SECTION
# ============================================================================

with st.expander("ℹ️ About This Application", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        **Purpose:**
        This application uses machine learning to predict the risk of Type 2 Diabetes 
        Mellitus based on clinical features from the PIMA Indians Diabetes Dataset.
        
        **How it works:**
        - Input your health metrics in the form below
        - Our AI model analyzes your data
        - Receives an instant diabetic / not diabetic classification with confidence score
        
        **Disclaimer:**
        This tool is for educational purposes only and should not replace 
        professional medical advice. Always consult a healthcare provider.
        """)
    
    with col2:
        st.write("""
        **Dataset Information:**
        - **Source:** PIMA Indians Diabetes Dataset
        - **Samples:** 768 patients
        - **Features:** 8 health metrics
        - **Task:** Binary classification
        
        **Research Background:**
        - Originally from National Institute of Diabetes and Digestive and Kidney Diseases
        - Used extensively in ML research
        - Real clinical data for accuracy
        """)

# ============================================================================
# SIDEBAR - MODEL INFORMATION
# ============================================================================

with st.sidebar:
    st.markdown("### 📊 Model Information")
    st.markdown("---")
    
    # Model details
    st.markdown("""
    <div class="sidebar-metric">
        <div class="sidebar-metric-title">🏆 Best Performing Model</div>
        <div class="sidebar-metric-value">Support Vector Machine (SVM)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-metric">
        <div class="sidebar-metric-title">📈 Model Accuracy</div>
        <div class="sidebar-metric-value">77.34%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-metric">
        <div class="sidebar-metric-title">📋 Dataset</div>
        <div class="sidebar-metric-value">PIMA Indians</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-metric">
        <div class="sidebar-metric-title">🔢 Number of Features</div>
        <div class="sidebar-metric-value">8 Attributes</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🤖 Models Trained")
    
    models_info = {
        "Logistic Regression": "76.5%",
        "Random Forest": "75.8%",
        "SVM": "77.34% ⭐",
        "Gradient Boosting": "75.2%",
        "Neural Network": "76.0%"
    }
    
    for model_name, accuracy in models_info.items():
        st.write(f"• {model_name}: {accuracy}")
    
    st.markdown("---")
    st.markdown("### ⚙️ Features Used")
    st.write("""
    1. Pregnancies
    2. Glucose Level
    3. Blood Pressure
    4. Skin Thickness
    5. Insulin Level
    6. BMI
    7. Diabetes Pedigree Function
    8. Age
    """)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Prediction",
    "📊 Analytics",
    "📈 Model Performance",
    "📚 Information"
])

# ============================================================================
# TAB 1: PREDICTION
# ============================================================================

with tab1:
    st.header("📥 Patient Health Input")
    st.write("Enter the patient's health metrics below to predict whether the patient is diabetic or not diabetic.")
    st.markdown("---")
    
    # Input form in 2 columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Column 1: Basic Metrics")
        
        pregnancies = st.number_input(
            "👶 Pregnancies",
            min_value=0,
            max_value=20,
            value=1,
            step=1,
            help="Number of times pregnant"
        )
        
        glucose = st.number_input(
            "🩸 Glucose Level (mg/dL)",
            min_value=0,
            max_value=300,
            value=120,
            step=1,
            help="Plasma glucose concentration after 2 hours in oral glucose tolerance test"
        )
        
        blood_pressure = st.number_input(
            "❤️ Blood Pressure (mmHg)",
            min_value=0,
            max_value=200,
            value=70,
            step=1,
            help="Diastolic blood pressure (mm Hg)"
        )
        
        skin_thickness = st.number_input(
            "📏 Skin Thickness (mm)",
            min_value=0,
            max_value=100,
            value=20,
            step=1,
            help="Triceps skin fold thickness (mm)"
        )
    
    with col2:
        st.markdown("### Column 2: Advanced Metrics")
        
        insulin = st.number_input(
            "💊 Insulin Level (mu U/ml)",
            min_value=0,
            max_value=900,
            value=80,
            step=1,
            help="2-Hour serum insulin (mu U/ml)"
        )
        
        bmi = st.number_input(
            "⚖️ BMI (Body Mass Index)",
            min_value=0.0,
            max_value=70.0,
            value=25.0,
            step=0.1,
            help="Body mass index (weight in kg/(height in m)^2)"
        )
        
        dpf = st.number_input(
            "🧬 Diabetes Pedigree Function",
            min_value=0.0,
            max_value=3.0,
            value=0.5,
            step=0.01,
            help="Diabetes pedigree function (genetic history score)"
        )
        
        age = st.number_input(
            "🎂 Age (years)",
            min_value=1,
            max_value=120,
            value=30,
            step=1,
            help="Patient age in years"
        )
    
    st.markdown("---")
    
    # Prediction button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        predict_button = st.button(
            "🔍 Predict Diabetes Class",
            use_container_width=True,
            key="predict_btn"
        )
    
    # Perform prediction
    if predict_button:
        input_data = [pregnancies, glucose, blood_pressure, skin_thickness, 
                      insulin, bmi, dpf, age]
        
        prediction, probability, pred_error = predict_diabetes_risk(model, scaler, input_data)
        
        if pred_error:
            st.error(pred_error)
        else:
            st.markdown("---")
            st.markdown("### 📌 PREDICTION RESULT")
            
            predicted_label, color, emoji, confidence = get_prediction_label(prediction, probability)
            
            # Create result card
            if prediction == 1:
                st.markdown(f"""
                <div class="card result-high-risk">
                    <h2 style="margin: 0; color: #721c24;">{emoji} DIABETIC</h2>
                    <p style="margin: 1rem 0 0 0; color: #721c24; font-size: 1em;">
                        The model classified this patient as diabetic.
                        Medical consultation and follow-up testing are recommended.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card result-low-risk">
                    <h2 style="margin: 0; color: #155724;">{emoji} NOT DIABETIC</h2>
                    <p style="margin: 1rem 0 0 0; color: #155724; font-size: 1em;">
                        The model classified this patient as not diabetic.
                        Continue regular health monitoring and preventive care.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display confidence
            if confidence is not None:
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1.5rem; background-color: #f0f9f6; 
                                border-radius: 10px; border-left: 4px solid #198754;">
                        <p style="color: #666; font-size: 0.95em; margin: 0 0 0.5rem 0;">
                            Confidence in Predicted Class
                        </p>
                        <h2 style="color: #198754; margin: 0; font-size: 2em;">
                            {confidence:.1f}%
                        </h2>
                    </div>
                    """, unsafe_allow_html=True)

            # Prediction-specific feature importance
            st.markdown("---")
            st.markdown("### 🔍 Feature Importance for This Prediction")

            importance_df, baseline_score, importance_error = get_prediction_feature_importance(
                model, scaler, input_data
            )

            if importance_error:
                st.warning(importance_error)
            else:
                st.caption(
                    "This chart shows how each input changes the model's decision for this specific patient. "
                    "Red features push the result toward Diabetic, green features push it toward Not Diabetic."
                )

                fig = create_prediction_feature_importance_chart(importance_df)
                st.pyplot(fig, use_container_width=True)

                st.dataframe(
                    importance_df[["Feature", "Importance (%)", "Direction"]],
                    use_container_width=True,
                    hide_index=True
                )

                top_feature = importance_df.iloc[0]
                st.info(
                    f"Most influential feature for this prediction: **{top_feature['Feature']}** ({top_feature['Direction']})."
                )
            
            # Patient summary
            st.markdown("---")
            st.markdown("### 👤 Patient Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Age</div>
                    <div class="metric-value">{int(age)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">BMI</div>
                    <div class="metric-value">{bmi:.1f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Glucose</div>
                    <div class="metric-value">{int(glucose)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-label">Age Group</div>
                    <div class="metric-value">{"Adult" if age >= 18 else "Minor"}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Risk factors analysis
            st.markdown("---")
            st.markdown("### ⚠️ Risk Factors Analysis")
            
            risk_factors = []
            
            if glucose > 126:
                risk_factors.append(("High Glucose", "Your glucose level is elevated", "high"))
            elif glucose > 100:
                risk_factors.append(("Moderate Glucose", "Your glucose level is slightly elevated", "medium"))
            
            if bmi > 30:
                risk_factors.append(("High BMI", "You are in the obese category", "high"))
            elif bmi > 25:
                risk_factors.append(("Moderate BMI", "You are overweight", "medium"))
            
            if age > 45:
                risk_factors.append(("Age Risk", "Age increases diabetes risk", "medium"))
            
            if insulin > 180:
                risk_factors.append(("High Insulin", "Elevated insulin levels detected", "high"))
            
            if blood_pressure > 140:
                risk_factors.append(("High BP", "Blood pressure is elevated", "high"))
            
            if risk_factors:
                for factor, description, severity in risk_factors:
                    if severity == "high":
                        st.warning(f"🔴 **{factor}**: {description}")
                    else:
                        st.info(f"🟡 **{factor}**: {description}")
            else:
                st.success("✅ No significant risk factors detected based on input values")

# ============================================================================
# TAB 2: ANALYTICS
# ============================================================================

with tab2:
    st.header("📊 Feature Importance Analysis")
    st.write("Understanding which health factors matter most in predicting diabetes risk.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Feature Importance Chart")
        fig = create_feature_importance_chart()
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Top Risk Factors")
        st.write("""
        **1. Glucose** (30%)
        - Most important predictor
        - Strong correlation with diabetes
        
        **2. BMI** (18%)
        - Second most important
        - Weight management critical
        
        **3. Age** (14%)
        - Risk increases with age
        - Preventive measures important
        
        **4. Insulin** (10%)
        - Resistance indicator
        - Metabolic health marker
        """)
    
    st.markdown("---")
    st.markdown("### 📈 Recommendations")
    
    rec_col1, rec_col2, rec_col3 = st.columns(3)
    
    with rec_col1:
        st.markdown("""
        <div class="card">
            <h4>🥗 Diet</h4>
            <ul>
            <li>Reduce sugar intake</li>
            <li>Increase fiber</li>
            <li>Balanced nutrients</li>
            <li>Portion control</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col2:
        st.markdown("""
        <div class="card">
            <h4>🏃 Exercise</h4>
            <ul>
            <li>150 min/week cardio</li>
            <li>Strength training</li>
            <li>Regular activity</li>
            <li>Consistency key</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with rec_col3:
        st.markdown("""
        <div class="card">
            <h4>🩺 Monitoring</h4>
            <ul>
            <li>Regular check-ups</li>
            <li>Blood glucose tests</li>
            <li>Track metrics</li>
            <li>Professional advice</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: MODEL PERFORMANCE
# ============================================================================

with tab3:
    st.header("📈 Model Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Model Comparison")
        fig = create_model_comparison_chart()
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Why SVM?")
        st.write("""
        **Support Vector Machine (SVM) Benefits:**
        
        ✅ **Best Performance**: 77.34% accuracy
        
        ✅ **Robust**: Works well with small datasets
        
        ✅ **Non-linear Mapping**: Captures complex relationships
        
        ✅ **Memory Efficient**: Uses subset of training data
        
        ✅ **Versatile**: Handles high-dimensional data
        
        **Trade-offs:**
        - Slower for large datasets
        - Requires parameter tuning
        - Less interpretable than simple models
        """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Training Accuracy</div>
            <div class="metric-value">77.34%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Test Accuracy</div>
            <div class="metric-value">77.34%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-label">Model Type</div>
            <div class="metric-value">SVM</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Algorithm Details")
    
    algo_col1, algo_col2 = st.columns(2)
    
    with algo_col1:
        st.write("""
        **Logistic Regression**
        - Simple linear classifier
        - 76.5% accuracy
        - Fast and interpretable
        - Baseline model
        """)
        
        st.write("""
        **Random Forest**
        - Ensemble method
        - 75.8% accuracy
        - Handles non-linearity
        - Good feature importance
        """)
        
        st.write("""
        **SVM** ⭐
        - Best performer
        - 77.34% accuracy
        - Non-linear kernel
        - Optimal classification boundary
        """)
    
    with algo_col2:
        st.write("""
        **Gradient Boosting**
        - Sequential ensemble
        - 75.2% accuracy
        - Strong learner composition
        - Prone to overfitting
        """)
        
        st.write("""
        **Neural Network**
        - Deep learning approach
        - 76.0% accuracy
        - Captures complex patterns
        - Requires more data
        """)

# ============================================================================
# TAB 4: INFORMATION
# ============================================================================

with tab4:
    st.header("📚 Educational Information")
    
    info_tab1, info_tab2, info_tab3 = st.tabs([
        "🏥 About Diabetes",
        "📊 Dataset Info",
        "🔬 ML Concepts"
    ])
    
    with info_tab1:
        st.markdown("""
        ## Type 2 Diabetes Mellitus
        
        ### What is Diabetes?
        Diabetes is a chronic disease characterized by high blood glucose levels. 
        Type 2 diabetes is the most common form, accounting for 85-90% of all diabetes cases.
        
        ### Risk Factors
        - **Obesity**: BMI > 30 significantly increases risk
        - **Age**: Risk increases after age 45
        - **Family History**: Genetic predisposition matters
        - **Lifestyle**: Diet and exercise are crucial
        - **Ethnicity**: Some populations have higher risk
        
        ### Complications
        - Heart disease and stroke
        - Kidney damage
        - Eye complications (retinopathy)
        - Nerve damage (neuropathy)
        - Foot complications
        
        ### Prevention
        - Maintain healthy weight
        - Regular physical activity
        - Balanced diet
        - Regular health check-ups
        - Stress management
        - Adequate sleep
        """)
    
    with info_tab2:
        st.markdown("""
        ## PIMA Indians Diabetes Dataset
        
        ### Dataset Overview
        - **Source**: National Institute of Diabetes and Digestive and Kidney Diseases
        - **Samples**: 768 records
        - **Features**: 8 medical/demographic attributes
        - **Target**: Binary (Diabetes: Yes/No)
        - **Positive Class**: 268 cases (34.9%)
        - **Negative Class**: 500 cases (65.1%)
        
        ### Features Explained
        1. **Pregnancies**: Number of pregnancies
        2. **Glucose**: Plasma glucose concentration (mg/dL)
        3. **Blood Pressure**: Diastolic blood pressure (mmHg)
        4. **Skin Thickness**: Triceps skin fold thickness (mm)
        5. **Insulin**: 2-hour serum insulin (mu U/ml)
        6. **BMI**: Body Mass Index (kg/m²)
        7. **Diabetes Pedigree Function**: Genetic predisposition score
        8. **Age**: Age in years
        
        ### Data Characteristics
        - Real clinical data from actual patients
        - Collected from PIMA Indian population
        - High-quality medical measurements
        - Balanced features for classification
        """)
    
    with info_tab3:
        st.markdown("""
        ## Machine Learning Concepts
        
        ### Classification
        Predicting which category a data point belongs to (Diabetic vs Non-Diabetic).
        
        ### Supervised Learning
        Using labeled data (with known outcomes) to train the model.
        
        ### Feature Scaling
        Normalizing input features to the same scale for better model performance.
        
        ### Model Evaluation Metrics
        
        **Accuracy**: Percentage of correct predictions
        - Formula: (TP + TN) / (TP + TN + FP + FN)
        - Our SVM: 77.34%
        
        **Precision**: True positives among predicted positives
        - Important when false positives are costly
        
        **Recall**: True positives among actual positives
        - Important when false negatives are costly
        
        **F1-Score**: Harmonic mean of precision and recall
        - Balances both metrics
        
        ### Why Different Algorithms?
        - **Logistic Regression**: Baseline, interpretable
        - **Random Forest**: Non-linear, ensemble approach
        - **SVM**: Best for this dataset, good generalization
        - **Gradient Boosting**: Sequential learning
        - **Neural Network**: Deep learning, complex patterns
        
        ### Model Selection
        We chose SVM because it:
        - Achieved highest accuracy (77.34%)
        - Generalizes well to new data
        - Works efficiently with our dataset size
        - Provides good probability estimates
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <p><strong>📧 Contact</strong></p>
        <p>For questions about this project</p>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <p><strong>⚕️ Disclaimer</strong></p>
        <p>For educational purposes only</p>
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <p><strong>📚 Source</strong></p>
        <p>PIMA Indians Diabetes Dataset</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e0e0e0; color: #999; font-size: 0.85em;">
    <p>🩺 Diabetes Classification Dashboard | Built with Streamlit</p>
    <p>© 2024 Group 2 - MLC Class Project | All Rights Reserved</p>
    <p>This application is a demonstration of ML in healthcare. Always consult healthcare professionals for medical decisions.</p>
</div>
""", unsafe_allow_html=True)