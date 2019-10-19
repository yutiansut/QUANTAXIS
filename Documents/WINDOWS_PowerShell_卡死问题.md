## 控制台窗口和powershell运行服务会卡住的解决办法


之前使用nodejs做了一个简单的web服务，通过控制台窗口运行，通过浏览器访问发现有时候浏览器等很久数据都加载不出来，以为是代码有问题，后来发现是控制台卡住了，按一下enter键就好了，当时百度了一下，没有找到有用的消息，就没有管了，最近使用dotnet core 运行的时候，又遇到了，于是又百度了一下，所幸，这次找到原因和解决办法了，原来是控制台窗口的快速编辑模式导致的。

解决办法是可以打开任意一个cmd或powershell窗口，然后在title栏右键，点击属性，在选项界面有个快速编辑模式，去掉即可。

![](http://pic.yutiansut.com/powershell%E8%AE%BE%E7%BD%AE.png)

而原因则是有在控制台进行日志输出。。。

参考链接：
http://blog.csdn.net/java2000_net/article/details/2920155#reply
http://blog.csdn.net/sunjiaminaini/article/details/36631601
http://blog.csdn.net/qq_28919337/article/details/77931060
