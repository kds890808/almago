from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    Text
)
from database import Base
from pydantic import BaseModel

# =========================
# 회원
# =========================
class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    name = Column(String)
    birth = Column(String)
    phone = Column(String)

    created_at = Column(String)

    is_premium = Column(Boolean, default=False)

    point = Column(Integer, default=0)
    referral_code = Column(String, unique=True, index=True)
    referred_by = Column(String)

# =========================
# 관리자
# =========================
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


# =========================
# 슈퍼관리자
# =========================
class SuperAdmin(Base):
    __tablename__ = "superadmins"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


# =========================
# 분석
# =========================
class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    is_premium = Column(Boolean, default=False)


# =========================
# 메뉴
# =========================
class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    path = Column(String)

    template = Column(String, default="link")

    icon = Column(String, default="📄")

    description = Column(String, default="")

    sort_order = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

# =========================
# 포인트 기록
# =========================
class PointHistory(Base):

    __tablename__ = "point_history"

    id = Column(Integer, primary_key=True)

    email = Column(String)

    type = Column(String)
    # charge / use

    amount = Column(Integer)

    remain_point = Column(Integer)

    description = Column(String)

    created_at = Column(String)


# =========================
# 경주전개분석
# =========================
class PaceAnalysis(Base):
    __tablename__ = "pace_analysis"

    id = Column(Integer, primary_key=True)

    지역 = Column(String)
    경주 = Column(Integer)
    경주일자 = Column(String)

    번호 = Column(Integer)
    마명 = Column(String)

    주행유형 = Column(String)
    최근흐름 = Column(String)
    전개패턴 = Column(String)
    코스적합 = Column(String)

    코멘트 = Column(String)
    점수 = Column(Integer)

# =========================
# 텔레그램 설정
# =========================
class TelegramSetting(Base):

    __tablename__ = "telegram_settings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    chat_id = Column(String)

    is_active = Column(
        Integer,
        default=1
    )

# =========================
# 텔레그램 설정 변경
# =========================
class TelegramSettingUpdate(BaseModel):

    chat_id: str

# =========================
# 경주 테이블
# =========================
class Race(Base):
    __tablename__ = "race"

    id = Column(Integer, primary_key=True, index=True)
    지역 = Column(String)
    마명=Column(String)
    순 = Column(Integer)
    경주일자 = Column(String)
    경주 = Column(Integer)
    등급 = Column(String)
    거리 = Column(String)
    편성 = Column(String)
    출전 = Column(String)
    경주명 = Column(String)
    출발시각 = Column(String)
    비고 = Column(String)
    취소마 = Column(Integer, default=0)

    # =========================
# 분석 테이블
# =========================
class RaceAnalysis(Base):
    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True, index=True)

    region = Column(String)
    race_no = Column(Integer)
    race_date = Column(String)

    star = Column(String)
    square = Column(String)
    empty = Column(String)
    up = Column(String)
    triangle = Column(String)
    darkhorse = Column(String)

    single = Column(String)
    double = Column(String)
    triple = Column(String)

# =========================
# 경주상세 테이블
# =========================
class RaceDetail(Base):

    __tablename__="race_detail"

    id=Column(Integer,primary_key=True,index=True)

    경주일자=Column(String)
    지역=Column(String)
    경주=Column(Integer)

    번호=Column(String)
    마명=Column(String)
    성별=Column(String)
    나이=Column(String)

    기수=Column(String)
    조교사=Column(String)

    부담중량=Column(String)
    체중=Column(String)

    레이팅=Column(String)
    증감=Column(String)
    마주명=Column(String)
    조교횟수=Column(String)
    출전주기=Column(String)
    장구현황=Column(String)
    특이사항=Column(String)
    마종=Column(String)
    최근전적=Column(String)

# =========================
# 경주마 테이블
# =========================
class Horse(Base):

    __tablename__="horse"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    hr_no=Column(String)

    마명=Column(String)
    성별=Column(String)
    나이=Column(String)

    생년월일=Column(String)

    기수=Column(String)
    조교사=Column(String)
    마주=Column(String)

    부마=Column(String)
    모마=Column(String)

    통산전적=Column(String)
    승률=Column(String)

    수득상금=Column(String)
    특징=Column(String)

    최근전적=Column(String)    

# =========================
# 기수 테이블
# =========================
class Jockey(Base):

    __tablename__="jockey"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    jk_no=Column(String)

    지역명=Column(String)
    기수명=Column(String)

    생년월일=Column(String)
    데뷔일자=Column(String)
    기승가능중량=Column(String)

    통산전적=Column(String)

    통산승률=Column(String)
    통산복승률=Column(String)
    통산연승률=Column(String)

    최근1년=Column(String)

    최근1년승률=Column(String)
    최근1년복승률=Column(String)
    최근1년연승률=Column(String)    

