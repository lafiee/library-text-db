import sys
import os

class LibraryTextDB:
    def __init__(self, db_file:str):
        """
        Create a new LibraryTextDB object with a given database file.
        """
        try:
            with open(db_file):
                self.db_file = db_file 
        except FileNotFoundError:
            print("database_file or path does not exist. Please check the input or create a new database file", db_file)
            sys.exit(1)

    db_file:str

    def AddBook(self):
        """ 
        AddBook promps user with inputs for a new book entry and validates the input.
        """
        title = input("Enter title: ")
        title = title.replace("/", " ")
        if title == "":
            print("Title can not be empty.\n")
            return
        author = input("Enter author: ")
        author = author.replace("/", " ")
        if author == "":
            print("Author can not be empty.\n")
            return
        ISBN = (input("Enter ISBN (without - or whitespace): "))
        if not ISBN.isdigit() or int(ISBN) <= 0:
            print("ISBN can not be empty, and has to be a number.\n")
            return
        year = (input("Enter year: "))
        if not year.isdigit() or int(year) <= 0:
            print("Year can not be empty, and has to be a number.\n")
            return
        confirm = input(f"Add {title}/{author}/{ISBN}/{year}? (Y/N): ")
        if confirm == "Y" or confirm == "y":
            self.Write(title, author, int(ISBN), int(year))

    def Write(self, title:str, author:str, ISBN:int, year:int) -> None:
        """ 
        Write inserts a new book entry into the database file. The entries are sorted by year in ascending order.
        """
        temp_file = self.db_file + ".tmp"
        new_entry = f"{title}/{author}/{ISBN}/{year}\n"
        inserted = False
        line = None

        with open(self.db_file, "r") as read_file, open(temp_file, "w") as write_file:
            for line in read_file:
                entry = line.split("/")
                if not inserted and int(entry[3]) >= year:
                    write_file.write(new_entry)
                    inserted = True
                write_file.write(line)
            
            # If the new entry has the largest year, append it at the end
            if not inserted:
                if line is not None and not line.endswith("\n"):
                    write_file.write("\n")
                write_file.write(new_entry)
        # Replace the original file with the temporary file
        os.replace(temp_file, self.db_file)

    def Print(self):
        """
        Print styling. Title 30 chars, author row 15 chars, ISBN 13 chars, year 4 chars. Truncated and padded to fit.
        """
        print("Title..........................Author..........ISBN..........Year")
        with open(self.db_file, "r") as f:
            for line in f:
                entry = line.split("/")
                print('{:30.30}'.format(entry[0]), '{:15.15}'.format(entry[1]),'{:13.13}'.format(entry[2]),'{:4.4}'.format(entry[3]))

if __name__ == "__main__":
    # Takes 1 command line argument, database text file
    if len(sys.argv) != 2:
        print("Usage: python my_library_db.py <database_file>")
        sys.exit(1)

    db = LibraryTextDB(sys.argv[1])

    while True:
        print("Book library database, usage:")
        print("1. Add book")
        print("2. Print library")
        print("Q. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            db.AddBook()
        elif choice == "2":
            db.Print()
        elif choice == "Q" or choice == "q":
            break
        else:
            print("Invalid choice, try again.")
        print() # Newline for readability between choices

