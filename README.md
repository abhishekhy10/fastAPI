# MongoDB with FastAPI CRUD APP Boilerplate

This is a small sample project demonstrating how to build an API with [MongoDB](https://developer.mongodb.com/) and [FastAPI](https://fastapi.tiangolo.com/).

## TL;DR

create virtual environment 'env'
```python -m venv env```
activate your Python virtualenv, and then run the following from your terminal (edit the `MONGODB_URL` first!):

```bash
# Install the requirements:
pip install -r requirements.txt

# Start the service:
uvicorn main:app --reload
```

Now you can load http://localhost:8000/docs in your browser.