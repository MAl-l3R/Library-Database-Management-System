import sys
import sqlite3 
import getpass

# Global variables for database connection and cursor
connection = None 
cursor = None

# Variable to store the current user's email
currentUser = None

def connect(path):
    """
    Establishes connection to the database at the given path.
    
    Arguements: (path(str)): The file path to the  database.
    
    Returns: None
    """
    
    global connection,cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def main_menu():
    """
    Displays the main menu options and executes corresponding actions based on user input.
    
    Returns: None
    """

        
    print("\nWhat would you like to do?")
    print("Press 1 to view your profile")
    print("Press 2 to return a book")
    print("Press 3 to search for books")
    print("Press 4 to pay a penalty")
    print("Press 5 to log out")
    user_input = int(input("> "))

    # Execute actions based on user input
    if(user_input == 1):
        profile_page()

    elif(user_input == 2):
        return_books()

    elif(user_input == 3):
        search_books()

    elif(user_input == 4):
        pay_penalty()

    elif(user_input == 5):
        return
    
    else:
        print("Please enter a valid choice (1-5): ")

def create_account():
    """
    Creates a new user account by gathering user information and inserting it into the database.
    
    Returns: None
    """
    global connection, cursor
    user_email = input("\nPlease enter your email: ")

    cursor.execute("SELECT * FROM members WHERE email = ?", (user_email,))
    user = cursor.fetchone()

    while user:
        if user:
            # Check if the user already exists
            print("User already exists with this email.")
            user_email = input("Please enter yout email: ")
            cursor.execute("SELECT * FROM members WHERE email = ?", (user_email,))
            user = cursor.fetchone()

    
    # Gather user information and insert into the database
    user_password = getpass.getpass("Enter your password: ")
    user_name = input("Please enter your name: ")
    user_byear = input("Please enter your birth year: ")


    while (not(user_byear.isdigit())):
        print("Please enter a valid birth year!")
        user_byear = (input("Please enter your birth year: "))

    user_byear = int(user_byear)
    user_faculty = input("Please enter faculty: ")

    signup_query =  """
                    INSERT INTO members (email, passwd, name, byear, faculty) 
                    values(?, ?, ?, ?, ?);
                    """
    cursor.execute(signup_query, (user_email, user_password, user_name,user_byear,user_faculty))
    global currentUser 
    currentUser = user_email
    connection.commit()
    return
    
def sign_in():
    """
    Authenticates the user by checking if the provided email and password match any existing user in the database.
    
    Returns: None
    """

    global connection,cursor,currentUser
    print()

    while True:

        try:
            email = input("Enter your email: ")
            password = getpass.getpass("Enter your password: ")
            cursor.execute("""
            SELECT * FROM members as m WHERE email = ? AND passwd = ? """, (email, password,))
            user = cursor.fetchone()

            if user:
                print("Login successful!")
                currentUser = email
                break
            else: 
                print("Login failed. Invalid email or password. Please try again.\n")

        except Exception as e:
            print(f"AN ERROR OCCURED: {e}")
            print(f"Debug: cursor = {cursor}, connection = {connection}")


    return

def login_page():
    """
    Displays the login page and prompts the user to sign in or create a new account.
    
    Returns: (str) A message indicating whether the user successfully logged in or not.
    """

    print("\nPress 1 to sign in")
    print("Press 2 to create an account")

    while True:
        try:
            user_input = input("> ")
            if user_input == "1":
                sign_in()
                return ("Logged In")
            elif user_input == '2':
                create_account()
                return ("Logged In")
            else:
                print("Invalid input, please try again")
        except Exception as e:
            print(f"AN ERROR OCCURED: {e}")
    

