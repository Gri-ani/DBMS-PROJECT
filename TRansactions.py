import threading
import mysql.connector
import time;

connect = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='BACKEND')
cursor_ = connect.cursor()
# -----------------------------------------------------------   EXAMPLE 1    ------------------------------------------------
def increase_product_quantity(product_id):
    print("incraese product quantity")
    try:
        query = "UPDATE Product SET product_quantity = product_quantity + 1 WHERE product_id = %s"
        cursor_.execute(query, (product_id,))
        connect.commit()
        print("Product quantity increased successfully!")
    except mysql.connector.Error as e:
        print(f"An error occurred in increase_product_quantity: {e}")

def increase_product_quantity_(product_id, cursor, connect):
    print("Increasing product quantity...")
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            query = "UPDATE Product SET product_quantity = product_quantity + 1 WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            connect.commit()
            print("Product quantity increased successfully!")
            break  # Exit the loop if the update is successful
        except mysql.connector.Error as e:
            print(f"An error occurred in increase_product_quantity: {e}")
            retries += 1
            if retries < max_retries:
                print("Retrying after 1 second...")
                time.sleep(1)  # Wait for 1 second before retrying
            else:
                print("Max retries reached. Failed to increase product quantity.")
def decrease_product_quantity_(product_id, cursor, connect):
    print("Decreasing product quantity...")
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            query = "UPDATE Product SET product_quantity = product_quantity - 1 WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            connect.commit()
            print("Product quantity decreased successfully!")
            break  # Exit the loop if the update is successful
        except mysql.connector.Error as e:
            print(f"An error occurred in decrease_product_quantity: {e}")
            retries += 1
            if retries < max_retries:
                print("Retrying after 1 second...")
                time.sleep(1)  # Wait for 1 second before retrying
            else:
                print("Max retries reached. Failed to decrease product quantity.")
def decrease_product_quantity(product_id):
    print("decreade product quantity")
    try:
        query = "UPDATE Product SET product_quantity = product_quantity - 1 WHERE product_id = %s"
        cursor_.execute(query, (product_id,))
        connect.commit()
        print("Product quantity decreased successfully!")
    except mysql.connector.Error as e:
        print(f"An error occurred in decrease_product_quantity: {e}")

id = int(input("Enter product id: "))

# Define the conflicting transactions as functions
def conflicting_transaction_1():
    try:
        decrease_product_quantity_(id,cursor_,connect)
    except mysql.connector.Error as e:
        print(f"An error occurred in conflicting_transaction_1: {e}")

def conflicting_transaction_2():
    try:
        increase_product_quantity_(id,cursor_,connect)
    except mysql.connector.Error as e:
        print(f"An error occurred in conflicting_transaction_2: {e}")

# Create threads for each conflicting transaction
thread1 = threading.Thread(target=conflicting_transaction_1)
thread2 = threading.Thread(target=conflicting_transaction_2)
print("2 threads for decrease product quanity and incresed created")

# Start the threads to execute the conflicting transactions concurrently
thread1.start()
thread2.start()

# Wait for both threads to finish execution
thread1.join()
thread2.join()




#specific to deadline 6 TRANSACTIONS


