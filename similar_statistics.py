import pandas as pd
import json
import os


# =========================
# 파일 경로
# =========================

EXCEL_PATH = "유사경주분석.xlsx"

OUTPUT_JS = "static/similar_statistics.js"


# =========================
# 기본 설정
# =========================

RANK_NAMES = {
    1: "rank1",
    2: "rank2",
    3: "rank3",
    4: "rank4",
    5: "rank5"
}

NUM_COLS = [
    "거리",
    "착순",
    "마번",
    "RI",
    "CPI",
    "SPR",
    "평균속도지수",
    "최대속도지수",
    "속도폭발력",
    "B",
    "I",
    "C",
    "S",
    "P",
    "DI",
    "CD",
    "COI"
]

STAT_COLS = {
    "gate": "마번",
    "DI": "DI",
    "CD": "CD",
    "COI": "COI",
    "RI": "RI",
    "CPI": "CPI",
    "SPR": "SPR",
    "avgSpeed": "평균속도지수",
    "maxSpeed": "최대속도지수",
    "speedPower": "속도폭발력"
}

PACE_COLS = [
    "B",
    "I",
    "C",
    "S",
    "P"
]


# =========================
# 숫자 변환
# =========================

def to_num(series):

    return pd.to_numeric(
        series,
        errors="coerce"
    )


# =========================
# 평균 / 최소 / 최대
# =========================

def stat_block(df, col):

    if col not in df.columns:
        return empty_stat()

    s = to_num(df[col]).dropna()

    if len(s) == 0:
        return empty_stat()

    avg = float(s.mean())
    std = float(s.std()) if len(s) > 1 else 0
    q1 = float(s.quantile(0.25))
    median = float(s.quantile(0.5))
    q3 = float(s.quantile(0.75))
    iqr = q3 - q1

    cv = None
    if avg != 0:
        cv = std / abs(avg)

    return {
        "count": int(len(s)),

        "avg": round(avg, 2),
        "median": round(median, 2),
        "std": round(std, 2),

        "min": round(float(s.min()), 2),
        "max": round(float(s.max()), 2),

        "q1": round(q1, 2),
        "q3": round(q3, 2),
        "iqr": round(iqr, 2),

        # 우수 오차범위
        "goodMin": round(q1, 2),
        "goodMax": round(q3, 2),

        # 평균 기준 참고범위
        "stdMin": round(avg - std, 2),
        "stdMax": round(avg + std, 2),

        "cv": round(cv, 3) if cv is not None else None
    }


def empty_stat():

    return {
        "count": 0,
        "avg": None,
        "median": None,
        "std": None,
        "min": None,
        "max": None,
        "q1": None,
        "q3": None,
        "iqr": None,
        "goodMin": None,
        "goodMax": None,
        "stdMin": None,
        "stdMax": None,
        "cv": None
    }


# =========================
# 전개 평균
# =========================

def pace_summary(df):

    result = {}

    for col in PACE_COLS:

        result[col] = stat_block(
            df,
            col
        )

    return result


# =========================
# 가장 강한 전개값
# =========================

def best_pace_name(pace):

    if not pace:
        return "-"

    valid = {}

    for k, v in pace.items():

        if (
            isinstance(v, dict)
            and v.get("avg") is not None
        ):
            valid[k] = v["avg"]

    if not valid:
        return "-"

    best = max(
        valid,
        key=valid.get
    )

    name_map = {
        "B":"도주형",
        "I":"선행형",
        "C":"선입형",
        "S":"추입형",
        "P":"후미형"
    }

    return name_map.get(best, best)


# =========================
# 게이트 구간
# =========================

def gate_zone(avg_gate):

    if avg_gate is None:

        return "-"

    if avg_gate <= 4:
        return "1~4번 (내측)"

    if avg_gate <= 8:
        return "5~8번 (중간)"

    return "9번 이상 (외측)"


# =========================
# 단일 착순 통계
# =========================

def rank_summary(group, rank_no):

    target = group[
        group["착순"] == rank_no
    ]

    result = {
        "count": int(len(target))
    }

    for out_key, col in STAT_COLS.items():

        result[out_key] = stat_block(
            target,
            col
        )

    result["pace"] = pace_summary(
        target
    )

    result["paceScore"] = {}

    for col in PACE_COLS:


        result["bestPace"] = best_pace_name(
            result["pace"]
        )

    result["gateZone"] = gate_zone(
        result["gate"]["avg"]
    )

    return result


# =========================
# Top N 통계
# =========================

def top_summary(group, max_rank):

    target = group[
        group["착순"] <= max_rank
    ]

    result = {
        "count": int(len(target))
    }

    for out_key, col in STAT_COLS.items():

        result[out_key] = stat_block(
            target,
            col
        )

    result["pace"] = pace_summary(
        target
    )


    result["bestPace"] = best_pace_name(
        result["pace"]
    )

    result["gateZone"] = gate_zone(
        result["gate"]["avg"]
    )

    return result