def profile_page():
    """
    Displays the user's profile information regarding their personal information, borrowings, and unpaid penalties.
    
    Returns: None
    """

    print("\nProfile Page")
    print("------------")
    print()

    global currentUser

    # Retrieve the user info
    print("Personal Information")
    cursor.execute("SELECT name, email, faculty, byear FROM members WHERE email = ?", (currentUser,))
    user_info = cursor.fetchone()
    if user_info is not None:
        name, email, faculty, byear = user_info
        print("\tName: " + name + "\n\tEmail: " + email + "\n\tFaculty: " + faculty + "\n\tBirth Year: " + str(byear))
    else:
        print("\tUser information not found.")
        
     
    # Retrieve previous borrowings, current borrowings, and overdue borrowings
    print("\nBorrowings")
    query = """
    SELECT
        (SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NOT NULL) AS previous_borrowings,
        (SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NULL) AS current_borrowings,
        (SELECT COUNT(*) FROM borrowings WHERE member = ? AND end_date IS NULL AND DATE(start_date, '+20 days') < DATE('now')) AS overdue_borrowings
    """
    cursor.execute(query, (currentUser, currentUser, currentUser))
    all_borrowings = cursor.fetchone()
    if all_borrowings:
        previous_borrowings, current_borrowings, overdue_borrowings = all_borrowings
        print("\tPrevious borrowings: " + str(previous_borrowings) + "\n\tCurrent borrowings: " + str(current_borrowings) + "\n\tOverdue borrowings: " + str(overdue_borrowings))
    else:
        print("\tNo borrowing records found.")
        
        
    # Retrieve number of unpaid penalties and total debt amount
    print("\nUnpaid Penalties")
    query = """
    SELECT
        COUNT(p.pid) AS unpaid_penalties_count,
        IFNULL(SUM(p.amount - IFNULL(p.paid_amount, 0)), 0) AS total_debt
    FROM penalties p
    JOIN borrowings b ON p.bid = b.bid
    WHERE b.member = ?
    AND p.amount > IFNULL(p.paid_amount, 0)
    """
    cursor.execute(query, (currentUser,))
    penalty_info = cursor.fetchone()
    if penalty_info != []:
        unpaid_penalties_count, total_debt = penalty_info
        print("\tUnpaid penalties: " + str(unpaid_penalties_count) + "\n\tTotal debt amount: " + str(total_debt))
    else:
        print("\tNo unpaid penalty records found.")
    
    input("\nPress any key to return to Main Menu > ")
    main_menu()


def is_float(string):
    """
    Checks if a string can be converted to a float.
    
    Args: string (str): The string to be checked.
    
    Returns: (bool): True if the string can be converted to a float otherwise return False
    """

    try:
        float(string)
        return True
    except ValueError:
        return False

def pay_penalty():
    """
    Allows the user to pay penalties for overdue books.
    
    Returns: None
    """

    global currentUser 

    while True:
        # Retrieve penalty information for the current user
        query = """
        SELECT
            p.pid AS unpaid_penalties,
            bk.title AS book_name,
            (p.amount - IFNULL(p.paid_amount,0)) as penalty_to_pay,
            IFNULL(p.paid_amount, 0) as paid,
            IFNULL(p.amount, 0) as penalty_amount 
        FROM penalties p
        JOIN borrowings b ON p.bid = b.bid
        JOIN books bk ON b.book_id = bk.book_id
        WHERE b.member = ?
        AND p.amount > IFNULL(p.paid_amount, 0)
        """
        cursor.execute(query, (currentUser,))
        penalty_info = cursor.fetchall()
        
        print("\nUnpaid Penalties")
        print("----------------")
        
        # Check if there are any unpaid penalties for the user
        if penalty_info == []:
            print("No unpaid penalty records found.")
            input("\nPress any key to return to Main Menu > ")
            break
            

        else:
                serial_number = 1
                # Display each unpaid penalty along with its details
                for penalty in penalty_info:
                    print(f"{serial_number}. Book name: {penalty[1]}, PID: {penalty[0]}, penalty_to_pay: {penalty[2]}")
                    serial_number += 1

                print("\n(Type Cancel to go back to main menu)")
                    
                user_input = input("\nSelect the penalty you want to pay off or type cancel: ")

                if(user_input.lower() == "cancel"):
                    break


                # Validate user input for selecting the penalty and taking input untill users enters a valid choice
                while (not(user_input.isdigit()) or (int(user_input) > len(penalty_info))):
                    print("Please enter a valid choice. ")
                    user_input = input("\nSelect the penalty you want to pay off type cancel: ")

                    if(user_input.lower() == "cancel"):
                        break

                if(user_input.lower() == "cancel"):
                    break

                #saving the input to a variable if it is valid
                user_input = int(user_input) - 1 

                
                # Ask user for payment amount
                payment_amount = input("How much do you want to pay? Or you can type cancel select to go back to main menu: ")

                if (payment_amount.lower() == "cancel"):
                    break

            
                # Validate payment amount
                while (not(is_float(payment_amount)) or float(payment_amount)<=0):
                    print("Please enter a valid amount")
                    payment_amount = input("How much do you want to pay? Or you can type cancel select to go back to main menu: ")

                    if (payment_amount.lower() == "cancel"):
                        break

                if (payment_amount.lower() == "cancel"):
                        break

                if float(payment_amount) <= penalty_info[user_input][2]:

                    # Update the paid amount for the penalty
                    new_paid_amount = (penalty_info[user_input][3] + float(payment_amount))
                    cursor.execute('''UPDATE penalties SET paid_amount=? WHERE pid=?''', (new_paid_amount, penalty_info[user_input][0]))
                    connection.commit()
                    
                    print(f"Payment of ${payment_amount} successfully applied to penalty with ID: {penalty_info[user_input][0]}.")

                else:
                    # If payment amount exceeds penalty amount, pay the full penalty
                    new_paid_amount = penalty_info[user_input][4]
                    cursor.execute('''UPDATE penalties SET paid_amount=? WHERE pid=?''', (new_paid_amount, penalty_info[user_input][0]))
                    connection.commit()
                    
                    print(f"Payment of ${penalty_info[user_input][2]} successfully applied to penalty with ID: {penalty_info[user_input][0]}.")

                # Ask if the user wants to pay more penalties
                more_penalty = input("\nDo you want to pay any other penalty? (Y/N) ").upper()

                choices = ["Y","N","y","n"] #creating a list to check for valid choices

                #checking if the user entered a valid choice
                while more_penalty not in choices:
                    print("Please enter a valid choice!(Y/N)")
                    more_penalty = input("\nDo you want to pay any other penalty? (Y/N) ")

                #if user enters N then breaking out of the loop and returning to main menu
                if more_penalty.upper() == "N":
                    break
    
    main_menu()
    

