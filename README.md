# dayu_path

[![Build Status](https://travis-ci.org/phenom-films/dayu_path.svg?branch=master)](https://travis-ci.org/phenom-films/dayu_path)

针对影视行业的文件路径处理类。比起传统的os.path 有着下面的优点：

* 将文件路径作为对象处理
* 更好的针对影视行业文件优化。可以快速得到frame count、version 等字段
* 扫描文件自动拼合序列帧，并且可以识别丢帧
* 更快捷的文件序列帧格式转换。支持%0?d、####、$F? 的三种形式
* 序列批量改名、移动、拷贝（帧数自动重排）
* 支持用户自行对DayuPath 添加更多的方法、属性

# 如何安装
```bash
pip install -U dayu-path
```

# 简单用法说明

```python
from dayu_path import DayuPath

# 初始化
disk_path = DayuPath('/some/v0001/A001C001_170922_E4FB.1001.exr')

# 查询父级目录
assert disk_path.parent == '/some/v0001'

# 拼接子文件夹、子文件
assert disk_path.parent.child('child', 'new_file.txt') == '/some/v0001/child/new_file.txt'

# 获得文件名、文件扩展名、文件主干部分
assert disk_path.name == 'A001C001_170922_E4FB.1001.exr'
assert disk_path.ext == '.exr'
assert disk_path.stem == 'A001C001_170922_E4FB.1001'

# 扫描当前目录下的所有文件夹、文件
print disk_path.parent.listdir()

# 遍历当前文件夹下所有深度的文件夹、文件
for single_file in disk_path.parent.walk():
    print single_file

# 快速获得相应的version、frame count、udim
assert disk_path.frame == 1001
assert disk_path.version == 'v0001'
assert disk_path.udim == 1001

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
    print sequence_file.frames  # [1001, 1002, 1003, 1004]
    print sequence_file.missing  # []
    
# 批量改名移动、拷贝
src_path = DayuPath('/src/path/seq.%04d.exr')
dst_path = DayuPath('/dst/path/new_name.%04d.exr')
src_path.rename_sequence(dst_path, start=2000, step=1, parents=True, keep_missing=True)
src_path.copy_sequence(dst_path)

# 直接打开系统文件浏览器，弹窗查看
disk_path.show()

```


# DayuPathPlugin 的插件用法

如果用户需要对DayuPath 添加自定义的函数属性，除了常规的继承方法之外。还可以使用DayuPathPlugin 将自定义的方法、属性以插件的形式加入DayuPath。
这样可以更加灵活的在代码的任意地方根据需要增加、减少功能。

```python
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

```