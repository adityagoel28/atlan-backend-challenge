# atlan-backend-challenge
# Data Collection Platform with SMS Notification Feature
This repository contains the code for a data collection platform that also has an SMS notification feature.

## Tools and Technologies Used :computer:
- Python (Django)
- AWS (S3, SQS, Lambda)
- Postman
- Twilio
- Docker

## Consistency and Scalability :rocket:
```Eventual consistency is what the clients expect as an outcome of this feature, making sure no responses get missed in the journey. Do keep in mind that this solution must be failsafe, should eventually recover from circumstances like power/internet/service outages, and should scale to cases like millions of responses across hundreds of forms for an organization```

My first approach to handle Scalability at Millions of requests, was to use AWS Lambda (Serverless) as a event based architecture to give response.
This approach is great in itself because it provides continuous scaling for huge number of requests.

### 2nd Approach
Amazon Simple Queue Service (SQS) is a fully managed message queuing service that enables us to decouple and scale microservices, distributed systems, and serverless applications.

In this approach, SQS can act as a buffer and rate limiter for our Lambda function. Instead of directly triggering the Lambda function upon S3 upload, I can send a message to SQS. Then, the Lambda function can be triggered by SQS to process the file. This can help to prevent the Lambda function from getting overwhelmed with too many requests at once, especially when there is huge records in the file or many files are uploaded to S3 at the same time.

To handle failsafe, we can use AWS SQS (i.e. Message queue) where if the Lambda can have 3 retries for a request and even then if the Lambda fails to process the request, we can drop it to a "Dead Queue" to check later manually.


### Task - 1 ✅
```One of the clients wanted to search for slangs (in local language) for an answer to a text question on the basis of cities (which was the answer to a different MCQ question)```

```
class Forms(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    email = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    metadata = JSONField()
```

```
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
```

```
class Choice(models.Model):
    choice_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Questions, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
```


```
class Responses(models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, related_name="responses")
    submitted_at = models.DateTimeField(auto_now_add=True)
    metadata = JSONField()
```

```
class Answers(models.Model):
    response = models.ForeignKey(Responses, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer_text  = models.TextField()
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    metadata = JSONField()
```

## Schema Design

The schema provided here supports data collection using forms, and manages form definitions, questions, responses, and answers.

### Model Descriptions
#### Forms Model
The Forms model defines a form to be filled out. Each form has a title, description, email, created_at, updated_at and metadata fields. The metadata field is a JSONField that can be used to store any additional, form-specific information in JSON format.

#### Questions Model
The Questions model defines the individual questions within a form. Each question is associated with a form through a foreign key relationship to the Forms model. A question has a question_text, question_type, and metadata. The question_type can be either 'Text' or 'Multiple Choice', and the metadata field is a JSONField that can store any additional question-specific information in JSON format.

#### Choice Model
The Choice model defines the choices for multiple choice questions. Each choice is associated with a Questions model through a foreign key relationship. Each choice has a choice_text which is the text of the choice.

#### Responses Model
The Responses model captures the responses to a form. Each response is associated with a form through a foreign key relationship to the Forms model. Each response has a submitted_at timestamp and a metadata field that can store any additional response-specific information in JSON format.

#### Answers Model
The Answers model captures the individual answers within a response. Each answer is associated with a Responses model and a Questions model through foreign key relationships. If the question is a text question, the answer is stored in answer_text. If the question is a multiple choice question, the selected choice is stored in selected_choice, which is a foreign key field pointing to the Choice model. Each answer also has a submitted_at timestamp and a metadata field that can store any additional answer-specific information in JSON format.

### Usage
This schema design enables handling forms, their questions (both text and multiple choice), and the responses and individual answers to those forms. It supports flexible data collection, and the JSONField in each model allows for storing additional information specific to forms, questions, responses, and answers.


### Task - 2 ✅
```A market research agency wanted to validate responses coming in against a set of business rules (eg. monthly savings cannot be more than monthly income) and send the response back to the data collector to fix it when the rules generate a flag.```

![image](https://github.com/adityagoel28/atlan-backend-challenge/assets/67872867/fafcd5fa-6eb9-4ff7-88b0-17f45c9bdb51)

### AWS Architecture
![image](https://github.com/adityagoel28/atlan-backend-challenge/assets/67872867/bd6c2c1f-2d79-4ea4-b6d2-c80f12de59d9)


### Task - 3 ✅
```A very common need for organizations is wanting all their data onto Google Sheets, wherein they could connect their CRM, and also generate graphs and charts offered by Sheets out of the box. In such cases, each response to the form becomes a row in the sheet, and questions in the form become columns.```

### Data in the sheet
![image](https://github.com/adityagoel28/atlan-backend-challenge/assets/67872867/c804159b-c446-4aa8-b47c-70d7f50afcd5)


### Task - 4 ✅
```A recent client partner wanted us to send an SMS to the customer whose details are collected in the response as soon as the ingestion was complete reliably. The content of the SMS consists of details of the customer, which were a part of the answers in the response. This customer was supposed to use this as a “receipt” for them having participated in the exercise.```

## Sending response via API endpoint from Postman
![image](https://github.com/adityagoel28/atlan-backend-challenge/assets/67872867/c7a1104a-2123-465f-9c89-b2a27f450d69)

## Message received after submitting the response via Twilio
![WhatsApp Image 2023-07-31 at 09 01 40](https://github.com/adityagoel28/atlan-backend-challenge/assets/67872867/8b165d4d-e71f-4f43-8971-a3823c8e8f50)

I have used Twilio, a cloud communications platform, for the SMS feature. Twilio's APIs enable us to send SMS messages globally and reliably.
This is one of the unique features - the ability to send an SMS to the customer whose details are collected in the response as soon as the ingestion is complete reliably. The content of the SMS consists of details of the customer, which were a part of the answers in the response. This allows the customer to use the SMS as a “receipt” for their participation in the exercise.