def search_books():

    """
    Allows the user to search for books by title or author, and optionally borrow a book from the system
    
    Returns: None
    """
    print("\nSearch for a book")
    print("-------------------")
    
    while (True):
        keyword = input("\nEnter a keyword: ")
        
        # Retrieve books with title matching the keyword
        query_for_book_title = """
        SELECT b.book_id, b.title, b.author, b.pyear,
            IFNULL((SELECT AVG(rating) FROM reviews WHERE book_id = b.book_id), 0) AS avg_rating,
            IFNULL((SELECT CASE WHEN COUNT(*) > 0 THEN 'No' ELSE 'Yes' END FROM borrowings WHERE book_id = b.book_id AND end_date IS NULL), 'Yes') AS available
        FROM books b
        WHERE b.title LIKE ?
        GROUP BY b.book_id
        ORDER BY b.title ASC;
        """
        cursor.execute(query_for_book_title, ('%' + keyword + '%',))
        books_with_title = cursor.fetchall()

        # Retrieve books with author matching the keyword
        query_for_author_name = """
        SELECT b.book_id, b.title, b.author, b.pyear,
            IFNULL((SELECT AVG(rating) FROM reviews WHERE book_id = b.book_id), 0) AS avg_rating,
            IFNULL((SELECT CASE WHEN COUNT(*) > 0 THEN 'No' ELSE 'Yes' END FROM borrowings WHERE book_id = b.book_id AND end_date IS NULL), 'Yes') AS available
        FROM books b
        WHERE b.author LIKE ? AND b.title NOT LIKE ?
        GROUP BY b.book_id
        ORDER BY b.author ASC;
        """
        cursor.execute(query_for_author_name, ('%' + keyword + '%', '%' + keyword + '%'))
        books_with_author = cursor.fetchall()
        
        # Display books with title matching the keyword
        print("Books with title matching keyword:")
        for book_id, title, author, pyear, avg_rating, available in books_with_title:
            print("\tBook ID: " + str(book_id) + ", Title: " + title + ", Author: " + author + ", Publish Year: " + str(pyear) + ", Average Rating: " + str(avg_rating) + ", Available: " + available)        
                
        # Display books with author matching the keyword
        print("\nBooks with author matching keyword:")
        for book_id, title, author, pyear, avg_rating, available in books_with_author:
            print("\tBook ID: " + str(book_id) + ", Title: " + title + ", Author: " + author + ", Publish Year: " + str(pyear) + ", Average Rating: " + str(avg_rating) + ", Available: " + available)

        choices = ["Y","N", "y", "n"] #creating a list to check for valid choices
        
        # Ask user if they want to borrow a book
        borrow_choice = input("\nDo you want to borrow a book? (Y/N): ")

        while borrow_choice not in choices:
            print("Please enter a valid choice!(Y/N)")
            borrow_choice = input("\nDo you want to borrow a book? (Y/N): ")

        
        if borrow_choice.upper() == 'Y':
            borrow_book()
            
        # Ask user if they want to search again with a different keyword
        search_again = input("\nDo you want to search with a different keyword? (Y/N): ")

        while search_again not in choices:
            print("Please enter a valid choice!(Y/N)")
            search_again = input("\nDo you want to borrow a book? (Y/N): ")

        if search_again.upper() == 'N':
            break
    
    main_menu()
        
        
