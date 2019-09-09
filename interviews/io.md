## 1.简单介绍一下 zero copy [***]

通常发送一个文件要经历四次拷贝。read：先拷贝数据到内核态，之后再从内核态拷贝到用户态；write：先从用户态下拷贝内容到内核态（比如 socket buffer）在拷贝到文件或网卡设备中传送。

sendFile 系统调用不再使用 read-write 两次系统调用，而是直接一次系统调用。数据也不再进入用户态。 1.将文件拷贝到 kernel buffer 中； 2.向 socket buffer 中追加当前要发送的数据在 kernel buffer 中的位置和偏移量； 3.根据 socket buffer 中的位置和偏移量直接将 kernel buffer 的数据 copy 到网卡设备（protocol engine）中；

## 2.什么文件空洞？[***]
