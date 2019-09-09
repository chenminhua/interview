## 1. 介绍下乐观锁 OCC 和悲观锁 OCC 的区别？什么时候用乐观锁？[**]

乐观锁假设并发的事务不会彼此影响，各个事务在不产生锁的情况下各自处理数据。在提交之前，检查在该事务读取数据后，数据是否有被修改过。如果出现了冲突则回滚。悲观锁则在进行任意记录修改前，先尝试为该记录加写锁，只有加锁成功才能操作。一般来说，读明显大于写的情况采用乐观锁，而写频繁的情况下则采用悲观锁。

## 2.介绍下共享锁和排他锁的区别？如何加这两种锁?[**]

共享锁又被称为读锁(SELECT ... LOCK IN SHARE MODE;)，一旦数据被加了读锁，其他事务还是可以加读锁，但是不能加写锁。排他锁又被称为写锁(SELECT ... FOR UPDATE)，一旦加上写锁，其他事务就不能再加任何锁。

## 1. ACID 分别是什么意思？[**]

A(atomic,原子)，C(consistency,一致性),I(isolation,隔离性),D(durability,持久性)。原子性指事务中的操作要么都做要么都不做。一致性指事务总是让数据从一个正确状态转换到另一个正确状态。隔离性有好多种，表示事务中间状态是否能相互感知。持久性表示事务提交成功后的结果是永久的。

## 2.什么是脏读？不可重复读？幻读？[**]

脏读：一个事务还没提交，其他事务却访问到了其中间结果。不可重复读：同一个事务读取同一条记录两次，却得到不同的结果（被另一个事务修改了）。幻读：一个事务读取两次，得到了不同的记录条数（另一个事务进行了增删）。

## 3.innodb 的隔离级别从低到高有哪几个[**]

READ UNCOMMITTED 脏读，不可重复读，幻读
READ COMMITTED 不可重复读，幻读
REPEATABLE READ （InnoDB 默认） 幻读 (InnoDB 默认隔离级别为 REPEATABLE READ，使用 NEXT-KEY Lock 的锁算法避免幻读。)
SERIALIZABLE 完全串行化的读，每次读都要获得共享锁，读写都会相互阻塞。
隔离级别从低到高分为 (隔离级别越低，事务请求的锁越少，持有锁的时间越短。)

## 1. 简单讲讲 B tree 和 B+ tree？为什么数据库会用他们来构建索引[***]

## 2. mysql 是如何使用索引的？[**]

mysql 可以在 where, order by 以及 group by 列中使用索引。一般来说 mysql 在一个表上只选择一个索引，在个别情况下 Mysql 会使用一个以上的索引。

## 3. 添加过多索引有什么坏处？[**]

写会变慢，读也可能变慢，会占用更多磁盘，后期加索引会阻塞其他语句。

## 1. 如何选择主键？[**]

## 2. char vs varchar [**]

## 3. 什么时候使用 Null，什么使用使用 NOT Null? [***]

[提高搜索性能](http://stackoverflow.com/questions/1017239/how-do-null-values-affect-performance-in-a-database-search)

## 1. 什么是主从复制，主主复制 [***]

主从复制是指一个主库多个从库的扩展模式，数据写入集中在主库，从库不停地从主库复制数据，主从都可以提供查询，但是只有主库可以处理增删改请求。主从复制主要的问题在于，主库依然是一个单点，当主库出现故障时，需要将从库提升为主库。主主复制则是多个主库都负责读和写操作，写入时需要相互协调，如果一个主库挂了，系统可以继续读写。主主复制的问题在于需要保持一致性。除此之外，复制还可能会带来很多问题，比如主库在将数据写入其他节点前挂掉怎么办？

## 1. mysql 中 join 有哪几种？区别是什么？

join 主要有 CROSS/INNER/OUTER JOIN，CROSS join 只进行逻辑查询第一个步骤（产生笛卡尔积虚拟表），INNER join 进行第一第二步（按照 ON 过滤条件来进行数据匹配操作），OUTER join 进行前三步（添加外部行）。

```
CROSS JOIN假设A表有3条记录，B有4条记录SELECT count(1) FROM A, B有12条结果。

INNER JOIN INNER 可以省略。由于不会添加外部行，对于 INNER JOIN 来说，on 子句和 where 子句没啥区别。比如下面两个查询的逻辑查询和物理查询都一样。
SELECT ... FROM a, b WHERE a.x = b.x
SELECT ... FROM a INNER JOIN b on a.x = b.x

与INNER JOIN不同的是，在通过OUTER JOIN添加的保留表汇总存在未找到的匹配数据。 mysql 支持 LEFT OUTER JOIN 和 RIGHT OUTER JOIN,其中 OUTER 可以省略

多表连接
SELECT m.name, l.id, t.action from LgUnit as l
JOIN Material as m ON l.material_id=m.id
JOIN `LgTransfer` as t on l.`lastTransferId` = t.id
```

## 2. 逻辑 io 和物理 io 的区别是什么？ [****]

## 3. 谈谈 sql 调优有哪些方法？

SQL 调优是一个范围很广的话题，有很多相关的[书](https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=sql+tuning)可以作为参考。
利用**基准测试**和**性能分析**来模拟和发现系统瓶颈很重要。

- **基准测试** - 用 [ab](http://httpd.apache.org/docs/2.2/programs/ab.html) 等工具模拟高负载情况。
- **性能分析** - 通过启用如[慢查询日志](http://dev.mysql.com/doc/refman/5.7/en/slow-query-log.html)等工具来辅助追踪性能问题。

基准测试和性能分析可能会指引你到以下优化方案。

为查询缓存优化你的查询