def borrow_book():
    """
    Allows the user to borrow a book by entering the book ID.
    
    Returns: None
    """

    global currentUser
    
    # Ask user for book ID to borrow
    while True:
        book_id = input("Enter the Book ID for the book you want to borrow, or type cancel to go back: ")
        if book_id.lower() == 'cancel':
            return
        elif book_id.isdigit():
            book_id = int(book_id)
            # Check if input is a valid book id
            cursor.execute("SELECT MAX(book_id) FROM books")
            max_bookId = cursor.fetchone()[0]
            if book_id > max_bookId or book_id <= 0:
                print("Selected book ID does not exist. Please enter a valid book ID.\n")
            else:
                break
        else:
            print("Invalid Input\n")

    
    # Check if the book is available
    cursor.execute("SELECT COUNT(*) FROM borrowings WHERE book_id = ? AND end_date IS NULL", (book_id,))
    result = cursor.fetchone()[0]  # Because there should be only one row returned
    if result > 0:
        print("Sorry, the book is not available.")
    else:
        # Insert new borrowing record
        cursor.execute("SELECT MAX(bid) FROM borrowings")
        max_bid = cursor.fetchone()[0]
        bid = max_bid + 1 if max_bid else 1  # Generating unique borrow id
        cursor.execute("INSERT INTO borrowings VALUES (?, ?, ?, DATE('now'), NULL)", (bid, currentUser, book_id))
        connection.commit()
        print("Book borrowed successfully.")
    
    
def borrowings_list(cursor, user): # COMPLETED

    """
    Retrieves and displays current borrowings for the user.
    
    Arguements:
    (cursor): The cursor object for executing SQL queries.
    (user(str)): The email of the user for whom to retrieve borrowings.
    
    Returns: None
    """

    query='''
    SELECT bid,title,start_date,
    DATE(start_date, '+20 days') AS deadline     
    FROM books as b JOIN borrowings as borrow on b.book_id = borrow.book_id
    WHERE end_date IS NULL AND member = ?;
    '''
    cursor.execute(query,(user,)) #borrowing id, book title, borrowing date, and return deadline for each unreturned borrowing (including overdue ones).
    row = cursor.fetchone()
    list_of_borrowigs = [] # To store all the current borrowings
    print("\nList of Current Borrowings")
    print("--------------------------------")
    while row is not None:
        bid, title, start_date, deadline = row
        list_of_borrowigs.append(bid)
        print(f"Borrowing id: {bid}")
        print(f"Book Title: {title}")
        print(f"Borrowing Date: {start_date}")
        print(f"Return Deadline: {deadline}")
        print("--------------------------------")
        row = cursor.fetchone()
    return list_of_borrowigs

