from django import forms
from django.shortcuts import render
import random

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control title"}), max_length=100)
    markdown_content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control textarea"}), max_length=10000)

class EditPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control title", "readonly": "True"}), max_length=100)
    markdown_content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control textarea"}), max_length=10000) 

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display(request, title):
    content = util.get_entry(title)
    if content == None:
        return error(request, f"No article with the name '{title}'.")
    else:
        entries = util.list_entries()
        for entry in entries:
            if title in entry:
                title = entry
        return render(request, "encyclopedia/entry.html", {
            "content": content,
            "title": title
        })

def search(request):
    q = request.GET.get('q')
    if util.get_entry(q) == None:
        entries = util.list_entries()
        results = []
        for entry in entries:
            if q.lower() in entry.lower():
                results.append(entry)
        return render(request, "encyclopedia/search.html", {
            "q": q,
            "results": results
    })
    else:
        return display(request, q)
        
def new(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["markdown_content"]
            if util.get_entry(title) == None:
                util.save_entry(title, content)
                return display(request, title)
            else:
                return error(request, "Page already exists.")
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm()
    })

def edit(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["markdown_content"]
            util.save_entry(title, content)
            return display(request, title)
    else:
        title = request.GET.get("title")
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "form": EditPageForm({"title": title, "markdown_content": content}),
            "title": title
        })

def rndm(request):
    entries = util.list_entries()
    return display(request, entries[random.randint(0, len(entries)-1)])

def error(request, message):
    return render(request, "encyclopedia/error.html", {
        "message": message
    })




# TRY TO FIX TITLE CASE FOR DISPLAY FUNCTION WHICH IS ALSO PASSED TO EDIT FUNCTION
# IMPLEMENT MARKDOWN TO HTML CONVERSION