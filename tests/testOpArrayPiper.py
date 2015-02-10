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
#		   http://ilastik.org/license/
###############################################################################

__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$Feb 06, 2015 12:28:04 EST$"



import numpy

import vigra

from lazyflow.graph import Graph
from lazyflow.operators.opArrayPiper import OpArrayPiper


class TestOpArrayPiper(object):
    def setUp(self):
        self.graph = Graph()

        self.operator_identity = OpArrayPiper(graph=self.graph)

        self.operator_identity.Input.meta.axistags = vigra.AxisTags("txyzc")

    def test1(self):
        # Generate a random dataset and see if it we get the right masking from the operator.
        data = numpy.random.random((4, 5, 6, 7, 3)).astype(numpy.float32)
        expected_output = data.copy()

        # Provide input read all output.
        self.operator_identity.Input.setValue(data)
        output = self.operator_identity.Output[None].wait()

        assert((expected_output == output).all())

    def test2(self):
        # Generate a dataset and grab chunks of it from the operator. The result should be the same as above.
        data = numpy.random.random((4, 5, 6, 7, 3)).astype(numpy.float32)
        expected_output = data.copy()

        # Create array to store results. Don't keep original data.
        output = expected_output.copy()
        output[:] = 0

        # Provide input and grab chunks.
        self.operator_identity.Input.setValue(data)
        output[:2] = self.operator_identity.Output[:2].wait()
        output[2:] = self.operator_identity.Output[2:].wait()

        assert((expected_output == output).all())

    def tearDown(self):
        # Take down operators
        self.operator_identity.Input.disconnect()
        self.operator_identity.Output.disconnect()
        self.operator_identity.cleanUp()


class TestOpArrayPiper2(object):
    def setUp(self):
        self.graph = Graph()

        self.operator_identity = OpArrayPiper(graph=self.graph)

        self.operator_identity.Input.meta.axistags = vigra.AxisTags("txyzc")
        self.operator_identity.Input.meta.has_mask = True

    def test1(self):
        # Generate a random dataset and see if it we get the right masking from the operator.
        data = numpy.random.random((4, 5, 6, 7, 3)).astype(numpy.float32)
        expected_output = numpy.ma.masked_array(data,
                                                mask=numpy.zeros(data.shape, dtype=bool),
                                                shrink=False
                          )

        # Provide input read all output.
        self.operator_identity.Input.setValue(data)
        output = self.operator_identity.Output[None].wait()

        assert((expected_output == output).all())
        assert(expected_output.mask.shape == output.mask.shape)
        assert((expected_output.mask == output.mask).all())

    def test2(self):
        # Generate a dataset and grab chunks of it from the operator. The result should be the same as above.
        data = numpy.random.random((4, 5, 6, 7, 3)).astype(numpy.float32)
        expected_output = numpy.ma.masked_array(data,
                                                mask=numpy.zeros(data.shape, dtype=bool),
                                                shrink=False
                          )

        # Create array to store results. Don't keep original data.
        output = expected_output.copy()
        output[:] = 0
        output[:] = numpy.ma.nomask

        # Provide input and grab chunks.
        self.operator_identity.Input.setValue(data)
        output[:2] = self.operator_identity.Output[:2].wait()
        output[2:] = self.operator_identity.Output[2:].wait()

        assert((expected_output == output).all())
        assert(expected_output.mask.shape == output.mask.shape)
        assert((expected_output.mask == output.mask).all())

    def tearDown(self):
        # Take down operators
        self.operator_identity.Input.disconnect()
        self.operator_identity.Output.disconnect()
        self.operator_identity.cleanUp()


class TestOpArrayPiper3(object):
    def setUp(self):
        self.graph = Graph()

        self.operator_identity = OpArrayPiper(graph=self.graph)

        self.operator_identity.Input.meta.axistags = vigra.AxisTags("txyzc")
        self.operator_identity.Input.meta.has_mask = True

    def test1(self):
        # Generate a random dataset and see if it we get the right masking from the operator.
        data = numpy.random.random((4, 5, 6, 7, 3)).astype(numpy.float32)
        expected_output = numpy.ma.masked_array(data,
                                                mask=numpy.zeros(data.shape, dtype=bool),
                                                shrink=False
                          )

        # Provide input read all output.
        self.operator_identity.Input.setValue(data)
        assert(self.operator_identity.Input.meta.has_mask)
        assert(self.operator_identity.Output.meta.has_mask)
        output = self.operator_identity.Output[None].wait()

        assert((expected_output == output).all())
        assert(expected_output.mask.shape == output.mask.shape)
        assert((expected_output.mask == output.mask).all())

    def test2(self):
        # Generate a dataset and grab chunks of it from the operator. The result should be the same as above.
        data = numpy.random.random((4, 5, 6, 7, 3)).astype(numpy.float32)
        expected_output = numpy.ma.masked_array(data,
                                                mask=numpy.zeros(data.shape, dtype=bool),
                                                shrink=False
                          )

        # Create array to store results. Don't keep original data.
        output = expected_output.copy()
        output[:] = 0
        output[:] = numpy.ma.nomask

        # Provide input and grab chunks.
        self.operator_identity.Input.setValue(data)
        assert(self.operator_identity.Input.meta.has_mask)
        assert(self.operator_identity.Output.meta.has_mask)
        output[:2] = self.operator_identity.Output[:2].wait()
        output[2:] = self.operator_identity.Output[2:].wait()

        assert((expected_output == output).all())
        assert(expected_output.mask.shape == output.mask.shape)
        assert((expected_output.mask == output.mask).all())

    def tearDown(self):
        # Take down operators
        self.operator_identity.Input.disconnect()
        self.operator_identity.Output.disconnect()
        self.operator_identity.cleanUp()