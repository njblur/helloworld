#! /bin/bash
targets="cplist.sh  kfiles.sh  reboot_test.sh restart_test.sh"
for target in $targets
    do
    echo "copying $target"
    cp $target ~/bin/
done
