### PostScene ——————  一个强大的工具，基于 Postman 接口自动化场景设计
***

**使用Xmind或者Yaml 设计 postman 自动化场景**

**背景**: postman是一个比较轻量级的接口测试工具，在单个接口的测试表现优秀。在批量测试接口方面则提供了Runner Collections这种方式，虽然可以用来做流程测试，但在管理上不是很方便。例如：在postman建立一个collection作为接口文档，然后再建立另外一个collection作为场景测试，接着从接口文档的collection中挑选接口，并复制到场景测试的collection中，而且可能在不同的场景都共用同一个接口，这种方式是听不错的，只是当接口的版本升级之后，需要在场景中找出所有对应的接口进行修改，这样在管理上会比较麻烦。

 **思想**: 这个工具根据Xmind或Yaml所写的场景流程，从接口文档的collection中生成一个场景测试的collection，这样即使版本升级，只需要重新生成一次即可，相当方便，同时也提供了一些方便的设参方式和断言。

1.  **管理方便** 。只需要管理接口文档的collection和Xmind/Yaml脚本。
2.  **场景流程更直观** 。在Xmind/Yaml上可以直观的看到整个流程，在细节上也可以看到每个接口的参数定义，以及断言内容。
3.  **代码编写简化** 。在测试行业中，普遍都是代码能力比较差，虽然测试不需要特别强的代码编写能力，postman在Tests界面中也提供了一些快捷片段，但是还是不足够简化，而且也不全面，比如对请求的参数进行签名。
4.  **提供一些快捷的函数**。postman提供的内置函数还是比较少的，比如随机生成32的UUID，md5,获取当前时间，获取前7天，前30天的日期，参数签名等等，这些都需要自己手动写代码。
5.  **无依赖性**。本工具只是一个脚本转换成Postman的脚本工具，即使以后不用，完全可以自己维护Postman的脚本。
.......

