from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import joblib
import numpy as np
from .forms import DiseaseInputForm

# Load model at startup
try:
    model = joblib.load('models/disease_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    feature_names = joblib.load('models/feature_names.pkl')
except FileNotFoundError:
    model = None
    scaler = None
    feature_names = None


def home(request):
    """Landing page"""
    context = {
        'title': 'Disease Prediction App',
        'description': 'Get a prediction based on your health metrics'
    }
    return render(request, 'predictor/home.html', context)


@require_http_methods(["GET", "POST"])
def predict(request):
    """Main prediction view - handles form display and submission"""
    
    # Check if model is loaded
    if not model:
        error_message = "⚠️ Model not loaded. Please train the model first by running: python ml_model.py"
        return render(request, 'predictor/predict.html', {'error': error_message})
    
    if request.method == 'POST':
        form = DiseaseInputForm(request.POST)
        
        if form.is_valid():
            try:
                # Extract all features in correct order
                data = []
                for feature in feature_names:
                    value = float(form.cleaned_data.get(feature))
                    data.append(value)
                
                # Convert to numpy array
                input_data = np.array(data).reshape(1, -1)
                
                # Scale the input using the scaler from training
                input_scaled = scaler.transform(input_data)
                
                # Get prediction
                prediction = model.predict(input_scaled)[0]
                probabilities = model.predict_proba(input_scaled)[0]
                
                # Get probability of disease (class 1)
                disease_probability = round(probabilities[1] * 100, 1)
                
                # Determine risk level
                if disease_probability > 70:
                    risk_level = 'HIGH'
                    risk_color = 'red'
                    risk_icon = '🔴'
                elif disease_probability > 40:
                    risk_level = 'MEDIUM'
                    risk_color = 'orange'
                    risk_icon = '🟡'
                else:
                    risk_level = 'LOW'
                    risk_color = 'green'
                    risk_icon = '🟢'
                
                # Get top 5 important features
                top_features_idx = np.argsort(model.feature_importances_)[-5:][::-1]
                top_features = [
                    {
                        'name': feature_names[i],
                        'importance': round(model.feature_importances_[i], 4),
                        'value': float(form.cleaned_data.get(feature_names[i]))
                    }
                    for i in top_features_idx
                ]
                
                # Prepare context with all data
                context = {
                    'form': form,
                    'prediction': int(prediction),
                    'probability': disease_probability,
                    'risk_level': risk_level,
                    'risk_color': risk_color,
                    'risk_icon': risk_icon,
                    'top_features': top_features,
                    'has_disease': prediction == 1,
                    'prediction_made': True,
                }
                
                return render(request, 'predictor/result.html', context)
            
            except Exception as e:
                error_message = f"❌ Prediction error: {str(e)}"
                return render(request, 'predictor/predict.html', {
                    'form': form,
                    'error': error_message
                })
        else:
            # Form has errors
            return render(request, 'predictor/predict.html', {'form': form})
    
    else:  # GET request - show empty form
        form = DiseaseInputForm()
        context = {
            'form': form,
            'prediction_made': False,
        }
        return render(request, 'predictor/predict.html', context)