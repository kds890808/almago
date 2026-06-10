from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request, Body
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from database import SessionLocal, engine, Base
import models, schemas
from models import (
    Member,
    Admin,
    SuperAdmin,
    Menu,
    PointHistory,
    PaceAnalysis
)
from schemas import MenuCreate
from passlib.context import CryptContext
from auth import create_access_token 
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pandas as pd
from playwright.sync_api import sync_playwright
import os
from sqlalchemy import text
import subprocess
from pydantic import BaseModel
class FindAccountRequest(BaseModel):
    name: str
    birth: str
    phone: str


class ResetPasswordRequest(BaseModel):
    email: str
    name: str
    birth: str
    phone: str
    new_password: str


print("🔥 현재 DB 위치:", os.path.abspath("db.sqlite3"))
from database import DATABASE_URL

print("🔥 현재 DATABASE_URL:", DATABASE_URL)

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
    
# =========================
# 분석 테이블
# =========================
class raceAnalysis(Base):
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

Base.metadata.create_all(bind=engine)

with engine.connect() as conn:

    pass
    
    # race_detail 컬럼 추가
    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "나이" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "기수" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        ##ADD COLUMN IF NOT EXISTS "조교사" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "부담중량" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "체중" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "최근전적" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "레이팅" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "증감" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "마주명" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "조교횟수" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "출전주기" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "장구현황" VARCHAR
    #"""))

    #conn.execute(text("""
        ##ALTER TABLE race_detail
        #ADD COLUMN IF NOT EXISTS "특이사항" VARCHAR
    #"""))

    # horse
    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "성별" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "나이" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "최근전적" VARCHAR
    #"""))

with engine.connect() as conn:

    pass

# =========================
# horse
# =========================
    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "성별" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "나이" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "최근전적" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "생년월일" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "기수" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "조교사" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "마주" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "부마" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "모마" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "통산전적" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "승률" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "수득상금" VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE horse
        #ADD COLUMN IF NOT EXISTS "특징" VARCHAR
    #"""))
    # 👆 여기까지 추가

    #conn.execute(text("""
    #ALTER TABLE race
    #ADD COLUMN IF NOT EXISTS "마명" VARCHAR
    #"""))

# =========================
# jockey
# =========================

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "지역명" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "생년월일" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "데뷔일자" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "기승가능중량" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "통산전적" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "통산승률" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "통산복승률" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "통산연승률" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "최근1년" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "최근1년승률" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "최근1년복승률" VARCHAR
    #"""))

    #conn.execute(text("""
    #ALTER TABLE jockey
    #ADD COLUMN IF NOT EXISTS "최근1년연승률" VARCHAR
    #"""))


#with engine.connect() as conn:



    # =========================
    # trainer
    # =========================
    #for col in [

        #"지역명",
        #"데뷔일자",

        #"통산전적",
        #"통산승률",
        #"통산복승률",
        #"통산연승률",

        #"최근1년",
        #"최근1년승률",
        #"최근1년복승률",
        #"최근1년연승률"

    #]:

        #conn.execute(text(
            #f'''
            #ALTER TABLE trainer
            #ADD COLUMN IF NOT EXISTS "{col}" VARCHAR
            #'''
        #))

    #conn.commit()

with engine.connect() as conn:

    #conn.execute(text("""
        #ALTER TABLE menus
        #ADD COLUMN IF NOT EXISTS template VARCHAR
    #"""))

    #conn.execute(text("""
        #ALTER TABLE members
        #ADD COLUMN IF NOT EXISTS "point" INTEGER DEFAULT 0
    #"""))

    conn.commit()

app = FastAPI()

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
security = HTTPBearer()

# =========================
# 기본분석점수
# =========================

class BasicAnalysisSave(
    BaseModel

):
    지역:str
    경주:int
    경주일자:str

    번호:int
    마명:str

    코멘트:str
    점수:int

def calc_basic_score(
    horse,
    jockey,
    trainer
):

    score = 0

    # =====================
    # 기수 승률
    # =====================

    try:
        jockey_rate = float(
            str(
                jockey.최근1년승률
            ).replace("%", "")
        )
    except:
        jockey_rate = 0

    # =====================
    # 조교사 승률
    # =====================

    try:
        trainer_rate = float(
            str(
                trainer.최근1년승률
            ).replace("%", "")
        )
    except:
        trainer_rate = 0

    score += jockey_rate * 1.5
    score += trainer_rate * 1.2

    # =====================
    # 수득상금
    # =====================

    try:
        prize = int(
            str(
                horse.수득상금
            )
            .replace(",", "")
            .replace("원", "")
        )

    except:
        prize = 0

    if prize >= 5000000:
        score += 20

    elif prize >= 2000000:
        score += 15

    elif prize >= 500000:
        score += 10

    # =====================
    # 통산전적
    # =====================

    try:

        race_count = int(
            str(
                horse.통산전적
            ).split("전")[0]
        )

    except:

        race_count = 0

    score += min(
        race_count,
        20
    )

    score = round(score)

    # =====================
    # 플래그
    # =====================

    flags = []

    if jockey_rate >= 20:

        flags.append(
            "🔥 기수 강세"
        )

    if trainer_rate >= 15:

        flags.append(
            "🎯 조교사 강세"
        )

    if prize >= 5000000:

        flags.append(
            "💰 상금 우위"
        )

    if race_count >= 10:

        flags.append(
            "🐎 경험 우위"
        )

    if race_count <= 1:

        flags.append(
            "⚠️ 검증 필요"
        )

    # =====================
    # DH 등급
    # =====================

    if score >= 80:

        dh = "A+ 강력추천"

    elif score >= 60:

        dh = "A 입상유력"

    elif score >= 40:

        dh = "B+ 복병주의"

    else:

        dh = "C 관망"

    # =====================
    # 코멘트 생성
    # =====================

    comment = dh + "\n\n"

    if flags:

        comment += (
            "\n".join(flags)
            + "\n\n"
        )

    if score >= 80:

        comment += (
            "이번 경주에서는 가장 눈에 띄는 전력으로 평가됩니다.\n"
            "기수와 조교사 전력이 모두 안정적인 모습을 보이고 있습니다.\n"
            "기본 능력과 경험에서도 경쟁마 대비 우위를 가지고 있습니다.\n"
            "큰 이변이 없다면 우승권 경쟁이 충분히 가능해 보입니다."
        )

    elif score >= 60:

        comment += (
            "전체적인 전력은 상위권 수준으로 평가됩니다.\n"
            "기본 능력과 최근 흐름도 비교적 안정적입니다.\n"
            "전개가 무난하게 풀린다면 입상권 경쟁이 가능합니다.\n"
            "이번 경주에서는 관심마로 볼 만합니다."
        )

    elif score >= 40:

        comment += (
            "객관적인 전력은 중위권 수준으로 평가됩니다.\n"
            "일부 강점은 있으나 불안요소도 함께 존재합니다.\n"
            "경주 흐름에 따라 충분히 변수가 될 수 있습니다.\n"
            "복병으로는 관심을 가져볼 만합니다."
        )

    else:

        comment += (
            "현재 전력만 놓고 보면 쉽지 않은 경주가 예상됩니다.\n"
            "기수와 조교사 전력에서도 뚜렷한 강점은 보이지 않습니다.\n"
            "최근 성적과 경험 면에서도 보완이 필요한 모습입니다.\n"
            "다만 경마 특성상 이변 가능성은 항상 존재합니다."
        )

    return score, comment

# =========================
# 혈통분석
# =========================
class BloodAnalysisSave(BaseModel):

    지역:str
    경주:int
    경주일자:str

    번호:int
    마명:str

    도시지프로필:str=""

    DI:str=""
    CD:str=""
    근친:str=""

    AWD:str=""
    부AWD:str=""
    모AWD:str=""
    모부AWD:str=""

    거리적합:str=""
    경주마특성:str=""

    코멘트:str=""
    점수:int=0

# =========================
# DB 연결
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# =========================
# 현재 로그인 사용자
# =========================
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email = payload.get("sub")
        role = payload.get("role")

        if not email or not role:
            raise HTTPException(401, "인증 실패")

        return {
            "email": email,
            "role": role
        }

    except Exception:
        raise HTTPException(401, "인증 실패")


def require_admin(current=Depends(get_current_user)):
    if current["role"] not in ["admin", "superadmin"]:
        raise HTTPException(403, "관리자만 가능")
    return current


def require_superadmin(current=Depends(get_current_user)):
    if current["role"] != "superadmin":
        raise HTTPException(403, "슈퍼관리자만 가능")
    return current


# =========================
# 회원가입
# =========================
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    exist = db.query(Member).filter(Member.email == user.email).first()
    if exist:
        raise HTTPException(400, "이미 존재하는 이메일")

    new_user = Member(
        email=user.email,
        password=hash_password(user.password),
        name=user.name,
        birth=user.birth,
        phone=user.phone,
        is_premium=False,
        point=0
    )

    db.add(new_user)
    db.commit()

    return {"msg": "회원가입 완료"}


# =========================
# 로그인
# =========================
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    print("===== LOGIN =====")
    print("LOGIN EMAIL =", repr(user.email))

    try:

        all_superadmins = db.query(
            SuperAdmin
        ).all()

        print(
            "SUPERADMIN COUNT =",
            len(all_superadmins)
        )

        for s in all_superadmins:

            print(
                "DB SUPERADMIN =",
                repr(s.email)
            )

    except Exception as e:

        print(
            "SUPERADMIN ERROR =",
            str(e)
        )

    member = db.query(Member).filter(
        Member.email == user.email
    ).first()

    admin = db.query(Admin).filter(
        Admin.email == user.email
    ).first()

    superadmin = db.query(SuperAdmin).filter(
        SuperAdmin.email == user.email
    ).first()

    print("member =", member)
    print("admin =", admin)
    print("superadmin =", superadmin)

    target = member or admin or superadmin

    if not target:
        print("❌ 계정 없음")
        raise HTTPException(400, "로그인 실패")

    ok = verify_password(
        user.password,
        target.password
    )

    print(
        "password check =",
        ok
    )

    if not ok:
        print("❌ 비밀번호 불일치")
        raise HTTPException(400, "로그인 실패")

    # 역할 판별
    if superadmin:
        role = "superadmin"

    elif admin:
        role = "admin"

    else:
        role = "member"

    token = create_access_token(
        {
            "sub": target.email,
            "role": role
        }
    )

    print("✅ 로그인 성공")
    print("ROLE =", role)

    return {
        "access_token": token,
        "role": role
    }

