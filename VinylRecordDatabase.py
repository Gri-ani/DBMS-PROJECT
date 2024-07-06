import mysql
from mysql.connector import errors
from mysql.connector import Error
import uuid
import time
import mysql.connector
import re
import time
import mysql.connector
from datetime import date, datetime
from datetime import timedelta
connect = mysql.connector.connect(user='root', password='Grishma_12345@iiitd', host='localhost', database='BACKEND')
cursor_ = connect.cursor()



def customer_creation(connect):
    try:
        # Collect customer data
        customer_id = input("Enter the ID of the customer: ")
        email = input("Enter the email of the customer: ")
        password = input("Enter the password of the customer: ")
        first_name = input("Enter the first name of the customer: ")
        last_name = input("Enter the last name of the customer: ")
        # age = int(input("Enter the age of the customer: "))
        street_address = input("Enter the street address of the customer: ")
        city = input("Enter the city of the customer: ")
        state = input("Enter the state of the customer: ")
        contact_number = input("Enter the contact number of the customer: ")

        # Attempt to insert the new customer record
        cursor = connect.cursor()
        query = """
        INSERT INTO Customer (customer_id, email, password, first_name, last_name, street_address, city, state, contact_number) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            customer_id, email, password, first_name, last_name, street_address, city, state, contact_number))
        connect.commit()
        print("Customer added successfully!")
        # break;
    except mysql.connector.IntegrityError as e:
        print("A customer with the provided email or ID already exists." if '1062' in str(e) else f"An error occurred: {e}")
    except Error as err:
        print(f"An error occurred: {err}")
    except ValueError as ve:
        print("Invalid input. Please ensure all inputs are correct and try again.")

def add_genre():
    genre_id = int(input("Enter the genre ID: "))
    genre_name = input("Enter the genre name: ")
    cursor = connect.cursor()
    query = "INSERT INTO GENRE (GENRE_ID, GENRE_name) VALUES (%s, %s)"
    cursor.execute(query, (genre_id, genre_name))
    connect.commit()
    print("Genre added successfully!")

def view_genres():
    cursor = connect.cursor()
    query = "SELECT GENRE_ID, GENRE_name FROM GENRE ORDER BY GENRE_ID"
    cursor.execute(query)
    result = cursor.fetchall()
    print("Genre ID --- Genre Name")
    for genre in result:
        print(f"{genre[0]} --- {genre[1]}")


def view_artists():
    cursor = connect.cursor()
    query = "SELECT ARTIST_ID, ARTIST_name FROM ARTIST ORDER BY ARTIST_ID"
    cursor.execute(query)
    result = cursor.fetchall()
    print("Artist ID --- Artist Name")
    for artist in result:
        print(f"{artist[0]} --- {artist[1]}")


def view_products():
    cursor = connect.cursor()
    # Adjusted the query to match the table schema you've provided
    query = """SELECT product_id, title, artist, genre, release_year, vinyl_condition, price, 
               inventory_status, seller_id, product_quantity, product_discount FROM Product"""
    cursor.execute(query)
    result = cursor.fetchall()
    # Adjusted the print statement to include all relevant columns from your table
    print(
        "Product ID --- Title --- Artist --- Genre --- Release Year --- Vinyl Condition --- Price --- Inventory Status --- Seller ID --- Product Quantity --- Product Discount")
    for product in result:
        print(
            f"{product[0]} --- {product[1]} --- {product[2]} --- {product[3]} --- {product[4]} --- {product[5]} --- {product[6]} --- {product[7]} --- {product[8]} --- {product[9]} --- {product[10]}")


def view_cart(customer_id, connect):
    """Function to view the cart of a customer"""
    if connect is not None:
        cursor = connect.cursor()

        # Using parameterized query to prevent SQL injection
        query = """SELECT c.customer_ID, p.product_id, p.title, p.price, c.quantity 
                   FROM Cart c 
                   JOIN Product p ON c.product_ID = p.product_id 
                   WHERE c.customer_ID = %s;"""
        try:
            cursor.execute(query, (customer_id,))
            results = cursor.fetchall()

            if results:
                print("Customer ID --- Product ID --- Product Title --- Product Price --- Quantity")
                for result in results:
                    print(f"{result[0]} --- {result[1]} --- {result[2]} --- {result[3]} --- {result[4]}")
            else:
                print("The cart is empty.")

        except Error as e:
            print(f"A database error occurred: {e}")



def check_wallet_amount(id):
    try:
        cursor2 = connect.cursor()
        # It's better to use parameterized queries to prevent SQL injection
        query = "SELECT wallet_amount FROM wallet WHERE customer_id = %s"
        cursor2.execute(query, (id,))
        result = cursor2.fetchall()

        if result:
            print("Wallet Balance is: ", result[0][0])
        else:
            print("No wallet found for the given customer ID.")

    except Exception as e:
        print(f"An error occurred: {e}")



def add_money_to_wallet(id):
    try:
        # Connect to your database
        cursor2 = connect.cursor()

        # Get the amount to add
        amount_input = input("Enter the amount: ")

        # Validate the input to ensure it's a positive integer
        try:
            amount = int(amount_input)
            if amount <= 0:
                print("Please enter a positive amount.")
                return
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return

        # First, check if a wallet entry exists for this customer ID
        check_query = "SELECT wallet_amount FROM wallet WHERE customer_id = %s"
        cursor2.execute(check_query, (id,))
        result = cursor2.fetchone()

        if result:
            # If a wallet entry exists, update it
            update_query = "UPDATE wallet SET wallet_amount = wallet_amount + %s WHERE customer_id = %s"
            cursor2.execute(update_query, (amount, id))
        else:
            # If no wallet entry exists, create it with the initial amount
            insert_query = "INSERT INTO wallet (customer_id, wallet_amount) VALUES (%s, %s)"
            cursor2.execute(insert_query, (id, amount))

        # Commit the transaction to make sure the changes are saved
        connect.commit()

        if cursor2.rowcount > 0:
            print("Transaction successful.")
        else:
            print("No changes were made. Please check the customer ID.")

    except Exception as e:
        # Handle any other errors that occur during the process
        print(f"An error occurred: {e}")

def add_to_cart(cust_id):
    cursor = connect.cursor(buffered=True)

    # Ask for the product ID
    prod_id = int(input("Enter the product ID: "))

    # Check if the product ID exists in the Product table
    cursor.execute("SELECT product_quantity FROM Product WHERE product_id = %s", (prod_id,))
    prod = cursor.fetchone()

    if not prod:
        print("Wrong product ID.")
        return

    available_quantity = prod[0]
    quantity = int(input("Enter the quantity: "))

    # Check if the requested quantity is available
    if quantity > available_quantity:
        print(f"Requested quantity exceeds available stock. Only {available_quantity} items available.")
        return

    # Check if the product already exists in the user's cart
    cursor.execute("SELECT quantity FROM Cart WHERE customer_ID = %s AND product_ID = %s", (cust_id, prod_id))
    result = cursor.fetchone()

    if result:
        new_quantity = result[0] + quantity
        if new_quantity > available_quantity:
            print(f"Unable to add {quantity} more items to the cart. It exceeds the available stock.")
            return
        # Update cart quantity if it does not exceed available stock
        query_update = "UPDATE Cart SET quantity = %s WHERE customer_ID = %s AND product_ID = %s"
        cursor.execute(query_update, (new_quantity, cust_id, prod_id))
        print("Cart updated successfully.")
    else:
        # Product not in cart, insert as new item
        query_insert = "INSERT INTO Cart (customer_ID, product_ID, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query_insert, (cust_id, prod_id, quantity))
        print("Product added to cart successfully.")

    connect.commit()



def remove_from_cart(customer_id):
    cursor = connect.cursor(buffered=True)

    cursor.execute("select * from product")

    product_id = int(input("Enter the product id: "))
    quantity_to_remove = int(input("Enter the quantity to remove: "))

    # Check if the product is in the cart for this customer
    query_check = "SELECT quantity FROM Cart WHERE customer_ID = %s AND product_ID = %s"
    cursor.execute(query_check, (customer_id, product_id))
    result = cursor.fetchone()

    if result:
        current_quantity = result[0]
        new_quantity = current_quantity - quantity_to_remove

        if new_quantity > 0:
            # Update the quantity in the cart since it's more than zero after removal
            query_update = "UPDATE Cart SET quantity = %s WHERE customer_ID = %s AND product_ID = %s"
            cursor.execute(query_update, (new_quantity, customer_id, product_id))
            print("Cart updated successfully. Quantity reduced.")

        else:
            print("check ur input")
            # because we need that add to wishlist scenario or wishlist linked to save for later
            # Remove the product from the cart since the quantity will be zero or less
            query_delete = "DELETE FROM Cart WHERE customer_ID = %s AND product_ID = %s"
            cursor.execute(query_delete, (customer_id, product_id))
            print("Product removed from cart successfully.")
    else:
        print("Product not found in cart.")

    connect.commit()

def update_customer_details():
    # Step 1: Verify the customer's email and password
    email = input("Enter your current email: ")
    password = input("Enter your current password: ")

    cursor = connect.cursor()
    query = "SELECT customer_id FROM customer WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()

    if result:
        customer_id = result[0]  # Assuming the first column is the customer_id

        # Proceed with the updates
        while True:
            print("\nWhich detail would you like to update?")
            print("1. Change First Name")
            print("2. Change Last Name")
            print("3. Change Password")
            print("4. Change Phone Number")
            print("5. Change Email ID")
            print("6. Change City")
            print("7. Change State")
            print("0. Exit")

            choice = int(input("\nEnter your choice: "))

            if choice == 1:
                new_first_name = input("Enter the new first name: ")
                query = "UPDATE customer SET first_name = %s WHERE customer_id = %s"
            elif choice == 2:
                new_last_name = input("Enter the new last name: ")
                query = "UPDATE customer SET last_name = %s WHERE customer_id = %s"
            elif choice == 3:
                new_password = input("Enter the new password: ")
                query = "UPDATE customer SET password = %s WHERE customer_id = %s"
            elif choice == 4:
                new_phone_number = input("Enter the new phone number: ")
                query = "UPDATE customer SET contact_number = %s WHERE customer_id = %s"
            elif choice == 5:
                new_email = input("Enter the new email: ")
                query = "UPDATE customer SET email = %s WHERE customer_id = %s"
            elif choice == 6:
                new_city = input("Enter the new city: ")
                query = "UPDATE customer SET city = %s WHERE customer_id = %s"
            elif choice == 7:
                new_state = input("Enter the new state: ")
                query = "UPDATE customer SET state = %s WHERE customer_id = %s"
            elif choice == 0:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            if choice in range(1, 8):
                cursor.execute(query, (locals()['new_' + query.split()[3]], customer_id))
                connect.commit()
                print("Details updated successfully.")
    else:
        print("Invalid email or password. Please try again.")


def checkout(connect, customer_id):
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
            # create_before_add_to_order_trigger(connect)
            cursor.execute(update_product_query, (item[2], item[0]))

            tracking_id = int(time.time()) -10100000 +item[4] # Generate tracking ID as order_id + 101
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


def view_tracking_details(order_id):
    cursor = connect.cursor()
    # Fetching order details including order date and time
    query = "SELECT order_date, order_time FROM Order_ WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    order_details = cursor.fetchone()

    if order_details:
        order_date, order_time = order_details
        print(f"Order Date: {order_date}, Order Time: {order_time}")

        # Assuming `order_date` is a date object
        current_date = datetime.now().date()
        days_difference = (current_date - order_date).days

        # Determine the delivery status based on the days difference
        if days_difference < 1:
            status = "Ready for Dispatch"
        elif 1 <= days_difference <= 3:
            status = "Shipment"
        elif 3 < days_difference <= 5:
            status = "Delivery Expected Soon"
        elif 5 < days_difference <= 7:
            status = "In Transit"
        elif days_difference > 7:
            status = "Order Delivered"
        else:
            status = "Processing"

        print(f"Delivery Status: {status}")

        # Optionally, fetch and print tracking status from the TrackingDetails table without location
        tracking_query = "SELECT status FROM TrackingDetails WHERE order_id = %s"
        cursor.execute(tracking_query, (order_id,))
        tracking_details = cursor.fetchall()
        for detail in tracking_details:
            print(f"Tracking Status: {detail[0]}")
    else:
        print("No order found with the provided ID.")




def cancel_order_and_delete_( customer_id, order_id):
    try:
        cursor = connect.cursor()

        # Step 1: Check order eligibility for cancellation
        query = "SELECT order_date, payment_amount FROM Order_ WHERE order_id = %s AND customer_id = %s"
        cursor.execute(query, (order_id, customer_id))
        order_details = cursor.fetchone()

        if not order_details:
            print("Order not found or you do not have permission to cancel this order.")
            return

        order_date, payment_amount = order_details
        current_date = datetime.now().date()
        days_difference = (current_date - order_date).days

        if days_difference >= 2:
            print("Cancellation period has expired. Unable to cancel the order.")
            return

        # Calculate refund amount
        refund_amount = payment_amount

        # Update wallet balance
        update_wallet_query = "UPDATE Wallet SET wallet_amount = wallet_amount + %s WHERE customer_ID = %s"
        cursor.execute(update_wallet_query, (refund_amount, customer_id))

        # Delete the order
        delete_order_query = "DELETE FROM Order_ WHERE order_id = %s AND customer_id = %s"
        cursor.execute(delete_order_query, (order_id, customer_id))

        connect.commit()
        print("Order has been successfully cancelled, payment refunded, and the order entry deleted.")
    except Exception as e:
        connect.rollback()  # Rollback in case of error
        print(f"Failed to cancel and delete the order: {e}")
    finally:
        cursor.close()

# def cancel_order_and_delete(customer_id, order_id):
#     cursor = connect.cursor()
#
#     # Step 1: Check order eligibility for cancellation
#     query = "SELECT order_date FROM Order_ WHERE order_id = %s AND customer_id = %s"
#     cursor.execute(query, (order_id, customer_id))
#     order_details = cursor.fetchone()
#
#     if not order_details:
#         print("Order not found or you do not have permission to cancel this order.")
#         return
#
#     order_date = order_details[0]
#     current_date = datetime.now().date()
#     days_difference = (current_date - order_date).days
#
#     if days_difference >= 1:
#         print("Cancellation period has expired. Unable to cancel the order.")
#         return
#
#     # Assuming the refund amount is either known or obtained through other means (e.g., user input)
#
#     try:
#         # Directly update Wallet balance
#         update_wallet_query = "UPDATE Wallet SET wallet_amount = wallet_amount + %s WHERE customer_ID = %s"
#         cursor.execute(update_wallet_query, (refund_amount, customer_id))
#
#         # Delete the order
#         delete_order_query = "DELETE FROM Order_ WHERE order_id = %s AND customer_id = %s"
#         cursor.execute(delete_order_query, (order_id, customer_id))
#
#         connect.commit()
#         print("Order has been successfully cancelled, payment refunded, and the order entry deleted.")
#     except Exception as e:
#         connect.rollback()  # Rollback in case of error
#         print(f"Failed to cancel and delete the order: {e}")
#     finally:
#         cursor.close()



def view_order(customer_id):
    try:
        # Assuming 'connect' is a valid database connection object
        cursor = connect.cursor()

        # SQL query to select orders for the given customer_id
        query = """
        SELECT order_ID, order_date, order_time, product_id, customer_id, tracking_id, delivery_date, seller_id, 
        payment_amount
        FROM order_
        WHERE customer_id = %s
        ORDER BY order_date DESC, order_time DESC
        """
        cursor.execute(query, (customer_id,))

        # Fetch all matching records
        orders = cursor.fetchall()

        if orders:
            print(f"Orders for Customer ID {customer_id}:")
            for order in orders:
                print(f"Order ID: {order[0]}, Date: {order[1]}, Time: {order[2]}, Product ID: {order[3]}, "
                      f"Tracking ID: {order[5]}, Delivery Date: {order[6]}, Seller ID: {order[7]}, Payment Amount: {order[8]}")
        else:
            print("No orders found for the given Customer ID.")

    except Exception as e:
        print(f"An error occurred: {e}")


def create_trigger_email_format_check(connect):
    try:
        cursor = connect.cursor()
        trigger_command = """
        CREATE TRIGGER Check_Email_Format
        BEFORE INSERT ON Seller
        FOR EACH ROW
        BEGIN
            DECLARE email_pattern VARCHAR(100);
            SET email_pattern = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}';
            IF NEW.email NOT REGEXP email_pattern THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid email format';
            END IF;
        END;
        """
        cursor.execute(trigger_command)
        connect.commit()
        print("Trigger 'Check_Email_Format' created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_trigger_capitalize_names(connect):
    try:
        cursor = connect.cursor()
        trigger_command = """
        CREATE TRIGGER Capitalize_Seller_Names
        BEFORE INSERT ON Seller
        FOR EACH ROW
        BEGIN
            SET NEW.seller_name = CONCAT(UCASE(LEFT(NEW.seller_name, 1)), LCASE(SUBSTRING(NEW.seller_name, 2)));
        END;
        """
        cursor.execute(trigger_command)
        connect.commit()
        print("Trigger 'Capitalize_Seller_Names' created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")






def customer_login(connect, cursor_):
    max_login_attempts = 3
    login_attempts = 0

    while True:
        print()
        print("Welcome to the login page for Customers.")
        print("Press 1 if you want to login")
        print("Press 2 if you want to signup")
        print("Press 0 to get to the Previous Menu")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            while True:
                if login_attempts >= max_login_attempts:
                    print(f"Maximum login attempts reached. Please wait for 10 seconds before trying again.")
                    time.sleep(10)  # Wait for 10 seconds before allowing another attempt
                    login_attempts = 0  # Reset login attempts counter after the waiting period

                customer_username = input("Enter your email: ")
                customer_password = input("Enter your password: ")



                # Check customer credentials
                query = "SELECT customer_id FROM customer WHERE email = %s AND password = %s"
                cursor_.execute(query, (customer_username, customer_password))
                result = cursor_.fetchone()

                if result:
                    customer_id = result[0]
                    print(f"Customer ID: {customer_id}")
                    print("Welcome to the customer menu!")

                    while True:
                        print()
                        print("1. Change Personal Details")
                        print("2. View Genres")
                        print("3. view artists")
                        print("4. View Products")
                        print("5. View Cart")
                        print("6. Add Money to Wallet")
                        print("7. Check Wallet Balance")
                        print("8. Remove Product from Cart")
                        print("9. Add Products to Cart")
                        print("10. View Orders")
                        print("11. Checkout")
                        print("12. View Delivery Status/tracking details")
                        # print("13. Resell")
                        # print("14. View Product ratings")
                        # print("16. Add Product Ratings")
                        # print("17. Remove Product Ratings")
                        print("22. Cancel order")
                        print("0. Exit")

                        choice = int(input("Enter your choice:"))
                        if choice == 1:
                            update_customer_details()

                        if choice == 2:
                            view_genres()
                        if choice == 3:
                            view_artists()

                        if choice == 4:
                            view_products()

                        if choice == 5:
                            view_cart(customer_id, connect)

                        if choice == 6:
                            add_money_to_wallet(customer_id)
                        if choice == 7:
                            check_wallet_amount(customer_id)

                        if choice == 8:
                            remove_from_cart(customer_id)

                        if choice == 9:
                            add_to_cart(customer_id)

                        if choice == 10:
                            view_order(customer_id)

                        if choice == 11:
                            checkout(connect, customer_id)

                        if choice == 12:
                            order_id = input("Enter order id:")
                            view_tracking_details(order_id)

                        # if choice == 13:
                            # resell_product(connect, cursor_, customer_id)

                        if choice == 14:
                            view_all_ratings(customer_id, connect)

                        if choice == 16:
                            add_rating()


                        if choice == 22:
                            order_id = input("Enter the order id:")
                            cancel_order_and_delete_(customer_id, order_id)

                        if choice == 0:
                            return
                    break
                else:
                    print("Incorrect email or password.")
                    login_attempts += 1
        elif choice == 2:
            customer_creation(connect)
        elif choice == 0:
            print("Exiting...")
            return
        else:
            print("Invalid choice. Please enter a valid option.")





def generate_seller_id(cursor):
    # Fetch the seller ID of the last entry in the Seller table
    query = "SELECT MAX(seller_ID) FROM Seller"
    cursor.execute(query)
    result = cursor.fetchone()
    last_seller_id = result[0]

    # If there are no existing sellers, start from seller_ID 1
    if last_seller_id is None:
        new_seller_id = 1
    else:
        new_seller_id = last_seller_id + 1

    return new_seller_id

def generate_reseller_id(cursor):
    # Fetch the seller ID of the last entry in the Seller table
    query = "SELECT MAX(reseller_ID) FROM Reseller"
    cursor.execute(query)
    result = cursor.fetchone()
    last_seller_id = result[0]

    # If there are no existing sellers, start from seller_ID 1
    if last_seller_id is None:
        new_seller_id = 1
    else:
        new_seller_id = last_seller_id + 1

    return new_seller_id



def seller_creation(connect):
    try:
        seller_ID = int(input("Enter the ID of the seller: "))
        seller_name = input("Enter the name of the seller: ")
        email = input("Enter the email of the seller: ")
        seller_password = input("Enter the password of the seller: ")
        seller_phone_number = input("Enter the phone number of the seller: ")
        seller_city = input("Enter the city of the seller: ")
        seller_state = input("Enter the state of the seller: ")

        cursor = connect.cursor()
        query = """
        INSERT INTO Seller (seller_ID, seller_name, email, seller_password, seller_phone_number, seller_city, seller_state)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (seller_ID, seller_name, email, seller_password, seller_phone_number, seller_city, seller_state))
        connect.commit()
        print("Seller added successfully!")
    except mysql.connector.Error as e:
        if isinstance(e, mysql.connector.IntegrityError):
            error_message = str(e)
            if '1062' in error_message:  # Check if it's a duplicate entry error
                if 'email' in error_message:
                    print("A seller with the provided email already exists.")
                elif 'seller_ID' in error_message:
                    print("A seller with the provided ID already exists.")
                else:
                    print("A seller with the provided email or ID already exists.")
            else:
                print("An integrity error occurred while trying to add the seller:", e)
        else:
            print("A database error occurred:", e)


