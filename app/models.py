from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Forms(models.Model):
    # form_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    email = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.CharField(max_length=255, blank=True)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
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
    # mandatory = models.BooleanField(default=False)
    metadata = JSONField()
class Choice(models.Model):
    choice_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Questions, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

class Responses(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, related_name="responses")
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    metadata = JSONField()

class Answers(models.Model):
    response = models.ForeignKey(Responses, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_text  = models.TextField()
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    metadata = JSONField()