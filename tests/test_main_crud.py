from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json

from ..database import Base
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

test_user_id=1
test_user_name = "test1"
test_isbn = 103

chapters = '[{"chapter_name":"Chapter 1","chapter_notes":["test 1","test 2"]},{"chapter_name":"Chapter 2","chapter_notes":["test 3","test 4"]}]'
notes = '["fabulous","amaze"]'
#test_data = '{"notes":'+notes+',"chapters":'+chapters+',"isbn":'+str(test_isbn)+',"owner_id":'+str(test_user_id)+'}'

t2_chapters = '[{"chapter_name":"Chapter 1","chapter_notes":["yoyoy","test 2"]},{"chapter_name":"Chapter 2","chapter_notes":["test 3","test 4"]}]'
t2_notes = '["not amaze","amaze"]'
#test_data = '{"notes":'+notes+',"chapters":'+chapters+',"isbn":'+str(test_isbn)+',"owner_id":'+str(test_user_id)+'}'

#Base practise test
def test_read_hello_world():
    print("--------------------------------")
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
    print("Hello world read successfully")


def test_user_create(user_name = test_user_name,id = test_user_id):
    print("--------------------------------")
    response = client.post(
        "/users/",
        json={"user_name": user_name,"password": "string"},
    )
    assert response.status_code == 200,response.text
    assert response.json() == {"user_name": user_name,"id":id,"is_active": True,"books": []}
    print("Test user created successfully")

def test_read_new_user(user_name = test_user_name, id = test_user_id):
    print("--------------------------------")
    response = client.get("/users/"+str(id), headers={"accept": "application/json"})
    assert response.status_code == 200
    assert response.json() == {
    "user_name": user_name, 
    "id": id,
    "is_active": True,
    "books": []
    }
    print("Test user accessed successfully")

def test_create_book(id = test_user_id,loc_chapters = chapters, loc_notes = notes,loc_isbn = test_isbn):
    print("--------------------------------")
    response = client.post("/users/"+str(id)+"/books/", headers={"accept": "application/json"}, json= {
        "notes":loc_notes,
        "chapters":loc_chapters,
        "isbn":loc_isbn,

    })
    assert response.status_code == 200
    assert response.json() == {
    "notes": loc_notes,
    "owner_id": id,
    "isbn": loc_isbn,
    "chapters": loc_chapters
    }
    print("Book created successfully")

def test_read_book_user(id = test_user_id,loc_chapters = chapters, loc_notes = notes):
    print("--------------------------------")
    response = client.get("/users/"+str(id), headers={"accept": "application/json"})
    assert response.status_code == 200
    data = response.json()

    #Book is returned as a dict, which can then be indexed by notes, owner_id, isbn and chapters
    book = data["books"][0]
    assert book["chapters"] == loc_chapters
    assert book["notes"] == loc_notes
    print("Read test user books successfully")


def test_read_all_books():
    response = client.get("/books/?skip=0&limit=100", headers={"accept": "application/json"})
    assert response.status_code == 200
    data = response.json()

    #Book is returned as a dict, which can then be indexed by notes, owner_id, isbn and chapters
    print("--------------------------------")
    print("Printing all books in database")
    for bk in data:
        print(bk)

    print("--------------------------------")
    book = data[0]
    assert book["chapters"] == chapters
    assert book["notes"] == notes
    print("Read all books successfully")
    print("--------------------------------")

def test_multiple_books_and_users():
    print("--------------------------------")
    print("Creating new user 'test2'")
    test_user_create("test 2",2)
    test_read_new_user("test 2",2)
    test_create_book(2,t2_chapters,t2_notes,802)
    test_read_book_user(2,t2_chapters,t2_notes)
    test_read_all_books()
    print("--------------------------------")