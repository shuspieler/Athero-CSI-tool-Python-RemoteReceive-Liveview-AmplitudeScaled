INCLUDE_DIR=$(TOOLCHAIN_DIR)/usr/include
OBJS = csi_fun.o main.o
CC = mips-openwrt-linux-gcc

CFLAGS= -std=gnu99

recvCSI: $(OBJS)
	$(CC) $(OBJS) -o recvCSI

csi_fun.o: csi_fun.c csi_fun.h
	$(CC) -c $(CFLAGS) -I $(INCLUDE_DIR) -o $@ $<

recvCSI.o: main.c csi_fun.h
	$(CC) -c $(CFLAGS) -I $(INCLUDE_DIR) -o $@ $<

clean:
	rm -f *.o recvCSI

