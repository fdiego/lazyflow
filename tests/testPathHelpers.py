###############################################################################
#   lazyflow: data flow based lazy parallel computation framework
#
#       Copyright (C) 2011-2014, the ilastik developers
#                                <team@ilastik.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the Lesser GNU General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# See the files LICENSE.lgpl2 and LICENSE.lgpl3 for full text of the
# GNU Lesser General Public License version 2.1 and 3 respectively.
# This information is also available on the ilastik web site at:
#                 http://ilastik.org/license/
###############################################################################
import os
from lazyflow.utility.pathHelpers import compressPathForDisplay, getPathVariants, PathComponents

class TestPathHelpers(object):

    def testPathComponents(self):
        components = PathComponents('/some/external/path/to/file.h5/with/internal/path/to/data')
        assert components.externalPath == '/some/external/path/to/file.h5'
        assert components.extension == '.h5'
        assert components.internalPath == '/with/internal/path/to/data'

        components = PathComponents('/some/external/path/to/file.h5_crazy_ext.h5/with/internal/path/to/data')
        assert components.externalPath == '/some/external/path/to/file.h5_crazy_ext.h5'
        assert components.extension == '.h5'
        assert components.internalPath == '/with/internal/path/to/data'

        # Everything should work for URLs, too.
        components = PathComponents('http://somehost:8000/path/to/data/with.ext')
        assert components.externalPath == 'http://somehost:8000/path/to/data/with.ext'
        assert components.extension == '.ext'
        assert components.internalPath is None
        assert components.externalDirectory == 'http://somehost:8000/path/to/data'
        assert components.filenameBase == 'with'

        # Try modifying the properties and verify that the total path is updated.
        components = PathComponents('/some/external/path/to/file.h5/with/internal/path/to/data')
        components.extension = '.hdf5'
        assert components.externalPath == '/some/external/path/to/file.hdf5'
        assert components.totalPath() == '/some/external/path/to/file.hdf5/with/internal/path/to/data'
        components.filenameBase = 'newbase'
        assert components.totalPath() == '/some/external/path/to/newbase.hdf5/with/internal/path/to/data'
        components.internalDirectory = 'new/internal/dir'
        assert components.totalPath() == '/some/external/path/to/newbase.hdf5/new/internal/dir/data'
        components.internalDatasetName = 'newdata'
        assert components.totalPath() == '/some/external/path/to/newbase.hdf5/new/internal/dir/newdata'
        components.externalDirectory = '/new/extern/dir/'
        assert components.totalPath() == '/new/extern/dir/newbase.hdf5/new/internal/dir/newdata'
        components.externalDirectory = '/new/extern/dir'
        assert components.totalPath() == '/new/extern/dir/newbase.hdf5/new/internal/dir/newdata'
        components.externalPath = '/new/externalpath/somefile.h5'
        assert components.totalPath() == '/new/externalpath/somefile.h5/new/internal/dir/newdata'
        components.filename = 'newfilename.h5'
        assert components.totalPath() == '/new/externalpath/newfilename.h5/new/internal/dir/newdata'
        components.internalPath = '/new/internal/path/dataset'
        assert components.totalPath() == '/new/externalpath/newfilename.h5/new/internal/path/dataset'

    def testCompressPathForDisplay(self):
        assert compressPathForDisplay("/a/b.txt", 30) == "/a/b.txt"
        path = "/test/bla/bla/this_is_a_very_long_filename_bla_bla.txt"
        for l in [5,10,15,20,30]:
            assert len(compressPathForDisplay(path, l)) == l

    def test_getPathVariants(self):
        abs, rel = getPathVariants('/aaa/bbb/ccc/ddd.txt', '/aaa/bbb/ccc/eee')
        #assert abs == '/aaa/bbb/ccc/ddd.txt'
        # Use normpath to make sure this test works on windows...
        assert abs == os.path.normpath(os.path.join('/aaa/bbb/ccc/eee', '/aaa/bbb/ccc/ddd.txt'))
        assert rel == '../ddd.txt'

        abs, rel = getPathVariants('../ddd.txt', '/aaa/bbb/ccc/eee')
        #assert abs == '/aaa/bbb/ccc/ddd.txt'
        # Use normpath to make sure this test works on windows...
        assert abs == os.path.normpath(os.path.join('/aaa/bbb/ccc/eee', '../ddd.txt'))
        assert rel == '../ddd.txt'

        abs, rel = getPathVariants('ddd.txt', '/aaa/bbb/ccc')
        #assert abs == '/aaa/bbb/ccc/ddd.txt'
        # Use normpath to make sure this test works on windows...
        assert abs == os.path.normpath(os.path.join('/aaa/bbb/ccc', 'ddd.txt'))
        assert rel == 'ddd.txt'

        assert getPathVariants('', '/abc') == ('/abc', '')

if __name__ == "__main__":
    import sys
    import nose
    sys.argv.append("--nocapture")    # Don't steal stdout.  Show it on the console as usual.
    sys.argv.append("--nologcapture") # Don't set the logging level to DEBUG.  Leave it alone.
    nose.run(defaultTest=__file__)
