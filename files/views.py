from django.shortcuts import render, redirect
from .forms import FileForm, DirectoryForm
from .models import File, Directory, FileVisibility
from social.models import Friends, FriendRequestStatus
from django.http import FileResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from flashcards.views import user_list

@xframe_options_sameorigin
def view(request, directory_path):
    directories = directory_path.split('/')
    user = request.user
    parent = None
    parent_dir = "/".join(directories[:-1])
    print("User:", user)
    directory = directories[::-1]
    while directory:
        try:
            curr = Directory.objects.get(name=directory.pop(), parent_directory=parent)
        except Directory.DoesNotExist:
            return redirect('home')
        if curr.visibility != FileVisibility.PUBLIC and curr.user != user:
            if curr.visibility == FileVisibility.FRIENDS:
                if not are_friends(user, curr.user):
                    return redirect('home')
            else:
                return redirect('home')
        parent = curr

    if parent is None:
        return redirect('home')
    
    if request.method == 'POST':
        if 'file_upload_form' in request.POST:
            file_form = FileForm(request.POST, request.FILES)
            if file_form.is_valid():
                file_instance = file_form.save(commit=False)
                file_instance.name = request.FILES['file'].name
                file_instance.user = request.user
                file_instance.user_id = request.user.id
                file_instance.file_type = File.get_file_type(request.FILES['file'].name)
                file_instance.parent_directory = parent
                file_instance.save()
                return redirect('view', directory_path=directory_path)
            directory_form = DirectoryForm()
        elif 'directory_creation_form' in request.POST:
            directory_form = DirectoryForm(request.POST)
            if directory_form.is_valid():
                directory_instance = directory_form.save(commit=False)
                directory_instance.name = request.POST['name']
                directory_instance.user = request.user
                directory_instance.parent_directory = parent
                directory_instance.save()
                print("Directory", directory_instance.name, "created")
                return redirect('view', directory_path=directory_path)
            print(directory_form.errors)
            file_form = FileForm()
        else:
            file_form = FileForm()
            directory_form = DirectoryForm()
    else:
        file_form = FileForm()
        directory_form = DirectoryForm()
    
    files = []

    output_dirs = []
    if parent.user == user:
        files = File.objects.filter(parent_directory=parent)
        output_dirs = Directory.objects.filter(parent_directory=parent)
    elif user.is_authenticated and are_friends(user, parent.user):
        files = File.objects.filter(parent_directory=parent, visibility=FileVisibility.FRIENDS | FileVisibility.PUBLIC)
        output_dirs = Directory.objects.filter(parent_directory=parent, visibility=FileVisibility.FRIENDS | FileVisibility.PUBLIC)
    else:
        files = File.objects.filter(parent_directory=parent, visibility=FileVisibility.PUBLIC)
        output_dirs = Directory.objects.filter(parent_directory=parent, visibility=FileVisibility.PUBLIC)
    
    for file in files:
        file.url = file.file.url

    for directory in output_dirs:
        directory.full_path = directory_path + '/' + directory.name

    return render(request, 'files/view.html', {'files': files, 'directories': output_dirs, 'parent': parent, 'path': directory_path, 'parent_dir': parent_dir, 'file_form': file_form, 'directory_form': directory_form, 'owner': parent.user.username, 'user_list': user_list()})

def serve_file(request, file_id):
    file = File.objects.get(id=file_id)
    file_path = file.file.path
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf', as_attachment=False)



def are_friends(user1, user2):
    return Friends.objects.filter(requester=user1, receiver=user2, status=FriendRequestStatus.ACCEPTED) or Friends.objects.filter(requester=user2, receiver=user1, status=FriendRequestStatus.ACCEPTED)

def home(request):
    resp = {
        'files': [],
        'directories': [],
        'parent': None,
        'path': '',
        'parent_dir': '',
        'file_form': FileForm(),
        'directory_form': DirectoryForm(),
        'owner': '',
        'user_list': user_list()
    }

    return render(request, 'files/view.html', resp)