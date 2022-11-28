import pytest
from donaldson_asu_twitter.HandleManagement import ManageHandles

@pytest.mark.parametrize("input, expected", [
    ('bob',[]),
    ('volvocars',[342772500])
])
def test_get_twitter_id_by_handle(input, expected):
    assert ManageHandles.get_twitter_id_by_handle(input) == expected

@pytest.mark.parametrize("handle_to_test, expected", [
    ('bob',False),
    ('volvocars',True),
    ('volvocars_',True),
    ('volvocars.',False),
    ('v456',True),
    ('_vrtf_',True),
    ('one',False),
    ('one_',True),
    ('',False),
    ('fdasjklfadjklfadjklfasdkfadskjlfdsakjadfsk',False),
    ('@wookies',False),
    ('@_wookies',False),
    ('IAMTHEWALRUS',True),
    ('N/A',False)
])
def test_handle_validity(handle_to_test, expected):
    assert ManageHandles.check_username_validity(handle_to_test) == expected