from sqlalchemy.orm import Session
from main import SessionLocal, Horse, RaceDetail

print("경주마 수집 시작")

db: Session = SessionLocal()

try:

    # 기존 데이터 초기화
    db.query(Horse).delete()
    db.commit()

    details = db.query(RaceDetail).all()

    print("======== RaceDetail 확인 ========")

    count = 0

    for d in details:

        try:

            horse_name = d.마명.strip()

            print("==== 데이터 확인 ====")
            print("마명:", d.마명)
            print("마주:", getattr(d,"마주",None))
            print("부마:", getattr(d,"부마",None))
            print("모마:", getattr(d,"모마",None))
            print("통산전적:", getattr(d,"통산전적",None))
            print("================")

            print("수집:", horse_name)

            exists = db.query(Horse).filter(
                Horse.마명 == horse_name
            ).first()

            if exists:
                db.delete(exists)
                db.commit()

            horse = Horse(

                hr_no="",

                마명=horse_name,

                성별=d.성별 if hasattr(d,"성별") else "",
                나이=d.나이 if hasattr(d,"나이") else "",

                생년월일=d.생년월일 if hasattr(d,"생년월일") else "",

                기수=d.기수 if hasattr(d,"기수") else "",
                조교사=d.조교사 if hasattr(d,"조교사") else "",

                마주=d.마주 if hasattr(d,"마주") else "",

                부마=d.부마 if hasattr(d,"부마") else "",
                모마=d.모마 if hasattr(d,"모마") else "",

                통산전적=d.통산전적 if hasattr(d,"통산전적") else "",
                승률=d.승률 if hasattr(d,"승률") else "",

                수득상금=d.수득상금 if hasattr(d,"수득상금") else "",
               특징=d.특징 if hasattr(d,"특징") else "",

                최근전적=d.최근전적 if hasattr(d,"최근전적") else ""

            )

            db.add(horse)

            count += 1

            print("저장:", horse_name)

        except Exception as e:

            print("오류:", e)

            continue

    db.commit()

    print(f"저장 완료 : {count}건")

except Exception as e:

    print("오류:", e)

finally:

    db.close()
