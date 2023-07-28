# run separate development server at http://127.0.0.1:8050/
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EditNote
import requests
import json


def home_view(request):
    link = 'http://127.0.0.1:8000/api/notes/notes-public/'
    try:
        r = requests.get(url=link)
        # r.content would have shown the data in bytes,  r.text shows in html
        return render(request, 'frontapp/home.html', {'data': json.loads(r.text)['data']})
    except:
        messages.warning(request, message=f"You're not connected to the backend server")
        return render(request, 'frontapp/home.html', {})
    
        
    

def make_notes(request):    
    link = 'http://127.0.0.1:8000/api/notes/notes-view/'
    if request.POST:
        try:
            full_token = 'Bearer ' + access_token  # token comes from login_view
            Authorization = {'Authorization': full_token}
            title = request.POST.get('title')
            matter = request.POST.get('matter')
            data_packet = {'title': title, 'matter': matter}
            r = requests.post(url=link, data=data_packet, headers=Authorization) # the data has to go with the argument 'data' not 'json'
            response_received = json.loads(r.text).get('message')
            if 200 <= r.status_code <= 299:
                messages.success(request, message=f"{response_received}, Status code: {r.status_code}")
            else:        
                messages.warning(request, message=f"{response_received}, Status code: {r.status_code}")
            return render(request, 'frontapp/notes.html', {})
        except:
            messages.warning(request, message=f"Access token missing or invalid")
            return render(request, 'frontapp/notes.html', {})
    else:
        return render(request, 'frontapp/notes.html', {})
            
        


def view_notes(request):    
    link = 'http://127.0.0.1:8000/api/notes/notes-view/'
    try:
        full_token = 'Bearer ' + access_token  # token comes from login_view
        Authorization = {'Authorization': full_token}
        term = request.POST.get('sname')
        if term:
            link = f'http://127.0.0.1:8000/api/notes/notes-view/?search={term}'
        r = requests.get(url=link, headers=Authorization)  # the searching happens in GET, POST not needed
        if 200 <= r.status_code <= 299:
            messages.success(request, message=f"Data received, Status code: {r.status_code}")
        else:
            messages.warning(request, message=f"Data not received, Status code: {r.status_code}")
        return render(request, 'frontapp/personal.html', {'data':json.loads(r.text).get('data'), 'agent': json.loads(r.text).get('agent')})
    except:
        messages.warning(request, message=f"Access token missing or invalid, please login")
        return render(request, 'frontapp/personal.html', {})
    # using same template as in home.view
    

def search_notes(request):
    link = 'http://127.0.0.1:8000/api/notes/notes-view/'
    try:
        full_token = 'Bearer ' + access_token  # token comes from login_view
        Authorization = {'Authorization': full_token}
        search = request.POST.get('sname')
        data_packet = {'search': search}
        r = requests.post(url=link, data=data_packet, headers=Authorization)
        if 200 <= r.status_code <= 299:
            messages.success(request, message=f"Data received, Status code: {r.status_code}")
        else:
            messages.warning(request, message=f"Data not received, Status code: {r.status_code}")
        return render(request, 'frontapp/search.html', {'data':json.loads(r.text).get('data'), 'agent': json.loads(r.text).get('agent')})
    except:
        messages.warning(request, message=f"Access token missing or invalid, please login")
        return render(request, 'frontapp/search.html', {})


def login_view(request):
    global access_token # to broadcast the token to other views that require it.
    # response is ok implies login is successful, token is only received in this view, it is not required for login per se
    link = 'http://127.0.0.1:8000/api/members/login/'
    username = request.POST.get('uname')
    password = request.POST.get('pname')
    login_credentials = {'username': username, 'password': password}
    if request.POST:            
        r = requests.post(url=link, json=login_credentials)
        # print('***code', r.status_code) # if the response is 200, the response from the website is good.
        # print('***ok', r.ok) # will return True for anything less than a 400 response
        # print('***headers', r.headers)
        access_token = json.loads(r.text).get('data').get('access')
        response_received = json.loads(r.text).get('message')
        if 200 <= r.status_code <= 299:
            messages.success(request, message=f"{response_received}, Status code: {r.status_code}")
        else:        
            messages.warning(request, message=f"{response_received}, Status code: {r.status_code}")
        # return render( request, 'frontapp/login.html', {})
        return redirect('view')
    else:
        return render( request, 'frontapp/login.html', {})



