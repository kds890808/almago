function showAnalysisTab(tab){

document
.querySelectorAll(".analysis-section")
.forEach(el=>{
el.classList.remove("active");
});

document
.querySelectorAll(".analysis-tab-btn")
.forEach(el=>{
el.classList.remove("active");
});

document
.getElementById(`tab-${tab}`)
.classList.add("active");

document
.getElementById(`btn-${tab}`)
.classList.add("active");

}

async function loadUserInfo(){

    const token =
    localStorage.getItem(
        "token"
    );

    if(!token){
        return;
    }

    const res =
    await fetch(
        "/my-info",
        {
            headers:{
                Authorization:
                `Bearer ${token}`
            }
        }
    );

    const user =
    await res.json();

    document.getElementById(
    "user-name"
    ).innerHTML =
    `👤 ${user.name}님`;

    document.getElementById(
    "user-point"
    ).innerHTML =
    `💰 ${user.point}P`;

}

async function loadAI(
    region,
    raceNo
) {

    const token =
    localStorage.getItem(
        "token"
    );

    if(!token){
        alert("로그인이 필요합니다.");
        return;
    }    

    const feeRes =
    await fetch(
    "/fee-settings"
    );

    const feeData =
    await feeRes.json();

    basicFee =
    feeData.find(
    x=>x.item==="basic"
    )?.point || 100;

  const res = await fetch(
  "/analysis-table",
{
    headers: {
      "Authorization": "Bearer " + token
    }
  });

  if (!res.ok) {

    alert("출전표가 아직 등록되지 않았습니다.");
    return;

}

  const data = await res.json();


const filtered =
data.filter(r =>

    r.지역 === region &&

    String(r.경주) ===
    String(raceNo)

);

const latest =
filtered.length
? [filtered[0]]
: [];

console.log(
"filtered 개수:",
filtered.length
);

console.log(
"filtered 데이터:",
filtered
);

  


  if(filtered.length === 0){

    document.getElementById(
        "analysis-area"
    ).innerHTML =
    "현재 표시할 AI 분석이 없습니다.";

    return;

}
  
  const area = document.getElementById("analysis-area");
  area.innerHTML = "";

  for (const r of latest) {

    const detailRes = await fetch(
`/race-detail-data/${r.경주}?date=${r.경주일자}&region=${r.지역}`
);

    const detailData =
    await detailRes.json();


console.log(
"선택AI",
r
);

const raceDate =
String(r.경주일자)
.replace(/\//g,"");

console.log(
"raceDate",
raceDate
);

console.log(
"기본분석 URL",
`/user-basic-analysis/${r.지역}/${r.경주}/${raceDate}`
);

const basicRes = await fetch(
`/user-basic-analysis/${r.지역}/${r.경주}/${raceDate}`
);

const basicData =
await basicRes.json();

let basicTable = "";
let basicComment = "";
let compareCards = "";

const commentGroups = {
    "S": [],
    "A+": [],
    "A": [],
    "B+": [],
    "B": [],
    "C+": [],
    "C": [],
    "D+": [],
    "D": [],
    "F": [],
    "E": []
};

const gradeNames = {
    "S": "🏆 S 최상위",
    "A+": "🥇 A+ 강력추천",
    "A": "🥈 A 입상유력",
    "B+": "🟦 B+ 경쟁력",
    "B": "🟨 B 복병주의",
    "C+": "🟧 C+ 변수주의",
    "C": "👀 C 관망",
    "D+": "⚠️ D+ 열세",
    "D": "⚠️ D 열세",
    "F": "🚫 F 어려움",
    "E": "🚫 E 어려움"
};

console.log(
"basicData =",
basicData
);

// =======================
// 기본분석 1위
// =======================

const topHorse = basicData[0];

// =======================
// TOP5
// =======================

const top5 = basicData.slice(0,5);

// =======================
// 복병마 선정
// TOP5 제외 말 중
// 기본점수 + 기수 + 조교사 경쟁력 평가
// =======================

const darkHorseCandidates =
basicData.slice(5);

const darkHorse =
darkHorseCandidates
.map(h=>{

    const basicScore =
        Number(h.점수) || 0;

    const jockeyRate =
        parseFloat(h.기수승률) || 0;

    const trainerRate =
        parseFloat(h.조교사승률) || 0;

    return {
        ...h,

        darkScore:
            basicScore * 0.5 +
            jockeyRate * 1.5 +
            trainerRate * 1.2
    };

})
.sort(
    (a,b)=>
    b.darkScore - a.darkScore
)[0];

// =======================
// 최저점수
// =======================

const minScore = Math.min(
    ...basicData.map(h => Number(h.점수))
);

// =======================
// 성별 통계
// =======================

const maleCount =
    basicData.filter(h => h.성별 === "수").length;

const femaleCount =
    basicData.filter(h => h.성별 === "암").length;

const geldingCount =
    basicData.filter(h => h.성별 === "거").length;

const totalCount =
    basicData.length;

const maleAngle =
    maleCount / totalCount * 360;

const femaleAngle =
    femaleCount / totalCount * 360;

const geldingAngle =
    geldingCount / totalCount * 360;    

// =======================
// 연령 통계
// =======================

const ageMap = {};

basicData.forEach(h => {

    const age = Number(h.나이);

    if (!isNaN(age)) {

        ageMap[age] = (ageMap[age] || 0) + 1;

    }

});

const maxAgeCount = Math.max(...Object.values(ageMap));

// =======================
// Hero
// =======================

const heroHtml = `

<div class="basic-hero">

    <div class="basic-hero-title">

        🏆 1위 예상마 정보

    </div>

<div class="basic-hero-result">

    <div class="basic-hero-name">
        ${topHorse.번호} ${topHorse.마명}
    </div>

    <div
    class="basic-hero-score count-up"
    data-target="${topHorse.점수}"
    >
        ${topHorse.점수}점
    </div>

</div>

<!-- 여기 추가 -->
<div class="basic-mini-grid">

    <div class="basic-mini-card">

        <div class="mini-title">

            🏇 출전마

        </div>

        <div class="mini-value">

            ${basicData.length}두

        </div>

    </div>

    <div class="basic-mini-card">

        <div class="mini-title">

            📉 최저점

        </div>

        <div class="mini-value">

            ${minScore}

        </div>

    </div>

    <div class="basic-mini-card">

        <div class="mini-title">

            🏆 최고점

        </div>

        <div class="mini-value">

            ${topHorse.점수}

        </div>

    </div>

</div>

</div>

</div>


`;

const top5Html = `

<div class="top5-area">

<h3>🏆 AI 추천 TOP5(+복병마)</h3>

<div class="top5-grid">

${top5.map((h,index)=>`

<div class="top5-card">

<div class="top5-rank">

${
index===0 ? "🥇" :
index===1 ? "🥈" :
index===2 ? "🥉" :
index===3 ? "④" :
"⑤"
}

</div>

<div class="top5-name">

${h.번호}
${h.마명}

</div>

<div class="top5-score">

${h.점수}점

</div>

<div class="top5-reason">

${makeReason(h)}

</div>

</div>

`).join("")}

${darkHorse ? `

<div class="top5-card darkhorse-card">

    <div class="top5-rank">
        🐎
    </div>

    <div class="top5-name">
        ${darkHorse.번호}
        ${darkHorse.마명}
    </div>

    <div class="top5-score">
        ${darkHorse.점수}점
    </div>

    <div class="top5-reason">
        🌑 복병마
    </div>

</div>

` : ""}
</div>

</div>

`;

function makeReason(h){

const horse = Number(h.점수);
const jockey = Number(h.기수승률);
const trainer = Number(h.조교사승률);

// 완성형
if(
horse>=95 &&
jockey>=20 &&
trainer>=15
){
return "👑 완성형";
}

// 폭발력
if(horse>=95){
return "🔥 폭발력";
}

// 기수형
if(jockey>=20){
return "⚡ 기수강점";
}

// 조교형
if(trainer>=15){
return "🛡️ 조교강점";
}

// 균형형
if(
horse>=70 &&
jockey>=10 &&
trainer>=10
){
return "⚖️ 균형형";
}

// 기본
return "🎯 다크호스";

}

// =======================
// 기본분석
// =======================

basicData.forEach(h=>{

    console.log(
        "개별데이터",
        h
    );

    let scoreClass = "";
    let rankText = "";
    let jockeyClass = "";
    let trainerClass = "";

    const jockey =
    parseFloat(h.기수승률) || 0;

    const trainer =
    parseFloat(h.조교사승률) || 0;

    // ===================
    // 기수
    // ===================

    if(jockey>=20){

        jockeyClass="rate-excellent";

    }else if(jockey>=15){

        jockeyClass="rate-good";

    }else if(jockey>=10){

        jockeyClass="rate-mid";

    }else{

        jockeyClass="rate-low";

    }

    // ===================
    // 조교사
    // ===================

    if(trainer>=18){

        trainerClass="rate-excellent";

    }else if(trainer>=14){

        trainerClass="rate-good";

    }else if(trainer>=10){

        trainerClass="rate-mid";

    }else{

        trainerClass="rate-low";

    }

    if(h.점수 >= 100){

        scoreClass = "score-top";
        rankText = "🥇 유력";

    }else if(h.점수 >= 70){

        scoreClass = "score-good";
        rankText = "🥈 주력";

    }else if(h.점수 >= 50){

        scoreClass = "score-mid";
        rankText = "🥉 관심";

    }else{

        scoreClass = "score-low";
        rankText = "관망";

    }

    basicTable += `
    <tr>

    <td>${h.번호}</td>

    <td>${h.마명}</td>

    <td>
    <span class="rate-badge ${jockeyClass}">
    ${h.기수승률}
    </span>
    </td>

    <td>
    <span class="rate-badge ${trainerClass}">
    ${h.조교사승률}
    </span>
    </td>

    </tr>
    `;

    const gradeLine =
    (h.코멘트 || "")
    .split("\n")[0]
    .trim();

    let grade =
    gradeLine.split(" ")[0];

    if(!commentGroups[grade]){
        grade = "E";
    }

    commentGroups[grade].push(h);

});


function parseRecord(text){

    console.log("원본=", text);

    if(!text) return null;

    text = String(text).trim();

    console.log("trim=", text);

    const m = text.match(/^(\d+)\((.*?)\)$/);

    console.log("match=", m);

    if(!m) return null;

    const total = Number(m[1]);

    const arr = m[2]
        .split("/")
        .map(Number);

    console.log(arr);

    const first = arr[0] || 0;
    const second = arr[1] || 0;
    const third = arr[2] || 0;
    const fourth = arr[3] || 0;
    const fifth = arr[4] || 0;

    const etc =
        total -
        first -
        second -
        third -
        fourth -
        fifth;

    const placeRate =
        total
        ? ((first + second + third) / total * 100).toFixed(1)
        : 0;

    return {
        total,
        first,
        second,
        third,
        fourth,
        fifth,
        etc,
        placeRate
    };
}

compareCards += `

<div class="compare-card">

    <div id="score"></div>
<h3 class="section-title">🏆 1. 기본능력 점수</h3>

    ${[...basicData]
        .sort((a,b)=>Number(b.점수)-Number(a.점수))
        .map((h,i)=>`

        <div class="compare-row">

            <div class="compare-rank">
                ${i===0?"🥇":i===1?"🥈":i===2?"🥉":`${i+1}위`}
            </div>

            <div class="compare-name">
                ${h.번호}번 ${h.마명}
            </div>

            <div class="compare-value">
                ${h.점수}점
            </div>

        </div>

        `).join("")}

</div>


    <div class="compare-card">

    <div id="age"></div>
    <h3 class="section-title">🎂 2. 연령 분포</h3>

    ${Object.entries(ageMap)

    .sort((a, b) => Number(a[0]) - Number(b[0]))

    .map(([age, count]) => `

    <div class="age-row">

        <span class="age-label">
            ${age}세
        </span>

        <div class="age-bar">

            <div
                class="age-fill"
                style="width:${(count / maxAgeCount) * 100}%">
            </div>

        </div>

        <span class="age-count">
            ${count}두
            ${count === maxAgeCount ? "🏆" : ""}
        </span>

    </div>

    `).join("")}

    </div>

<div class="compare-card">

    <div id="gender"></div>
    <h3 class="section-title">⚥ 3. 성별 분포</h3>

    <div class="gender-chart">

            <div
            class="gender-circle"

            style="
            background:
            conic-gradient(

            #3b82f6 0deg ${maleAngle}deg,

            #ec4899 ${maleAngle}deg ${maleAngle+femaleAngle}deg,

            #22c55e ${maleAngle+femaleAngle}deg 360deg

            );

            "
            >

        <div class="gender-center">

        <div class="gender-title">
        출전
        </div>

        <div class="gender-total">
        ${totalCount}두
        </div>

        </div>

        </div>

    </div>

    <div class="gender-item">

    <span class="male-dot"></span>

    수말

    <b>${maleCount}두</b>

    </div>

    <div class="gender-item">

    <span class="female-dot"></span>

    암말

    <b>${femaleCount}두</b>

    </div>

    <div class="gender-item">

    <span class="gelding-dot"></span>

    거세

    <b>${geldingCount}두</b>

    </div>

</div>

<div class="compare-card">

<div id="record"></div>
<h3 class="section-title">🏆 4. 통산 전적</h3>

${basicData.map(h=>{

console.log(h.최근순위);
console.log(h.통산전적);

const r = parseRecord(h.통산전적);
    if(!r){

        return `
        <div class="record-card">

        <b>${h.번호} ${h.마명}</b>

        <div>데이터 없음</div>

        </div>
        `;

    }

    return `

    <div class="record-card">

        <div class="record-title">
            ${h.번호} ${h.마명}
        </div>

        <div class="record-total">
            출전 ${r.total}전
        </div>

        <div class="record-grid">

            <span>🥇 ${r.first}회</span>
            <span>🥈 ${r.second}회</span>
            <span>🥉 ${r.third}회</span>
            <span>④ ${r.fourth}회</span>
            <span>⑤ ${r.fifth}회</span>
            <span>➅↓ ${r.etc}회</span>

        </div>

        <div class="record-rate">
            ⭐ 입상률 ${r.placeRate}%
        </div>

    </div>

    `;

}).join("")}

</div>


<div class="compare-card">

    <div id="rating"></div>
    <h3 class="section-title">⭐ 5. 레이팅 비교</h3>

    ${[...basicData]
        .sort(
            (a, b) =>
            Number(b.레이팅 || 0) -
            Number(a.레이팅 || 0)
        )
        .map((h, i) => `

        <div class="compare-row">

            <div class="compare-rank">
                ${
                    i === 0
                    ? "🥇"
                    : i === 1
                    ? "🥈"
                    : i === 2
                    ? "🥉"
                    : `${i + 1}위`
                }
            </div>

            <div class="compare-name">
                ${h.번호}번 ${h.마명}
            </div>

            <div class="compare-value">
                ${
                    h.레이팅 &&
                    h.레이팅 !== "-"
                    ? h.레이팅
                    : "-"
                }
            </div>

        </div>

        `).join("")}

</div>

`;

basicComment = "";

Object.keys(commentGroups).forEach(g=>{

    const horses = commentGroups[g];

    if(horses.length===0){
        return;
    }

    basicComment += `

    <details class="comment-group">

    <summary>

    ${gradeNames[g]}
    (${horses.length}두)

    </summary>

    `;

    basicComment += `

    <div class="group-comment">

    ${getGroupComment(g)}

    </div>

    `;    

    horses.forEach(h=>{

        const lines =
        (h.코멘트 || "")
        .split("\n")
        .map(v=>v.trim())
        .filter(v=>v);

        const flags =
        lines.filter(v=>
            v.startsWith("🔥") ||
            v.startsWith("🎯") ||
            v.startsWith("⚠")
        );

        const detail =
        lines.filter(v=>
            !v.startsWith("S") &&
            !v.startsWith("A") &&
            !v.startsWith("B") &&
            !v.startsWith("C") &&
            !v.startsWith("D") &&
            !v.startsWith("E") &&
            !v.startsWith("F") &&
            !v.startsWith("🔥") &&
            !v.startsWith("🎯") &&
            !v.startsWith("⚠")
        ).join("<br>");

        basicComment += `

        <div class="comment-item">

            <div class="comment-title">

                <b>
                🐎 ${h.번호} ${h.마명}
                </b>

                <span class="comment-score">
                ${h.점수}점
                </span>

            </div>

            <div class="comment-flags">

                ${
                    flags
                    .map(f=>`<span>${f}</span>`)
                    .join("")
                }

            </div>

            <details class="horse-detail" open>

                <summary>
                상세 AI 코멘트
                </summary>

                <div class="comment-detail">
                    ${detail || "-"}
                </div>

            </details>

        </div>

        `;

    });

    basicComment += `
    </details>
    `;

});


console.log(
"조회",
r.지역,
r.경주,
r.경주일자
);

console.log(detailData);

    area.innerHTML += `
      <div style="background:white; padding:20px; margin-bottom:20px; border-radius:10px;">

        <h3>${r.지역} ${r.경주}경주</h3>

        

<details class="entry-detail">

<summary>

🏇 출전마 정보 (클릭하여 펼치기)

</summary>

<div class="table-wrap">

<table>

<div class="table-wrap">

<table>

<tr>

<th>번호</th>
<th>마명</th>
<th>성별</th>
<th>나이</th>
<th>레이팅</th>
<th>중량</th>
<th>증감</th>
<th>기수</th>
<th>조교사</th>
<th>마주</th>
<th>조교횟수</th>
<th>출전주기</th>

</tr>

${detailData.map(h=>`

<tr>

<td>${h.번호}</td>

<td>

<a
class="info-pill"
href="#"
onclick="
event.preventDefault();
showHorseInfo(
'${h.마명}'
)
"
>

🐎 ${h.마명}

</a>

</td>

<td>${h.성별 || "-"}</td>

<td>${h.나이 || "-"}</td>

<td>${h.레이팅 || "-"}</td>

<td>${h.부담중량 || "-"}</td>

<td>${h.증감 || "-"}</td>

<td>

<a
class="info-pill"
href="#"
onclick="
event.preventDefault();
showJockeyInfo(
'${h.기수}'
)
"
>

🏇 ${h.기수 || "-"}

</a>

</td>

<td>

<a
class="info-pill"
href="#"
onclick="
event.preventDefault();
showTrainerInfo(
'${h.조교사}'
)
"
>

👨‍🏫 ${h.조교사 || "-"}

</a>

</td>

<td>${h.마주명 || "-"}</td>

<td>${h.조교횟수 || "-"}</td>

<td>${h.출전주기 || "-"}</td>

</tr>

`).join("")}

</table>

</div>

</details>

<div
id="tab-basic"
class="analysis-section active"
>

<div id="top5"></div>

${top5Html}

${heroHtml}

<div class="basic-summary">

    <div class="summary-icon">
        🤖
    </div>

    <div class="summary-text">

        <b>${topHorse.번호} ${topHorse.마명}</b>은
        이번 경주에서 가장 높은 기본능력 점수를 기록했습니다.

        기수, 조교사, 기본능력 등을 종합했을 때
        가장 안정적인 전력으로 평가됩니다.

    </div>

</div>



${compareCards}

<br>

<div id="jockey"></div>
<h3 class="section-title">🏇 6. 기수·조교사 승률 비교</h3>

<div class="table-wrap compare-table-wrap">

<table>

<thead>
<tr>
<th>번호</th>
<th>마명</th>
<th>🏇 기수</th>
<th>👨‍🏫 조교사</th>
</tr>
</thead>

<tbody>

${basicTable}

</tbody>

</table>

</div>


<br>

</div>

<br>

<div class="table-wrap compare-table-wrap">

<div id="training"></div>
<h3 class="section-title">📅 7. 출전주기 · 🏋 조교횟수</h3>

<table>

<thead>

<tr>
<th>번호</th>
<th>마명</th>
<th>출전주기</th>
<th>조교횟수</th>
</tr>

</thead>

<tbody>

${[...basicData].map(h=>`

<tr>

<td>${h.번호}</td>
<td>${h.마명}</td>
<td>
    <span class="compare-badge">
        ${h.출전주기 || "-"}
    </span>
</td>

<td>
    <span class="compare-badge">
        ${h.조교횟수 || "-"}
    </span>
</td>

</tr>

`).join("")}

</tbody>

</table>

</div>

<br>

<div class="table-wrap compare-table-wrap">

<div id="swim"></div>
<h3 class="section-title">🏊 8. 평균훈련량 · 수영훈련</h3>

<table>

<thead>

<tr>
<th>번호</th>
<th>마명</th>
<th>평균훈련량</th>
<th>수영훈련</th>
</tr>

</thead>

<tbody>

${[...basicData].map(h=>`

<tr>

<td>${h.번호}</td>
<td>${h.마명}</td>
<td>${h.평균훈련량 || "-"}</td>
<td>

${(() => {

    if(!h.수영훈련 || h.수영훈련=="-")
        return "-";

    const txt = h.수영훈련;

    const match = txt.match(/(.*?분)\s*(.*)/);

    if(!match) return txt;

    return `
        <div class="swim-main">${match[1]}</div>
        <div class="swim-sub">${match[2]}</div>
    `;

})()}

</td>

</tr>

`).join("")}

</tbody>

</table>

</div>

<br>

<div id="comment"></div>
<h3 class="section-title">📝 9. AI 코멘트</h4>

${basicComment}

</div>

</div>

</div>

`;

}

}

const params =
new URLSearchParams(
location.search
);

const region =
params.get("region");

const raceNo =
params.get("raceNo");

console.log(
"지역:",
region,
"경주:",
raceNo
);

loadUserInfo();

loadAI(
    region,
    raceNo
);;

let modalResolve = null;

function showModal(
title,
message,
icon="📌"
){

    return new Promise(resolve=>{

        modalResolve = resolve;

        document.getElementById(
        "modal-title"
        ).innerHTML = title;

        document.getElementById(
        "modal-message"
        ).innerHTML = message;

        document.getElementById(
        "modal-icon"
        ).innerHTML = icon;

        document.getElementById(
        "custom-modal"
        ).style.display = "flex";

    });

}

function closeModal(result){

    document.getElementById(
    "custom-modal"
    ).style.display = "none";

    if(modalResolve){

        modalResolve(result);

    }

}

async function showJockeyInfo(jockeyName){

const res = await fetch(
`/jockey/${encodeURIComponent(jockeyName)}`
);

const j = await res.json();

let html=`

<div style="
display:flex;
align-items:center;
gap:15px;
margin-bottom:20px;
">

<div style="
width:65px;
height:65px;
border-radius:50%;
background:#dcfce7;
display:flex;
align-items:center;
justify-content:center;
font-size:34px;
">

🏇

</div>

<div>

<div style="
font-size:28px;
font-weight:800;
">

${j.기수명 || jockeyName}

</div>

<div style="
color:#666;
font-size:14px;
margin-top:4px;
">

${j.지역명 || "-"} ·
데뷔 ${j.데뷔일자 || "-"}

</div>

</div>

</div>

<div style="
display:grid;
grid-template-columns:1fr 1fr;
gap:12px;
">

<div class="card">
<b>기승가능중량</b>
<div>${j.기승가능중량 || "-"}</div>
</div>

<div class="card">
<b>통산전적</b>
<div>${j.통산전적 || "-"}</div>
</div>

<div class="card">
<b>통산승률</b>
<div>${j.통산승률 || "-"}</div>
</div>

<div class="card">
<b>최근1년승률</b>
<div>${j.최근1년승률 || "-"}</div>
</div>

<div class="card">
<b>통산복승률</b>
<div>${j.통산복승률 || "-"}</div>
</div>

<div class="card">
<b>최근1년복승률</b>
<div>${j.최근1년복승률 || "-"}</div>
</div>

<div class="card">
<b>통산연승률</b>
<div>${j.통산연승률 || "-"}</div>
</div>

<div class="card">
<b>최근1년연승률</b>
<div>${j.최근1년연승률 || "-"}</div>
</div>

</div>
`;

document.querySelector(
"#horse-modal h2"
).innerText="🏇 기수 정보";

document.getElementById(
"horse-body"
).innerHTML=html;

document.getElementById(
"horse-modal"
).style.display="flex";

}

async function showTrainerInfo(
trainerName
){

const res = await fetch(
`/trainer/${encodeURIComponent(
trainerName
)}`
);

const t = await res.json();

let html=`

<div style="
display:flex;
justify-content:space-between;
align-items:center;
gap:20px;
margin-bottom:25px;
flex-wrap:wrap;
">

<div style="
display:flex;
align-items:center;
gap:15px;
">

<div style="
width:65px;
height:65px;
border-radius:50%;
background:#fee2e2;
display:flex;
align-items:center;
justify-content:center;
font-size:34px;
">

🐎

</div>

<div>

<div style="
font-size:28px;
font-weight:800;
">

${t.조교사명 || trainerName}

</div>

<div style="
color:#666;
font-size:14px;
margin-top:4px;
">

${t.지역명 || "-"}

</div>

</div>

</div>

<div style="
display:grid;
grid-template-columns:1fr 1fr;
gap:10px;
">

<div style="
display:grid;
grid-template-columns:
repeat(4,1fr);

gap:10px;

min-width:520px;
">

<button
class="trainer-tab-btn"
onclick="
showTrainerTab('${trainerName}','info')
"
>
📋 인적사항
</button>

<button
class="trainer-tab-btn"
onclick="
showTrainerTab('${trainerName}','horse')
"
>
🐎 위탁관리말
</button>

<button
class="trainer-tab-btn"
onclick="
showTrainerTab('${trainerName}','year')
"
>
📈 연도별성적
</button>

<button
class="trainer-tab-btn"
onclick="
showTrainerTab('${trainerName}','recent')
"
>
🕒 최근1개월
</button>

</div>

</div>

</div>

<div id="trainer-tab-content">

<div style="
display:grid;
grid-template-columns:1fr 1fr;
gap:12px;
">

<div class="card">
<b>통산전적</b>
<div>${t.통산전적 || "-"}</div>
</div>

<div class="card">
<b>통산승률</b>
<div>${t.통산승률 || "-"}</div>
</div>

<div class="card">
<b>통산복승률</b>
<div>${t.통산복승률 || "-"}</div>
</div>

<div class="card">
<b>통산연승률</b>
<div>${t.통산연승률 || "-"}</div>
</div>

<div class="card">
<b>최근1년전적</b>
<div>${t.최근1년 || "-"}</div>
</div>

<div class="card">
<b>최근1년승률</b>
<div>${t.최근1년승률 || "-"}</div>
</div>

<div class="card">
<b>최근1년복승률</b>
<div>${t.최근1년복승률 || "-"}</div>
</div>

<div class="card">
<b>최근1년연승률</b>
<div>${t.최근1년연승률 || "-"}</div>
</div>

</div>

</div>

`;

document.querySelector(
"#horse-modal h2"
).innerText="🐎 조교사 정보";

document.getElementById(
"horse-body"
).innerHTML=html;

document.getElementById(
"horse-modal"
).style.display="flex";

}

async function showTrainerTab(
trainerName,
tab
){

let url="";

if(tab==="info"){
showTrainerInfo(trainerName);
return;
}

if(tab==="horse"){
url=`/trainer-horse-name/${encodeURIComponent(trainerName)}`;
}

if(tab==="year"){
url=`/trainer-year-name/${encodeURIComponent(trainerName)}`;
}

if(tab==="recent"){
url=`/trainer-recent-name/${encodeURIComponent(trainerName)}`;
}

const res=await fetch(url);

const data=await res.json();

let html=`
<table style="
width:100%;
border-collapse:collapse;
font-size:13px;
">


`;


// =====================
// 위탁관리말
// =====================

if(tab==="horse"){

html+=`
<tr>
<th>마명</th>
<th>마주명</th>
<th>조번</th>
<th>등급</th>
<th>레이팅</th>
<th>산지</th>
<th>성별</th>
<th>연령</th>
</tr>
`;

data.forEach(r=>{

html+=`
<tr>

<td>${r.마명||"-"}</td>
<td>${r.마주명||"-"}</td>
<td>${r.조번||"-"}</td>
<td>${r.등급||"-"}</td>
<td>${r.레이팅||"-"}</td>
<td>${r.산지||"-"}</td>
<td>${r.성별||"-"}</td>
<td>${r.연령||"-"}</td>

</tr>
`;

});

}


// =====================
// 연도별성적
// =====================

if(tab==="year"){

html+=`
<tr>
<th>연도</th>
<th>출전</th>
<th>1위</th>
<th>2위</th>
<th>3위</th>
<th>승률</th>
<th>복승률</th>
<th>연승률</th>
<th>순위상금</th>
</tr>
`;

data.forEach(r=>{

html+=`
<tr>

<td>${r.연도||"-"}</td>
<td>${r.출전||"-"}</td>
<td>${r.일위||"-"}</td>
<td>${r.이위||"-"}</td>
<td>${r.삼위||"-"}</td>
<td>${r.승률||"-"}</td>
<td>${r.복승률||"-"}</td>
<td>${r.연승률||"-"}</td>
<td>${r.순위상금||"-"}</td>

</tr>
`;

});

}


// =====================
// 최근1개월
// =====================

if(tab==="recent"){

html+=`
<tr>
<th>날짜</th>
<th>마번</th>
<th>마명</th>
<th>기수명</th>
<th>등급</th>
<th>순위</th>
<th>중량</th>
<th>거리</th>
<th>기록</th>
<th>도착차</th>
<th>마체중</th>
</tr>
`;

data.forEach(r=>{

html+=`
<tr>

<td>${r.경주일자||"-"}</td>
<td>${r.마번||"-"}</td>
<td>${r.마명||"-"}</td>
<td>${r.기수명||"-"}</td>
<td>${r.등급||"-"}</td>
<td>${r.순위||"-"}</td>
<td>${r.중량||"-"}</td>
<td>${r.거리||"-"}</td>
<td>${r.기록||"-"}</td>
<td>${r.도착차||"-"}</td>
<td>${r.마체중||"-"}</td>

</tr>
`;

});

}

html+="</table>";

document.getElementById(
"trainer-tab-content"
).innerHTML=html;

}

function goPointLog(){

    location.href =
    "point.html";

}

function logout(){

    localStorage.clear();

    location.href = "/";

}

function goHome(){

    location.href = "/";

}

function goCharge(){

    location.href =
    "charge.html";

}

function closeHorseModal(){

    document.getElementById(
        "horse-modal"
    ).style.display = "none";

}

async function showHorseInfo(horseName){

const res = await fetch(
`/horse/${encodeURIComponent(horseName)}`
);

const data = await res.json();

let html=`

<div class="card">

<h2>
🏇 ${data.마명 || horseName}
</h2>

<table
style="
width:100%;
border-collapse:collapse;
"
>

<tr>
<th>성별</th>
<td>${data.성별 || "-"}</td>
</tr>

<tr>
<th>나이</th>
<td>${data.나이 || "-"}</td>
</tr>

<tr>
<th>조교사</th>
<td>${data.조교사 || "-"}</td>
</tr>

<tr>
<th>마주</th>
<td>${data.마주 || "-"}</td>
</tr>

<tr>
<th>부마</th>
<td>${data.부마 || "-"}</td>
</tr>

<tr>
<th>모마</th>
<td>${data.모마 || "-"}</td>
</tr>

<tr>
<th>통산전적</th>
<td>${data.통산전적 || "-"}</td>
</tr>

<tr>
<th>승률</th>
<td>${data.승률 || "-"}</td>
</tr>

<tr>
<th>수득상금</th>
<td>${data.수득상금 || "-"}</td>
</tr>

<tr>
<th>생년월일</th>
<td>${data.생년월일 || "-"}</td>
</tr>

<tr>
<th>산지</th>
<td>${data.산지 || "-"}</td>
</tr>

</table>

</div>
`;

document.querySelector(
"#horse-modal h2"
).innerText="🏇 경주마 정보";

document.getElementById(
"horse-body"
).innerHTML=html;

document.getElementById(
"horse-modal"
).style.display="flex";

}

function getGroupComment(grade){

switch(grade){

case "S":
return `
가장 높은 평가를 받은 최상위 전력입니다.<br>
우승 후보로 가장 유력합니다.
`;

case "A+":
return `
입상 가능성이 매우 높습니다.<br>
우승 경쟁이 충분한 전력입니다.
`;

case "A":
return `
상위권 경쟁력이 있습니다.<br>
입상권 후보입니다.
`;

case "B+":
return `
상위권과 중위권의 경계입니다.<br>
전개에 따라 충분히 입상이 가능합니다.
`;

case "B":
return `
중위권 이상의 경쟁력을 갖추고 있습니다.<br>
복병으로 관심을 가져볼 만합니다.
`;

case "C+":
return `
변수 요소가 있는 전력입니다.<br>
경주 흐름에 따라 기대 이상의 결과도 가능합니다.
`;

case "C":
return `
객관적인 전력은 다소 부족합니다.<br>
관망 전략이 적절합니다.
`;

case "D":
case "D+":
return `
입상 가능성은 높지 않습니다.<br>
이변이 필요합니다.
`;

default:
return `
현실적으로 쉽지 않은 경주입니다.
`;

}

}

function scrollToTop(){

window.scrollTo({

top:0,

behavior:"smooth"

});

}

function toggleFloatingMenu(){

document
.getElementById(
"floatingList"
)
.classList.toggle(
"show"
);

}

function goSection(id){

document
.getElementById(id)
.scrollIntoView({

behavior:"smooth"

});

toggleFloatingMenu();

}

function scrollTopSmooth(){

    document
        .getElementById("floatingList")
        .classList.remove("show");

    window.scrollTo({

        top:0,

        behavior:"smooth"

    });

}