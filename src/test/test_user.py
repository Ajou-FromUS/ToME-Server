import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def user():
    """Dummy User for Testing"""

    return {
        "user_id": 25,
        "nickname": "dummy",
        "access_token": "asdas",
        "refresh_token": "asdasd"
    }


def test_create_user(test_app: TestClient, user):
    """Testcase: Creating User"""

    response = test_app.post('/user', json=user)

    assert response.status_code == 200
    assert response.json()["detail"] == "사용자 생성 성공"


def test_create_user_less_info(test_app: TestClient, user):
    """Testcase: Creating User Failed Due to Lack of Mandatory Field"""

    del user["access_token"]
    response = test_app.post('/user', json=user)

    assert response.status_code == 422
    assert response.json()["detail"] == "필수 항목 중 일부가 누락되었습니다"


def test_create_user_dup(test_app: TestClient, user):
    """Testcase: Creating User Failed Due to Duplicated User"""

    response = test_app.post('/user', json=user)

    assert response.status_code == 400
    assert response.json()["detail"] == "이미 존재하는 사용자입니다"


def test_get_user(test_app: TestClient, user):
    """Testcase: Getting User"""

    response = test_app.get(f"/user/{user['user_id']}")

    assert response.status_code == 200
    assert response.json()["detail"] == "사용자 조회 성공"


def test_get_user_no_matching_user(test_app: TestClient, user):
    """Testcase: Getting User Failed Due to No Matching User"""

    response = test_app.get(f"/user/{user['user_id'] + 1}")

    assert response.status_code == 404
    assert response.json()["detail"] == "일치하는 사용자가 존재하지 않습니다"


def test_update_user(test_app: TestClient, user):
    """Testcase: Updating User"""

    user["nickname"] = "수정_테스트"
    response = test_app.patch(f"/user/{user['user_id']}", json=user)

    assert response.status_code == 200
    assert response.json()["detail"] == "사용자 업데이트 성공"


def test_update_user_no_matching_user(test_app: TestClient, user):
    """Testcase: Updating User Failed Due to No Matching User"""

    user["nickname"] = "수정_테스트"
    response = test_app.patch(f"/user/{user['user_id'] + 1}", json=user)

    assert response.status_code == 404
    assert response.json()["detail"] == "일치하는 사용자가 존재하지 않습니다"


def test_update_user_no_matching_field(test_app: TestClient, user):
    """Testcase: Updating User Failed Due to No Matching Field"""

    user["test_field"] = "test_data"
    response = test_app.patch(f"/user/{user['user_id']}", json=user)

    assert response.status_code == 422
    assert response.json()["detail"] == "일치하는 항목이 존재하지 않습니다"


def test_delete_user(test_app: TestClient, user):
    """Testcase: Deleting User"""

    response = test_app.delete(f"/user/{user['user_id']}")

    assert response.status_code == 200
    assert response.json()["detail"] == "사용자 삭제 성공"


def test_delete_user_no_matching_user(test_app: TestClient, user):
    """Testcase: Deleting User Failed Due to No Matching User"""

    response = test_app.delete(f"/user/{user['user_id']}")

    assert response.status_code == 404
    assert response.json()["detail"] == "일치하는 사용자가 존재하지 않습니다"
