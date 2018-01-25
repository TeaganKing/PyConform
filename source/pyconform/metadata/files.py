"""
File Metadata Class

Copyright 2017-2018, University Corporation for Atmospheric Research
LICENSE: See the LICENSE.rst file for details
"""

from memberobjects import MemberObject


class File(MemberObject):
    """
    Metadata describing a NetCDF file
    """
    _NETCDF3_FORMATS_ = {'NETCDF4_CLASSIC', 'NETCDF3_CLASSIC',
                         'NETCDF3_64BIT_OFFSET', 'NETCDF3_64BIT_DATA',
                         'NETCDF3_64BIT'}

    _NETCDF4_FORMATS_ = {'NETCDF4'}

    def __init__(self, name, format='NETCDF4_CLASSIC', deflate=1,   # @ReservedAssignment
                 shuffle='off', variables=(), dimensions=(), attributes={}, **kwds):
        super(File, self).__init__(name, **kwds)
        self.__attributes = self.__validate_attributes(attributes)
        self.__format = self.__validate_format(format)
        self.__deflate = self.__validate_deflate(deflate)
        self.__shuffle = self.__validate_shuffle(shuffle)
        self.__variables = self.__validate_variables(variables)
        self.__dimensions = self.__validate_dimensions(dimensions)
        self.path = None

    def __validate_attributes(self, attributes):
        if not isinstance(attributes, dict):
            msg = 'File {!r} attributes should be a dictionary'
            raise TypeError(msg.format(self.name))
        return attributes

    def __validate_format(self, format):  # @ReservedAssignment
        if not (format in File._NETCDF3_FORMATS_ or format in File._NETCDF4_FORMATS_):
            msg = 'File {!r} format {!r} is not recognized'
            raise TypeError(msg.format(self.name, format))
        return format

    def __validate_deflate(self, deflate):
        if not isinstance(deflate, int):
            msg = 'File {!r} deflate level must be an integer'
            raise TypeError(msg.format(self.name))
        return deflate

    def __validate_shuffle(self, shuffle):
        if not (isinstance(shuffle, basestring) and shuffle in ('on', 'off')):
            msg = 'File {!r} shuffle must be "on" or "off"'
            raise TypeError(msg.format(self.name))
        return shuffle

    def __validate_variables(self, variables):
        if not (isinstance(variables, (list, tuple)) and
                all(isinstance(v, basestring) for v in variables)):
            msg = 'File {!r} can only accept a list/tuple of variable names'
            raise TypeError(msg.format(self.name))
        return frozenset(variables)

    def __validate_dimensions(self, dimensions):
        if not (isinstance(dimensions, (list, tuple)) and
                all(isinstance(v, basestring) for v in dimensions)):
            msg = 'File {!r} can only accept a list/tuple of dimension names'
            raise TypeError(msg.format(self.name))
        return frozenset(dimensions)

    @property
    def attributes(self):
        return self.__attributes

    @property
    def format(self):
        return self.__format

    def is_netcdf3(self):
        if self.format in File._NETCDF3_FORMATS_:
            return True
        else:
            return False

    @property
    def deflate(self):
        return self.__deflate

    @property
    def shuffle(self):
        return self.__shuffle

    @property
    def dimensions(self):
        return self.__dimensions

    def get_dimensions(self):
        return {n: self._dataset.get_dimension(n) for n in self.dimensions}

    @property
    def variables(self):
        return self.__variables

    def get_variables(self):
        return {n: self._dataset.get_variable(n) for n in self.variables}

    @property
    def coordinates(self):
        return frozenset()
