## SuperQA - Question Answering Bot

API that answers a list of questions according to given source file (PDF/JSON).

### Dev Setup
- Using Python 3.9.6, create venv and activate it.
```
python3 -m venv .venv
source .venv/bin/activate
```
- Install dependencies
```
pip install -r requirements.txt`
```
- For code formatting run 
```
black app tests
```
- To run tests 
```
pytest
```

### Manage dependencies
- Freeze dependencies
```
pip freeze > requirements.txt
```


### How to run app?
- Create `.env` file similar to `.env.sample`
- Run command
```
uvicorn app.main:app --reload --log-config logging.yaml
```
- Swagger UI http://127.0.0.1:8000/docs


### Sample Query 1 : JSON Source File
Input:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/answer' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'source_file=@samples/e1source.json;type=application/json' \
  -F 'question_file=@samples/e1questions.json;type=application/json'
```

Output:
```
{"When do employees get time off?":"Employees get time off to vote.","How many times do we conduct Incident Response Program?":"The Incident Response Program is conducted at least once a year."}
```

### Sample Query 2 : PDF Source File

Input:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/answer' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'source_file=@samples/e2source.pdf;type=application/pdf' \
  -F 'question_file=@samples/e2questions.json;type=application/json'
```
Output:
```
{
"What is the page count?":"The page count is not specified in the given context.",
"What is this text about?":"The text is about a simple PDF file that is being used for demonstration purposes in Virtual Mechanics tutorials."
}%
```