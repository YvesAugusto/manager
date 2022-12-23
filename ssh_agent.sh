#!/bin/sh
eval $(ssh-agent)
ssh-add /home/energy/.ssh/manager_deploy_key
git pull