# 🩺 Diabetes Risk Prediction Dashboard

A professional, modern healthcare AI dashboard built with Streamlit for predicting diabetes risk using machine learning.

## 📋 Project Overview

This project is a **complete machine learning deployment** showcasing:
- Advanced ML model selection and optimization
- Professional UI/UX design with healthcare theming
- Production-ready error handling and debugging
- Educational content about diabetes and ML concepts
- Real clinical data from PIMA Indians Diabetes Dataset

### 🎯 Key Features

✅ **Advanced ML Models** - 5 different algorithms trained and evaluated  
✅ **Best Performer** - SVM with 77.34% accuracy  
✅ **Modern UI** - Healthcare-themed dashboard with green/white color scheme  
✅ **Interactive Predictions** - Real-time diabetes risk assessment  
✅ **Comprehensive Analytics** - Feature importance, model comparison, visualizations  
✅ **Educational Content** - About diabetes, dataset info, ML concepts  
✅ **Production Ready** - Complete error handling and debugging  
✅ **Responsive Design** - Works on desktop and tablet  

---

## 📊 Dataset Information

**PIMA Indians Diabetes Dataset**
- **Source:** National Institute of Diabetes and Digestive and Kidney Diseases
- **Samples:** 768 patient records
- **Features:** 8 health metrics
- **Target:** Binary classification (Diabetes: Yes/No)
- **Positive Class:** 268 cases (34.9%)
- **Negative Class:** 500 cases (65.1%)

### Features Used:
1. **Pregnancies** - Number of times pregnant
2. **Glucose** - Plasma glucose concentration (mg/dL)
3. **Blood Pressure** - Diastolic blood pressure (mmHg)
4. **Skin Thickness** - Triceps skin fold thickness (mm)
5. **Insulin** - 2-hour serum insulin (mu U/ml)
6. **BMI** - Body Mass Index (kg/m²)
7. **Diabetes Pedigree Function** - Genetic predisposition score
8. **Age** - Age in years

---

## 🤖 Machine Learning Models

All models were trained and compared:

| Model | Accuracy | Status |
|-------|----------|--------|
| **SVM** | **77.34%** | ⭐ **BEST** |
| Logistic Regression | 76.5% | Good baseline |
| Neural Network | 76.0% | Deep learning |
| Random Forest | 75.8% | Ensemble method |
| Gradient Boosting | 75.2% | Sequential learning |

### Why SVM?

Support Vector Machine (SVM) was selected as the best model because:
- **Highest Accuracy** - 77.34% on test data
- **Robust Performance** - Works well with limited data
- **Non-linear Mapping** - Captures complex relationships
- **Good Generalization** - Prevents overfitting
- **Memory Efficient** - Uses subset of training data

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git (optional)

### Installation

1. **Clone or download this project**
   ```bash
   cd "d:\MLC CLASS PROJECT 2"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify model files exist**
   ```
   MLC CLASS PROJECT 2/
   ├── models/
   │   ├── diabetes_model.pkl ✓
   │   └── scaler.pkl ✓
   ├── dataset/
   │   └── diabetes.csv
   ├── app.py
   └── requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the dashboard**
   - Browser will open automatically at `http://localhost:8501`
   - If not, open that URL in your browser

---

## 🛠️ Troubleshooting Common Issues

### ❌ Blank White Screen

**Causes & Solutions:**

1. **Missing Model Files**
   - Check: `models/diabetes_model.pkl` exists
   - Check: `models/scaler.pkl` exists
   - Solution: Re-run your training notebook to regenerate

2. **Import Error**
   - Run: `pip install -r requirements.txt`
   - Verify all packages installed successfully

3. **Working Directory Error**
   - Ensure you're in the correct directory
   - Run: `cd d:\MLC CLASS PROJECT 2`
   - Then: `streamlit run app.py`

4. **Port Already in Use**
   - Run: `streamlit run app.py --server.port 8502`
   - (Use different port number if needed)

5. **Cache Issue**
   - Clear Streamlit cache: `streamlit cache clear`
   - Or: `rm -r ~/.streamlit/cache` (Linux/Mac)

### ⚠️ Model Loading Error

If you see: "❌ Model file not found"
- Verify pickle files exist in `models/` folder
- Check file spelling: `diabetes_model.pkl` and `scaler.pkl`
- Regenerate by running your training notebook

### 📦 Dependency Issues

If packages won't install:
```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt

# Or install individually
pip install streamlit scikit-learn pandas numpy matplotlib
```

---

## 📁 Project Structure

```
MLC CLASS PROJECT 2/
│
├── app.py                          # Main Streamlit application (COMPLETE)
├── main.ipynb                      # Training notebook
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── dataset/
│   ├── diabetes.csv               # Original dataset
│   └── diabetes (1).csv           # Backup copy
│
└── models/
    ├── diabetes_model.pkl         # Trained SVM model
    └── scaler.pkl                 # Feature scaler
```

---

## 🎨 UI Features

### Dashboard Sections

1. **🔍 Prediction Tab**
   - Input 8 health metrics in 2-column layout
   - Real-time prediction on button click
   - Risk assessment with confidence score
   - Patient summary with key metrics
   - Automatic risk factor analysis

