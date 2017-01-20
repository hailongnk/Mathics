#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from mathics.builtin.base import Builtin
from mathics.core.expression import Expression, Integer, Symbol
from mathics.core.convert import from_sympy, sympy_symbol_prefix

import sympy
# import mpmath
# from six.moves import range

def sympy_factor(expr_sympy):
    try:
        result = sympy.together(expr_sympy)
        numer, denom = result.as_numer_denom()
        if denom == 1:
            result = sympy.factor(expr_sympy)
        else:
            result = sympy.factor(numer) / sympy.factor(denom)
    except sympy.PolynomialError:
        return expr_sympy
    return result

def cancel(expr):
    if expr.has_form('Plus', None):
        return Expression('Plus', *[cancel(leaf) for leaf in expr.leaves])
    else:
        try:
            result = expr.to_sympy()
            if result is None:
                return None

            # result = sympy.powsimp(result, deep=True)
            result = sympy.cancel(result)

            # cancel factors out rationals, so we factor them again
            result = sympy_factor(result)

            return from_sympy(result)
        except sympy.PolynomialError:
            # e.g. for non-commutative expressions
            return expr

class ExtraTogether(Builtin):
    """
    <dl>
    <dt>'ExtraTogether[$expr$]'
        <dd>writes sums of fractions in $expr$ together.
    </dl>

    >> ExtraTogether[a / c + b / c]
     = (a + b) / c
    'ExtraTogether' operates on lists:
    >> ExtraTogether[{x / (y+1) + x / (y+1)^2}]
     = {x (2 + y) / (1 + y) ^ 2}
    But it does not touch other functions:
    >> ExtraTogether[f[a / c + b / c]]
     = f[a / c + b / c]

    #> f[x]/x+f[x]/x^2//ExtraTogether
     = f[x] (1 + x) / x ^ 2
    """

    attributes = ['Listable']

    def apply_2(self, expr, evaluation):
        'ExtraTogether[expr_]'
        print("Calling apply_2")
        expr_sympy = expr.to_sympy()
        if expr_sympy is None:
            return None
        result = sympy.together(expr_sympy)
        result = from_sympy(result)
        result = cancel(result)
        return result

    def apply_3(self, expr, cond, evaluation):
        'ExtraTogether[expr_, cond_]'
        print("Calling apply_3")
        return None

