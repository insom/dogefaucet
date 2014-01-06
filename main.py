from flask import Flask, request, render_template, flash, session, redirect, url_for, g
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from flask.ext.wtf import Form
from flask.ext.wtf.recaptcha import RecaptchaField
from flask.ext.coin import Coin, coin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
import datetime
import sys

if len(sys.argv) < 2:
    print >>sys.stderr, '%s <config file>' % sys.argv[0]
    sys.exit(-1)

app = Flask(__name__)
app.config.from_pyfile(sys.argv[1])
c = Coin(app)
db = SQLAlchemy(app)

def before_request():
    g.doge_address = app.config['DOGE_ADDRESS']

app.before_request(before_request)

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(250))
    wallet = db.Column(db.String(250))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class SecureWalletForm(Form):
    wallet = TextAreaField("Wallet", validators=[DataRequired()])
    recaptcha = RecaptchaField()

class WalletForm(Form):
    wallet = TextAreaField("Wallet", validators=[DataRequired()])

@app.route('/')
def index(form=None):
    if form is None:
        form = app.config.get('RECAPTCHA_PRIVATE_KEY') and SecureWalletForm() or WalletForm()
    wallet = session.get("wallet", [])
    return render_template("index.html", wallet=wallet, form=form)

@app.route("/drink/", methods=("POST",))
def drink():
    form = app.config.get('RECAPTCHA_PRIVATE_KEY') and SecureWalletForm() or WalletForm()
    if form.validate_on_submit():
        wallet = form.wallet.data.strip()
        validation = coin.validateaddress(wallet)
        if not validation.isvalid:
            flash("Not a valid Dogecoin Wallet address")
            return index(form)
        an_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        res = Wallet.query.filter(and_(or_(Wallet.wallet == wallet,
                                           Wallet.ip == request.remote_addr),
                                       Wallet.created > an_hour_ago))
        info = coin.getinfo()
        if info.balance < app.config.get('DOGE_MINIMUM', 100):
            flash("So shame. Dogefaucet has run dry.")
            return index(form)
        for result in res:
            flash("You've had a drink too recently. 1 hour between payouts!")
            return index(form)
        wallet_row = Wallet(wallet=wallet, ip=request.remote_addr)
        db.session.add(wallet_row)
        db.session.commit()
        if app.config.get('WALLET_PASSPHRASE'):
            coin.walletpassphrase(app.config['WALLET_PASSPHRASE'], 3600,
                                  dont_raise=True)
        try:
            tx = coin.sendtoaddress(wallet, app.config['DOGE_AMOUNT'],
                                    comment="Dogebowl #{}".format(wallet_row.id))
        except:
            flash('There was an error paying out your Doge :-(')
            return index(form)
        tx_url = 'http://dogechain.info/tx/{}'.format(tx)
        return render_template("success.html", block_chain_url=tx_url,
                               doge_amount=app.config['DOGE_AMOUNT'])
    return index(form)

if len(sys.argv) > 2 and (sys.argv[2] == 'init'):
    db.create_all()
else:
    app.run(host='0.0.0.0')
