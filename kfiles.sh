#! /bin/bash
if [ $ANDROID_BUILD_TOP ]; then
   echo "Android built!"
else
    echo "Build Env not setup!!"
    exit 1
fi
cd $ANDROID_BUILD_TOP/kernel/include
all_includes=`find . -type d |grep -v xen`
cd $ANDROID_PRODUCT_OUT/kernel_build
all_objects=`find .  -type f -name \*.o`
for obj in $all_objects
    do
    obj=${obj#./}
    name=${obj%.o}
    file=${name##./*/}
    c_src=$name.c
    s_src=$name.S
    c_hdr=$name.h 
    if [ -f $ANDROID_BUILD_TOP/kernel/$c_src ]; then
        echo $ANDROID_BUILD_TOP/kernel/$c_src
    fi
    if [ -f $ANDROID_BUILD_TOP/kernel/$s_src ]; then
        echo $ANDROID_BUILD_TOP/kernel/$s_src
    fi
    if [ -f $ANDROID_BUILD_TOP/kernel/$c_hdr ]; then
        echo $ANDROID_BUILD_TOP/kernel/$c_hdr
    fi
    for include in $all_includes
        do
        inc=${include#./}
        if [ -f $ANDROID_BUILD_TOP/kernel/include/$inc/$file.h ]; then
            echo ./include/$inc/$file.h
        fi
    done
done

