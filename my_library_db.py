import sys

class LibraryTextDB:
    def __init__(self, db_file:str):
        self.db_file = db_file

    db_file:str

    class entry:
        title: str
        author: str
        ISBN: int
        year: int

    def AddBook(self):
        title = input("Enter title: ")
        if title == "":
            print("Title can not be empty.\n")
            return
        author = input("Enter author: ")
        if author == "":
            print("Author can not be empty.\n")
            return
        ISBN = (input("Enter ISBN (without - or whitespace): "))
        if ISBN == "" or not ISBN.isdigit():
            print("ISBN can not be empty, and has to be a number.\n")
            return
        year = (input("Enter year: "))
        if year == "" or not year.isdigit():
            print("Year can not be empty, and has to be a number.\n")
            return
        confirm = input(f"Add {title}/{author}/{ISBN}/{year}? (Y/N): ")
        if confirm == "Y" or confirm == "y":
            self.Write(title, author, int(ISBN), int(year))

    # AddBook inserts a new book entry into the database file. The entries are sorted by year in ascending order.
    def Write(self, title:str, author:str, ISBN:int, year:int):
        # Clean up any / characters from the input
        title = title.replace("/", " ")
        author = author.replace("/", " ")

        with open(self.db_file, "r+") as f:
            data = f.readlines()
            # Find the right spot for the given Book, where the year is larger or equal for a given line
            for i, line in enumerate(data):
                entry = line.split("/")
                if int(entry[3]) >= year:
                    data.insert(i, f"{title}/{author}/{ISBN}/{year}\n")
                    break
            else:
                # If the year is the largest, append the new book to the end of the file
                data.append(f"{title}/{author}/{ISBN}/{year}\n")
            # Write everything back to the file.
            f.seek(0)
            f.writelines(data)

    def Print(self):
        # Print styling. Title 30 chars, author row 15 chars, ISBN 13 chars, year 4 chars. Truncated and padded to fit.
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

    # Validate the database file exist
    try:
        with open(sys.argv[1]):
            pass 
    except:
        print("database_file or path does not exist. Please check the input or create a new database file", sys.argv[1])
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

