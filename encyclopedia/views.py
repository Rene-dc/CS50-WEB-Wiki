from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entrypage(request, entry):
    content = util.get_entry(entry)
    title = entry
    conversion = util.convert_markdown(content)
    if content == None:
        content = "The page you asked for was not found."
        title = "not found"
    return render(request, "encyclopedia/entry.html", {
        "content": conversion,
        "entry": title
    })

def search(request):
    q = request.GET['q'].lower()
    list = util.list_entries()
    listlen = len(list)
    lowlist = []
    for i in range(listlen):
        lowlist.append(list[i].lower())
    if q in lowlist or q in list: 
        print(q)
        print(lowlist)
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[q]))
    else: 
        matchlist = []
        for i in range(listlen):
            if q in lowlist[i]:
                matchlist.append(list[i])
        print(matchlist)
        return render(request, "encyclopedia/searched.html", {
            "entries": matchlist
        })

class NewPageForm(forms.Form):
    entry = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={'required':'True', 'placeholder':'Use Markdown to edit content'}))

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        list = util.list_entries()
        listlen = len(list)
        lowlist = []
        for i in range(listlen):
            lowlist.append(list[i].lower())
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            content = form.cleaned_data["content"]
            if entry.lower() in lowlist:
                return render(request, "encyclopedia/error.html", {
                    "message": "Entry is already in Wiki pages !"
                })
            else:
                # If everything ok, redirect to entry page
                util.save_entry(entry, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry]))
        else: 
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })
    else:
        content = """# This is a title

## This is a secondary title

This is an unordered list:

* item 1
+ item 2
- item 3

A paragraph is placed between blank lines.

You can add a new line with 2 spaces at the end of this line.  
This is a new line.

**This is bold text**

*This is italic*"""
    
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm(initial={'content': content})
    })

def editpageselect(request):
    return render(request, "encyclopedia/editpagelist.html", {
        "entries": util.list_entries()
    })

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'required':'True'}))

def editpage(request, entry):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entry, content)
            # Redirect to the entry page
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry]))
        else: 
            # Redirect to the page with the form
            return render(request, "encyclopedia/editpage.html", {
                "entry": entry,
                "form": form
            })
    else:
        # Check entry
        content = util.get_entry(entry)
        if content == None:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry is not in Wiki ! Where did you find it ?"
            })
        form = EditPageForm(initial={'content': content})
        # Render edition page
        return render(request, "encyclopedia/editpage.html", {
            "entry": entry,
            "form": form
        })

def randompage(request):
    list = util.list_entries()
    listlen = len(list) - 1
    i = random.randint(0, listlen)
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[list[i]]))
