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

    is_premium = Column(Boolean, default=False)


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
    is_active = Column(Boolean, default=True)