# from pip._internal.network import auth
from pip._vendor.requests import auth
from sqlalchemy.sql.functions import user
from flask_login import login_user, login_required, logout_user, current_user
from market import app
from flask import redirect, url_for, flash, render_template, request
from .models import *
from .forms import *


#@manager.command
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("Invalide route")


@app.route('/market', methods=['GET', 'POST'])
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        # Purchase logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                p_item_object.owner = current_user.id
                current_user.budget -= p_item_object.price
                db.session.commit()
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$",
                      category='success')
            else:
                flash(f"Unfortunately, you do not have enough money to purchase", category='danger')
                # Selling logic
                sold_item = request.form.get('sold_item')
                s_item_object = Item.query.filter_by(name=sold_item).first()
                if s_item_object:
                    if current_user.can_sell(s_item_object):
                        s_item_object.sell(current_user)
                    flash(f"Congratulations! You sold {s_item_object.name} back to market!",
                          category='success')
                else:
                    flash(f"Sorry, something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user)

    return render_template('components/market.html', items=items, purchase_form=purchase_form, owned_items=owned_items,
                           selling_form=selling_form)


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    # hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data

                              )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account is created successfully! You are now  logged in as: {user_to_create.username}",
              category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('components/register.html', form=form)


@app.route("/search", methods=['GET', 'POST'])
def search_user():
    form = UserSeacrh()
    if form.validate_on_submit():
        flash('{}'.format(user))
        return redirect(url_for("home_page"))
        # return render_template("users.html", users=user)
    return render_template("components/userSearch.html", form=form)


@app.route('/my_page')
def my_page():
    return render_template('components/account_page.html')


@app.route('/contact')
def contact():
    return render_template('components/contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user, remember=form.remember.data)
            flash(f"Success! You have successfully logged in as: {attempted_user.username}", category='success')

            return redirect(url_for('home_page'))
    else:
        flash(f"Username and password do not match! Please try again!", category='danger')
    return render_template('components/login.html', form=form)


@app.route('/edit')
def edit_page():
    return render_template('components/edit_profile.html')


@app.route('/terms')
def terms():
    return render_template('components/terms.html')


@app.route('/about')
def about():
    return render_template('components/about.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out', category='info')
    return redirect(url_for('home_page'))


@app.route('/owned')
def owned_page():
    return render_template('components/owned_page.html')
