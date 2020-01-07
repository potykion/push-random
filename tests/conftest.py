from typing import cast

import pytest

from push_random.containers import AppContainer, TestContainer


@pytest.fixture()
def container() -> AppContainer:
    return cast(AppContainer, TestContainer)
