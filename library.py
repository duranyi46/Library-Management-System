import pandas as pd
# If you get an error for opening booksdb.csv, get the location of the file below here.
df = pd.read_csv("booksdb.csv", nrows=2000)
#
df.rename(columns={"  num_pages": "book_number_of_pages"}, inplace=True)
df.rename(columns={"title": "book_name"}, inplace=True)
df.rename(columns={"authors": "book_author"}, inplace=True)
df.rename(columns={"publication_date": "book_release_date"}, inplace=True)

df_books = df[["book_name","book_author","book_release_date","book_number_of_pages"]]

df_books.to_csv("books.txt", index=False, sep=",")

class Library:
    def __init__(self):
        self.file = open("books.txt", "a+", encoding="utf-8")
    def __del__(self):
        self.file.close()
    
    def list_book(self):
        choice = input("Would you like to see full information about the books?\n(For only Book name and Author, type No)  ")
        self.file.seek(0)
        book_shelf = self.file.read().splitlines()
        for each_line in book_shelf:
            info = each_line.split(',')  
            if len(info) == 4:
                book_name, book_author, book_release_date, book_number_of_pages = info
                if choice.lower() == "no":
                    print("Book Name: ", book_name, "       Author: ", book_author) 
                elif choice.lower() == "yes":
                    print("Book Name: ", book_name, "       Author: ", book_author, "       Release Date: ", book_release_date,  "       Number of Pages: ", book_number_of_pages)
                else:
                    print("Invalid answer. Try again.")
        
    def add_book(self):
        book_name = input("Book name: ")
        book_author = input("Author :")
        book_release_date = input("Release Date: ")
        book_number_of_pages = input("Number of pages: ")
        info = f"{book_name},{book_author},{book_release_date},{book_number_of_pages}\n"
        print('Book added.')
        self.file.write(info)
        
    def remove_book(self):
        remove_book_name = input("Book Name: ")
        self.file.seek(0)
        book_shelf = self.file.read().splitlines()

        remove_book_index = None

        for index, each_line in enumerate(book_shelf):
            info = each_line.split(',')
            if len(info) == 4:
                book_name, book_author, book_release_date, book_number_of_pages = info
                if book_name == remove_book_name:
                    remove_book_index = index
                    break

        if remove_book_index is not None:
            book_shelf.pop(remove_book_index)
            self.file.seek(0)
            self.file.truncate()
            for each_line in book_shelf:
                self.file.write(each_line + "\n")
            print("Book removed.")
        else:
            print("Book not found.")
        
    def find_book(self):
        book_to_find = input("Book name: ").strip()
        self.file.seek(0)
        book_shelf = self.file.read().splitlines()
        for each_line in book_shelf:
            info = each_line.split(',')  
            if len(info) == 4:
                book_name, book_author, book_release_date, book_number_of_pages = info
                if book_name.lower() == book_to_find.lower():
                    print("Book found.")
                    print(info)
                    break
        else:
            print('Book not found.')

# This feature uses a DataFrame which contains some columns booksdb.csv as database. It can recommend you a book randomly according to your rating interval preference.
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
df.rename(columns={"bookID": "book_ID"}, inplace=True)
df.rename(columns={"average_rating": "book_average_rating"}, inplace=True)

df_books = df[['book_ID','book_name','book_author','book_release_date','book_number_of_pages','book_average_rating']]    
df_books['book_release_date'] = pd.to_datetime(df_books['book_release_date']).dt.year
lib = Library()
while True:
    print(" *** MENU***")
    print("1) List Books")
    print("2) Find Book")
    print("3) Add Book")
    print("4) Remove Book")
    print('5) Recommend me!(Beta)')
    print('6) Library insights')
    print("7) Exit")
    choice_move = input("Select an option: ")
    
    if choice_move == "1":
        lib.list_book()
    elif choice_move == "2":
        lib.find_book()
    elif choice_move == "3":
        lib.add_book()
    elif choice_move == "4":
        lib.remove_book()
    elif choice_move == '5':
        print(" *** RECOMMEND MENU ***")
        print('1) Based on rating')
        print('2) Based on author')
        print('3) Based on release year')
        
        beta_choice = input("Select an option :")
        if beta_choice == '1':
            min_rating = float(input('What would be the minimum rating of your book?'))
            max_rating = float(input('What would be the maximum rating of your book?'))
            conditioned_df = df_books[(df_books['book_average_rating'] <= max_rating) & (df_books['book_average_rating'] >= min_rating)]
            if conditioned_df.empty == False:
                sample_row = conditioned_df.sample(3, replace=False)
                print(sample_row)
            else:
                print('Library does not have a book which has rating in that inretval.')
        elif beta_choice == '2':
            author_name = input('Author: ')    
            conditioned_df = df_books[df_books['book_author'] == author_name]
            if conditioned_df.empty == False:
                sample_row = conditioned_df.sample(3, replace=False)
                print(sample_row)
            else:
                print('Library does not have a book which is written by that author.')
        elif beta_choice == '3':
            condition_year = int(input('Year: '))
            conditioned_df = df_books.loc[df_books['book_release_date'] == condition_year]
            if conditioned_df.empty == False:
                sample_row = conditioned_df.sample(3, replace=False)
                print(sample_row)
            else:
                print('Library does not have a book which released that year.')
        else:
            print('Invalid option. Try again.')
    elif choice_move == '6':
            print('1) Library properties')
            print('2) Graphs')
            choice = input('Select an option: ')
            if choice == '1':
                print('Data properties') 
                print(df_books.info())
                print('Some valuable information about books like maximum number of page etc.')
                print(df_books.describe())
                print('Book properties')
                print(df_books.columns)
                print('Number of books in library')
                print(df_books.index)
            elif choice == '2':
                print('1) Average rating based on author')
                move = input('Select an option: ') 
                if move == '1':
                    author = input('Author :')
                    conditioned_df = df_books[df_books['book_author'] == author]
                    a = sns.catplot(x='book_average_rating',y='book_name',data=conditioned_df,kind='bar',hue='book_name')
                    sns.set_palette("RdBu_r")
                    sns.set_context('notebook')
                    a.set(xlabel='Average Rating')
                    a.set_xticklabels(rotation=90)
                    a.set_yticklabels(rotation=45)
                    a.set_titles('Average rating based on', author)
                    plt.show()
                else:
                    print('Invalid option. Try again.')
    elif choice_move == "7":
        print("System shut down.")
        break
    else:
        print("Invalid answer. Try again.")
        







