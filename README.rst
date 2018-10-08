dayu_path
=========

|Build Status|

针对影视行业的文件路径处理类。比起传统的os.path 有着下面的优点：

-  基于unipath，将文件路径作为对象处理
-  更好的针对影视行业文件优化。可以快速得到frame count、version 等字段
-  扫描文件自动拼合序列帧，并且可以识别丢帧
-  更快捷的文件序列帧格式转换。支持%0?d、####、$F? 的三种形式
-  支持用户自行对DayuPath 添加更多的方法、属性

简单用法说明
============

继承与unipath，因此具备所有unipath 的方法。 （unipath
的git：https://github.com/mikeorr/Unipath ）

.. code:: python

   from dayu_path import DayuPath

   # 初始化
   disk_path = DayuPath('/some/v0001/A001C001_170922_E4FB.1001.exr')

   # 查询父级目录
   assert disk_path.parent == '/some/v0001'

   # 拼接子文件夹、子文件
   assert disk.path.parent.child('child', 'new_file.txt') == '/some/v0001/child/new_file.txt'

   # 获得文件名、文件扩展名、文件主干部分
   assert disk_path.name == 'A001C001_170922_E4FB.1001.exr'
   assert disk.path.ext == '.exr'
   assert disk_path.stem == 'A001C001_170922_E4FB.1001'

   # 扫描当前目录下的所有文件夹、文件
   print disk_path.parent.listdir()

   # 遍历当前文件夹下所有深度的文件夹、文件
   for single_file in disk_path.parent.walk():
       print single_file

   # 快速获得相应的version、frame count
   assert disk_path.frame == 1001
   assert disk_path.version == 'v0001'

   # 快速得到文件的挂载目录（盘符、挂载点）
   assert disk_path.root == '/'

   # 判断文件是本地文件系统，还是网络文件系统
   assert DayuPath('/some/local/file').is_local == True
   assert DayuPath('/some/network/file').is_network == True

   # 文件实际名称转换为序列帧形式
   assert disk_path.to_pattern() == '/some/v0001/A001C001_170922_E4FB.%04d.exr'
   assert disk_path.to_pattern('#') == '/some/v0001/A001C001_170922_E4FB.####.exr'
   assert disk_path.to_pattern('$') == '/some/v0001/A001C001_170922_E4FB.$F4.exr'

   # 从序列帧的形式，恢复成为绝对文件路径
   disk_pattern = disk_path.to_pattern()
   assert disk_pattern.pattern == '%04d'
   assert disk_pattern.restore_pattern(1234) == '/some/v0001/A001C001_170922_E4FB.1234.exr'

   # 文件扫描，支持递归深度。并且将扫描的文件自动识别为序列帧的形式
   for sequence_file in disk_path.scan(recursive=True):
       print sequence_file
       # SequenceFile(filename='/some/v0001/A001C001_170922_E4FB.%04d.exr'
       #               frames=[1001, 1002, 1003, 1004, 1006],
       #               missing=[1005])

DayuPathPlugin 的插件用法
=========================

如果用户需要对DayuPath
添加自定义的函数属性，除了常规的继承方法之外。还可以使用DayuPathPlugin
将自定义的方法、属性以插件的形式加入DayuPath。
这样可以更加灵活的在代码的任意地方根据需要增加、减少功能。

.. code:: python

   from dayu_path import DayuPath, DayuPathPlugin

   # 用户自己添加的功能函数
   def my_function(self, *args, **kwargs):
       print args, kwargs

   # 增加插件函数 （实例化方法）
   DayuPathPlugin.register_func(my_function)
   DayuPath('/some/path/file').my_function(123)    # (1,2,3), {}

   # 也可以使用装饰器来进行注册
   @DayuPathPlugin.register_func
   def other_function(self):
       return 'hello world'


   # 增加插件属性 （类属性）
   DayuPathPlugin.register_attribute('my_key', default_value=100)
   assert DayuPath('/some/other/file').my_key == 100

   # 取消插件函数、插件属性
   ret = DayuPathPlugin.unregister('my_function')
   assert ret == True
   ret = DayuPathPlugin.unregister('my_key')
   assert ret == True

.. |Build Status| image:: https://travis-ci.org/phenom-films/dayu_path.svg?branch=master
   :target: https://travis-ci.org/phenom-films/dayu_path
