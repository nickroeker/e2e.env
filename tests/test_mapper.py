"""Tests for e2e.env.EnvMapper."""

import os

import pytest

import e2e.env


@pytest.fixture
def setenv():
    """Fixture to set up environment variables used in these tests.

    Additionally returns the name of a variable known to not exist.
    """
    os.environ['ENVTEST_EMPTY'] = ''

    os.environ['ENVTEST_STR1'] = 'env test str 1'
    os.environ['ENVTEST_STR2'] = 'env test str 2'

    os.environ['ENVTEST_INT_NEG'] = '-1'
    os.environ['ENVTEST_INT_ZERO'] = '0'
    os.environ['ENVTEST_INT_POS'] = '1'
    os.environ['ENVTEST_INT_BIG'] = '19223372036854775807'

    os.environ['ENVTEST_BOOL_TRUE'] = 'true'
    os.environ['ENVTEST_BOOL_FALSE'] = 'false'

    os.environ['ENVTEST_FLOAT_NEG'] = '-2.5'
    os.environ['ENVTEST_FLOAT_ZERO'] = '0.0'
    os.environ['ENVTEST_FLOAT_POS'] = '2.5'

    unset_var = 'THIS_DEFINITELY_DOESNT_EXIST_123456'

    if unset_var in os.environ:
        del os.environ[unset_var]
    assert unset_var not in os.environ, (
        "Precondition failed -- could not provide an unset environment variable"
    )

    return unset_var


def test_model_is_transferable() -> None:
    """Ensures that environment variable names can be accessed from the model.

    This ensures that the name is accessible for any purpose that `e2e.env`
    alone does not serve, while still providing access to it via the same model
    instead of requiring users to maintain two mappings.
    """

    class IntEnv0(e2e.env.EnvMapper):
        int_zero: int = 'ENVTEST_INT_ZERO'  # type: ignore

    # Accessed via the class, it should still just be the env var name
    assert IntEnv0.int_zero == 'ENVTEST_INT_ZERO'


def test_raises_iff_var_does_not_exist_on_access() -> None:
    """Ensures that non-existant environment vars trigger exceptional behaviour.

    Though it is possible to communicate an unset environment variable via other
    means (e.g. returning `None` without trying to convert the type), it is
    generally a special condition for the caller and should be treated
    exceptionally.

    This also gives the opportunity to raise a helpful message.
    """

    class InvalidEnv(e2e.env.EnvMapper):
        dne: str = 'THIS_DEFINITELY_DOESNT_EXIST_123456'

    # Create on outside ; nothing should be raised yet, since we haven't asked
    env_inst = InvalidEnv()

    # Once accessed, it should raise to inform the caller.
    with pytest.raises(e2e.env.exceptions.NoSuchVariableError) as e:
        env_inst.dne
        pytest.fail("Non-existant should raise NoSuchVariableError on access.")

    assert 'THIS_DEFINITELY_DOESNT_EXIST_123456' in str(e.value)


def test_string_models(setenv: str) -> None:
    """Ensures that string-modeled variables output strings."""

    class StrEnv(e2e.env.EnvMapper):
        empty: str = 'ENVTEST_EMPTY'
        str1: str = 'ENVTEST_STR1'
        str2: str = 'ENVTEST_STR2'

    assert StrEnv().empty == ''
    assert StrEnv().str1 == 'env test str 1'
    assert StrEnv().str2 == 'env test str 2'


def test_int_models(setenv: str):
    """Ensures that int-modeled variables output ints."""

    os.environ['ENVTEST_INT_NEG'] = '-1'
    os.environ['ENVTEST_INT_ZERO'] = '0'
    os.environ['ENVTEST_INT_POS'] = '1'
    os.environ['ENVTEST_INT_POSPLUS'] = '+1'
    os.environ['ENVTEST_INT_BIG'] = '19223372036854775807'

    class IntEnv(e2e.env.EnvMapper):
        empty: int = 'ENVTEST_EMPTY'  # type: ignore
        negative: int = 'ENVTEST_INT_NEG'  # type: ignore
        zero: int = 'ENVTEST_INT_ZERO'  # type: ignore
        positive: int = 'ENVTEST_INT_POS'  # type: ignore
        big: int = 'ENVTEST_INT_BIG'  # type: ignore

    int_env = IntEnv()
    assert int_env.negative == -1
    assert int_env.zero == 0
    assert int_env.positive == 1
    assert int_env.big == 19223372036854775807

    with pytest.raises(ValueError):
        int_env.empty
        pytest.fail("Should raise original int('') exception")


def test_float_models(setenv: str) -> None:
    """Ensures that float-modeled variables output floats."""

    class FloatEnv(e2e.env.EnvMapper):
        empty: float = 'ENVTEST_EMPTY'  # type: ignore
        negative: float = 'ENVTEST_FLOAT_NEG'  # type: ignore
        zero: float = 'ENVTEST_FLOAT_ZERO'  # type: ignore
        positive: float = 'ENVTEST_FLOAT_POS'  # type: ignore

    float_env = FloatEnv()
    assert float_env.negative == -2.5
    assert float_env.zero == 0.0
    assert float_env.positive == 2.5
    with pytest.raises(ValueError):
        float_env.empty
        pytest.fail("Should raise original float('') exception")


def test_raises_attribute_error_logically():
    """Access of an unmapped name should raise the common exception."""

    class FooEnv(e2e.env.EnvMapper):
        bar: str = 'BAZ'

    foo_env = FooEnv()

    with pytest.raises(AttributeError):
        foo_env.does_not_exist_as_a_mapping
        pytest.fail("Should raise common AttributeError, as standard")
