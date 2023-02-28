from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=255)


class Library(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    bucket = models.CharField(max_length=255)


class File(models.Model):
    name = models.CharField(max_length=255)
    library = models.ForeignKey("Library", on_delete=models.CASCADE)
    creation_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'library'], name='pk'
            )
        ]
