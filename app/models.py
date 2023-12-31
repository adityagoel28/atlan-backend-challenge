from django.db import models
from django.db.models import JSONField

# Create your models here.
class Forms(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    email = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = JSONField()

class Questions(models.Model):
    QUESTION_TYPES  = [
        ('text', 'Text'),
        ('mcq', 'Multiple Choice'),
    ]

    form = models.ForeignKey(Forms, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=100, choices=QUESTION_TYPES, default='text')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = JSONField()

class Choice(models.Model):
    choice_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Questions, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

class Responses(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, related_name="responses")
    submitted_at = models.DateTimeField(auto_now_add=True)
    metadata = JSONField()

class Answers(models.Model):
    response = models.ForeignKey(Responses, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_text  = models.TextField()
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    metadata = JSONField()

class Clients(models.Model):
    client_email = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    income_per_annum = models.FloatField()
    savings_per_annum = models.FloatField()
    mobile_number = models.CharField(max_length=15)