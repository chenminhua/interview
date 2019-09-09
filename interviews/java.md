## java 内存模型

1.  如何最快的写出一个 OOM 的程序?[*]

2.  如何最快的写出一个 stackOverFlow 的程序?[*]

## 讲讲并发

http://tutorials.jenkov.com/java-concurrency/concurrency-models.html

1.  threadLocal 原理？[**]

2.  java synchronized 锁一个对象的方法，和锁一个静态方法有啥区别？[**]

3.  啥时候使用 Volatile 关键字？[***]
    如果 shared Object 只对一个线程是读写，其他都是只读，则可以使用 Volatile.
    Volatile 变量具有 synchronized 的可见性特性，但是不具备原子特性。
    读写 volatile 变量一定会去内存读，而不会去 cpu 缓存中读。

volatile 表示线程所见的值总是从主内存读出来，线程所写的值总是会刷入主内存。

    https://www.ibm.com/developerworks/cn/java/j-jtp06197.html'

4.  介绍一下线程间信号 singaling？[***]
    利用线程间的 shared object 进行通信 wait(), notify(), notifyAll()

6)  java 中的线程调度是抢占式还是非抢占式？ 抢占式线程调度

7)  什么是死锁？如何避免死锁？
    线程一以 A,B 顺序获取对象锁，线程二以 B,A 顺序获取对象锁就可能发生死锁。处理死锁问题的一个方法是始终以相同顺序获取锁。

8)  JIT 是啥?
    方法一开始都是以字节码形态存在的，当调用发生时 jvm 只会对字节码进行解释调用。当调用次数达到某个数值后（默认 10000 次），jvm 就会把它编译成机器吗，以后所有对该方法的调用都会用它的编译结果。改善性能通常都要先弄明白程序中哪些方法比较重要，哪些方法被 jit 编译了。

## 泛型

## jvm

## 1. java 是编译型语言还是解释型语言

字节码实际上是一种中间语言（比如 llvm 的 IR）,而不是真正的机器码。javac 也不是 gcc 那种编译器，而是所谓的编译器前端，java 中真正的编译器是 JIT。所以 java 既有编译又有解释执行。

2.  热部署

3.  GC 分代， GC 算法

4.  如何避免 jvm 在执行过程中调整堆的大小?
    设置-Xms 和-Xmx 一样大

## 1. 为什么 java 没有多继承？[****]

开放题，可以聊聊多继承的实现难点在什么地方。为什么 c++有多继承而 java 没有之类的。

## 2. java 引用类型有哪几种？[****]

Strong Reference: 默认引用实现，对象尽可能存活在堆上，直到没有任何引用执行它。

WeakReference: 当对象没有强引用指向的时候会被回收。（don't keep it for me）WeakHashMap 使用 WeakReference 作为 key,一旦没有指向 key 的强引用，entry 就会被 GC

SoftReference: 当对象没有强引用时可以回收，但只在 JVM 内存不足时回收。（don't keep it for me if we don't have enough memory）

PhantomReference: 虚引用，不能通过它来访问对象。用来跟踪对象被垃圾回收器回收的活动，当一个虚引用关联的对象被垃圾收集器回收之前会收到一条系统通知。

很多缓存的实现会使用弱引用和软引用。

3.  性能优化需要测量什么？怎么测量？
    等待时间，吞吐量，利用率，容量，扩展性，退化。
    通过类加载器自动测量。

4.  下面这段代码有啥问题

```java
// 这段代码是错的，千万不要这么写
Comparator<Integer> naturalOrder = (i,j) -> (i < j) ? -1 : (i == j ? 0 : 1)
```

5.  聊聊内部类

静态成员类优于非静态成员类

静态成员类，非静态成员类，匿名类，local 类。后三种都是内部类。

你可以认为静态成员类就是一个普通的类，不过由于刚好定义在了一个类的内部，所以可以访问外部类的其他成员。一个常用的静态成员类的用法是做 public helper (ITEM 34)。
事实上，静态成员类可以独立于外部类存在，即使外部类没有实例化，内部类还是可以实例化。而非静态成员类则和外部类绑定在了一起，这带来的一个坏处是内部的实例会有一个执行外部实例的引，这会浪费时间和空间，更有可能导致对象不能被 gc，从而导致内存泄露。

如果你定义的一个成员类不需要访问外部封装的实例，就把它定义成静态成员类。