# =========================
# 게이트 카운트
# =========================

def gate_count_summary(group, max_rank):

    target = group[
        group["착순"] <= max_rank
    ]

    gate_series = to_num(
        target["마번"]
    ).dropna()

    counts = {}

    for gate in range(1, 15):

        counts[str(gate)] = int(
            (gate_series == gate).sum()
        )

    total = int(
        gate_series.count()
    )

    if total == 0:

        return {
            "total": 0,
            "counts": counts,
            "bestGate": "-",
            "bestZone": "-"
        }

    best_gate = max(
        counts,
        key=counts.get
    )

    zone_counts = {
        "내측": sum(
            counts[str(i)]
            for i in range(1, 5)
        ),
        "중간": sum(
            counts[str(i)]
            for i in range(5, 9)
        ),
        "외측": sum(
            counts[str(i)]
            for i in range(9, 15)
        )
    }

    best_zone = max(
        zone_counts,
        key=zone_counts.get
    )

    zone_rates = {
        k: round(v / total * 100, 1)
        for k, v in zone_counts.items()
    }

    gate_rates = {
        k: round(v / total * 100, 1)
        for k, v in counts.items()
    }

    worst_gate = min(
        counts,
        key=counts.get
    )

    worst_zone = min(
        zone_counts,
        key=zone_counts.get
    )

    return {
        "total": total,
        "counts": counts,
        "rates": gate_rates,

        "bestGate": best_gate,
        "bestGateRate": gate_rates[best_gate],

        "worstGate": worst_gate,
        "worstGateRate": gate_rates[worst_gate],

        "bestZone": best_zone,
        "worstZone": worst_zone,

        "zoneCounts": zone_counts,
        "zoneRates": zone_rates,

        "insideRate": zone_rates["내측"],
        "middleRate": zone_rates["중간"],
        "outsideRate": zone_rates["외측"]
    }


# =========================
# 조건 요약
# =========================

def condition_summary(group):

    race_count = int(
        len(
            group[
                group["착순"] == 1
            ]
        )
    )

    #race_count = real_race_count * 10    

    top3 = top_summary(
        group,
        3
    )

    top5 = top_summary(
        group,
        5
    )

    gate_top3 = gate_count_summary(
        group,
        3
    )

    gate_top5 = gate_count_summary(
        group,
        5
    )

    top5_di = top5["DI"]
    top5_cd = top5["CD"]
    top5_coi = top5["COI"]

    blood_comment = (
        f"DI {top5_di['goodMin']}~{top5_di['goodMax']} / "
        f"CD {top5_cd['goodMin']}~{top5_cd['goodMax']} / "
        f"COI {top5_coi['goodMin']}~{top5_coi['goodMax']}"
    )

    gate_comment = (
        f"{gate_top5['bestZone']} 구간의 입상 비율이 "
        f"{gate_top5['zoneRates'][gate_top5['bestZone']]}%로 가장 높았습니다."
    )

    pace_comment = (
        f"{top5['bestPace']} 전개가 가장 우세했습니다."
    )

    summary_comment = (
        f"최근 {race_count}경주를 분석한 결과, "
        f"{gate_top5['bestZone']} 게이트와 "
        f"{top5['bestPace']} 전개가 강세였습니다."
    )

    return {
        "raceCount": race_count,

        "top3BestGateZone": gate_top3["bestZone"],
        "top5BestGateZone": gate_top5["bestZone"],

        "top3BestPace": top3["bestPace"],
        "top5BestPace": top5["bestPace"],

        "top3AvgDI": top3["DI"]["avg"],
        "top3AvgCD": top3["CD"]["avg"],
        "top3AvgCOI": top3["COI"]["avg"],

        "top5AvgDI": top5["DI"]["avg"],
        "top5AvgCD": top5["CD"]["avg"],
        "top5AvgCOI": top5["COI"]["avg"],

        "top5GoodDI": {
            "min": top5_di["goodMin"],
            "max": top5_di["goodMax"]
        },

        "top5GoodCD": {
            "min": top5_cd["goodMin"],
            "max": top5_cd["goodMax"]
        },

        "top5GoodCOI": {
            "min": top5_coi["goodMin"],
            "max": top5_coi["goodMax"]
        },

        "bloodComment": blood_comment,
        "gateComment": gate_comment,
        "paceComment": pace_comment,
        "summaryComment": summary_comment
    }

