# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

import awkward as ak
from awkward._v2.index import Index
from awkward._v2.contents.content import Content, NestedIndexError
from awkward._v2.forms.unionform import UnionForm

np = ak.nplike.NumpyMetadata.instance()


class UnionArray(Content):
    def __init__(self, tags, index, contents, identifier=None, parameters=None):
        if not (isinstance(tags, Index) and tags.dtype == np.dtype(np.int8)):
            raise TypeError(
                "{0} 'tags' must be an Index with dtype=int8, not {1}".format(
                    type(self).__name__, repr(tags)
                )
            )
        if not isinstance(index, Index) and index.dtype in (
            np.dtype(np.int32),
            np.dtype(np.uint32),
            np.dtype(np.int64),
        ):
            raise TypeError(
                "{0} 'index' must be an Index with dtype in (int32, uint32, int64), "
                "not {1}".format(type(self).__name__, repr(index))
            )

        if not isinstance(contents, Iterable):
            raise TypeError(
                "{0} 'contents' must be iterable, not {1}".format(
                    type(self).__name__, repr(contents)
                )
            )
        if not isinstance(contents, list):
            contents = list(contents)

        for content in contents:
            if not isinstance(content, Content):
                raise TypeError(
                    "{0} all 'contents' must be Content subclasses, not {1}".format(
                        type(self).__name__, repr(content)
                    )
                )

        if not len(tags) <= len(index):
            raise ValueError(
                "{0} len(tags) ({1}) must be <= len(index) ({2})".format(
                    type(self).__name__, len(tags), len(index)
                )
            )

        self._tags = tags
        self._index = index
        self._contents = contents
        self._init(identifier, parameters)

    @property
    def tags(self):
        return self._tags

    @property
    def index(self):
        return self._index

    def content(self, index):
        return self._contents[index]

    @property
    def contents(self):
        return self._contents

    @property
    def nplike(self):
        return self._tags.nplike

    Form = UnionForm

    @property
    def form(self):
        return self.Form(
            self._tags.form,
            self._index.form,
            [x.form for x in self._contents],
            has_identifier=self._identifier is not None,
            parameters=self._parameters,
            form_key=None,
        )

    def __len__(self):
        return len(self._tags)

    def __repr__(self):
        return self._repr("", "", "")

    def _repr(self, indent, pre, post):
        out = [indent, pre, "<UnionArray len="]
        out.append(repr(str(len(self))))
        out.append(">\n")
        out.append(self._tags._repr(indent + "    ", "<tags>", "</tags>\n"))
        out.append(self._index._repr(indent + "    ", "<index>", "</index>\n"))
        for i, x in enumerate(self._contents):
            out.append("{0}    <content index={1}>\n".format(indent, repr(str(i))))
            out.append(x._repr(indent + "        ", "", "\n"))
            out.append("{0}    </content>\n".format(indent))
        out.append(indent)
        out.append("</UnionArray>")
        out.append(post)
        return "".join(out)

    def _getitem_nothing(self):
        return self._getitem_range(slice(0, 0))

    def _getitem_at(self, where):
        if where < 0:
            where += len(self)
        if not (0 <= where < len(self)):
            raise NestedIndexError(self, where)
        tag, index = self._tags[where], self._index[where]
        return self._contents[tag]._getitem_at(index)

    def _getitem_range(self, where):
        start, stop, step = where.indices(len(self))
        assert step == 1
        return UnionArray(
            self._tags[start:stop],
            self._index[start:stop],
            self._contents,
            self._range_identifier(start, stop),
            self._parameters,
        )

    def _getitem_field(self, where, only_fields=()):
        return UnionArray(
            self._tags,
            self._index,
            [x._getitem_field(where, only_fields) for x in self._contents],
            self._field_identifier(where),
            None,
        )

    def _getitem_fields(self, where, only_fields=()):
        return UnionArray(
            self._tags,
            self._index,
            [x._getitem_fields(where, only_fields) for x in self._contents],
            self._fields_identifer(where),
            None,
        )

    def _carry(self, carry, allow_lazy, exception):
        assert isinstance(carry, ak._v2.index.Index)

        try:
            nexttags = self._tags[carry.data]
            nextindex = self._index[: len(self._tags)][carry.data]
        except IndexError as err:
            if issubclass(exception, NestedIndexError):
                raise exception(self, carry.data, str(err))
            else:
                raise exception(str(err))

        return UnionArray(
            nexttags,
            nextindex,
            self._contents,
            self._carry_identifier(carry, exception),
            self._parameters,
        )

    def _project(self, index):
        nplike = self.nplike
        lentags = len(self._tags)
        assert len(self._index) == lentags
        lenout = ak._v2.index.Index64.empty(1, nplike)
        tmpcarry = ak._v2.index.Index64.empty(lentags, nplike)
        self._handle_error(
            nplike[
                "awkward_UnionArray_project",
                lenout.dtype.type,
                tmpcarry.dtype.type,
                self._tags.dtype.type,
                self._index.dtype.type,
            ](
                lenout.to(nplike),
                tmpcarry.to(nplike),
                self._tags.to(nplike),
                self._index.to(nplike),
                lentags,
                index,
            )
        )
        nextcarry = ak._v2.index.Index64(tmpcarry.data[: lenout[0]], nplike)
        return self._contents[index]._carry(nextcarry, False, NestedIndexError)

    def _regular_index(self, tags):
        nplike = self.nplike
        lentags = len(tags)
        size = ak._v2.index.Index64.empty(1, nplike)
        self._handle_error(
            nplike[
                "awkward_UnionArray_regular_index_getsize",
                size.dtype.type,
                tags.dtype.type,
            ](
                size.to(nplike),
                tags.to(nplike),
                lentags,
            )
        )
        current = ak._v2.index.Index64.empty(size[0], nplike)
        outindex = ak._v2.index.Index64.empty(lentags, nplike)
        self._handle_error(
            nplike[
                "awkward_UnionArray_regular_index",
                outindex.dtype.type,
                current.dtype.type,
                tags.dtype.type,
            ](
                outindex.to(nplike),
                current.to(nplike),
                size[0],
                tags.to(nplike),
                lentags,
            )
        )
        return outindex

    def _getitem_next(self, head, tail, advanced):
        nplike = self.nplike  # noqa: F841

        if head == ():
            return self

        elif isinstance(head, (int, slice, ak._v2.index.Index64)):
            outcontents = []
            for i in range(len(self._contents)):
                projection = self._project(i)
                outcontents.append(projection._getitem_next(head, tail, advanced))
            outindex = self._regular_index(self._tags)

            out = UnionArray(
                self._tags,
                outindex,
                outcontents,
                self._identifier,
                self._parameters,
            )
            return out._simplify_uniontype()

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