非静态成员类的一个 common use 是 Adapter 模式。

```java
public class MySet<E> extends AbstractSet<E> {
    @Override public Iterator<E> iterator() {
        return new MyIterator();
    }

    private class MyIterator implements Iterator<E> {
        ...
    }
}
```

匿名类则是没有名称的类，他们在被定义的时候就实例化了。比如

```java
public class A {
    private int foo;
    public void test() {
        Runnable r = new Runnable() {
            System.out.println(foo);
        };
    }
}
```

local class 就是在定义本地变量的地方定义的类，感觉实在没啥用。

## 为什么 netty 比标准 Nio 库性能更高

单独从性能角度，netty 在 NIO 上进行了很多改进，例如：1.更加优雅的 reactor 模式，灵活的线程模型，利用 eventloop 等等。2.充分利用了 zero-copy 机制，利用池化的 direct buffer 等等。3.使用更多 native 代码。4.在通信协议和序列化技术方面的优化。

netty 是一个异步的、基于事件 Client/Server 的网络框架，java 的标准类库往往从通用性角度考虑，过于关注技术模型的抽象，而不是从一线应用开发的角度考虑。java nio 使用起来也比较复杂，学习路径长。而 netty 通过精巧设计的事件机制，将业务逻辑和无关的技术逻辑进行隔离，并通过各种方便的抽象，一定程度上填补了基础平台和业务开发直接的鸿沟。

从 api 范围来看，netty 完全是 java nio 的一个大超集。除了核心的事件机制外，netty 还提供了各种网络协议的支持，编解码框架，扩展了 java nio buffer 等。

## 为什么说 perfer Lists to arrays

数组是协变的，Sub[]是 Super[]的子类型。而泛型则是逆变的。换句话说，泛型（比如 List）能带来更好的类型安全。

```java
Object[] objectArray = new Long[1];
objectArray[0] = "I don't fit in"; // 编译通过，运行时抛错

List<Object> ol = new ArrayList<Long>(); // 直接抛错
```

另外，数组是具体化的，在运行时检查类型错误。而泛型在运行时已经擦除了类型。

## 为什么不能创建一个泛型数组呢？比如 List<String>[],或者 E[]

因为它不是类型安全的。泛型在运行时没有类型，而数组在编译时又是协变的，因此可能会导致把一组不同的泛型放入同一个泛型数组，从而破坏类型安全。泛型 List<E>, List<String>这种被称为 non-reifiable(非具体化)，它们在运行时的信息要少于编译时。但是有一种情况可以认为是具体化的泛型，List<?>这种类型在运行时和编译时的信息是一样多的，因此创建List<?>[]是合法的（虽然没啥用）。

## 什么时候使用反射，反射有什么用？有什么坏处？

使用反射会导致你失去编译时类型检查的好处。同时性能也会降低。

## 枚举到底是什么？

一个枚举在经过编译器编译过后，变成了一个抽象类，它继承了 java.lang.Enum；
而枚举中定义的枚举常量，变成了相应的 public static final 属性，而且其类型就抽象类的类型，名字就是枚举常量的名字，同时我们可以在 Operator.class 的相同路径下看到四个内部类的.也就是说这四个命名字段分别使用了内部类来实现的；同时添加了两个方法 values()和 valueOf(String)；我们定义的构造方法本来只有一个参数，但却变成了三个参数；同时还生成了一个静态代码块。

## java 对象头里有什么？

Hotspot 虚拟机的对象头主要包括两部分数据：Mark Word（标记字段）、Klass Pointer（类型指针）。Mark Word 用于存储对象自身的运行时数据，它是实现轻量级锁和偏向锁的关键。Mark Word 用于存储对象自身的运行时数据，如哈希码（HashCode）、GC 分代年龄、锁状态标志、线程持有的锁、偏向线程 ID、偏向时间戳等等。Java 对象头一般占有两个机器码（在 32 位虚拟机中，1 个机器码等于 4 字节，也就是 32bit），但是如果对象是数组类型，则需要三个机器码，因为 JVM 虚拟机可以通过 Java 对象的元数据信息确定 Java 对象的大小，但是无法从数组的元数据来确认数组的大小，所以用一块来记录数组长度。

## 热部署

