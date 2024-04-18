from django.db import models
from django.contrib.auth.models import User


class FileOrDirectory(models.TextChoices):
    FILE = "FILE", "File"
    DIRECTORY = "DIRECTORY", "Directory"


class FileType(models.TextChoices):
    PDF = "PDF", "pdf"
    DOC = "DOC", "doc"
    DOCX = "DOCX", "docx"
    PPT = "PPT", "ppt"
    PPTX = "PPTX", "pptx"
    XLS = "XLS", "xls"
    XLSX = "XLSX", "xlsx"
    TXT = "TXT", "txt"
    ZIP = "ZIP", "zip"
    JPG = "JPG", "jpg"
    JPEG = "JPEG", "jpeg"
    PNG = "PNG", "png"
    GIF = "GIF", "gif"
    MP4 = "MP4", "mp4"
    MOV = "MOV", "mov"
    AVI = "AVI", "avi"
    MKV = "MKV", "mkv"
    MP3 = "MP3", "mp3"
    WAV = "WAV", "wav"
    FLAC = "FLAC", "flac"
    OGG = "OGG", "ogg"
    FLASHCARD = "FLASHCARD", "flashcard"
    OTHER = "OTHER", "other"


class FileVisibility(models.TextChoices):
    PUBLIC = "PUBLIC", "Public"
    PRIVATE = "PRIVATE", "Private"
    FRIENDS = "FRIENDS", "Friends"


class Directory(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_directory = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    visibility = models.CharField(
        max_length=100, choices=FileVisibility.choices, default=FileVisibility.PUBLIC
    )

    indexes = [
        models.Index(fields=["user", "parent_directory"]),
        models.Index(fields=["parent_directory"]),
    ]

    def __str__(self):
        return self.name


# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=100)
    file_type = models.CharField(
        max_length=100, choices=FileType.choices, default=FileType.OTHER
    )
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_directory = models.ForeignKey(
        Directory, on_delete=models.CASCADE, blank=True, null=True
    )
    visibility = models.CharField(
        max_length=100, choices=FileVisibility.choices, default=FileVisibility.PUBLIC
    )

    indexes = [
        models.Index(fields=["user", "parent_directory"]),
        models.Index(fields=["parent_directory"]),
        models.Index(
            fields=[
                "user",
                "object_name",
            ]
        ),
        models.Index(fields=["user", "object_name", "parent_directory"]),
        models.Index(fields=["object_name"]),
    ]

    def __str__(self):
        return self.name
    
    def get_file_type(file_name:str):
        file_name = file_name.lower()
        if file_name.endswith('.pdf'):
            return FileType.PDF
        elif file_name.endswith('.doc'):
            return FileType.DOC
        elif file_name.endswith('.docx'):
            return FileType.DOCX
        elif file_name.endswith('.ppt'):
            return FileType.PPT
        elif file_name.endswith('.pptx'):
            return FileType.PPTX
        elif file_name.endswith('.xls'):
            return FileType.XLS
        elif file_name.endswith('.xlsx'):
            return FileType.XLSX
        elif file_name.endswith('.txt'):
            return FileType.TXT
        elif file_name.endswith('.zip'):
            return FileType.ZIP
        elif file_name.endswith('.jpg'):
            return FileType.JPG
        elif file_name.endswith('.jpeg'):
            return FileType.JPEG
        elif file_name.endswith('.png'):
            return FileType.PNG
        elif file_name.endswith('.gif'):
            return FileType.GIF
        elif file_name.endswith('.mp4'):
            return FileType.MP4
        elif file_name.endswith('.mov'):
            return FileType.MOV
        elif file_name.endswith('.avi'):
            return FileType.AVI
        elif file_name.endswith('.mkv'):
            return FileType.MKV
        elif file_name.endswith('.mp3'):
            return FileType.MP3
        elif file_name.endswith('.wav'):
            return FileType.WAV
        elif file_name.endswith('.flac'):
            return FileType.FLAC
        elif file_name.endswith('.ogg'):
            return FileType.OGG
        else:
            return FileType.OTHER