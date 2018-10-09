#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from unipath import Path

from config import *
from data_structure import SequentialFiles


class DayuPath(Path):

    def __new__(cls, *args, **kw):
        '''
        重载 __new__ , 为了保证不论win32、darwin、linux2 三个操作系统的路径都是使用 '/' 进行层级切割
        :param args: 理论上只有args[0]，类型是string
        :param kw:
        :return:
        '''
        if args:
            if not args[0]:
                return None

            if isinstance(args[0], DayuPath):
                return args[0]

            if isinstance(args[0], basestring):
                normalize_path = args[0].replace('\\', '/').replace('//', '/')
                match = WIN32_DRIVE_REGEX.match(normalize_path)
                if match:
                    normalize_path = normalize_path.replace(match.group(1), match.group(1).lower())
                new_args = (normalize_path,)
                return super(DayuPath, cls).__new__(cls, *new_args, **kw)

            return None
        return None

    @property
    def is_network(self):
        try:
            import psutil
        except ImportError as e:
            raise

        disk_partition = next((d for d in psutil.disk_partitions(True) if DayuPath(d.mountpoint) == self.root), None)
        if disk_partition:
            return True if disk_partition.fstype in NETWORK_FILE_SYSTEM else False
        return False

    @property
    def is_local(self):
        return not self.is_network

    @property
    def frame(self):
        '''
        返回解析出的帧数
        :return: int 类型。如果没有解析成功，返回-1
        '''
        if self.ext.lower() in tuple(EXT_SINGLE_MEDIA.keys()):
            return -1

        match = FRAME_REGEX.match(self.stem)
        if match:
            return int(match.group(1))
        return -1

    @property
    def root(self):
        import os
        is_mount = os.path.ismount
        temp_path = self
        while not is_mount(temp_path.parent):
            temp_path = temp_path.parent

        return temp_path.parent

    @property
    def version(self):
        match = VERSION_REGEX.match(self)
        if match:
            return match.group(1)
        return None

    @property
    def pattern(self):
        '''
        提取出当前路径的pattern 标识。
        支持 %0xd，####，$Fn 这三种形式
        :return: 如果匹配成功，返回匹配的pattern string；否则返回None
        '''
        match = PATTERN_REGEX.match(self.stem)
        return match.group(1) or match.group(3) or match.group(4) if match else None

    def to_pattern(self, pattern='%'):
        '''
        将绝对路径转换为pattern 形式的路径。
        :param pattern: '%' 表示变成%04d 类型的路径；'#' 表示变成#### 类型类型的路径；'$'表示变成$F4 类型的路径
        :return: DayuPath 对象
        '''
        if self.ext and self.ext.lower() in tuple(EXT_SINGLE_MEDIA.keys()):
            return self

        pattern_match = PATTERN_REGEX.match(self.stem)
        if pattern_match:
            if pattern_match.group(1):
                if pattern == '%':
                    return self
                if pattern == '#':
                    return DayuPath(self.replace(pattern_match.group(1),
                                                 '#' * int(pattern_match.group(2) if pattern_match.group(2) else 1)))
                if pattern == '$':
                    return DayuPath(self.replace(pattern_match.group(1),
                                                 '$F{}'.format(
                                                         int(pattern_match.group(2) if pattern_match.group(2) else 1))))
                else:
                    return self

            if pattern_match.group(3):
                if pattern == '%':
                    return DayuPath(self.replace(pattern_match.group(3),
                                                 '%0{}d'.format(len(pattern_match.group(3)))))
                if pattern == '#':
                    return self
                if pattern == '$':
                    return DayuPath(self.replace(pattern_match.group(3),
                                                 '$F{}'.format(len(pattern_match.group(3)))))
                else:
                    return DayuPath(self.replace(pattern_match.group(3),
                                                 '%0{}d'.format(len(pattern_match.group(3)))))
            if pattern_match.group(4):
                if pattern == '%':
                    return DayuPath(self.replace(pattern_match.group(4),
                                                 '%0{}d'.format(
                                                         pattern_match.group(5) if pattern_match.group(5) else 1)))
                if pattern == '#':
                    return DayuPath(self.replace(pattern_match.group(4),
                                                 '#' * int(pattern_match.group(5) if pattern_match.group(5) else 1)))
                if pattern == '$':
                    return self
                else:
                    return DayuPath(self.replace(pattern_match.group(4),
                                                 '%0{}d'.format(
                                                         pattern_match.group(5) if pattern_match.group(5) else 1)))

            return self

        else:
            match = FRAME_REGEX.match(self.stem)
            if match:
                if pattern == '%':
                    replace_string = '%0{}d'.format(len(match.group(1)))
                elif pattern == '#':
                    replace_string = '#' * len(match.group(1))
                elif pattern == '$':
                    replace_string = '$F{}'.format(len(match.group(1)))
                else:
                    replace_string = '%0{}d'.format(len(match.group(1)))

                new_name = self.name[:match.start(1)] + \
                           replace_string + \
                           self.name[match.end(1):]
                return DayuPath(self.parent + '/' + new_name)

            else:
                return self

    def escape(self):
        import re
        return re.sub("(!|\$|#|&|\"|\'|\(|\)| |\||<|>|`|;)", r'\\\1', self)

    def restore_pattern(self, frame):
        '''
        将pattern 化的序列帧，回复成为正常的帧数据对路径
        :param frame: int，可以是任意的正整数
        :return: DayuPath 对象
        '''
        if frame is None:
            return self

        if int(frame) < 0:
            return self

        match = PATTERN_REGEX.match(self.name)
        if match:
            if match.group(1):
                return DayuPath(self.replace(match.group(1),
                                             '{{:0{frame_padding}d}}'.format(
                                                     frame_padding=int(match.group(2) if match.group(2) else 1)).format(
                                                     frame)))
            elif match.group(3):
                return DayuPath(self.replace(match.group(3),
                                             '{{:0{frame_padding}d}}'.format(
                                                     frame_padding=len(match.group(3))).format(frame)))
            elif match.group(4):
                return DayuPath(self.replace(match.group(4),
                                             '{{:0{frame_padding}d}}'.format(
                                                     frame_padding=(match.group(5) if match.group(5) else 1)).format(
                                                     frame)))
        else:
            return self

    def scan(self, recursive=False, filter=None):
        '''
        扫描硬盘路径，可以是递归或者非递归。
        返回的文件总是会被加入 SequentialFiles() 这个数据结构中。
        如果.frames 为[]，表示是独立的文件，而不是序列文件。
        如果用户希望是常规意义的遍历文件，请使用 DayuPath.walk() 方法。

        :param recursive: True，表示递归搜索；False 表示只搜索当前文件
        :return: list of SequentialFiles 对象
        '''

        from config import EXT_SINGLE_MEDIA
        if self.lower().endswith(tuple(EXT_SINGLE_MEDIA.keys())):
            yield SequentialFiles(self, [], [])
            raise StopIteration

        import os
        import bisect
        from collections import Iterable

        def filter_callback(filter):
            is_file = os.path.isfile

            if filter is None:
                ignore_start = SCAN_IGNORE['start']
                ignore_end = SCAN_IGNORE['end']
                return lambda p: is_file(p) and \
                                 not (p.name.startswith(ignore_start)) and \
                                 not (p.name.endswith(ignore_end))

            if callable(filter):
                return filter
            if isinstance(filter, basestring):
                return lambda p: is_file(p) and p.lower().endswith(filter)
            if isinstance(filter, dict):
                ignore_start = filter.get('start', SCAN_IGNORE['start'])
                ignore_end = filter.get('end', SCAN_IGNORE['end'])
                return lambda p: is_file(p) and \
                                 not (p.name.startswith(ignore_start)) and \
                                 not (p.name.endswith(ignore_end))

            if isinstance(filter, Iterable):
                return lambda p: is_file(p) and p.lower().endswith(tuple(filter))
            return is_file

        scan_path, file_flag = (self, False) if self.isdir() else (self.parent, True)
        run_filter = filter_callback(filter)

        if recursive:
            for root, sub_folder, sub_files in os.walk(scan_path):
                seq_list = {}
                for single_file in sub_files:
                    full_path = DayuPath(root).child(single_file)
                    if run_filter(full_path):
                        filename_pattern = full_path.absolute().to_pattern()
                        frames_list = seq_list.setdefault(filename_pattern, [])
                        if filename_pattern != full_path:
                            bisect.insort(frames_list, full_path.frame)

                if file_flag:
                    k = self.absolute().to_pattern()
                    v = seq_list.get(k, None)
                    if v is not None:
                        yield SequentialFiles(k, v, (sorted(set(range(v[0], v[-1] + 1)) - set(v))) if v else [])
                    raise StopIteration

                if seq_list:
                    for k, v in seq_list.items():
                        yield SequentialFiles(k, v, (sorted(set(range(v[0], v[-1] + 1)) - set(v))) if v else [])
                else:
                    raise StopIteration

        else:
            seq_list = {}
            for x in scan_path.listdir(filter=run_filter):
                filename_pattern = x.absolute().to_pattern()
                frames_list = seq_list.setdefault(filename_pattern, [])
                if filename_pattern != x:
                    bisect.insort(frames_list, x.frame)

            if file_flag:
                k = self.absolute().to_pattern()
                v = seq_list.get(k, None)
                if v is not None:
                    yield SequentialFiles(k, v, (sorted(set(range(v[0], v[-1] + 1)) - set(v))) if v else [])
                raise StopIteration

            if seq_list:
                for k, v in seq_list.items():
                    yield SequentialFiles(k, v, (sorted(set(range(v[0], v[-1] + 1)) - set(v))) if v else [])
            else:
                raise StopIteration

    def _show_in_win32(self, show_file=False):
        import os
        if show_file:
            os.startfile(self)
        else:
            os.startfile(self if self.isdir() else self.parent)

    def _show_in_darwin(self, show_file=False):
        import subprocess
        if show_file:
            subprocess.Popen('osascript -e \'tell application "Finder" to reveal ("{}" as POSIX file)\''.format(self),
                             shell=True)
        else:
            subprocess.Popen(['open', self if self.isdir() else self.parent])

    def _show_in_linux2(self, show_file=False):
        import subprocess
        subprocess.Popen(['xdg-open', self if self.isdir() else self.parent])

    def show(self, show_file=False):
        '''
        在不同的操作系统中直接弹出窗口，显示文件所在的路径
        :param show_file: 如果希望显示的是某个具体的文件，使用True；如果希望显示路径的上层文件夹，使用False
        :return:
        '''
        import sys
        sub_func = getattr(self, '_show_in_{}'.format(sys.platform), None)
        if sub_func:
            sub_func(show_file=show_file)


if __name__ == '__main__':
    aa = DayuPath('/Users/andyguo/Desktop/camera_format_tets.nk')
    for x in aa.scan(recursive=True):
        print x
