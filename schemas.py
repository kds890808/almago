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

class MenuOut(BaseModel):
    id: int
    name: str
    path: str
    is_active: bool

    class Config:
        orm_mode = True