@app.get("/me")
def read_me(current=Depends(get_current_user)):
    return current


# =========================
# 회원 관리
# =========================
@app.get("/members")
def get_members(
    db: Session = Depends(get_db),
    current=Depends(require_admin)
):
    return db.query(Member).all()


@app.put("/members/{member_id}")
def update_member(
    member_id: int,
    is_premium: bool = False,
    db: Session = Depends(get_db),
    current=Depends(require_admin)
):
    member = db.query(Member).filter(Member.id == member_id).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    member.is_premium = is_premium
    db.commit()

    return {"msg": "회원 수정 완료"}


@app.delete("/members/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_admin)
):
    member = db.query(Member).filter(Member.id == member_id).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    db.delete(member)
    db.commit()

    return {"msg": "회원 삭제 완료"}


@app.post("/upgrade")
def upgrade_user(
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    member = db.query(Member).filter(Member.email == current["email"]).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    member.is_premium = True
    db.commit()

    return {"msg": "유료 사용자로 전환 완료"}

# =========================
# 슈퍼관리자 생성
# =========================
@app.post("/superadmin/create")
def create_superadmin(
    email:str,
    password:str,
    db:Session=Depends(get_db)
):

    all_data = db.query(
        SuperAdmin
    ).all()

    print(
        "CREATE SUPERADMIN COUNT =",
        len(all_data)
    )

    for s in all_data:

        print(
            "CREATE SUPERADMIN EMAIL =",
            repr(s.email)
        )

    exist = db.query(
        SuperAdmin
    ).filter(
        SuperAdmin.email == email
    ).first()

    print(
        "CREATE EXIST =",
        exist
    )

    if exist:
        raise HTTPException(
            400,
            "이미 존재하는 슈퍼관리자"
        )

    new = SuperAdmin(
        email=email,
        password=hash_password(password)
    )

    db.add(new)
    db.commit()

    return {
        "msg":"슈퍼관리자 생성 완료"
    }


# =========================
# 관리자 관리
# =========================
@app.post("/admin/create")
def create_admin(
    email: str,
    password: str,
    db: Session = Depends(get_db),
    current=Depends(require_superadmin)
):
    exist = db.query(Admin).filter(Admin.email == email).first()
    if exist:
        raise HTTPException(400, "이미 존재하는 관리자")

    new_admin = Admin(
        email=email,
        password=hash_password(password)
    )

    db.add(new_admin)
    db.commit()

    return {"msg": "관리자 생성 완료"}


@app.get("/admins")
def get_admins(
    db: Session = Depends(get_db),
    current=Depends(require_superadmin)
):
    return db.query(Admin).all()


@app.delete("/admins/{admin_id}")
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_superadmin)
):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()

    if not admin:
        raise HTTPException(404, "관리자 없음")

    db.delete(admin)
    db.commit()

    return {"msg": "관리자 삭제 완료"}


# =========================
# 분석 글 관리
# =========================
@app.post("/analyses")
def create_analysis(
    data: schemas.AnalysisCreate,
    db: Session = Depends(get_db),
    current=Depends(require_admin)
):
    new_data = models.Analysis(
        title=data.title,
        content=data.content,
        is_premium=data.is_premium
    )

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return new_data


@app.get("/analyses", response_model=list[schemas.AnalysisOut])
def get_analyses(
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    if current["role"] in ["admin", "superadmin"]:
        return db.query(models.Analysis).all()

    member = db.query(Member).filter(Member.email == current["email"]).first()

    if member and member.is_premium:
        return db.query(models.Analysis).all()

    return db.query(models.Analysis).filter(models.Analysis.is_premium == False).all()


@app.put("/analyses/{analysis_id}")
def update_analysis(
    analysis_id: int,
    data: schemas.AnalysisCreate,
    db: Session = Depends(get_db),
    current=Depends(require_admin)
):
    analysis = db.query(models.Analysis).filter(models.Analysis.id == analysis_id).first()

    if not analysis:
        raise HTTPException(404, "데이터 없음")

    analysis.title = data.title
    analysis.content = data.content
    analysis.is_premium = data.is_premium

    db.commit()

    return {"msg": "수정 완료"}


@app.delete("/analyses/{analysis_id}")
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_admin)
):
    analysis = db.query(models.Analysis).filter(models.Analysis.id == analysis_id).first()

    if not analysis:
        raise HTTPException(404, "데이터 없음")

    db.delete(analysis)
    db.commit()

    return {"msg": "삭제 완료"}


# =========================
# 메뉴 관리
# =========================
@app.post("/menus")
def create_menu(
    data: MenuCreate,
    db: Session = Depends(get_db),
    current=Depends(require_admin)
):
    menu = Menu(
    name=data.name,
    path=data.path,
    template=data.template,
    icon=data.icon,
    description=data.description,
    sort_order=data.sort_order,
    is_active=data.is_active
)
    db.add(menu)
    db.commit()
    db.refresh(menu)

    return menu


@app.get("/menus")
def get_menus(db: Session = Depends(get_db)):

    try:
        return db.query(Menu)\
            .order_by(Menu.sort_order.asc())\
            .all()

    except Exception as e:
        return {"error": str(e)}


@app.delete("/menus/{menu_id}")
def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_admin)
):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()

    if not menu:
        raise HTTPException(404, "메뉴 없음")

    db.delete(menu)
    db.commit()

    return {"msg": "삭제 완료"}


# =========================
# 경주 업로드
# =========================
@app.post("/upload-race")
async def upload_race(file: UploadFile = File(...)):
    df = pd.read_excel(file.file)

    # 🔥 컬럼명 정리
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("▲","")
    )

    print(
        "상세컬럼:",
        df.columns.tolist()
    )

    db = SessionLocal()

    db.query(Race).delete()

    for _, row in df.iterrows():

        try:

            print(
                "출전표행:",
                row.to_dict()
            )

            race = Race(

                지역 = clean(
                    row.get("지역","")
                ),

                마명 = clean(
                    row.get("마명",
                    row.get("출전마",
                    row.get("출전마명","")))
                ),
                
                순 = int(
                    row.get("순",0)
                ),

                경주일자 = clean(
                    row.get("경주일자","")
                ),

                경주 = int(
                    row.get("경주",0)
                ),

                등급 = clean(
                    row.get("등급","")
                ),

                거리 = clean(
                    row.get("거리","")
                ),

                편성 = clean(
                    row.get("편성","")
                ),

                출전 = clean(
                    row.get("출전","")
                ),

                경주명 = clean(
                    row.get("경주명","")
                ),

                출발시각 = clean(
                    row.get("출발시각","")
                ),

                비고 = clean(
                    row.get("비고","")
                )

            )

            db.add(race)

        except Exception as e:

            print("🔥 출전표 에러:")
            print(e)

            return {
                "error":str(e),
                "row":row.to_dict()
            }

    db.commit()

    return {
       "message":"업로드 완료"
    }


@app.get("/race")
def get_race():

    db = SessionLocal()

    data = db.query(
        Race
    ).all()

    db.close()

    return [

        {
            "id":r.id,
            "지역":r.지역,
            "마명":r.마명,
            "순":r.순,
            "경주일자":r.경주일자,
            "경주":r.경주,
            "등급":r.등급,
            "거리":r.거리,
            "편성":r.편성,
            "출전":r.출전,
            "경주명":r.경주명,
            "출발시각":r.출발시각,
            "비고":r.비고
        }

        for r in data
    ]


from datetime import datetime
import re


@app.get("/current-race")
def get_current_race():

    db=SessionLocal()

    races=db.query(
        Race
    ).all()

    db.close()

    if not races:

        return {

            "지역":"-",
            "경주":"-",
            "시간":"-"

        }

    now=datetime.now()

    upcoming=[]

    for r in races:

        try:

            # 2026/05/30(토) → 20260530
            date_num=''.join(
                c for c in str(r.경주일자)
                if c.isdigit()
            )[:8]


            # 10:35 → 1035
            # 9:05 → 905
            time_text=''.join(
                c for c in str(r.출발시각)
                if c.isdigit()
            )


            if len(time_text)==4:

                time_text=(

                    time_text[:2]
                    + ":"
                    + time_text[2:]

                )


            elif len(time_text)==3:

                time_text=(

                    "0"
                    + time_text[:1]
                    + ":"
                    + time_text[1:]

                )


            race_dt=datetime.strptime(

                f"{date_num} {time_text}",
                "%Y%m%d %H:%M"

            )


            print(
                "파싱성공:",
                race_dt
            )


            if race_dt > now:

                upcoming.append({

                    "지역":r.지역,
                    "경주":r.경주,
                    "시간":race_dt

                })


        except Exception as e:

            print(

                "시간변환오류:",
                r.경주일자,
                r.출발시각,
                e

            )

            continue


    if not upcoming:

        return {

            "지역":"-",
            "경주":"-",
            "시간":"-"

        }


    next_race=min(

        upcoming,
        key=lambda x:x["시간"]

    )


    return {

        "지역":
        next_race["지역"],

        "경주":
        next_race["경주"],

        "시간":
        next_race["시간"].strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    }
    
@app.put("/race/{race_id}")
def update_race(race_id: int, data: dict = Body(...)):
    db = SessionLocal()

    race = db.query(Race).filter(Race.id == race_id).first()

    if not race:
        db.close()
        raise HTTPException(404, "경주 없음")

    for key, value in data.items():
        setattr(race, key, value)

    db.commit()
    db.close()

    return {"msg": "수정 완료"}