### 先来看看效果图
![输入图片说明](https://github.com/yajuntang/PostScene/blob/master/screenshots/101586877574_.pic.jpg)


#### 例子
***
* 新建一个文件，名字叫什么不重要，但为了迭代开发的考虑，最好还是加上版本号。
> 外卖App接口测试v1.0.yaml
* 脚本编写

```yaml
name: demo*scene                                              #collection 的名字
scene:
   name: 下单流程                                             #collection文件夹的名字
   scene:
     登陆:                                                   #API接口名称
       pre:                                                 #接口请求前脚本
         sign:                                              #参数签名
           secret: 1850e165f1fc19420f2ba3d3a1a5ffe4
         set:                                               #设置变量值
           username: user
           password: user123
           time: $$times                                    #获取现在的时间
           onceToken: $$uuid32                              #生成32位的uuid
       tests:                                               #请求后脚本
         assert:                                            #请求后断言
           express:
             content: $json.data.code === '1'               #断言返回的json数据的code 是否等于1
             set:                                           #断言成功保存token和uid数据
               token: $json.data.token
               uid: $json.data.uid
     通过餐厅名字搜索餐厅:
       pre:
         sign:
           secret: 1850e165f1fc19420f2ba3d3a1a5ffe4
         set:
           canteenName: 喜茶
       tests:
         assert:
           expect:                                         #断言返回的canteenList的每一个对象的名称都包含喜茶
             content: $json.data.canteenList
             item: $it.name                                 
             include: 喜茶
             set:
               canteenId: $$find(json.data.canteenList, it.canteenName == '喜茶GO').canteenId  #获取喜茶Go的CanteenId
     通过商品名字搜索商品:
       pre:
         sign:
           secret: 1850e165f1fc19420f2ba3d3a1a5ffe4
         ref: canteenId
         set:
           goodsName: 奥利奥千层
       tests:
         assert:
           expect:
             content: $json.data.goodsList
             item: $item.name
             include: 奥利奥千层
             set:
               goodsId: $$find(json.data.goodsList, it.goodsName == '奥利奥千层').goodsId
     加入购物车:
       pre:
         sign:
           secret: 1850e165f1fc19420f2ba3d3a1a5ffe4
         ref: goodsId
         set:
           count: 1
       tests:
         assert:
           express:
             content: $json.code === '1'
             set:
               pocketId: $json.data.pocketId
.......

```
* 脚本转换
1. 使用git或者浏览器下载本项目，再用pycharm打开。

2. 在Postman中选择你已经准备好的api文档collection 然后导出。这里导出为 demo.postman_collection.json

![导出api文档collection](https://github.com/yajuntang/PostScene/blob/master/screenshots/71586877556_.pic.jpg)

3. 把导出的文档放入项目中的api_document 脚本放入xmind或yaml

![放置脚本](https://github.com/yajuntang/PostScene/blob/master/screenshots/781586877562_.pic_hd.jpg)

4. 打开postman_collection_generator文件中的Index.py 把xmind_path和api_document_path改成你的，右键 Run Index。

![开始转换](https://github.com/yajuntang/PostScene/blob/master/screenshots/91586877568_.pic_hd.jpg)

5. 生成的场景文件放在scene文件夹中，使用postman的import 把他导入

![使用postman的import](https://github.com/yajuntang/PostScene/blob/master/screenshots/101586877574_.pic.jpg)

6. 最后可以开始Run collection啦

![最后可以开始Run collection啦](https://github.com/yajuntang/PostScene/blob/master/screenshots/111586877579_.pic.jpg)
#### 教程
***
>如果你对Postman的Script很熟悉，那以下的内容对你来说绝对是无障碍的。不熟悉也没关系，只要照猫画虎，也能完成脚本的编写，设计这个初中就是为了降低门槛。

**学前须知** : 每一个测试用例都由两部分组成 **pre(请求前)** 和 **tests(请求后)** ，pre可以没有，但tests断言一定要有，不然没有意义。每一个测试用例的名称必须和文档中的collection的接口名称一致。这是规范。

 **基础(Postman的设置变量)**  
1. 常规， **变量名称** 可以和 **参数名称** 相同，也可以不同，用{{}}包裹

![输入图片说明](https://github.com/yajuntang/PostScene/blob/master/screenshots/121587005682_.pic.jpg)

2. json，  **变量名称** 可以和 **参数名称** 相同，也可以不同，用{{}}包裹

![输入图片说明](https://github.com/yajuntang/PostScene/blob/master/screenshots/131587005688_.pic.jpg)

### 脚本语法标签

 + **请求前: pre**  
    - [参数设置变量: set]()   
    - [参数引用变量: ref]()      
    - [参数签名: sign]()      
 + **请求后: tests**  
    - 断言: assert  
        - [状态: status]()    
        - [是: tobe]()    
        - [不是: notTobe]()    
        - [有: tohave]()    
        - [没有: notTohave]()    
        - [表达式: express]()    
        - [预期: except]()    
        - [条件跳转: next]()    
        - [保存变量: set]()    
 + **快捷函数**  
    - [唯一标识: $uuid32]()    
    - [md5加密: $md5]()    
    - [获取列表最后一个: $last]()    
    - [查找列表元素: $find]()    
    - [反向查找列表元素: $find_last]()    
    - [获取符合的元素: $filter]()    
    - [获取毫秒级时间戳: $timeS]()    
    - [获取秒级时间戳: $times]()    
    - [获取本周开始时间戳: $weekStart]()    
    - [获取本周结束时间戳: $weekEnd]()    
    - [获取上周开始时间戳: $lastWeekStart]()    
    - [获取上周开始时间戳: $lastWeekEnd]()    
    - [获取本月1号时间戳: $monthStart]()    
    - [获取本月结束时间戳: $monthEnd]()    
    - [获取上月1号时间戳: $lastMonthStart]()    
    - [获取上月结束时间戳: $lastMonthEnd]()    
    - [获取前7天时间戳: $last7DaysStart]()    
    - [获取前30天时间戳: $last30DaysStart]()    
    - [时间戳转日期格式: $dateFormat]()    

> 写在最后: 目前只提供了这些内置函数，虽然不多但也够用，如果你有什么特别的需要，可以提一个issues。
> 最后，祝你测试愉快 :blush: 
