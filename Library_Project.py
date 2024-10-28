# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 21:07:02 2024

@author: ltngu
"""

import sqlite3
import os
import sys
import time
from datetime import datetime, timedelta

class Color:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = '\033[0m'
    
    @staticmethod
    def color_text(text: str, color: str) -> str:
        return f"{color}{text}{Color.RESET}"
    
def timer(f):
    """
    Wrapper function for excution time

    Parameters
    ----------
    f : TYPE
        Function

    Returns
    -------
    TYPE
        Function return

    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        stop_time = time.time()
        time_delta = stop_time - start_time
        
        print(Color.color_text(f'Time Delta = {time_delta:.4f} seconds for [{f.__name__}]', Color.CYAN))
        return result
    return wrapper

@timer
def create_database(path: str) -> bool:
    """
    Create a sqlite database name library.db at current directory.
    Then create a table name books
    Then Create 10 dummy records 
    Then return True if table is successfully created
    
    Parameters
    -------
    path : str
        The database path
        
    Returns
    -------
    bool: 
        success or fail to create database
    """
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                Book_ID TEXT PRIMARY KEY,
                Title TEXT, 
                Author TEXT, 
                Borrowers TEXT, 
                Status REAL, 
                Due_Date REAL
            )
        ''')
        connection.commit()
        print('Table Created')

        books_list = [
            ('1', 'Test Book', 'Loi Nguyen', 'Loi Nguyen B', 1.0, datetime.now().timestamp()),
            ('2', 'Book 2', 'Author 2', 'Borrower 2', 0.0, datetime(2024, 2, 2).timestamp()),
            ('3', 'Book 3', 'Author 3', 'Borrower 3', 1.0, datetime(2024, 3, 3).timestamp()),
            ('4', 'Book 4', 'Author 4', 'Borrower 4', 1.0, datetime(2024, 4, 4).timestamp()),
            ('5', 'Book 5', 'Author 5', 'Borrower 5', 0.0, datetime(2024, 5, 5).timestamp()),
            ('6', 'Book 6', 'Author 6', 'Borrower 6', 1.0, datetime(2024, 6, 6).timestamp()),
            ('7', 'Book 7', 'Author 7', 'Borrower 7', 0.0, datetime(2024, 7, 7).timestamp()),
            ('8', 'Book 8', 'Author 8', 'Borrower 8', 0.0, datetime(2024, 8, 8).timestamp()),
            ('9', 'Book 9', 'Author 2', 'Borrower 9', 1.0, datetime(2024, 9, 9).timestamp()),
            ('10', 'Final Book', 'Author 10', 'Borrower 10', 1.0, datetime(2024, 10, 10).timestamp()),
        ]
        
        query = '''
            INSERT INTO books (Book_ID, Title, Author, Borrowers, Status, Due_Date) 
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor.executemany(query, books_list)
        connection.commit()
        print("records inserted")
        return True
    except sqlite3.Error as e:
        print(Color.color_text(f'Error occurred: {e}', Color.RED))
        return False
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
@timer         
def print_all_records(path: str):
    """
    Display all book

    Parameters
    ----------
    path : str
        The database path

    Returns
    -------
    None.

    """
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    try:
        query = 'SELECT * FROM books'
        book_data = cursor.execute(query)
        _print_book_list(book_data)
    except sqlite3.Error as e:
        print(Color.color_text(f'Error occurred: {e}', Color.RED))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@timer
def search_books(path: str, status: int):
    """
    Search the database for all records with the Status value of status

    Parameters
    ----------
    path : str
        The database path
    status : int
        The Status value for the search 

    Returns
    -------
    None.

    """
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    try:
        query = 'SELECT * FROM books WHERE Status=?'
        param = [status]
        book_data = cursor.execute(query, param)
        _print_book_list(book_data)
    except sqlite3.Error as e:
        print(Color.color_text(f'Error occurred: {e}', Color.RED))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
@timer
def print_all_records_sorted(path: str):
    """
    Display all book in Status descending order and Due_Date Descending order

    Parameters
    ----------
    path : str
        The database path

    Returns
    -------
    None.

    """
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    try:
        query = 'SELECT * FROM books ORDER BY Status DESC, Due_Date DESC'
        book_data = cursor.execute(query)
        _print_book_list(book_data)
    except sqlite3.Error as e:
        print(Color.color_text(f'Error occurred: {e}', Color.RED))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@timer