@app.delete("/race/{race_id}")
def delete_race(race_id: int):
    db = SessionLocal()

    race = db.query(Race).filter(Race.id == race_id).first()

    if race:
        db.delete(race)
        db.commit()

    db.close()

    return {"msg": "삭제 완료"}
    
def clean(v):
    if str(v).lower() == "nan":
        return "-"
    return str(v)
# =========================
# 경주상세 업로드
# =========================
@app.post("/upload-race-detail")
async def upload_race_detail(
    file: UploadFile = File(...)
):

    df = pd.read_excel(file.file)

    # 🔥 컬럼명 정리
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("▲","", regex=False)
    )

    print(
        "상세컬럼:",
        df.columns.tolist()
    )

    db = SessionLocal()

    db.query(RaceDetail).delete()

    for _, row in df.iterrows():

        try:

            print("행 데이터:", row.to_dict())

            print(
                "번호확인=",
                row.get("번호"),
                row.get("번호▲"),
                "| 컬럼목록=",
                row.index.tolist()
            )

            경주번호값 = str(
                row.get("경주번호","0")
            ).replace(
                "R",""
            ).replace(
                "경주",""
            ).strip()

            if (
                경주번호값 == ""
                or 경주번호값.lower() == "nan"
            ):
                경주번호값 = "0"

            item = RaceDetail(

                경주일자 = clean(
                    row.get(
                        "출전날짜",
                        row.get("날짜","")
                    )
                ),

                지역 = clean(
                    row.get(
                        "지역명",
                        row.get("지역","")
                    )
                ),

                # 🔥 이 줄 복구
                경주 = int(
                    경주번호값
                ),

                번호 = clean(
                    row.get("번호","")
                ),

                마명 = clean(
                    row.get("마명","")
                ),

                체중 = clean(
                    row.get(
                        "체중",
                        row.get("마중","")
                    )
                ),

                성별 = clean(
                    row.get("성별","")
                ),

                나이 = clean(
                    row.get("연령","")
                ),

                레이팅 = clean(
                    row.get("레이팅","")
                ),

                부담중량 = clean(
                    row.get("중량","")
                ),

                증감 = clean(
                    row.get("증감","")
                ),

                기수 = clean(
                    row.get("기수명","")
                ),

                조교사 = clean(
                    row.get("조교사명","")
                ),

                마주명 = clean(
                    row.get("마주명","")
                ),

                조교횟수 = clean(
                    row.get(
                        "조교횟수",
                        row.get("조교 횟수","")
                    )
                ),

                출전주기 = clean(
                    row.get(
                        "출전주기",
                        row.get("출전 주기","")
                    )
                ),

                장구현황 = clean(
                    row.get("장구현황","")
                ),

                특이사항 = clean(
                    row.get("특이사항","")
                )
            )
            
            db.add(item)

    

        except Exception as e:

            print("🔥 에러:")
            print(e)

            return {
                "error": str(e),
                "row": row.to_dict()
            }

    db.commit()
    db.close()

    return {
        "msg":"경주상세 저장 완료"
    }
    
@app.get("/race-detail-data/{race_no}")
def get_race_detail_data(
    race_no:int,
    date:str=None,
    region:str=None,
    db:Session=Depends(get_db)
):

    if region == "부산":
        region = "부산경남"

    query = db.query(
        RaceDetail
    ).filter(
        RaceDetail.경주 == race_no
    )

    print(
       "조회지역=",
        region
    )

    # 지역 필터
    if region:
        query = query.filter(
            RaceDetail.지역 == region
        )

    # 날짜 필터
    if date:

        rows = query.all()

        # 예:
        # 2026-06-06 00:00:00
        # ↓
        # 20260606
        input_clean = ''.join(
            c for c in str(date)
            if c.isdigit()
        )[:8]

        data = []

        for r in rows:

            # 예:
            # 20260606
            # ↓
            # 20260606
            db_clean = ''.join(
                c for c in str(r.경주일자)
                if c.isdigit()
            )[:8]

            print(
                "비교:",
                input_clean,
                db_clean
            )

            if input_clean == db_clean:
                data.append(r)

    else:

        data = query.all()

    print("조회건수 =", len(data))

    for r in data:
        print(
            r.경주일자,
            r.지역,
            r.경주,
            r.마명
        )

    return [
        {
            "경주일자": r.경주일자,
            "지역": r.지역,
            "경주": r.경주,
            "번호": r.번호,
            "마명": r.마명,
            "성별": r.성별,
            "나이": r.나이,
            "레이팅": r.레이팅,
            "기수": r.기수,
            "조교사": r.조교사,
            "마주명": r.마주명,
            "부담중량": r.부담중량,
            "증감": r.증감,
            "조교횟수": r.조교횟수,
            "출전주기": r.출전주기,
            "장구현황": r.장구현황,
            "특이사항": r.특이사항,
            "체중": r.체중,
            "최근전적": r.최근전적
        }
        for r in data
    ]
    
# =========================
# 경주 상세 조회
# =========================
@app.get("/race-detail/{region}/{rcNo}")
def get_race_detail(
    region:str,
    rcNo:int,
    date:str=None,
    db:Session=Depends(get_db)
):

    query = db.query(
        RaceDetail
    ).filter(
        RaceDetail.경주 == rcNo,
        RaceDetail.지역 == region
    )

    if date:

        rows = query.all()

        input_clean = ''.join(
            c for c in str(date)
            if c.isdigit()
        )[:8]

        data = []

        for r in rows:

            db_clean = ''.join(
                c for c in str(r.경주일자)
                if c.isdigit()
            )[:8]

            print(
                "홈팝업 비교:",
                input_clean,
                db_clean
            )

            if input_clean == db_clean:
                data.append(r)

    else:

        data = query.all()

    print(
        "홈팝업 조회건수 =",
        len(data)
    )

    return [

        {
            "지역": r.지역 or "",
            "날짜": r.경주일자 or "",
            "경주번호": r.경주 or "",

            "번호": r.번호 or "",
            "마명": r.마명 or "",
            "마중": r.체중 or "",

            "성별": r.성별 or "",
            "연령": r.나이 or "",

            "레이팅": r.레이팅 or "",
            "중량": r.부담중량 or "",
            "증감": r.증감 or "",

            "기수명": r.기수 or "",
            "조교사명": r.조교사 or "",

            "마주명": r.마주명 or "",
            "조교횟수": r.조교횟수 or "",
            "출전주기": r.출전주기 or "",

            "장구현황": r.장구현황 or "",
            "특이사항": r.특이사항 or ""

        }

        for r in data

    ]
# =========================
# 경주 분석 저장
# =========================
@app.post("/analysis-save")
async def save_raceanalysis(req: Request, db: Session = Depends(get_db)):
    data = await req.json()

    # 🔥 기존 데이터 있는지 확인
    existing = db.query(raceAnalysis).filter(
        raceAnalysis.region == data["region"],
        raceAnalysis.race_no == data["race_no"],
        raceAnalysis.race_date == data["race_date"]
    ).first()

    if existing:
        # 🔥 업데이트
        existing.star = data["star"]
        existing.square = data["square"]
        existing.empty = data["empty"]
        existing.up = data["up"]
        existing.triangle = data["triangle"]
        existing.darkhorse = data["darkhorse"]
        existing.single = data["single"]
        existing.double = data["double"]
        existing.triple = data["triple"]

    else:
        # 🔥 신규 생성
        new_data = raceAnalysis(**data)
        db.add(new_data)

    db.commit()

    return {"msg": "ok"}


@app.get("/analysis-table")
def get_raceanalysis_table(
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    if current["role"] not in [
      "admin",
      "superadmin"
    ]:
        member = db.query(Member).filter(Member.email == current["email"]).first()

        if not member or not member.is_premium:
            raise HTTPException(403, "결제 필요")

    races = db.query(Race).all()
    analyses = db.query(raceAnalysis).all()

    result = []

    for r in races:
        matched = next(
            (
                a for a in analyses
                if a.race_no == r.경주
                and a.region == r.지역
                and a.race_date == r.경주일자
            ),
            None
        )

        result.append({
            "id": r.id,
            "지역": r.지역,
            "경주": r.경주,
            "경주일자": r.경주일자,
            "star": matched.star if matched else "",
            "square": matched.square if matched else "",
            "empty": matched.empty if matched else "",
            "up": matched.up if matched else "",
            "triangle": matched.triangle if matched else "",
            "darkhorse": matched.darkhorse if matched else "",
            "single": matched.single if matched else "",
            "double": matched.double if matched else "",
            "triple": matched.triple if matched else "",
        })

    return result

@app.get("/admin/users")
def get_users(db: Session = Depends(get_db), current=Depends(get_current_user)):

    if current["role"] not in ["admin", "superadmin"]:
        raise HTTPException(403, "관리자만 가능")

    members = db.query(Member).all()
    admins = db.query(Admin).all()

    admin_emails = {a.email for a in admins}

    result = []

    for m in members:
        result.append({
            "id": m.id,
            "email": m.email,
            "name": m.name,
            "birth": m.birth,
            "phone": m.phone,
            "is_premium": m.is_premium,
            "is_admin": m.email in admin_emails,
            "point": m.point
        })

    return result

@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    is_premium: bool = False,
    is_admin: bool = False,
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):

    if current["role"] not in ["admin", "superadmin"]:
        raise HTTPException(403, "관리자만 가능")

    member = db.query(Member).filter(Member.id == user_id).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    # 유료 변경
    member.is_premium = is_premium

    # 관리자 토글
    admin = db.query(Admin).filter(Admin.email == member.email).first()

    if is_admin:
        if not admin:
            db.add(Admin(email=member.email, password=member.password))
    else:
        if admin:
            db.delete(admin)

    db.commit()

    return {"msg": "수정 완료"}

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):

    if current["role"] not in ["admin", "superadmin"]:
        raise HTTPException(403, "관리자만 가능")

    member = db.query(Member).filter(Member.id == user_id).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    # 관리자면 같이 삭제
    admin = db.query(Admin).filter(Admin.email == member.email).first()
    if admin:
        db.delete(admin)

    db.delete(member)
    db.commit()

    return {"msg": "삭제 완료"}

