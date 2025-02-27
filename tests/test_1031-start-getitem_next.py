# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

from awkward._v2.tmp_for_testing import v1_to_v2


def test_EmptyArray():
    a = ak._v2.contents.emptyarray.EmptyArray()
    assert len(a) == 0
    with pytest.raises(IndexError):
        a[
            0,
        ]
    assert isinstance(
        a[
            10:20,
        ],
        ak._v2.contents.emptyarray.EmptyArray,
    )
    assert (
        len(
            a[
                10:20,
            ]
        )
        == 0
    )
    with pytest.raises(IndexError):
        a[
            "bad",
        ]
    with pytest.raises(IndexError):
        a[
            ["bad", "good", "ok"],
        ]


def test_NumpyArray_toRegularArray():
    a = v1_to_v2(ak.from_numpy(np.arange(2 * 3 * 5).reshape(2, 3, 5)).layout)
    b = a.toRegularArray()
    assert isinstance(b, ak._v2.contents.RegularArray)
    assert len(b) == len(a) == 2
    assert b.size == 3
    assert isinstance(b.content, ak._v2.contents.RegularArray)
    assert len(b.content) == 6
    assert b.content.size == 5
    assert isinstance(b.content.content, ak._v2.contents.NumpyArray)
    assert len(b.content.content) == 30

    a = v1_to_v2(ak.from_numpy(np.arange(2 * 0 * 5).reshape(2, 0, 5)).layout)
    b = a.toRegularArray()
    assert isinstance(b, ak._v2.contents.RegularArray)
    assert len(b) == len(a) == 2
    assert b.size == 0
    assert isinstance(b.content, ak._v2.contents.RegularArray)
    assert len(b.content) == 0
    assert b.content.size == 5
    assert isinstance(b.content.content, ak._v2.contents.NumpyArray)
    assert len(b.content.content) == 0


