# -*- coding: utf-8 -*-

import os
from cromlech.webob import Response
from mimetypes import guess_type

CHUNK_SIZE = 1 << 12


class FileIterable(object):

    def __init__(self, iterator):
        self.iterator = iterator

    def __iter__(self):
        return iter(self.iterator)

    @classmethod
    def make_response(cls, file, filename, content_type, content_length):
        fileobj = cls(file)
        res = Response(content_type=content_type)
        res.content_disposition = 'attachment; filename="%s"' % filename
        res.app_iter = fileobj
        res.content_length = content_length
        return res


class FileIterator(object):
    chunk_size = CHUNK_SIZE

    def __init__(self, f):
        self.fp = f

    def __iter__(self):
        return self

    def next(self):
        chunk = self.fp.read(self.chunk_size)
        if not chunk:
            self.fp.close()
            raise StopIteration
        return chunk


class Folder(Location):

    def __init__(self, path):
        assert os.path.isdir(path)
        self.root_path = path

    def get_file(self, name):
        path = os.path.join(self.root_path, name)
        assert os.path.isfile(path)
        iterator = FileIterator(open(path, 'rb'))
        size = os.path.getsize(path)
        return name, iterator, size

    def keys(self):
        return os.listdir(self.root_path)
    
    def __getitem__(self, name):
        filename, data, size = self.get_file(name)
        type, encoding = guess_type(filename)
        return FileIterable.make_response(data, name, type, size)
