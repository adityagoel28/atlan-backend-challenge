from django.db import models

# Create your models here.
class Forms(models.Model):
    title = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)

class Questions(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=255)
    mandatory = models.BooleanField(default=False)

class Responses(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, related_name="responses")

class Answers(models.Model):
    response = models.ForeignKey(Responses, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    text = models.TextField()
