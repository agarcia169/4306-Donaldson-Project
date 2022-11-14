import pytest
from donaldson_asu_twitter.HandleManagement import ManageHandles

@pytest.mark.parametrize("input, expected", [
    ('bob',[]),
    ('volvocars',[342772500])
])
def test_get_twitter_id_by_handle(input, expected):
    assert ManageHandles.get_twitter_id_by_handle(input) == expected