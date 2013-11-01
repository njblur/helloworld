src=unpack_boot.c
target=unpack_boot
$(target):$(src)
	gcc $(src) -o $(target)
	cp $(target) ~/bin/