# #-------------------------------------------------------------------------------------------------------------------------------------
#
# import threading
#
#
# def increase_product_quantity(product_id):
#     try:
#         # Increase the quantity of the specified product in the database
#         query = "UPDATE Product SET product_quantity = product_quantity + 1 WHERE product_id = %s"
#         cursor.execute(query, (product_id,))
#         connect.commit()
#         print("Product quantity increased successfully!")
#     except mysql.connector.Error as e:
#         print(f"An error occurred in increase_product_quantity: {e}")
#
# def decrease_product_quantity(product_id):
#     try:
#         # Decrease the quantity of the specified product in the database
#         query = "UPDATE Product SET product_quantity = product_quantity - 1 WHERE product_id = %s"
#         cursor.execute(query, (product_id,))
#         connect.commit()
#         print("Product quantity decreased successfully!")
#     except mysql.connector.Error as e:
#         print(f"An error occurred in decrease_product_quantity: {e}")
#
# id=int(inpt("enter product id: "))
#
# # Define the conflicting transactions as functions
# def conflicting_transaction_1():
#     try:
#         # Simulate conflicting transaction 1
#         # Let's say two users simultaneously try to update the quantity of the same product
#         # id=int(input("product id: "))
#         decrease_product_quantity(id)  # Call the function to update product quantity
#         # Here we can add more operations that may conflict with the above update
#     except mysql.connector.Error as e:
#         print(f"An error occurred in conflicting_transaction_1: {e}")
#
# def conflicting_transaction_2():
#     try:
#         # Simulate conflicting transaction 2
#         # Let's say two users simultaneously try to update the quantity of the same product
#         # id=int(input("product id: "))
#         increase_product_quantity(id)  # Call the function to update product quantity
#
#     except mysql.connector.Error as e:
#         print(f"An error occurred in conflicting_transaction_1: {e}")
#
#
#
# # Create threads for each conflicting transaction
# thread1 = threading.Thread(target=conflicting_transaction_1)
# thread2 = threading.Thread(target=conflicting_transaction_2)
#
# #if both transaction 1 and 2 are working on the same product_id in a threaded way then it can lead to conflicting transactions
#
# # Start the threads to execute the conflicting transactions concurrently
# thread1.start()
# thread2.start()
#
# # Wait for both threads to finish execution
# thread1.join()
# thread2.join()
#




# Once both threads have finished execution, you can continue with other parts of your program


#-------------------------------------------------------------------------------------------------------------------------



#here since both the threads are making the transaction using the same cust_id and both are adding so it does not lead to conflicts but
# suppose id we had conflicting operations like both trying to reduce from wallet then as soon as 1 thread runs the wallet might become empty and
#and the 2nd trannsaction is not possible

#-------------------example 3--------------------------------------


# this is an example of conflicting since both of them are trying to addd the saem product to their respective carts
#
# import threading
# import random
# import mysql.connector
#
#
#
# def add_to_cart(customer_id, product_id, quantity):
#     try:
#         # Create a new MySQL connection for each thread
#         connect = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='backend')
#         cursor = connect.cursor()
#
#         print(f"Customer {customer_id} is adding product {product_id} to the cart with quantity {quantity}.")
#         # Simulate adding a product to the customer's cart
#         # Check if there is sufficient stock available for the product
#         query = "SELECT product_quantity FROM Product WHERE product_id = %s"
#         cursor.execute(query, (product_id,))
#         available_stock = cursor.fetchone()[0]
#
#         if available_stock >= quantity:
#             # If there is sufficient stock, add the product to the customer's cart
#             insert_query = "INSERT INTO Cart (customer_ID, product_ID, quantity) VALUES (%s, %s, %s)"
#             cursor.execute(insert_query, (customer_id, product_id, quantity))
#             connect.commit()
#             print(f"Product added to cart successfully for customer ID {customer_id}.")
#         else:
#             # If there is not enough stock available, print an error message
#             print(f"Not enough stock available for product ID {product_id}.")
#     except mysql.connector.Error as e:
#         print(f"An error occurred in add_to_cart: {e}")
#     finally:
#         # Close the MySQL connection after execution
#         cursor.close()
#         connect.close()
#
#
# def conflicting_add_to_cart(customer_id, product_id, quantity):
#     # Simulate non conflicting scenario where two customers try to add the same product to their carts simultaneously
#     add_to_cart(customer_id, product_id, quantity)
#
# # Define product ID and quantity
# product_id = 4 # Assuming the product ID is 1
# quantity = 2  # Quantity to add to cart
#
# # Define customer IDs
# cust1_id = 11
# cust2_id = 3
#
# # Create threads for both customers trying to add the same product to their carts simultaneously
# thread1 = threading.Thread(target=conflicting_add_to_cart, args=(cust1_id, product_id, quantity))
# thread2 = threading.Thread(target=conflicting_add_to_cart, args=(cust2_id, product_id, quantity))
#
# # Start both threads
# thread1.start()
# thread2.start()
#
# # Wait for both threads to finish execution
# thread1.join()
# thread2.join()




