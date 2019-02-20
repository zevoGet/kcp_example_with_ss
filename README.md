# 这是个ss使用kcp的简单例子
把 kcp和ss 一起使用，让科学更加科学，

## 【注意事项和声明】，以上步骤，本文只有python ctypes 调用 和 测试
运行kcp_struct1.py 可以测试

## 主要步骤
  - ~~gcc 编译kcp源文件~~（已完成）【必须有这个编译好的文件】
    + 克隆kcp的git仓库（git clone https://github.com/skywind3000/kcp）
    + 进入到项目，执行 gcc -fPIC -shared ikcp.c -o kcp_clib.so
    + 拿到编译成功的文件 cp kcp_clib.so ~/kcp_clib.so
  - ~~python ctypes调用~~（已完成）
    + python编写对应的kcp的主结构体和主要回调函数（update 和 writelog）
    + 按照kcp的文档配置kcp
  - 将ss的tcp流转化到kcp（正在做）
    - 拿到ss的仓库
    - 修改server.py,tcpReply.py
    
  - kcp 发送流，可以自己封装，也可以直接使用udp（这里的流建议加密一下，如果能修改udp的src源地址和ttl也是可以的）
    + 发送加密
    + 接收解密
    + 如果被运营商封udp（这个可以做udp心跳） 则自动走tcp
  - 重新编译 ss
  

