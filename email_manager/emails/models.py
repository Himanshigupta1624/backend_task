from django.db import models

class Subscriber(models.Model):
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    

class Campaign(models.Model):
    subject=models.CharField(max_length=200)
    preview_text=models.TextField()
    article_url=models.URLField()
    html_content=models.TextField()
    plain_text_content=models.TextField()
    published_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject    
