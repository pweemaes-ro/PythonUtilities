"""Simulation of MRO generation in Python since 2.3 (C3 linearization). For
   readability, class.__names__'s are used to represent the classes.
"""
from typing import Any


def _merge(lists: list[list[Any]]) -> list[Any]:
    """Return C3 linearization or [] if inconsistent. """
    _inconsistency_detected = False

    def __merge(_lists: list[list[Any]]):
        """Return C3 linearization or [] if inconsistent.
        """
        _result: list[Any] = []

        nonlocal _inconsistency_detected
        if _inconsistency_detected:
            return _result

        for lst in _lists:
            if len(lst) and not any(lst[0] in any_list[1::]
                                    for any_list in _lists
                                    if any_list is not lst):
                # we have a head that's not in any other list's tail.
                _result = [_head := lst[0]]   # Append head of lst to result
                for any_list in _lists:       # Remove head of lst in any lists
                    if _head in any_list:
                        any_list.remove(_head)
                break
        else:  # No break in for-loop, so nothing removed, so we're stuck!
            _inconsistency_detected = True
            return _result

        if any(len(lst) for lst in _lists):  # lists not empty, more to merge.
            _result += __merge(_lists)

        return [] if _inconsistency_detected else _result

    return __merge(lists)


def mro(cls: Any) -> list[Any]:
    """Return cls C3 linearization (or [] if inconsistent)."""
    expanded = [[cls.__name__]]
    bases_list = []

    for base in cls.__bases__:
        expanded += [mro(base)]
        bases_list.append(base.__name__)
    expanded.append(bases_list)

    return _merge(expanded)


if __name__ == '__main__':

    def _get_python_mro(cls):
        """Return a list of all __name__'s of classes in cls's __mro__, that
           is, the Python (2.3 and up) linearization).
        """
        return [item.__name__ for item in cls.__mro__]

    def _test_complex():
        # a very complex (whaaah...) example:

        class C:
            """Class with only object as base"""
            pass

        class A:
            """Class with only object as base"""
            pass

        class B:
            """Class with only object as base"""
            pass

        class D:
            """Class with only object as base"""
            pass

        class E:
            """Class with only object as base"""
            pass

        class K1(C, A, B):
            """Class with C, A, B as bases"""
            pass

        class K3(A, D):
            """Class with A, D as bases"""
            pass

        class K2(B, D, E):
            """Class with B, D, E as bases"""
            pass

        class Z(K1, K3, K2):
            """Class with K1, K3, K2 as bases"""
            pass

        for x in (A, B, C, D, E, K1, K2, K3, Z):
            assert mro(x) == _get_python_mro(x)

        print("test complex: ok")

    def _test_simple():
        """A simple example."""
        class A:
            """class with object as its only base"""
            pass

        class B:
            """class with object as its only base"""
            pass

        class C(B, A):
            """class with B and A as its bases"""
            pass

        class D(C, B):
            """class with C and B as its bases"""
            pass

        for x in (object, A, B, C, D):
            assert mro(x) == _get_python_mro(x)
        print("test simple: ok")

    def _test_inconsistent():
        # There is no way to test the linearization of classes with
        # inconsistent mro, since Python will not allow such classes.
        # The _merge function however allows for testing lists of strings
        # representing class names, even if they result in inconsistent
        # mro (_merge will return [] in such cases).
        pass

    def _test_linearization():
        _test_simple()
        _test_complex()

    # noinspection SpellCheckingInspection
    def _test_merge():
        # X cannot precede Y in one linearization and NOT precede it in
        # another, so the following is inconsistent:
        assert _merge([['X', 'Y', 'O'], ['Y', 'X', 'O']]) == []

        # The following also represents an inconsistent mro:
        # - X and Y derive from O
        # - A derives (in order) from X and Y
        # - B derives (in order) from Y and X
        # - C derives (in order) from A and B
        # Y is in the tail of X, and cannot be taken out...
        # X is in the tail of Y, and connot be taken out...
        # We end up with a non empty reduced list that cannot be further
        # reduced: [['X', 'Y', 'O'], ['Y', 'X', 'O']].
        assert _merge([['A', 'X', 'Y', 'O'],
                       ['B', 'Y', 'X', 'O'],
                       ['A', 'B']]) == []
        assert ['A'] + _merge([['B', 'D', 'E', 'O'],
                               ['C', 'D', 'F', 'O'],
                               ['B', 'C']]) == \
               ['A', 'B', 'C', 'D', 'E', 'F', 'O']
        print("test merge: ok")

    _test_linearization()
    _test_merge()
