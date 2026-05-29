import pandas as pd
from sqlalchemy.orm import Session

from main import SessionLocal, Jockey

FILE_NAME="KRA_20260515.xlsx"

print("기수 수집 시작")

db:Session=SessionLocal()

try:

    df=pd.read_excel(
        FILE_NAME,
        sheet_name="출전표"
    )

    df=df[["기수명"]]
    df=df.drop_duplicates()

    count=0

    for _,row in df.iterrows():

        exists=db.query(Jockey).filter(
            Jockey.기수명==str(row["기수명"])
        ).first()

        if exists:
            continue

        jockey=Jockey(

            jk_no="",
            기수명=str(row["기수명"]),
            승률="",
            최근성적=""

        )

        db.add(jockey)

        count+=1

    db.commit()

    print(f"기수 {count}건 저장 완료")

except Exception as e:

    print("오류:",e)

finally:

    db.close()