@app.get("/admin/admins")
def get_admins_only(db: Session = Depends(get_db), current=Depends(get_current_user)):

    if current["role"] not in ["admin", "superadmin"]:
        raise HTTPException(403, "관리자만 가능")

    admins = db.query(Admin).all()
    members = db.query(Member).all()

    member_map = {m.email: m for m in members}

    result = []

    for a in admins:
        m = member_map.get(a.email)

        if m:
            result.append({
                "id": m.id,
                "email": m.email,
                "name": m.name,
                "birth": m.birth,
                "phone": m.phone,
                "is_premium": m.is_premium,
                "is_admin": True
            })

    return result

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.get("/ai.html")
def ai_page():
    return FileResponse("frontend/ai.html")
 
@app.put("/menus/{menu_id}")
def update_menu(
    menu_id:int,
    data:schemas.MenuCreate,
    db:Session = Depends(get_db)
):

    menu = db.query(models.Menu)\
        .filter(models.Menu.id == menu_id)\
        .first()

    if not menu:
        return {"error":"not found"}

    menu.name = data.name
    menu.path = data.path
    menu.template = data.template
    menu.icon = data.icon
    menu.description = data.description
    menu.sort_order = data.sort_order
    menu.is_active = data.is_active

    db.commit()

    return {"message":"updated"}

@app.get("/admin.html")
def admin_page():
    return FileResponse("frontend/admin.html")


@app.post("/collect-horse")
def collect_horse():

    result = subprocess.run(
        ["python","horse_collect.py"],
        capture_output=True,
        text=True
    )

    print("stdout:")
    print(result.stdout)

    print("stderr:")
    print(result.stderr)

    return {
        "message":"경주마 수집 완료",
        "stdout": result.stdout,
        "stderr": result.stderr
    }


@app.post("/collect-jockey")
def collect_jockey():

    os.system("python jockey_collect.py")

    return {
        "message":"기수 수집 완료"
    }


@app.post("/collect-trainer")
def collect_trainer():

    os.system("python trainer_collect.py")

    return {
        "message":"조교사 수집 완료"
    }

# =========================
# 경주마 목록 조회
# =========================
@app.get("/horse")
def get_horse(
    db: Session = Depends(get_db)
):

    horses = db.query(
        Horse
    ).all()

    return horses

# =========================
# 조교사 목록 조회
# =========================
@app.get("/trainer")
def get_trainer():

    db=SessionLocal()

    data=db.query(
        Trainer
    ).all()

    db.close()

    return [

        {

            "id":t.id,

            "tr_no":t.tr_no,

            "지역명":t.지역명,
            "조교사명":t.조교사명,

            "통산전적":t.통산전적,

            "통산승률":t.통산승률,
            "통산복승률":t.통산복승률,
            "통산연승률":t.통산연승률,

            "최근1년":t.최근1년,

            "최근1년승률":t.최근1년승률,
            "최근1년복승률":t.최근1년복승률,
            "최근1년연승률":t.최근1년연승률

        }

        for t in data

    ]
# =========================
# 경주마 자료업로드
# =========================
@app.post("/upload-horse")
async def upload_horse(
    file: UploadFile,
    db: Session = Depends(get_db)
):

    import pandas as pd

    df = pd.read_excel(
        file.file
    )

    db.query(Horse).delete()
    db.commit()

    for _, row in df.iterrows():

        horse = Horse(

    hr_no = str(row.get("마번","")),

        마명 = str(row.get("마명","")),
        성별 = str(row.get("성별","")),
        나이 = str(row.get("연령","")),

        생년월일 = str(row.get("생년월일","")),

        조교사 = str(
                row.get("조교사명",
                row.get("조교사",""))
            ),

            마주 = str(
                row.get("마주명",
                row.get("마주",""))
            ),

        부마 = str(row.get("부마","")),
        모마 = str(row.get("모마","")),

        통산전적 = str(row.get("통산전적","")),
        승률 = str(row.get("승률","")),

        수득상금 = str(row.get("수득상금","")),

        최근전적 = "",
        특징 = ""
    )

        db.add(horse)

    db.commit()

    return {
        "message":"업로드 완료"
    }

# =========================
# 경주마 상세보기
# =========================
@app.get("/horse/{horse_name}")
def get_horse(
    horse_name:str,
    db:Session=Depends(get_db)
):

    horse=db.query(
        Horse
    ).filter(
        Horse.마명==horse_name
    ).first()

    if not horse:
        return {}

    return {

        "마명": horse.마명,
        "부마": horse.부마,
        "모마": horse.모마,
        "성별": horse.성별,
        "나이": horse.나이,
        "생년월일": horse.생년월일,
        "조교사": horse.조교사,
        "마주": horse.마주,
        "통산전적": horse.통산전적,
        "승률": horse.승률,
        "수득상금": horse.수득상금,
        "최근전적": horse.최근전적,
        "특징": horse.특징

    }

# =========================
# 기수 업로드
# =========================
@app.post("/upload-jockey")
async def upload_jockey(
    file: UploadFile=File(...)
):

    df=pd.read_excel(file.file)

    df.columns=(
        df.columns
        .str.strip()
    )

    db=SessionLocal()

    db.query(Jockey).delete()

    for _,row in df.iterrows():

        item=Jockey(

            지역명=clean(
                row.get("지역명","")
            ),

            기수명=clean(
                row.get("기수명","")
            ),

            생년월일=clean(
                row.get("생년월일","")
            ),

            데뷔일자=clean(
                row.get("데뷔일자","")
            ),

            기승가능중량=clean(
                row.get("기승가능중량","")
            ),

            통산전적=clean(
                row.get("통산전적","")
            ),

            통산승률=clean(
                row.get("통산승률","")
            ),

            통산복승률=clean(
                row.get("통산복승률","")
            ),

            통산연승률=clean(
                row.get("통산연승률","")
            ),

            최근1년=clean(
                row.get("최근1년","")
            ),

            최근1년승률=clean(
                row.get("최근1년승률","")
            ),

            최근1년복승률=clean(
                row.get("최근1년복승률","")
            ),

            최근1년연승률=clean(
                row.get("최근1년연승률","")
            )
        )

        db.add(item)

    db.commit()

    return{
        "message":"기수 업로드 완료"
    }

# =========================
# 조교사 업로드
# =========================
@app.post("/upload-trainer")
async def upload_trainer(
    file: UploadFile=File(...)
):

    xls=pd.ExcelFile(
        file.file
    )

    # =====================
    # 시트 읽기
    # =====================

    df=pd.read_excel(
        xls,
        sheet_name="인적사항"
    )

    horse_df=pd.read_excel(
        xls,
        sheet_name="위탁관리말"
    )

    year_df=pd.read_excel(
        xls,
        sheet_name="연도별성적"
    )

    recent_df=pd.read_excel(
        xls,
        sheet_name="최근1개월"
    )

    # 컬럼 공백 제거
    df.columns=df.columns.str.strip()
    horse_df.columns=horse_df.columns.str.strip()
    year_df.columns=year_df.columns.str.strip()
    recent_df.columns=recent_df.columns.str.strip()


    # =====================
    # 통산 + 최근1년 합치기
    # =====================

    df=df.pivot_table(

        index=[
            "tr_no",
            "조교사명",
            "지역명"
        ],

        columns="구분",

        values=[
            "전적",
            "승률",
            "복승률",
            "연승률"
        ],

        aggfunc="first"

    )

    df.columns=[
        f"{b}_{a}"
        for a,b in df.columns
    ]

    df=df.reset_index()


    db=SessionLocal()

    db.query(Trainer).delete()
    db.query(TrainerHorse).delete()
    db.query(TrainerYear).delete()
    db.query(TrainerRecent).delete()


    # =====================
    # 인적사항 저장
    # =====================

    for _,row in df.iterrows():

        item=Trainer(

            tr_no=clean(
                row.get("tr_no","")
            ),

            지역명=clean(
                row.get("지역명","")
            ),

            조교사명=clean(
                row.get("조교사명","")
            ),

            통산전적=clean(
                row.get("통산_전적","")
            ),

            통산승률=clean(
                row.get("통산_승률","")
            ),

            통산복승률=clean(
                row.get("통산_복승률","")
            ),

            통산연승률=clean(
                row.get("통산_연승률","")
            ),

            최근1년=clean(
                row.get("최근1년_전적","")
            ),

            최근1년승률=clean(
                row.get("최근1년_승률","")
            ),

            최근1년복승률=clean(
                row.get("최근1년_복승률","")
            ),

            최근1년연승률=clean(
                row.get("최근1년_연승률","")
            )
        )

        db.add(item)


    # =====================
    # 위탁관리말 저장
    # =====================

    for _,row in horse_df.iterrows():

        db.add(

            TrainerHorse(

                tr_no=clean(
                    row.get("tr_no","")
                ),

                마명=clean(
                    row.get("마명","")
                ),

                마주명=clean(
                    row.get("마주명","")
                ),

                조번=clean(
                    row.get("조번","")
                ),

                등급=clean(
                    row.get("등급","")
                ),

                레이팅=clean(
                    row.get("레이팅","")
                ),

                산지=clean(
                    row.get("산지","")
                ),

                성별=clean(
                    row.get("성별","")
                ),

                연령=clean(
                    row.get("연령","")
                )
            )
        )


    # =====================
    # 연도별성적 저장
    # =====================

    for _,row in year_df.iterrows():

        db.add(

            TrainerYear(

                tr_no=clean(
                    row.get("tr_no","")
                ),

                연도=clean(
                    row.get("연도","")
                ),

                출전=clean(
                    row.get("출전","")
                ),

                일위=clean(
                    row.get("1위","")
                ),

                이위=clean(
                    row.get("2위","")
                ),

                삼위=clean(
                    row.get("3위","")
                ),

                승률=clean(
                    row.get("승률","")
                ),

                복승률=clean(
                    row.get("복승률","")
                ),

                연승률=clean(
                    row.get("연승률","")
                ),

                순위상금=clean(
                    row.get("순위상금","")
                )
            )
        )


    # =====================
    # 최근1개월 저장
    # =====================

    for _,row in recent_df.iterrows():

        db.add(

            TrainerRecent(

                tr_no=clean(
                    row.get("tr_no","")
                ),

                경주일자=clean(
                    row.get("경주일자","")
                ),

                마번=clean(
                    row.get("마번","")
                ),

                마명=clean(
                    row.get("마명","")
                ),

                기수명=clean(
                    row.get("기수명","")
                ),

                등급=clean(
                    row.get("등급","")
                ),

                순위=clean(
                    row.get("순위","")
                ),

                중량=clean(
                    row.get("중량","")
                ),

                거리=clean(
                    row.get("거리","")
                ),

                기록=clean(
                    row.get("기록","")
                ),

                도착차=clean(
                    row.get("도착차","")
                ),

                마체중=clean(
                    row.get("마체중","")
                )
            )
        )

    db.commit()
    db.close()

    return {
        "message":"조교사 업로드 완료"
    }


