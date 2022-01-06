# SAPIENCE STORE
#### [Video Demo](https://youtu.be/HBnj7MTYh28)
#### Description:
This project is a **Flask App** that simulates an **e-commerce**: Sapience Store,
the place where just the most wise people buy stuff, given their intelligence to
know that the most cheap but high quality products are all here.

I tried to make it responsive, so it adapts to a large range of screen sizes.

 I decided to do that for my CS50 final project because of the challenges and,
 consequently, the knowledge it'd bring me.

Techonologies and frameworks: 

- HTML
- CSS
- JS
- Python
- SQL
- Bootstrap
---
## How to run it locally:

1. [Download Python]('https://www.python.org/downloads/')
2. In the terminal, open the project directory
3. Activate the virtual environment:
On Windows, run:
```
env\Scripts\activate.bat
```
On Unix or MacOS, run:
```
env/bin/activate
```

4. Install the required libraries by typing:
```
pip install -r requirements.txt
```

5. Then run the flask app:
```
flask run
```

---
Functionalities:

 **User registering and authentication**: In the register page you just need to
 chose an username, besides a pass and a confirm this pass;

 **Change password**: here you don't even need to know your current pass to change
 it, which makes you able to change it in case of you forget it, but is still logged in;

 **Add products to cart**: this cart is pretty much like a wish list, you just see
 all the products you've been wanting to buy and don't want to forget them;

**Buy products**;

**Sell products**: To add products, you just need to specify the product name, price
and an image, but also  you can optionatily add a description and one main category;

 **See history of purchases**;

 **Search for products**: it's just input a keyword and the algorithm is gonna look for
 products that have it in the name or description.

---
By default you have **$1,000.00 of cash**, which allow you make your first purchases.
But, as specified above, you are also able to add products to the store and, if any
user buy it, your cash is increased!

----
Possible improvements:
As pretty much all other thing, this project is far from being perfect or even next to that. I suggest some improvements i could've had implemented:

- **Product slider**: the products rows in the homepage are 'static', it's not possible to see all the products of a big screen in a smaller one. The solution for that is add a product slider, which actually I tried to do with lightslider, but wasn't able to.
- **Sell history page**: the sellers could have access to a page where they can see their sellings perfomance of the month or year, for example (and going even 'further', it could be implemented some charts with JS or Python).
- **Categories page**: a page that shows all the categories would be useful for a usel that just wanna explore in the products of a specific category.
- **Rating and commenting about the products**: would make the product have its average rating and show the users how many people approve that.
- **Search filter**: a great functionality would the possibility to filter the searchs with price variables, rating, localization, etc.
- **Checkout API**: an API used to simulate the payments would make it feels more like real life.
- **Custom profile**: with pics, banners and status (it'd be good for the sellers especially).
- **Make tweaks in cart and add a wish list**: The cart should be used for, after picking all the products the user want, just go to the checkout.
- **More images for each product**