# =========================
# 유사경주 TOP5
# =========================
def similar_top5(group):

    # 최근 경주부터 정렬
    group = group.sort_values(
        ["날짜", "경주번호"],
        ascending=False
    )

    # 같은 경주는 하나만 남김
    top5 = (
        group
        .drop_duplicates(
            subset=["날짜", "지역", "경주번호"]
        )
        .head(5)
    )

    result = []

    for _, row in top5.iterrows():

        winner = group[
            (group["날짜"] == row["날짜"]) &
            (group["지역"] == row["지역"]) &
            (group["경주번호"] == row["경주번호"]) &
            (group["착순"] == 1)
        ]

        if len(winner):

            w = winner.iloc[0]

            winner_name = w["마명"]

            gate = int(w["마번"])

            di = round(float(w["DI"]), 2)

            cd = round(float(w["CD"]), 2)

            coi = round(float(w["COI"]), 2)

        else:

            winner_name = "-"

            gate = None

            di = None

            cd = None

            coi = None

        result.append({

            "date": str(row["날짜"]),

            "region": row["지역"],

            "raceNo": int(row["경주번호"]),

            "winner": winner_name,

            "track": row["주로상태"],

            "distance": int(row["거리"]),

            "grade": row["등급"],

            "gate": gate,

            "di": di,

            "cd": cd,

            "coi": coi

        })

    print(top5[["날짜","지역","경주번호","마명","착순"]])

    print("===== TOP5 RESULT =====")
    print(result)

    return result

# =========================
# 등급 정리
# =========================

def clean_grade(v):

    if pd.isna(v):

        return "-"

    return str(v).strip()


# =========================
# 거리 정리
# =========================

def clean_distance(v):

    if pd.isna(v):

        return None

    try:

        return str(
            int(float(v))
        )

    except Exception:

        return str(v).strip()


# =========================
# 메인 실행
# =========================

print("엑셀 읽는 중...")

df = pd.read_excel(
    EXCEL_PATH
)

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)

print("컬럼:")
print(
    df.columns.tolist()
)

# =========================
# 필수 컬럼 확인
# =========================

required_cols = [
    "거리",
    "등급",
    "착순",
    "마번"
]

missing = [
    col
    for col in required_cols
    if col not in df.columns
]

if missing:

    raise ValueError(
        f"필수 컬럼 없음: {missing}"
    )


# =========================
# 숫자형 변환
# =========================

for col in NUM_COLS:

    if col in df.columns:

        df[col] = to_num(
            df[col]
        )


# =========================
# 결측 제거
# =========================

df = df.dropna(
    subset=[
        "거리",
        "등급",
        "착순"
    ]
)


# =========================
# 통계 생성
# =========================

statistics = {}

groups = df.groupby(
    [
        "거리",
        "등급"
    ],
    dropna=True
)

print()
print(
    f"총 {len(groups)}개 조건 분석"
)

for (distance, grade), group in groups:

    distance_key = clean_distance(
        distance
    )

    grade_key = clean_grade(
        grade
    )

    if distance_key is None:

        continue

    key = f"{distance_key}_{grade_key}"

    race_count = int(
        len(
            group[
                group["착순"] == 1
            ]
        )
    )

    if race_count == 0:

        continue

    item = {
        "raceCount": race_count
    }

    for rank_no, rank_key in RANK_NAMES.items():

        item[rank_key] = rank_summary(
            group,
            rank_no
        )

    item["top3"] = top_summary(
        group,
        3
    )

    item["top5"] = top_summary(
        group,
        5
    )

    item["gateTop3"] = gate_count_summary(
        group,
        3
    )

    item["gateTop5"] = gate_count_summary(
        group,
        5
    )

    item["summary"] = condition_summary(
        group
    )

# =========================
# 유사경주 TOP5
# =========================
    item["similarTop5"] = similar_top5(group)

    statistics[key] = item


# =========================
# JS 파일 생성
# =========================

os.makedirs(
    os.path.dirname(OUTPUT_JS),
    exist_ok=True
)

with open(
    OUTPUT_JS,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "const similarStatistics = "
    )

    json.dump(
        statistics,
        f,
        ensure_ascii=False,
        indent=4
    )

    f.write(
        ";"
    )


# =========================
# 확인 출력
# =========================

print()
print("완료!")
print(
    f"{len(statistics)}개 조건 저장"
)
print(
    OUTPUT_JS
)

print()
print("샘플 출력:")

for key in list(statistics.keys())[:5]:

    stat = statistics[key]

    print("=" * 50)
    print(key)
    print(
        "분석경주수:",
        stat["raceCount"]
    )
    print(
        "1위 DI:",
        stat["rank1"]["DI"]
    )
    print(
        "1위 CD:",
        stat["rank1"]["CD"]
    )
    print(
        "1위 COI:",
        stat["rank1"]["COI"]
    )
    print(
        "1위 평균마번:",
        stat["rank1"]["gate"]
    )
    print(
        "Top3 평균 DI:",
        stat["top3"]["DI"]
    )
    print(
        "Top5 평균 DI:",
        stat["top5"]["DI"]
    )
    print(
        "Top5 유리 게이트:",
        stat["gateTop5"]["bestZone"]
    )
    print(
        "Top5 우세 전개:",
        stat["top5"]["bestPace"]
    )