from django.db import models
from django.contrib import messages

class Message(models.Model):

    level = models.CharField(max_length=7)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False, db_index=True)

    def display(self, request):
        if self.level == 'success':
            messages.success(request, self.message)
        elif self.level == 'info':
            messages.info(request, self.message)
        elif self.level == 'error':
            messages.error(request, self.message)
        else:
            raise Exception('Not implemented')
        self.read = True
        self.save()
    
    @classmethod
    def success(cls, msg):
        cls.objects.create(message=msg, level='success', read=False)

    @classmethod
    def info(cls, msg):
        cls.objects.create(message=msg, level='info', read=False)        
    
    @classmethod
    def error(cls, msg):
        cls.objects.create(message=msg, level='error', read=False)

    