# =========================
# 혈통업로드
# =========================
# =========================
# 혈통업로드
# =========================
@app.post("/upload-blood")
async def upload_blood(
    file: UploadFile = File(...)
):

    df = pd.read_excel(file.file)

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace(" ", "", regex=False)
    )

    print("혈통 컬럼명:", df.columns.tolist())
    print("혈통 첫행:", df.iloc[0].to_dict())

    db = SessionLocal()

    db.query(Blood).delete()

    for _, row in df.iterrows():

        item = Blood(

            출전날짜=clean(row.get("출전날짜", "")),

            지역=clean(row.get("지역", "")),
            meet=clean(row.get("meet", "")),

            경주번호=clean(row.get("경주번호", "")),
            거리=clean(row.get("거리", "")),

            표번호=clean(row.get("표번호", "")),
            원본URL=clean(row.get("원본URL", "")),

            번호=clean(row.get("번호", "")),

            부마=clean(row.get("부마", "")),
            모마=clean(row.get("모마", "")),
            외조부마=clean(row.get("외조부마", "")),

            도시지프로필=clean(
                row.get("도시지프로필", "")
            ),

            DI=clean(row.get("DI", "")),
            CD=clean(row.get("CD", "")),

            근친=clean(row.get("근친", "")),

            AWD=clean(row.get("AWD", "")),
            부AWD=clean(row.get("부AWD", "")),
            모AWD=clean(row.get("모AWD", "")),
            모부AWD=clean(row.get("모부AWD", "")),

            마명=clean(row.get("마명", "")),

            연령=clean(row.get("연령", "")),
            레이팅=clean(row.get("레이팅", "")),

            최근순위=clean(
                row.get("최근순위(6개월)", "")
            ),

            도착차=clean(
                row.get("최근1위와의도착차(6개월)", "")
            ),

            경주성적=clean(
                row.get("경주성적", "")
            ),

            기수=clean(
                row.get("기수", "")
            ),

            기수복승률=clean(
                row.get("기수복승률", "")
            ),

            부담중량=clean(
                row.get("부담중량", "")
            ),

            최고기록=clean(
                row.get("최고기록", "")
            ),

            평균기록=clean(
                row.get("평균기록", "")
            ),

            평균S1F=clean(
                row.get("평균S1F", "")
            ),

            평균G3F=clean(
                row.get("평균G3F", "")
            ),

            평균G1F=clean(
                row.get("평균G1F", "")
            ),

            최고G3F=clean(
                row.get("최고G3F", "")
            ),

            통산펄롱=clean(
                row.get("통산펄롱", "")
            ),

            통산부담=clean(
                row.get("통산부담", "")
            ),

            평균경주전개=clean(
                row.get("평균경주전개", "")
            ),

            전적=clean(
                row.get("상대전적", "")
            ),

            현군성적=clean(
                row.get("현군성적", "")
            ),

            상금비율=clean(
                row.get("상금비율", "")
            ),

            훈련량수영훈련=clean(
                row.get("훈련량수영훈련", "")
            ),

            평균훈련량=clean(
                row.get("평균훈련량", "")
            ),

            수입전경주성적=clean(
                row.get("수입전경주성적", "")
            ),

            경매가수입가=clean(
                row.get("경매가수입가", "")
            ),

            조교사=clean(
                row.get("조교사", "")
            )

        )

        db.add(item)

    db.commit()
    db.close()

    return {
        "message": "혈통정보 업로드 완료"
    }

# =========================
# 혈통
# =========================
@app.get("/blood")
def get_blood():

    db = SessionLocal()

    data = db.query(
        Blood
    ).all()

    db.close()

    return [

{
    "id": b.id,

    "출전날짜": b.출전날짜,
    "지역": b.지역,
    "meet": b.meet,

    "경주번호": b.경주번호,
    "거리": b.거리,

    "표번호": b.표번호,
    "원본URL": b.원본URL,

    "번호": b.번호,

    "부마": b.부마,
    "모마": b.모마,
    "외조부마": b.외조부마,

    "도시지프로필": b.도시지프로필,

    "DI": b.DI,
    "CD": b.CD,
    "근친": b.근친,

    "AWD": b.AWD,
    "부AWD": b.부AWD,
    "모AWD": b.모AWD,
    "모부AWD": b.모부AWD,

    "마명": b.마명,

    "연령": b.연령,
    "레이팅": b.레이팅,

    "최근순위": b.최근순위,
    "도착차": b.도착차,

    "경주성적": b.경주성적,

    "기수": b.기수,
    "기수복승률": b.기수복승률,

    "부담중량": b.부담중량,

    "최고기록": b.최고기록,
    "평균기록": b.평균기록,

    "평균S1F": b.평균S1F,
    "평균G3F": b.평균G3F,
    "평균G1F": b.평균G1F,

    "최고G3F": b.최고G3F,

    "통산펄롱": b.통산펄롱,
    "통산부담": b.통산부담,

    "평균경주전개": b.평균경주전개,

    "전적": b.전적,
    "현군성적": b.현군성적,

    "상금비율": b.상금비율,

    "훈련량수영훈련": b.훈련량수영훈련,
    "평균훈련량": b.평균훈련량,

    "수입전경주성적": b.수입전경주성적,

    "경매가수입가": b.경매가수입가,

    "조교사": b.조교사
    }

    for b in data
    ]

# =========================
# 조교사 추가탭 조회
# =========================

@app.get("/trainer-horse/{tr_no}")
def get_trainer_horse(
    tr_no:str,
    db:Session=Depends(get_db)
):

    data=db.query(
        TrainerHorse
    ).filter(
        TrainerHorse.tr_no==tr_no
    ).all()

    return [

    {
        "마명":r.마명,
        "마주명":r.마주명,
        "조번":r.조번,
        "등급":r.등급,
        "레이팅":r.레이팅,
        "산지":r.산지,
        "성별":r.성별,
        "연령":r.연령
    }

    for r in data
    ]


@app.get("/trainer-year/{tr_no}")
def get_trainer_year(
    tr_no:str,
    db:Session=Depends(get_db)
):

    data=db.query(
        TrainerYear
    ).filter(
        TrainerYear.tr_no==tr_no
    ).all()

    return [

    {
        "연도":r.연도,
        "출전":r.출전,
        "일위":r.일위,
        "이위":r.이위,
        "삼위":r.삼위,
        "승률":r.승률,
        "복승률":r.복승률,
        "연승률":r.연승률,
        "순위상금":r.순위상금
    }

    for r in data
    ]


@app.get("/trainer-recent/{tr_no}")
def get_trainer_recent(
    tr_no:str,
    db:Session=Depends(get_db)
):

    data=db.query(
        TrainerRecent
    ).filter(
        TrainerRecent.tr_no==tr_no
    ).all()

    return [

    {
        "경주일자":r.경주일자,
        "마번":r.마번,
        "마명":r.마명,
        "기수명":r.기수명,
        "등급":r.등급,
        "순위":r.순위,
        "중량":r.중량,
        "거리":r.거리,
        "기록":r.기록,
        "도착차":r.도착차,
        "마체중":r.마체중
    }

    for r in data
    ]
    
# =========================
# 기수 보여주기(인덱스)
# =========================
@app.get("/jockey/{jockey_name}")
def get_jockey_detail(
    jockey_name:str,
    db:Session=Depends(get_db)
):

    jockey=db.query(
        Jockey
    ).filter(
        Jockey.기수명==jockey_name
    ).first()

    if not jockey:
        return {}

    return {

        "지역명":jockey.지역명,
        "기수명":jockey.기수명,

        "생년월일":jockey.생년월일,
        "데뷔일자":jockey.데뷔일자,
        "기승가능중량":jockey.기승가능중량,

        "통산전적":jockey.통산전적,

        "통산승률":jockey.통산승률,
        "통산복승률":jockey.통산복승률,
        "통산연승률":jockey.통산연승률,

        "최근1년":jockey.최근1년,

        "최근1년승률":jockey.최근1년승률,
        "최근1년복승률":jockey.최근1년복승률,
        "최근1년연승률":jockey.최근1년연승률
    }


@app.get("/jockey")
def get_jockey():

    db=SessionLocal()

    data=db.query(
        Jockey
    ).all()

    db.close()

    return [

        {
            "id":j.id,
            "지역명":j.지역명,
            "기수명":j.기수명,

            "생년월일":j.생년월일,
            "데뷔일자":j.데뷔일자,

            "통산전적":j.통산전적,
            "통산승률":j.통산승률,
            "통산복승률":j.통산복승률,
            "통산연승률":j.통산연승률,

            "최근1년":j.최근1년,
            "최근1년승률":j.최근1년승률,
            "최근1년복승률":j.최근1년복승률,
            "최근1년연승률":j.최근1년연승률
        }

        for j in data
    ]

