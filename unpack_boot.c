/*
** description : a tool to unpack intel boot image
** author      : Hu Jianwu (jianwu.hu@intel.com)
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ISU_SIZE 512
#define CMDLINE_OFFSET ISU_SIZE
#define CMDLINE_SIZE 4096
#define BOOTSTUB_SIZE 4096
#define BOOTSTUB_OFFSET (CMDLINE_OFFSET + CMDLINE_SIZE)
#define KERNEL_OFFSET (BOOTSTUB_OFFSET + BOOTSTUB_SIZE)
#define INFOBLOCK_OFFSET  (CMDLINE_OFFSET + 1024)

int main(int argc, char** argv)
{
    char* boot_name;
    char* kernel_name;
    char* ramdisk_name;
    char* cmdline_name;
    char* magic = "$OS$";
    FILE *boot_image,*kernel,*ramdisk,*cmdline;
    int kernel_size;
    int ramdisk_size;
    int cmdline_size;
    static char buffer[10*1024*1024];
    int count;
    if(argc !=2) 
    {
        printf("usage: unpack_boot boot.bin\n");
        exit(0);
    }
    boot_name = argv[1];
    kernel_name = "kernel.extract";
    cmdline_name = "cmdline.extract";
    ramdisk_name = "ramdisk.extract";
    boot_image = fopen(boot_name,"rb");
    kernel = fopen(kernel_name,"wb");
    ramdisk = fopen(ramdisk_name,"wb");
    cmdline = fopen(cmdline_name,"w");
    if(!(boot_image || kernel || ramdisk || cmdline))
    {
        printf("failed to open files");
        goto exit;
    }
    count = fread(buffer,4,1,boot_image);
    if( (count != 1) || memcmp(buffer,magic,4))
    {
        printf("bad boot image !\n");
        goto exit;
    }
    fseek(boot_image,CMDLINE_OFFSET,SEEK_SET);
    fread(buffer,1024,1,boot_image);
    cmdline_size = strlen(buffer);
    fwrite(buffer,cmdline_size+1,1,cmdline);
    fseek(boot_image,INFOBLOCK_OFFSET,SEEK_SET);
    fread(buffer,8,1,boot_image);

    kernel_size = *((int*)&buffer[0]);
    ramdisk_size = *((int*)&buffer[4]);

    printf(" block info offset is %04x kernel size is %d, ramdisk size is %d \n",INFOBLOCK_OFFSET,kernel_size,ramdisk_size);

    fseek(boot_image,KERNEL_OFFSET,SEEK_SET);

    fread(buffer,kernel_size,1,boot_image);
    fwrite(buffer,kernel_size,1,kernel);

    fread(buffer,ramdisk_size,1,boot_image);
    fwrite(buffer,ramdisk_size,1,ramdisk);
exit:
    fclose(boot_image);
    fclose(kernel);
    fclose(ramdisk);
    fclose(cmdline);

    return 0;
}
