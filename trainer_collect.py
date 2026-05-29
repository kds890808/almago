import pandas as pd
from sqlalchemy.orm import Session

from main import SessionLocal, Trainer

FILE_NAME="KRA_20260515.xlsx"

print("조교사 수집 시작")

db:Session=SessionLocal()

try:

    df=pd.read_excel(
        FILE_NAME,
        sheet_name="출전표"
    )

    df=df[["조교사명"]]
    df=df.drop_duplicates()

    count=0

    for _,row in df.iterrows():

        exists=db.query(Trainer).filter(
            Trainer.조교사명==str(row["조교사명"])
        ).first()

        if exists:
            continue

        trainer=Trainer(

            tr_no="",
            조교사명=str(row["조교사명"]),
            승률="",
            최근성적=""

        )

        db.add(trainer)

        count+=1

    db.commit()

    print(f"조교사 {count}건 저장 완료")

except Exception as e:

    print("오류:",e)

finally:

    db.close()
