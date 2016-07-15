#!/usr/bin/env python
# coding=utf-8

from flask import (
    Flask, render_template, make_response, request, abort,
    jsonify
)
from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect, generate_csrf
import wtforms.fields as fld
import wtforms.validators as vld
from wtf_otp import OTPSecretKeyField, OTPCheck

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = (
    lambda: "2ekN1=0dafF2g6Ijk~tNMzo5_B;a02zK729MAhY|I9EN52JD1z"
)()
app.config["WTF_CSRF_METHODS"] = ["POST", "PUT", "PATCH", "DELETE"]
CsrfProtect(app)


class SecretKeyTestForm(Form):
    jquery_secret = OTPSecretKeyField(
        "JQuery Secret Key with QR Code",
        render_kw={"qrcode_url": "/qrcode"}
    )
    jquery_secret_noqrcode = OTPSecretKeyField(
        "JQuery Secret Key without QR Code"
    )
    jquery_secret_hasdata = OTPSecretKeyField(
        "JQuery Secret Key with QR Code and data",
        render_kw={"qrcode_url": "/qrcode"}
    )
    jquery_secret_noqrcode_hasdata = OTPSecretKeyField(
        "JQuery Secret Key without QR Code, but it has data"
    )
    angular_secret = OTPSecretKeyField(
        "Angular Secret Key with QR Code",
        render_kw={
            "qrcode_url": "/qrcode",
            "data-ng-model": "model.test",
            "module": "OTPApp"
        }
    )
    angular_secret_noqrcode = OTPSecretKeyField(
        "Angular Secret Key without QR Code", render_kw={
            "data-ng-model": "model.test_noqr",
            "module": "OTPApp"
        }
    )
    angular_secret_hasdata = OTPSecretKeyField(
        "Angular Secret Key with QR Code and data",
        render_kw={
            "qrcode_url": "/qrcode",
            "data-ng-model": "model.test_data",
            "module": "OTPApp"
        }
    )
    angular_secret_noqrcode_hasdata = OTPSecretKeyField(
        "Angular Secret Key without QR Code, but it has data",
        render_kw={
            "data-ng-model": "model.test_noqr_data",
            "module": "OTPApp"
        }
    )


class OTPAuthentication(Form):
    """OTP Authentication form."""

    secret = OTPSecretKeyField(qrcode_url="/qrcode", render_kw={
        "data-ng-model": "model.secret",
        "module": "OTPApp"
    })
    check = fld.IntegerField(validators=[
        vld.NumberRange(min=0, max=999999),
        OTPCheck(
            secret=lambda form, field: form.secret.data,
            method="TOTP"
        )
    ], render_kw={"data-ng-model": "model.check"})


@app.route("/")
def index():
    form = SecretKeyTestForm()
    form.jquery_secret_hasdata.data = form.jquery_secret_hasdata.generate()
    form.jquery_secret_noqrcode_hasdata.data = \
        form.jquery_secret_noqrcode_hasdata.generate()
    form.angular_secret_hasdata.data = form.angular_secret_hasdata.generate()
    form.angular_secret_noqrcode_hasdata.data = \
        form.angular_secret_noqrcode_hasdata.generate()

    auth_form = OTPAuthentication()
    return render_template("index.html", form=form, auth_form=auth_form)


@app.route("/postload")
def postload():
    form = SecretKeyTestForm()
    form.jquery_secret_hasdata.data = form.jquery_secret_hasdata.generate()
    form.jquery_secret_noqrcode_hasdata.data = \
        form.jquery_secret_noqrcode_hasdata.generate()
    form.angular_secret_hasdata.data = form.angular_secret_hasdata.generate()
    form.angular_secret_noqrcode_hasdata.data = \
        form.angular_secret_noqrcode_hasdata.generate()

    auth_form = OTPAuthentication()
    return render_template(
        "index_postload.html", form=form, auth_form=auth_form
    )


@app.route("/qrcode")
def render_qrcode():
    form = SecretKeyTestForm()
    secret = request.args.get("secret")
    if not secret:
        abort(404)
    resp = make_response(form.jquery_secret_noqrcode.qrcode(
        secret, name="Test Example", issuer_name="Test Corp"
    ))
    resp.mimetype = "image/svg+xml"
    return resp


@app.route("/auth", methods=["POST"])
def auth():
    form = OTPAuthentication()
    status = {"status": "ok" if form.validate() else "wrong"}
    status.update({"errors": form.errors})
    return make_response(jsonify(status), 417 if form.errors else 200)


@app.after_request
def csrf_prevent(resp):
    """Add CSRF Preventation for angularJS."""
    resp.set_cookie("X-CSRFToken", generate_csrf())
    return resp

def main():
    app.run()


if __name__ == '__main__':
    main()
