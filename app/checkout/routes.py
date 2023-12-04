from app.checkout import bp
from flask import redirect, request, url_for, render_template, session
import stripe
from flask_login import login_required
from app.models.paid_chats import PaidChats
from app.extensions import db

stripe.api_key = 'sk_test_51OENqKBe96cxMC6cXhZ3iMsz60VAjdkKu68bQnGQYuPlKQup1a6Ftuq0cQTsydkMcrEaCvuL4gmZsBbIByDgBmxf00d7u913Ga'

YOUR_DOMAIN = 'http://localhost:5000'

doctor_chatting = stripe.Product.create(
  name="Doctor chat",
  description="doctor_email",
)

doctor_chatting_price = stripe.Price.create(
  unit_amount=2500,
  currency="cad",
  #recurring={"interval": "month"},
  product=doctor_chatting['id'],
)

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': doctor_chatting_price.id, #'price_1OENt6Be96cxMC6cDCpZVfpf',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url = YOUR_DOMAIN + url_for('checkout.success'),
            cancel_url = YOUR_DOMAIN + url_for('checkout.cancel'),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@bp.route("/success")
@login_required
def success():
    new_paid_chat = PaidChats(user=session['email'], doctor_email=doctor_chatting['description'])
    db.session.add(new_paid_chat)
    db.session.commit()
    
    return render_template("checkout/success.html")

@bp.route("/cancel")
@login_required
def cancel():
    return render_template("checkout/cancel.html")