#
# #--------------------------------example 4---------------------------------------------------------------------------
# import threading
import mysql.connector
#
def add_money_to_wallet(customer_id, amount):
    try:
        # Create a new MySQL connection for each thread
        connect = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='backend')
        cursor = connect.cursor()

        print(f"Adding {amount} money to the wallet for customer ID {customer_id}.")
        # Update the wallet amount for the customer
        update_query = "UPDATE Wallet SET wallet_amount = wallet_amount + %s WHERE customer_id = %s"
        cursor.execute(update_query, (amount, customer_id))
        connect.commit()
        print(f"{amount} added to the wallet successfully for customer ID {customer_id}.")
        check_wallet_amount(customer_id)
    except mysql.connector.Error as e:
        print(f"An error occurred in add_money_to_wallet: {e}")
    finally:
        # Close the MySQL connection after execution
        cursor.close()
        connect.close()

def add_to_cart(customer_id, product_id, quantity):
    try:
        # Create a new MySQL connection for each thread
        connect = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='backend')
        cursor = connect.cursor()

        print(f"Customer {customer_id} is adding product {product_id} to the cart with quantity {quantity}.")
        # Check if the product already exists in the customer's cart
        query = "SELECT * FROM Cart WHERE customer_ID = %s AND product_ID = %s"
        cursor.execute(query, (customer_id, product_id))
        existing_entry = cursor.fetchone()

        if existing_entry:
            # If the product already exists in the cart, update the quantity instead of inserting a new entry
            update_query = "UPDATE Cart SET quantity = quantity + %s WHERE customer_ID = %s AND product_ID = %s"
            cursor.execute(update_query, (quantity, customer_id, product_id))
            connect.commit()
            print(f"Quantity updated in the cart for customer ID {customer_id}.")
        else:
            # If the product does not exist in the cart, insert a new entry
            # Check if there is sufficient stock available for the product
            query = "SELECT product_quantity FROM Product WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            available_stock = cursor.fetchone()[0]

            if available_stock >= quantity:
                # If there is sufficient stock, add the product to the customer's cart
                insert_query = "INSERT INTO Cart (customer_ID, product_ID, quantity) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (customer_id, product_id, quantity))
                connect.commit()
                print(f"Product added to cart successfully for customer ID {customer_id}.")
                # view_cart(customer_id, connect)
            else:
                # If there is not enough stock available, print an error message
                print(f"Not enough stock available for product ID {product_id}.")
    except mysql.connector.Error as e:
        print(f"An error occurred in add_to_cart: {e}")
    finally:
        # Close the MySQL connection after execution
        cursor.close()
        connect.close()

# Define customer ID, product ID, and quantity
customer_id = 1
product_id = 1
quantity = 6
amount = 50  # Amount to add to the wallet

# Create threads for adding money to wallet and adding product to cart
thread1 = threading.Thread(target=add_money_to_wallet, args=(customer_id, amount))
thread2 = threading.Thread(target=add_to_cart, args=(customer_id, product_id, quantity))

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to finish execution
thread1.join()



