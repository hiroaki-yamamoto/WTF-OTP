# One-Time Password Field for WT-Forms

[![Build Status]][Build Status Link]
[![Maintainability]][Maintainability Link]
[![Test Coverage]][Coverage Link]

[Build Status]: https://app.travis-ci.com/hiroaki-yamamoto/WTF-OTP.svg?branch=master
[Build Status Link]: https://app.travis-ci.com/hiroaki-yamamoto/WTF-OTP
[Maintainability]: https://api.codeclimate.com/v1/badges/c03f10d1351fa391e1d2/maintainability
[Maintainability Link]: https://codeclimate.com/github/hiroaki-yamamoto/WTF-OTP/maintainability
[Test Coverage]: https://api.codeclimate.com/v1/badges/c03f10d1351fa391e1d2/test_coverage
[Coverage Link]: https://codeclimate.com/github/hiroaki-yamamoto/WTF-OTP/test_coverage


## What This?

This module has Google's [2 factor authentication fields] for [WT-Forms].

[2 factor authentication fields]: https://github.com/google/google-authenticator
[WT-Forms]: https://wtforms.readthedocs.org/

## Features
* Single-Page Application driven secret key generation.
* **QRCode Generation**
* Secret field and authentication validator that is based on [WTForms]

[WT-Forms]: https://wtforms.readthedocs.org/

## How to use

### If you want QR Code:
First, write the form to generate secret key and authenticate it:

`form.py`
```python
#!/usr/bin/env python
# coding=utf-8

from flask_wtf import Form
import wtforms.fields as fld
import wtforms.fields.html5 as fld5
import wtforms.validators as vld
from wtf_otp import OTPSecretKeyField, OTPCheck

class UserInfoForm(Form):
  name = fld.StringField()
  email = fld5.EmailField(validators=[
    vld.InputRequired(), vld.Email()
  ])
  password = fld.PasswordField()
  new_password = fld.PasswordField()
  confirm_password = fld.PasswordField(validators=[
    vld.EqualTo("new_password")
  ])
  secret = OTPSecretKeyField(
    qrcode_url="/qrcode", validators=[vld.InputRequired()]
  )

class LoginForm(Form):
  email = fld5.EmailField(validators=[
    vld.InputRequired(), vld.Email()
  ])
  passwrd = fld.PasswordField(validators=[
    vld.InputRequired()
  ])
  auth = fld.IntegerField(validators=[
    validators=[vld.InputRequired(), OTPCheck()]
  ])
```

Next, write the app as usual. However, you want to add a new route of which
path is "/qrcode" that generates the qrcode. Fortuantely, the sufficient
function is provided. An instance of `OTPSecretKeyField` provides `qrcode`
function:

```python
from .form import UserInfoForm

# /qrcode is assigned to generate_qrcode.
def generate_qrcode(req, res):
  form = UserInfoForm()
  secret = req.args.get("secret")
  if not secret:
      abort(404)
  res.make_response(form.secret.qrcode(
      secret, name="Test Example", issuer_name="Test Corp"
  ))
  resp.mimetype = "image/svg+xml"
```

Note that you can't get the instance by `UserInfoForm.secret`, because
`UserInfoForm.secret` returns an instance of `UnboundField`.

## If you don't want QRCode
If you don't want QRCode, just remove `qrcode_url` from the corresponding
classes and remove QRCode generation class.

## More detail
If you want more detail, please refer [source code] and [example code].

[source code]: wtf_otp
[example code]: example

## License (MIT License)

The MIT License (MIT)
Copyright (c) 2016- Hiroaki Yamamoto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
