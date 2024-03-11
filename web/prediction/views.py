import datetime
import json
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from .forms import LoanApplicationForm


REGIONS = {
    "AL": "Southeast",
    "AK": "Northwest",
    "AZ": "Southwest",
    "AR": "Southeast",
    "CA": "Southwest",
    "CO": "Southwest",
    "CT": "Northeast",
    'DC': 'Northeast',
    "DE": "Northeast",
    "FL": "Southeast",
    "GA": "Southeast",
    "HI": "Northwest",
    "ID": "Northwest",
    "IL": "Northeast",
    "IN": "Northeast",
    "IA": "Northwest",
    "KS": "Northwest",
    "KY": "Southeast",
    "LA": "Southeast",
    "ME": "Northeast",
    "MD": "Northeast",
    "MA": "Northeast",
    "MI": "Northeast",
    "MN": "Northwest",
    "MS": "Southeast",
    "MO": "Northwest",
    "MT": "Northwest",
    "NE": "Northwest",
    "NV": "Northwest",
    "NH": "Northeast",
    "NJ": "Northeast",
    "NM": "Southwest",
    "NY": "Northeast",
    "NC": "Southeast",
    "ND": "Northwest",
    "OH": "Northeast",
    "OK": "Southwest",
    "OR": "Northwest",
    "PA": "Northeast",
    "RI": "Northeast",
    "SC": "Southeast",
    "SD": "Northwest",
    "TN": "Southeast",
    "TX": "Southwest",
    "UT": "Northwest",
    "VT": "Northeast",
    "VA": "Southeast",
    "WA": "Northwest",
    "WV": "Southeast",
    "WI": "Northwest",
    "WY": "Northwest"
}

RECESSION_PERIODS = [
    (1969, 1970),
    (1973, 1975),
    (1980, 1980),
    (1981, 1982),
    (1990, 1991),
    (2001, 2001),
    (2007, 2009),
    (2020, 2020),  # Including the COVID-19 pandemic recession
]

def is_year_in_recession(year: int) -> bool:
    """Determine if a year is within a recession period or not"""
    return any(start <= year <= end for start, end in RECESSION_PERIODS)


@login_required
def predict_api_page(request):
    url = os.getenv("URL_API")
    session = Session()

    # If this is a POST request we need to process the form data
    if request.method == "POST":
        # Create a form instance and populate it with data from the request
        form = LoanApplicationForm(request.POST)
        # Check whether it's valid or not
        if form.is_valid():
            form.save()  # THIS MAY HAVE TO BE MOVED

            formulaire = form.cleaned_data  # Transform the form to a dict

            # Update formulaire with created features
            date = datetime.datetime.now()
            new_info = {
                "Region" : REGIONS[formulaire["State"]],
                "SameState" : formulaire["State"] == formulaire["BankState"],
                "ApprovalMonth" : date.month,
                "ApprovalDoW" : date.weekday(),
                "Recession" : is_year_in_recession(date.year)
                }
            formulaire.update(new_info)

            # Serialize formulaire to send it to the API
            payload = json.dumps(formulaire)
            
            try:
                response = session.post(url, data=payload)
                api_resp = response.json()
                return render(request, "prediction/predict.html",
                              context={"form": form, "api_resp": api_resp})
            except (ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
                return render(request, "prediction/predict.html",
                            context={"form": form, "error": f"{type(e)}: {e}"})
    else:
        form = LoanApplicationForm()
    return render(request, "prediction/predict.html", context={"form": form})