# =========================
# 조교사 보여주기(인덱스)
# =========================
@app.get("/trainer/{trainer_name}")
def get_trainer_info(
    trainer_name:str,
    db:Session=Depends(get_db)
):

    trainer=db.query(
        Trainer
    ).filter(
        Trainer.조교사명==trainer_name
    ).first()

    if not trainer:
        return {}

    return trainer


# =========================
# 조교사 이름기준 추가탭 조회
# =========================

@app.get("/trainer-horse-name/{trainer_name}")
def get_trainer_horse_name(
    trainer_name:str,
    db:Session=Depends(get_db)
):

    trainer=db.query(
        Trainer
    ).filter(
        Trainer.조교사명==trainer_name
    ).first()

    if not trainer:
        return []

    data=db.query(
        TrainerHorse
    ).filter(
        TrainerHorse.tr_no==trainer.tr_no
    ).all()

    return data


@app.get("/trainer-year-name/{trainer_name}")
def get_trainer_year_name(
    trainer_name:str,
    db:Session=Depends(get_db)
):

    trainer=db.query(
        Trainer
    ).filter(
        Trainer.조교사명==trainer_name
    ).first()

    if not trainer:
        return []

    data=db.query(
        TrainerYear
    ).filter(
        TrainerYear.tr_no==trainer.tr_no
    ).all()

    return data


@app.get("/trainer-recent-name/{trainer_name}")
def get_trainer_recent_name(
    trainer_name:str,
    db:Session=Depends(get_db)
):

    trainer=db.query(
        Trainer
    ).filter(
        Trainer.조교사명==trainer_name
    ).first()

    if not trainer:
        return []

    data=db.query(
        TrainerRecent
    ).filter(
        TrainerRecent.tr_no==trainer.tr_no
    ).all()

    return data

@app.post("/find-id")
def find_id(data: FindAccountRequest):

    db = SessionLocal()

    user = db.query(Member).filter(
        Member.name == data.name,
        Member.birth == data.birth,
        Member.phone == data.phone
    ).first()

    db.close()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="일치하는 회원정보 없음"
        )

    return {
        "email": user.email
    }


@app.post("/reset-password")
def reset_password(data: ResetPasswordRequest):

    db = SessionLocal()

    user = db.query(Member).filter(
        Member.email == data.email,
        Member.name == data.name,
        Member.birth == data.birth,
        Member.phone == data.phone
    ).first()

    if not user:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="회원정보 불일치"
        )

    user.password = pwd_context.hash(
        data.new_password
    )

    db.commit()
    db.close()

    return {
        "msg": "비밀번호 변경 완료"
    }

# =========================
# 포인트 지급
# =========================
@app.put("/users/{user_id}/point")
def update_point(
    user_id: int,
    point: int,
    db: Session = Depends(get_db),
    current=Depends(require_admin)
):

    user = db.query(Member).filter(
        Member.id == user_id
    ).first()

    if not user:
        raise HTTPException(404, "회원 없음")

    user.point += point

    history = PointHistory(

    email=user.email,

    type="charge",

    amount=point,

    remain_point=user.point,

    description="관리자 지급",

    created_at=str(datetime.now())

)

    db.add(history)

    if user.point < 0:
        user.point = 0

    db.commit()

    return {
        "msg":"포인트 지급 완료",
        "point":user.point
    }

# =========================
# 포인트 차감
# =========================
@app.put("/users/{user_id}/use-point")
def use_point(
    user_id:int,
    point:int,
    db:Session=Depends(get_db),
    current=Depends(require_admin)
):

    user = db.query(Member).filter(
        Member.id == user_id
    ).first()

    if not user:
        raise HTTPException(404, "회원 없음")

    if user.point is None:
        user.point = 0

    # 포인트 부족
    if user.point < point:
        raise HTTPException(400, "포인트 부족")

    user.point -= point

    db.commit()

    return {
        "msg":"포인트 차감 완료",
        "point":user.point
    }

# =========================
# 분석 상세 조회
# =========================
@app.get("/analysis-view/{analysis_id}")
def analysis_view(
    analysis_id:int,
    db:Session=Depends(get_db),
    current=Depends(get_current_user)
):

    # =====================
    # 분석 찾기
    # =====================
    analysis = db.query(models.Analysis).filter(
        models.Analysis.id == analysis_id
    ).first()

    if not analysis:
        raise HTTPException(404, "분석 없음")

    # =====================
    # 슈퍼관리자
    # =====================
    if current["role"] == "superadmin":

        return {
            "title": analysis.title,
            "content": analysis.content,
            "remain_point": 999999
        }

    # =====================
    # 일반 회원
    # =====================
    member = db.query(Member).filter(
        Member.email == current["email"]
    ).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    need_point = 100

    if member.point < need_point:
        raise HTTPException(400, "포인트 부족")

    member.point -= need_point

    history = PointHistory(
        email=member.email,
        type="use",
        amount=-need_point,
        remain_point=member.point,
        description="AI 추천 이용",
        created_at=str(datetime.now())
    )

    db.add(history)
    db.commit()

    return {
        "title": analysis.title,
        "content": analysis.content,
        "remain_point": member.point
    }
@app.post("/use-ai")
def use_ai(
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
):

    print("CURRENT =", current)

    # =====================
    # 슈퍼관리자
    # =====================
    if current["role"] == "superadmin":

        return {
            "msg": "슈퍼관리자",
            "remain_point": 999999
        }

    member = db.query(Member).filter(
        Member.email == current["email"]
    ).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    need_point = 100

    if member.point < need_point:
        raise HTTPException(400, "포인트 부족")

    member.point -= need_point

    history = PointHistory(

        email=member.email,

        type="use",

        amount=-need_point,

        remain_point=member.point,

        description="AI 추천 이용",

        created_at=str(datetime.now())

    )

    db.add(history)

    db.commit()

    return {
        "msg":"차감 완료",
        "remain_point":member.point
    }

@app.post("/use-blood-analysis")
def use_blood_analysis(
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
):

    print("CURRENT =", current)

    # =====================
    # 슈퍼관리자
    # =====================
    if current["role"] == "superadmin":

        return {
            "msg": "슈퍼관리자",
            "remain_point": 999999
        }

    member = db.query(Member).filter(
        Member.email == current["email"]
    ).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    need_point = 200

    if member.point < need_point:
        raise HTTPException(400, "포인트 부족")

    member.point -= need_point

    history = PointHistory(

        email=member.email,

        type="use",

        amount=-need_point,

        remain_point=member.point,

        description="혈통분석 이용",

        created_at=str(datetime.now())

    )

    db.add(history)

    db.commit()

    return {
        "msg":"차감 완료",
        "remain_point":member.point
    }

# =========================
# 포인트 로그 조회
# =========================
@app.get("/point-history")
def get_point_history(
    db: Session = Depends(get_db)
):

    history = db.query(
        PointHistory
    ).order_by(
        PointHistory.id.desc()
    ).all()

    return [

    {
        "id": h.id,

        "email": h.email,

        "type": h.type,

        "amount": h.amount,

        "remain_point": h.remain_point,

        "description": h.description,

        "created_at": h.created_at
    }

    for h in history
]

# =========================
# 내 정보 조회
# =========================
@app.get("/my-info")
def get_my_info(
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):

    # =====================
    # 슈퍼관리자
    # =====================
    if current["role"] == "superadmin":

        return {
            "email": current["email"],
            "name": "SuperAdmin",
            "point": 999999,
            "is_premium": True,
            "role": "superadmin"
        }

    member = db.query(Member).filter(
        Member.email == current["email"]
    ).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    return {

        "email": member.email,
        "name": member.name,
        "point": member.point,
        "is_premium": member.is_premium,
        "role": current["role"]

    }
@app.get("/my-profile/{email}")
def my_profile(
    email:str,
    db:Session=Depends(get_db)
):

    user=db.query(Member).filter(
        Member.email==email
    ).first()

    if not user:
        raise HTTPException(
            404,
            "회원 없음"
        )

    return {
        "email":user.email,
        "name":user.name,
        "birth":user.birth,
        "phone":user.phone,
        "point":user.point
    }
@app.get("/my.html")
def my_page():
    return FileResponse(
        "frontend/my.html"
    )

# =========================
# 비밀번호 변경
# =========================
@app.post("/change-password")
def change_password(
    email:str,
    old_password:str,
    new_password:str,
    db:Session=Depends(get_db)
):

    user = db.query(Member).filter(
        Member.email == email
    ).first()

    if not user:
        raise HTTPException(
            404,
            "회원 없음"
        )

    if not verify_password(
        old_password,
        user.password
    ):
        raise HTTPException(
            400,
            "현재 비밀번호 불일치"
        )

    user.password = hash_password(
        new_password
    )

    db.commit()

    return {
        "msg":"비밀번호 변경 완료"
    }

@app.get("/point.html")
def point_page():

    return FileResponse(
        "frontend/point.html"
    )

@app.get("/hitrate.html")
def hitrate_page():

    return FileResponse(
        "frontend/hitrate.html"
    )

@app.get("/raceinfo.html")
def raceinfo_page():

    return FileResponse(
        "frontend/raceinfo.html"
    )

@app.get("/result.html")
def result_page():

    return FileResponse(
        "frontend/result.html"
    )

@app.get("/dividend.html")
def dividend_page():

    return FileResponse(
        "frontend/dividend.html"
    )

@app.get("/race-detail")
def get_all_race_detail(
    db: Session = Depends(get_db)
):
    data = db.query(
        RaceDetail
    ).all()

    return [
        {
            "경주일자": r.경주일자,
            "지역": r.지역,
            "경주": r.경주,
            "번호": r.번호,
            "마명": r.마명,
            "기수": r.기수,
            "조교사": r.조교사
        }
        for r in data
    ]