2. **📊 Analytics Tab**
   - Feature importance visualization
   - Top risk factors explanation
   - Health recommendations (diet, exercise, monitoring)

3. **📈 Model Performance Tab**
   - Model accuracy comparison chart
   - Explanation of why SVM is best
   - Algorithm details for all 5 models
   - Performance metrics

4. **📚 Information Tab**
   - About diabetes and risk factors
   - Dataset information and characteristics
   - ML concepts and explanations

### Design Elements

- **Color Scheme:** Green (#198754) and white (#f5fff7) - healthcare themed
- **Typography:** Segoe UI for clean, professional look
- **Components:** Cards, gradients, icons, badges
- **Responsive:** Works on different screen sizes
- **Accessibility:** Clear hierarchy and contrast

---

## 🔧 How the App Works

### 1. **Model & Scaler Loading** (Cached)
```
app.py → Load model.pkl → Load scaler.pkl → Cache for performance
```

### 2. **Error Handling**
```
If files missing → Display friendly error message
If model crashes → Catch exception and show error
If prediction fails → User-friendly error notification
```

### 3. **Prediction Flow**
```
User Input (8 values) → Scaler.transform() → Model.predict() 
                     → Get probability → Display results
```

### 4. **Probability Calculation**
```
For SVM:
- Try predict_proba() first
- If not available, use decision_function()
- Convert to probability using sigmoid
- Return confidence score 0-100%
```

---

## 💻 Technical Details

### Dependencies
- **streamlit**: Web framework
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **matplotlib**: Data visualization

### Key Functions

- `load_model_and_scaler()` - Load with caching
- `predict_diabetes_risk()` - Make prediction with error handling
- `get_risk_level()` - Interpret results
- `create_feature_importance_chart()` - Visualization
- `create_model_comparison_chart()` - Model comparison chart

---

## 🚀 Deployment

### Deploy on Streamlit Cloud (Recommended)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Add diabetes risk prediction dashboard"
   git push
   ```

2. **Go to** [share.streamlit.io](https://share.streamlit.io)

3. **Click "New app"** and select your repository

4. **Configure:**
   - Branch: `main`
   - File: `app.py`
   - Python version: `3.9`

5. **Deploy!** 🎉

### Deploy Locally (For Presentation)

```bash
# Make sure you're in the project directory
cd "d:\MLC CLASS PROJECT 2"

# Start the app
streamlit run app.py

# Keep running while presenting
# Access at: http://localhost:8501
```

### Requirements for Deployment

- `app.py` ✓
- `requirements.txt` ✓
- `models/diabetes_model.pkl` ✓
- `models/scaler.pkl` ✓
- `.gitignore` (recommended, to exclude large files)

---

## 📋 Debugging Checklist

Use this if something doesn't work:

- [ ] Python 3.8+ installed: `python --version`
- [ ] All packages installed: `pip install -r requirements.txt`
- [ ] In correct directory: `cd d:\MLC CLASS PROJECT 2`
- [ ] Model files exist: `models/diabetes_model.pkl` and `models/scaler.pkl`
- [ ] No port conflict: Run `streamlit run app.py --server.port 8502`
- [ ] Cache cleared: `streamlit cache clear`
- [ ] Dependencies up-to-date: `pip install --upgrade -r requirements.txt`
- [ ] Check Streamlit version: `streamlit version`
- [ ] Run directly: `python -m streamlit run app.py`

---

## 📊 Why This Design Works

### For College Project Presentation

✅ **Professional Appearance** - Modern healthcare UI  
✅ **Complete Documentation** - All components explained  
✅ **Real Data** - PIMA Indians clinical dataset  
✅ **Multiple Models** - Shows ML expertise  
✅ **Educational Content** - Demonstrates understanding  
✅ **Error Handling** - Shows production mindset  
✅ **Responsive Design** - Looks good on projector  

### Suitable For:
- Final year college projects
- Machine learning portfolio pieces
- Internship interviews and portfolios
- LinkedIn project showcase
- Graduation capstone projects

---

## 🎓 Learning Resources

Embedded in the app:
- About diabetes (medical background)
- Dataset information (data science)
- ML concepts explained (algorithms)
- Feature importance (interpretability)
- Model comparison (selection criteria)

---

## ⚠️ Important Notes

### For Accuracy Testing:
- Use realistic health values in normal ranges
- Model was trained on PIMA Indian population data
- Results should be interpreted by healthcare professionals
- This is for educational purposes only

### For Deployment:
- Ensure model files are with the app
- Test locally before deploying
- Keep dependencies up-to-date
- Monitor app performance

---


## 📞 Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Verify all **files exist** in correct locations
3. Run the **Debugging Checklist**
4. Check **requirements.txt** is installed
5. Try running from **project directory**

---

## 📄 License

This project is for educational purposes. Feel free to modify and use for your class project.

---

## 🎉 You're All Set!

Your professional healthcare AI dashboard is ready to use!

**To start the app:**
```bash
cd "d:\MLC PROJECT"
streamlit run app.py
```

**Happy presenting! 🩺**

---

*Built with ❤️ using Streamlit and Machine Learning*
