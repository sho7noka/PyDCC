# -*- coding: utf-8 -*-
from yurlungur.core.env import Blender, Numpy
from yurlungur.core.wrapper import _YVector, _YMatrix, _YColors


class Vector(_YVector):
    __slots__ = ('__data',)
    __hash__ = None

    def __init__(self, *args, **kwargs):
        if Blender():
            super(Vector, self).__init__()
            self.vector = [self.x, self.y, self.z]
        else:
            super(Vector, self).__init__(*args, **kwargs)
            self.vector = args

    def __new__(cls, *args):
        if len(args) is 1:
            v = args[0]
            if hasattr(v, '_Vector__data'):
                return _newV(_MP(v.__data), cls)
        try:
            return _newV(_MP(*args), cls)
        except:
            raise ValueError(cls.__name__ + ' : not matching constructor found.')

    def __reduce__(self):
        return type(self), tuple(self.__data)

    def __repr__(self):
        if self.__data[3] == 1.:
            return '%s(%f, %f, %f)' % (type(self).__name__, self.__data[0], self.__data[1], self.__data[2])
        return '%s(%f, %f, %f, %f)' % ((type(self).__name__,) + tuple(self.__data))

    def __str__(self):
        if self.__data[3] == 1.:
            return '(%f, %f, %f)' % (self.__data[0], self.__data[1], self.__data[2])
        return '(%f, %f, %f, %f)' % tuple(self.__data)

    def __len__(self):
        return 3 if self.__data[3] == 1. else 4

    def __getitem__(self, i):
        if 0 <= i < 3 or (i == 3 and self.__data[3] != 1.):
            return self.__data[i]
        raise IndexError('Vector index out of range.')

    def __setitem__(self, i, v):
        if 0 <= i < 4:
            self.__data[i] = v
        raise IndexError('Vector index out of range.')

    def __getattr__(self, k):
        try:
            return getattr(self.__data, k)
        except:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, k))

    def __setattr__(self, k, v):
        try:
            return setattr(self.__data, k, v)
        except:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, k))

    def __eq__(self, v):
        try:
            return self.__data == v.__data
        except:
            return False

    def __ne__(self, v):
        try:
            return self.__data != v.__data
        except:
            return True

    def __neg__(self):
        d = self.__data
        return _newV(_MP(-d[0], -d[1], -d[2], d[3]))

    def __add__(self, v):
        try:
            d = self.__data
            s = v.__data
            return _newV(_MP(d[0] + s[0], d[1] + s[1], d[2] + s[2], d[3]))
        except:
            raise ValueError("%s + %r" % (type(self).__name__, v))

    def __iadd__(self, v):
        try:
            d = self.__data
            s = v.__data
            d[0] += s[0]
            d[1] += s[1]
            d[2] += s[2]
        except:
            raise ValueError("%s += %r" % (type(self).__name__, v))
        return self

    def __sub__(self, v):
        try:
            d = self.__data
            s = v.__data
            return _newV(_MP(d[0] - s[0], d[1] - s[1], d[2] - s[2], d[3]))
        except:
            raise ValueError("%s - %r" % (type(self).__name__, v))

    def __isub__(self, v):
        try:
            d = self.__data
            s = v.__data
            d[0] -= s[0]
            d[1] -= s[1]
            d[2] -= s[2]
        except:
            raise ValueError("%s -= %r" % (type(self).__name__, v))
        return self

    def __mul__(self, v):
        if hasattr(v, '_Matrix__data'):
            return _newV(self.__data * v._Matrix__data)
        elif hasattr(v, '_Quaternion__data'):
            v = _MV(self.__data).rotateBy(v._Quaternion__data)
            return _newV(_MP(v[0], v[1], v[2], self.__data[3]))
        elif isinstance(v, Number):
            return _newV(self.__data * v)
        else:
            try:
                d = self.__data
                s = v.__data
                return d[0] * s[0] + d[1] * s[1] + d[2] * s[2]
            except:
                raise ValueError("%s * %r" % (type(self).__name__, v))

    def __imul__(self, v):
        if hasattr(v, '_Matrix__data'):
            self.__data *= v._Matrix__data
        elif hasattr(v, '_Quaternion__data'):
            d = self.__data
            v = _MV(d).rotateBy(v._Quaternion__data)
            d[0] = v[0]
            d[1] = v[1]
            d[2] = v[2]
        else:
            try:
                self.__data *= v
            except:
                raise ValueError("%s *= %r" % (type(self).__name__, v))
        return self

    def __rmul__(self, v):
        try:
            return _newV(self.__data * v)  # MPoint のスカラー倍は __mul__ のみ。
        except:
            raise ValueError("%r * %s" % (v, type(self).__name__))

    def __div__(self, v):
        try:
            return _newV(self.__data / v)
        except:
            raise ValueError("%s / %r" % (type(self).__name__, v))

    def __idiv__(self, v):
        try:
            self.__data /= v
        except:
            raise ValueError("%s /= %r" % (type(self).__name__, v))
        return self

    def __rdiv__(self, v):
        try:
            d = self.__data
            return _newV(_MP(v / d[0], v / d[1], v / d[2], d[3]))
        except:
            raise ValueError("%r / %s" % (v, type(self).__name__))

    def __xor__(self, v):
        try:
            v = _MV(self.__data) ^ _MV(v.__data)
            return _newV(_MP(v[0], v[1], v[2], self.__data[3]))
        except:
            raise ValueError("%s ^ %r" % (type(self).__name__, v))

    def __ixor__(self, v):
        try:
            d = self.__data
            v = _MV(d) ^ _MV(v.__data)
            d[0] = v[0]
            d[1] = v[1]
            d[2] = v[2]
        except:
            raise ValueError("%s ^= %r" % (type(self).__name__, v))
        return self

    def __abs__(self):
        v = self.__data
        return _newV(_MP(abs(v[0]), abs(v[1]), abs(v[2]), abs(v[3])))

    def isEquivalent(self, v, tol=_TOLERANCE):
        u"""
        ほぼ同値かどうか。

        :type v: `Vector`
        :param v: 比較するベクトル。
        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        try:
            return self.__data.isEquivalent(v.__data, tol)
        except:
            return False

    def isZero(self, tol=_TOLERANCE):
        u"""
        ほぼゼロかどうか。

        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        return self.__data.isEquivalent(_MP_Zero, tol)

    def isParallel(self, v, tol=_TOLERANCE):
        u"""
        2つの3次元ベクトルが平行かどうか。

        :type v: `Vector`
        :param v: 比較するベクトル。
        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        return _MV(self.__data).isParallel(_MV(v.__data), tol)

    def set(self, *args):
        u"""
        他の値をセットする。

        コンストラクタと同様に、以下の値を指定可能。

        - `Vector`
        - x, y, z, w
        - x, y, z
        - x, y
        - 4値までのシーケンス

        :rtype: `Vector` (self)
        """
        if len(args) is 1:
            args = args[0]
            if hasattr(args, '_Vector__data'):
                args = args.__data
        try:
            for i, v in enumerate(args):
                self.__data[i] = v
        except:
            raise ValueError(type(self).__name__ + '.set : unsupported arguments.')
        return self

    def angle(self, v):
        u"""
        2つの3次元ベクトルの成す角を得る。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `float`
        """
        return _MV(self.__data).angle(_MV(v.__data))

    def length(self):
        u"""
        3次元ベクトルの長さを得る。

        :rtype: `float`
        """
        d = self.__data
        return sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])

    def lengthSq(self):
        u"""
        3次元ベクトルの長さの2乗を得る。

        :rtype: `float`
        """
        d = self.__data
        return d[0] * d[0] + d[1] * d[1] + d[2] * d[2]

    def normal(self):
        u"""
        正規化3次元ベクトルを得る。

        :rtype: `Vector`
        """
        v = _MV(self.__data).normalize()
        return _newV(_MP(v[0], v[1], v[2], self.__data[3]))

    def normalize(self):
        u"""
        正規化3次元ベクトルをセットする。

        :rtype: `Vector` (self)
        """
        d = self.__data
        v = _MV(d).normalize()
        d[0] = v[0]
        d[1] = v[1]
        d[2] = v[2]
        return self

    normalizeIt = normalize

    def rotateBy(self, q):
        u"""
        クォータニオンで回転したベクトルを得る。

        演算子 * でクォータニオンを乗じることと同じ。

        :type q: `.Quaternion`
        :param q: クォータニオン。
        :rtype: `Vector`
        """
        v = _MV(self.__data).rotateBy(q._Quaternion__data)
        return _newV(_MP(v[0], v[1], v[2], self.__data[3]))

    def rotateTo(self, v, factor=1.):
        u"""
        ベクトルを指定方向に向ける最小弧回転を得る。

        `.Quaternion`
        に2つのベクトルを渡して生成することと同じ。

        :type v: `Vector`
        :param v: 向ける方向。
        :param `float` factor: 完全に向ける量を 1.0 とする回転量。
        :rtype: `.Quaternion`
        """
        return _newQ(_MQ(_MV(self.__data), _MV(v.__data), factor))

    def transformAsNormal(self, m):
        u"""
        法線ベクトルとしてトランスフォームしたベクトルを得る。

        :type m: `.Matrix`
        :param m: 変換マトリックス。
        :rtype: `Vector`
        """
        src = self.__data
        w = src[3]
        src[3] = 0.
        dst = src * m._Matrix__data.inverse().transpose()
        src[3] = w
        dst[3] = w
        return _newV(dst)

    def distanceTo(self, v):
        u"""
        2つの位置ベクトル間の距離を得る。

        :type v: `Vector`
        :param v: もう1方の位置。
        :rtype: `float`
        """
        return self.__data.distanceTo(v.__data)

    def distanceSqTo(self, v):
        u"""
        2つの位置ベクトル間の2乗距離を得る。

        :type v: `Vector`
        :param v: もう1方の位置。
        :rtype: `float`
        """
        v = self.__data.distanceTo(v.__data)
        return v * v

    def cartesianize(self):
        u"""
        同次座標を直交座標(W=1)に変換する。

        (W*x, W*y, W*z, W) が (x, y, z, 1) に変換される。

        :rtype: `Vector` (self)
        """
        self.__data.cartesianize()
        return self

    def rationalize(self):
        u"""
        同次座標を有利形式に変換する。

        (W*x, W*y, W*z, W) が (x, y, z, W) に変換される。

        :rtype: `Vector` (self)
        """
        self.__data.rationalize()
        return self

    def homogenize(self):
        u"""
        有理形式の座標を同次座標に変換する。

        (x, y, z, W) が (W*x, W*y, W*z, W) に変換される。

        :rtype: `Vector` (self)
        """
        self.__data.homogenize()
        return self

    def cross(self, v):
        u"""
        3次元ベクトルの外積を得る。

        演算子 ^ と同じ。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `Vector`
        """
        v = _MV(self.__data).__xor__(_MV(v.__data))
        return _newV(_MP(v[0], v[1], v[2], self.__data[3]))

    def dot(self, v):
        u"""
        3次元ベクトルの内積を得る。

        1x3 と 3x1 の行列としての乗算ともいえる。

        演算子 * と同じ。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `float`
        """
        d = self.__data
        s = v.__data
        return d[0] * s[0] + d[1] * s[1] + d[2] * s[2]

    def dot4(self, v):
        u"""
        4次元ベクトルの内積を得る。

        1x4 と 4x1 の行列としての乗算ともいえる。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `float`
        """
        d = self.__data
        s = v.__data
        return d[0] * s[0] + d[1] * s[1] + d[2] * s[2] + d[3] * s[3]

    def dot4r(self, v):
        u"""
        4次元ベクトルを 4x1 と 1x4 の行列として乗算する。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `.Matrix`
        """
        a = self.__data
        b = v.__data
        return _newM(_MM([
            a[0] * b[0], a[0] * b[1], a[0] * b[2], a[0] * b[3],
            a[1] * b[0], a[1] * b[1], a[1] * b[2], a[1] * b[3],
            a[2] * b[0], a[2] * b[1], a[2] * b[2], a[2] * b[3],
            a[3] * b[0], a[3] * b[1], a[3] * b[2], a[3] * b[3],
        ]))

    def xform3(self, m):
        u"""
        3次元ベクトル（方向ベクトル）をトランスフォームする。
        """
        src = self.__data
        w = src[3]
        src[3] = 0.
        dst = src * m._Matrix__data
        src[3] = w
        dst[3] = w
        return _newV(dst)

    def xform4(self, m):
        u"""
        4次元ベクトル（3次元同次座標）をトランスフォームする。

        演算子 * で行列を乗じることと同じ。

        :type m: `.Matrix`
        :param m: 変換マトリックス。
        :rtype: `Vector`
        """
        return _newV(self.__data * m._Matrix__data)

    def abs(self):
        u"""
        4次元ベクトルの各要素を絶対値にしたベクトルを得る。

        abs 組み込み関数を使用する場合と等価。

        :rtype: `Vector`
        """
        v = self.__data
        return _newV(_MP(abs(v[0]), abs(v[1]), abs(v[2]), abs(v[3])))

    def iabs(self):
        u"""
        4次元ベクトルの各要素を絶対値にする。

        :rtype: `Vector` (self)
        """
        v = self.__data
        v[0] = abs(v[0])
        v[1] = abs(v[1])
        v[2] = abs(v[2])
        v[3] = abs(v[3])
        return self

    def mul(self, v):
        u"""
        4次元ベクトルの各要素を乗算したベクトルを得る。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `Vector`
        """
        a = self.__data
        b = v.__data
        return _newV(_MP(a[0] * b[0], a[1] * b[1], a[2] * b[2], a[3] * b[3]))

    def imul(self, v):
        u"""
        4次元ベクトルの各要素を乗算したベクトルをセットする。

        :type v: `Vector`
        :param v: もう1方のベクトル。
        :rtype: `Vector` (self)
        """
        a = self.__data
        b = v.__data
        a[0] *= b[0]
        a[1] *= b[1]
        a[2] *= b[2]
        a[3] *= b[3]
        return self

    def div(self, v, pre=AVOID_ZERO_DIV_PRECISION):
        u"""
        4次元ベクトルの各要素を除算したベクトルを得る。

        :type v: `Vector`
        :param v: 分母のベクトル。
        :param `float` pre: ゼロ除算を避ける為の許容誤差。
        :rtype: `Vector`
        """
        a = self.__data
        b = v.__data
        return _newV(_MP(
            a[0] / avoidZeroDiv(b[0], pre),
            a[1] / avoidZeroDiv(b[1], pre),
            a[2] / avoidZeroDiv(b[2], pre),
            a[3] / avoidZeroDiv(b[3], pre),
        ))

    def idiv(self, v, pre=AVOID_ZERO_DIV_PRECISION):
        u"""
        4次元ベクトルの各要素を除算したベクトルをセットする。

        :type v: `Vector`
        :param v: 分母のベクトル。
        :param `float` pre: ゼロ除算を避ける為の許容誤差。
        :rtype: `Vector` (self)
        """
        a = self.__data
        b = v.__data
        a[0] /= avoidZeroDiv(b[0], pre)
        a[1] /= avoidZeroDiv(b[1], pre)
        a[2] /= avoidZeroDiv(b[2], pre)
        a[3] /= avoidZeroDiv(b[3], pre)
        return self

    def orthogonal(self, vec):
        u"""
        指定ベクトルに直交化したベクトルを得る。

        :type vec: `Vector`
        :param vec: 軸ベクトル。
        :rtype: `Vector`
        """
        a = self.__data
        b = _MV(vec.__data).normalize()
        v = a - b * (a[0] * b[0] + a[1] * b[1] + a[2] * b[2])
        return _newV(_MP(v[0], v[1], v[2], a[3]))

    def orthogonalize(self, vec):
        u"""
        指定ベクトルに直交化したベクトルをセットする。

        :type vec: `Vector`
        :param vec: 軸ベクトル。
        :rtype: `Vector` (self)
        """
        a = self.__data
        b = _MV(vec.__data).normalize()
        a -= b * (a[0] * b[0] + a[1] * b[1] + a[2] * b[2])
        return self

    def maxAxis(self, noSign=False):
        u"""
        絶対値が最大の要素の軸IDを得る。

        :param `bool` noSign: 符号ビットを含まない軸ID (0～2) を得る。
        :rtype: `int`
        """
        dt = self.__data
        ax = abs(dt[0])
        ay = abs(dt[1])
        az = abs(dt[2])
        if ax > ay:
            if ax > az:
                return AXIS_X if (noSign or dt[0] >= 0.) else AXIS_NEG_X
        elif ay > az:
            return AXIS_Y if (noSign or dt[1] >= 0.) else AXIS_NEG_Y
        return AXIS_Z if (noSign or dt[2] >= 0.) else AXIS_NEG_Z

    def minAxis(self, noSign=False):
        u"""
        絶対値が最小の要素の軸IDを得る。

        :param `bool` noSign: 符号ビットを含まない軸ID (0～2) を得る。
        :rtype: `int`
        """
        dt = self.__data
        ax = abs(dt[0])
        ay = abs(dt[1])
        az = abs(dt[2])
        if ax < ay:
            if ax < az:
                return AXIS_X if (noSign or dt[0] >= 0.) else AXIS_NEG_X
        elif ay < az:
            return AXIS_Y if (noSign or dt[1] >= 0.) else AXIS_NEG_Y
        return AXIS_Z if (noSign or dt[2] >= 0.) else AXIS_NEG_Z

    def findNearestAxis(self, asId=False):
        u"""
        方向ベクトルに最も近い X,Y,Z,-X,-Y,-Z 軸方向を得る。

        殆どゼロベクトルで判定できない場合は None となる。

        :param `bool` asId: 結果をIDで得る。
        :rtype: `Vector`, `int` or None
        """
        dt = self.__data
        max_a = 0.
        axis = None
        for key in _XYZ_AXES:
            v = dt[key]
            a = abs(v)
            if a > max_a:
                max_a = a
                axis = key
                if v < 0.:
                    axis += AXIS_NEG
        return axis if asId else _AXIS_VECTOR_DICT.get(axis)

    @Numpy
    def ndarray(self):
        import numpy as np
        return np.array(self.vector, dtype=np.float16)


V = Vector  #: `Vector` の別名。

_MUTATOR_DICT[V] = (
    'set',
    'normalize',
    'normalizeIt',
    'cartesianize',
    'rationalize',
    'homogenize',
    'iabs',
    'imul',
    'idiv',
    'orthogonalize',
)
ImmutableVector = immutableType(V)  #: `Vector` の `immutable` ラッパー。


def _newV(data, cls=V):
    obj = _object_new(cls)
    _V_setdata(obj, data)
    return obj


_object_new = object.__new__

_V_setdata = V._Vector__data.__set__

V.Tolerance = _TOLERANCE  #: 同値とみなす許容誤差。

V.Zero4 = ImmutableVector(0., 0., 0., 0.)  #: 4次元ゼロベクトル。
V.Zero = ImmutableVector()  #: ゼロベクトル。
V.Origin = V.Zero  #: `Zero` と同じ。
V.One = ImmutableVector(1., 1., 1.)  #: 各要素が 1.0 のベクトル。
V.XAxis = ImmutableVector(1., 0., 0.)  #: X軸ベクトル。
V.YAxis = ImmutableVector(0., 1., 0.)  #: Y軸ベクトル。
V.ZAxis = ImmutableVector(0., 0., 1.)  #: Z軸ベクトル。
V.XNegAxis = ImmutableVector(-1., 0., 0.)  #: -X軸ベクトル。
V.YNegAxis = ImmutableVector(0., -1., 0.)  #: -Y軸ベクトル。
V.ZNegAxis = ImmutableVector(0., 0., -1.)  #: -Z軸ベクトル。

_AXIS_VECTOR_DICT = ImmutableDict({
    AXIS_X: V.XAxis,
    AXIS_Y: V.YAxis,
    AXIS_Z: V.ZAxis,
    AXIS_NEG_X: V.XNegAxis,
    AXIS_NEG_Y: V.YNegAxis,
    AXIS_NEG_Z: V.ZNegAxis,
})
V.AXIS_VECTOR_DICT = _AXIS_VECTOR_DICT  #: 軸 ID からベクトルを得る辞書。

import maya.api.OpenMaya as _api2

__all__ = ['Matrix', 'M', 'ImmutableMatrix']

_MM = _api2.MMatrix
_MQ = _api2.MQuaternion
_ME = _api2.MEulerRotation
_MP = _api2.MPoint
_MV = _api2.MVector
_MX = _api2.MTransformationMatrix
_MSpace_kTransform = _api2.MSpace.kTransform
_MV_Zero = _MV.kZeroVector
_MQ_Identity = _MQ.kIdentity
_MM_Identity = _MM.kIdentity

_TOLERANCE = _MM.kTolerance

_ZERO3 = (0., 0., 0.)


class Matrix(_YMatrix):
    def __init__(self, *args, **kwargs):
        super(Matrix, self).__init__(*args, **kwargs)

    __slots__ = ('__data',)
    __hash__ = None

    def __new__(cls, *args, **kwargs):
        n = len(args)
        if n >= 3:
            vx = args[0]._Vector__data
            vy = args[1]._Vector__data
            vz = args[2]._Vector__data
            vt = args[3]._Vector__data if n >= 4 else _ZERO3
            if kwargs.get('transpose'):
                return _newM(_MM([
                    vx[0], vy[0], vz[0], 0.,
                    vx[1], vy[1], vz[1], 0.,
                    vx[2], vy[2], vz[2], 0.,
                    vt[0], vt[1], vt[2], 1.,
                ]), cls)
            else:
                return _newM(_MM([
                    vx[0], vx[1], vx[2], 0.,
                    vy[0], vy[1], vy[2], 0.,
                    vz[0], vz[1], vz[2], 0.,
                    vt[0], vt[1], vt[2], 1.,
                ]), cls)
        return _newM(_MM(*args), cls)

    def __reduce__(self):
        return type(self), (tuple(self.__data),)

    def __repr__(self):
        return type(self).__name__ + str(self.__data)

    def __str__(self):
        return str(self.__data)

    def __len__(self):
        return 16

    def __getitem__(self, i):
        return self.__data[i]

    u'''
    def __contains__(self, v):
        return v in self.__data

    def __iter__(self):
        d = self.__data
        for i in _RANGE16:
            yield d[i]

    def __reversed__(self):
        d = self.__data
        for i in _REVERSED_RANGE16:
            yield d[i]

    def index(self, v):
        d = self.__data
        for i in _RANGE16:
            if d[i] == v:
                return i
        raise ValueError(repr(v) + ' is not in matrix')

    def count(self, v):
        c = 0
        for x in self.__data:
            if x == v:
                c += 1
        return c
    '''

    def __setitem__(self, i, v):
        # Fix DoubleAccessorBug
        vals = [
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
        ]
        vals[i] = v - self[i]
        self.__data += _MM(vals)

    def __eq__(self, v):
        try:
            return self.__data == v.__data
        except:
            return False

    def __ne__(self, v):
        try:
            return self.__data != v.__data
        except:
            return True

    def __neg__(self):
        return _newM(self.__data * -1.)

    def __add__(self, v):
        try:
            return _newM(self.__data + v.__data)
        except:
            raise ValueError("%s + %r" % (type(self).__name__, v))

    def __iadd__(self, v):
        try:
            self.__data += v.__data
        except:
            raise ValueError("%s += %r" % (type(self).__name__, v))
        return self

    def __sub__(self, v):
        try:
            return _newM(self.__data - v.__data)
        except:
            raise ValueError("%s - %r" % (type(self).__name__, v))

    def __isub__(self, v):
        try:
            self.__data -= v.__data
        except:
            raise ValueError("%s -= %r" % (type(self).__name__, v))
        return self

    def __mul__(self, v):
        if isinstance(v, Number):
            return _newM(self.__data * v)
        elif hasattr(v, '_Transformation__data'):
            return _newM(self.__data * v.m.__data)
        else:
            try:
                return _newM(self.__data * v.__data)
            except:
                raise ValueError("%s * %r" % (type(self).__name__, v))

    def __imul__(self, v):
        if isinstance(v, Number):
            self.__data *= v
        elif hasattr(v, '_Transformation__data'):
            self.__data *= v.m.__data
        else:
            try:
                self.__data *= v.__data
            except:
                raise ValueError("%s *= %r" % (type(self).__name__, v))
        return self

    def __rmul__(self, v):
        try:
            return _newM(self.__data.__rmul__(v))
        except:
            raise ValueError("%r * %s" % (v, type(self).__name__))

    def __div__(self, v):
        try:
            return _newM(self.__data * (1. / v))
        except:
            raise ValueError("%s / %r" % (type(self).__name__, v))

    def __idiv__(self, v):
        try:
            self.__data *= (1. / v)
        except:
            raise ValueError("%s /= %r" % (type(self).__name__, v))
        return self

    def __rdiv__(self, v):
        try:
            return _newM(_MM([v / x for x in self]))
        except:
            raise ValueError("%r / %s" % (v, type(self).__name__))

    def isEquivalent(self, m, tol=_TOLERANCE):
        u"""
        ほぼ同値かどうか。

        :type m: `Matrix`
        :param m: 比較するマトリックス。
        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        try:
            return self.__data.isEquivalent(m.__data, tol)
        except:
            return False

    def isIdentity(self, tol=_TOLERANCE):
        u"""
        ほぼ単位行列かどうか。

        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        return self.__data.isEquivalent(_MM_Identity, tol)

    def isSingular(self):
        u"""
        特異行列かどうか。

        :rtype: `bool`
        """
        return self.__data.isSingular()

    def set(self, v):
        u"""
        他の値をセットする。

        コンストラクタと同様に、以下の値を指定可能。

        - `Matrix`
        - 16値のシーケンス

        :rtype: `Matrix` (self)
        """
        # Fix DoubleAccessorBug
        self.__data += _MM([s - d for s, d in zip(v, self.__data)])
        return self

    def setToIdentity(self):
        u"""
        単位行列をセットする。

        :rtype: `self`
        """
        self.__data.setToIdentity()
        return self

    def init3x3(self):
        u"""
        3x3 部分を初期化する。

        4x4 全て初期化する場合は `setToIdentity` が利用できる。

        平行移動成分のみの行列を新規に得たい場合は
        `asTranslationMatrix` が利用できる。

        :rtype: `Matrix` (self)
        """
        dt = self.__data
        # Fix DoubleAccessorBug:
        dt -= _MM([
            dt[0] - 1., dt[1], dt[2], 0.,
            dt[4], dt[5] - 1., dt[6], 0.,
            dt[8], dt[9], dt[10] - 1., 0.,
            0., 0., 0., 0.,
        ])
        return self

    def initTranslation(self):
        u"""
        4行目の平行移動成分をクリアする。

        3x3 以外を初期化したマトリクスを新規に得たい場合は
        `as3x3` が利用できる。

        :rtype: `Matrix` (self)
        """
        dt = self.__data
        dt[12] = 0.
        dt[13] = 0.
        dt[14] = 0.
        return self

    initT = initTranslation  #: `initTranslation` の別名。

    def getElem(self, row, col):
        u"""
        指定位置の要素を得る。

        :param `int` row: 行インデックス (0-3)
        :param `int` col: 列インデックス (0-3)
        :rtype: `float`
        """
        return self[row * 4 + col]

    def setElem(self, row, col, val):
        u"""
        指定位置の要素をセットする。

        :param `int` row: 行を 0 ～ 3 で指定。
        :param `int` col: 列を 0 ～ 3 で指定。
        :param `float` val: セットする値。
        """
        self[row * 4 + col] = val

    def asTransformation(self):
        u"""
        トランスフォーメーションとして得る。

        :rtype: `.Transformation`
        """
        return _newX(dict(m=_newM(_MM(self.__data), ImmutableMatrix)))

    asX = asTransformation  #: `asTransformation` の別名。

    def asQuaternion(self):
        u"""
        クォータニオンを得る。

        :rtype: `.Quaternion`
        """
        # return _newQ(_MX(self.__data).rotation(True))
        # MQuaternion の場合 MTransformationMatrix より直接の方が速い。
        return _newQ(_MQ().setValue(self.__data.homogenize()))

    asQ = asQuaternion  #: `asQuaternion` の別名。

    def asEulerRotation(self, order=XYZ):
        u"""
        オイラー角回転を得る。

        :param `int` order: 得たい回転オーダー。
        :rtype: `.EulerRotation`

        .. note::
            `EulerRotation` の単位は弧度法なので、
            度数法で得たい場合は `asDegrees` を使用すると良い。
        """
        # return _newE(_ME(0., 0., 0., order).setValue(self.__data.homogenize()))
        # MEulerRotation の場合 MTransformationMatrix の方が直接よりやや速い。
        if order is XYZ:
            return _newE(_MX(self.__data).rotation(False))
        else:
            return _newE(_MX(self.__data).reorderRotation(order + 1).rotation(False))

    asE = asEulerRotation  #: `asEulerRotation` の別名。

    def asDegrees(self, order=XYZ):
        u"""
        オイラー角回転を度数法の `list` として得る。

        :param `int` order: 得たい回転オーダー。
        :rtype: `list`

        .. note::
            単位を弧度法で得たい場合は `asEulerRotation` を使用すると良い。
        """
        if order is XYZ:
            e = _MX(self.__data).rotation(False)
        else:
            e = _MX(self.__data).reorderRotation(order + 1).rotation(False)
        return [e[0] * TO_DEG, e[1] * TO_DEG, e[2] * TO_DEG]

    asD = asDegrees  #: `asDegrees` の別名。

    def asTranslation(self):
        u"""
        平行移動成分を得る。

        :rtype: `.Vector`
        """
        return _newV(_MP(self.__data[12], self.__data[13], self.__data[14]))

    asT = asTranslation  #: `asTranslation` の別名。

    def asScaling(self):
        u"""
        スケーリング成分を得る。

        :rtype: `.Vector`
        """
        return _newV(_MP(_MX(self.__data).scale(_MSpace_kTransform)))

    asS = asScaling  #: `asScaling` の別名。

    def asShearing(self):
        u"""
        シアー成分を得る。

        :rtype: `.Vector`
        """
        return _newV(_MP(_MX(self.__data).shear(_MSpace_kTransform)))

    asSh = asShearing  #: `asShearing` の別名。

    def asTranslationMatrix(self):
        u"""
        平行移動のみの行列を得る。

        :rtype: `Matrix`
        """
        return _newM(_MM([
            1., 0., 0., 0.,
            0., 1., 0., 0.,
            0., 0., 1., 0.,
            self.__data[12], self.__data[13], self.__data[14], 1.,
        ]))

    asTM = asTranslationMatrix  #: `asTranslationMatrix` の別名。

    def asRotationMatrix(self):
        u"""
        回転のみの行列を得る。

        :rtype: `Matrix`
        """
        m = self.__data.homogenize()
        return _newM(_MM([
            m[0], m[1], m[2], 0.,
            m[4], m[5], m[6], 0.,
            m[8], m[9], m[10], 0.,
            0., 0., 0., 1.,
        ]))

    asRM = asRotationMatrix  #: `asRotationMatrix` の別名。

    def asScalingMatrix(self):
        u"""
        スケーリング成分(scale+shear)のみの行列を得る。

        :rtype: `Matrix`:
        """
        xm = _MX(self.__data)
        xm.setTranslation(_MV_Zero, _MSpace_kTransform)
        xm.setRotation(_MQ_Identity)
        return _newM(xm.asMatrix())

    asSM = asScalingMatrix  #: `asScalingMatrix` の別名。

    def as3x3(self):
        u"""
        3x3部分以外を初期化した行列を得る。

        :rtype: `Matrix`
        """
        m = self.__data
        return _newM(_MM([
            m[0], m[1], m[2], 0.,
            m[4], m[5], m[6], 0.,
            m[8], m[9], m[10], 0.,
            0., 0., 0., 1.,
        ]))

    def asTransposed3x3(self):
        u"""
        3x3部分は転置、それ以外の部分は初期化した行列を得る。

        :rtype: `Matrix`
        """
        m = self.__data
        return _newM(_MM([
            m[0], m[4], m[8], 0.,
            m[1], m[5], m[9], 0.,
            m[2], m[6], m[10], 0.,
            0., 0., 0., 1.,
        ]))

    def transpose(self):
        u"""
        転置行列を得る。

        :rtype: `Matrix`
        """
        return _newM(self.__data.transpose())

    def transposeIt(self):
        u"""
        転置行列をセットする。

        :rtype: `Matrix` (self)
        """
        _M_setdata(self, self.__data.transpose())
        return self

    def inverse(self):
        u"""
        逆行列を得る。

        :rtype: `Matrix`
        """
        return _newM(self.__data.inverse())

    def invertIt(self):
        u"""
        逆行列をセットする。

        :rtype: `Matrix` (self)
        """
        _M_setdata(self, self.__data.inverse())
        return self

    def adjoint(self):
        u"""
        余因子行列を得る。

        :rtype: `Matrix`
        """
        return _newM(self.__data.adjoint())

    def adjointIt(self):
        u"""
        余因子行列をセットする。

        :rtype: `Matrix` (self)
        """
        _M_setdata(self, self.__data.adjoint())
        return self

    def homogenize(self):
        u"""
        3x3部分を正規直交化した行列を得る。

        :rtype: `Matrix`
        """
        return _newM(self.__data.homogenize())

    def homogenizeIt(self):
        u"""
        3x3部分を正規直交化した行列をセットする。

        :rtype: `Matrix` (self)
        """
        _M_setdata(self, self.__data.homogenize())
        return self

    def det4x4(self):
        u"""
        行列式を得る。

        :rtype: `float`
        """
        return self.__data.det4x4()

    def det3x3(self):
        u"""
        3x3部分の行列式を得る。

        :rtype: `float`
        """
        return self.__data.det3x3()

    def row(self, i):
        u"""
        行ベクトルを得る。

        :param `int` i: 行インデックス（0～3）。
        :rtype: `.Vector`
        """
        d = self.__data
        i *= 4
        return _newV(_MP(d[i], d[i + 1], d[i + 2], d[i + 3]))

    def rows(self):
        u"""
        行ベクトルを4つ全て得る。

        :rtype: `tuple`
        """
        d = self.__data
        return (
            _newV(_MP(d[0], d[1], d[2], d[3])),
            _newV(_MP(d[4], d[5], d[6], d[7])),
            _newV(_MP(d[8], d[9], d[10], d[11])),
            _newV(_MP(d[12], d[13], d[14], d[15])),
        )

    def setRow(self, i, v):
        u"""
        行ベクトルをセットする。

        :param `int` i: 行インデックス（0～3）。
        :type v: `.Vector`
        :param v: セットする4次元ベクトル。
        """
        # Fix DoubleAccessorBug
        vals = [
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
        ]
        data = self.__data
        i *= 4
        vals[i] = v[0] - data[i]
        i += 1
        vals[i] = v[1] - data[i]
        i += 1
        vals[i] = v[2] - data[i]
        i += 1
        vals[i] = v[3] - data[i]
        data += _MM(vals)

    def setRows(self, v0, v1, v2, v3):
        u"""
        行ベクトルを4つ全てセットする。

        :type v0: `.Vector`
        :param v0: 1行目の4次元ベクトル。
        :type v1: `.Vector`
        :param v1: 2行目の4次元ベクトル。
        :type v2: `.Vector`
        :param v2: 3行目の4次元ベクトル。
        :type v3: `.Vector`
        :param v3: 4行目の4次元ベクトル。
        """
        # Fix DoubleAccessorBug
        m = _MM([
            v0[0], v0[1], v0[2], v0[3],
            v1[0], v1[1], v1[2], v1[3],
            v2[0], v2[1], v2[2], v2[3],
            v3[0], v3[1], v3[2], v3[3],
        ])
        self.__data += m - self.__data

    def column(self, i):
        u"""
        列ベクトルを得る。

        :param `int` i: 列インデックス（0～3）。
        :rtype: `.Vector`
        """
        d = self.__data
        return _newV(_MP(d[i], d[i + 4], d[i + 8], d[i + 12]))

    def columns(self):
        u"""
        列ベクトルを4つ全て得る。

        :rtype: `tuple`
        """
        d = self.__data
        return (
            _newV(_MP(d[0], d[4], d[8], d[12])),
            _newV(_MP(d[1], d[5], d[9], d[13])),
            _newV(_MP(d[2], d[6], d[10], d[14])),
            _newV(_MP(d[3], d[7], d[11], d[15])),
        )

    def setColumn(self, i, v):
        u"""
        列ベクトルをセットする。

        :param `int` i: 列インデックス（0～3）。
        :type v: `.Vector`
        :param v: セットする4次元ベクトル。
        """
        # Fix DoubleAccessorBug
        vals = [
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
        ]
        data = self.__data
        vals[i] = v[0] - data[i]
        i += 4
        vals[i] = v[1] - data[i]
        i += 4
        vals[i] = v[2] - data[i]
        i += 4
        vals[i] = v[3] - data[i]
        data += _MM(vals)

    def setColumns(self, v0, v1, v2, v3):
        u"""
        列ベクトルを4つ全てセットする。

        :type v0: `.Vector`
        :param v0: 1列目の4次元ベクトル。
        :type v1: `.Vector`
        :param v1: 2列目の4次元ベクトル。
        :type v2: `.Vector`
        :param v2: 3列目の4次元ベクトル。
        :type v3: `.Vector`
        :param v3: 4列目の4次元ベクトル。
        """
        # Fix DoubleAccessorBug
        m = _MM([
            v0[0], v1[0], v2[0], v3[0],
            v0[1], v1[1], v2[1], v3[1],
            v0[2], v1[2], v2[2], v3[2],
            v0[3], v1[3], v2[3], v3[3],
        ])
        self.__data += m - self.__data

    def axis(self, i, transpose=False):
        u"""
        3x3部分の行や列を軸ベクトルとして得る。

        `.Vector` の w は 1.0 となる。

        :param `int` i: 軸指定(0=X, 1=Y, 2=Z)。
        :param `bool` transpose:
            転置行列の軸ベクトルを得る。
            言い換えると False では行ベクトルを
            True では列ベクトルを得ることになる。
        :rtype: `.Vector`
        """
        if transpose:
            return _newV(_MP(self.__data[i], self.__data[i + 4], self.__data[i + 8]))
        i *= 4
        return _newV(_MP(self.__data[i], self.__data[i + 1], self.__data[i + 2]))

    def axes(self, transpose=False):
        u"""
        3x3部分の行や列の軸ベクトルを3つ得る。

        各 `.Vector` の w は 1.0 となる。

        :param `bool` transpose:
            転置行列の軸ベクトルを得る。
            言い換えると False では行ベクトルを
            True では列ベクトルを得ることになる。
        :rtype: `tuple`
        """
        m = self.__data
        if transpose:
            return (
                _newV(_MP(m[0], m[4], m[8])),
                _newV(_MP(m[1], m[5], m[9])),
                _newV(_MP(m[2], m[6], m[10])),
            )
        return (
            _newV(_MP(m[0], m[1], m[2])),
            _newV(_MP(m[4], m[5], m[6])),
            _newV(_MP(m[8], m[9], m[10])),
        )

    def setAxis(self, i, v, transpose=False):
        u"""
        3x3部分の行や列のベクトルをセットする。

        :param `int` i: 軸指定(0=X, 1=Y, 2=Z)。
        :type v: `.Vector`
        :param v:
            セットする軸ベクトル。
        :param `bool` transpose:
            転置行列の軸ベクトルをセットする。
            言い換えると False では行ベクトルを
            True では列ベクトルをセットすることになる。
        """
        # Fix DoubleAccessorBug
        vals = [
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
        ]
        data = self.__data
        if transpose:
            vals[i] = v[0] - data[i]
            i += 4
            vals[i] = v[1] - data[i]
            i += 4
            vals[i] = v[2] - data[i]
        else:
            i *= 4
            vals[i] = v[0] - data[i]
            i += 1
            vals[i] = v[1] - data[i]
            i += 1
            vals[i] = v[2] - data[i]
        data += _MM(vals)

    def setAxes(self, i, vx, vy, vz, vt=V.Zero, transpose=False):
        u"""
        3x3部分の行や列と4行目の平行移動ベクトルをセットする。

        :type vx: `.Vector`
        :param vx: セットするX軸ベクトル。
        :type vy: `.Vector`
        :param vy: セットするY軸ベクトル。
        :type vz: `.Vector`
        :param vz: セットするZ軸ベクトル。
        :type vt: `.Vector`
        :param vt:
            セットする平行移動ベクトル。
            これだけは transpose オプションの影響を受けない。
        :param `bool` transpose:
            3x3部分には転置行列の軸ベクトルをセットする。
            言い換えると False では行ベクトルを
            True では列ベクトルをセットすることになる。
        """
        # Fix DoubleAccessorBug
        if transpose:
            m = _MM([
                vx[0], vy[0], vz[0], 0.,
                vx[1], vy[1], vz[1], 0.,
                vx[2], vy[2], vz[2], 0.,
                vt[0], vt[1], vt[2], 1.,
            ])
        else:
            m = _MM([
                vx[0], vx[1], vx[2], 0.,
                vy[0], vy[1], vy[2], 0.,
                vz[0], vz[1], vz[2], 0.,
                vt[0], vt[1], vt[2], 1.,
            ])
        self.__data += m - self.__data

    def mul(self, m):
        u"""
        マトリックス要素同士を乗算する。

        :type m: `Matrix`
        :param m: 乗じるマトリックス。
        :rtype: `Matrix`
        """
        a = self.__data
        b = m.__data
        return _newM(_MM([
            a[0] * b[0], a[1] * b[1], a[2] * b[2], a[3] * b[3],
            a[4] * b[4], a[5] * b[5], a[6] * b[6], a[7] * b[7],
            a[8] * b[8], a[9] * b[9], a[10] * b[10], a[11] * b[11],
            a[12] * b[12], a[13] * b[13], a[14] * b[14], a[15] * b[15],
        ]))

    def imul(self, m):
        u"""
        マトリックス要素同士を乗算してセットする。

        :type m: `Matrix`
        :param m: 乗じるマトリックス。
        :rtype: `Matrix` (self)
        """
        a = self.__data
        b = m.__data
        # Fix DoubleAccessorBug:
        a += _MM([
            a[0] * b[0] - a[0],
            a[1] * b[1] - a[1],
            a[2] * b[2] - a[2],
            a[3] * b[3] - a[3],
            a[4] * b[4] - a[4],
            a[5] * b[5] - a[5],
            a[6] * b[6] - a[6],
            a[7] * b[7] - a[7],
            a[8] * b[8] - a[8],
            a[9] * b[9] - a[9],
            a[10] * b[10] - a[10],
            a[11] * b[11] - a[11],
            a[12] * b[12] - a[12],
            a[13] * b[13] - a[13],
            a[14] * b[14] - a[14],
            a[15] * b[15] - a[15],
        ])
        return self

    def div(self, m, pre=AVOID_ZERO_DIV_PRECISION):
        u"""
        マトリックス要素同士を除算する。

        ゼロ除算を避ける為、分母が `.avoidZeroDiv`
        でフィルタされてから実行される。

        :type m: `Matrix`
        :param m: 分母のマトリックス。
        :param `float` pre: ゼロ除算を避ける為の許容誤差。
        :rtype: `Matrix`
        """
        a = self.__data
        b = m.__data
        return _newM(_MM([
            a[0] / avoidZeroDiv(b[0], pre),
            a[1] / avoidZeroDiv(b[1], pre),
            a[2] / avoidZeroDiv(b[2], pre),
            a[3] / avoidZeroDiv(b[3], pre),
            a[4] / avoidZeroDiv(b[4], pre),
            a[5] / avoidZeroDiv(b[5], pre),
            a[6] / avoidZeroDiv(b[6], pre),
            a[7] / avoidZeroDiv(b[7], pre),
            a[8] / avoidZeroDiv(b[8], pre),
            a[9] / avoidZeroDiv(b[9], pre),
            a[10] / avoidZeroDiv(b[10], pre),
            a[11] / avoidZeroDiv(b[11], pre),
            a[12] / avoidZeroDiv(b[12], pre),
            a[13] / avoidZeroDiv(b[13], pre),
            a[14] / avoidZeroDiv(b[14], pre),
            a[15] / avoidZeroDiv(b[15], pre),
        ]))

    def idiv(self, m, pre=AVOID_ZERO_DIV_PRECISION):
        u"""
        各要素同士を除算し自身を更新する。

        ゼロ除算を避ける為、分母が `~Happy.util.avoidZeroDiv`
        でフィルタされてから実行される。

        :param iterable v: 要素数16個以上のシーケンス。
        :param `float` pre: ゼロ除算を避ける為の許容誤差。
        """
        a = self.__data
        b = m.__data
        # Fix DoubleAccessorBug:
        a += _MM([
            a[0] / avoidZeroDiv(b[0], pre) - a[0],
            a[1] / avoidZeroDiv(b[1], pre) - a[1],
            a[2] / avoidZeroDiv(b[2], pre) - a[2],
            a[3] / avoidZeroDiv(b[3], pre) - a[3],
            a[4] / avoidZeroDiv(b[4], pre) - a[4],
            a[5] / avoidZeroDiv(b[5], pre) - a[5],
            a[6] / avoidZeroDiv(b[6], pre) - a[6],
            a[7] / avoidZeroDiv(b[7], pre) - a[7],
            a[8] / avoidZeroDiv(b[8], pre) - a[8],
            a[9] / avoidZeroDiv(b[9], pre) - a[9],
            a[10] / avoidZeroDiv(b[10], pre) - a[10],
            a[11] / avoidZeroDiv(b[11], pre) - a[11],
            a[12] / avoidZeroDiv(b[12], pre) - a[12],
            a[13] / avoidZeroDiv(b[13], pre) - a[13],
            a[14] / avoidZeroDiv(b[14], pre) - a[14],
            a[15] / avoidZeroDiv(b[15], pre) - a[15],
        ])
        return self

    def hasNonUniformScaling(self, tol=_TOLERANCE):
        u"""
        非一様スケーリングが含まれているかどうか。

        :param `float` tol: 許容誤差。
        :rtype: `bool`
        """
        xm = _MX(self.__data)
        v = xm.shear(_MSpace_kTransform)
        if abs(v[0]) > tol or abs(v[1]) > tol or abs(v[2]) > tol:
            return True
        v = xm.scale(_MSpace_kTransform)
        return abs(v[0] - v[1]) > tol or abs(v[0] - v[2]) > tol

    def setTranslation(self, v):
        u"""
        平行移動値をセットする。

        :type v: `.Vector`
        :param v: 平行移動の3次元ベクトル。
        """
        # Fix DoubleAccessorBug
        data = self.__data
        data += _MM([
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            v[0] - data[12], v[1] - data[13], v[2] - data[14], 0.,
        ])

    setT = setTranslation  #: `setTranslation` の別名。

    def addTranslation(self, v):
        u"""
        平行移動値を加算する。

        :type v: `.Vector`
        :param v: 平行移動の3次元ベクトル。
        """
        # Fix DoubleAccessorBug
        self.__data += _MM([
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            v[0], v[1], v[2], 0.,
        ])

    addT = addTranslation  #: `addTranslation` の別名。

    def subTranslation(self, v):
        u"""
        平行移動値を減算する。

        :type v: `.Vector`
        :param v: 平行移動の3次元ベクトル。
        """
        # Fix DoubleAccessorBug
        self.__data -= _MM([
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            0., 0., 0., 0.,
            v[0], v[1], v[2], 0.,
        ])

    subT = subTranslation  #: `subTranslation` の別名。

    @classmethod
    def makeTranslation(cls, v):
        u"""
        平行移動行列を作成する。

        :type v: `.Vector`
        :param v: 平行移動の3次元ベクトル。
        :rtype: `Matrix`
        """
        return cls([
            1., 0., 0., 0.,
            0., 1., 0., 0.,
            0., 0., 1., 0.,
            v[0], v[1], v[2], 1.,
        ])

    makeT = makeTranslation  #: `makeTranslation` の別名。

    @classmethod
    def makeInverseTranslation(cls, v):
        u"""
        平行移動の逆行列を作成する。

        :type v: `.Vector`
        :param v: 平行移動の3次元ベクトル。
        :rtype: `Matrix`
        """
        return cls([
            1., 0., 0., 0.,
            0., 1., 0., 0.,
            0., 0., 1., 0.,
            -v[0], -v[1], -v[2], 1.,
        ])

    makeInvT = makeInverseTranslation  #: `makeInverseTranslation` の別名。

    @classmethod
    def makeScaling(cls, v):
        u"""
        スケーリング行列を作成する。

        :type v: `.Vector`
        :param v: スケール値の3次元ベクトル。
        :rtype: `Matrix`
        """
        return cls([
            v[0], 0., 0., 0.,
            0., v[1], 0., 0.,
            0., 0., v[2], 0.,
            0., 0., 0., 1.,
        ])

    makeS = makeScaling  #: `makeScaling` の別名。

    @classmethod
    def makeInverseScaling(cls, v, pre=AVOID_ZERO_DIV_PRECISION):
        u"""
        スケーリングの逆行列を作成する。

        :type v: `.Vector`
        :param v: スケール値の3次元ベクトル。
        :param `float` pre: ゼロ除算を避ける為の許容誤差。
        :rtype: `Matrix`
        """
        return cls([
            1. / avoidZeroDiv(v[0], pre), 0., 0., 0.,
            0., 1. / avoidZeroDiv(v[1], pre), 0., 0.,
            0., 0., 1. / avoidZeroDiv(v[2], pre), 0.,
            0., 0., 0., 1.,
        ])

    makeInvS = makeInverseScaling  #: `makeInverseScaling` の別名。

    @classmethod
    def makeShearing(cls, v):
        u"""
        シアー行列を作成する。

        :type v: `.Vector`
        :param v: シアー値 (xy, yz, yx)
        :rtype: `Matrix`
        """
        return cls([
            1., 0., 0., 0.,
            v[0], 1., 0., 0.,
            v[1], v[2], 1., 0.,
            0., 0., 0., 1.,
        ])

    makeSh = makeShearing  #: `makeShearing` の別名。

    @classmethod
    def makeInverseShearing(cls, v):
        u"""
        シアーの逆行列を作成する。

        :type v: `.Vector`
        :param v: シアー値 (xy, yz, yx)
        :rtype: `Matrix`
        """
        return cls([
            1., 0., 0., 0.,
            -v[0], 1., 0., 0.,
            v[0] * v[2] - v[1], -v[2], 1., 0.,
            0., 0., 0., 1.,
        ])

    makeInvSh = makeInverseShearing  #: `makeInverseShearing` の別名。

    def mirror(self, mirrorAxis=AXIS_X, negAxis=True, t=True):
        u"""
        指定軸方向でミラーしたマトリックスを得る。

        :param `int` mirrorAxis:
            ミラーする基準軸。
            `.AXIS_X` 、 `.AXIS_Y` 、 `.AXIS_Z` のいずれかを指定する。
        :param `int` negAxis:
            行列式（スケール）が反転しないように、
            ミラー結果の逆を向けるローカル軸。
            `.AXIS_X` 、 `.AXIS_Y` 、 `.AXIS_Z` の他に、
            None 、 False 、 True を指定可能。

            省略時(True)はミラー基準軸と同じになる。
            False では 3x3 部は反転しない。
            None ではミラー結果から全軸を逆に向ける。
        :param `bool` t:
            平行移動値（4行目）も反転するかどうか。
        :rtype: `Matrix`
        """
        return _newM(_mirror(self.__data, mirrorAxis, negAxis, t))

    def mirrorIt(self, mirrorAxis=AXIS_X, negAxis=True, t=True):
        u"""
        指定軸方向でミラーしたマトリックスをセットする。

        :param `int` mirrorAxis:
            ミラーする基準軸。
            `.AXIS_X` 、 `.AXIS_Y` 、 `.AXIS_Z` のいずれかを指定する。
        :param `int` negAxis:
            行列式（スケール）が反転しないように、
            ミラー結果の逆を向けるローカル軸。
            `.AXIS_X` 、 `.AXIS_Y` 、 `.AXIS_Z` の他に、
            None 、 False 、 True を指定可能。

            省略時(True)はミラー基準軸と同じになる。
            False では 3x3 部は反転しない。
            None ではミラー結果から全軸を逆に向ける。
        :param `bool` t:
            平行移動値（4行目）も反転するかどうか。
        :rtype: `Matrix` (self)
        """
        self.__data = _mirror(self.__data, mirrorAxis, negAxis, t)
        return self


M = Matrix  #: `Matrix` の別名。

_MUTATOR_DICT[M] = (
    'set',
    'setToIdentity',
    'init3x3',
    'initTranslation',
    'initT',
    'setElem',
    'transposeIt',
    'invertIt',
    'adjointIt',
    'homogenizeIt',
    'setRow',
    'setRows',
    'setColumn',
    'setColumns',
    'setAxis',
    'setAxes',
    'imul'
    'idiv'
    'setTranslation',
    'setT',
    'addTranslation',
    'addT',
    'subTranslation',
    'subT',
    'mirrorIt',
)
ImmutableMatrix = immutableType(M)  #: `Matrix` の `immutable` ラッパー。


def _newM(data, cls=M):
    obj = _object_new(cls)
    _M_setdata(obj, data)
    return obj


_object_new = object.__new__

_M_setdata = M._Matrix__data.__set__

M.Tolerance = _TOLERANCE  #: 同値とみなす許容誤差。

M.Identity = ImmutableMatrix()  #: 単位行列。
M.Zero = ImmutableMatrix([0] * 16)  #: ゼロ。


# ------------------------------------------------------------------------------
def _mirror(d, mirrorAxis, negAxis, t):
    if mirrorAxis is AXIS_X:
        t = -d[12] if t else d[12]
        if negAxis is mirrorAxis or negAxis is True:
            return _MM([d[0], -d[1], -d[2], 0., -d[4], d[5], d[6], 0., -d[8], d[9], d[10], 0., t, d[13], d[14], 1.])
        elif negAxis is None:
            return _MM([d[0], -d[1], -d[2], 0., d[4], -d[5], -d[6], 0., d[8], -d[9], -d[10], 0., t, d[13], d[14], 1.])
        elif negAxis is AXIS_Y:
            return _MM([-d[0], d[1], d[2], 0., d[4], -d[5], -d[6], 0., -d[8], d[9], d[10], 0., t, d[13], d[14], 1.])
        elif negAxis is AXIS_Z:
            return _MM([-d[0], d[1], d[2], 0., -d[4], d[5], d[6], 0., d[8], -d[9], -d[10], 0., t, d[13], d[14], 1.])
        else:
            return _MM([d[0], d[1], d[2], 0., d[4], d[5], d[6], 0., d[8], d[9], d[10], 0., t, d[13], d[14], 1.])

    elif mirrorAxis is AXIS_Y:
        t = -d[13] if t else d[13]
        if negAxis is mirrorAxis or negAxis is True:
            return _MM([d[0], -d[1], d[2], 0., -d[4], d[5], -d[6], 0., d[8], -d[9], d[10], 0., d[12], t, d[14], 1.])
        elif negAxis is None:
            return _MM([-d[0], d[1], -d[2], 0., -d[4], d[5], -d[6], 0., -d[8], d[9], -d[10], 0., d[12], t, d[14], 1.])
        elif negAxis is AXIS_X:
            return _MM([-d[0], d[1], -d[2], 0., d[4], -d[5], d[6], 0., d[8], -d[9], d[10], 0., d[12], t, d[14], 1.])
        elif negAxis is AXIS_Z:
            return _MM([d[0], -d[1], d[2], 0., d[4], -d[5], d[6], 0., -d[8], d[9], -d[10], 0., d[12], t, d[14], 1.])
        else:
            return _MM([d[0], d[1], d[2], 0., d[4], d[5], d[6], 0., d[8], d[9], d[10], 0., d[12], t, d[14], 1.])

    else:  # AXIS_Z
        t = -d[14] if t else d[14]
        if negAxis is mirrorAxis or negAxis is True:
            return _MM([d[0], d[1], -d[2], 0., d[4], d[5], -d[6], 0., -d[8], -d[9], d[10], 0., d[12], d[13], t, 1.])
        elif negAxis is None:
            return _MM([-d[0], -d[1], d[2], 0., -d[4], -d[5], d[6], 0., -d[8], -d[9], d[10], 0., d[12], d[13], t, 1.])
        elif negAxis is AXIS_X:
            return _MM([-d[0], -d[1], d[2], 0., d[4], d[5], -d[6], 0., d[8], d[9], -d[10], 0., d[12], d[13], t, 1.])
        elif negAxis is AXIS_Y:
            return _MM([d[0], d[1], -d[2], 0., -d[4], -d[5], d[6], 0., d[8], d[9], -d[10], 0., d[12], d[13], t, 1.])
        else:
            return _MM([d[0], d[1], d[2], 0., d[4], d[5], d[6], 0., d[8], d[9], d[10], 0., d[12], d[13], t, 1.])


class Color(_YColors):
    def __init__(self, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
