import copy
import unittest

from google.protobuf import text_format

from proto_matcher.compare import compare
from proto_matcher.testdata import test_pb2

_TEST_PROTO = """
bars {
    short_id: -123
    name: "a bar"
    size: 1
    notes: "hehe"
    notes: "123"
}
bars {
    long_id: 888899990000
    progress: 0.31415926
    checked: True
    notes: "photo"
}
baz {
    status: ERROR
}
mapping {
    key: 5
    value: "haha"
}
mapping {
    key: 10
    value: "hello world!"
}
"""


class ProtoCompareTest(unittest.TestCase):

    def assertProtoCompareToBe(self, result: compare.ProtoComparisonResult,
                               to_be: bool):
        self.assertEqual(result.is_equal, to_be, result.explanation)\

    def test_proto_comparable(self):
        self.assertTrue(compare.proto_comparable(test_pb2.Foo(),
                                                 test_pb2.Foo()))
        self.assertFalse(
            compare.proto_comparable(test_pb2.Foo(), test_pb2.Bar()))
        self.assertFalse(
            compare.proto_comparable(test_pb2.Baz(), test_pb2.Bar()))

        foo1 = test_pb2.Foo()
        foo1.baz.status = test_pb2.Baz.OK
        foo2 = test_pb2.Foo()
        bar = test_pb2.Bar()
        bar.progress = 0.75
        foo2.bars.append(bar)
        self.assertTrue(compare.proto_comparable(foo1, foo1))
        self.assertTrue(compare.proto_comparable(foo1, foo2))
        self.assertFalse(compare.proto_comparable(foo1, bar))

    def test_basic_equality(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    True)

    def test_basic_inequality(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        expected.baz.Clear()
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

    def test_repeated_field_inequality(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        expected.bars.add().progress = 0.1
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

    def test_map_field_inequality(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        expected.mapping[15] = 'luck'
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

    def test_basic_partial_equality(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        opts = compare.ProtoComparisonOptions(
            scope=compare.ProtoComparisonScope.PARTIAL)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

    def test_partial_equality_test_extra_field(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        expected.baz.Clear()

        opts = compare.ProtoComparisonOptions(
            scope=compare.ProtoComparisonScope.PARTIAL)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

    def test_basic_partial_inequality(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        expected.baz.status = test_pb2.Baz.OK

        opts = compare.ProtoComparisonOptions(
            scope=compare.ProtoComparisonScope.PARTIAL)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), False)

    def test_partial_inequality_missing_field(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual.baz.Clear()

        opts = compare.ProtoComparisonOptions(
            scope=compare.ProtoComparisonScope.PARTIAL)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), False)

    def test_repeated_field_partial_inequality(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        expected.bars.add().progress = 0.1

        opts = compare.ProtoComparisonOptions(
            scope=compare.ProtoComparisonScope.PARTIAL)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), False)

    def test_aproximate_equality(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    True)

    def test_aproximate_modified_equality(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        expected.bars[0].progress = 2.300005
        actual.bars[0].progress = 2.300006
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

        opts = compare.ProtoComparisonOptions(
            float_comp=compare.ProtoFloatComparison.APPROXIMATE)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

    def test_aproximate_modified_equality_double(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        expected.bars[0].precision = 2.3 + 1.1e-15
        actual.bars[0].precision = 2.3 + 1.2e-15
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

        opts = compare.ProtoComparisonOptions(
            float_comp=compare.ProtoFloatComparison.APPROXIMATE)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

    def test_within_fraction_or_margin_float(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        expected.bars[0].progress = 100.0
        actual.bars[0].progress = 109.9
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

        # fraction and margin do not matter when |float_comp| is EXACT.
        opts = compare.ProtoComparisonOptions(float_fraction=0.0,
                                              float_margin=10.0)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), False)

        opts = compare.ProtoComparisonOptions(
            float_fraction=0.0,
            float_margin=10.0,
            float_comp=compare.ProtoFloatComparison.APPROXIMATE)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

        opts = compare.ProtoComparisonOptions(
            float_fraction=0.2,
            float_margin=0.0,
            float_comp=compare.ProtoFloatComparison.APPROXIMATE)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

        opts = compare.ProtoComparisonOptions(
            float_fraction=0.01,
            float_margin=0.0,
            float_comp=compare.ProtoFloatComparison.APPROXIMATE)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), False)

        opts = compare.ProtoComparisonOptions(
            float_fraction=0.10,
            float_margin=10.0,
            float_comp=compare.ProtoFloatComparison.APPROXIMATE)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

    def test_oneof_inequality(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        expected.bars[0].long_id = expected.bars[0].short_id
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

    def test_compare_proto_ignoring_fields(self):
        # a: 1,      2,    3, 9, 4, 5, 7,   2
        # b:   9, 0, 2, 7, 3,    4, 5,   6, 2
        pass

    def test_ignore_field_single(self):
        expected = text_format.Parse('baz { status: ERROR }', test_pb2.Foo())
        actual = text_format.Parse('', test_pb2.Foo())
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

        opts = compare.ProtoComparisonOptions(ignore_field_paths={('baz',)})
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

    def test_ignore_field_repeated(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        del actual.bars[:]
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

        opts = compare.ProtoComparisonOptions(ignore_field_paths={('bars',)})
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

    def test_ignore_field_multiple(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        del actual.bars[:]
        actual.baz.status = test_pb2.Baz.OK

        opts = compare.ProtoComparisonOptions(ignore_field_paths={('bars',)})
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), False)
        opts = compare.ProtoComparisonOptions(ignore_field_paths={('baz',)})
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), False)

        opts = compare.ProtoComparisonOptions(
            ignore_field_paths={('bars',), ('baz',)})
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

    def test_ignore_field_nested(self):
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual.bars[0].size = 2
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

        opts = compare.ProtoComparisonOptions(ignore_field_paths={('bars',
                                                                   'size')})
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

    def test_compare_proto_repeated_fields_ignoring_order(self):
        # Create expected and actual protos with the same content but reverse the `bars` field in the actual proto.
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        reversed_bars = actual.bars[::-1]
        del actual.bars[:]
        actual.bars.extend(reversed_bars)

        # Compare without ignoring repeated fields order - expect comparison to fail.
        self.assertProtoCompareToBe(compare.proto_compare(actual, expected),
                                    False)

        # Compare with ignoring repeated fields order - expect comparison to pass.
        opts = compare.ProtoComparisonOptions(
            repeated_field_comp=compare.RepeatedFieldComparison.AS_SET)
        self.assertProtoCompareToBe(
            compare.proto_compare(actual, expected, opts=opts), True)

    def test_compare_proto_repeated_fields_ignoring_order_does_not_modify_objects(self):
        # Create expected and actual protos with the same content but reverse
        # the `bars` field in the actual proto.
        expected = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        actual = text_format.Parse(_TEST_PROTO, test_pb2.Foo())
        reversed_bars = actual.bars[::-1]
        del actual.bars[:]
        actual.bars.extend(reversed_bars)

        # Copy the expected and actual protos to ensure that the original
        # objects are not modified.
        expected_copy = copy.deepcopy(expected)
        actual_copy = copy.deepcopy(actual)

        # Compare with ignoring repeated fields order (we don't really care
        # about the comparison result in this test).
        opts = compare.ProtoComparisonOptions(
            repeated_field_comp=compare.RepeatedFieldComparison.AS_SET)
        compare.proto_compare(actual, expected, opts=opts)
        self.assertEqual(expected, expected_copy)
        self.assertEqual(actual, actual_copy)


if __name__ == '__main__':
    unittest.main()