def test_NumpyArray():
    a = ak._v2.contents.numpyarray.NumpyArray(
        np.array([0.0, 1.1, 2.2, 3.3], dtype=np.float64)
    )
    assert len(a) == 4
    assert (
        a[
            2,
        ]
        == 2.2
    )
    assert (
        a[
            -2,
        ]
        == 2.2
    )
    assert (
        type(
            a[
                2,
            ]
        )
        is np.float64
    )
    with pytest.raises(IndexError):
        a[
            4,
        ]
    with pytest.raises(IndexError):
        a[
            -5,
        ]
    assert isinstance(
        a[
            2:,
        ],
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert (
        a[2:,][  # noqa: E231
            0,
        ]
        == 2.2
    )
    assert (
        len(
            a[
                2:,
            ]
        )
        == 2
    )
    with pytest.raises(IndexError):
        a[
            "bad",
        ]
    with pytest.raises(IndexError):
        a[
            ["bad", "good", "ok"],
        ]

    b = ak._v2.contents.numpyarray.NumpyArray(
        np.arange(2 * 3 * 5, dtype=np.int64).reshape(2, 3, 5)
    )
    assert len(b) == 2
    assert isinstance(
        b[
            1,
        ],
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert (
        len(
            b[
                1,
            ]
        )
        == 3
    )
    with pytest.raises(IndexError):
        b[
            2,
        ]
    assert (
        b[1,][2,][  # noqa: E231
            0,
        ]
        == 25
    )
    assert (
        len(
            b[1,][2,][  # noqa: E231
                1:,
            ]
        )
        == 4
    )
    assert (
        b[1,][2,][1:,][  # noqa: E231
            2,
        ]
        == 28
    )
    with pytest.raises(IndexError):
        b[
            "bad",
        ]
    with pytest.raises(IndexError):
        b[
            ["bad", "good", "ok"],
        ]


def test_RegularArray_NumpyArray():
    # 6.6 is inaccessible
    a = ak._v2.contents.regulararray.RegularArray(
        ak._v2.contents.numpyarray.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
        ),
        3,
    )
    assert len(a) == 2
    assert isinstance(
        a[
            1,
        ],
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert (
        len(
            a[
                1,
            ]
        )
        == 3
    )
    assert (
        a[1,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    assert (
        a[-1,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    assert isinstance(
        a[
            1:2,
        ],
        ak._v2.contents.regulararray.RegularArray,
    )
    assert (
        len(
            a[
                1:,
            ]
        )
        == 1
    )
    assert (
        len(
            a[
                1:100,
            ]
        )
        == 1
    )
    with pytest.raises(IndexError):
        a[
            2,
        ]
    with pytest.raises(IndexError):
        a[
            -3,
        ]
    with pytest.raises(IndexError):
        a[1,][  # noqa: E231
            3,
        ]
    with pytest.raises(IndexError):
        a[
            "bad",
        ]
    with pytest.raises(IndexError):
        a[
            ["bad", "good", "ok"],
        ]

    b = ak._v2.contents.regulararray.RegularArray(
        ak._v2.contents.emptyarray.EmptyArray(), 0, zeros_length=10
    )
    assert len(b) == 10
    assert isinstance(
        b[
            5,
        ],
        ak._v2.contents.emptyarray.EmptyArray,
    )
    assert (
        len(
            b[
                5,
            ]
        )
        == 0
    )
    assert isinstance(
        b[
            7:,
        ],
        ak._v2.contents.regulararray.RegularArray,
    )
    assert (
        len(
            b[
                7:,
            ]
        )
        == 3
    )
    assert (
        len(
            b[
                7:100,
            ]
        )
        == 3
    )
    with pytest.raises(IndexError):
        b[
            "bad",
        ]
    with pytest.raises(IndexError):
        b[
            ["bad", "good", "ok"],
        ]


def test_ListArray_NumpyArray():
    # 200 is inaccessible in stops
    # 6.6, 7.7, and 8.8 are inaccessible in content
    a = ak._v2.contents.listarray.ListArray(
        ak._v2.index.Index(np.array([4, 100, 1], dtype=np.int64)),
        ak._v2.index.Index(np.array([7, 100, 3, 200], dtype=np.int64)),
        ak._v2.contents.numpyarray.NumpyArray(
            np.array([6.6, 4.4, 5.5, 7.7, 1.1, 2.2, 3.3, 8.8])
        ),
    )
    assert len(a) == 3
    with pytest.raises(IndexError):
        a[
            3,
        ]
    with pytest.raises(IndexError):
        a[
            -4,
        ]
    assert isinstance(
        a[
            2,
        ],
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert (
        len(
            a[
                0,
            ]
        )
        == 3
    )
    assert (
        len(
            a[
                1,
            ]
        )
        == 0
    )
    assert (
        len(
            a[
                2,
            ]
        )
        == 2
    )
    assert (
        len(
            a[
                -3,
            ]
        )
        == 3
    )
    assert (
        len(
            a[
                -2,
            ]
        )
        == 0
    )
    assert (
        len(
            a[
                -1,
            ]
        )
        == 2
    )
    assert (
        a[0,][  # noqa: E231
            -1,
        ]
        == 3.3
    )
    assert (
        a[2,][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        a[
            1:,
        ],
        ak._v2.contents.listarray.ListArray,
    )
    assert (
        len(
            a[
                1:,
            ]
        )
        == 2
    )
    assert (
        len(
            a[
                -2:,
            ]
        )
        == 2
    )
    assert (
        len(
            a[
                1:100,
            ]
        )
        == 2
    )
    assert (
        len(
            a[
                -2:100,
            ]
        )
        == 2
    )
    with pytest.raises(IndexError):
        a[
            "bad",
        ]
    with pytest.raises(IndexError):
        a[
            ["bad", "good", "ok"],
        ]


def test_ListOffsetArray_NumpyArray():
    # 6.6 and 7.7 are inaccessible
    a = ak._v2.contents.listoffsetarray.ListOffsetArray(
        ak._v2.index.Index(np.array([1, 4, 4, 6])),
        ak._v2.contents.numpyarray.NumpyArray([6.6, 1.1, 2.2, 3.3, 4.4, 5.5, 7.7]),
    )
    assert len(a) == 3
    with pytest.raises(IndexError):
        a[
            3,
        ]
    with pytest.raises(IndexError):
        a[
            -4,
        ]
    assert isinstance(
        a[
            2,
        ],
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert (
        len(
            a[
                0,
            ]
        )
        == 3
    )
    assert (
        len(
            a[
                1,
            ]
        )
        == 0
    )
    assert (
        len(
            a[
                2,
            ]
        )
        == 2
    )
    assert (
        len(
            a[
                -3,
            ]
        )
        == 3
    )
    assert (
        len(
            a[
                -2,
            ]
        )
        == 0
    )
    assert (
        len(
            a[
                -1,
            ]
        )
        == 2
    )
    assert (
        a[0,][  # noqa: E231
            -1,
        ]
        == 3.3
    )
    assert (
        a[2,][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        a[
            1:,
        ],
        ak._v2.contents.listarray.ListArray,
    )
    assert (
        len(
            a[
                1:,
            ]
        )
        == 2
    )
    assert (
        len(
            a[
                -2:,
            ]
        )
        == 2
    )
    assert (
        len(
            a[
                1:100,
            ]
        )
        == 2
    )
    assert (
        len(
            a[
                -2:100,
            ]
        )
        == 2
    )
    with pytest.raises(IndexError):
        a[
            "bad",
        ]
    with pytest.raises(IndexError):
        a[
            ["bad", "good", "ok"],
        ]


def test_RecordArray_NumpyArray():
    # 5.5 is inaccessible
    a = ak._v2.contents.recordarray.RecordArray(
        [
            ak._v2.contents.numpyarray.NumpyArray(np.array([0, 1, 2, 3, 4])),
            ak._v2.contents.numpyarray.NumpyArray(
                np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5])
            ),
        ],
        ["x", "y"],
    )
    assert len(a) == 5
    with pytest.raises(IndexError):
        a[
            5,
        ]
    with pytest.raises(IndexError):
        a[
            -6,
        ]
    assert isinstance(
        a[
            2,
        ],
        ak._v2.record.Record,
    )
    assert (
        a[
            2,
        ]["y"]
        == 2.2
    )
    assert (
        a[
            -3,
        ]["y"]
        == 2.2
    )
    assert isinstance(
        a[
            2:,
        ],
        ak._v2.contents.indexedarray.IndexedArray,
    )
    assert (
        len(
            a[
                2:,
            ]
        )
        == 3
    )
    assert (
        len(
            a[
                -3:,
            ]
        )
        == 3
    )
    assert (
        len(
            a[
                2:100,
            ]
        )
        == 3
    )
    assert (
        len(
            a[
                -3:100,
            ]
        )
        == 3
    )
    assert isinstance(
        a[
            "y",
        ],
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert (
        a["y",][  # noqa: E231
            2,
        ]
        == 2.2
    )
    assert (
        a["y",][  # noqa: E231
            -3,
        ]
        == 2.2
    )
    with pytest.raises(IndexError):
        a[
            "z",
        ]
    with pytest.raises(IndexError):
        a[
            ["x", "z"],
        ]
    assert (
        len(
            a[
                ["x", "y"],
            ]
        )
        == 5
    )

    # 5.5 is inaccessible
    b = ak._v2.contents.recordarray.RecordArray(
        [
            ak._v2.contents.numpyarray.NumpyArray(np.array([0, 1, 2, 3, 4])),
            ak._v2.contents.numpyarray.NumpyArray(
                np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5])
            ),
        ],
        None,
    )
    assert len(b) == 5
    with pytest.raises(IndexError):
        b[
            5,
        ]
    with pytest.raises(IndexError):
        b[
            -6,
        ]
    assert isinstance(b[2], ak._v2.record.Record)
    assert (
        b[2,][  # noqa: E231
            "1",
        ]
        == 2.2
    )
    assert (
        b[-3,][  # noqa: E231
            "1",
        ]
        == 2.2
    )
    assert isinstance(
        b[
            2:,
        ],
        ak._v2.contents.indexedarray.IndexedArray,
    )
    assert (
        len(
            b[
                2:,
            ]
        )
        == 3
    )
    assert (
        len(
            b[
                -3:,
            ]
        )
        == 3
    )
    assert (
        len(
            b[
                2:100,
            ]
        )
        == 3
    )
    assert (
        len(
            b[
                -3:100,
            ]
        )
        == 3
    )
    assert isinstance(
        b[
            "1",
        ],
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert (
        b["1",][  # noqa: E231
            2,
        ]
        == 2.2
    )
    assert (
        b["1",][  # noqa: E231
            -3,
        ]
        == 2.2
    )
    with pytest.raises(IndexError):
        a[
            "2",
        ]
    assert (
        len(
            b[
                ["0", "1"],
            ]
        )
        == 5
    )

    c = ak._v2.contents.recordarray.RecordArray([], [], 10)
    assert len(c) == 10
    assert isinstance(
        c[
            5,
        ],
        ak._v2.record.Record,
    )
    assert isinstance(
        c[
            7:,
        ],
        ak._v2.contents.indexedarray.IndexedArray,
    )
    assert (
        len(
            c[
                7:,
            ]
        )
        == 3
    )
    assert (
        len(
            c[
                -3:,
            ]
        )
        == 3
    )
    with pytest.raises(IndexError):
        c[
            "x",
        ]

    d = ak._v2.contents.recordarray.RecordArray([], None, 10)
    assert len(d) == 10
    assert isinstance(
        d[
            5,
        ],
        ak._v2.record.Record,
    )
    assert isinstance(
        d[
            7:,
        ],
        ak._v2.contents.indexedarray.IndexedArray,
    )
    assert (
        len(
            d[
                7:,
            ]
        )
        == 3
    )
    assert (
        len(
            d[
                -3:,
            ]
        )
        == 3
    )
    with pytest.raises(IndexError):
        d[
            "0",
        ]


def test_IndexedArray_NumpyArray():
    # 4.4 is inaccessible; 3.3 and 5.5 appear twice
    a = ak._v2.contents.indexedarray.IndexedArray(
        ak._v2.index.Index(np.array([2, 2, 0, 1, 4, 5, 4])),
        ak._v2.contents.numpyarray.NumpyArray(np.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])),
    )
    assert len(a) == 7
    assert (
        a[
            0,
        ]
        == 3.3
    )
    assert (
        a[
            1,
        ]
        == 3.3
    )
    assert (
        a[
            2,
        ]
        == 1.1
    )
    assert (
        a[
            3,
        ]
        == 2.2
    )
    assert (
        a[
            4,
        ]
        == 5.5
    )
    assert (
        a[
            5,
        ]
        == 6.6
    )
    assert (
        a[
            6,
        ]
        == 5.5
    )
    assert (
        a[
            -7,
        ]
        == 3.3
    )
    assert (
        a[
            -6,
        ]
        == 3.3
    )
    assert (
        a[
            -5,
        ]
        == 1.1
    )
    assert (
        a[
            -4,
        ]
        == 2.2
    )
    assert (
        a[
            -3,
        ]
        == 5.5
    )
    assert (
        a[
            -2,
        ]
        == 6.6
    )
    assert (
        a[
            -1,
        ]
        == 5.5
    )
    with pytest.raises(IndexError):
        a[
            7,
        ]
    with pytest.raises(IndexError):
        a[
            -8,
        ]
    assert isinstance(
        a[
            3:,
        ],
        ak._v2.contents.indexedarray.IndexedArray,
    )
    assert (
        len(
            a[
                3:,
            ]
        )
        == 4
    )
    assert (
        len(
            a[
                -4:,
            ]
        )
        == 4
    )
    assert (
        len(
            a[
                3:100,
            ]
        )
        == 4
    )
    assert (
        len(
            a[
                -4:100,
            ]
        )
        == 4
    )
    assert (
        a[3:,][  # noqa: E231
            1,
        ]
        == 5.5
    )
    assert (
        a[-4:,][  # noqa: E231
            1,
        ]
        == 5.5
    )
    with pytest.raises(IndexError):
        a[
            "bad",
        ]
    with pytest.raises(IndexError):
        a[
            ["bad", "good", "ok"],
        ]


def test_IndexedOptionArray_NumpyArray():
    # 1.1 and 4.4 are inaccessible; 3.3 appears twice
    a = ak._v2.contents.indexedoptionarray.IndexedOptionArray(
        ak._v2.index.Index(np.array([2, 2, -1, 1, -1, 5, 4])),
        ak._v2.contents.numpyarray.NumpyArray(np.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])),
    )
    assert len(a) == 7
    assert (
        a[
            0,
        ]
        == 3.3
    )
    assert (
        a[
            1,
        ]
        == 3.3
    )
    assert (
        a[
            2,
        ]
        is None
    )
    assert (
        a[
            3,
        ]
        == 2.2
    )
    assert (
        a[
            4,
        ]
        is None
    )
    assert (
        a[
            5,
        ]
        == 6.6
    )
    assert (
        a[
            6,
        ]
        == 5.5
    )
    assert (
        a[
            -7,
        ]
        == 3.3
    )
    assert (
        a[
            -6,
        ]
        == 3.3
    )
    assert (
        a[
            -5,
        ]
        is None
    )
    assert (
        a[
            -4,
        ]
        == 2.2
    )
    assert (
        a[
            -3,
        ]
        is None
    )
    assert (
        a[
            -2,
        ]
        == 6.6
    )
    assert (
        a[
            -1,
        ]
        == 5.5
    )
    with pytest.raises(IndexError):
        a[
            7,
        ]
    with pytest.raises(IndexError):
        a[
            -8,
        ]
    assert isinstance(
        a[
            3:,
        ],
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert (
        len(
            a[
                3:,
            ]
        )
        == 4
    )
    assert (
        len(
            a[
                -4:,
            ]
        )
        == 4
    )
    assert (
        len(
            a[
                3:100,
            ]
        )
        == 4
    )
    assert (
        len(
            a[
                -4:100,
            ]
        )
        == 4
    )
    assert (
        a[3:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        a[-4:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        a[3:,][  # noqa: E231
            2,
        ]
        == 6.6
    )
    assert (
        a[-4:,][  # noqa: E231
            2,
        ]
        == 6.6
    )
    with pytest.raises(IndexError):
        a[
            "bad",
        ]
    with pytest.raises(IndexError):
        a[
            ["bad", "good", "ok"],
        ]


def test_ByteMaskedArray_NumpyArray():
    # 2.2, 4.4, and 6.6 are inaccessible
    a = ak._v2.contents.bytemaskedarray.ByteMaskedArray(
        ak._v2.index.Index(np.array([1, 0, 1, 0, 1], dtype=np.int8)),
        ak._v2.contents.numpyarray.NumpyArray(np.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])),
        valid_when=True,
    )
    assert len(a) == 5
    with pytest.raises(IndexError):
        a[
            5,
        ]
    with pytest.raises(IndexError):
        a[
            -6,
        ]
    assert (
        a[
            0,
        ]
        == 1.1
    )
    assert (
        a[
            1,
        ]
        is None
    )
    assert (
        a[
            2,
        ]
        == 3.3
    )
    assert (
        a[
            3,
        ]
        is None
    )
    assert (
        a[
            4,
        ]
        == 5.5
    )
    assert (
        a[
            -5,
        ]
        == 1.1
    )
    assert (
        a[
            -4,
        ]
        is None
    )
    assert (
        a[
            -3,
        ]
        == 3.3
    )
    assert (
        a[
            -2,
        ]
        is None
    )
    assert (
        a[
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        a[
            2:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            a[
                2:,
            ]
        )
        == 3
    )
    assert (
        len(
            a[
                -3:,
            ]
        )
        == 3
    )
    assert (
        len(
            a[
                2:100,
            ]
        )
        == 3
    )
    assert (
        len(
            a[
                -3:100,
            ]
        )
        == 3
    )
    assert (
        a[2:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        a[-3:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        a[2:,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    assert (
        a[-3:,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    with pytest.raises(IndexError):
        a[
            "bad",
        ]
    with pytest.raises(IndexError):
        a[
            ["bad", "good", "ok"],
        ]

    # 2.2, 4.4, and 6.6 are inaccessible
    b = ak._v2.contents.bytemaskedarray.ByteMaskedArray(
        ak._v2.index.Index(np.array([0, 1, 0, 1, 0], dtype=np.int8)),
        ak._v2.contents.numpyarray.NumpyArray(np.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])),
        valid_when=False,
    )
    assert len(b) == 5
    with pytest.raises(IndexError):
        b[
            5,
        ]
    with pytest.raises(IndexError):
        b[
            -6,
        ]
    assert (
        b[
            0,
        ]
        == 1.1
    )
    assert (
        b[
            1,
        ]
        is None
    )
    assert (
        b[
            2,
        ]
        == 3.3
    )
    assert (
        b[
            3,
        ]
        is None
    )
    assert (
        b[
            4,
        ]
        == 5.5
    )
    assert (
        b[
            -5,
        ]
        == 1.1
    )
    assert (
        b[
            -4,
        ]
        is None
    )
    assert (
        b[
            -3,
        ]
        == 3.3
    )
    assert (
        b[
            -2,
        ]
        is None
    )
    assert (
        b[
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        b[
            2:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            b[
                2:,
            ]
        )
        == 3
    )
    assert (
        len(
            b[
                -3:,
            ]
        )
        == 3
    )
    assert (
        len(
            b[
                2:100,
            ]
        )
        == 3
    )
    assert (
        len(
            b[
                -3:100,
            ]
        )
        == 3
    )
    assert (
        b[2:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        b[-3:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        b[2:,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    assert (
        b[-3:,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    with pytest.raises(IndexError):
        b[
            "bad",
        ]
    with pytest.raises(IndexError):
        b[
            ["bad", "good", "ok"],
        ]


def test_BitMaskedArray_NumpyArray():
    # 4.0, 5.0, 6.0, 7.0, 2.2, 4.4, and 6.6 are inaccessible
    a = ak._v2.contents.bitmaskedarray.BitMaskedArray(
        ak._v2.index.Index(
            np.packbits(
                np.array(
                    [
                        1,
                        1,
                        1,
                        1,
                        0,
                        0,
                        0,
                        0,
                        1,
                        0,
                        1,
                        0,
                        1,
                    ],
                    dtype=np.uint8,
                )
            )
        ),
        ak._v2.contents.numpyarray.NumpyArray(
            np.array(
                [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6]
            )
        ),
        valid_when=True,
        length=13,
        lsb_order=False,
    )
    assert len(a) == 13
    with pytest.raises(IndexError):
        a[
            13,
        ]
    with pytest.raises(IndexError):
        a[
            -14,
        ]
    assert (
        a[
            0,
        ]
        == 0.0
    )
    assert (
        a[
            1,
        ]
        == 1.0
    )
    assert (
        a[
            2,
        ]
        == 2.0
    )
    assert (
        a[
            3,
        ]
        == 3.0
    )
    assert (
        a[
            4,
        ]
        is None
    )
    assert (
        a[
            5,
        ]
        is None
    )
    assert (
        a[
            6,
        ]
        is None
    )
    assert (
        a[
            7,
        ]
        is None
    )
    assert (
        a[
            8,
        ]
        == 1.1
    )
    assert (
        a[
            9,
        ]
        is None
    )
    assert (
        a[
            10,
        ]
        == 3.3
    )
    assert (
        a[
            11,
        ]
        is None
    )
    assert (
        a[
            12,
        ]
        == 5.5
    )
    assert (
        a[
            -13,
        ]
        == 0.0
    )
    assert (
        a[
            -12,
        ]
        == 1.0
    )
    assert (
        a[
            -11,
        ]
        == 2.0
    )
    assert (
        a[
            -10,
        ]
        == 3.0
    )
    assert (
        a[
            -9,
        ]
        is None
    )
    assert (
        a[
            -8,
        ]
        is None
    )
    assert (
        a[
            -7,
        ]
        is None
    )
    assert (
        a[
            -6,
        ]
        is None
    )
    assert (
        a[
            -5,
        ]
        == 1.1
    )
    assert (
        a[
            -4,
        ]
        is None
    )
    assert (
        a[
            -3,
        ]
        == 3.3
    )
    assert (
        a[
            -2,
        ]
        is None
    )
    assert (
        a[
            -1,
        ]
        == 5.5
    )

    assert isinstance(
        a[
            5:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            a[
                5:,
            ]
        )
        == 8
    )
    assert (
        len(
            a[
                -8:,
            ]
        )
        == 8
    )
    assert (
        len(
            a[
                5:100,
            ]
        )
        == 8
    )
    assert (
        len(
            a[
                -8:100,
            ]
        )
        == 8
    )
    assert (
        a[5:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        a[5:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    assert (
        a[-8:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        a[-8:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    with pytest.raises(IndexError):
        a[
            "bad",
        ]

    # 4.0, 5.0, 6.0, 7.0, 2.2, 4.4, and 6.6 are inaccessible
    b = ak._v2.contents.bitmaskedarray.BitMaskedArray(
        ak._v2.index.Index(
            np.packbits(
                np.array(
                    [
                        0,
                        0,
                        0,
                        0,
                        1,
                        1,
                        1,
                        1,
                        0,
                        1,
                        0,
                        1,
                        0,
                    ],
                    dtype=np.uint8,
                )
            )
        ),
        ak._v2.contents.numpyarray.NumpyArray(
            np.array(
                [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6]
            )
        ),
        valid_when=False,
        length=13,
        lsb_order=False,
    )
    assert len(b) == 13
    with pytest.raises(IndexError):
        b[
            13,
        ]
    with pytest.raises(IndexError):
        b[
            -14,
        ]
    assert (
        b[
            0,
        ]
        == 0.0
    )
    assert (
        b[
            1,
        ]
        == 1.0
    )
    assert (
        b[
            2,
        ]
        == 2.0
    )
    assert (
        b[
            3,
        ]
        == 3.0
    )
    assert (
        b[
            4,
        ]
        is None
    )
    assert (
        b[
            5,
        ]
        is None
    )
    assert (
        b[
            6,
        ]
        is None
    )
    assert (
        b[
            7,
        ]
        is None
    )
    assert (
        b[
            8,
        ]
        == 1.1
    )
    assert (
        b[
            9,
        ]
        is None
    )
    assert (
        b[
            10,
        ]
        == 3.3
    )
    assert (
        b[
            11,
        ]
        is None
    )
    assert (
        b[
            12,
        ]
        == 5.5
    )
    assert (
        b[
            -13,
        ]
        == 0.0
    )
    assert (
        b[
            -12,
        ]
        == 1.0
    )
    assert (
        b[
            -11,
        ]
        == 2.0
    )
    assert (
        b[
            -10,
        ]
        == 3.0
    )
    assert (
        b[
            -9,
        ]
        is None
    )
    assert (
        b[
            -8,
        ]
        is None
    )
    assert (
        b[
            -7,
        ]
        is None
    )
    assert (
        b[
            -6,
        ]
        is None
    )
    assert (
        b[
            -5,
        ]
        == 1.1
    )
    assert (
        b[
            -4,
        ]
        is None
    )
    assert (
        b[
            -3,
        ]
        == 3.3
    )
    assert (
        b[
            -2,
        ]
        is None
    )
    assert (
        b[
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        b[
            5:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            b[
                5:,
            ]
        )
        == 8
    )
    assert (
        len(
            b[
                -8:,
            ]
        )
        == 8
    )
    assert (
        len(
            b[
                5:100,
            ]
        )
        == 8
    )
    assert (
        len(
            b[
                -8:100,
            ]
        )
        == 8
    )
    assert (
        b[5:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        b[5:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    assert (
        b[-8:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        b[-8:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    with pytest.raises(IndexError):
        b[
            "bad",
        ]

    # 4.0, 5.0, 6.0, 7.0, 2.2, 4.4, and 6.6 are inaccessible
    c = ak._v2.contents.bitmaskedarray.BitMaskedArray(
        ak._v2.index.Index(
            np.packbits(
                np.array(
                    [
                        0,
                        0,
                        0,
                        0,
                        1,
                        1,
                        1,
                        1,
                        0,
                        0,
                        0,
                        1,
                        0,
                        1,
                        0,
                        1,
                    ],
                    dtype=np.uint8,
                )
            )
        ),
        ak._v2.contents.numpyarray.NumpyArray(
            np.array(
                [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6]
            )
        ),
        valid_when=True,
        length=13,
        lsb_order=True,
    )
    assert len(c) == 13
    with pytest.raises(IndexError):
        c[
            13,
        ]
    with pytest.raises(IndexError):
        c[
            -14,
        ]
    assert (
        c[
            0,
        ]
        == 0.0
    )
    assert (
        c[
            1,
        ]
        == 1.0
    )
    assert (
        c[
            2,
        ]
        == 2.0
    )
    assert (
        c[
            3,
        ]
        == 3.0
    )
    assert (
        c[
            4,
        ]
        is None
    )
    assert (
        c[
            5,
        ]
        is None
    )
    assert (
        c[
            6,
        ]
        is None
    )
    assert (
        c[
            7,
        ]
        is None
    )
    assert (
        c[
            8,
        ]
        == 1.1
    )
    assert (
        c[
            9,
        ]
        is None
    )
    assert (
        c[
            10,
        ]
        == 3.3
    )
    assert (
        c[
            11,
        ]
        is None
    )
    assert (
        c[
            12,
        ]
        == 5.5
    )
    assert (
        c[
            -13,
        ]
        == 0.0
    )
    assert (
        c[
            -12,
        ]
        == 1.0
    )
    assert (
        c[
            -11,
        ]
        == 2.0
    )
    assert (
        c[
            -10,
        ]
        == 3.0
    )
    assert (
        c[
            -9,
        ]
        is None
    )
    assert (
        c[
            -8,
        ]
        is None
    )
    assert (
        c[
            -7,
        ]
        is None
    )
    assert (
        c[
            -6,
        ]
        is None
    )
    assert (
        c[
            -5,
        ]
        == 1.1
    )
    assert (
        c[
            -4,
        ]
        is None
    )
    assert (
        c[
            -3,
        ]
        == 3.3
    )
    assert (
        c[
            -2,
        ]
        is None
    )
    assert (
        c[
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        c[
            5:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            c[
                5:,
            ]
        )
        == 8
    )
    assert (
        len(
            c[
                -8:,
            ]
        )
        == 8
    )
    assert (
        len(
            c[
                5:100,
            ]
        )
        == 8
    )
    assert (
        len(
            c[
                -8:100,
            ]
        )
        == 8
    )
    assert (
        c[5:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        c[5:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    assert (
        c[-8:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        c[-8:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    with pytest.raises(IndexError):
        c[
            "bad",
        ]

    # 4.0, 5.0, 6.0, 7.0, 2.2, 4.4, and 6.6 are inaccessible
    d = ak._v2.contents.bitmaskedarray.BitMaskedArray(
        ak._v2.index.Index(
            np.packbits(
                np.array(
                    [
                        1,
                        1,
                        1,
                        1,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        1,
                        0,
                        1,
                        0,
                    ],
                    dtype=np.uint8,
                )
            )
        ),
        ak._v2.contents.numpyarray.NumpyArray(
            np.array(
                [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6]
            )
        ),
        valid_when=False,
        length=13,
        lsb_order=True,
    )
    assert len(d) == 13
    with pytest.raises(IndexError):
        d[
            13,
        ]
    with pytest.raises(IndexError):
        d[
            -14,
        ]
    assert (
        d[
            0,
        ]
        == 0.0
    )
    assert (
        d[
            1,
        ]
        == 1.0
    )
    assert (
        d[
            2,
        ]
        == 2.0
    )
    assert (
        d[
            3,
        ]
        == 3.0
    )
    assert (
        d[
            4,
        ]
        is None
    )
    assert (
        d[
            5,
        ]
        is None
    )
    assert (
        d[
            6,
        ]
        is None
    )
    assert (
        d[
            7,
        ]
        is None
    )
    assert (
        d[
            8,
        ]
        == 1.1
    )
    assert (
        d[
            9,
        ]
        is None
    )
    assert (
        d[
            10,
        ]
        == 3.3
    )
    assert (
        d[
            11,
        ]
        is None
    )
    assert (
        d[
            12,
        ]
        == 5.5
    )
    assert (
        d[
            -13,
        ]
        == 0.0
    )
    assert (
        d[
            -12,
        ]
        == 1.0
    )
    assert (
        d[
            -11,
        ]
        == 2.0
    )
    assert (
        d[
            -10,
        ]
        == 3.0
    )
    assert (
        d[
            -9,
        ]
        is None
    )
    assert (
        d[
            -8,
        ]
        is None
    )
    assert (
        d[
            -7,
        ]
        is None
    )
    assert (
        d[
            -6,
        ]
        is None
    )
    assert (
        d[
            -5,
        ]
        == 1.1
    )
    assert (
        d[
            -4,
        ]
        is None
    )
    assert (
        d[
            -3,
        ]
        == 3.3
    )
    assert (
        d[
            -2,
        ]
        is None
    )
    assert (
        d[
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        d[
            5:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            d[
                5:,
            ]
        )
        == 8
    )
    assert (
        len(
            d[
                -8:,
            ]
        )
        == 8
    )
    assert (
        len(
            d[
                5:100,
            ]
        )
        == 8
    )
    assert (
        len(
            d[
                -8:100,
            ]
        )
        == 8
    )
    assert (
        d[5:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        d[5:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    assert (
        d[-8:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        d[-8:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    with pytest.raises(IndexError):
        d[
            "bad",
        ]


def test_UnmaskedArray_NumpyArray():
    a = ak._v2.contents.unmaskedarray.UnmaskedArray(
        ak._v2.contents.numpyarray.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3], dtype=np.float64)
        )
    )
    assert len(a) == 4
    assert (
        a[
            2,
        ]
        == 2.2
    )
    assert (
        a[
            -2,
        ]
        == 2.2
    )
    assert (
        type(
            a[
                2,
            ]
        )
        is np.float64
    )
    with pytest.raises(IndexError):
        a[
            4,
        ]
    with pytest.raises(IndexError):
        a[
            -5,
        ]
    assert isinstance(
        a[
            2:,
        ],
        ak._v2.contents.unmaskedarray.UnmaskedArray,
    )
    assert (
        a[2:,][  # noqa: E231
            0,
        ]
        == 2.2
    )
    assert (
        len(
            a[
                2:,
            ]
        )
        == 2
    )
    with pytest.raises(IndexError):
        a[
            "bad",
        ]


def test_UnionArray_NumpyArray():
    # 100 is inaccessible in index
    # 1.1 is inaccessible in contents[1]
    a = ak._v2.contents.unionarray.UnionArray(
        ak._v2.index.Index(np.array([1, 1, 0, 0, 1, 0, 1], dtype=np.int8)),
        ak._v2.index.Index(np.array([4, 3, 0, 1, 2, 2, 4, 100])),
        [
            ak._v2.contents.numpyarray.NumpyArray(np.array([1, 2, 3])),
            ak._v2.contents.numpyarray.NumpyArray(np.array([1.1, 2.2, 3.3, 4.4, 5.5])),
        ],
    )
    assert len(a) == 7
    with pytest.raises(IndexError):
        a[
            7,
        ]
    with pytest.raises(IndexError):
        a[
            -8,
        ]
    assert (
        a[
            0,
        ]
        == 5.5
    )
    assert (
        a[
            1,
        ]
        == 4.4
    )
    assert (
        a[
            2,
        ]
        == 1.0
    )
    assert (
        a[
            3,
        ]
        == 2.0
    )
    assert (
        a[
            4,
        ]
        == 3.3
    )
    assert (
        a[
            5,
        ]
        == 3.0
    )
    assert (
        a[
            6,
        ]
        == 5.5
    )
    assert (
        a[
            -7,
        ]
        == 5.5
    )
    assert (
        a[
            -6,
        ]
        == 4.4
    )
    assert (
        a[
            -5,
        ]
        == 1.0
    )
    assert (
        a[
            -4,
        ]
        == 2.0
    )
    assert (
        a[
            -3,
        ]
        == 3.3
    )
    assert (
        a[
            -2,
        ]
        == 3.0
    )
    assert (
        a[
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        a[
            3:,
        ],
        ak._v2.contents.unionarray.UnionArray,
    )
    assert (
        len(
            a[
                3:,
            ]
        )
        == 4
    )
    assert (
        len(
            a[
                -4:,
            ]
        )
        == 4
    )
    assert (
        len(
            a[
                3:100,
            ]
        )
        == 4
    )
    assert (
        len(
            a[
                -4:100,
            ]
        )
        == 4
    )
    assert (
        a[3:,][  # noqa: E231
            1,
        ]
        == 3.3
    )
    assert (
        a[3:,][  # noqa: E231
            2,
        ]
        == 3.0
    )
    assert (
        a[-4:,][  # noqa: E231
            1,
        ]
        == 3.3
    )
    assert (
        a[-4:,][  # noqa: E231
            2,
        ]
        == 3.0
    )
    with pytest.raises(IndexError):
        a[
            "bad",
        ]
    with pytest.raises(IndexError):
        a[
            ["bad", "good", "ok"],
        ]


def test_RegularArray_RecordArray_NumpyArray():
    # 6.6 is inaccessible
    a = ak._v2.contents.regulararray.RegularArray(  # noqa: F841
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
                )
            ],
            ["nest"],
        ),
        3,
    )
    assert (
        len(
            a[
                "nest",
            ]
        )
        == 2
    )
    assert isinstance(
        a["nest",][  # noqa: E231
            1,
        ],
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                1,
            ]
        )
        == 3
    )
    assert (
        a["nest",][1,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    assert (
        a["nest",][-1,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    assert isinstance(
        a["nest",][  # noqa: E231
            1:2,
        ],
        ak._v2.contents.regulararray.RegularArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                1:,
            ]
        )
        == 1
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                1:100,
            ]
        )
        == 1
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            2,
        ]
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            -3,
        ]
    with pytest.raises(IndexError):
        a["nest",][1,][  # noqa: E231
            3,
        ]
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            "bad",
        ]

    b = ak._v2.contents.regulararray.RegularArray(  # noqa: F841
        ak._v2.contents.recordarray.RecordArray(
            [ak._v2.contents.emptyarray.EmptyArray()], ["nest"]
        ),
        0,
        zeros_length=10,
    )
    assert (
        len(
            b[
                "nest",
            ]
        )
        == 10
    )
    assert isinstance(
        b["nest",][  # noqa: E231
            5,
        ],
        ak._v2.contents.emptyarray.EmptyArray,
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                5,
            ]
        )
        == 0
    )
    assert isinstance(
        b["nest",][  # noqa: E231
            7:,
        ],
        ak._v2.contents.regulararray.RegularArray,
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                7:,
            ]
        )
        == 3
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                7:100,
            ]
        )
        == 3
    )
    with pytest.raises(IndexError):
        b["nest",][  # noqa: E231
            "bad",
        ]


def test_ListArray_RecordArray_NumpyArray():
    # 200 is inaccessible in stops
    # 6.6, 7.7, and 8.8 are inaccessible in content
    a = ak._v2.contents.listarray.ListArray(  # noqa: F841
        ak._v2.index.Index(np.array([4, 100, 1])),
        ak._v2.index.Index(np.array([7, 100, 3, 200])),
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array([6.6, 4.4, 5.5, 7.7, 1.1, 2.2, 3.3, 8.8])
                )
            ],
            ["nest"],
        ),
    )
    assert (
        len(
            a[
                "nest",
            ]
        )
        == 3
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            3,
        ]
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            -4,
        ]
    assert isinstance(
        a["nest",][  # noqa: E231
            2,
        ],
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                0,
            ]
        )
        == 3
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                1,
            ]
        )
        == 0
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                2,
            ]
        )
        == 2
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -3,
            ]
        )
        == 3
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -2,
            ]
        )
        == 0
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -1,
            ]
        )
        == 2
    )
    assert (
        a["nest",][0,][  # noqa: E231
            -1,
        ]
        == 3.3
    )
    assert (
        a["nest",][2,][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        a["nest",][  # noqa: E231
            1:,
        ],
        ak._v2.contents.listarray.ListArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                1:,
            ]
        )
        == 2
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -2:,
            ]
        )
        == 2
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                1:100,
            ]
        )
        == 2
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -2:100,
            ]
        )
        == 2
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            "bad",
        ]


def test_ListOffsetArray_RecordArray_NumpyArray():
    # 6.6 and 7.7 are inaccessible
    a = ak._v2.contents.listoffsetarray.ListOffsetArray(  # noqa: F841
        ak._v2.index.Index(np.array([1, 4, 4, 6])),
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    [6.6, 1.1, 2.2, 3.3, 4.4, 5.5, 7.7]
                )
            ],
            ["nest"],
        ),
    )
    assert (
        len(
            a[
                "nest",
            ]
        )
        == 3
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            3,
        ]
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            -4,
        ]
    assert isinstance(
        a["nest",][  # noqa: E231
            2,
        ],
        ak._v2.contents.numpyarray.NumpyArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                0,
            ]
        )
        == 3
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                1,
            ]
        )
        == 0
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                2,
            ]
        )
        == 2
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -3,
            ]
        )
        == 3
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -2,
            ]
        )
        == 0
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -1,
            ]
        )
        == 2
    )
    assert (
        a["nest",][0,][  # noqa: E231
            -1,
        ]
        == 3.3
    )
    assert (
        a["nest",][2,][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        a["nest",][  # noqa: E231
            1:,
        ],
        ak._v2.contents.listarray.ListArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                1:,
            ]
        )
        == 2
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -2:,
            ]
        )
        == 2
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                1:100,
            ]
        )
        == 2
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -2:100,
            ]
        )
        == 2
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            "bad",
        ]


