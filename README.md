# dayu_path

针对影视行业的文件路径处理类。比起传统的os.path 有着下面的优点：

* 基于unipath，将文件路径作为对象处理
* 更好的针对影视行业文件优化。可以快速得到frame count、version 等字段
* 扫描文件自动拼合序列帧，并且可以识别丢帧
* 更快捷的文件序列帧格式转换。支持%0?d、####、$F? 的三种形式


# 简单用法说明

继承与unipath，因此具备所有unipath 的方法。
（unipath 的git：https://github.com/mikeorr/Unipath ）

```python
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
```