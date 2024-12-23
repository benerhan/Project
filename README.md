# The Futbole Store
#### Video Demo:  <(https://youtu.be/NpLFP-Btuc0)>
#### Description:
For the Final Project for CS50 I created an online webstore called The Futbol store where I offer different kinds of articles related to Futbol. 

If you enter the Main Page first you are requested to Login with your crediantals or to Register if you do not have registered yet. After you Login successfully you will get to the main page the index.html of the webstore. On index.html I did created a carousel where all my articles are displayed in a carousel. To create the carousel I used the bootsrap feature in my index.html and connected the URL of the images with it which are all entered in my database. The carousel styles are all entered directly in index.html as style tags. 

Further Tabs of the page are Shirts, Shorts, Accesoires, Search, Add cash to account, Cart. All the articles visible on the carousel in index.html are splitted up in the tabs Shirts, Shorts and Accesoires. They are all implemented with the same design style visible in styles.cc where I tried to be consistent with all the pages and the articles of the store. 

In the search tab I did implement a search form where I search for a searchterm. If entered in search the word "accesoires" only the accesoires are displayed. If you enter in the search Scarf, which is one of the two articles in accesoires, the result of the search are only scarfs. Also some team names do contain non english symbols for example the team Beşiktaş but if you do search Besiktas the correct outcome is that Beşiktaş is displayed it does display correctly all the articles related to Beşiktaş. Furthermore you can search for example for a country and all the articles related to the country will appear. To do so I did implement a normalization of the entered search term and the products in the database with the help of unidecode. After the normalization with unidecode the entered search term and the products in the database get compared with a for loop and if conditionals. 

Next tab Add Cash to Account was inspired by the finance problemset where you entered an amount and you had this amount to spend later without checking for credit card data and here it is the same. On my final project The Futbol Store, the registered user can go to Add Cash to Account and simply enter a value to add cash to the account. Also on this tab the current balance is visible so the user always can see how much cash is left on the balance. 

The last tab is the Cart tab which contains all the articles added to the cart or if the cart is empty it displayes an apology saying cart is empty. The user can add articles to the cart from the Product Detail Page. To the Product Detail Page you get by clicking on the wanted article and this can be the article on index.html in the carousel or the shirt tab or you get to the Product Detail Page also by clicking on the article from the search results. In the Product Detail Page you can increase the quantity and add it to the cart. For this I created a separate route in app.py. Similarly on the cart itself you can remove some quantity from the cart so if you added too many items of one article which was also implemented with a separate route in app.py. After you checked the data you can confirm and proceed to checkout.

Finally there is a checkout form where the user sees the articles with the price, the subtotal, the total and a form to enter the shipping data. After the shipping data is entered the user can confirm and purchase the articles from the cart if they have enough balance, if not an apology is displayed saying not enough cash. After the successfull purchase the user gets transferred to the confirmation page where a confirmation of the order is displayed.

In total I did implement 15 app.routes for 
- accesoires -> basically a DB query to display the type accesoires on page
- add_to_cart -> checking for the product id and the quantity from detail page with a for loop to loop through the cart with if conditionals to check if there is quantity to increase 
- cart -> session from cart and sum of all articles in the cart to provide subtotal and total
- checkout -> if get display the items in the cart and if post request from user the shipping data and when purchasing update cash balance
- index -> query of DB for the products to be displayed in carousel
- login -> very similar to finance.db
- logout -> very similar to finance.db
- order_success -> simply return render_template to the success html 
- product_detail -> matching the product id and query the article information from DB
- register -> very similar to finance.db
- remove_from_cart -> checking for the product id and removing the quantity from cart with a for loop to loop through the cart and if conditionals to check if there is quantity to decrease
- search -> if post it will normalize the entered search term and also normalize the articles DB and compare them to each other for matches
- shirts -> basically a DB query to display the type shirts on page
- shorts -> basically a DB query to display the type shorts on page
- update_cash -> if get it displays the current balance from DB and if post it will check if you enter data and update the DB with the entered cash amount


Furthermore I did implement 14 HTMLs for following:
- accesoires.html -> loop through the DB query from route and display the wanted information
- apology.html -> apology from fincance.db
- cart.html -> a for loop to loop through the cart and a form to decrease quantity
- cash.html -> display the query from route and a form to increase the cash 
- checkout.html -> a for loop for the articles in cart and a form to enter shipping data 
- index.html -> carousel to display all the articles from query in route in a carousel
- layout.html -> very similar to finance.db
- login.html -> very similar to finance.db
- order_confirmation.html -> basic order confirmation information 
- product_detail.html -> display of the query from route and a form for increasing quantity
- register.html -> very similar to finance.db
- search.html -> loop through the data provided from search route
- shirts.html -> loop through the DB query from route and display the wanted information
- shorts html -> loop through the DB query from route and display the wanted information

Furthermore I did also implement a helpers.py with helper functions, a db.py for a db query, the db itself which has the name futbol_store.db and for the applied styles a styles.cc.

Additionally I did create a simple database called futbol_store.db with two tables, the products and users table. 

For the final project I used mainly chatgpt and cs50ai as helping tools.