thread2.join()
#
#
# #even though this happens simultaneously still no issue as one wrks on wallet and other on cart
#
#
# #---------------------------------------------example 5-------------------------------------------------------------
#
#
# import threading
# import mysql.connector
#
# def deduct_money_from_wallet(customer_id, amount):
#     try:
#         # Create a new MySQL connection for each thread
#         connect = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='backend')
#         cursor = connect.cursor()
#
#         # Read the current wallet balance
#         cursor.execute("SELECT wallet_amount FROM Wallet WHERE customer_id = %s", (customer_id,))
#         current_balance = cursor.fetchone()[0]
#
#         print(f"Deducting {amount} money from the wallet for customer ID {customer_id}.")
#
#         # Deduct the specified amount from the wallet balance
#         new_balance = current_balance - amount
#
#         # Update the wallet balance
#         cursor.execute("UPDATE Wallet SET wallet_amount = %s WHERE customer_id = %s", (new_balance, customer_id))
#         connect.commit()
#         print(f"{amount} deducted from the wallet successfully for customer ID {customer_id}.")
#     except mysql.connector.Error as e:
#         print(f"An error occurred in deduct_money_from_wallet: {e}")
#         # Rollback the transaction
#         connect.rollback()
#     finally:
#         # Close the MySQL connection after execution
#         cursor.close()
#         connect.close()
#
# def add_money_to_wallet(customer_id, amount):
#     try:
#         # Create a new MySQL connection for each thread
#         connect = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='backend')
#         cursor = connect.cursor()
#
#         # Read the current wallet balance
#         cursor.execute("SELECT wallet_amount FROM Wallet WHERE customer_id = %s", (customer_id,))
#         current_balance = cursor.fetchone()[0]
#
#         print(f"Adding {amount} money to the wallet for customer ID {customer_id}.")
#
#         # Add the specified amount to the wallet balance
#         new_balance = current_balance + amount
#
#         # Update the wallet balance
#         cursor.execute("UPDATE Wallet SET wallet_amount = %s WHERE customer_id = %s", (new_balance, customer_id))
#         connect.commit()
#         print(f"{amount} added to the wallet successfully for customer ID {customer_id}.")
#     except mysql.connector.Error as e:
#         print(f"An error occurred in add_money_to_wallet: {e}")
#         # Rollback the transaction
#         connect.rollback()
#     finally:
#         # Close the MySQL connection after execution
#         cursor.close()
#         connect.close()
#
# # Define customer ID and amount
# customer_id = 1
# amount = 50  # Amount to add to/deduct from the wallet
#
# # Create threads for deducting money from the wallet and adding money to the wallet
# thread1 = threading.Thread(target=deduct_money_from_wallet, args=(customer_id, amount))
# thread2 = threading.Thread(target=add_money_to_wallet, args=(customer_id, amount))
#
# # Start both threads
# thread1.start()
# thread2.start()
#
# # Wait for both threads to finish execution
# thread1.join()
# thread2.join()
#
#
# #in this as you can see that I have done roll back for both the transactions but still there is a dirty read and it cannot be recovered maney
# #gets updated in wrong way
# #this is non conflicting for sure
#
#
#
# """
# A dirty read occurs when one transaction reads data that has been modified by another transaction but not yet committed. In this scenario, if the transaction that made the modification is rolled back, the data read by the first transaction becomes invalid. Let's illustrate this with an example:
#
# Suppose we have two transactions:
#
# Transaction A: Reads a customer's wallet balance and then deducts some money from it.
# Transaction B: Simultaneously reads the same customer's wallet balance and then adds some money to it.
# If Transaction A reads the wallet balance first (before Transaction B commits its changes) and then Transaction B rolls back, Transaction A will have read incorrect data (dirty read). Even if Transaction A rolls back after reading the incorrect data, the inconsistency caused by the dirty read cannot be fully recovered.
# """
import threading
import mysql.connector
from mysql.connector import Error

# Establish a database connection
try:
    connect = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='BACKEND')

    if connect.is_connected():
        print("Connected to the database.")

except Error as e:
    print("Error connecting to the database:", e)

# Assuming you have a database connection object named 'connect'
# Define th
# e customer data for conflicting transactions
customer_data1 = {
    "customer_id": "1001",
    "email": "customer1@example.com",
    "password": "password1",
    "first_name": "John",
    "last_name": "Doe",
    "street_address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "contact_number": "1234567890"
}

customer_data2 = {
    "customer_id": "1002",
    "email": "customer2@example.com",
    "password": "password2",
    "first_name": "Jane",
    "last_name": "Doe",
    "street_address": "456 Elm St",
    "city": "Los Angeles",
    "state": "CA",
    "contact_number": "9876543210"
}

