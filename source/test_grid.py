#! /usr/bin/env python3
'''
Tests N-dimensional grid library.

Copyright 2017 Ilja Honkonen

NdGrid is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License
version 3 as published by the Free Software Foundation.

NdGrid is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with Foobar. If not, see
<http://www.gnu.org/licenses/>.
'''


import unittest
import cell
import ndgrid


class test_ndgrid(unittest.TestCase):

	def test_init(self):
		c = cell.cell()
		g = ndgrid.ndgrid(c)
		self.assertIn(c, g.graph)
		self.assertEqual(len(g.get_cells()), 1)


	def test_split1(self):
		dim = 0

		c = cell.cell()
		g = ndgrid.ndgrid(c)
		self.assertRaises(ValueError, g.split, cell.cell(), dim)

		for c in g.get_cells():
			g.split(c, dim)
		cells = g.get_cells()
		self.assertEqual(len(cells), 2)

		for c in cells:
			self.assertIn(dim, c.volume)

		for c in cells:
			ext = c.get_extent(dim)
			self.assertTrue(ext[0] == 0.0 or ext[1] == 0.0)
			self.assertTrue(ext[0] == -1.0 or ext[1] == +1.0)


	'''
	|    | -> |||||
	'''
	def test_split2(self):
		dim = 123
		g = ndgrid.ndgrid(cell.cell())
		for c in g.get_cells():
			g.split(c, dim)
		self.assertEqual(len(g.get_cells()), 2)
		for c in g.get_cells():
			g.split(c, dim)
		cells = g.get_cells()
		self.assertEqual(len(cells), 4)

		for c in cells:
			self.assertIn(dim, c.volume)
			self.assertNotIn(0, c.volume)
			self.assertTrue(len(g.get_neighbors(c)) <= 2)
			self.assertTrue(c.get_extent(dim)[0] < +1)
			self.assertTrue(c.get_extent(dim)[1] > -1)


	'''
	---    ---
	| |    ||| dim1
	| | -> ---  ^
	| |    |||  |
	---    ---  |--> dim2
	'''
	def test_split3(self):
		dim1 = 2
		dim2 = -2
		c = cell.cell()
		c.set_extent(dim1, -3, 3)
		c.set_extent(dim2, 10, 20)
		g = ndgrid.ndgrid(c)
		g.split(c, dim1)
		for c in g.get_cells():
			g.split(c, dim2)
		cells = g.get_cells()
		self.assertEqual(len(cells), 4)
		for c in cells:
			self.assertTrue(len(g.get_neighbors(c)) <= 2)
			ext1 = c.get_extent(dim1)
			self.assertTrue(ext1[0] == -3 or ext1[0] == 0)
			self.assertTrue(ext1[1] == 0 or ext1[1] == +3)
			ext2 = c.get_extent(dim2)
			self.assertTrue(ext2[0] == 10 or ext2[0] == 15)
			self.assertTrue(ext2[1] == 15 or ext2[1] == 20)


	def test_remove(self):
		c = cell.cell()
		c.set_extent(0, -1, 1)
		c.set_extent(3, -1, 1)
		g = ndgrid.ndgrid(c)
		g.split(c, 0)
		for c in g.get_cells():
			g.split(c, 3)
		g.remove(g.get_cells()[0])
		self.assertEqual(len(g.get_cells()), 3)
		self.assertEqual(len(g.get_neighbors(g.get_cells()[0])), 2)


if __name__ == '__main__':
	unittest.main()