@app.post("/use-final-analysis")
def use_final_analysis(
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
):

    # =====================
    # 슈퍼관리자
    # =====================
    if current["role"] == "superadmin":

        return {
            "msg": "슈퍼관리자",
            "remain_point": 999999
        }

    member = db.query(Member).filter(
        Member.email == current["email"]
    ).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    need_point = 300

    if member.point < need_point:
        raise HTTPException(400, "포인트 부족")

    member.point -= need_point

    history = PointHistory(
        email=member.email,
        type="use",
        amount=-need_point,
        remain_point=member.point,
        description="종합분석 열람",
        created_at=str(datetime.now())
    )

    db.add(history)

    db.commit()

    return {
        "msg":"차감 완료",
        "remain_point":member.point
    }

@app.get("/basic-analysis-data/{region}/{race_no}/{race_date}")
def get_basic_analysis_data(
    region:str,
    race_no:int,
    race_date:str,
    db:Session=Depends(get_db)
):

    race_horses = db.query(
         RaceDetail
    ).filter(
         RaceDetail.지역 == region,
         RaceDetail.경주 == race_no
    ).all()

    date_clean = ''.join(
      c for c in str(race_date)
      if c.isdigit()
    )[:8]

    race_horses = [

    r for r in race_horses

    if ''.join(
        c for c in str(r.경주일자)
        if c.isdigit()
    )[:8] == date_clean

]

    result=[]

    for r in race_horses:

        horse = db.query(Horse).filter(
            Horse.마명 == r.마명
        ).first()

        jockey = db.query(Jockey).filter(
            Jockey.기수명 == r.기수
        ).first()

        trainer = db.query(Trainer).filter(
            Trainer.조교사명 == r.조교사
        ).first()

        try:
            horse_no = int(r.번호)
        except:
            horse_no = 0

        saved = db.query(
            BasicAnalysis
        ).filter(

            BasicAnalysis.지역 == region,
            BasicAnalysis.경주 == race_no,
            BasicAnalysis.번호 == horse_no

        ).first()

        
        score, comment = calc_basic_score(
            horse,
            jockey,
            trainer
        )

        result.append({

            "번호": r.번호,
            "마명": r.마명,

            "성별":
            horse.성별 if horse else "-",

            "나이":
            horse.나이 if horse else "-",

            "통산전적":
            horse.통산전적 if horse else "-",

            "승률":
            horse.승률 if horse else "-",

            "수득상금":
            horse.수득상금 if horse else "-",

            "기수":
            r.기수,

            "기수승률":
            jockey.최근1년승률
            if jockey else "-",

            "조교사":
            r.조교사,

            "조교사승률":
            trainer.최근1년승률
            if trainer else "-",

            "코멘트":
            saved.기본코멘트
            if saved and saved.기본코멘트
            else comment,

            "점수":
            saved.기본점수
            if saved and saved.기본점수
            else score

        })

    return result


@app.post("/save-basic-analysis")
def save_basic_analysis(
    item: BasicAnalysisSave,
    db: Session = Depends(get_db)
):

    print(
        "저장:",
        item.지역,
        item.경주,
        item.경주일자,
        item.번호
    )

    row = db.query(
        BasicAnalysis
    ).filter(

        BasicAnalysis.지역 == item.지역,
        BasicAnalysis.경주 == item.경주,
        BasicAnalysis.경주일자 == item.경주일자,
        BasicAnalysis.번호 == item.번호

    ).first()

    if row:

        print(
            "저장 마명:",
            item.마명
        )

        row.마명 = item.마명
        
        row.기본코멘트 = item.코멘트
        row.기본점수 = item.점수

    else:

        row = BasicAnalysis(

            지역=item.지역,
            경주=item.경주,
            경주일자=item.경주일자,

            번호=item.번호,
            마명=item.마명,

            기본코멘트=item.코멘트,
            기본점수=item.점수

        )

        db.add(row)

    db.commit()

    return {
        "msg": "저장완료"
    }

@app.get(
"/user-basic-analysis/{region}/{race_no}/{race_date}"
)
def get_user_basic_analysis(

    region:str,
    race_no:int,
    race_date:str,

    db:Session=Depends(get_db)

):

    print("원본지역=", region)

    if region == "부산":
        region = "부산경남"

    print("변환후지역=", region)

    rows = db.query(
        BasicAnalysis
    ).filter(

        BasicAnalysis.지역 == region,
        BasicAnalysis.경주 == race_no

    ).order_by(

        BasicAnalysis.기본점수.desc()

    ).all()

    print(
        "지역+경주 매칭:",
        len(rows)
    )

    for r in rows[:10]:

        print(
            "후보:",
            r.지역,
            r.경주,
            r.경주일자,
            r.번호,
            r.마명
        )

    # 여기 추가
    print("===== BasicAnalysis 전체 확인 =====")

    all_rows = db.query(
      BasicAnalysis
    ).all()

    for r in all_rows[:30]:

       print(
            "DB:",
           r.지역,
            r.경주,
           r.경주일자
     )

    for r in rows:

        print(
            "후보:",
            r.지역,
            r.경주,
            r.경주일자
        )

    date_clean = ''.join(
        c for c in str(race_date)
        if c.isdigit()
    )[:8]

    print(
        "요청 race_date =",
        repr(race_date)
    )

    print(
        "date_clean =",
        repr(date_clean)
    )

    print(
        "요청 race_date =",
        repr(race_date)
    )

    print(
        "date_clean =",
        repr(date_clean)
    )

    for r in rows:

        db_clean = ''.join(
            c for c in str(r.경주일자)
            if c.isdigit()
        )[:8]

        print(
            "날짜비교:",
            repr(date_clean),
            repr(db_clean)
        )

    rows = [

        r for r in rows

        if ''.join(
            c for c in str(r.경주일자)
            if c.isdigit()
        )[:8] == date_clean

    ]

    print(
        "날짜필터후:",
        len(rows)
    )

    for r in rows:

        print(
            "통과:",
            r.지역,
            r.경주,
            r.경주일자
        )

    result = []

    for row in rows:

        race = db.query(
            RaceDetail
        ).filter(

            RaceDetail.지역 == row.지역,
            RaceDetail.경주 == row.경주,
            RaceDetail.번호 == str(row.번호)

        ).first()

        # =====================
        # 마명 보정
        # =====================
        horse_name = row.마명

        if (not horse_name) and race:
            horse_name = race.마명

        horse = db.query(
        Horse
        ).filter(
            Horse.마명 == horse_name
        ).first()

        print(
    "row.번호 =",
    row.번호
        )

        print(
    "row.마명 =",
    row.마명
        )

        print(
    "horse =",
    horse
        )

        jockey = None
        trainer = None

        if race:

            jockey = db.query(
                Jockey
            ).filter(
                Jockey.기수명 == race.기수
            ).first()

            trainer = db.query(
                Trainer
            ).filter(
                Trainer.조교사명 == race.조교사
            ).first()

        result.append({

                "번호": row.번호,
                "마명": horse_name,

            "성별":
            horse.성별 if horse else "-",

            "나이":
            horse.나이 if horse else "-",

            "통산전적":
            horse.통산전적 if horse else "-",

            "승률":
            horse.승률 if horse else "-",

            "수득상금":
            horse.수득상금 if horse else "-",

            "기수":
            race.기수 if race else "-",

            "조교사":
            race.조교사 if race else "-",

            "기수승률":
            jockey.최근1년승률
            if jockey else "-",

            "조교사승률":
            trainer.최근1년승률
            if trainer else "-",

            "코멘트":
            row.기본코멘트,

            "점수":
            row.기본점수

        })

    return result

@app.get("/basic-analysis-all")
def get_basic_analysis_all(
    db:Session=Depends(get_db)
):
    return db.query(
        BasicAnalysis
    ).all()

@app.get(
    "/blood-analysis-data/{region}/{race_no}/{race_date}"
)
def get_blood_analysis_data(

    region:str,
    race_no:int,
    race_date:str,

    db:Session=Depends(get_db)

):

    if region == "부산":
        region = "부산경남"

    rows = db.query(
        Blood
    ).filter(

        Blood.지역 == region,
        Blood.경주번호 == str(race_no)

    ).all()

    date_clean = ''.join(
        c for c in str(race_date)
        if c.isdigit()
    )[:8]

    result = []

    for b in rows:

        blood_date = ''.join(
            c for c in str(b.출전날짜)
            if c.isdigit()
        )[:8]

        if blood_date != date_clean:
            continue

        result.append({

            "번호": b.번호,
            "마명": b.마명,

            "도시지프로필": b.도시지프로필,

            "DI": b.DI,
            "CD": b.CD,

            "근친": b.근친,

            "AWD": b.AWD,
            "부AWD": b.부AWD,
            "모AWD": b.모AWD,
            "모부AWD": b.모부AWD,

            "경주마특성": "",
            "코멘트": "",
            "점수": 0

        })

    return result

