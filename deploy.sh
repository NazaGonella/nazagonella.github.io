#!/bin/bash

set -e

main_branch="master"
working_branch="working"

git checkout "$main_branch"
git merge "$working_branch" --no-ff -m "Merge $working_branch branch into $main_branch."
git push origin "$main_branch"

echo "Main branch updated"

git checkout "$working_branch"
