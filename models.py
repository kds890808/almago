from sqlalchemy import Column, Integer, String, Boolean
from database import Base

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
