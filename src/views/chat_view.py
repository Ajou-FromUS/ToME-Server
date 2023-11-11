from fastapi import HTTPException, status
from redis import Redis
from bardapi import BardCookies
import time
import traceback

# 채팅 답변 요청
def chat(chat_data: dict, redis_client: Redis, token: str):
# def chat(chat_data: dict, redis_client: Redis):
    # 필수 항목 누락 체크
    required_fields = ['content']
    if not all(field in chat_data for field in required_fields):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="필수 항목 중 일부가 누락되었습니다")

    try:
        # test
        # token={'uid':'dummy'}

        uid = token['uid']

        cookie_dict = redis_client.hgetall('cookies')

        bard = BardCookies(cookie_dict=cookie_dict)

        length = '20'

        user_text = chat_data['content']

        input_text = f'''
        너는 앞으로 말투를 친구랑 대화하듯이 해줘. 답변은 꼭 {length}자 이내로 해주고, 답변을 할 때에는 내 말에 대한 공감과 질문도 함께 해줘야 돼.
        답변은 대괄호로 감싸줘. 다음 말에 대해 답변을 해줘.

        {user_text}
        '''

        start_time = time.time()
        response=bard.get_answer(input_text)['content']
        end_time = time.time()
        elapsed_time = end_time-start_time

        
        start_idx = response.find('[')
        end_idx = response.find(']')
        answer = response[start_idx+1:end_idx]
        print(f"uid: {uid} Elapsed Time: {elapsed_time} Input Text: {user_text} Output Text: {answer}")
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "채팅 답변 생성 성공",
            "message": answer
        }
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="채팅 답변 생성 중 서버에 오류가 발생하였습니다")