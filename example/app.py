#!/usr/bin/env python
# coding=utf-8

from flask import Flask, render_template, make_response, request, abort
from flask_wtf import Form
import wtforms.fields as fld
import wtforms.validators as vld
from wtf_otp import OTPSecretKeyField, OTPCheck

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = (
    lambda: "2ekN1=0dafF2g6Ijk~tNMzo5_B;a02zK729MAhY|I9EN52JD1z"
)()


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

    secret = OTPSecretKeyField(render_kw={
        "qrcode_url": "/qrcode",
        "data-ng-model": "model.test",
        "module": "OTPApp"
    })
    check = fld.IntegerField(validators=[
        vld.NumberRange(min=0, max=999999),
        OTPCheck(
            secret=lambda form, field: form.secret.data,
            method="TOTP"
        )
    ])


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


def main():
    app.run()


if __name__ == '__main__':
    main()
