#!/bin/bash

working_branch="working"

git checkout master
git merge "$working_branch"
git push origin master

echo "Master branch updated"

git checkout "$working_branch"
