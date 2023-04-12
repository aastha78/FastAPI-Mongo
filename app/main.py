from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, validator, constr
from datetime import datetime
# export MONGODB_URL="mongodb+srv://aasthavashist78:Qwertyuiop567@@cluster0.ij8wbul.mongodb.net/?retryWrites=true&w=majority"
app = FastAPI()

# Connect to the MongoDB server and database
client = MongoClient('mongodb://localhost:27017')
db = client['mydatabase']
collection = db['mycollection']


# Define a model for the data
class Todo(BaseModel):
    name: str
    age: int
    email: constr(regex=r"[^@]+@[^@]+\.[^@]+")
    gender: str
    mobile_number: constr(min_length=10, max_length=10)
    birthday: str
    city: str
    state: str
    country: str
    address1: str
    address2: str

    # Add validators to check the request payload
    @validator('birthday')
    def validate_birthday(cls, value):
        try:
            datetime.strptime(value, '%d-%m-%Y')
        except ValueError:
            raise ValueError('Incorrect date format, should be DD-MM-YYYY')
        return value
    
    @validator('age')
    def validate_age(cls, value):
        if value < 18:
            raise ValueError('Age should be greater than 18')
        return value

# Define the CRUD endpoints

@app.post('/todos')
def create(todo: Todo):
    # Insert a new document into the collection
    result = collection.insert_one(todo.__dict__)
    # Return the ID of the newly created document
    return {'id': str(result.inserted_id)}

@app.get('/todos/{todo_id}')
def read(todo_id: str):
    # Find the document with the specified ID
    todo = collection.find_one({'_id': ObjectId(todo_id)})
    if todo:
        # Create a Todo object from the document and return it
        return Todo(**todo)
    else:
        # Return a 404 error if the document is not found
        raise HTTPException(status_code=404, detail="Todo not found")


@app.put('/todos/{todo_id}')
def update(todo_id: str, todo: Todo):
    # Update the document with the specified ID
    collection.update_one({'_id': ObjectId(todo_id)}, {'$set': todo.__dict__})
    print(todo.__dict__)
    # Return a success message
    return {'message': 'Todo updated successfully'}

@app.delete('/todos/{todo_id}')
def delete(todo_id: str):
    # Delete the document with the specified ID
    collection.delete_one({'_id': ObjectId(todo_id)})
    # Return a success message
    return {'message': 'Todo deleted successfully'}