def test_IndexedArray_RecordArray_NumpyArray():
    # 4.4 is inaccessible; 3.3 and 5.5 appear twice
    a = ak._v2.contents.indexedarray.IndexedArray(  # noqa: F841
        ak._v2.index.Index(np.array([2, 2, 0, 1, 4, 5, 4])),
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
                )
            ],
            ["nest"],
        ),
    )
    assert (
        len(
            a[
                "nest",
            ]
        )
        == 7
    )
    assert (
        a["nest",][  # noqa: E231
            0,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            1,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            2,
        ]
        == 1.1
    )
    assert (
        a["nest",][  # noqa: E231
            3,
        ]
        == 2.2
    )
    assert (
        a["nest",][  # noqa: E231
            4,
        ]
        == 5.5
    )
    assert (
        a["nest",][  # noqa: E231
            5,
        ]
        == 6.6
    )
    assert (
        a["nest",][  # noqa: E231
            6,
        ]
        == 5.5
    )
    assert (
        a["nest",][  # noqa: E231
            -7,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            -6,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            -5,
        ]
        == 1.1
    )
    assert (
        a["nest",][  # noqa: E231
            -4,
        ]
        == 2.2
    )
    assert (
        a["nest",][  # noqa: E231
            -3,
        ]
        == 5.5
    )
    assert (
        a["nest",][  # noqa: E231
            -2,
        ]
        == 6.6
    )
    assert (
        a["nest",][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            7,
        ]
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            -8,
        ]
    assert isinstance(
        a["nest",][  # noqa: E231
            3:,
        ],
        ak._v2.contents.indexedarray.IndexedArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                3:,
            ]
        )
        == 4
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -4:,
            ]
        )
        == 4
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                3:100,
            ]
        )
        == 4
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -4:100,
            ]
        )
        == 4
    )
    assert (
        a["nest",][3:,][  # noqa: E231
            1,
        ]
        == 5.5
    )
    assert (
        a["nest",][-4:,][  # noqa: E231
            1,
        ]
        == 5.5
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            "bad",
        ]


