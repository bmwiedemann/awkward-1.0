# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import awkward as ak
from awkward._v2.index import Index
from awkward._v2.contents.content import Content, NestedIndexError
from awkward._v2.contents.bytemaskedarray import ByteMaskedArray
from awkward._v2.forms.bitmaskedform import BitMaskedForm

np = ak.nplike.NumpyMetadata.instance()


class BitMaskedArray(Content):
    def __init__(
        self,
        mask,
        content,
        valid_when,
        length,
        lsb_order,
        identifier=None,
        parameters=None,
    ):
        if not (isinstance(mask, Index) and mask.dtype == np.dtype(np.uint8)):
            raise TypeError(
                "{0} 'mask' must be an Index with dtype=uint8, not {1}".format(
                    type(self).__name__, repr(mask)
                )
            )
        if not isinstance(content, Content):
            raise TypeError(
                "{0} 'content' must be a Content subtype, not {1}".format(
                    type(self).__name__, repr(content)
                )
            )
        if not isinstance(valid_when, bool):
            raise TypeError(
                "{0} 'valid_when' must be boolean, not {1}".format(
                    type(self).__name__, repr(valid_when)
                )
            )
        if not ak._util.isint(length):
            raise TypeError(
                "{0} 'length' must be an integer, not {1}".format(
                    type(self).__name__, repr(length)
                )
            )
        if not isinstance(lsb_order, bool):
            raise TypeError(
                "{0} 'lsb_order' must be boolean, not {1}".format(
                    type(self).__name__, repr(lsb_order)
                )
            )
        if not length <= len(mask) * 8:
            raise ValueError(
                "{0} 'length' ({1}) must be <= len(mask) * 8 ({2})".format(
                    type(self).__name__, length, len(mask) * 8
                )
            )
        if not length <= len(content):
            raise ValueError(
                "{0} 'length' ({1}) must be <= len(content) ({2})".format(
                    type(self).__name__, length, len(content)
                )
            )

        self._mask = mask
        self._content = content
        self._valid_when = valid_when
        self._length = length
        self._lsb_order = lsb_order
        self._init(identifier, parameters)

    @property
    def mask(self):
        return self._mask

    @property
    def content(self):
        return self._content

    @property
    def valid_when(self):
        return self._valid_when

    @property
    def lsb_order(self):
        return self._lsb_order

    @property
    def nplike(self):
        return self._mask.nplike

    Form = BitMaskedForm

    @property
    def form(self):
        return self.Form(
            self._mask.form,
            self._content.form,
            self._valid_when,
            self._lsb_order,
            has_identifier=self._identifier is not None,
            parameters=self._parameters,
            form_key=None,
        )

    def __len__(self):
        return self._length

    def __repr__(self):
        return self._repr("", "", "")

    def _repr(self, indent, pre, post):
        out = [indent, pre, "<BitMaskedArray len="]
        out.append(repr(str(len(self))))
        out.append(" valid_when=")
        out.append(repr(str(self._valid_when)))
        out.append(" lsb_order=")
        out.append(repr(str(self._lsb_order)))
        out.append(">\n")
        out.append(self._mask._repr(indent + "    ", "<mask>", "</mask>\n"))
        out.append(self._content._repr(indent + "    ", "<content>", "</content>\n"))
        out.append(indent)
        out.append("</BitMaskedArray>")
        out.append(post)
        return "".join(out)

    def bytemask(self):
        nplike = self._mask.nplike
        bytemask = ak._v2.index.Index8.empty(len(self._mask) * 8, nplike)
        self._handle_error(
            nplike[
                "awkward_BitMaskedArray_to_ByteMaskedArray",
                bytemask.dtype.type,
                self._mask.dtype.type,
            ](
                bytemask.to(nplike),
                self._mask.to(nplike),
                len(self._mask),
                self._valid_when,
                self._lsb_order,
            )
        )
        return bytemask.data[: self._length]

    def toByteMaskedArray(self):
        nplike = self._mask.nplike
        bytemask = ak._v2.index.Index8.empty(len(self._mask) * 8, nplike)
        self._handle_error(
            nplike[
                "awkward_BitMaskedArray_to_ByteMaskedArray",
                bytemask.dtype.type,
                self._mask.dtype.type,
            ](
                bytemask.to(nplike),
                self._mask.to(nplike),
                len(self._mask),
                False,  # this differs from the kernel call in 'bytemask'
                self._lsb_order,
            )
        )
        return ByteMaskedArray(
            bytemask[: self._length],
            self._content,
            self._valid_when,
            self._identifier,
            self._parameters,
        )

    def _getitem_nothing(self):
        return self._content._getitem_range(slice(0, 0))

    def _getitem_at(self, where):
        if where < 0:
            where += len(self)
        if not (0 <= where < len(self)):
            raise NestedIndexError(self, where)
        if self._lsb_order:
            bit = bool(self._mask[where // 8] & (1 << (where % 8)))
        else:
            bit = bool(self._mask[where // 8] & (128 >> (where % 8)))
        if bit == self._valid_when:
            return self._content._getitem_at(where)
        else:
            return None

    def _getitem_range(self, where):
        return self.toByteMaskedArray()._getitem_range(where)

    def _getitem_field(self, where, only_fields=()):
        return BitMaskedArray(
            self._mask,
            self._content._getitem_field(where, only_fields),
            self._valid_when,
            self._length,
            self._lsb_order,
            self._field_identifier(where),
            None,
        )

    def _getitem_fields(self, where, only_fields=()):
        return BitMaskedArray(
            self._mask,
            self._content._getitem_fields(where, only_fields),
            self._valid_when,
            self._length,
            self._lsb_order,
            self._fields_identifier(where),
            None,
        )

    def _carry(self, carry, allow_lazy, exception):
        assert isinstance(carry, ak._v2.index.Index)

        return self.toByteMaskedArray()._carry(carry, allow_lazy, exception)

    def _getitem_next(self, head, tail, advanced):
        nplike = self.nplike  # noqa: F841

        if head == ():
            return self

        elif isinstance(head, (int, slice, ak._v2.index.Index64)):
            return self.toByteMaskedArray()._getitem_next(head, tail, advanced)

        elif ak._util.isstr(head):
            return self._getitem_next_field(head, tail, advanced)

        elif isinstance(head, list):
            return self._getitem_next_fields(head, tail, advanced)

        elif head is np.newaxis:
            return self._getitem_next_newaxis(tail, advanced)

        elif head is Ellipsis:
            return self._getitem_next_ellipsis(tail, advanced)

        elif isinstance(head, ak._v2.contents.ListOffsetArray):
            raise NotImplementedError

        elif isinstance(head, ak._v2.contents.IndexedOptionArray):
            raise NotImplementedError

        else:
            raise AssertionError(repr(head))
