#!/bin/bash

set -e

working_branch="working"

git checkout master
git merge "$working_branch" --no-ff -m "Merge $working_branch branch into master"
git push origin master

echo "Master branch updated"

git checkout "$working_branch"
