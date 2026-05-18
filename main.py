from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request, Body
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from database import SessionLocal, engine, Base
import models, schemas
from models import Member, Admin, SuperAdmin, Menu
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
# 경주 테이블
# =========================
class RaceDetail(Base):
    __tablename__="race_detail"

    id=Column(Integer,primary_key=True,index=True)

    지역=Column(String)
    경주일자=Column(String)
    경주=Column(Integer)

    번호=Column(String)
    마명=Column(String)

    기수명=Column(String)
    조교사=Column(String)

    산지=Column(String)
    성별=Column(String)
    연령=Column(String)

    레이팅=Column(String)

    체중=Column(String)
    증감=Column(String)

    전적=Column(String)
    거리전적=Column(String)

    장구현황=Column(String)
    특이사항=Column(String)

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

Base.metadata.create_all(bind=engine)
with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE menus
        ADD COLUMN IF NOT EXISTS template VARCHAR;
    """))
    conn.commit()
app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        is_premium=False
    )

    db.add(new_user)
    db.commit()

    return {"msg": "회원가입 완료"}


# =========================
# 로그인
# =========================
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.email == user.email).first()
    admin = db.query(Admin).filter(Admin.email == user.email).first()
    superadmin = db.query(SuperAdmin).filter(SuperAdmin.email == user.email).first()

    target = member or admin or superadmin

    if not target or not verify_password(user.password, target.password):
        raise HTTPException(400, "로그인 실패")

    role = "member"
    if admin:
        role = "admin"
    if superadmin:
        role = "superadmin"

    token = create_access_token({
        "sub": target.email,
        "role": role
    })

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
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    exist = db.query(SuperAdmin).filter(SuperAdmin.email == email).first()
    if exist:
        raise HTTPException(400, "이미 존재하는 슈퍼관리자")

    new = SuperAdmin(
        email=email,
        password=hash_password(password)
    )

    db.add(new)
    db.commit()

    return {"msg": "슈퍼관리자 생성 완료"}


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

    db = SessionLocal()
    db.query(Race).delete()

    for _, row in df.iterrows():
        race = Race(
            지역=row["지역"],
            순=int(row["순"]),
            경주일자=row["경주일자"],
            경주=int(row["경주"]),
            등급=row["등급"],
            거리=row["거리"],
            편성=row["편성"],
            출전=row["출전"],
            경주명=row["경주명"],
            출발시각=str(row["출발시각"]),
            비고=row["비고"],
        )
        db.add(race)

    db.commit()
    db.close()

    return {"msg": "저장 완료"}
# =========================
# 경주상세보기
# =========================
@app.post("/upload-race-detail")
async def upload_race_detail(
    file: UploadFile=File(...),
    db: Session=Depends(get_db)
):

    df=pd.read_excel(file.file)

    db.query(RaceDetail).delete()

    for _,row in df.iterrows():

        item=RaceDetail(

            지역=row.get("지역",""),
            경주일자=row.get("날짜",""),
            경주=row.get("경주번호",""),

            번호=row.get("번호",""),
            마명=row.get("마명",""),

            기수명=row.get("기수명",""),
            조교사=row.get("조교사명",""),

            산지=row.get("산지",""),
            성별=row.get("성별",""),
            연령=row.get("연령",""),

            레이팅=row.get("레이팅",""),

            체중=row.get("중량",""),
            증감=row.get("증감",""),

            전적=row.get("전적",""),
            거리전적=row.get("해당거리전적",""),

            장구현황=row.get("장구현황",""),
            특이사항=row.get("특이사항","")

        )

        db.add(item)

    db.commit()

    return {"msg":"상세 저장 완료"}
    
@app.get("/race")
def get_race():
    db = SessionLocal()
    data = db.query(Race).all()
    db.close()

    return [
        {
            "id": r.id,
            "지역": r.지역,
            "순": r.순,
            "경주일자": r.경주일자,
            "경주": r.경주,
            "등급": r.등급,
            "거리": r.거리,
            "편성": r.편성,
            "출전": r.출전,
            "경주명": r.경주명,
            "출발시각": r.출발시각,
            "비고": r.비고
        }
        for r in data
    ]


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


# =========================
# 경주 상세 조회
# =========================
@app.get("/race-detail/{region}/{raceDate}/{raceNo}")
def get_race_detail(
    region:str,
    raceDate:str,
    raceNo:int,
    db: Session=Depends(get_db)
):

    formattedDate=(
        raceDate[:4]
        +"/"+
        raceDate[4:6]
        +"/"+
        raceDate[6:8]
    )

    races=db.query(
        RaceDetail
    ).filter(
        RaceDetail.지역==region,
        RaceDetail.경주일자.contains(formattedDate),
        RaceDetail.경주==raceNo
    ).all()

    return [
        {
            "번호": r.번호,
            "마명": r.마명,
            "기수명": r.기수명,
            "조교사": r.조교사,
            "산지": r.산지,
            "성별": r.성별,
            "연령": r.연령,
            "레이팅": r.레이팅,
            "체중": r.체중,
            "증감": r.증감,
            "전적": r.전적,
            "거리전적": r.거리전적,
            "장구현황": r.장구현황,
            "특이사항": r.특이사항
        }
        for r in races
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
            "is_admin": m.email in admin_emails
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
