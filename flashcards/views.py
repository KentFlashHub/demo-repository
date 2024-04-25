from django.shortcuts import render, redirect, HttpResponse
from .models import FlashCard
from classes.models import Class
from .forms import FlashCardForm
import random
import csv
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from files.models import File
from social.views import get_friend_status, get_friends


# -------------------------------------------------------------------------------

# get number of cards in evey category
def get_counts(all_cards):
    counts = []
    count_alg = all_cards.filter(category='AI').count()
    counts.append(count_alg)
    count_ds = all_cards.filter(category='ML').count()
    counts.append(count_ds)
    count_com = all_cards.filter(category='Others').count()
    counts.append(count_com)
    return counts

# get n popular/most liked cards
def get_popular_cards(all_cards, n):
    popular_cards = all_cards.order_by('likes')[:n]
    return popular_cards

def get_base_context(request):
    user = request.user
    if user.is_authenticated:
        print("User is authenticated")
        all_cards = FlashCard.objects.filter(creator=user)
        friends = get_friends(user)
    else:
        print("User is not authenticated")
        all_cards = FlashCard.objects.all()
        friends = { 'accepted': [], 'pending': []}
    counts = get_counts(all_cards)
    popular_cards = get_popular_cards(all_cards, 3)
    paginator = Paginator(all_cards, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'counts': counts, 'page_obj': page_obj, 'user_list': user_list(), 'popular_cards': popular_cards, 'pending_friends': friends['pending'], 'accepted_friends': friends['accepted']}

# -------------------------------------------------------------------------------
# home - show all cards 
def home(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
        all_files = File.objects.filter(user=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
        all_files = File.objects.all()
    popular_cards = [i for i in all_cards.order_by('-likes')[:10]]
    files = [i for i in all_files.order_by('-created_at')[:10]]

    for f in files:
        f.type = "file"
        f.url = f.file.url


    for c in popular_cards:
        c.type = "card"

    lst = sorted(files + popular_cards, key=lambda x: random.randint(1,1000), reverse=True)

    context = get_base_context(request)
    context['items'] = lst
    return render(request, 'flashcards/home.html', context)


# get flashcards by a specific category with pagination
def get_cards_by_category(request, category):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    cards = all_cards.filter(category=category)
    paginator = Paginator(cards, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    counts = get_counts(all_cards)
    popular_cards = cards.order_by('-likes')[:3]
    context = get_base_context(request)
    context['popular_cards'] = popular_cards
    context['page_obj'] = page_obj
    context['counts'] = counts
    
    for card in cards:
        card.type = "card"

    context['items'] = cards

    return render(request, 'flashcards/home.html', context)

# add flashcard
@login_required
def add_card(request, course_id):
    if request.method == 'POST':
        form = FlashCardForm(request.POST)
        if form.is_valid():
            new_card = form.save(commit=False)
            new_card.creator = request.user
            new_card.course = Class.objects.get(pk=course_id)
            new_card.save()
            messages.success(request, f'Flashcard added!')
            return redirect('/courses/' + course_id)
    else:
        form = FlashCardForm()
    context = get_base_context(request)
    context['course_id'] = request.GET.get('course_id')
    context['form'] = form
    return render(request, 'flashcards/add_card.html', context)


# edit card
@login_required
def edit_card(request, id):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    card = FlashCard.objects.get(id=id)
    if request.method == 'POST':
        form = FlashCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, f'Flashcard updated!')
            return redirect('home')
    else:
        form = FlashCardForm(instance=card)

    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'form':form, 'counts':counts, 'popular_cards':popular_cards, 'user_list': user_list()}
    return render(request, 'flashcards/edit_card.html', context)

def user_profile(request, username):
    user = User.objects.get(username=username)
    cards = FlashCard.objects.filter(creator=user)
    counts = get_counts(cards)
    popular_cards = cards.order_by('-likes')[:3]
    paginator = Paginator(cards, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    friend_status = get_friend_status(request.user, user)
    context = get_base_context(request)
    context['friend_status'] = friend_status
    context['owner'] = username
    return render(request, 'flashcards/user_profile.html', context)


# search keywords - top 20 results
def search_keywords(request):
    cards = FlashCard.objects.filter(front__contains=request.GET.get('keywords'))[:20]
    paginator = Paginator(cards, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = get_base_context(request)
    context['page_obj'] = page_obj
    context['counts'] = get_counts(FlashCard.objects.filter(front__contains=request.GET.get('keywords')))
    context['popular_cards'] = cards
    return render(request, 'flashcards/home.html', context)


# learn with flashcards
def learn(request, course_id):
    course = Class.objects.get(pk=course_id)
    all_cards = FlashCard.objects.filter(course=course)

    if all_cards.exists():
        card = all_cards.order_by('?').first()
        context = get_base_context(request)
        context['card'] = card
        return render(request, 'flashcards/learn.html', context)
    else:
        messages.info(request, "No cards to learn. Add some cards!")
        return redirect('home')


# mark a card as known
@login_required
def mark_known(request, id):
    referer = request.META.get('HTTP_REFERER')
    rdr = "/".join(referer.split('/')[:6])
    print("Redirecting to:", redirect)
    card = FlashCard.objects.get(id=id)
    card.known = 1
    card.save()
    return redirect(rdr)


# liking a card
def mark_liked(request, id):
    card = FlashCard.objects.get(id=id)
    card.likes += 1
    card.save()
    return redirect('home')


# save and export cards as csv file
def dump_csv(request):
    cards = FlashCard.objects.all()
    response = HttpResponse (content_type='text/csv')
    writer = csv.writer(response)
    response['Content-Disposition'] = 'attachment; filename="flashcards.csv"'
    fieldnames = ['ID', 'Category', 'Front', 'Back', 'Creator', 'Likes', 'Known']
    writer.writerow(fieldnames)
    output = []
    for card in cards:
            output.append([card.id, card.category, card.front, card.back, card.creator, card.likes, card.known])
    writer.writerows(output)

    return response

def user_list():
    users = User.objects.filter(is_staff= False)
    res = [
        {'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'image': f"images/u{random.randint(1, 9)}.png"}
        for user in users
    ]
    return res