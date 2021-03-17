#!/bin/bash

current_path=`pwd`
path="/Users/whl/tools/auto_add_ssh"
cmd="/Users/whl/.virtualenvs/test/bin/python run.py "

cd $path

var=" "
for i
do
    var+=" $i"
done

$cmd $var
cd "$current_path"