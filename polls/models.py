from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=2500)
    pub_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='polls')

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text
    
class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='votes')