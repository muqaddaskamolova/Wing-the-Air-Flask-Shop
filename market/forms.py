from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, EmailField, BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, InputRequired, email_validator
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):

        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('The Username`s already exists! Please choose another username!')

    def validate_email_address(self, email_address_to_check):

        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('The Email address`s already exists! Please choose another email address!')

    username = StringField(label="Username", validators=[Length(min=2, max=30), DataRequired()])
    email_address = EmailField(label="Email Address",
                               validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm Password", validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    email = EmailField("Email", validators=[DataRequired(), Email()])
    remember = BooleanField("Remember Me")
    submit = SubmitField(label="SIGN IN")


class UserSeacrh(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('Search')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell item')
