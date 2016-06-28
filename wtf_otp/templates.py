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
    "})})()"
    "</script>"
)
