from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# import pandas as pd
# import plotly.express as px 
# import plotly.offline as py
    
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .models import User

class SignupPage(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Enregistrer l'utilisateur
        self.object = form.save()
        # Envoyer un e-mail d'approbation à l'administrateur
        send_approval_request_email(self.object)
        return redirect(self.get_success_url())
    
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def signup(request):
    if request.method == 'POST':
        # Traitement du formulaire d'inscription
        # Envoyer l'e-mail d'activation
        subject = 'Activation de compte'
        message = 'Veuillez cliquer sur le lien suivant pour activer votre compte : http://example.com/activation/'
        sender = settings.EMAIL_HOST_USER
        recipient = request.POST.get('email')
        
        send_mail(subject, message, sender, [recipient])
        return render(request, 'signup_success.html')
    else:
        return render(request, 'signup_form.html')


def send_approval_request_email(new_user):
    subject = "Demande d'approbation d'inscription"
    message = f"Un nouvel utilisateur, {new_user.username}, a demandé à s'inscrire. Veuillez approuver ou rejeter cette demande."
    approval_link = reverse('approve_user', args=[new_user.id])  # Assurez-vous d'avoir une vue et un URL correspondant
    message += f"<Cliquez ici pour approuver>{approval_link}"
    send_mail(subject, message, 'from@example.com', ['admin@example.com'])

def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_approved = True
    user.save()
    # Vous pouvez ajouter ici une notification par email à l'utilisateur pour lui dire qu'il a été approuvé
    return redirect('admin_dashboard')  # Redirigez vers la page souhaitée après l'approbation



def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def eda(request):

    # path_data = "main/cleandata.csv"
    # data = pd.read_csv(path_data)
    # data.State = data.State.dropna()
    # data.ApprovalYear = data.ApprovalYear.dropna()
    # data["SBA_Appv"] = data["SBA_Appv"].dropna()
    # data = data.groupby(['State', 'ApprovalYear'],).sum('SBA_Appv').sort_values(by='ApprovalYear', ascending=True).reset_index()
    # data = data[["State", "SBA_Appv", 'ApprovalYear']]
    # data = data.rename(columns={'SBA_Appv':'Amount guaranteed by SBA'})

    # fig = px.choropleth(data,
    #                     locations='State',
    #                     locationmode='USA-states',
    #                     scope="usa",
    #                     color='Amount guaranteed by SBA',
    #                     hover_name = 'State',
    #                     # hover_data = 'Amount guaranteed by SBA',
    #                     animation_frame='ApprovalYear',
    #                     color_continuous_scale='viridis',
    #                     title='AMOUNT OF LOANS GUARANTEED BY SBA TO EACH STATE OVER TIME')
    # # fig.update_geos(fitbounds="locations", visible=False)

    # fig.update_layout(width=800, height=600)
    # fig.show()

    # graph_interactif = py.plot(fig, filename='graphique_interactif.html')
    # Plotly.newPlot('graph-container', fig);
    # window.onload = loadGraph;
    return render(request, 'main/eda.html')


def model(request):
    return render(request, 'main/model.html')

@login_required
def special_page(request):
    return render(request, "main/special_page.html")

@login_required
def predict_page(request):
    return render(request, 'main/predict.html')

def graphique_interactif(request):
    return render(request, 'static/graphique_interactif.html')


from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect

def custom_logout(request):
    next_url = request.GET.get('next')  # Récupérer l'URL 'next' de la requête GET
    django_logout(request)
    if next_url:
        return redirect(next_url)  # Rediriger vers l'URL 'next' après la déconnexion
    else:
        # Rediriger vers la page actuelle si 'next' n'est pas spécifié
            return redirect(request.path)