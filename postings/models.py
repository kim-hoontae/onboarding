from django.db import models

class Posting(models.Model): 
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'postings'