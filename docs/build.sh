#!/bin/bash
cd $(dirname $0)
for old_name in $(cd ..; ls *.md); do {
    new_name=$(echo "$old_name" | sed 's@\([0-9][0-9]\)@2021-\1-@');
    ln -svf "../../$old_name" "_posts/$new_name"
} done
jekyll build

