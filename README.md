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

# 快速获得相应的version、frame count
assert disk_path.frame == 1001
assert disk_path.version == 'v0001'

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