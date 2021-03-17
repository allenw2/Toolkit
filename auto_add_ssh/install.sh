#!/usr/local/bin/zsh

mkdir ~/tools/ &> /dev/null
cp -r "$PWD" ~/tools/ &> /dev/null
ln -sf ~/tools/auto_add_ssh/add_alias.sh /usr/local/bin/add-ssh

if [ $? -eq 0 ]; then
  echo 'Finished! add-ssh command is available now.'
fi