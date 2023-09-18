from fastapi.testclient import TestClient

# from app.main import app
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/user",
                           json={
                               "user_id":1,
                               "nickname":"dummy",
                               "access_token":"abcdef",
                               "refresh_token":"abcdefg"
                           })
    assert response.status_code == 200
    # assert response.json() == {
    #     "status_code": 200,
    #     "message": "사용자 생성 성공"
    # }

def test_create_user_less_info():
    response = client.post("/user",
                           json={
                               "user_id":1,
                               "nickname":"dummy",
                               "access_token":"abcdef"
                           })
    assert response.status_code == 400
    assert response.json() == {
        "detail": "입력값에 빈 항목이 있습니다" # 이거 포맷 통일해야할듯
    }

def test_create_user_dup(): # 이게 왜 200이 나오는지? user_id 확인해서 중복되었는지 확인해야함
    response = client.post("/user",
                           json={
                               "user_id":1,
                               "nickname":"dummy",
                               "access_token":"abcdef",
                               "refresh_token":"abcdefg"
                           })
    assert response.status_code == 500
    assert response.json() == {
        "message": "사용자 생성 실패"
    }

# def test_create_user_fail(): # 이게 왜 200이 나오는지? user_id 확인해서 중복되었는지 확인해야함
#     response = client.post("/user",
#                            json={
#                                "user_id":1,
#                                "nickname":"dummy",
#                                "access_token":"abcdef",
#                                "refresh_token":"abcdefg"
#                            })
#     assert response.status_code == 500
#     assert response.json() == {
#         "message": "사용자 생성 실패"
#     }

def test_get_user():
    response = client.get("/user/1")
    assert response.status_code == 200
    # assert response.json() == {
    #     "status_code": 200,
    #     "message": "사용자 조회 성공"
    # }

def test_get_user_fail():
    response = client.get("/user/3") # 쿼리해서 아무것도 안 나와도 200임
    assert response.status_code == 500
    assert response.json() == {
        "message": "사용자 조회 실패"
    }

def test_update_user():
    response = client.patch("/user/1",json={
        "nickname":"nickname-changed"
    })
    assert response.status_code==200
    # assert response.json() == {
    #     "status_code": 200,
    #     "message": "사용자 업데이트 성공"
    # }

def test_update_user_fail(): # 없는 유저에 대해 업데이트 요청을 해도 200..?
    response = client.patch("/user/3",json={
        "nickname":"nickname-changed"
    })
    assert response.status_code==500
    assert response.json() == {
        "message": "사용자 업데이트 실패"
    }

def test_delete_user():
    response = client.delete("/user/1")
    assert response.status_code==200
    # assert response.json() == {
    #     "status_code": 200,
    #     "message": "사용자 삭제 성공"
    # }

def test_delete_user_fail(): # 이게 왜 200??
    response = client.delete("/user/1")
    assert response.status_code==400
    assert response.json() == {
        "message": "사용자 삭제 실패"
    }