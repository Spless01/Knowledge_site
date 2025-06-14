from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def auth_forms(request):
    return {
        'login_form': AuthenticationForm(),
        'reg_form': UserCreationForm()
    }
