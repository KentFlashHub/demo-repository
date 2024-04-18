from django.shortcuts import redirect
from .models import Friends, FriendRequestStatus
from django.contrib.auth.models import User

# Create your views here.
def get_friend_status(user, friend):
    friendship = list(Friends.objects.filter(requester=user, receiver=friend)) + list(Friends.objects.filter(requester=friend, receiver=user))
    if user == friend:
        return 'accepted'
    switcher = {
        FriendRequestStatus.ACCEPTED: 'accepted',
        FriendRequestStatus.PENDING: 'pending',
        FriendRequestStatus.REJECTED: 'rejected'
    }
    if friendship:
        return switcher[friendship[0].status]
    return None
    
def request_friendship(request, friend_name):
    friend = User.objects.get(username=friend_name)
    referer = request.META.get('HTTP_REFERER')
    if friend == request.user:
        return redirect(referer)
    friendship = list(Friends.objects.filter(requester=friend, receiver=request.user)) + list(Friends.objects.filter(requester=request.user, receiver=friend))
    if not friendship:
        Friends.objects.create(requester=request.user, receiver=friend)
    return redirect(referer)

def respond_to_friend_request(request, friend_name, status):
    friend = User.objects.get(username=friend_name)
    referer = request.META.get('HTTP_REFERER')
    if status == 'remove':
        Friends.objects.filter(requester=friend, receiver=request.user).delete()
        Friends.objects.filter(requester=request.user, receiver=friend).delete()
        return redirect(referer)
    friendship = Friends.objects.filter(requester=friend, receiver=request.user)
    if friendship.exists():
        friendship = friendship[0]
        switcher = {
            'accept': FriendRequestStatus.ACCEPTED,
            'reject': FriendRequestStatus.REJECTED
        }
        friendship.status = switcher[status]
        friendship.save()
    return redirect(referer)

def get_friends(user):
    return {
        'accepted': [User.objects.get(id=f.receiver.id) for f in Friends.objects.filter(requester=user, status=FriendRequestStatus.ACCEPTED)] + [User.objects.get(id=f.requester.id) for f in Friends.objects.filter(receiver=user, status=FriendRequestStatus.ACCEPTED)],
        'pending': [User.objects.get(id=f.requester.id) for f in Friends.objects.filter(receiver=user, status=FriendRequestStatus.PENDING)]
    }