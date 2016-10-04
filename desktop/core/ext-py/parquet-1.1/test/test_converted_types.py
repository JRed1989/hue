# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import array
import datetime
import struct
import io
import unittest
from decimal import Decimal

from parquet.converted_types import convert_column
from parquet import parquet_thrift as pt
from bson import Binary

class TestDecimal(unittest.TestCase):

	def test_int32(self):
		schema = pt.SchemaElement(
			type=pt.Type.INT32,
			name="test",
			converted_type=pt.ConvertedType.DECIMAL,
			scale=10,
			precision=9
		)

		self.assertEquals(
			convert_column([9876543210], schema)[0],
			Decimal('9.87654321')
		)

	def test_int64(self):
		schema = pt.SchemaElement(
			type=pt.Type.INT64,
			name="test",
			converted_type=pt.ConvertedType.DECIMAL,
			scale=3,
			precision=13
		)

		self.assertEquals(
			convert_column([1099511627776], schema)[0],
			Decimal('10995116277.76')
		)

	def test_fixedlength(self):
		schema = pt.SchemaElement(
			type=pt.Type.FIXED_LEN_BYTE_ARRAY,
			type_length=3,
			name="test",
			converted_type=pt.ConvertedType.DECIMAL,
			scale=3,
			precision=13
		)

		self.assertEquals(
			convert_column([b'\x02\x00\x01'], schema)[0],
			Decimal('1310.73')
		)

	def test_binary(self):
		schema = pt.SchemaElement(
			type=pt.Type.BYTE_ARRAY,
			name="test",
			converted_type=pt.ConvertedType.DECIMAL,
			scale=3,
			precision=13
		)

		self.assertEquals(
			convert_column([b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x01'], schema)[0],
			Decimal('94447329657392904273.93')
		)


class TestDateTypes(unittest.TestCase):

	def test_date(self):
		schema = pt.SchemaElement(
			type=pt.Type.INT32,
			name="test",
			converted_type=pt.ConvertedType.DATE,
		)
		self.assertEquals(
			convert_column([731888], schema)[0],
			datetime.date(2004, 11, 3)
		)

	def test_time_millis(self):
		schema = pt.SchemaElement(
			type=pt.Type.INT32,
			name="test",
			converted_type=pt.ConvertedType.TIME_MILLIS,
		)
		self.assertEquals(
			convert_column([731888], schema)[0],
			datetime.timedelta(milliseconds=731888)
		)

	def test_timestamp_millis(self):
		schema = pt.SchemaElement(
			type=pt.Type.INT64,
			name="test",
			converted_type=pt.ConvertedType.TIMESTAMP_MILLIS,
		)
		self.assertEquals(
			convert_column([1099511625014], schema)[0],
			datetime.datetime(2004, 11, 3, 19, 53, 45, 14*1000)
		)

	def test_utf8(self):
		schema = pt.SchemaElement(
			type = pt.Type.BYTE_ARRAY,
			name="test",
			converted_type=pt.ConvertedType.UTF8
		)
		data = b'foo\xf0\x9f\x91\xbe'
		self.assertEquals(
			convert_column([data], schema)[0],
			'foo👾'
		)

	def test_uint8(self):
		schema = pt.SchemaElement(
			type = pt.Type.INT32,
			name="test",
			converted_type=pt.ConvertedType.UINT_8
		)
		self.assertEquals(
			convert_column([-3], schema)[0],
			253
		)

	def test_uint16(self):
		schema = pt.SchemaElement(
			type = pt.Type.INT32,
			name="test",
			converted_type=pt.ConvertedType.UINT_16
		)
		self.assertEquals(
			convert_column([-3], schema)[0],
			65533
		)

	def test_uint32(self):
		schema = pt.SchemaElement(
			type = pt.Type.INT32,
			name="test",
			converted_type=pt.ConvertedType.UINT_32
		)
		self.assertEquals(
			convert_column([-6884376], schema)[0],
			4288082920
		)

	def test_uint64(self):
		schema = pt.SchemaElement(
			type = pt.Type.INT64,
			name="test",
			converted_type=pt.ConvertedType.UINT_64
		)
		self.assertEquals(
			convert_column([-6884376], schema)[0],
			18446744073702667240
		)

	def test_json(self):
		schema = pt.SchemaElement(
			type = pt.Type.BYTE_ARRAY,
			name="test",
			converted_type=pt.ConvertedType.JSON
		)
		self.assertEquals(
			convert_column([b'{"foo": ["bar", "\\ud83d\\udc7e"]}'], schema)[0],
			{'foo': ['bar','👾']}
		)

	def test_bson(self):
		schema = pt.SchemaElement(
			type = pt.Type.BYTE_ARRAY,
			name="test",
			converted_type=pt.ConvertedType.BSON
		)
		self.assertEquals(
			convert_column([b'&\x00\x00\x00\x04foo\x00\x1c\x00\x00\x00\x020\x00\x04\x00\x00\x00bar\x00\x021\x00\x05\x00\x00\x00\xf0\x9f\x91\xbe\x00\x00\x00'], schema)[0],
			{'foo': ['bar','👾']}
		)
