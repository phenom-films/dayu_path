#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import unittest
from unittest import TestCase

from dayu_path import DayuPath


class TestDayuPath(TestCase):
    def test___new__(self):
        self.assertEqual(DayuPath(''), None)
        self.assertEqual(DayuPath([]), None)
        self.assertEqual(DayuPath(tuple()), None)
        self.assertEqual(DayuPath(set()), None)
        self.assertEqual(DayuPath(dict()), None)
        self.assertEqual(DayuPath('any_string'), 'any_string')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/111111111.jpg'), '/Users/andyguo/Desktop/111111111.jpg')
        self.assertEqual(DayuPath(u'/Users/andyguo/Desktop/中文路径 测试.jpg'), u'/Users/andyguo/Desktop/中文路径 测试.jpg')
        self.assertEqual(DayuPath('D:/data/test.jpg'), 'd:/data/test.jpg')
        self.assertEqual(DayuPath('d:\\data\\test.jpg'), 'd:/data/test.jpg')
        self.assertEqual(DayuPath('D:\\data\\test.jpg'), 'd:/data/test.jpg')
        obj = DayuPath('/Users/andyguo/Desktop/111111111.jpg')
        self.assertIs(DayuPath(obj), obj)

    def test_os_functions(self):
        path = DayuPath(self.mock_path).child('cam_test', 'A001C001_180212_RG8C.9876521.exr')
        self.assertIsNotNone(path.state())
        self.assertIsNotNone(path.lstate())
        self.assertIsNotNone(path.exists())
        self.assertIsNotNone(path.lexists())
        self.assertIsNotNone(path.isfile())
        self.assertIsNotNone(path.isdir())
        self.assertIsNotNone(path.islink())
        self.assertIsNotNone(path.ismount())
        self.assertIsNotNone(path.atime())
        self.assertIsNotNone(path.ctime())
        self.assertIsNotNone(path.mtime())
        self.assertIsNotNone(path.size())

    def test_frame(self):
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/1.jpg').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/12.jpg').frame, 12)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/1001.jpg').frame, 1001)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/0024.jpg').frame, 24)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/1.mov').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/14.mov').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/123.mp4').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/v001.jpg').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/v002_999.jpg').frame, 999)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/aaa_test.1.jpg').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/aaa_test.12.jpg').frame, 12)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/aaa_test.123.jpg').frame, 123)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/aa_v001.jpg').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_v0023.012.jpg').frame, 12)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_v0023_1234.jpg').frame, 1234)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_v0023.jpg').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_v0023.mov').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/MVI1023.jpg').frame, 1023)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/MVI1023.MP4').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/test576bb.mov').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/test576bb.jpg').frame, -1)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/576_hkke.jpg').frame, -1)
        self.assertEqual(DayuPath(u'/Users/andyguo/Desktop/中文_1001.jpg').frame, 1001)
        self.assertEqual(DayuPath(u'/Users/andyguo/Desktop/中文 1001.jpg').frame, 1001)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/ttt/asdfasdf/pl_0010.1012.tiff').frame, 1012)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/ttt/asdfasdf/pl_0010.1012.mov').frame, -1)

    def test_pattern(self):
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_v0023.jpg').pattern, None)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_%d.jpg').pattern, '%d')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_%02d.jpg').pattern, '%02d')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_%03d.jpg').pattern, '%03d')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_%04d.jpg').pattern, '%04d')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_#.jpg').pattern, '#')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_##.jpg').pattern, '##')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_###.jpg').pattern, '###')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_####.jpg').pattern, '####')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_$F.jpg').pattern, '$F')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_$F2.jpg').pattern, '$F2')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_$F3.jpg').pattern, '$F3')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_0010_plt_$F4.jpg').pattern, '$F4')
        self.assertEqual(DayuPath(u'/Users/andyguo/Desktop/中文的测试$F4.jpg').pattern, '$F4')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/pl_%04d_ani_$F4.jpg').pattern, '%04d')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/ani_$F4.mov').pattern, '$F4')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/abc.mov').pattern, None)

    def test_to_pattern(self):
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/1.jpg').to_pattern(), '/Users/andyguo/Desktop/1.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/11.jpg').to_pattern(), '/Users/andyguo/Desktop/%02d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/11.jpg').to_pattern('#'), '/Users/andyguo/Desktop/##.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/11.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F2.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/123.jpg').to_pattern(), '/Users/andyguo/Desktop/%03d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/123.jpg').to_pattern('#'), '/Users/andyguo/Desktop/###.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/123.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F3.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/1234.jpg').to_pattern(), '/Users/andyguo/Desktop/%04d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/1234.jpg').to_pattern('#'), '/Users/andyguo/Desktop/####.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/1234.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F4.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/1234.jpg').to_pattern('ss'),
                         '/Users/andyguo/Desktop/%04d.jpg')

        self.assertEqual(DayuPath('/Users/andyguo/Desktop/%02d.jpg').to_pattern('%'), '/Users/andyguo/Desktop/%02d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/%02d.jpg').to_pattern('#'), '/Users/andyguo/Desktop/##.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/%02d.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F2.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/%03d.jpg').to_pattern('%'), '/Users/andyguo/Desktop/%03d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/%03d.jpg').to_pattern('#'), '/Users/andyguo/Desktop/###.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/%03d.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F3.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/%04d.jpg').to_pattern('%'), '/Users/andyguo/Desktop/%04d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/%04d.jpg').to_pattern('#'), '/Users/andyguo/Desktop/####.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/%04d.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F4.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/%04d.jpg').to_pattern('1'), '/Users/andyguo/Desktop/%04d.jpg')

        self.assertEqual(DayuPath('/Users/andyguo/Desktop/##.jpg').to_pattern('%'), '/Users/andyguo/Desktop/%02d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/##.jpg').to_pattern('#'), '/Users/andyguo/Desktop/##.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/##.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F2.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/###.jpg').to_pattern('%'), '/Users/andyguo/Desktop/%03d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/###.jpg').to_pattern('#'), '/Users/andyguo/Desktop/###.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/###.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F3.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/####.jpg').to_pattern('%'), '/Users/andyguo/Desktop/%04d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/####.jpg').to_pattern('#'), '/Users/andyguo/Desktop/####.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/####.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F4.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/####.jpg').to_pattern('f'), '/Users/andyguo/Desktop/%04d.jpg')

        self.assertEqual(DayuPath('/Users/andyguo/Desktop/$F2.jpg').to_pattern('%'), '/Users/andyguo/Desktop/%02d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/$F2.jpg').to_pattern('#'), '/Users/andyguo/Desktop/##.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/$F2.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F2.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/$F3.jpg').to_pattern('%'), '/Users/andyguo/Desktop/%03d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/$F3.jpg').to_pattern('#'), '/Users/andyguo/Desktop/###.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/$F3.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F3.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/$F4.jpg').to_pattern('%'), '/Users/andyguo/Desktop/%04d.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/$F4.jpg').to_pattern('#'), '/Users/andyguo/Desktop/####.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/$F4.jpg').to_pattern('$'), '/Users/andyguo/Desktop/$F4.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/$F4.jpg').to_pattern('dd'), '/Users/andyguo/Desktop/%04d.jpg')

        self.assertEqual(DayuPath('/Users/andyguo/Desktop/MVI1001.mov').to_pattern('%'),
                         '/Users/andyguo/Desktop/MVI1001.mov')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/MVI1001.mov').to_pattern('#'),
                         '/Users/andyguo/Desktop/MVI1001.mov')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/MVI1001.mov').to_pattern('$'),
                         '/Users/andyguo/Desktop/MVI1001.mov')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/MVI1001.MP4').to_pattern(),
                         '/Users/andyguo/Desktop/MVI1001.MP4')

    def test_restore_pattern(self):
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.$F.jpg').restore_pattern(12),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.12.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.$F2.jpg').restore_pattern(12),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.12.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.$F3.jpg').restore_pattern(12),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.012.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.$F4.jpg').restore_pattern(12),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.0012.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.%d.jpg').restore_pattern(1920),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.1920.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.%0d.jpg').restore_pattern(192),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.192.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.%02d.jpg').restore_pattern(1920),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.1920.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.%03d.jpg').restore_pattern(1001),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.1001.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.%04d.jpg').restore_pattern(364),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.0364.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.#.jpg').restore_pattern(364),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.364.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.##.jpg').restore_pattern(364),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.364.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.###.jpg').restore_pattern(364),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.364.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.####.jpg').restore_pattern(364),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.0364.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.%04d.jpg').restore_pattern(0),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.0000.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.1234.jpg').restore_pattern(-1),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.1234.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.1234.jpg').restore_pattern(2345),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.1234.jpg')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/sd_0010_plt_v0002.1234.jpg').restore_pattern(None),
                         '/Users/andyguo/Desktop/sd_0010_plt_v0002.1234.jpg')

    def setUp(self):
        super(TestDayuPath, self).setUp()

        from uuid import uuid4
        self.mock_path = DayuPath('~').expand_user().child(uuid4().hex)
        self.mock_path2 = DayuPath('~').expand_user().child(uuid4().hex)
        content_list = ['first_depth_0010.1001.dpx',
                        'first_depth_0010.1002.dpx',
                        'cam_test/A001C001_180212_RG8C.9876521.exr',
                        'cam_test/A001C001_180212_RG8C.9876522.exr',
                        'cam_test/A001C001_180212_RG8C.9876523.exr',
                        'vfx_test/pl_0010_plt_v0001.1001.exr',
                        'vfx_test/pl_0010_plt_v0001.1002.exr',
                        'vfx_test/pl_0010_plt_v0001.1003.exr',
                        'not_a_sequence/abc.exr',
                        'single_media_test/pl_0010_plt_v0001.1003.mov',
                        'single_media_test/MVI1022.MP4',
                        u'single_media_test/测试中文.MP4',
                        'missing_test/dd_0090_ani_1001.jpg',
                        'missing_test/dd_0090_ani_1003.jpg',
                        'missing_test/dd_0090_ani_1005.jpg',
                        'ignore_test/._DS_store',
                        'ignore_test/..sdf',
                        'recursive_test/a_001.exr',
                        'recursive_test/a_002.exr',
                        'recursive_test/inside/b_100.exr',
                        'recursive_test/inside/b_101.exr',
                        'recursive_test/inside/b_102.exr',
                        ]
        for x in content_list:
            file_path = DayuPath(u'{}/{}'.format(self.mock_path, x))
            file_path.parent.mkdir(parents=True)
            with open(file_path, 'w') as f:
                f.write('1')

        self.mock_path.child('empty_folder', 'inside').mkdir(parents=True)

    def tearDown(self):
        super(TestDayuPath, self).tearDown()
        self.mock_path.rmtree()

    def test_scan(self):
        path = self.mock_path

        result = list(path.scan())
        self.assertEqual(result[0], path.child('first_depth_0010.%04d.dpx'))
        self.assertEqual(result[0].frames, [1001, 1002])
        self.assertEqual(result[0].missing, [])

        ground_truth_result = {path.child('first_depth_0010.%04d.dpx')                      : [[1001, 1002], []],
                               path.child('cam_test', 'A001C001_180212_RG8C.%07d.exr')      : [
                                   [9876521, 9876522, 9876523], []],
                               path.child('vfx_test', 'pl_0010_plt_v0001.%04d.exr')         : [[1001, 1002, 1003], []],
                               path.child('not_a_sequence', 'abc.exr')                      : [[], []],
                               path.child('single_media_test', 'pl_0010_plt_v0001.1003.mov'): [[], []],
                               path.child('single_media_test', 'MVI1022.MP4')               : [[], []],
                               path.child(u'single_media_test', u'测试中文.MP4')                : [[], []],
                               path.child('missing_test', 'dd_0090_ani_%04d.jpg')           : [[1001, 1003, 1005],
                                                                                               [1002, 1004]],
                               path.child('recursive_test', 'a_%03d.exr')                   : [[1, 2], []],
                               path.child('recursive_test', 'inside', 'b_%03d.exr')         : [[100, 101, 102], []],
                               }
        ground_truth_result.update({
            self.mock_path2.child('recursive_test', 'inside', 'b_%03d.exr'): [[100, 101, 102], []]
        })

        print ground_truth_result.keys()
        for x in path.scan(recursive=True):
            if x:
                print x
                self.assertTrue(x in ground_truth_result.keys())
                self.assertListEqual([x.frames, x.missing], ground_truth_result[x])

        for x in self.mock_path2.scan(recursive=True):
            self.assertTrue(x in ground_truth_result.keys())
            self.assertListEqual([x.frames, x.missing], ground_truth_result[x])

        for x in path.child('vfx_test', 'pl_0010_plt_v0001.1001.exr').scan():
            self.assertEqual(x, path.child('vfx_test', 'pl_0010_plt_v0001.%04d.exr'))
            self.assertEqual(x.frames, [1001, 1002, 1003])
            self.assertEqual(x.missing, [])

        for x in path.child('missing_test').scan():
            if x:
                self.assertEqual(x, path.child('missing_test', 'dd_0090_ani_%04d.jpg'))
                self.assertListEqual([x.frames, x.missing], ground_truth_result[x])

        for x in path.child(u'single_media_test', u'测试中文.MP4').scan():
            self.assertEqual(x, path.child(u'single_media_test', u'测试中文.MP4'))
            self.assertEqual(x.frames, [])
            self.assertEqual(x.missing, [])

        for x in path.child('not_a_sequence', 'abc.exr').scan():
            self.assertEqual(x, path.child('not_a_sequence', 'abc.exr'))
            self.assertEqual(x.frames, [])
            self.assertEqual(x.missing, [])

        self.assertFalse(list(path.child('vfx_test', 'pl_0010_plt_v0002.1001.exr').scan()))
        self.assertFalse(list(path.child('vfx_test', 'pl_0010_plt_v0002.1001.exr').scan(recursive=True)))
        self.assertFalse(list(path.child('empty_folder').scan(recursive=True)))

        self.assertNotIn(path.child('ignore_test', '._DS_store'), [x for x in path.scan(recursive=True)])
        self.assertNotIn(path.child('ignore_test', '..sdf'), [x for x in path.scan(recursive=True)])
        self.assertNotIn(path.child('ignore_test', 'Thumbnail'), [x for x in path.scan(recursive=True)])
        self.assertNotIn(path.child('ignore_test', 'temp.tmp'), [x for x in path.scan(recursive=True)])

    def test_escape(self):
        legal_path = DayuPath('/Users/andyguo/Desktop/111.mov')
        self.assertEqual(legal_path.escape(), '/Users/andyguo/Desktop/111.mov')
        whitespace_path = DayuPath('/Users/andyguo/Desktop/some words with space.mov')
        self.assertEqual(whitespace_path.escape(), '/Users/andyguo/Desktop/some\ words\ with\ space.mov')
        bash_string = DayuPath('The$!cat#&ran\"\'up()a|<>tree`;')
        self.assertEqual(bash_string.escape(), r'The\$\!cat\#\&ran\"\'up\(\)a\|\<\>tree\`\;')
        unicode_string = DayuPath(u'/Users/andyguo/Desktop/中文 和 空格12234 rer.jpg')
        self.assertEqual(unicode_string.escape(), u'/Users/andyguo/Desktop/中文\ 和\ 空格12234\ rer.jpg')

    def test_version(self):
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/v001/111.mov').version, 'v001')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/V001/111.mov').version, 'V001')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/v001/A001C001_180212_DF3X.mov').version, 'v001')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/v003/pl_0010_plt_bga_v0002.1001.mov').version, 'v0002')
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/dd/pl_0010_plt_bga.1001.mov').version, None)
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/vv/pl_0010_plt_bga.1001.mov').version, None)
        self.assertEqual(DayuPath('not a path').version, None)

    @unittest.skip('only for mac local test')
    def test_root(self):
        self.assertEqual(DayuPath('/Users/andyguo/Desktop/abc.jpg').root, '/')
        self.assertEqual(DayuPath('/Volumes/filedata/td/finder.lnk').root, '/Volumes/filedata')
        self.assertIsInstance(DayuPath('/Volumes/filedata/td/finder.lnk').root, DayuPath)

    @unittest.skip('only for mac local test')
    def test_is_network(self):
        self.assertTrue(DayuPath('/Volumes/filedata/td/finder.lnk').is_network)
        self.assertFalse(DayuPath('/Users/andyguo/Desktop/log.txt').is_network)

    @unittest.skip('only for mac local test')
    def test_is_local(self):
        self.assertFalse(DayuPath('/Volumes/filedata/td/finder.lnk').is_local)
        self.assertTrue(DayuPath('/Users/andyguo/Desktop/log.txt').is_local)
