"""
Generic curves.
"""

from sage.categories.finite_fields import FiniteFields
from sage.categories.fields import Fields
from sage.misc.all import latex

from sage.schemes.generic.algebraic_scheme import AlgebraicScheme_subscheme

from sage.schemes.generic.divisor_group import DivisorGroup

from sage.schemes.generic.divisor import Divisor_curve

class Curve_generic(AlgebraicScheme_subscheme):
    r"""
    Generic curve class.

    EXAMPLES::

        sage: A.<x,y,z> = AffineSpace(QQ,3)
        sage: C = Curve([x-y,z-2])
        sage: loads(C.dumps()) == C
        True
    """

    def _repr_(self):
        """
        Return a string representation of this curve.

        EXAMPLES::

            sage: A.<x,y,z> = AffineSpace(QQ,3)
            sage: C = Curve([x-y,z-2])
            sage: C
            Affine Curve over Rational Field defined by x - y, z - 2

            sage: P.<x,y,z> = ProjectiveSpace(QQ,2)
            sage: C = Curve(x-y)
            sage: C
            Projective Plane Curve over Rational Field defined by x - y
        """
        return "%s Curve over %s defined by %s"%(
            self._repr_type(), self.base_ring(), ', '.join([str(x) for x in self.defining_polynomials()]))

    def _repr_type(self):
        r"""
        Return a string representation of the type of this curve.

        EXAMPLES::

            sage: P.<x,y,z,w> = ProjectiveSpace(QQ, 3)
            sage: C = Curve([w^3 - z^3, w*x - x^2])
            sage: from sage.schemes.curves.curve import Curve_generic
            sage: Curve_generic._repr_type(C)
            'Generic'
        """
        return "Generic"

    def _latex_(self):
        """
        Return a latex representation of this curve.

        EXAMPLES::

            sage: x,y,z = PolynomialRing(QQ, 3, names='x,y,z').gens()
            sage: C = Curve(y^2*z - x^3 - 17*x*z^2 + y*z^2)
            sage: latex(C)
            - x^{3} + y^{2} z - 17 x z^{2} + y z^{2}

            sage: A2 = AffineSpace(2, QQ, names=['x','y'])
            sage: x, y = A2.coordinate_ring().gens()
            sage: C = Curve(y^2 - x^3 - 17*x + y)
            sage: latex(C)
            - x^{3} + y^{2} - 17 x + y
        """
        return latex(self.defining_polynomial())

    def defining_polynomial(self):
        """
        Return the defining polynomial of the curve.

        EXAMPLES::

            sage: x,y,z = PolynomialRing(QQ, 3, names='x,y,z').gens()
            sage: C = Curve(y^2*z - x^3 - 17*x*z^2 + y*z^2)
            sage: C.defining_polynomial()
            -x^3 + y^2*z - 17*x*z^2 + y*z^2
        """
        return self.defining_polynomials()[0]

    def divisor_group(self, base_ring=None):
        r"""
        Return the divisor group of the curve.

        INPUT:

        - ``base_ring`` -- the base ring of the divisor
          group. Usually, this is `\ZZ` (default) or `\QQ`.

        OUTPUT:

        The divisor group of the curve.

        EXAMPLES::

            sage: x,y,z = PolynomialRing(QQ, 3, names='x,y,z').gens()
            sage: C  = Curve(y^2*z - x^3 - 17*x*z^2 + y*z^2)
            sage: Cp = Curve(y^2*z - x^3 - 17*x*z^2 + y*z^2)
            sage: C.divisor_group() is Cp.divisor_group()
            True
        """
        return DivisorGroup(self, base_ring)

    def divisor(self, v, base_ring=None, check=True, reduce=True):
        r"""
        Return the divisor specified by ``v``.

        .. WARNING::

            The coefficients of the divisor must be in the base ring
            and the terms must be reduced. If you set ``check=False``
            and/or ``reduce=False`` it is your responsibility to pass
            a valid object ``v``.
        """
        return Divisor_curve(v, check=check, reduce=reduce, parent=self.divisor_group(base_ring))

    def genus(self):
        """
        The geometric genus of the curve.
        """
        return self.geometric_genus()

    def geometric_genus(self):
        r"""
        Return the geometric genus of the curve.

        This is by definition the
        genus of the normalization of the projective closure of the
        curve over the algebraic closure of the base field; the base
        field must be a prime field.

        .. NOTE::

            This calls Singular's genus command.

        EXAMPLE:

        Examples of projective curves. ::

            sage: P2 = ProjectiveSpace(2, GF(5), names=['x','y','z'])
            sage: x, y, z = P2.coordinate_ring().gens()
            sage: C = Curve(y^2*z - x^3 - 17*x*z^2 + y*z^2)
            sage: C.geometric_genus()
                  1
            sage: C = Curve(y^2*z - x^3)
            sage: C.geometric_genus()
                  0
            sage: C = Curve(x^10 + y^7*z^3 + z^10)
            sage: C.geometric_genus()
                  3

        Examples of affine curves. ::

            sage: x, y = PolynomialRing(GF(5), 2, 'xy').gens()
            sage: C = Curve(y^2 - x^3 - 17*x + y)
            sage: C.geometric_genus()
            1
            sage: C = Curve(y^2 - x^3)
            sage: C.geometric_genus()
            0
            sage: C = Curve(x^10 + y^7 + 1)
            sage: C.geometric_genus()
            3

        """
        try:
            return self.__genus
        except AttributeError:
            self.__genus = self.defining_ideal().genus()
            return self.__genus

    def union(self, other):
        """
        Return the union of ``self`` and ``other``.

        EXAMPLES::

            sage: x,y,z = PolynomialRing(QQ, 3, names='x,y,z').gens()
            sage: C1 = Curve(z - x)
            sage: C2 = Curve(y - x)
            sage: C1.union(C2).defining_polynomial()
            x^2 - x*y - x*z + y*z
        """
        from constructor import Curve
        return Curve(AlgebraicScheme_subscheme.union(self, other))

    __add__ = union

    def singular_subscheme(self):
        r"""
        Return the subscheme of singular points of this curve.

        OUTPUT:

        - a subscheme in the ambient space of this curve.

        EXAMPLES::

            sage: A.<x,y> = AffineSpace(CC, 2)
            sage: C = Curve([y^4 - 2*x^5 - x^2*y], A)
            sage: C.singular_subscheme()
            Closed subscheme of Affine Space of dimension 2 over Complex Field with
            53 bits of precision defined by:
              (-2.00000000000000)*x^5 + y^4 - x^2*y,
              (-10.0000000000000)*x^4 + (-2.00000000000000)*x*y,
              4.00000000000000*y^3 - x^2

        ::

            sage: P.<x,y,z,w> = ProjectiveSpace(QQ, 3)
            sage: C = Curve([y^8 - x^2*z*w^5, w^2 - 2*y^2 - x*z], P)
            sage: C.singular_subscheme()
            Closed subscheme of Projective Space of dimension 3 over Rational Field
            defined by:
              y^8 - x^2*z*w^5,
              -2*y^2 - x*z + w^2,
              -x^3*y*z^4 + 3*x^2*y*z^3*w^2 - 3*x*y*z^2*w^4 + 8*x*y*z*w^5 + y*z*w^6,
              x^2*z*w^5,
              -5*x^2*z^2*w^4 - 4*x*z*w^6,
              x^4*y*z^3 - 3*x^3*y*z^2*w^2 + 3*x^2*y*z*w^4 - 4*x^2*y*w^5 - x*y*w^6,
              -2*x^3*y*z^3*w + 6*x^2*y*z^2*w^3 - 20*x^2*y*z*w^4 - 6*x*y*z*w^5 +
            2*y*w^7,
              -5*x^3*z*w^4 - 2*x^2*w^6
        """
        return self.ambient_space().subscheme(self.Jacobian())

    def singular_points(self, F=None):
        r"""
        Return the set of singular points of this curve.

        INPUT:

        - ``F`` -- (default: None) field over which to find the singular points. If not given,
          the base ring of this curve is used.

        OUTPUT:

        - a list of points in the ambient space of this curve.

        EXAMPLES::

            sage: A.<x,y,z> = AffineSpace(QQ, 3)
            sage: C = Curve([y^2 - x^5, x - z], A)
            sage: C.singular_points()
            [(0, 0, 0)]

        ::

            sage: R.<a> = QQ[]
            sage: K.<b> = NumberField(a^8 - a^4 + 1)
            sage: P.<x,y,z> = ProjectiveSpace(QQ, 2)
            sage: C = Curve([359/12*x*y^2*z^2 + 2*y*z^4 + 187/12*y^3*z^2 + x*z^4\
            + 67/3*x^2*y*z^2 + 117/4*y^5 + 9*x^5 + 6*x^3*z^2 + 393/4*x*y^4\
            + 145*x^2*y^3 + 115*x^3*y^2 + 49*x^4*y], P)
            sage: C.singular_points(K)
            [(1/2*b^5 + 1/2*b^3 - 1/2*b - 1 : 1 : 0), (-2/3*b^4 + 1/3 : 0 : 1),
            (2/3*b^4 - 1/3 : 0 : 1), (b^6 : -b^6 : 1), (-b^6 : b^6 : 1),
            (-1/2*b^5 - 1/2*b^3 + 1/2*b - 1 : 1 : 0)]
        """
        if F is None:
            if not self.base_ring() in Fields():
                raise TypeError("curve must be defined over a field")
        elif not F in Fields():
            raise TypeError("(=%s) must be a field"%F)
        X = self.singular_subscheme()
        return X.rational_points(F=F)

    def is_singular(self, P=None):
        r"""
        Return whether ``P`` is a singular point of this curve, or if no point is passed,
        whether this curve is singular or not.

        This just uses the is_smooth function for algebraic subschemes.

        INPUT:

        - ``P`` -- (default: None) a point on this curve.

        OUTPUT:

        - Boolean. If a point ``P`` is provided, and if ``P`` lies on this curve, returns True
          if ``P`` is a singular point of this curve, and False otherwise. If no point is provided,
          returns True or False depending on whether this curve is or is not singular, respectively.

        EXAMPLES::

            sage: P.<x,y,z,w> = ProjectiveSpace(QQ, 3)
            sage: C = P.curve([y^2 - x^2 - z^2, z - w])
            sage: C.is_singular()
            False

        ::

            sage: A.<x,y,z> = AffineSpace(GF(11), 3)
            sage: C = A.curve([y^3 - z^5, x^5 - y + 1])
            sage: Q = A([7,0,0])
            sage: C.is_singular(Q)
            True
        """
        return not self.is_smooth(P)

    def intersects_at(self, C, P):
        r"""
        Return whether the point ``P`` is or is not in the intersection of this curve with the curve ``C``.

        INPUT:

        - ``C`` -- a curve in the same ambient space as this curve.

        - ``P`` -- a point in the ambient space of this curve.

        OUTPUT:

        Boolean.

        EXAMPLES::

            sage: P.<x,y,z,w> = ProjectiveSpace(QQ, 3)
            sage: C = Curve([x^2 - z^2, y^3 - w*x^2], P)
            sage: D = Curve([w^2 - 2*x*y + z^2, y^2 - w^2], P)
            sage: Q1 = P([1,1,-1,1])
            sage: C.intersects_at(D, Q1)
            True
            sage: Q2 = P([0,0,1,-1])
            sage: C.intersects_at(D, Q2)
            False

        ::

            sage: A.<x,y> = AffineSpace(GF(13), 2)
            sage: C = Curve([y + 12*x^5 + 3*x^3 + 7], A)
            sage: D = Curve([y^2 + 7*x^2 + 8], A)
            sage: Q1 = A([9,6])
            sage: C.intersects_at(D, Q1)
            True
            sage: Q2 = A([3,7])
            sage: C.intersects_at(D, Q2)
            False
        """
        if C.ambient_space() != self.ambient_space():
            raise TypeError("(=%s) must be a curve in the same ambient space as (=%s)"%(C,self))
        if not isinstance(C, Curve_generic):
            raise TypeError("(=%s) must be a curve"%C)
        try:
            P = self.ambient_space()(P)
        except TypeError:
            raise TypeError("(=%s) must be a point in the ambient space of this curve"%P)
        try:
            P = self(P)
            P = C(P)
        except TypeError:
            return False
        return True

    def intersection_points(self, C, F=None):
        r"""
        Return the points in the intersection of this curve and the curve ``C``.

        If the intersection of these two curves has dimension greater than zero, and if
        the base ring of this curve is not a finite field, then an error is returned.

        INPUT:

        - ``C`` -- a curve in the same ambient space as this curve.

        - ``F`` -- (default: None). Field over which to compute the intersection points. If not specified,
          the base ring of this curve is used.

        OUTPUT:

        - a list of points in the ambient space of this curve.

        EXAMPLES::

            sage: R.<a> = QQ[]
            sage: K.<b> = NumberField(a^2 + a + 1)
            sage: P.<x,y,z,w> = ProjectiveSpace(QQ, 3)
            sage: C = Curve([y^2 - w*z, w^3 - y^3], P)
            sage: D = Curve([x*y - w*z, z^3 - y^3], P)
            sage: C.intersection_points(D, F=K)
            [(-b - 1 : -b - 1 : b : 1), (b : b : -b - 1 : 1), (1 : 1 : 1 : 1)]

        ::

            sage: A.<x,y> = AffineSpace(GF(7), 2)
            sage: C = Curve([y^3 - x^3], A)
            sage: D = Curve([-x*y^3 + y^4 - 2*x^3 + 2*x^2*y], A)
            sage: C.intersection_points(D)
            [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 3), (5, 5), (5, 6), (6, 6)]

        ::

            sage: A.<x,y> = AffineSpace(QQ, 2)
            sage: C = Curve([y^3 - x^3], A)
            sage: D = Curve([-x*y^3 + y^4 - 2*x^3 + 2*x^2*y], A)
            sage: C.intersection_points(D)
            Traceback (most recent call last):
            ...
            NotImplementedError: the intersection must have dimension zero or
            (=Rational Field) must be a finite field
        """
        if C.ambient_space() != self.ambient_space():
            raise TypeError("(=%s) must be a curve in the same ambient space as (=%s)"%(C,self))
        if not isinstance(C, Curve_generic):
            raise TypeError("(=%s) must be a curve"%C)
        X = self.intersection(C)
        if F is None:
            F = self.base_ring()
        if X.dimension() == 0 or F in FiniteFields():
            return X.rational_points(F=F)
        else:
            raise NotImplementedError("the intersection must have dimension zero or (=%s) must be a finite field"%F)
