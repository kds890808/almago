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
    PointHistory
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

    query = db.query(
        RaceDetail
    ).filter(
        RaceDetail.경주 == race_no
    )

    # 지역 먼저 필터
    if region:
        query = query.filter(
            RaceDetail.지역 == region
        )

    # 날짜 필터
    if date:

        rows = query.all()

        input_date = str(date)

        data = []

        for r in rows:

            db_date = str(r.경주일자)

            input_clean = ''.join(
                c for c in input_date
                if c.isdigit()
            )

            db_clean = ''.join(
                c for c in db_date
                if c.isdigit()
            )

            if input_clean[-4:] == db_clean[-4:]:
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

        input_date = str(date)

        data = []

        for r in rows:

            db_date = str(r.경주일자)

            # 숫자만 남김
            input_clean = ''.join(
                c for c in input_date
                if c.isdigit()
            )

            db_clean = ''.join(
                c for c in db_date
                if c.isdigit()
            )

            # 뒤 4자리(월일) 비교
            if input_clean[-4:] == db_clean[-4:]:
                data.append(r)

    else:

        data = query.all()

    return [

    {
        "지역":r.지역 or "",
        "날짜":r.경주일자 or "",
        "경주번호":r.경주 or "",

        "번호":r.번호 or "",
        "마명":r.마명 or "",
        "마중":r.체중 or "",

        "성별":r.성별 or "",
        "연령":r.나이 or "",

        "레이팅":r.레이팅 or "",
        "중량":r.부담중량 or "",
        "증감":r.증감 or "",

        "기수명":r.기수 or "",
        "조교사명":r.조교사 or "",

        "마주명":r.마주명 or "",
        "조교횟수":r.조교횟수 or "",
        "출전주기":r.출전주기 or "",

        "장구현황":r.장구현황 or "",
        "특이사항":r.특이사항 or ""

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
    if current["role"] == "member":
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

    # 회원 확인
    member = db.query(Member).filter(
        Member.email == current["email"]
    ).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    # 분석 찾기
    analysis = db.query(models.Analysis).filter(
        models.Analysis.id == analysis_id
    ).first()

    if not analysis:
        raise HTTPException(404, "분석 없음")

    # 필요 포인트
    need_point = 100

    # 포인트 부족
    if member.point < need_point:
        raise HTTPException(400, "포인트 부족")

    # 포인트 차감
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
        "title":analysis.title,
        "content":analysis.content,
        "remain_point":member.point
    }

# =========================
# AI 사용 포인트 차감
# =========================
@app.post("/use-ai")
def use_ai(
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
):

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

    member = db.query(Member).filter(
        Member.email == current["email"]
    ).first()

    if not member:
        raise HTTPException(404, "회원 없음")

    return {

        "email": member.email,
        "name": member.name,
        "point": member.point,
        "is_premium": member.is_premium

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