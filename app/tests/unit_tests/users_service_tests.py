
import pytest

from app.users.service import UsersService


@pytest.mark.parametrize('user_id, email, user_exists', [
    (1, 'first@test.com', True),
    (2, 'second@test.com', True),
    (99, 'nonexistent', False)
])
async def test_find_user_by_id(user_id, email, user_exists):
    user = await UsersService.get_by_id(user_id)

    if user_exists:
        assert user
        assert user.email == email
    else:
        assert not user