# def seller_creation_(connect):
#     try:
#         seller_ID = int(input("Enter the ID of the seller: "))
#         seller_name = input("Enter the name of the seller: ")
#         email = input("Enter the email of the seller: ")
#         seller_password = input("Enter the password of the seller: ")
#         seller_phone_number = input("Enter the phone number of the seller: ")
#         seller_city = input("Enter the city of the seller: ")
#         seller_state = input("Enter the state of the seller: ")
#
#         cursor = connect.cursor()
#         query = """
#         INSERT INTO Seller (seller_ID, seller_name, email, seller_password, seller_phone_number, seller_city, seller_state)
#         VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """
#         cursor.execute(query, (seller_ID, seller_name, email, seller_password, seller_phone_number, seller_city, seller_state))
#         connect.commit()
#         print("Seller added successfully!")
#     except mysql.connector.Error as e:
#         if isinstance(e, mysql.connector.IntegrityError):
#             error_message = str(e)
#             if '1062' in error_message:  # Check if it's a duplicate entry error
#                 print("A seller with the provided email or ID already exists.")
#             else:
#                 print("An integrity error occurred while trying to add the seller:", e)
#         else:
#             print("A database error occurred:", e)

def add_product():
    product_id = int(input("Enter the product ID: "))
    title = input("Enter the product title: ")
    artist_name = input("Enter the artist name: ")
    genre = input("Enter the genre: ")
    release_year = int(input("Enter the release year: "))
    vinyl_condition = input("Enter the vinyl condition: ")
    price = float(input("Enter the price: "))
    inventory_status = input("Enter the inventory status: ")
    seller_id = int(input("Enter the seller ID: "))
    product_quantity = int(input("Enter the product quantity: "))
    product_discount = int(input("Enter the product discount: "))

    cursor = connect.cursor()

    # Check if the artist exists in the ARTIST table
    query = "SELECT ARTIST_ID FROM ARTIST WHERE ARTIST_name = %s"
    cursor.execute(query, (artist_name,))
    result = cursor.fetchone()

    if result:
        artist_id = result[0]
    else:
        # Generate a random artist ID of 3 digits
        artist_id = random.randint(100, 999)

        # Insert the new artist into the ARTIST table
        query = "INSERT INTO ARTIST (ARTIST_ID, ARTIST_name) VALUES (%s, %s)"
        cursor.execute(query, (artist_id, artist_name))
        connect.commit()

    # Insert the product into the Product table
    query = """INSERT INTO Product (product_id, title, artist, genre, release_year, vinyl_condition, price, 
              inventory_status, seller_id, product_quantity, product_discount) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (product_id, title, artist_id, genre, release_year, vinyl_condition, price,
                           inventory_status, seller_id, product_quantity, product_discount))
    connect.commit()
    print("Product added successfully!")

    return



def add_artist(artist_name, artist_id):
    cursor = connect.cursor()
    try:
        # Check if the artist already exists
        if get_artist_id(artist_name):
            print("Artist already exists in the database.")
            return

        # If the artist doesn't exist, insert it into the ARTIST table
        cursor.execute("INSERT INTO ARTIST (ARTIST_ID,ARTIST_name) VALUES (%s,%s)",(artist_id, artist_name,))
        connect.commit()
        print("Artist added successfully.")
    except Exception as e:
        print("Error adding artist:", e)
    cursor.close()

def get_artist_id(artist_name):
    cursor = connect.cursor()
    try:
        # Query the ARTIST table to get the ID of the artist
        cursor.execute("SELECT ARTIST_ID FROM ARTIST WHERE ARTIST_name = %s", (artist_name,))
        artist_id = cursor.fetchone()
        if artist_id:
            return artist_id[0]
        else:
            return None
    except Exception as e:
        print("Error fetching artist ID:", e)
        return None
    cursor.close()



#
def view_sales_and_order_history(seller_id):
    cursor = connect.cursor()

    # Query to identify top selling products by seller
    query_top_selling_products = """
    SELECT s.seller_id, s.first_name, s.last_name, p.product_id, p.title, p.artist, SUM(oi.quantity) AS total_sold
    FROM Seller s
    JOIN Product p ON s.seller_id = p.seller_id
    JOIN OrderItem oi ON p.product_id = oi.product_id
    WHERE s.seller_id = %s
    GROUP BY s.seller_id, p.product_id
    ORDER BY total_sold DESC
    """
    cursor.execute(query_top_selling_products, (seller_id,))
    top_selling_products = cursor.fetchall()

    if top_selling_products:
        print("Top Selling Products by Seller:")
        print("Seller ID --- First Name --- Last Name --- Product ID --- Title --- Artist --- Total Sold")
        for sale in top_selling_products:
            print(f"{sale[0]} --- {sale[1]} --- {sale[2]} --- {sale[3]} --- {sale[4]} --- {sale[5]} --- {sale[6]}")
    else:
        print("No sales history found for this seller.")

    # Query to identify top genre preferences by customer
    query_top_genre_preferences = """
    SELECT c.customer_id, c.first_name, c.last_name, p.genre, COUNT(*) AS genre_count
    FROM Customer c
    JOIN Orders o ON c.customer_id = o.customer_id
    JOIN OrderItem oi ON o.order_id = oi.order_id
    JOIN Product p ON oi.product_id = p.product_id
    GROUP BY c.customer_id, c.first_name, c.last_name, p.genre
    ORDER BY genre_count DESC
    """
    cursor.execute(query_top_genre_preferences)
    top_genre_preferences = cursor.fetchall()

    if top_genre_preferences:
        print("\nTop Genre Preferences by Customer:")
        print("Customer ID --- First Name --- Last Name --- Genre --- Genre Count")
        for preference in top_genre_preferences:
            print(f"{preference[0]} --- {preference[1]} --- {preference[2]} --- {preference[3]} --- {preference[4]}")
    else:
        print("No genre preferences found.")

def sales_analytics(seller_id):
    cursor = connect.cursor()

    try:
        # Total revenue generated by the seller
        query_total_revenue = """
            SELECT SUM(Product.price * Order_.product_quantity) AS total_revenue
            FROM Order_
            INNER JOIN Product ON Order_.product_id = Product.product_id
            WHERE Order_.seller_id = %s
        """
        cursor.execute(query_total_revenue, (seller_id,))
        total_revenue_result = cursor.fetchone()
        total_revenue = total_revenue_result[0] if total_revenue_result[0] else 0

        print("Total Revenue:", total_revenue)

        # Number of orders received by the seller
        query_num_orders = """
            SELECT COUNT(order_ID) AS num_orders
            FROM Order_
            WHERE seller_id = %s
        """
        cursor.execute(query_num_orders, (seller_id,))
        num_orders_result = cursor.fetchone()
        num_orders = num_orders_result[0] if num_orders_result[0] else 0

        print("Number of Orders:", num_orders)

        # Average order value
        if num_orders > 0:
            avg_order_value = total_revenue / num_orders
            print("Average Order Value:", avg_order_value)
        else:
            print("Average Order Value: N/A (No orders)")

        # Best-selling products by quantity
        query_best_selling_products = """
            SELECT Product.title, SUM(Order_.product_quantity) AS total_quantity
            FROM Order_
            INNER JOIN Product ON Order_.product_id = Product.product_id
            WHERE Order_.seller_id = %s
            GROUP BY Product.product_id
            ORDER BY total_quantity DESC
            LIMIT 5
        """
        cursor.execute(query_best_selling_products, (seller_id,))
        best_selling_products = cursor.fetchall()

        print("Best-selling Products (by quantity):")
        for row in best_selling_products:
            product_title, total_quantity = row
            print(f"{product_title}: {total_quantity} units")

        # Most profitable products
        query_most_profitable_products = """
            SELECT Product.title, SUM(Product.price * Order_.product_quantity) AS total_profit
            FROM Order_
            INNER JOIN Product ON Order_.product_id = Product.product_id
            WHERE Order_.seller_id = %s
            GROUP BY Product.product_id
            ORDER BY total_profit DESC
            LIMIT 5
        """
        cursor.execute(query_most_profitable_products, (seller_id,))
        most_profitable_products = cursor.fetchall()

        print("Most Profitable Products:")
        for row in most_profitable_products:
            product_title, total_profit = row
            print(f"{product_title}: ${total_profit}")

    except mysql.connector.Error as err:
        print("Error:", err)

    cursor.close()


def edit_vinyl_listing(product_id):
    cursor = connect.cursor()
    query = "SELECT * FROM Product WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    product_info = cursor.fetchone()

    if product_info:
        print("Current Vinyl Record Information:")
        print("1. Artist:", product_info[2])
        print("2. Genre:", product_info[3])
        print("3. Release Year:", product_info[4])
        print("4. Vinyl Condition:", product_info[5])
        print("5. Price:", product_info[6])
        print("6. Inventory Status:", product_info[7])

        choice = int(input("\nEnter the number corresponding to the detail you want to edit (0 to exit): "))

        if choice == 0:
            print("Exiting...")
            return

        elif choice == 1:
            artist_id = int(input("Enter the new artist ID: "))
            query = "UPDATE Product SET artist = (SELECT ARTIST_name FROM ARTIST WHERE ARTIST_ID = %s) WHERE product_id = %s"
            cursor.execute(query, (artist_id, product_id))

        elif choice == 2:
            genre_id = int(input("Enter the new genre ID: "))
            query = "UPDATE Product SET genre = (SELECT GENRE_name FROM GENRE WHERE GENRE_ID = %s) WHERE product_id = %s"
            cursor.execute(query, (genre_id, product_id))

        elif choice == 3:
            new_release_year = int(input("Enter the new release year: "))
            query = "UPDATE Product SET release_year = %s WHERE product_id = %s"
            cursor.execute(query, (new_release_year, product_id))

        elif choice == 4:
            new_vinyl_condition = input("Enter the new vinyl condition: ")
            query = "UPDATE Product SET vinyl_condition = %s WHERE product_id = %s"
            cursor.execute(query, (new_vinyl_condition, product_id))

        elif choice == 5:
            new_price = float(input("Enter the new price: "))
            query = "UPDATE Product SET price = %s WHERE product_id = %s"
            cursor.execute(query, (new_price, product_id))

        elif choice == 6:
            new_inventory_status = input("Enter the new inventory status: ")
            query = "UPDATE Product SET inventory_status = %s WHERE product_id = %s"
            cursor.execute(query, (new_inventory_status, product_id))

        else:
            print("Invalid choice. Please try again.")
            return

        connect.commit()
        print("Vinyl record details updated successfully.")

    else:
        print("Vinyl record not found.")


def remove_vinyl_listing(product_id):
    cursor = connect.cursor()
    query = "DELETE FROM Ratings WHERE product_ID = %s"
    cursor.execute(query, (product_id,))
    query = "DELETE FROM Cart WHERE product_ID = %s"
    cursor.execute(query, (product_id,))
    query = "DELETE FROM Product WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    connect.commit()
    print("Vinyl listing removed successfully.")


def edit_seller_details(seller_id):
    cursor = connect.cursor()
    query = "SELECT * FROM Seller WHERE seller_ID = %s"
    cursor.execute(query, (seller_id,))
    seller_info = cursor.fetchone()

    if seller_info:
        print("Current Seller Information:")
        print("1. Email:", seller_info[1])
        print("2. Contact Number:", seller_info[4])
        print("3. City:", seller_info[5])
        print("4. State:", seller_info[6])

        choice = int(input("\nEnter the number corresponding to the detail you want to edit (0 to exit): "))

        if choice == 0:
            print("Exiting...")
            return

        elif choice == 1:
            new_email = input("Enter the new email: ")
            query = "UPDATE Seller SET email = %s WHERE seller_ID = %s"
            cursor.execute(query, (new_email, seller_id))

        elif choice == 2:
            new_contact_number = input("Enter the new contact number: ")
            query = "UPDATE Seller SET seller_phone_number = %s WHERE seller_ID = %s"
            cursor.execute(query, (new_contact_number, seller_id))

        elif choice == 3:
            new_city = input("Enter the new city: ")
            query = "UPDATE Seller SET seller_city = %s WHERE seller_ID = %s"
            cursor.execute(query, (new_city, seller_id))

        elif choice == 4:
            new_state = input("Enter the new state: ")
            query = "UPDATE Seller SET seller_state = %s WHERE seller_ID = %s"
            cursor.execute(query, (new_state, seller_id))

        else:
            print("Invalid choice. Please try again.")
            return

        connect.commit()
        print("Seller details updated successfully.")

    else:
        print("Seller not found.")



def search_by_title(title_query):
    cursor = connect.cursor()
    query = """
    SELECT * FROM Product WHERE title LIKE %s
    """
    cursor.execute(query, ('%' + title_query + '%',))
    result = cursor.fetchall()

    if result:
        print("Search Results:")
        print("Product ID --- Title --- Artist --- Genre --- Release Year --- Price --- Inventory Status")
        for row in result:
            print(f"{row[0]} --- {row[1]} --- {row[2]} --- {row[3]} --- {row[4]} --- {row[6]} --- {row[7]}")
            return
    else:
        print("No products found matching the title.")
        return



def search_by_artist(artist_query):
    cursor = connect.cursor()
    query = """
    SELECT * FROM Product WHERE artist LIKE %s
    """
    cursor.execute(query, ('%' + artist_query + '%',))
    result = cursor.fetchall()

    if result:
        print("Search Results:")
        print("Product ID --- Title --- Artist --- Genre --- Release Year --- Price --- Inventory Status")
        for row in result:
            print(f"{row[0]} --- {row[1]} --- {row[2]} --- {row[3]} --- {row[4]} --- {row[6]} --- {row[7]}")
    else:
        print("No products found matching the artist.")


############################################### NUMBER 7777777777777777777777 ########################################################################################3

def show_running_orders(seller_id):
    cursor = connect.cursor()

    # Query to select running orders for the seller
    query = """
        SELECT Order_.order_ID, Order_.order_date, Order_.delivery_date, Product.title, Product.price, Order_.product_quantity
        FROM Order_
        INNER JOIN Product ON Order_.product_id = Product.product_id
        WHERE Order_.seller_id = %s AND Order_.delivery_date IS NULL
        ORDER BY Order_.order_date
    """

    try:
        # Execute the query
        cursor.execute(query, (seller_id,))

        # Fetch all results
        results = cursor.fetchall()

        # Print the header
        print("Running Orders:")
        print("{:<10} {:<15} {:<15} {:<50} {:<10} {:<10}".format("Order ID", "Order Date", "Delivery Date", "Product Title", "Price", "Quantity"))
        print("-" * 110)

        # Print each running order
        for row in results:
            order_id, order_date, delivery_date, product_title, price, quantity = row
            print("{:<10} {:<15} {:<15} {:<50} {:<10} {:<10}".format(order_id, order_date, delivery_date or "Not delivered", product_title, price, quantity))

    except mysql.connector.Error as err:
        print("Error:", err)

    cursor.close()



################################################    NUMBER 8888888888888 ##################################################################################################################################
def calculate_total_revenue(seller_id):
    try:

        cursor = connect.cursor()

        # Construct the SQL query to calculate the total revenue of the seller
        revenue_query = """
            SELECT SUM(payment_amount) 
            FROM Order_ 
            WHERE seller_id = %s
        """

        # Execute the query
        cursor.execute(revenue_query, (seller_id,))

        # Fetch the total revenue
        total_revenue = cursor.fetchone()[0]

        print(f"Total revenue of seller with ID {seller_id}: ${total_revenue}")

    except Exception as e:
        # Handle any errors that occur during the process
        print(f"An error occurred: {e}")


def get_previous_orders_of_seller(seller_id):
    try:

        cursor = connect.cursor()

        orders_query = """
            SELECT * 
            FROM Order_ 
            WHERE seller_id = %s
        """

        # Execute the query
        cursor.execute(orders_query, (seller_id,))

        # Fetch all previous orders
        previous_orders = cursor.fetchall()

        print(f"Previous orders of seller with ID {seller_id}:")
        for order in previous_orders:
            print(order)

    except Exception as e:

        print(f"An error occurred: {e}")

def search_by_genre(genre_query):
    cursor = connect.cursor()
    query = """
    SELECT * FROM Product WHERE genre LIKE %s
    """
    cursor.execute(query, ('%' + genre_query + '%',))
    result = cursor.fetchall()

    if result:
        print("Search Results:")
        print("Product ID --- Title --- Artist --- Genre --- Release Year --- Price --- Inventory Status")
        for row in result:
            print(f"{row[0]} --- {row[1]} --- {row[2]} --- {row[3]} --- {row[4]} --- {row[6]} --- {row[7]}")
    else:
        print("No products found matching the genre.")

############################################# NUMBER 222222222222222222222222222222222222222222222222222222222
def search_product_by_id(product_id):
    cursor = connect.cursor()
    query = """
    SELECT * FROM Product WHERE product_id = %s
    """
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()

    if result:
        print("Product found:")
        print("Product ID --- Title --- Artist --- Genre --- Release Year --- Price --- Inventory Status")
        print(
            f"{result[0]} --- {result[1]} --- {result[2]} --- {result[3]} --- {result[4]} --- {result[6]} --- {result[7]}")
    else:
        print("Product not found.")


def search_by_release_year(release_year_query):
    cursor = connect.cursor()
    query = """
    SELECT * FROM Product WHERE release_year = %s
    """
    cursor.execute(query, (release_year_query,))
    result = cursor.fetchall()

    if result:
        print("Search Results:")
        print("Product ID --- Title --- Artist --- Genre --- Release Year --- Price --- Inventory Status")
        for row in result:
            print(f"{row[0]} --- {row[1]} --- {row[2]} --- {row[3]} --- {row[4]} --- {row[6]} --- {row[7]}")
    else:
        print("No products found matching the release year.")
############################################## NUMBER 11111111111111111111111111111111111111111111111111111
def search_category():
    print("Search by Category:")
    print("1. Title")
    print("2. Artist")
    print("3. Genre")
    print("4. Release Year")
    print("0. Exit")

    choice = input("Enter the number corresponding to the category you want to search in: ")

    if choice == '1':
        title_query = input("Enter the title you want to search for: ")
        search_by_title(title_query)
    elif choice == '2':
        artist_query = input("Enter the artist you want to search for: ")
        search_by_artist(artist_query)
    elif choice == '3':
        genre_query = input("Enter the genre you want to search for: ")
        search_by_genre(genre_query)
    elif choice == '4':
        release_year_query = int(input("Enter the release year you want to search for: "))
        search_by_release_year(release_year_query)
    elif choice == '0':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Please try again.")


def add_to_cart(cust_id):
    cursor = connect.cursor(buffered=True)

    # Ask for the product ID
    prod_id = int(input("Enter the product ID: "))

    # Check if the product ID exists in the Product table
    cursor.execute("SELECT product_quantity FROM Product WHERE product_id = %s", (prod_id,))
    prod = cursor.fetchone()

    if not prod:
        print("Wrong product ID.")
        return

    available_quantity = prod[0]
    quantity = int(input("Enter the quantity: "))

    # Check if the requested quantity is available
    if quantity > available_quantity:
        print(f"Requested quantity exceeds available stock. Only {available_quantity} items available.")
        return

    # Check if the product already exists in the user's cart
    cursor.execute("SELECT quantity FROM Cart WHERE customer_ID = %s AND product_ID = %s", (cust_id, prod_id))
    result = cursor.fetchone()

    if result:
        new_quantity = result[0] + quantity
        if new_quantity > available_quantity:
            print(f"Unable to add {quantity} more items to the cart. It exceeds the available stock.")
            return
        # Update cart quantity if it does not exceed available stock
        query_update = "UPDATE Cart SET quantity = %s WHERE customer_ID = %s AND product_ID = %s"
        cursor.execute(query_update, (new_quantity, cust_id, prod_id))
        print("Cart updated successfully.")
    else:
        # Product not in cart, insert as new item
        query_insert = "INSERT INTO Cart (customer_ID, product_ID, quantity) VALUES (%s, %s, %s)"
        cursor.execute(query_insert, (cust_id, prod_id, quantity))
        print("Product added to cart successfully.")

    connect.commit()




def main_menu():
    while True:
        print("Submission for final deadline of DBMS")
        print()
        print("Press 1 to continue")
        print("Press 0 to exit")
        a = int(input())
        if a == 0:
            break
        elif a == 1:
            user_menu()

def user_menu():
    while True:
        print("Press 1 if you want to enter as Customer")
        print("Press 2 if you want to enter as Seller")
        print("Press 0 to get to the Previous Menu")
        b = int(input())
        if b == 0:
            break
        elif b == 1:
            customer_login(connect, cursor_)
        elif b == 2:
            seller_login()

def seller_login():
    while True:
        print()
        print("Welcome to the login/signup page of Seller")
        print("Press 1 if you want to login")
        print("Press 2 if you want to signup")
        print("Press 0 to get to the Previous Menu")
        d = int(input())
        if d == 0:
            break
        elif d == 1:
            id = int(input("Enter the id of the seller: "))
            seller_email = input("Enter email: ")
            seller_password = input("Enter the password of Seller: ")
            query = "SELECT email, seller_password FROM seller WHERE seller_id = %s"
            cursor_.execute(query, (id,))
            result = cursor_.fetchall()
            if result and seller_email == result[0][0] and seller_password == result[0][1]:
                print("Welcome to Seller Menu")
                seller_menu(id)
            else:
                print("Wrong username or Password!!")
        elif d == 2:
            seller_creation(connect)

def seller_menu(id):
    while True:
        print()
        print("1. Search Category")
        print("2. Search Product")
        print("3. Add Artist")
        print("4. Add Product")
        print("5. Sales Analytics")
        print("6. Show all previous orders")
        print("7. Show all running orders")
        print("8. Total revenue")
        print("9. Edit vinyl listing")
        print("10. Remove vinyl listing")
        print("11. Edit My details")
        print("To EXIT press 0")
        choice1 = int(input("Enter your choice: "))
        if choice1 == 0:
            break
        elif choice1 == 1:
            search_category()
        elif choice1 == 2:
            product_id = int(input("Enter the product ID you want to search: "))
            search_product_by_id(product_id)
        elif choice1 == 3:
            artist_name = input("Please enter Artist's name: ")
            artistid = input("Enter the artist ID: ")
            add_artist(artist_name, artistid)
        elif choice1 == 4:
            add_product()
        elif choice1 == 5:
            sales_analytics(id)
        elif choice1 == 6:
            get_previous_orders_of_seller(id)
        elif choice1 == 7:
            show_running_orders(id)
        elif choice1 == 8:
            calculate_total_revenue(id)
        elif choice1 == 9:
            product_id = int(input("Enter the product ID of the listing you want to update details of: "))
            edit_vinyl_listing(product_id)
        elif choice1 == 10:
            product_id = int(input("Enter the product ID of the listing you want to delete: "))
            remove_vinyl_listing(product_id)
        elif choice1 == 11:
            edit_seller_details(id)

# Call the main menu to start the program
main_menu()

























































