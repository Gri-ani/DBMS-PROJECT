# Vinyl Record MarketPlace DBMS

Introduction
Welcome to the Vinyl Record Marketplace Transaction Management System README! This system is designed to facilitate seamless interaction with a MySQL database for both customers and sellers. Below, you'll find comprehensive instructions for using the system effectively.

Features Overview
1. Customer Operations
   
-Customer Login and Signup: Log in with existing credentials or sign up to create a new customer account.

-Customer Menu Options:
Change Personal Details: Update personal information such as name, address, etc.

View Genres: Browse through available music genres.
View Artists: Explore the list of artists associated with the products.
View Products: See details of available vinyl records.
View Cart: Check items in the shopping cart.

Add Money to Wallet: Add funds for purchases.

Check Wallet Balance: View current wallet balance.

Remove Product from Cart: Remove items from the shopping cart.

Add Products to Cart: Add desired products to the shopping cart.

View Orders: Review previous orders and their details.

Checkout: Proceed to checkout and place orders.

View Delivery Status/Tracking Details: Track the delivery status of orders.

Cancel Order: Cancel an existing order.

3. Seller Operations
Seller Login and Signup: Log in with seller ID, email, and password or sign up as a new seller.

Seller Menu Options:
Search Category: Find products based on categories.

Search Product: Look up products by ID.

Add Artist: Add new artists to the database.

Add Product: Add new products to the inventory.

Sales Analytics: Analyze sales data and performance metrics.

Show All Previous Orders: View previous orders made by customers.

Show All Running Orders: Check the status of current orders.

Total Revenue: Calculate total revenue generated from sales.

Edit Vinyl Listing: Modify details of existing product listings.

Remove Vinyl Listing: Remove products from the inventory.

Edit My Details: Update seller information such as contact details.

5. Order Management
Order Processing:
Customer: Place orders, view order history, and track delivery status.

Seller: Manage orders, confirm delivery, view sales analytics, and handle product listings.

Order Cancellation:
Customer: Cancel an order before it is shipped. The option is available in the customer menu.
Admin: Monitor and manage order cancellations through the admin panel.

Transaction Management in MySQL:
Overview:
This repository provides examples and scripts for implementing transaction management in MySQL using Python. Transactions are used to ensure data integrity when performing concurrent operations on a database.

Features:
Non-Conflicting Transactions: Examples where multiple operations can run concurrently without data inconsistency, such as updating customer information or placing orders.
Conflicting Transactions: Examples demonstrating potential issues with concurrent operations, such as updating the same product quantity or handling wallet transactions.
