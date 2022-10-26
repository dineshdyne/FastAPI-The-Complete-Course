from typing import Optional
from enum import Enum
from fastapi import FastAPI, HTTPException,Request,status,Form,Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse

app = FastAPI()

class NegativeNumberException(Exception):
    def __init__(self,books_to_return):
        self.books_to_return =books_to_return


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(
        title="Description of book",
        max_length=100,
        min_length=1
    )
    volume: Optional[str]
    rating: int = Field(ge=1, lt=10)

    class Config:
        schema_extra = {
            "example": {
                "id": "59e2f912-c2ce-4069-b043-3a758767d157",
                "title": "book tile entered 1",
                "author": "bkyucsgmndg",
                "description": "deghjvfsxghf",
                "rating": 6
            }
        }

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str= Field(min_length=1,max_length=100)
    description: Optional[str] = Field(None,
        title="Description of book",
        max_length=100,
        min_length=1
    )
    volume: Optional[str]
    #rating: int = Field(ge=1, lt=10)




BOOKS = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request,exception:NegativeNumberException):
    return JSONResponse(status_code=418,content={'message':f'Why do you want {exception.books_to_return} of books?'})


@app.post("/books/login")
async def book_login(username:str=Form(), password:str=Form(),):
    return {'username':username, 'password':password}


@app.post("/books/login/")
async def book_login(book_id:int,username:Optional[str]=Header(None), password:Optional[str]=Header(None),):
    if username=='FastAPIUser' and password=='test1234':
        return BOOKS[book_id]
    return "Invalid User"

@app.get("/headers") # headers
async def read_header(random_header: Optional[str]=Header(None)):
    return {'Random-Header':random_header}


@app.get("/")
async def read_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return<0:
        raise NegativeNumberException(books_to_return)

    if len(BOOKS) < 1:
        create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books

    return BOOKS


@app.get("/book/{book_id}")
async def get_book_by_id(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.get("/book/rating/{book_id}",response_model=BookNoRating) #fast api  validated the output  to the response model class
async def get_book_no_rating_by_id(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter-1] = book
            return BOOKS[counter-1]
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter-1]
            return book_id
    raise raise_item_cannot_be_found_exception()

def create_books_no_api():
    book_1 = Book(id="59e2f912-c2ce-4069-b043-3a758767d157", title="book tile entered 1",
                  author="bkyucsgmndg", description="deghjvfsxghf", rating=6)
    book_2 = Book(id="69e2f912-c2ce-4069-b043-3a758767d157", title="book tile entered 2",
                  author="dsfjhbfdcv", description="qewjgfvds", rating=8)
    book_3 = Book(id="79e2f912-c2ce-4069-b043-3a758767d157", title="book tile entered 3",
                  author="dfgvfdxd ", description="edghmcs", rating=4)
    book_4 = Book(id="89e2f912-c2ce-4069-b043-3a758767d157", title="book tile entered 4",
                  author="dfsgnbv", description="dstghvdsvc", rating=9)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)

def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail="Book not found", headers={
                        'X-Header-Error': "Nothing to be seen at the UUID"})