def return_books(): # COMPLETED

    """
    Allows the user to return borrowed books and optionally write a review for the book.

    Returns: None
    """ 
    global connection,cursor  
    
    # Retrieve the list of current borrowings for the user
    list_of_borrowigs = borrowings_list(cursor, currentUser)

    # Check if the user has any books borrowed
    if not list_of_borrowigs:
        print("You currently don't have any books borrowed")
        input("\nPress any key to return to Main Menu > ")
        main_menu()
        return
    
    while True:
        try: 
            return_id_input =  input("\nTo return a Book, please enter its Borrowing Id (or type cancel to return back to main menu) > ")
            if  return_id_input.lower() == "cancel":
                    main_menu()
                    return
            if return_id_input.isdigit(): 
                return_id= int(return_id_input) 
                if return_id in list_of_borrowigs:
                    query_penalty = '''
                        SELECT julianday(DATE('now')) > julianday(DATE(start_date, '+20 days')) as late, 
                                CASE
                                    WHEN julianday(DATE('now')) - julianday(DATE(start_date, '+20 days')) < 0 THEN 0 
                                    ELSE julianday(DATE('now')) - julianday(DATE(start_date, '+20 days')) 
                                END AS delays_dates
                        FROM borrowings
                        WHERE bid = ? AND end_date IS NULL'''

                    cursor.execute(query_penalty, (return_id,))
                    result = cursor.fetchone()
                    late, delays_days = result

                    if delays_days > 0:
                        penalty = delays_days * 1 # adding $1 for each day 
                    else:
                        penalty = 0 #  not overdue

                    #if return_id in list_of_borrowigs:# check isdigit
                    query2 = ''' UPDATE borrowings SET end_date = date('now') WHERE bid = ?'''
                    cursor.execute(query2, (return_id,))
                    if penalty > 0:  # below check for null in amount attribute
                        update_penalty_query = '''INSERT INTO penalties (bid, amount) VALUES (?, ?)'''
                        cursor.execute(update_penalty_query, (return_id, penalty,))
                    connection.commit() # commiting all the changes 
                    print(f"Book return completed successfully. Penality applied: ${penalty}")

                    #The optional choice to write a review for the book 
                    while True:
                        user_input =  input("\nWould you like to write a review for this book? (Y/N) > ")
                        if user_input.lower() == "y":
                            rtext = input("\nPlease share you thoughts of the book > ")
                            rating = None # none for placeholder
                            while rating is None:
                                user_review_input = input("\nPlease rate the book on a scale of 1 to 5 > ") 
                                if user_review_input.isdigit():
                                    user_review_input = int(user_review_input)
                                    if  1 <= user_review_input <= 5:
                                        rating = int(user_review_input)
                                    else:
                                        print("Invalid input. Please try rating again on a scale of 1 to 5") 
                                else:
                                    print("Invalid input. Please try again")
                            # FINDING BOOK_ID
                            book_id_query = '''SELECT book_id FROM borrowings WHERE bid = ? '''
                            cursor.execute(book_id_query, (return_id,))
                            
                            book_id = cursor.fetchone()[0] # so that is it not tuple

                            # updating the datebase with reviews
                            review_update_query ='''
                                                    INSERT INTO reviews ( book_id, member, rating, rtext, rdate) 
                                                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP) '''
                            
                            cursor.execute(review_update_query, (book_id, currentUser, rating, rtext,)) 
                            connection.commit()
                            print("\nThank you for the review!")
                            break
                        elif user_input.lower() == "n":
                            break
                        else:
                            print("Invalid input. Please press 'Y' for yes and 'N' for no")

                    while True:      
                        return_again = input("\nWould you like to return another book? (Y/N) > ")
                        if return_again.upper() == 'N':
                            break
                        elif return_again.upper() == 'Y':
                            list_of_borrowigs = borrowings_list(cursor, currentUser)
                            # Check if the user still has any books borrowed
                            if not list_of_borrowigs:
                                print("You currently don't have any books borrowed")
                                input("\nPress any key to return to Main Menu > ")
                                main_menu()
                                return
                            break
                        else:
                            print("Invalid input. Please press 'Y' for yes and 'N' for no")
                    if return_again.upper() == 'N':
                        break
                else:
                    print("Invalid Borrowings ID. Please choose the correct borrowing id.")
            else:
                print("Invalid input. Please enter a valid borrowing id.")
        
        except Exception as e:
            print(f"An error occured: {e}")

    # Return to the main menu after completing return process
    main_menu()
    
def main(path):
    """
    The main function that initializes the connection to the database, prompts the user to log in or create an account,
    and displays the main menu for the library management system.

    Arguements: (path(str)): The path to the database file.

    Returns: None
    """
    connect(path)
    
    print("\nWelcome to public library")
    logged_in = login_page()
    if (logged_in == "Logged In"):
        main_menu()

    

if __name__ == "__main__":
    # Check if an argument is provided
    if len(sys.argv) > 1:
        path = sys.argv[1]  # Take the first argument as the database name
    else:
        print("\nNo database name provided, using default 'library_data.db'.\n")
     
        path = './library_data.db' # Default database name
    main(path)