# Define the function for customer creation
def customer_creation(connect, customer_data):
    try:
        cursor = connect.cursor()
        query = """
        INSERT INTO Customer (customer_id, email, password, first_name, last_name, street_address, city, state, contact_number)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            customer_data["customer_id"], customer_data["email"], customer_data["password"],
            customer_data["first_name"], customer_data["last_name"], customer_data["street_address"],
            customer_data["city"], customer_data["state"], customer_data["contact_number"]))
        connect.commit()
        print("Customer added successfully:", customer_data["customer_id"])
    except mysql.connector.IntegrityError as e:
        print("A customer with the provided email or ID already exists." if '1062' in str(e) else f"An error occurred: {e}")
    except Error as err:
        print(f"An error occurred: {err}")
    except ValueError as ve:
        print("Invalid input. Please ensure all inputs are correct and try again.")

# Define a function to demonstrate conflicting transactions
def conflicting_transactions():
    # Create two threads for conflicting transactions with different customer data
    thread1 = threading.Thread(target=customer_creation, args=(connect, customer_data1))
    thread2 = threading.Thread(target=customer_creation, args=(connect, customer_data2))

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish execution
    thread1.join()
    thread2.join()

# Call the function to demonstrate conflicting transactions
conflicting_transactions()

# Close the database connection
if connect.is_connected():
    connect.close()
    print("Database connection closed.")



------------------------------------------------------------------------------------------------------------------------------
import threading
import mysql.connector
from datetime import datetime, timedelta
import time

# Function to perform checkout for a customer
def checkout(connect, customer_id):
    print("placing order")
    # print("")
    try:
        cursor = connect.cursor()

        # Fetch cart items and calculate total payment amount
        query = """
        SELECT c.product_ID, p.price, c.quantity, p.product_quantity, p.seller_id
        FROM Cart c
        JOIN Product p ON c.product_ID = p.product_id
        WHERE c.customer_ID = %s;
        """
        cursor.execute(query, (customer_id,))
        cart_items = cursor.fetchall()

        if not cart_items:
            print("Your cart is empty.")
            return

        total_payment = sum(item[1] * item[2] for item in cart_items)

        for item in cart_items:
            if item[2] > item[3]:
                print(f"Cannot complete checkout: Requested quantity for product ID {item[0]} exceeds available stock.")
                return

        wallet_query = "SELECT wallet_amount FROM Wallet WHERE customer_ID = %s"
        cursor.execute(wallet_query, (customer_id,))
        wallet_balance = cursor.fetchone()[0]
        if wallet_balance < total_payment:
            print("Insufficient balance. Please add funds to your wallet.")
            return

        order_date = datetime.now().date()
        order_time = datetime.now().strftime("%H:%M:%S")
        delivery_date = order_date + timedelta(days=7)  # Calculate delivery date

        for item in cart_items:
            update_product_query = "UPDATE Product SET product_quantity = product_quantity - %s WHERE product_id = %s"
            cursor.execute(update_product_query, (item[2], item[0]))

            tracking_id = int(time.time()) - 10100000 + item[4]  # Generate tracking ID as order_id + 101
            seller_id = item[4]  # Get seller ID from cart items

            insert_order_query = """
            INSERT INTO Order_ (order_date, order_time, customer_id, product_id, product_quantity, payment_amount, delivery_date, tracking_id, seller_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_order_query,
                           (order_date, order_time, customer_id, item[0], item[2], item[1] * item[2], delivery_date, tracking_id, seller_id))

        clear_cart_query = "DELETE FROM Cart WHERE customer_ID = %s"
        cursor.execute(clear_cart_query, (customer_id,))

        connect.commit()
        print("Checkout successful. Your order has been placed.")
    except Exception as e:
        connect.rollback()
        print(f"An error occurred during checkout: {e}")
    finally:
        # Close cursor and connection after use
        cursor.close()
        connect.close()


