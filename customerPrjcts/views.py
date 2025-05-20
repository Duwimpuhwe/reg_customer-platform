from django.shortcuts import render,HttpResponse, redirect
from .forms import ProjectApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.cache import never_cache # added for caching

# Create your views here.

@login_required # This @login_required decorator ensures that only logged-in users can access the application form.
def customerpage(request):

  if request.method == "POST":
    form = ProjectApplicationForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('Success')  # Redirects to success page after form submission
  else:
        form = ProjectApplicationForm()
  # return HttpResponse('I love humility')
  # return render(request,"customerPrjcts/applicationform.html")
  return render(request, "customerPrjcts/applicationform.html", {"form": form})

def baseCustomer(request):
  return render(request,"customerPrjcts/base.html")

def app_successifully(request):
  return render(request,"customerPrjcts/appSuccess.html")

@never_cache
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("customerpage")  # Redirect to the form after signup
    else:
        form = UserCreationForm()
    return render(request, "customerPrjcts/register.html", {"form": form})