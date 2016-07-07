#!/usr/bin/env python
# coding=utf-8

from flask import Flask, render_template, make_response, request, abort
from flask_wtf import Form
from wtf_otp import OTPSecretKeyField

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = (
    lambda: "2ekN1=0dafF2g6Ijk~tNMzo5_B;a02zK729MAhY|I9EN52JD1z"
)()


class SecretKeyTestForm(Form):
    otp_secret = OTPSecretKeyField(render_kw={
        "qrcode_url": "/qrcode"
    })


@app.route("/")
def index():
    jqform = SecretKeyTestForm()
    return render_template("index.html", jqform=jqform)


@app.route("/qrcode")
def render_qrcode():
    form = SecretKeyTestForm()
    secret = request.args.get("secret")
    if not secret:
        abort(404)
    resp = make_response(form.otp_secret.qrcode(
        secret, name="Test Example", issuer_name="Test Corp"
    ))
    resp.mimetype = "image/svg+xml"
    return resp


def main():
    app.run()


if __name__ == '__main__':
    main()