def register_view(request):
    link = 'http://127.0.0.1:8000/api/members/register/'
    first_name = request.POST.get('fname')
    last_name = request.POST.get('lname')
    new_username = request.POST.get('uname')
    new_password = request.POST.get('pname')
    register_details = {'first_name': first_name, 'last_name': last_name, 'username': new_username, 'password': new_password}
    if request.POST:
        r = requests.post(url=link, json=register_details)
        response_received = json.loads(r.text).get('message')
        if 200 <= r.status_code <= 299:
            messages.success(request, message=f"{response_received}, Status code: {r.status_code}")
        else:        
            messages.warning(request, message=f"{response_received}, Status code: {r.status_code}")
        # return render(request, 'frontapp/register.html', {})
        return redirect('login')
    else:
        return render(request, 'frontapp/register.html', {})



def profile_view(request):
    link = 'http://127.0.0.1:8000/api/members/profile/'
    try:
        full_token = 'Bearer ' + access_token  # token comes from login_view
        headers = {'Authorization': full_token}
        r = requests.get(url=link, headers=headers) # passing the token in the get request
        return render(request, 'frontapp/profile.html', {'data': json.loads(r.text).get('data')})
    except:
        messages.warning(request, message=f"Access token missing or invalid, please login")
        return render(request, 'frontapp/profile.html', {})


def delete_profile(request):
    link = 'http://127.0.0.1:8000/api/members/profile/'
    full_token = 'Bearer ' + access_token  
    headers = {'Authorization': full_token}
    r = requests.delete(url=link, headers=headers) # passing the token in the get request
    return render(request, 'frontapp/profile.html', {'data': json.loads(r.text)})


def all_members(request):
    link = 'http://127.0.0.1:8000/api/members/all/'
    r = requests.get(link)
    # r.content would have shown the data in bytes,  r.text shows in html
    return render(request, 'frontapp/members.html', {'data': json.loads(r.text)['data']})


def delete_post(request, id):
    link = 'http://127.0.0.1:8000/api/notes/notes-view/'
    try:
        full_token = 'Bearer ' + access_token  
        Authorization = {'Authorization': full_token}
        data_packet = {'id': id}
        r = requests.delete(url=link, data=data_packet, headers=Authorization)
        response_received = json.loads(r.text).get('message')
        if 200 <= r.status_code <= 299:
            messages.success(request, message=f"{response_received}, Status code: {r.status_code}")
        else:
            messages.warning(request, message=f"{response_received}, Status code: {r.status_code}")
        # return render(request, 'frontapp/personal.html', {})
        return redirect('view')
    except:
        messages.warning(request, message=f"Access token missing or invalid, please login")
        return render(request, 'frontapp/personal.html', {})

        
def edit_post(request, id):
    link = 'http://127.0.0.1:8000/api/notes/notes-view/'
    try:
        full_token = 'Bearer ' + access_token  
        Authorization = {'Authorization': full_token}
    except:
        messages.warning(request, message=f"Access token missing or invalid, please login")
        return render(request, 'frontapp/editnotes.html', {})
    if request.method == 'POST':
        form_instance = EditNote(request.POST)
        if form_instance.is_valid():
            title        = form_instance.cleaned_data.get('title')
            matter        = form_instance.cleaned_data.get('matter')
            data_packet = {'id': id, 'title': title, 'matter': matter}
            r = requests.patch(url=link, data=data_packet, headers = Authorization)
            response_received = json.loads(r.text).get('message')
            if 200 <= r.status_code <= 299:
                messages.success(request, message=f"{response_received}, Status code: {r.status_code}")
            else:
                messages.warning(request, message=f"{response_received}, Status code: {r.status_code}")
            return redirect('view')
        else:
            messages.error(request, f'invalid data received')
            return render(request, 'frontapp/editnotes.html', {'edit_form': EditNote()})
    else:
        return render(request, 'frontapp/editnotes.html', {'edit_form': EditNote()})

        
    
    