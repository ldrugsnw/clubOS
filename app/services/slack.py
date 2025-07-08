from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from ..core.config import settings

# Slack 앱 초기화
app = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET
)

# FastAPI용 핸들러
handler = SlackRequestHandler(app)

@app.event("reaction_added")
def handle_reaction_added(event, say):
    """
    이모지 반응이 추가되었을 때 처리
    """
    try:
        # 이벤트 정보 추출
        item = event["item"]
        user = event["user"]
        reaction = event["reaction"]
        
        # TODO: 이벤트 참가 처리 로직 구현
        # 1. item.ts로 이벤트 찾기
        # 2. user로 회원 찾기
        # 3. 참가 정보 저장
        
    except Exception as e:
        say(f"Error processing reaction: {str(e)}")

@app.event("reaction_removed")
def handle_reaction_removed(event, say):
    """
    이모지 반응이 제거되었을 때 처리
    """
    try:
        # 이벤트 정보 추출
        item = event["item"]
        user = event["user"]
        reaction = event["reaction"]
        
        # TODO: 이벤트 참가 취소 처리 로직 구현
        # 1. item.ts로 이벤트 찾기
        # 2. user로 회원 찾기
        # 3. 참가 정보 삭제
        
    except Exception as e:
        say(f"Error processing reaction removal: {str(e)}")

# Slack 이벤트 핸들러 가져오기
async def get_slack_handler():
    return handler 