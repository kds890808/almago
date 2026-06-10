from pydantic import BaseModel

# =========================
# 사용자 관련
# =========================
class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    birth: str
    phone: str

class UserLogin(BaseModel):
    email: str
    password: str

# =========================
# 분석 관련
# =========================
class AnalysisCreate(BaseModel):
    title: str
    content: str
    is_premium: bool = False

class AnalysisOut(BaseModel):
    id: int
    title: str
    content: str
    is_premium: bool

    class Config:
        orm_mode = True

# =========================
# 메뉴추가 관련
# =========================
class MenuCreate(BaseModel):

    name: str

    path: str

    icon: str = "📄"

    description: str = ""

    sort_order: int = 0

    is_active: bool = True

    template: str = "link"

class MenuOut(BaseModel):
    id: int
    name: str
    path: str
    is_active: bool
    template: str

    class Config:
        orm_mode = True

# =========================
# 경주전개분석
# =========================
class PaceAnalysisSave(BaseModel):

    지역:str
    경주:int
    경주일자:str

    번호:int
    마명:str

    주행유형:str
    최근흐름:str
    전개패턴:str
    코스적합:str

    코멘트:str
    점수:int