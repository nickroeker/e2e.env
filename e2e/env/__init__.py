"""Class-based modeling of environment variables and their type conversions."""

import os
import typing

import e2e.env.exceptions


# Intentionally thin, pylint: disable=too-few-public-methods
class EnvMapper:
    """Class-based model of environment variables and their type conversions.

    Use to map environment variables as well as their conversions to native
    types, and fetch either the value or the name::

        class ServiceVars(e2e.env.EnvMapper):
            host: str = 'COMPANY_APP_HOST'
            port: int = 'COMPANY_APP_PORT'

        # Get the port via instance
        print(ServiceVars().port)    # 8080
        type(ServiceVars().port)     # <class 'int'>

        # Get the name of the port environment variable via class
        print(ServiceVars.port)      # COMPANY_APP_PORT
        type(ServiceVars.port)       # <class 'str'>

    """

    def __getattribute__(self, attr_name: str) -> typing.Any:
        clz = object.__getattribute__(self, '__class__')
        # Let any AttributeErrors raise first
        env_var_name = object.__getattribute__(self, attr_name)
        # Ensure we have a type
        if attr_name not in clz.__annotations__:
            raise TypeError(
                'Cannot convert environment value: No type-hint on "{}" in "{}"'
                .format(attr_name, clz))
        if env_var_name not in os.environ:
            raise e2e.env.exceptions.NoSuchVariableError(
                "Environment variable {} not found".format(env_var_name))
        conv_type = clz.__annotations__[attr_name]
        return typing.cast(conv_type, conv_type(os.getenv(env_var_name)))