def test_IndexedOptionArray_RecordArray_NumpyArray():
    # 1.1 and 4.4 are inaccessible; 3.3 appears twice
    a = ak._v2.contents.indexedoptionarray.IndexedOptionArray(  # noqa: F841
        ak._v2.index.Index(np.array([2, 2, -1, 1, -1, 5, 4])),
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
                )
            ],
            ["nest"],
        ),
    )
    assert (
        len(
            a[
                "nest",
            ]
        )
        == 7
    )
    assert (
        a["nest",][  # noqa: E231
            0,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            1,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            3,
        ]
        == 2.2
    )
    assert (
        a["nest",][  # noqa: E231
            4,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            5,
        ]
        == 6.6
    )
    assert (
        a["nest",][  # noqa: E231
            6,
        ]
        == 5.5
    )
    assert (
        a["nest",][  # noqa: E231
            -7,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            -6,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            -5,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            -4,
        ]
        == 2.2
    )
    assert (
        a["nest",][  # noqa: E231
            -3,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            -2,
        ]
        == 6.6
    )
    assert (
        a["nest",][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            7,
        ]
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            -8,
        ]
    assert isinstance(
        a["nest",][  # noqa: E231
            3:,
        ],
        ak._v2.contents.indexedoptionarray.IndexedOptionArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                3:,
            ]
        )
        == 4
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -4:,
            ]
        )
        == 4
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                3:100,
            ]
        )
        == 4
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -4:100,
            ]
        )
        == 4
    )
    assert (
        a["nest",][3:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        a["nest",][-4:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        a["nest",][3:,][  # noqa: E231
            2,
        ]
        == 6.6
    )
    assert (
        a["nest",][-4:,][  # noqa: E231
            2,
        ]
        == 6.6
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            "bad",
        ]


def test_ByteMaskedArray_RecordArray_NumpyArray():
    # 2.2, 4.4, and 6.6 are inaccessible
    a = ak._v2.contents.bytemaskedarray.ByteMaskedArray(  # noqa: F841
        ak._v2.index.Index(np.array([1, 0, 1, 0, 1], dtype=np.int8)),
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
                )
            ],
            ["nest"],
        ),
        valid_when=True,
    )
    assert (
        len(
            a[
                "nest",
            ]
        )
        == 5
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            5,
        ]
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            -6,
        ]
    assert (
        a["nest",][  # noqa: E231
            0,
        ]
        == 1.1
    )
    assert (
        a["nest",][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            2,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            3,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            4,
        ]
        == 5.5
    )
    assert (
        a["nest",][  # noqa: E231
            -5,
        ]
        == 1.1
    )
    assert (
        a["nest",][  # noqa: E231
            -4,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            -3,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            -2,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        a["nest",][  # noqa: E231
            2:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                2:,
            ]
        )
        == 3
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -3:,
            ]
        )
        == 3
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                2:100,
            ]
        )
        == 3
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -3:100,
            ]
        )
        == 3
    )
    assert (
        a["nest",][2:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        a["nest",][-3:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        a["nest",][2:,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    assert (
        a["nest",][-3:,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            "bad",
        ]

    # 2.2, 4.4, and 6.6 are inaccessible
    b = ak._v2.contents.bytemaskedarray.ByteMaskedArray(  # noqa: F841
        ak._v2.index.Index(np.array([0, 1, 0, 1, 0], dtype=np.int8)),
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
                )
            ],
            ["nest"],
        ),
        valid_when=False,
    )
    assert (
        len(
            b[
                "nest",
            ]
        )
        == 5
    )
    with pytest.raises(IndexError):
        b["nest",][  # noqa: E231
            5,
        ]
    with pytest.raises(IndexError):
        b["nest",][  # noqa: E231
            -6,
        ]
    assert (
        b["nest",][  # noqa: E231
            0,
        ]
        == 1.1
    )
    assert (
        b["nest",][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            2,
        ]
        == 3.3
    )
    assert (
        b["nest",][  # noqa: E231
            3,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            4,
        ]
        == 5.5
    )
    assert (
        b["nest",][  # noqa: E231
            -5,
        ]
        == 1.1
    )
    assert (
        b["nest",][  # noqa: E231
            -4,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            -3,
        ]
        == 3.3
    )
    assert (
        b["nest",][  # noqa: E231
            -2,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        b["nest",][  # noqa: E231
            2:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                2:,
            ]
        )
        == 3
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                -3:,
            ]
        )
        == 3
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                2:100,
            ]
        )
        == 3
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                -3:100,
            ]
        )
        == 3
    )
    assert (
        b["nest",][2:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        b["nest",][-3:,][  # noqa: E231
            1,
        ]
        is None
    )
    assert (
        b["nest",][2:,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    assert (
        b["nest",][-3:,][  # noqa: E231
            2,
        ]
        == 5.5
    )
    with pytest.raises(IndexError):
        b["nest",][  # noqa: E231
            "bad",
        ]


def test_BitMaskedArray_RecordArray_NumpyArray():
    # 4.0, 5.0, 6.0, 7.0, 2.2, 4.4, and 6.6 are inaccessible
    a = ak._v2.contents.bitmaskedarray.BitMaskedArray(
        ak._v2.index.Index(
            np.packbits(
                np.array(
                    [
                        True,
                        True,
                        True,
                        True,
                        False,
                        False,
                        False,
                        False,
                        True,
                        False,
                        True,
                        False,
                        True,
                    ]
                )
            )
        ),
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array(
                        [
                            0.0,
                            1.0,
                            2.0,
                            3.0,
                            4.0,
                            5.0,
                            6.0,
                            7.0,
                            1.1,
                            2.2,
                            3.3,
                            4.4,
                            5.5,
                            6.6,
                        ]
                    )
                )
            ],
            ["nest"],
        ),
        valid_when=True,
        length=13,
        lsb_order=False,
    )
    assert len(a["nest"]) == 13
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            13,
        ]
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            -14,
        ]
    assert (
        a["nest",][  # noqa: E231
            0,
        ]
        == 0.0
    )
    assert (
        a["nest",][  # noqa: E231
            1,
        ]
        == 1.0
    )
    assert (
        a["nest",][  # noqa: E231
            2,
        ]
        == 2.0
    )
    assert (
        a["nest",][  # noqa: E231
            3,
        ]
        == 3.0
    )
    assert (
        a["nest",][  # noqa: E231
            4,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            5,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            6,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            7,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            8,
        ]
        == 1.1
    )
    assert (
        a["nest",][  # noqa: E231
            9,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            10,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            11,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            12,
        ]
        == 5.5
    )
    assert (
        a["nest",][  # noqa: E231
            -13,
        ]
        == 0.0
    )
    assert (
        a["nest",][  # noqa: E231
            -12,
        ]
        == 1.0
    )
    assert (
        a["nest",][  # noqa: E231
            -11,
        ]
        == 2.0
    )
    assert (
        a["nest",][  # noqa: E231
            -10,
        ]
        == 3.0
    )
    assert (
        a["nest",][  # noqa: E231
            -9,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            -8,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            -7,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            -6,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            -5,
        ]
        == 1.1
    )
    assert (
        a["nest",][  # noqa: E231
            -4,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            -3,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            -2,
        ]
        is None
    )
    assert (
        a["nest",][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        a["nest",][  # noqa: E231
            5:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                5:,
            ]
        )
        == 8
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -8:,
            ]
        )
        == 8
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                5:100,
            ]
        )
        == 8
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -8:100,
            ]
        )
        == 8
    )
    assert (
        a["nest",][5:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        a["nest",][5:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    assert (
        a["nest",][-8:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        a["nest",][-8:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            "bad",
        ]

    # 4.0, 5.0, 6.0, 7.0, 2.2, 4.4, and 6.6 are inaccessible
    b = ak._v2.contents.bitmaskedarray.BitMaskedArray(  # noqa: F841
        ak._v2.index.Index(
            np.packbits(
                np.array(
                    [
                        0,
                        0,
                        0,
                        0,
                        1,
                        1,
                        1,
                        1,
                        0,
                        1,
                        0,
                        1,
                        0,
                    ],
                    dtype=np.uint8,
                )
            )
        ),
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array(
                        [
                            0.0,
                            1.0,
                            2.0,
                            3.0,
                            4.0,
                            5.0,
                            6.0,
                            7.0,
                            1.1,
                            2.2,
                            3.3,
                            4.4,
                            5.5,
                            6.6,
                        ]
                    )
                )
            ],
            ["nest"],
        ),
        valid_when=False,
        length=13,
        lsb_order=False,
    )
    assert (
        len(
            b[
                "nest",
            ]
        )
        == 13
    )
    with pytest.raises(IndexError):
        b["nest",][  # noqa: E231
            13,
        ]
    with pytest.raises(IndexError):
        b["nest",][  # noqa: E231
            -14,
        ]
    assert (
        b["nest",][  # noqa: E231
            0,
        ]
        == 0.0
    )
    assert (
        b["nest",][  # noqa: E231
            1,
        ]
        == 1.0
    )
    assert (
        b["nest",][  # noqa: E231
            2,
        ]
        == 2.0
    )
    assert (
        b["nest",][  # noqa: E231
            3,
        ]
        == 3.0
    )
    assert (
        b["nest",][  # noqa: E231
            4,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            5,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            6,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            7,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            8,
        ]
        == 1.1
    )
    assert (
        b["nest",][  # noqa: E231
            9,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            10,
        ]
        == 3.3
    )
    assert (
        b["nest",][  # noqa: E231
            11,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            12,
        ]
        == 5.5
    )
    assert (
        b["nest",][  # noqa: E231
            -13,
        ]
        == 0.0
    )
    assert (
        b["nest",][  # noqa: E231
            -12,
        ]
        == 1.0
    )
    assert (
        b["nest",][  # noqa: E231
            -11,
        ]
        == 2.0
    )
    assert (
        b["nest",][  # noqa: E231
            -10,
        ]
        == 3.0
    )
    assert (
        b["nest",][  # noqa: E231
            -9,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            -8,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            -7,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            -6,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            -5,
        ]
        == 1.1
    )
    assert (
        b["nest",][  # noqa: E231
            -4,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            -3,
        ]
        == 3.3
    )
    assert (
        b["nest",][  # noqa: E231
            -2,
        ]
        is None
    )
    assert (
        b["nest",][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        b["nest",][  # noqa: E231
            5:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                5:,
            ]
        )
        == 8
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                -8:,
            ]
        )
        == 8
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                5:100,
            ]
        )
        == 8
    )
    assert (
        len(
            b["nest",][  # noqa: E231
                -8:100,
            ]
        )
        == 8
    )
    assert (
        b["nest",][5:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        b["nest",][5:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    assert (
        b["nest",][-8:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        b["nest",][-8:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    with pytest.raises(IndexError):
        b["nest",][  # noqa: E231
            "bad",
        ]

    # 4.0, 5.0, 6.0, 7.0, 2.2, 4.4, and 6.6 are inaccessible
    c = ak._v2.contents.bitmaskedarray.BitMaskedArray(  # noqa: F841
        ak._v2.index.Index(
            np.packbits(
                np.array(
                    [
                        0,
                        0,
                        0,
                        0,
                        1,
                        1,
                        1,
                        1,
                        0,
                        0,
                        0,
                        1,
                        0,
                        1,
                        0,
                        1,
                    ],
                    dtype=np.uint8,
                )
            )
        ),
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array(
                        [
                            0.0,
                            1.0,
                            2.0,
                            3.0,
                            4.0,
                            5.0,
                            6.0,
                            7.0,
                            1.1,
                            2.2,
                            3.3,
                            4.4,
                            5.5,
                            6.6,
                        ]
                    )
                )
            ],
            ["nest"],
        ),
        valid_when=True,
        length=13,
        lsb_order=True,
    )
    assert (
        len(
            c[
                "nest",
            ]
        )
        == 13
    )
    with pytest.raises(IndexError):
        c["nest",][  # noqa: E231
            13,
        ]
    with pytest.raises(IndexError):
        c["nest",][  # noqa: E231
            -14,
        ]
    assert (
        c["nest",][  # noqa: E231
            0,
        ]
        == 0.0
    )
    assert (
        c["nest",][  # noqa: E231
            1,
        ]
        == 1.0
    )
    assert (
        c["nest",][  # noqa: E231
            2,
        ]
        == 2.0
    )
    assert (
        c["nest",][  # noqa: E231
            3,
        ]
        == 3.0
    )
    assert (
        c["nest",][  # noqa: E231
            4,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            5,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            6,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            7,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            8,
        ]
        == 1.1
    )
    assert (
        c["nest",][  # noqa: E231
            9,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            10,
        ]
        == 3.3
    )
    assert (
        c["nest",][  # noqa: E231
            11,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            12,
        ]
        == 5.5
    )
    assert (
        c["nest",][  # noqa: E231
            -13,
        ]
        == 0.0
    )
    assert (
        c["nest",][  # noqa: E231
            -12,
        ]
        == 1.0
    )
    assert (
        c["nest",][  # noqa: E231
            -11,
        ]
        == 2.0
    )
    assert (
        c["nest",][  # noqa: E231
            -10,
        ]
        == 3.0
    )
    assert (
        c["nest",][  # noqa: E231
            -9,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            -8,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            -7,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            -6,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            -5,
        ]
        == 1.1
    )
    assert (
        c["nest",][  # noqa: E231
            -4,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            -3,
        ]
        == 3.3
    )
    assert (
        c["nest",][  # noqa: E231
            -2,
        ]
        is None
    )
    assert (
        c["nest",][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        c["nest",][  # noqa: E231
            5:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            c["nest",][  # noqa: E231
                5:,
            ]
        )
        == 8
    )
    assert (
        len(
            c["nest",][  # noqa: E231
                -8:,
            ]
        )
        == 8
    )
    assert (
        len(
            c["nest",][  # noqa: E231
                5:100,
            ]
        )
        == 8
    )
    assert (
        len(
            c["nest",][  # noqa: E231
                -8:100,
            ]
        )
        == 8
    )
    assert (
        c["nest",][5:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        c["nest",][5:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    assert (
        c["nest",][-8:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        c["nest",][-8:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    with pytest.raises(IndexError):
        c["nest",][  # noqa: E231
            "bad",
        ]

    # 4.0, 5.0, 6.0, 7.0, 2.2, 4.4, and 6.6 are inaccessible
    d = ak._v2.contents.bitmaskedarray.BitMaskedArray(  # noqa: F841
        ak._v2.index.Index(
            np.packbits(
                np.array(
                    [
                        1,
                        1,
                        1,
                        1,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        1,
                        0,
                        1,
                        0,
                    ],
                    dtype=np.uint8,
                )
            )
        ),
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array(
                        [
                            0.0,
                            1.0,
                            2.0,
                            3.0,
                            4.0,
                            5.0,
                            6.0,
                            7.0,
                            1.1,
                            2.2,
                            3.3,
                            4.4,
                            5.5,
                            6.6,
                        ]
                    )
                )
            ],
            ["nest"],
        ),
        valid_when=False,
        length=13,
        lsb_order=True,
    )
    assert (
        len(
            d[
                "nest",
            ]
        )
        == 13
    )
    with pytest.raises(IndexError):
        d["nest",][  # noqa: E231
            13,
        ]
    with pytest.raises(IndexError):
        d["nest",][  # noqa: E231
            -14,
        ]
    assert (
        d["nest",][  # noqa: E231
            0,
        ]
        == 0.0
    )
    assert (
        d["nest",][  # noqa: E231
            1,
        ]
        == 1.0
    )
    assert (
        d["nest",][  # noqa: E231
            2,
        ]
        == 2.0
    )
    assert (
        d["nest",][  # noqa: E231
            3,
        ]
        == 3.0
    )
    assert (
        d["nest",][  # noqa: E231
            4,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            5,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            6,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            7,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            8,
        ]
        == 1.1
    )
    assert (
        d["nest",][  # noqa: E231
            9,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            10,
        ]
        == 3.3
    )
    assert (
        d["nest",][  # noqa: E231
            11,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            12,
        ]
        == 5.5
    )
    assert (
        d["nest",][  # noqa: E231
            -13,
        ]
        == 0.0
    )
    assert (
        d["nest",][  # noqa: E231
            -12,
        ]
        == 1.0
    )
    assert (
        d["nest",][  # noqa: E231
            -11,
        ]
        == 2.0
    )
    assert (
        d["nest",][  # noqa: E231
            -10,
        ]
        == 3.0
    )
    assert (
        d["nest",][  # noqa: E231
            -9,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            -8,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            -7,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            -6,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            -5,
        ]
        == 1.1
    )
    assert (
        d["nest",][  # noqa: E231
            -4,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            -3,
        ]
        == 3.3
    )
    assert (
        d["nest",][  # noqa: E231
            -2,
        ]
        is None
    )
    assert (
        d["nest",][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        d["nest",][  # noqa: E231
            5:,
        ],
        ak._v2.contents.bytemaskedarray.ByteMaskedArray,
    )
    assert (
        len(
            d["nest",][  # noqa: E231
                5:,
            ]
        )
        == 8
    )
    assert (
        len(
            d["nest",][  # noqa: E231
                -8:,
            ]
        )
        == 8
    )
    assert (
        len(
            d["nest",][  # noqa: E231
                5:100,
            ]
        )
        == 8
    )
    assert (
        len(
            d["nest",][  # noqa: E231
                -8:100,
            ]
        )
        == 8
    )
    assert (
        d["nest",][5:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        d["nest",][5:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    assert (
        d["nest",][-8:,][  # noqa: E231
            2,
        ]
        is None
    )
    assert (
        d["nest",][-8:,][  # noqa: E231
            3,
        ]
        == 1.1
    )
    with pytest.raises(IndexError):
        d["nest",][  # noqa: E231
            "bad",
        ]


def test_UnmaskedArray_RecordArray_NumpyArray():
    a = ak._v2.contents.unmaskedarray.UnmaskedArray(  # noqa: F841
        ak._v2.contents.recordarray.RecordArray(
            [
                ak._v2.contents.numpyarray.NumpyArray(
                    np.array([0.0, 1.1, 2.2, 3.3], dtype=np.float64)
                )
            ],
            ["nest"],
        )
    )
    assert (
        len(
            a[
                "nest",
            ]
        )
        == 4
    )
    assert (
        a["nest",][  # noqa: E231
            2,
        ]
        == 2.2
    )
    assert (
        a["nest",][  # noqa: E231
            -2,
        ]
        == 2.2
    )
    assert (
        type(
            a["nest",][  # noqa: E231
                2,
            ]
        )
        is np.float64
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            4,
        ]
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            -5,
        ]
    assert isinstance(
        a["nest",][  # noqa: E231
            2:,
        ],
        ak._v2.contents.unmaskedarray.UnmaskedArray,
    )
    assert (
        a["nest",][2:,][  # noqa: E231
            0,
        ]
        == 2.2
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                2:,
            ]
        )
        == 2
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            "bad",
        ]


def test_UnionArray_RecordArray_NumpyArray():
    # 100 is inaccessible in index
    # 1.1 is inaccessible in contents[1]
    a = ak._v2.contents.unionarray.UnionArray(  # noqa: F841
        ak._v2.index.Index(np.array([1, 1, 0, 0, 1, 0, 1], dtype=np.int8)),
        ak._v2.index.Index(np.array([4, 3, 0, 1, 2, 2, 4, 100])),
        [
            ak._v2.contents.recordarray.RecordArray(
                [ak._v2.contents.numpyarray.NumpyArray(np.array([1, 2, 3]))], ["nest"]
            ),
            ak._v2.contents.recordarray.RecordArray(
                [
                    ak._v2.contents.numpyarray.NumpyArray(
                        np.array([1.1, 2.2, 3.3, 4.4, 5.5])
                    )
                ],
                ["nest"],
            ),
        ],
    )
    assert (
        len(
            a[
                "nest",
            ]
        )
        == 7
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            7,
        ]
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            -8,
        ]
    assert (
        a["nest",][  # noqa: E231
            0,
        ]
        == 5.5
    )
    assert (
        a["nest",][  # noqa: E231
            1,
        ]
        == 4.4
    )
    assert (
        a["nest",][  # noqa: E231
            2,
        ]
        == 1.0
    )
    assert (
        a["nest",][  # noqa: E231
            3,
        ]
        == 2.0
    )
    assert (
        a["nest",][  # noqa: E231
            4,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            5,
        ]
        == 3.0
    )
    assert (
        a["nest",][  # noqa: E231
            6,
        ]
        == 5.5
    )
    assert (
        a["nest",][  # noqa: E231
            -7,
        ]
        == 5.5
    )
    assert (
        a["nest",][  # noqa: E231
            -6,
        ]
        == 4.4
    )
    assert (
        a["nest",][  # noqa: E231
            -5,
        ]
        == 1.0
    )
    assert (
        a["nest",][  # noqa: E231
            -4,
        ]
        == 2.0
    )
    assert (
        a["nest",][  # noqa: E231
            -3,
        ]
        == 3.3
    )
    assert (
        a["nest",][  # noqa: E231
            -2,
        ]
        == 3.0
    )
    assert (
        a["nest",][  # noqa: E231
            -1,
        ]
        == 5.5
    )
    assert isinstance(
        a["nest",][  # noqa: E231
            3:,
        ],
        ak._v2.contents.unionarray.UnionArray,
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                3:,
            ]
        )
        == 4
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -4:,
            ]
        )
        == 4
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                3:100,
            ]
        )
        == 4
    )
    assert (
        len(
            a["nest",][  # noqa: E231
                -4:100,
            ]
        )
        == 4
    )
    assert (
        a["nest",][3:,][  # noqa: E231
            1,
        ]
        == 3.3
    )
    assert (
        a["nest",][3:,][  # noqa: E231
            2,
        ]
        == 3.0
    )
    assert (
        a["nest",][-4:,][  # noqa: E231
            1,
        ]
        == 3.3
    )
    assert (
        a["nest",][-4:,][  # noqa: E231
            2,
        ]
        == 3.0
    )
    with pytest.raises(IndexError):
        a["nest",][  # noqa: E231
            "bad",
        ]
