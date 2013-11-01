#! /bin/bash
#author jianwu.hu@intel.com
#copy files in a list to target dir
usage()
{
    echo "usage: $0 file_list target_dir"
    exit 1
}
if [ $# -eq 2 ]; then
    :
else
    usage
    exit 1
fi
if [ -f $1 ] ; then
    :
else
    echo $1 does not exist !!
    exit 1
fi
list=$1
targetdir=$2
if [ -d $targetdir ]; then
    :
else
    if mkdir -p $targetdir; then
        :
    else
        echo "failed to create $targetdir, please check the patch"
        exit 1
    fi
fi
targetdir=${targetdir%/}
echo $targetdir
for file in `cat $1`
    do
    dir=${file%/*.*}
    dir=${dir#./}
    if [ ! -d $targetdir/$dir ]; then
        mkdir -p $targetdir/$dir
    fi
    cp -p $file $targetdir/$file

done
