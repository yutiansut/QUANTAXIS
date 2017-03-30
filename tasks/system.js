'use strict'
const exec = require('child_process').exec


function run (command) {
  let child = exec(command)
  child.on('exit', code => exit(code))

  children.push(child)
}

function exit (code) {
  children.forEach(child => {
    treeKill(child.pid)
  })
}

run('node ./backend/bin/www')