def update_book(path: str, book_id: str, checkin: int):
    """
    Find the the book with the given book id and update the status code if it is different from the database.
    Will also update the Due date by two week from current day if the user is checking the book out

    Parameters
    ----------
    path : str
        The database path
    book_id : str
        The book in
    checkin : int
        The status code

    Returns
    -------
    None.

    """
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    try:
        get_book_query = 'SELECT Status, Due_Date, Title FROM books WHERE Book_ID=?'
        get_book_param = [book_id]
        book_data = cursor.execute(get_book_query, get_book_param).fetchone()
        
        if book_data is None:
            print(f'No Book found with the ID "{book_id}"')
            return
        if book_data[0] == checkin == 1:
            print(Color.color_text(f'The book "{book_data[2]}" is already checked in', Color.MAGENTA))
            return
        if book_data[0] == checkin == 0:
            print(Color.color_text(f'The book "{book_data[2]}" is still checked out with the due date {datetime.fromtimestamp(book_data[1]).date()}', Color.MAGENTA))
            return

        update_book_query = 'UPDATE books SET'
        update_book_params = []
        updates = []
        print_string = f'Book "{book_data[2]}" successfully checked'
        
        updates.append(' Status = ?')
        update_book_params.append(checkin)
        if checkin == 0:
            current_datetime = datetime.now()
            new_due_date = current_datetime + timedelta(weeks=2)
            updates.append(' Due_Date = ?')
            update_book_params.append(new_due_date.timestamp())
            print_string += f' out with the new due date {new_due_date.date()}'
        else: 
            print_string += ' in'
        
        update_book_query += ', '.join(updates) + ' WHERE Book_ID = ?'
        update_book_params.append(book_id)
        
        cursor.execute(update_book_query, update_book_params)
        connection.commit()

        print(Color.color_text(print_string, Color.GREEN))
        
    except sqlite3.Error as e:
        print(Color.color_text(f'Error occurred: {e}', Color.RED))
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def _print_book_list(book_data):
    """
    Helper Function for printing list of book

    Parameters
    ----------
    book_data : TYPE
        List of book from sql

    Returns
    -------
    None.

    """
    for book in book_data:
        print(f'{book[0]}, {book[1]}, {book[2]}, {book[3]}, {book[4]}, {datetime.fromtimestamp(book[5])}')
"""
NOTES:
    Will create a sqlite database name library.db at which ever location this .py file is located at
    Add or Remove the timer decorator to see or remove timestamp
"""
if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lib_path = dir_path + "\library.db"
    if not (os.path.isfile(lib_path)):
        if not create_database(lib_path): 
            sys.exit("Failed to create the database.")
    
    while True:
        print('\nMenu:')
        print('1. View List of Book')
        print('2. View List of Books Order by Status and Due Date')
        print('3. View List of Books by Their Status')
        print('4. Update Book Status')
        print('5. Exit')
        
        choice = input('Select an option (1-5): ').strip()
        print()
        if choice == '1':
            print_all_records(lib_path)
        elif choice == '2':
            print_all_records_sorted(lib_path)
        elif choice == '3':
            choice_flag = True
            status = ''
            while choice_flag:
                status = input('Enter new Status(1 for check in, 0 for checkout, Exit to return to menu): ').strip()
                if status.lower() == 'exit':
                    choice_flag = False
                    continue
                if status not in ['0', '1']:
                    print(Color.color_text('Invalid Status. Please select a valid option', Color.MAGENTA))
                    continue
                choice_flag = False
            if status != 'exit':
                search_books(lib_path, status)
            
        elif choice == '4':
            choice_flag = True
            book_id = input('Enter Book ID to update: ').strip()
            status = ''
            while choice_flag:
                status = input('Enter new Status(1 for check in, 0 for checkout, Exit to return to menu): ').strip()
                if status.lower() == 'exit':
                    choice_flag = False
                    continue
                if status not in ['0', '1']:
                    print(Color.color_text('Invalid Status. Please select a valid option', Color.MAGENTA))
                    continue
                choice_flag = False
            
            if status != 'exit': 
                update_book(lib_path, book_id, int(status))
        elif choice == '5':
            print("End the program")
            break
        else:
            print(Color.color_text('Invalid Choice. Please select a valid option', Color.MAGENTA))
        
