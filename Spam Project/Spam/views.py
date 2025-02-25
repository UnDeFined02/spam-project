from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
import os
import joblib
import logging

logger = logging.getLogger(__name__)  # Django logging

# Load models with error handling
model1_path = os.path.join(os.path.dirname(__file__), "mySVCModel1.pkl")
model2_path = os.path.join(os.path.dirname(__file__), "myModel.pkl")

try:
    model1 = joblib.load(model1_path)
    model2 = joblib.load(model2_path)
except Exception as e:
    logger.error(f"Error loading models: {e}")
    model1, model2 = None, None

# Index View
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.method == "POST":
        un = request.POST.get('username')
        up = request.POST.get('password')

        if un == "maruf" and up == "Maruf@123":
            request.session['authdetails'] = "maruf"
            return render(request, 'index.html')
        else:
            return render(request, 'auth.html')
    else:
        if 'authdetails' in request.session:
            return render(request, 'index.html')
        else:
            return render(request, 'auth.html')

# Check Spam View
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkSpam(request):
    if request.method == "POST":
        if request.session.get('authdetails') == "maruf":
            algo = request.POST.get("algo")
            rawData = request.POST.get("rawdata")

            if not rawData or rawData.strip() == "":
                return render(request, 'output.html', {"answer": "Invalid input!"})

            rawData = [rawData]  # Ensure correct format

            # Model prediction
            if algo == "Algo-1" and model1:
                prediction = model1.predict(rawData)[0]
            elif algo == "Algo-2" and model2:
                prediction = model2.predict(rawData)[0]
            else:
                return render(request, 'output.html', {"answer": "Invalid model selection!"})

            # Map prediction to "ham" or "spam"
            result = "ham" if prediction == 0 else "spam"

            return render(request, 'output.html', {"answer": result})
        else:
            return redirect('/')
    else:
        return render(request, 'index.html')

# Logout View
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if 'authdetails' in request.session:
        request.session.flush()
    return redirect('/')
