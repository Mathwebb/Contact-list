from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from contact.forms import ContactForm


def create(request: HttpRequest) -> HttpResponse:

    if request.method == 'POST':
        context = {
            'form': ContactForm(request.POST),
        }

        return render(
            request,
            'contact/create.html',
            context,
        )
    
    context = {
        'form': ContactForm(),
    }

    return render(
        request,
        'contact/create.html',
        context,
    )