# =========================
# 위탁관리말
# =========================
class TrainerHorse(Base):

    __tablename__="trainer_horse"

    id=Column(Integer,primary_key=True,index=True)

    tr_no=Column(String)

    마명=Column(String)
    마주명=Column(String)

    조번=Column(String)
    등급=Column(String)

    레이팅=Column(String)

    산지=Column(String)
    성별=Column(String)

    연령=Column(String)

    데뷔일자=Column(String)

    전적=Column(String)    

# =========================
# 연도별성적
# =========================
class TrainerYear(Base):

    __tablename__="trainer_year"

    id=Column(Integer,primary_key=True,index=True)

    tr_no=Column(String)

    연도=Column(String)

    출전=Column(String)

    일위=Column(String)
    이위=Column(String)
    삼위=Column(String)

    승률=Column(String)
    복승률=Column(String)
    연승률=Column(String)

    순위상금=Column(String)    

# =========================
# 최근1개월
# =========================
class TrainerRecent(Base):

    __tablename__="trainer_recent"

    id=Column(Integer,primary_key=True,index=True)

    tr_no=Column(String)

    경주일자=Column(String)

    마번=Column(String)
    마명=Column(String)

    기수명=Column(String)

    등급=Column(String)

    순위=Column(String)

    중량=Column(String)

    거리=Column(String)

    기록=Column(String)

    도착차=Column(String)

    마체중=Column(String)


# =========================
# 조교사 테이블
# =========================
class Trainer(Base):

    __tablename__="trainer"

    id=Column(
        Integer,
        primary_key=True,
        index=True
    )

    tr_no=Column(String)

    지역명=Column(String)
    조교사명=Column(String)

    데뷔일자=Column(String)

    통산전적=Column(String)

    통산승률=Column(String)
    통산복승률=Column(String)
    통산연승률=Column(String)

    최근1년=Column(String)

    최근1년승률=Column(String)
    최근1년복승률=Column(String)
    최근1년연승률=Column(String)


# =========================
# 혈통테이블
# =========================
class Blood(Base):

    __tablename__="blood"

    id=Column(Integer, primary_key=True, index=True)

    출전날짜=Column(String)

    지역=Column(String)
    meet=Column(String)

    경주번호=Column(String)
    거리=Column(String)

    표번호=Column(String)
    원본URL=Column(String)

    번호=Column(String)

    부마=Column(String)
    모마=Column(String)
    외조부마=Column(String)

    도시지프로필=Column(String)

    DI=Column(String)
    CD=Column(String)

    근친=Column(String)

    AWD=Column(String)
    부AWD=Column(String)
    모AWD=Column(String)
    모부AWD=Column(String)

    마명=Column(String)

    연령=Column(String)
    레이팅=Column(String)

    최근순위=Column(String)
    도착차=Column(String)

    경주성적=Column(String)

    기수=Column(String)
    기수복승률=Column(String)

    부담중량=Column(String)

    최고기록=Column(String)
    평균기록=Column(String)

    평균S1F=Column(String)
    평균G3F=Column(String)
    평균G1F=Column(String)

    최고G3F=Column(String)

    통산펄롱=Column(String)
    통산부담=Column(String)

    평균경주전개=Column(String)

    전적=Column(String)
    현군성적=Column(String)

    상금비율=Column(String)

    훈련량수영훈련=Column(String)
    평균훈련량=Column(String)

    수입전경주성적=Column(String)

    경매가수입가=Column(String)

    조교사=Column(String)    

# =========================
# 기본분석 테이블
# =========================
class BasicAnalysis(Base):

    __tablename__ = "basic_analysis"

    id = Column(Integer, primary_key=True)

    지역 = Column(String)
    경주 = Column(Integer)
    경주일자 = Column(String)

    번호 = Column(Integer)
    마명 = Column(String)

    기본점수 = Column(Integer)
    기본코멘트 = Column(String)

    혈통점수 = Column(Integer)
    혈통코멘트 = Column(String)

    전개점수 = Column(Integer)
    전개코멘트 = Column(String)

    종합점수 = Column(Integer)
    종합코멘트 = Column(String)


# =========================
# 혈통분석 테이블
# =========================

class BloodAnalysis(Base):

    __tablename__ = "blood_analysis"

    id = Column(Integer, primary_key=True)

    지역 = Column(String)
    경주 = Column(Integer)
    경주일자 = Column(String)

    번호 = Column(Integer)
    마명 = Column(String)

    도시지프로필 = Column(String)

    DI = Column(String)
    CD = Column(String)

    근친 = Column(String)

    AWD = Column(String)
    부AWD = Column(String)
    모AWD = Column(String)
    모부AWD = Column(String)

    경주마특성 = Column(String)
    거리적합 = Column(String)

    코멘트 = Column(String)

    점수 = Column(Integer)    


