from django.db import models
from files.models import FileType
from django.contrib.auth.models import User

class MessageStatus(models.TextChoices):
    UNREAD = "UNREAD", "Unread"
    READ = "READ", "Read"
    # FAILED = 'FAILED', 'Failed'

class FriendRequestStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"



# Create your models here.
class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author + " : " + self.text


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    object_name = models.CharField(max_length=100, default="helloworld")
    file_type = models.CharField(
        max_length=100, choices=FileType.choices, default=FileType.OTHER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message + " : " + self.file


class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipient", null=True
    )
    status = models.CharField(
        max_length=100, choices=MessageStatus.choices, default=MessageStatus.UNREAD
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.sender + " : " + self.receiver + " : " + self.text


# class GroupMessage(models.Model): # We still need to think about implementation of group messaging.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )

    indexes = [
        models.Index(fields=["author", "message"]),
        models.Index(fields=["author"]),
        models.Index(fields=["message"]),
    ]

    def __str__(self):
        return self.author + " : " + self.message


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000, blank=False, null=False)
    status = models.CharField(
        max_length=100, choices=MessageStatus.choices, default=MessageStatus.UNREAD
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user + " : " + self.message + " : " + self.status
    
class Friends(models.Model):
    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requester"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    status = models.CharField(
        max_length=100,
        choices=FriendRequestStatus.choices,
        default=FriendRequestStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            self.requester.first_name
            + " "
            + self.requester.last_name
            + " - "
            + self.receiver.first_name
            + " "
            + self.receiver.last_name
        )
