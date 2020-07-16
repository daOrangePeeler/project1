from django import forms

from django.shortcuts import render, redirect

#ONLY USED FOR HTTP RESPONSE TESTING \/
from django.http import HttpResponse, Http404

from . import util
from . import compile

import markdown2
import re
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}),)
    body = forms.CharField(label='Body', max_length=50000, widget=forms.Textarea(attrs={'class': "form-control"}),)

class EditEntryForm(forms.Form):
    body = forms.CharField(label='Body', max_length=50000, widget=forms.Textarea(attrs={'class': "form-control"}),)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#def display_entry(request, entry_name):
#    return HttpResponse(f"works {entry_name}")

def display_entry(request, entry_name):
    if entry_name not in util.list_entries():
        #return HttpResponseNotFound(f"No wiki page found for '{entry_name}'")
        raise Http404()
    else:
        return render(request, "encyclopedia/entry_layout.html", {
            "title": entry_name,
            "body": markdown2.markdown(util.get_entry(entry_name)),
        })

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            #print(title + ".md")
            #print(util.list_entries())

            if('/' in title or '.' in title or '\\' in title):
                #print("you broke it")
                return render(request, "encyclopedia/new_entry.html", {
                "form": NewEntryForm,
                "error_text": "Invalid characters in title."
            })

            elif(title in util.list_entries()):
                #print("2you broke it")
                return render(request, "encyclopedia/new_entry.html", {
                "form": NewEntryForm,
                "error_text": "Page with that title already exists."
            })
            else:
                newEntryFile = open(rf"entries/{title}.md", "w")
                newEntryFile.write(body)
                newEntryFile.close()
                return redirect(f"/wiki/{title}")

        else:
            return render(request, "encyclopedia/new_entry.html", {
                "form": NewEntryForm,
            })
    else:
        return render(request, "encyclopedia/new_entry.html", {
            "form": NewEntryForm,
        })

    return render(request, "encyclopedia/new_entry.html", {
        "form": NewEntryForm,
    })

def random_page(request):
    rand_entry = random.choice(util.list_entries())
    return redirect(f"/wiki/{rand_entry}/")

def search(request):
    if request.method == 'GET':
        try:
            search_val = request.GET['q']

            if(request.GET['q'] in util.list_entries()):
                return redirect(f"/wiki/{request.GET['q']}")
            #Pass results list to html django search template for formatting
            results = []
            for i in util.list_entries():
                if(search_val in i):
                    results.append(i)
            return render(request, "encyclopedia/search.html", {
                "results": results,
                "title": search_val
            })

        except Exception as error:
            return render(request, "encyclopedia/search.html")

        return render(request, "encyclopedia/search.html")

def edit_entry(request, entry_name):
    if request.method == 'GET':
        if entry_name not in util.list_entries():
            #return HttpResponseNotFound(f"No wiki page found for '{entry_name}'")
            raise Http404()
        else:
            #form = EditEntryForm(request.POST, {"body": util.get_entry(entry_name)})
            eform = EditEntryForm({"body": util.get_entry(entry_name)})
            
            return render(request, "encyclopedia/edit_entry.html", {
                "entry_name": entry_name,
                "form": eform,
            })
    elif request.method == 'POST':
        
        eform = EditEntryForm(request.POST)
        
        if eform.is_valid():

            body = eform.cleaned_data["body"]
            newEntryFile = open(rf"entries/{entry_name}.md", "w")
            newEntryFile.write(body)
            newEntryFile.close()
            return redirect(f"/wiki/{entry_name}")
        else:
            return HttpResponse("invalid")