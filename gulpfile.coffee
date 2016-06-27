g = require "gulp"
toolbox = require "hyamamoto-job-toolbox"
helper = require "hyamamoto-job-toolbox/lib/helper"

toolbox.python "", "wtf_otp", []

g.task "tox", ["python.tox"], ->
  toolbox.virtualenv "coverage combine python27.coverage python35.coverage"

taskDep = []
if helper.isProduction
  taskDep.push "tox"
g.task "default", taskDep, ->
  if not helper.isProduction
    g.watch "wtf_otp/**/*.py", ["tox"]