# =========================
# 종합분석 테이블
# =========================
class FinalAnalysis(Base):

    __tablename__ = "final_analysis"

    id = Column(Integer, primary_key=True, index=True)

    예상순위 = Column(Integer)

    번호 = Column(Integer)
    마명 = Column(String)

    종합점수 = Column(Float)

    실전점수 = Column(Float)
    최근폼점수 = Column(Float)
    혈통점수 = Column(Float)
    거리점수 = Column(Float)
    주로점수 = Column(Float)

    RI = Column(Float)
    CPI = Column(Float)
    SPR = Column(Float)

    평균속도지수 = Column(Float)
    최대속도지수 = Column(Float)

    DI = Column(Float)
    CD = Column(Float)
    COI = Column(Float)

    승률 = Column(Float)
    복승률 = Column(Float)
    연승률 = Column(Float)

    오착내율 = Column(Float)

    최근5전평균착순 = Column(Float)
    최근10전평균착순 = Column(Float)

    주행유형 = Column(String)

    과거최적거리 = Column(String)
    과거최적주로 = Column(String)

    추천사유 = Column(Text)

    위험등급 = Column(String)
    추천유형 = Column(String)
    최종추천 = Column(String)

    RI순위 = Column(Integer)
    CPI순위 = Column(Integer)
    SPR순위 = Column(Integer)

    승률순위 = Column(Integer)
    복승률순위 = Column(Integer)
    연승률순위 = Column(Integer)

    폼순위 = Column(Integer)
    혈통순위 = Column(Integer)

    강점 = Column(Text)
    약점 = Column(Text)

    종합코멘트 = Column(Text)

    기수명 = Column(String)
    조교사명 = Column(String)

    중량 = Column(Float)

    기수점수 = Column(Float)
    조교사점수 = Column(Float)
    부담중량점수 = Column(Float)

    날짜 = Column(String)

    지역 = Column(String)
    경주번호 = Column(Integer)

    최근순위 = Column(String)

    평균경주전개 = Column(String)

    도착차 = Column(String)

    평균S1F = Column(String)

    평균G1F = Column(String)

    평균훈련량 = Column(String)

    수영훈련 = Column(String)


# =========================
# 이용요금 설정 테이블
# =========================
# =========================
# 포인트 정책
# =========================
class FeeSetting(Base):

    __tablename__ = "fee_settings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # 내부키
    item = Column(
        String,
        unique=True
    )

    # 관리자에 보여줄 이름
    name = Column(
        String
    )

    # 이용요금 / 일일보상 / 회원보상 ...
    category = Column(
        String
    )

    # 지급 또는 차감 포인트
    point = Column(
        Integer,
        default=0
    )

    # 표시순서
    sort_order = Column(
        Integer,
        default=0
    )

    # 사용여부
    is_active = Column(
        Boolean,
        default=True
    )

    # 설명
    description = Column(
        String,
        default=""
    )



# =========================
# 충전상품 설정
# =========================
class ChargeSetting(Base):

    __tablename__ = "charge_settings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)

    point = Column(Integer)

    price = Column(Integer)

    sort_order = Column(
        Integer,
        default=0
    )

    is_active = Column(
        Integer,
        default=1
    )    




# =========================
# 충전신청
# =========================
class ChargeRequest(Base):

    __tablename__ = "charge_requests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(String)

    depositor_name = Column(String)

    product_name = Column(String)

    point = Column(Integer)

    amount = Column(Integer)

    status = Column(
        String,
        default="대기"
    )

    created_at = Column(String)

    processed_at = Column(String)    


  

# =========================
# 입금계좌 설정
# =========================
class ChargeAccount(Base):

    __tablename__ = "charge_account"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    bank_name = Column(String)

    account_number = Column(String)

    account_holder = Column(String)

    notice = Column(String)    


# =========================
# 이용요금 변경 비밀번호
# =========================
class FeePassword(Base):

    __tablename__ = "fee_password"

    id = Column(Integer, primary_key=True)

    password = Column(String)

# =========================
# 출석체크
# =========================
class Attendance(Base):

    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)

    member_id = Column(Integer)

    attend_date = Column(String)

    streak = Column(Integer, default=1)

    reward = Column(Integer, default=10)

    created_at = Column(String)

# =========================
# 퀴즈히스토리
# =========================
class QuizHistory(Base):

    __tablename__ = "quiz_history"

    id = Column(Integer, primary_key=True)

    member_id = Column(Integer)

    quiz_date = Column(String)

    quiz_id = Column(Integer)

    is_correct = Column(Boolean)

    point = Column(Integer)