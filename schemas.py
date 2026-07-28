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
    referred_by: str | None = None
    
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


class FeeUpdate(BaseModel):

    item: str

    point: int

    is_active: bool

    password: str

# =========================
# 관리자 비밀번호변경
# =========================
class PasswordChange(BaseModel):

    current_password:str

    new_password:str

    confirm_password:str    


# =========================
# 이용요금관리
# ========================= 
class ChargeSettingUpdate(BaseModel):

    id:int

    name:str

    point:int

    price:int

    is_active:int

    password:str

class ChargeSettingCreate(BaseModel):

    name:str
    point:int
    price:int
    is_active:int = 1
    password:str            

# =========================
# 충전계좌변경
# =========================   
class ChargeAccountUpdate(BaseModel):

    bank_name:str
    account_number:str
    account_holder:str

    password:str         


# =========================
# 충전신청 요청
# =========================
class ChargeRequestCreate(BaseModel):

    depositor_name:str

    product_name:str

    point:int

    amount:int      

# =========================
# 출석체크
# =========================
class AttendanceCheck(BaseModel):

    email: str    

# =========================
# 퀴즈풀었는지
# =========================
class QuizCheck(BaseModel):

    email: str

    quiz_id: int

    answer: int    