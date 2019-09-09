## nginx 的进程模型是什么样的

nginx 启动后会以 daemon 方式在后台运行，包含一个 master 和多个 worker 进程。
master 进程主要负责接收请求，向 worker 发信号，监控 worker,重启 worker 等等。
每个 worker 都是 master fork 出来的，在 Master 里面先建立需要 Listen 的 socket，然后 fork 出 worker，每个 worker 会去竞争连接，但是只有一个能够抢到锁，并 accept 请求。

## 为什么 nginx 比 apache 能接受更高的并发

nginx 采用异步非阻塞的 IO（epoll/kqueue），好处是并发不会导致 cpu 上下文的切换，只是占用更多内存而已。
