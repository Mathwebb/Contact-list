from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from contact.models import Contact

def index(request: HttpRequest) -> HttpResponse:
    contacts = Contact.objects.filter(show=True).order_by('-id')[:20]

    context = {
        'contacts': contacts,
        'page_title': 'Contatos - ',
    }

    return render(
        request,
        'contact/index.html',
        context,
    )

def search(request: HttpRequest) -> HttpResponse:
    search_value = request.GET.get('q', '').strip()

    contacts = Contact.objects\
        .filter(show=True)\
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(email__icontains=search_value)
        )\
        .order_by('-id')[:20]

    if search_value == '':
        return redirect('contact:index')

    context = {
        'contacts': contacts,
        'page_title': 'Search - ',
        'search_value': search_value,
    }

    return render(
        request,
        'contact/index.html',
        context,
    )

def contact(request: HttpRequest, contact_id: int) -> HttpResponse:
    # single_contact: Contact = Contact.objects.filter(pk=contact_id).first()
    single_contact = get_object_or_404(Contact, pk=contact_id, show=True)
    
    context = {
        'contact': single_contact,
        'page_title': f'{single_contact.first_name} {single_contact.last_name} - ',
    }
    return render(
        request,
        'contact/contact.html',
        context
    )