@app.get(
"/user-blood-analysis/{region}/{race_no}/{race_date}"
)
def get_user_blood_analysis(

    region:str,
    race_no:int,
    race_date:str,

    db:Session=Depends(get_db)

):

    print("원본지역=", region)

    # if region == "부산":
    #     region = "부산경남"

    print("변환후지역=", region)

    print("===== BloodAnalysis 전체 =====")

    all_rows = db.query(
        BloodAnalysis
    ).all()

    for r in all_rows[:30]:

        print(
            "DB:",
            r.지역,
            r.경주,
            r.경주일자,
            r.번호,
            r.마명
        )

    rows = db.query(
        BloodAnalysis
    ).filter(

        BloodAnalysis.지역 == region,
        BloodAnalysis.경주 == race_no

    ).all()

    print("지역+경주 매칭=", len(rows))

    for r in rows[:20]:

        print(
            "후보:",
            r.지역,
            r.경주,
            r.경주일자,
            r.번호,
            r.마명
        )

    date_clean = ''.join(
        c for c in str(race_date)
        if c.isdigit()
    )[:8]

    print("요청날짜=", date_clean)

    for r in rows:

        db_date = ''.join(
            c for c in str(r.경주일자)
            if c.isdigit()
        )[:8]

        print(
            "날짜비교:",
            date_clean,
            db_date
        )

    rows = [

        r for r in rows

        if ''.join(
            c for c in str(r.경주일자)
            if c.isdigit()
        )[:8] == date_clean

    ]

    print("날짜필터후=", len(rows))

    result = []

    for r in rows:

        result.append({

            "번호": r.번호,
            "마명": r.마명,

            "도시지프로필": r.도시지프로필,

            "DI": r.DI,
            "CD": r.CD,
            "근친": r.근친,

            "AWD": r.AWD,
            "부AWD": r.부AWD,
            "모AWD": r.모AWD,
            "모부AWD": r.모부AWD,

            "거리적합": r.거리적합,
            "경주마특성": r.경주마특성,

            "코멘트": r.코멘트,
            "점수": r.점수

        })

    return result

    
@app.post("/save-blood-analysis")
def save_blood_analysis(
    item: BloodAnalysisSave,
    db: Session = Depends(get_db)
):

    print(
        "저장값:",
        item.번호,
        item.경주마특성,
        item.거리적합
    )

    row = db.query(
        BloodAnalysis
    ).filter(

        BloodAnalysis.지역 == item.지역,
        BloodAnalysis.경주 == item.경주,
        BloodAnalysis.경주일자 == item.경주일자,
        BloodAnalysis.번호 == item.번호

    ).first()

    if row:

        row.코멘트 = item.코멘트
        row.점수 = item.점수

        row.경주마특성 = item.경주마특성
        row.거리적합 = item.거리적합

    else:

        row = BloodAnalysis(

            지역=item.지역,
            경주=item.경주,
            경주일자=item.경주일자,

            번호=item.번호,
            마명=item.마명,

            도시지프로필=item.도시지프로필,

            DI=item.DI,
            CD=item.CD,
            근친=item.근친,

            AWD=item.AWD,
            부AWD=item.부AWD,
            모AWD=item.모AWD,
            모부AWD=item.모부AWD,

            거리적합=item.거리적합,
            경주마특성=item.경주마특성,

            코멘트=item.코멘트,
            점수=item.점수

        )

        db.add(row)

    db.commit()

    return {
        "msg":"저장 완료"
    }
    return []

@app.post("/save-blood-analysis")
def save_blood_analysis(
    item: BloodAnalysisSave,
    db: Session = Depends(get_db)
):

    print(
        "저장값:",
        item.번호,
        item.경주마특성,
        item.거리적합
    )

    row = db.query(
        BloodAnalysis
    ).filter(

        BloodAnalysis.지역 == item.지역,
        BloodAnalysis.경주 == item.경주,
        BloodAnalysis.경주일자 == item.경주일자,
        BloodAnalysis.번호 == item.번호

    ).first()

    if row:

        row.코멘트 = item.코멘트
        row.점수 = item.점수

        row.경주마특성 = item.경주마특성
        row.거리적합 = item.거리적합

    else:

        row = BloodAnalysis(

            지역=item.지역,
            경주=item.경주,
            경주일자=item.경주일자,

            번호=item.번호,
            마명=item.마명,

            도시지프로필=item.도시지프로필,

            DI=item.DI,
            CD=item.CD,
            근친=item.근친,

            AWD=item.AWD,
            부AWD=item.부AWD,
            모AWD=item.모AWD,
            모부AWD=item.모부AWD,

            거리적합=item.거리적합,
            경주마특성=item.경주마특성,

            코멘트=item.코멘트,
            점수=item.점수

        )

        db.add(row)

    db.commit()

    return {
        "msg":"저장 완료"
    }
    return []

@app.get("/fix-blood-columns")
def fix_blood_columns(
    db: Session = Depends(get_db)
):

    try:

        db.execute(text("""
        ALTER TABLE blood_analysis
        ADD COLUMN IF NOT EXISTS "거리적합" VARCHAR(100)
        """))

        db.execute(text("""
        ALTER TABLE blood_analysis
        ADD COLUMN IF NOT EXISTS "경주마특성" VARCHAR(100)
        """))

        db.commit()

        return {
            "msg":"컬럼 추가 완료"
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# =========================
# 전개분석 자동계산
# =========================
def make_pace_analysis(row):

    score = 0

    # =====================
    # 주행유형
    # =====================

    running = "보통"

    if row.평균경주전개:

        try:

            nums = [
                int(x)
                for x in str(
                    row.평균경주전개
                ).split("-")
                if x.strip().isdigit()
            ]

            if nums:

                avg_pos = (
                    sum(nums) / len(nums)
                )

                if avg_pos <= 3:

                    running = "선행"
                    score += 20

                elif avg_pos <= 6:

                    running = "선입"
                    score += 15

                else:

                    running = "추입"
                    score += 10

        except:
            pass

    # =====================
    # 최근흐름
    # =====================

    trend = "보통"

    if row.최근순위:

        try:

            nums = [
                int(x)
                for x in str(
                    row.최근순위
                ).replace("-", " ")
                 .replace(",", " ")
                 .split()
                if x.isdigit()
            ]

            if nums:

                avg_rank = (
                    sum(nums) / len(nums)
                )

                if avg_rank <= 3:

                    trend = "상승세"
                    score += 30

                elif avg_rank <= 7:

                    trend = "보통"
                    score += 20

                else:

                    trend = "부진"
                    score += 10

        except:
            pass

    # =====================
    # 코스적합
    # =====================

    course = "보통"

    try:

        g3f = float(
            row.평균G3F
        )

        if g3f <= 38:

            course = "우수"
            score += 30

        elif g3f <= 39:

            course = "양호"
            score += 20

        else:

            course = "보통"
            score += 10

    except:
        pass

    # =====================
    # 전개패턴
    # =====================

    pattern = f"{running}형"

    comment = (
        f"{trend}, "
        f"{running} 전개 예상"
    )

    return {

        "주행유형": running,
        "최근흐름": trend,
        "전개패턴": pattern,
        "코스적합": course,
        "코멘트": comment,
        "점수": score

    }
    
@app.get(
"/pace-analysis-data/{region}/{race_no}/{race_date}"
)
def get_pace_analysis_data(

    region:str,
    race_no:int,
    race_date:str,

    db:Session=Depends(get_db)

):

    # 부산 → 부산경남 변환
    if region == "부산":
        region = "부산경남"

    rows = db.query(
        Blood
    ).filter(

        Blood.지역 == region,
        Blood.경주번호 == str(race_no)

    ).all()

    print(
        "조회건수:",
        len(rows)
    )

    date_clean = ''.join(
        c for c in str(race_date)
        if c.isdigit()
    )[:8]

    rows = [

        r for r in rows

        if ''.join(
            c for c in str(r.출전날짜)
            if c.isdigit()
        )[:8] == date_clean

    ]

    print(
        "날짜필터후:",
        len(rows)
    )

    result=[]

    for r in rows:

        # 자동분석
        analysis = make_pace_analysis(r)

        # 저장값 조회
        saved_rows = db.query(
            PaceAnalysis
        ).filter(

            PaceAnalysis.지역 == region,
            PaceAnalysis.경주 == race_no,
            PaceAnalysis.번호 == int(r.번호)

        ).all()

        saved_rows = [

            x for x in saved_rows

            if ''.join(
                c for c in str(x.경주일자)
                if c.isdigit()
            )[:8] == date_clean

        ]

        saved = (
            saved_rows[0]
            if saved_rows
            else None
        )

        print(
            "저장조회:",
            r.번호,
            saved
        )

        result.append({

            "번호": r.번호,
            "마명": r.마명,

            "주행유형":
            saved.주행유형
            if saved
            else analysis["주행유형"],

            "최근흐름":
            saved.최근흐름
            if saved
            else analysis["최근흐름"],

            "전개패턴":
            saved.전개패턴
            if saved
            else analysis["전개패턴"],

            "코스적합":
            saved.코스적합
            if saved
            else analysis["코스적합"],

            "평균경주전개":
            r.평균경주전개,

            "최근순위":
            r.최근순위,

            "도착차":
            r.도착차,

            "평균S1F":
            r.평균S1F,

            "평균G3F":
            r.평균G3F,

            "평균G1F":
            r.평균G1F,

            "최고G3F":
            r.최고G3F,

            "평균훈련량":
            r.평균훈련량,

            "수영훈련":
            r.훈련량수영훈련,

            "코멘트":
            saved.코멘트
            if saved
            else analysis["코멘트"],

            "점수":
            saved.점수
            if saved
            else analysis["점수"]

        })

    return result

@app.post("/save-pace-analysis")
def save_pace_analysis(
    item: schemas.PaceAnalysisSave,
    db: Session = Depends(get_db)
):

    row = db.query(
        PaceAnalysis
    ).filter(

        PaceAnalysis.지역 == item.지역,
        PaceAnalysis.경주 == item.경주,
        PaceAnalysis.경주일자 == item.경주일자,
        PaceAnalysis.번호 == item.번호

    ).first()

    if row:

        row.주행유형 = item.주행유형
        row.최근흐름 = item.최근흐름

        row.전개패턴 = item.전개패턴
        row.코스적합 = item.코스적합

        row.코멘트 = item.코멘트
        row.점수 = item.점수

    else:

        row = PaceAnalysis(

            지역=item.지역,
            경주=item.경주,
            경주일자=item.경주일자,

            번호=item.번호,
            마명=item.마명,

            주행유형=item.주행유형,
            최근흐름=item.최근흐름,

            전개패턴=item.전개패턴,
            코스적합=item.코스적합,

            코멘트=item.코멘트,
            점수=item.점수

        )

        db.add(row)

    db.commit()

    return {
        "msg":"전개분석 저장 완료"
    }