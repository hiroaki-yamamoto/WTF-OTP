#!/usr/bin/env python
# coding=utf-8

"""Templates."""

from jinja2 import Template

jquery_template = Template(
    "<script>"
    "(function(){$(\"#{{btnid}}\").on(\"click\", function() {"
    "var m=\"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567\",v=[],i;"
    "for(i=0;i<16;i++){"
    "v.push(m[Math.floor(Math.random()*32)]);"
    "}"
    "v=v.join(\"\");"
    "$(\"#{{inputid}}\").val(v);"
    "{% if qrcode_url %}"
    "$(\"#otpauthQR{{inputid}}\").attr({\"src\": {{qrcode_url}}})"
    "{% endif %}"
    "})})()"
    "</script>"
)


angular_template = Template(
    "<script>"
    "(function() {"
    "angular.module(\"OTP{{fieldid}}Controller\",["
    "]).controller(\"OTP{{fieldid}}Controller\",["
    "\"$scope\","
    "function(scope){"
    "var m=\"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567\",v=[],i;"
    "scope.click{{fieldid}}=function(){"
    "for(i=0;i<16;i++){"
    "v.push(m[Math.floor(Math.random()*32)]);"
    "}"
    "scope.{{ng_model}}=v.join(\"\");"
    "};"
    "}"
    "]);"
    "})()"
    "</script>"
)
