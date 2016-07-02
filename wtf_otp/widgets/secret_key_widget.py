#!/usr/bin/env python
# coding=utf-8

"""OTP Widgets."""
from wtforms.widgets import html_params, HTMLString

from .templates import jquery_template, angular_template


class OTPSecretKeyWidget(object):
    """
    OTP Widget.

    This widget readonly input, and "Get Secret Key" button.
    Clicking the "Generate" button, a new secret key is generated thru
    browser-side generator.
    """

    def __call__(self, field, **kwargs):
        """
        Generate OTPWidget.

        Parameters:
            **kwargs: Any arguments to be applied to input.
                If input_args has dict value, input_args.update(kwargs) is
                called after parameter transformation.
                Note that the values of button_args and div_args are applied
                to button and div. For details, refer keyword arguments.
        Keyword Arguments:
            input_args: Any arguments to be applied to input.
            button_args: Any arguments to be applied to button only.
            div_args: Any argument that to applied to div wrap.
                i.e. inputs are wrapped with div tags.
        """
        input_args = kwargs.pop("input_args", {})
        button_args = kwargs.pop("button_args", {})
        div_args = kwargs.pop("div_args", {})
        qrcode = kwargs.pop("qrcode_url", None)

        input_args.update(kwargs)
        input_args.setdefault("id", field.id)
        input_args.setdefault("name", field.name)
        input_widget = HTMLString((
            "<input type=\"text\" readonly {}>"
        ).format(html_params(**input_args)))

        button_args.setdefault("id", "btn-" + field.id)
        # Because I strongly recommend to use data-* attribute for custom
        # attributes, angular aimed option is available only for data-*
        # attributes.
        if "data-ng-model" in input_args:
            button_args["data-ng-click"] = ("click{}()").format(id(field))
            div_args["data-ng-controller"] = ("OTP{}Controller").format(
                id(field)
            )
        button_widget = HTMLString((
            "<button type=\"button\" {}>Get Secret Key</button>"
        ).format(html_params(**button_args) if button_args else ""))
        div_widget = ("<div {}>").format(
            html_params(**div_args)
        ) if div_args else "<div>"
        script_widget = HTMLString(
            angular_template.render(
                fieldid=id(field), ng_model=input_args["data-ng-model"],
                qrcode_url=qrcode
            ) if "data-ng-model" in input_args else jquery_template.render(
                btnid=button_args["id"], inputid=input_args["id"],
                qrcode_url=qrcode
            )
        )

        qrcode_tag = HTMLString(
            ("<img {}>").format(
                html_params(id=("otpauthQR{}").format(field.id))
            )
        )

        output_widget = [widget for widget in [
            div_widget,
            qrcode_tag if qrcode else None,
            input_widget,
            button_widget,
            script_widget,
            "</div>"
        ] if widget]

        return ("").join(output_widget)
