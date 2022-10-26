from typing import Optional
from enum import Enum
from fastapi import FastAPI

app = FastAPI()


BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}

class DirectionName(str,Enum):
    north='North'
    south="South"
    east='East'
    west='West'


# @app.get("/")
# async def get_book_list():
#     return BOOKS



@app.get("/")
async def get_book_list(skip_book:Optional[str]=None):#="book_3"): #if default value is not set, then input required
    new_books=BOOKS.copy()
    if skip_book:
        
        del new_books[skip_book]
    return new_books

@app.get("/books/mybook")
def get_fav_book(): # will fail if defined after "read book" func
    return {'book':'My Favourite book'}

@app.get("/books/{book_id}")
async def read_book(book_id : int):
    return {'book':"book_"+str(book_id),'details':BOOKS["book_"+str(book_id)]}

@app.get("/directions/{direction_name}")
async def get_directions(direction_name : DirectionName):
    if direction_name ==DirectionName.north:
        return {'direction':direction_name,"sub":'up'}
    elif direction_name ==DirectionName.south:
        return {'direction':direction_name,"sub":'down'}
    elif direction_name ==DirectionName.east:
        return {'direction':direction_name,"sub":'right'}
    return {'direction':direction_name,"sub":'left'}



# Post
@app.post("/")
async def create_book(book_title,book_author):
    current_book_id=0
    if len(BOOKS)>0:
        for book in BOOKS:
            x=int(book.split("_")[-1])
            if x>current_book_id:
                current_book_id=x

    BOOKS[f"book_{current_book_id+1}"]={'title':book_title, 'author': book_author}
    return BOOKS[f"book_{current_book_id+1}"]
        

@app.put("/{book_name}")
async def update_book(book_name:str,book_title:str,book_author:str):
    book_info={'title':book_title, 'author':book_author}
    BOOKS[book_name]=book_info
    return book_info


@app.delete("/{book_name}")
async def delete_book(book_name):
    del BOOKS[book_name]
    return f"book {book_name} deleted"



@app.get("/assignment/") # from query rather than path
async def read_book_assignment(book_id : int):
    return {'book':"book_"+str(book_id),'details':BOOKS["book_"+str(book_id)]}
