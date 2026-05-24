from django import forms

class DiseaseInputForm(forms.Form):
    """Form for disease prediction input"""
    
    # These are the 13 features from the Heart Disease dataset
    # Adjust field names based on your dataset
    
    age = forms.IntegerField(
        label="Age",
        min_value=0,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '45'
        })
    )
    
    sex = forms.ChoiceField(
        label="Sex",
        choices=[(0, 'Female'), (1, 'Male'),(2,'Other')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    cp = forms.ChoiceField(
        label="Chest Pain Type",
        choices=[
            (0, 'Typical Angina'),
            (1, 'Atypical Angina'),
            (2, 'Non-anginal Pain'),
            (3, 'Asymptomatic')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    trestbps = forms.IntegerField(
        label="Resting Blood Pressure (mmHg)",
        min_value=0,
        max_value=300,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '120'})
    )
    
    chol = forms.IntegerField(
        label="Serum Cholesterol (mg/dl)",
        min_value=0,
        max_value=600,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '200'})
    )
    
    fbs = forms.ChoiceField(
        label="Fasting Blood Sugar > 120 mg/dl",
        choices=[(0, 'No'), (1, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    restecg = forms.ChoiceField(
        label="Resting ECG Results",
        choices=[(0, 'Normal'), (1, 'ST-T Abnormality'), (2, 'LV Hypertrophy')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    thalach = forms.IntegerField(
        label="Max Heart Rate Achieved",
        min_value=0,
        max_value=300,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '150'})
    )
    
    exang = forms.ChoiceField(
        label="Exercise Induced Angina",
        choices=[(0, 'No'), (1, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    oldpeak = forms.FloatField(
        label="ST Depression (oldpeak)",
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2.5', 'step': '0.1'})
    )
    
    slope = forms.ChoiceField(
        label="ST Slope",
        choices=[(0, 'Upsloping'), (1, 'Flat'), (2, 'Downsloping')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    ca = forms.ChoiceField(
        label="Major Vessels Colored",
        choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    thal = forms.ChoiceField(
        label="Thalassemia",
        choices=[(0, 'Normal'), (1, 'Fixed Defect'), (2, 'Reversible Defect'), (3, 'Unknown')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )