import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from unidecode import unidecode
from helpers import apology, login_required, eur, get_product_by_id
from db import db  # Import the db object from db.py

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["eur"] = eur

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure response arent cached"""
    response.headers["Cache-Control"] = "no-chache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-chache"
    return response


@app.route("/")
@login_required
def index():
    """Show home"""

    # Define variable for user id
    user_id = session["user_id"]

    products = db.execute("SELECT product_id, name, image_url, type FROM products")
    return render_template("index.html", products=products)


@app.route("/shirts", methods=["GET", "POST"])
@login_required
def shirts():
    """Shirts"""

    # Define variable for user id
    user_id = session["user_id"]

    shirts = db.execute(
        "SELECT product_id, name, size, price, team, country, image_url, description FROM products WHERE type = 'Shirt'"
    )
    return render_template("shirts.html", shirts=shirts)


@app.route("/shorts", methods=["GET", "POST"])
@login_required
def shorts():
    """Shorts"""

    # Define variable for user id
    user_id = session["user_id"]

    shorts = db.execute(
        "SELECT product_id, name, size, price, team, country, image_url, description FROM products WHERE type = 'Short'"
    )
    return render_template("shorts.html", shorts=shorts)


@app.route("/accesoires", methods=["GET", "POST"])
@login_required
def accesoires():
    """Accesoires"""

    # Define variable for user id
    user_id = session["user_id"]

    accesoires = db.execute(
        "SELECT product_id, name, size, price, team, country, image_url, description FROM products WHERE type = 'Accesoires'"
    )
    return render_template("accesoires.html", accesoires=accesoires)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user id
    session.clear()

    # When request post
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Username must be provided")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Password must be provided")

        # Query db for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure that username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("Invalid username or password")

        # Remember which user is logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home
        return redirect("/")

    # When via GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():

    # Define user variable
    user_id = session["user_id"]

    if request.method == "GET":
        return render_template("search.html")

    if request.method == "POST":
        search_term = request.form.get("search")

        # Ensure that term is entered
        if not search_term:
            return apology("Search must be provided")

        # Debug line
        print(f"Search term: {search_term}")

        # Normalize search term
        normalized_search_term = unidecode(search_term.lower())

        # degug line
        print(f"normalized search term: {normalized_search_term}")

        # Fetch all products to normalize their fields for matching
        all_products = db.execute(
            "SELECT product_id, name, type, team, country, image_url, description FROM products"
        )

        # Perform manual filtering with normalization
        results = []
        for product in all_products:
            product_name = unidecode(product["name"].lower())
            product_team = unidecode(product["team"].lower())
            product_type = unidecode(product["type"].lower())
            product_country = unidecode(product["country"].lower())

            # Check if the normalized search term matches any normalized product
            if (
                normalized_search_term in product_name
                or normalized_search_term in product_team
                or normalized_search_term in product_type
                or normalized_search_term in product_country
            ):
                results.append(product)

        if not results:
            flash("Searched term could not be found!")

        return render_template("search.html", results=results, search_term=search_term)


@app.route("/update_cash", methods=["GET", "POST"])
@login_required
def update_cash():
    """Add cash to user account"""

    # Session for user id
    user_id = session["user_id"]

    if request.method == "GET":
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        return render_template("cash.html", current_cash=current_cash)

    if request.method == "POST":
        cash_update = request.form.get("cash_amount")

        # Ensure seller enters a value
        if not cash_update:
            return apology("Cash must be entered")

        # Convert to integer
        cash_update = int(cash_update)

        # Ensure positive number is entered
        if cash_update <= 0:
            return apology("Positive cash value must be entered")

        # Update cash account in db
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?", cash_update, user_id
        )

        return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    print("Register route accessed")
    """ Register user """
    # Forget user
    session.clear()

    # When POST
    if request.method == "POST":

        password = request.form.get("password")
        username = request.form.get("username")
        confirmation = request.form.get("confirmation")

        # Ensure user name is submitted
        if not username:
            return apology("Username must be provided")

        # Ensure password is submitted
        elif not password:
            return apology("Password must be submitted")

        # Ensure confirmation is submitted
        elif not confirmation:
            return apology("Must provide confirmation")

        # Ensure password matches confirmation
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password does not match confirmation")

        # Ensure that provided user is not existing
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) > 0:
            return apology(
                "Username is taken already, choose different username please"
            )

        # Hash the password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Insert user to db
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            hashed_password,
        )

        # Redirect to login after
        return redirect("/login")

    # User reached via GET
    else:
        return render_template("register.html")


@app.route("/product_detail/<int:product_id>")
def product_detail(product_id):

    # Session for user id
    user_id = session["user_id"]

    product = get_product_by_id(product_id)  # Fetch product details from your database
    return render_template("product_detail.html", product=product)


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = int(request.form["product_id"])
    quantity = int(request.form["quantity"])

    # Fetch the product from db
    result = db.execute("SELECT * FROM products WHERE product_id = ?", (product_id))

    # Ensure that article exists
    if not result:
        return apology("Product not found")

    # Extract the first (and ideally only) product from the result list
    product = result[0]

    # Get the current cart from the session
    cart = session.get("cart", [])

    print(cart)

    # Check if the product is already in the cart
    for item in cart:
        if item["product"]["product_id"] == product_id:
            item["quantity"] += quantity  # Increment quantity if already in cart
            break

    else:
        # Add product to cart if not already in the cart
        cart.append({"product": product, "quantity": quantity})

    # Store cart in session
    session["cart"] = cart

    # Ensure you're accessing 'name' correctly from the product
    flash(f"{product['name']} added to cart!")

    # Redirect to the cart page
    return redirect("/cart")


@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():

    # Get the product_id from the form data
    product_id = request.form["product_id"]
    quantity_to_remove = int(request.form["quantity"])

    # Get the current cart from the session
    cart = session.get("cart", [])

    for item in cart:
        if item["product"]["product_id"] == int(product_id):
            item["quantity"] -= quantity_to_remove  # Decrease quantity
            if item["quantity"] <= 0:
                cart.remove(item)  # Remove item if quantity reaches 0
            break

    # Update the session cart and # Flash a success message
    session["cart"] = cart
    flash("Item removed from cart.")

    # Redirect back to the cart page
    return redirect("/cart")


@app.route("/cart")
def cart():
    # Get the cart from session
    cart = session.get("cart", [])

    # Check if the cart is empty and handle accordingly
    if not cart:
        return apology("Your cart is empty!")

    # Calculate the total price
    total_price = sum(item["product"]["price"] * item["quantity"] for item in cart)

    return render_template("cart.html", cart=cart, total_price=total_price)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    # Define variable for user_id
    user_id = session["user_id"]

    # Check if get
    if request.method == "GET":
        # Display the checkout page
        cart = session.get("cart", [])
        total_amount = sum(item["product"]["price"] * item["quantity"] for item in cart)

        if not cart:
            flash("Your cart is empty! Add items to your cart before checking out.")
            return redirect("/cart")

        return render_template("checkout.html", cart=cart, total_amount=total_amount)

    elif request.method == "POST":

        # Initialize variable to get cash amount of user
        cart = session.get("cart", [])
        total_amount = sum(item["product"]["price"] * item["quantity"] for item in cart)
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0][
            "cash"
        ]

        # Ensure enough cash is available
        if user_cash < total_amount:
            return apology("Not enough cash")

        # Update cash balance of user if enough caseh
        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?", total_amount, user_id
        )

        # Get the shipping details from the form
        name = request.form["name"]
        address = request.form["address"]
        city = request.form["city"]
        zip_code = request.form["zip"]
        country = request.form["country"]

        # Get the cart and calculate the total amount
        cart = session.get("cart", [])
        total_amount = sum(item["product"]["price"] * item["quantity"] for item in cart)

        # Handle empty cart scenario
        if not cart:
            flash("Your cart is empty! Add items to your cart checking out")
            return redirect("/cart")

        # Clear the cart after successfull checkout
        session["cart"] = []

        # Flash confirmation message and redirect to the success page
        flash("Your order has been placed successfully!")
        return redirect("/order_success")


@app.route("/order_success", methods=["GET"])
def order_success():
    """Display order success confirmation."""
    return render_template("order_confirmation.html")
