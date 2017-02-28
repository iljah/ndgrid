#! /usr/bin/env python3
'''
Tests cell class of NdGrid.

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


class test_cell(unittest.TestCase):

	def test_init(self):
		c = cell.cell()
		self.assertEqual(len(c.volume.keys()), 0)

	def test_get_extent(self):
		c = cell.cell()
		self.assertRaises(ValueError, c.get_extent, 'asdf')
		c.set_extent(1, 2, 3)
		self.assertEqual(c.get_extent(1), (2, 3))

	def test_set_extent(self):
		c = cell.cell()
		c.set_extent('asdf', 1, 3)
		self.assertEqual(c.get_extent('asdf'), (1, 3))
		self.assertRaises(ValueError, c.set_extent, 1, 3, 2)

	def test_split(self):
		c = cell.cell()
		c.set_extent(1, 2, 3)
		c.set_extent('asdf', -2, -1)
		first, second = c.split(1)
		self.assertEqual(first.get_extent('asdf'), (-2, -1))
		self.assertEqual(second.get_extent('asdf'), (-2, -1))
		self.assertEqual(first.get_extent(1), (2, (2+3)/2))
		self.assertEqual(second.get_extent(1), ((2+3)/2, 3))


if __name__ == '__main__':
	unittest.main()