# Define a function to simulate checkout for two customers simultaneously
def concurrent_checkout(customer_id_1, customer_id_2):
    # Establish a new connection for each thread
    connect_1 = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='backend')
    connect_2 = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='backend')

    # Perform checkout for each customer in separate threads
    thread1 = threading.Thread(target=checkout, args=(connect_1, customer_id_1))
    thread2 = threading.Thread(target=checkout, args=(connect_2, customer_id_2))

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish execution
    thread1.join()
    thread2.join()

    # Close connections after threads finish
    connect_1.close()
    connect_2.close()


# Define the customer IDs and product ID for testing
customer_id_1 = 11
customer_id_2 = 4
product_id = 5# Assuming the product ID is 1

# Simulate concurrent checkout for two customers
concurrent_checkout(customer_id_1, customer_id_2)



#
import threading
import mysql.connector

def deduct_money_from_wallet(customer_id, amount):
    try:
        # Create a new MySQL connection for each thread
        connect = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='backend')
        cursor = connect.cursor()

        # Read the current wallet balance
        cursor.execute("SELECT wallet_amount FROM Wallet WHERE customer_id = %s", (customer_id,))
        current_balance = cursor.fetchone()[0]

        print(f"Deducting {amount} money from the wallet for customer ID {customer_id}.")

        # Deduct the specified amount from the wallet balance
        new_balance = current_balance - amount

        # Update the wallet balance
        cursor.execute("UPDATE Wallet SET wallet_amount = %s WHERE customer_id = %s", (new_balance, customer_id))
        connect.commit()
        print(f"{amount} deducted from the wallet successfully for customer ID {customer_id}.")
    except mysql.connector.Error as e:
        print(f"An error occurred in deduct_money_from_wallet: {e}")
        # Rollback the transaction
        connect.rollback()
    finally:
        # Close the MySQL connection after execution
        cursor.close()
        connect.close()

def add_money_to_wallet(customer_id, amount):
    try:
        # Create a new MySQL connection for each thread
        connect = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='backend')
        cursor = connect.cursor()

        # Read the current wallet balance
        cursor.execute("SELECT wallet_amount FROM Wallet WHERE customer_id = %s", (customer_id,))
        current_balance = cursor.fetchone()[0]

        print(f"Adding {amount} money to the wallet for customer ID {customer_id}.")

        # Add the specified amount to the wallet balance
        new_balance = current_balance + amount

        # Update the wallet balance
        cursor.execute("UPDATE Wallet SET wallet_amount = %s WHERE customer_id = %s", (new_balance, customer_id))
        connect.commit()
        print(f"{amount} added to the wallet successfully for customer ID {customer_id}.")
    except mysql.connector.Error as e:
        print(f"An error occurred in add_money_to_wallet: {e}")
        # Rollback the transaction
        connect.rollback()
    finally:
        # Close the MySQL connection after execution
        cursor.close()
        connect.close()

# Define customer ID and amount
customer_id = 1
amount = 100 # Amount to add to/deduct from the wallet

# Create threads for deducting money from the wallet and adding money to the wallet

thread2 = threading.Thread(target=add_money_to_wallet, args=(customer_id, amount))
thread1 = threading.Thread(target=deduct_money_from_wallet, args=(customer_id, amount))


# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to finish execution
thread1.join()
thread2.join()


#in this as you can see that I have done roll back for both the transactions but still there is a dirty read and it cannot be recovered maney
#gets updated in wrong way
#this is non conflicting for sure



"""
A dirty read occurs when one transaction reads data that has been modified by another transaction but not yet committed. In this scenario, if the transaction that made the modification is rolled back, the data read by the first transaction becomes invalid. Let's illustrate this with an example:

Suppose we have two transactions:

Transaction A: Reads a customer's wallet balance and then deducts some money from it.
Transaction B: Simultaneously reads the same customer's wallet balance and then adds some money to it.
If Transaction A reads the wallet balance first (before Transaction B commits its changes) and then Transaction B rolls back, Transaction A will have read incorrect data (dirty read). Even if Transaction A rolls back after reading the incorrect data, the inconsistency caused by the dirty read cannot be fully recovered.
"""

