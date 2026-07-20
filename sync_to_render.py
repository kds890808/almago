import os
import sys

from sqlalchemy import create_engine, MetaData, Table, select, delete
from sqlalchemy.orm import sessionmaker


# ============================================================
# 설정
# ============================================================

# 로컬 SQLite DB
LOCAL_DB_URL = "sqlite:///./db.sqlite3"

# Render PostgreSQL 주소
#
# 방법 1)
# Windows 환경변수에 RENDER_DATABASE_URL을 등록
#
# 방법 2)
# 실행할 때 직접 입력
#
# 보안을 위해 코드에 PostgreSQL 비밀번호를 직접 넣지 않음
RENDER_DB_URL = os.getenv("RENDER_DATABASE_URL")


# ============================================================
# 동기화할 테이블
# ============================================================
#
# 회원 / 관리자 / 포인트 / 결제 관련 테이블은
# 절대로 포함하지 않음
#
# 필요한 테이블만 추가하거나 제거하면 됨
# ============================================================

SYNC_TABLES = [

    "race",

    "race_detail",

    "horse",

    "jockey",

    "trainer",

    "trainer_horse",

    "trainer_year",

    "trainer_recent",

    "blood",

    "basic_analysis",

    "blood_analysis",

    "pace_analysis",

    "final_analysis",

    "analysis",

]


# ============================================================
# Render DB 주소 확인
# ============================================================

if not RENDER_DB_URL:

    print()
    print("❌ RENDER_DATABASE_URL이 설정되어 있지 않습니다.")
    print()
    print("CMD에서 먼저 다음과 같이 입력하세요.")
    print()
    print('set RENDER_DATABASE_URL=postgresql://...')
    print()
    print("그 다음:")
    print()
    print("python sync_to_render.py")
    print()

    sys.exit(1)


# Render가 postgres:// 형식으로 제공하는 경우 대응
if RENDER_DB_URL.startswith("postgres://"):

    RENDER_DB_URL = RENDER_DB_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )


# ============================================================
# DB 연결
# ============================================================

print()
print("============================================")
print("🚀 ALMAGO Render DB 동기화")
print("============================================")
print()


local_engine = create_engine(
    LOCAL_DB_URL
)


render_engine = create_engine(
    RENDER_DB_URL,
    pool_pre_ping=True
)


# ============================================================
# 연결 테스트
# ============================================================

try:

    with local_engine.connect() as conn:

        conn.exec_driver_sql(
            "SELECT 1"
        )

    print("✅ 로컬 SQLite 연결 성공")


except Exception as e:

    print()
    print("❌ 로컬 SQLite 연결 실패")
    print(e)

    sys.exit(1)


try:

    with render_engine.connect() as conn:

        conn.exec_driver_sql(
            "SELECT 1"
        )

    print("✅ Render PostgreSQL 연결 성공")


except Exception as e:

    print()
    print("❌ Render PostgreSQL 연결 실패")
    print(e)

    sys.exit(1)


# ============================================================
# MetaData
# ============================================================

local_metadata = MetaData()

render_metadata = MetaData()


local_metadata.reflect(
    bind=local_engine
)


render_metadata.reflect(
    bind=render_engine
)


# ============================================================
# 동기화 시작 확인
# ============================================================

print()
print("동기화 대상:")
print()

for table_name in SYNC_TABLES:

    print(
        "  -",
        table_name
    )


print()
print("⚠️ 위 테이블의 Render 기존 데이터가 삭제되고")
print("   현재 PC의 db.sqlite3 데이터로 교체됩니다.")
print()
print("회원 / 포인트 / 결제 데이터는 건드리지 않습니다.")
print()


confirm = input(
    "계속하려면 YES 입력: "
)


if confirm.strip().upper() != "YES":

    print()
    print("동기화를 취소했습니다.")

    sys.exit(0)


# ============================================================
# 테이블별 동기화
# ============================================================

success_tables = []

failed_tables = []


for table_name in SYNC_TABLES:

    print()
    print("--------------------------------------------")
    print(
        f"📦 {table_name} 동기화 시작"
    )
    print("--------------------------------------------")


    # --------------------------------------------------------
    # 테이블 존재 확인
    # --------------------------------------------------------

    if table_name not in local_metadata.tables:

        print(
            f"⚠️ 로컬에 {table_name} 테이블이 없습니다."
        )

        continue


    if table_name not in render_metadata.tables:

        print(
            f"❌ Render에 {table_name} 테이블이 없습니다."
        )

        failed_tables.append(
            table_name
        )

        continue


    local_table = local_metadata.tables[
        table_name
    ]

    render_table = render_metadata.tables[
        table_name
    ]


    try:

        # ====================================================
        # 로컬 데이터 읽기
        # ====================================================

        with local_engine.connect() as conn:

            rows = conn.execute(
                select(local_table)
            ).mappings().all()


        print(
            f"📊 로컬 데이터: {len(rows)}건"
        )


        # ====================================================
        # Render 컬럼 목록
        # ====================================================

        render_columns = {

            column.name

            for column
            in render_table.columns

        }


        # ====================================================
        # 데이터 변환
        # ====================================================
        #
        # Render에 실제로 존재하는 컬럼만 전송
        #
        # id는 그대로 복사하지 않고
        # PostgreSQL이 새로 생성하도록 제외
        # ====================================================

        insert_rows = []


        for row in rows:

            clean_row = {}


            for key, value in row.items():

                if key == "id":

                    continue


                if key not in render_columns:

                    continue


                # NaN 방어
                try:

                    if value != value:

                        value = None

                except:

                    pass


                clean_row[key] = value


            insert_rows.append(
                clean_row
            )


        # ====================================================
        # Render 데이터 교체
        # ====================================================
        #
        # begin() 사용
        #
        # 해당 테이블 삭제 + 삽입 전체가 성공해야 commit
        #
        # 실패하면 자동 rollback
        # ====================================================

        with render_engine.begin() as conn:

            # 기존 데이터 삭제
            conn.execute(
                delete(render_table)
            )


            # 새 데이터 삽입
            if insert_rows:

                # 한 번에 너무 많은 데이터를 보내지 않도록
                # 500개씩 나누어 INSERT

                batch_size = 500


                for i in range(
                    0,
                    len(insert_rows),
                    batch_size
                ):

                    batch = insert_rows[
                        i:i + batch_size
                    ]


                    conn.execute(
                        render_table.insert(),
                        batch
                    )


                    print(
                        f"   → {min(i + batch_size, len(insert_rows))}"
                        f" / {len(insert_rows)}건"
                    )


        print(
            f"✅ {table_name} 동기화 완료"
        )


        success_tables.append(
            table_name
        )


    except Exception as e:

        print()
        print(
            f"❌ {table_name} 동기화 실패"
        )

        print()
        print(
            "오류:"
        )

        print(
            e
        )


        failed_tables.append(
            table_name
        )


# ============================================================
# 최종 결과
# ============================================================

print()
print()
print("============================================")
print("🏁 동기화 결과")
print("============================================")


print()
print(
    f"✅ 성공: {len(success_tables)}개"
)


for name in success_tables:

    print(
        "   ✔",
        name
    )


print()
print(
    f"❌ 실패: {len(failed_tables)}개"
)


for name in failed_tables:

    print(
        "   ✖",
        name
    )


print()


if failed_tables:

    print(
        "⚠️ 실패한 테이블은 기존 Render 데이터가 유지됩니다."
    )

    print(
        "   오류 내용을 확인한 뒤 해당 테이블만 수정하면 됩니다."
    )


else:

    print(
        "🎉 모든 경주 데이터 동기화가 완료되었습니다."
    )


print()