[java 热部署](https://www.ibm.com/developerworks/cn/java/j-lo-hotdeploy/index.html)

## 关于 gc 的一些经验

-XX:+HeapDumpOnOutOfMemoryError 或 -XX:+PrintGCDetails

### exception 和 error 有什么区别

Exception 和 Error 都继承了 Throwable，都可以被捕获。Exception 是意外情况，应该被捕获处理。而 Error 则是不正常的错误，不需要捕获(比如 OutOfMemoryError)。

Exception 又分为 checked 和 unchecked 两类，checked Exception 在编译器检查，必须显式处理；unchecked Exception 为运行时异常，比如 NullPointerException 和 ArrayIndexOutOfBoundsException 之类。

java 引入了新的 try-with-resources 语法，对实现了 AutoClosable 或者 Closeable 的对象可以自动回收。

关于异常的注意点：1.尽量不要捕获 Exception 这样的通用异常，而是捕获特定异常；2.捕获异常就要处理，若不想处理就往外抛。3.Throw early, catch late

4. java 每实例化一个 Exception，都是对当前栈的一个快照，还是比较昂贵的。

#### String, StringBuffer, StringBuilder 有什么区别？

String 不可变，final class,所有的拼接操作都会生成新的 String，所以性能不好。
StringBuffer 是一个线程安全的可修改字符序列。由于有线程安全的保证，相对性能开销也较大。
StringBuilder 去掉了线程安全的部分，减小了开销，是绝大部分情况下拼接字符串的首选。

#### 动态代理啥原理

反射赋予程序在运行时自省（introspect）的能力，通过反射我们可以直接操作类或者对象，比如获取对象的类定义，获取类声明的属性和方法，调用方法或者构造对象，甚至修改类定义。

动态代理是一种方便运行时动态构建代理，动态处理代理方法调用的机制。可以用于包装 rpc 调用，aop 等。

实现动态代理主要使用 jdk proxy，其原理就是反射。除此之外还有 ASM, cglib, javassist 等等。
https://docs.oracle.com/javase/tutorial/reflect/index.html

通过使用动态代理可以让调用者和实现者之间解耦。

jdk proxy 实现方式： 首先实现对应的 InvocationHandler; 然后以需要被代理的接口为纽带，为被调用目标构建代理对象。
cglib 实现方式： 创建目标类的子类

基于 jdk proxy 的特点： 最小化依赖关系，代码实现更简单。缺点是只能代理接口。
基于 cglib 的动态代理的特点： 可以处理没有接口的情况。

#### int 和 Integer 的区别是什么

int 是 primitive type，而 Integer 是对象。Integer 的值缓存默认是-128 到 127 之间（使用 valueOf 方法）。

### Vector, ArrayList, LinkedList 的区别

都实现了 List，都是有序集合

Vector： 线程安全，同步，性能差。数组实现，适合随机访问，插入和删除性能较差。

ArrayList： 非线程安全，性能好。数组实现，适合随机访问，插入和删除性能较差。

LinkedList： 非线程安全，不需要动态扩容。双向链表实现，插入删除性能较高，不适合随机访问场景。

考察 Java 集合框架，我觉得有很多方面需要掌握：Java 集合框架的设计结构，至少要有一个整体印象。Java 提供的主要容器（集合和 Map）类型，了解或掌握对应的数据结构、算法，思考具体技术选择。将问题扩展到性能、并发等领域。集合框架的演进与发展。

#### Collection 接口

List, Set, Queue/Deque

TreeSet 是由 TreeMap 实现的，HashSet 是由 HashMap 实现的

#### Hashtable, HashMap, TreeMap 有什么不同？

Hashtable： 哈希表，同步，不支持 null，不推荐使用（性能问题）

HashMap： 非同步，支持 null 的键和值，常数时间性能（首选）,线程不安全

LinkedHashMap： 为键值对维护一个双向链表，遍历顺序符合插入顺序。

TreeMap： 红黑树， get,put,remove 等都是 log(n)复杂度。整体顺序由键的顺序决定。

注意： 学习 Map 接口

#### HashMap 源码分析？

HashMap 内部可以看作是数组（Node<k,v>[] table）和链表结合组成的复合结构，数组被分为一个个桶（bucket），通过哈希值决定了键值对在这个数组的寻址；哈希值相同的键值对，则以链表形式存储，你可以参考下面的示意图。这里需要注意的是，如果链表大小超过阈值（TREEIFY_THRESHOLD, 8），图中的链表就会被改造为树形结构。

(秘密都在源码的 putVal 函数里面，添加一个 k-v 对时，如果 table 为空，则创建 table,如果 table 的容量不够了，则进行扩容)

如何避免哈希碰撞？ 有些数据计算出的哈希值差异主要在高位，而 hashmap 里的哈希寻址是忽略容量以上的高位的，将高位移动到低位可以有效避免哈希碰撞。

扩容主要的开销是什么？扩容的时候，需要将老数组中的元素重新放到新的数组中。

为什么 HashMap 要树化？ 容量不够，为了安全考虑

## 线程安全容器

ConcurrentHashMap
java8 以前基于分离锁,采用分段设计，每次只锁住相应的段。
java8 不再使用 Segment，修改为 lazy-load。使用 CAS 操作，在特定情况下进行无锁并发
CopyOnWriteArrayList
ArrayBlockingQueue
SynchronousQueue

#### java 提供了哪些 io 方式？NIO 如何实现多路复用？

IO 包，net 包，Socket,ServerSocket
NIO 包， Channel, Selector, Buffer 等抽象。多路复用，同步阻塞
NIO2 包，异步非阻塞，也有人叫它 AIO

InputStream/OutputStream 和 Reader/Writer 的区别。
NIO, NIO2(AIO)的基本组成（Buffer, Channel, Selector, Charset）。
NIO 的原理是什么。(linux 上依赖于 epoll)

#### synchronized 和 ReentrantLock 有什么区别？

Using Locks Instead of Synchronized Blocks（lock 是公平的，而 synchronized block 不公平，可能导致某个线程一直拿不到锁（starvation））
所谓公平就是指，倾向于把锁给等待时间最久的线程。如果使用 synchronized 是根本不能保证公平的，而 ReetrantLock 可用选择使用公平。
https://stackoverflow.com/questions/4201713/synchronization-vs-lock

#### synchronized 底层是如何实现的？

由一对 monitorenter 和 monitorexit 指令实现。monitor 对象是同步的基本单元。

当一个线程访问同步代码块时，它首先是需要得到锁才能执行同步代码，当退出或者抛出异常时必须要释放锁。monitorenter 指令插入到同步代码块的开始位置，monitorexit 指令插入到同步代码块的结束位置，JVM 需要保证每一个 monitorenter 都有一个 monitorexit 与之相对应。任何对象都有一个 monitor 与之相关联，当一个 monitor 被持有之后，他将处于锁定状态。线程执行到 monitorenter 指令时，将会尝试获取对象所对应的 monitor 所有权，即尝试获取对象的锁。锁存在 Java 对象头里。

### 什么是 Monitor？

我们可以把它理解为一个同步工具，也可以描述为一种同步机制，它通常被描述为一个对象。所有的 Java 对象是天生的 Monitor，每一个 Java 对象都有成为 Monitor 的潜质，因为在 Java 的设计中 ，每一个 Java 对象都带了一把看不见的锁，它叫做内部锁或者 Monitor 锁。Monitor 是线程私有的数据结构，每一个线程都有一个可用 monitor record 列表，同时还有一个全局的可用列表。每一个被锁住的对象都会和一个 monitor 关联（对象头的 MarkWord 中的 LockWord 指向 monitor 的起始地址），同时 monitor 中有一个 Owner 字段存放拥有该锁的线程的唯一标识，表示该锁被这个线程占用。

### jdk 1.6 中对 synchronized 的实现进行了那些优化，使得它显得不是那么重了？

自旋锁、适应性自旋锁、锁消除、锁粗化、偏向锁、轻量级锁等技术来减少锁操作的开销。
锁主要存在四种状态，依次是：无锁状态、偏向锁状态、轻量级锁状态、重量级锁状态，他们会随着竞争的激烈而逐渐升级。注意锁可以升级不可降级，这种策略是为了提高获得锁和释放锁的效率。

引入偏向锁是为了在无多线程竞争的情况下尽量减少不必要的轻量级锁执行路径，因为轻量级锁的获取及释放依赖多次 CAS 原子指令，而偏向锁只需要在置换 ThreadID 的时候依赖一次 CAS 原子指令（由于一旦出现多线程竞争的情况就必须撤销偏向锁，所以偏向锁的撤销操作的性能损耗必须小于节省下来的 CAS 原子指令的性能消耗）。上面说过，轻量级锁是为了在线程交替执行同步块时提高性能，而偏向锁则是在只有一个线程执行同步块时进一步提高性能。

所谓锁的升级就是 JVM 优化 synchorized 运行的机制。在不同的竞争条件下使用不同的锁。当没有竞争出现时，默认使用偏斜锁。jvm 会利用 CAS 操作，在对象头的 mark word 上设置线程 ID，表示这个对象偏向于当前线程。如果有另外的线程试图对某个已经被偏斜过的对象加锁，就要撤销(revoke)偏斜锁，并切换到轻量级锁。轻量级锁如果加锁成功则使用普通轻量级锁，否则使用重量级锁。

#### 一个线程调用两次 start()方法会出现什么情况？

抛出 IllegalThreadStateException，这是一个运行时异常。

线程状态包括：
NEW, 线程被创建出来但是还没有真正启动
RUNNABLE, 线程正在 jvm 中执行，它可能在执行或者在排队
BLOCKED, 线程被阻塞了，可能在等锁
WAITING, 正在等待其他线程采取操作，比如调用了 wait，在等待 notify；也可能调用了 Thread.join()
TIMED_WAIT, 等待状态（一定时间后超时不等）
TERMINATED, 挂了

#### java 并发类库提供的线程池有哪几种，有什么区别？

通常开发者利用 Executors 提供的通用线程池创建方法。目前提供了 5 种不同的线程池创建配置。

newCachedThreadPool(): 会试图缓存线程并重用，当无缓存线程时就创建新的。如果线程闲置时间过长就被移除。

newFixedThreadPool(): 指定线程数目的线程池。

newSingleThreadExecutor(): 只有一个工作线程。

newSingleThreadScheduledExecutor() / newScheduledThreadPool(int corePoolSize): 用来处理周期性任务

newWorkStealingPool(int parallelism): 内部使用 ForkJoinPool，利用 work-stealing 算法，并行处理任务。

```
线程数 = cpu 核数 * (1 + 平均等待时间 / 平均工作时间)
```

#### AtomicInteger 底层实现原理是什么？

基于 CAS 操作。依赖 Unsafe 提供的一些底层能力来进行操作，并用 volatile 的 value 字段来保证可见性。就是在更新的时候先比较原有数值，如果原有数值没变，则更新。如果原有数值已经变了，则更新失败或者重试。更底层的话，则是依赖 cpu 的指令集。

#### 类加载过程

类加载分为三个步骤：加载，链接，初始化。

加载表示将字节码 Load 到 jvm 并映射为 class 对象，加载阶段为用户可以参与的阶段，用户可以实现自己的 classLoader。

链接包括了验证，准备，解析等多个阶段。这一步将原始的类定义信息转入 jvm 运行的过程中。

初始化阶段真正去执行类初始化的逻辑，包括静态字段赋值以及执行静态初始化块内的逻辑等等。父类型的初始化优先于当前类型的初始化。

#### 什么是双亲委派模式？

当类加载器试图加载某个类型时，除非父加载器找不到相应类型，否则尽量将这个任务代理给当前加载器的父加载器去做。

## 有哪些方法可以在运行时动态生成一个类？

如何利用字节码操纵技术，实现基本的动态代理逻辑？

除了动态代理，字节码操纵技术还有哪些应用场景？
各种 mock 框架，orm 框架，ioc 框架,profiler 工具,代码生成工具。

## 如何监控和诊断 jvm 堆内内存和堆外内存的使用？

jconsole, visualvm
jstat, jmap
生成 heapdump
查看 gc 日志

jvm 堆被分为：新生代，老年代，永久代（jdk8 开始已经没了）。
新生代为大部分对象被创建和销毁的区域，在通常的 java 应用中，绝大部分对象生命周期都很短。其内部又分为 eden 区域（新分配的对象），from 区域和 to 区域（从 minor gc 中保留下来的对象,称为 survivor 区域）

老年代放置长生命周期的对象，通常为从 survivor 区域拷贝过来的对象。

## 有哪些垃圾收集器？

serial GC,
parNew GC
CMS GC
Parrallel GC
G1

## 如何打开 gc 日志

-XX:+PrintGCDetails

## 必读书单

thinking in java
java 核心技术

effective java
head first 设计模式
java 并发实战编程

深入理解 jvm
java 性能优化权威指南
