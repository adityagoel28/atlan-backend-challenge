# atlan-backend-challenge
Atlan Backend Challenge

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
