g = require "gulp"
q = require "q"
toolbox = require "hyamamoto-job-toolbox"
helper = require "hyamamoto-job-toolbox/lib/helper"
rimraf = require "rimraf"

toolbox.python "", "wtf_otp", []

g.task "tox", ["python.tox.only"], ->
  toolbox.virtualenv(
    "coverage combine python27.coverage python35.coverage"
  ).then -> toolbox.virtualenv(
    "coverage report -m"
  )

taskDep = []
if helper.isProduction
  taskDep.push "tox"
g.task "default", taskDep, ->
  if not helper.isProduction
    g.watch ["wtf_otp/**/*.py", "tests/**/*.py", "setup.py"], ["tox"]

g.task "clean", ->
  q.all([
    q.nfcall(rimraf, "**/*.pyc")
    q.nfcall(rimraf, "**/__pycache")
  ])
