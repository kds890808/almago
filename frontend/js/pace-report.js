let currentTrack = null;
let currentData = null;
let originalData = null;

function sleep(ms){

return new Promise(
resolve =>
setTimeout(resolve, ms)
);

}

async function loadUserInfo(){

    const token =
    localStorage.getItem("token");

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
    `💰 ${Number(user.point).toLocaleString()}P`;

}

async function loadAI(
    region,
    raceNo
) {

    const feeRes =
    await fetch(
    "/fee-settings"
    );

    const feeData =
    await feeRes.json();

    paceFee =
    feeData.find(
    x=>x.item==="pace"
    )?.point || 1000;

    finalFee =
    feeData.find(
    x=>x.item==="total"
    )?.point || 1500;

  const token = localStorage.getItem("token");

  if (!token) {
    alert("로그인 필요");
    return;
  }

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

  const top5 = [...data]
    .sort((a, b) => Number(b.점수) - Number(a.점수))
    .slice(0, 5);

    const darkHorse =
        [...data]
        .filter(h => !top5.some(t => t.번호 == h.번호))
        .sort((a, b) => Number(b.점수) - Number(a.점수))[0];

// =========================
// 실제 금일/예정 경주 기준 연동
// =========================
const raceRes = await fetch("/race");

const raceData = await raceRes.json();

const realRaces =
raceData
.filter(r =>
    r.지역 === region
)
.map(r => ({

    region : r.지역,

    raceNo : String(r.경주),

    date : String(r.경주일자)
        .replace(/\(.*?\)/g,"")
        .trim()

}));


console.log("AI DATA =", data);
console.log("RACE DATA =", raceData);
console.log("첫번째 AI =", data[0]);

// 선택한 지역 + 경주만 출력

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

    // 문자열 → 배열 변환
    const star = r.star || "-";
    const square = r.square || "-";
    const empty = r.empty || "-";
    const up = r.up || "-";
    const triangle = r.triangle || "-";
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

// =========================
// 전개분석 화면 생성
// =========================

area.innerHTML = `

<div class="analysis-box">

<h3 class="section-title"> 1. AI 전개요약</h3>
<div id="pace-summary-section">

<div id="pace-summary">
    
    분석중...</div>

</div>

<div class="pace-type-notice">
    ※ 주행유형은 최근 전개 데이터를 기준으로 분석합니다.<br>
    데이터가 부족하거나 뚜렷한 특성이 없는 경우
    ‘보통형’으로 표시될 수 있습니다.
</div>

</div>

<hr>

<div class="analysis-box">

<h3 class="section-title">2. 경주로 시각화</h3>
<div id="race-svg-section">

<div id="race-svg">
    
    분석중...</div>

</div>


</div>

<hr>

<div class="analysis-box">

<h3 class="section-title">3. 전개 유불리 순위</h3>
<div id="pace-ranking-section">

<div id="pace-ranking">
    
    분석중...</div>

</div>

</div>

<hr>

<div class="analysis-box">

<h3 class="section-title">4. 전개분석 상세표</h3>
<div id="pace-detail-section">

<div id="pace-detail">
    
    분석중...</div>

</div>

</div>

<hr>

<div class="analysis-box">

<h3 class="section-title">5. AI 코멘트</h3>
<div id="pace-final-section">

<div id="pace-final">
    
    분석중...</div>

</div>

</div>

`;

await loadPaceAnalysis(
    r.지역,
    r.경주,
    raceDate
);

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

async function unlockPace(
region,
raceNo,
raceDate
){

    const ok =
    await showModal(

        "전개분석",

        `확인 버튼을 누르면
        ${paceFee}P가 차감됩니다.`,

        "🏇",

        true

    );

    if(!ok){
        return;
    }

    const token =
    localStorage.getItem(
        "token"
    );

    const res =
    await fetch(
        "/use-pace-analysis",
        {
            method:"POST",
            headers:{
                "Authorization":
                `Bearer ${token}`
            }
        }
    );

    const data =
    await res.json();

    if(!res.ok){

        await showModal(

            "전개분석",

            data.detail ||
            "포인트 부족",

            "❌",

            false

        );

        return;
    }

        await showModal(

            "전개분석",

            `${data.use_point}P 차감 완료

            <div style="

            margin:15px 0 20px 0;

            padding:14px;

            background:linear-gradient(
            135deg,
            #eff6ff,
            #dbeafe
            );

            border-radius:14px;

            font-weight:800;
            font-size:17px;

            color:#1e40af;

            border-left:6px solid #2563eb;

            ">

            🏇 AI가 각 경주마의 주행습성을 바탕으로 이번 경주의 경주전개를 예상합니다. 

            </div>

            남은 포인트 :
            ${data.remain_point}P`,

            "🏇",

            false

        );

    const area =
    document.getElementById(
    `pace-analysis-${region}-${raceNo}`
    );

    if(!area){

        await showModal(

            "전개분석",

            "전개분석 영역을 찾을 수 없습니다.",

            "❌",

            false

        );

        return;

    }

    area.style.display = "block";

    area.innerHTML = `

<h2>🏇 AI 전개분석</h2>

<div class="analysis-box">

<h3>① AI 전개요약(후천적주행습성)</h3>

<div id="pace-summary">
분석중...
</div>

</div>

<hr>

<div class="analysis-box">

<h3>② 경주로 시각화</h3>

<br>

<div
id="race-svg"
style="
position:relative;
"
>
분석중...
</div>

</div>

<hr>

<div class="analysis-box">

<h3>③ 전개 유불리 순위</h3>

<div id="pace-ranking">
분석중...
</div>

</div>

<hr>

<div class="analysis-box">

<h3>④ 전개분석 상세표</h3>

<div id="pace-detail">
불러오는 중...
</div>

</div>

<hr>

<div class="analysis-box">

<h3>⑤ AI 최종 결론</h3>

<div id="pace-final">
분석중...
</div>

</div>

`;

    await loadPaceAnalysis(
        region,
        raceNo,
        raceDate
    );

}

async function unlockFinal(
    region,
    raceNo,
    raceDate
){

    const ok =
    await showModal(

        "종합분석",

        `확인 버튼을 누르면
        ${finalFee}P가 차감됩니다.`,

        "🏆",

        true

    );

    if(!ok){
        return;
    }

    const token =
    localStorage.getItem(
        "token"
    );

    const res =
    await fetch(
        "/use-final-analysis",
        {
            method:"POST",
            headers:{
                "Authorization":
                `Bearer ${token}`
            }
        }
    );

    const data =
    await res.json();

    if(!res.ok){

    await showModal(

        "종합분석",

        data.detail ||
        "포인트 부족",

        "❌",

        false

    );

        return;
    }

    await showModal(

        "종합분석",

        `${data.use_point}P 차감 완료

        <div style="

        margin:15px 0 20px 0;

        padding:14px;

        background:linear-gradient(
        135deg,
        #fff7ed,
        #ffedd5
        );

        border-radius:14px;

        font-weight:800;
        font-size:17px;

        color:#c2410c;

        border-left:6px solid #f97316;

        ">

        🏆 AI가 기본분석 · 혈통분석 ·
        전개분석을 통합 분석합니다.

        </div>

        남은 포인트 :
        ${data.remain_point}P`,

        "🏆",

        false

    );

    window.location.href =
    `/final-loading.html?region=${region}&raceNo=${raceNo}&raceDate=${raceDate}`;
}

async function showHorseInfo(horseName){

    const res = await fetch(
        `/horse/${encodeURIComponent(horseName)}`
    );

    const data = await res.json();

    let html = `

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

function closeHorseModal(){

document.getElementById(
"horse-modal"
).style.display="none";

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

<style>
.info-pill{

display:inline-block;

padding:6px 12px;

border-radius:999px;

background:#f1f5f9;

color:#0f172a;

font-weight:700;

text-decoration:none;

border:1px solid #cbd5e1;

transition:.2s;

}

.info-pill:hover{

background:#dbeafe;

border-color:#60a5fa;

}

    
th,td{
border:1px solid #ddd;
padding:8px;
text-align:center;
white-space:nowrap;
}

th{
background:#f5f7ff;
}

.info-pill{

display:inline-block;
padding:5px 10px;
border-radius:20px;
background:#eef2ff;
color:#1e40af;
font-weight:600;
cursor:pointer;
text-decoration:none;

}

.info-pill:hover{

background:#c7d2fe;

}

.analysis-card{

    background:white;
    border-radius:12px;
    padding:15px;
    margin-bottom:15px;

    box-shadow:
    0 2px 8px rgba(0,0,0,.08);

    border-left:
    5px solid #2563eb;

}

.analysis-header{

    display:flex;
    justify-content:space-between;
    align-items:center;

    margin-bottom:10px;

}

.analysis-horse{

    font-size:20px;
    font-weight:bold;

}

.analysis-score{

    background:#2563eb;
    color:white;

    padding:6px 12px;

    border-radius:20px;
    font-weight:bold;

}

.analysis-comment{

    line-height:1.7;
    color:#333;

}


.analysis-comment-card h4{

margin:0 0 10px 0;

color:#1e3a8a;

}


.rank-badge{

padding:4px 10px;

border-radius:20px;

font-size:12px;

font-weight:bold;

display:inline-block;

}

.score-top{
background:#fef3c7;
font-weight:bold;
color:#92400e;
}

.score-good{
background:#dbeafe;
font-weight:bold;
color:#1d4ed8;
}

.score-mid{
background:#dcfce7;
color:#166534;
}

.score-low{
background:#f3f4f6;
color:#6b7280;
}

.rank-badge{

padding:4px 10px;
border-radius:20px;
font-size:12px;
font-weight:bold;
display:inline-block;

}

.pace-map{

background:white;

padding:20px;

border-radius:15px;

box-shadow:
0 2px 10px rgba(0,0,0,.08);

}

.pace-lane{

padding:15px;

margin-bottom:10px;

border-radius:10px;

}

.pace-lead{
background:#ffe5e5;
}

.pace-middle{
background:#fff3d8;
}

.pace-normal{
background:#f2f2f2;
}

.pace-chase{
background:#e6f0ff;
}

.horse-chip{

display:inline-block;

margin:5px;

padding:8px 12px;

border-radius:20px;

background:white;

font-weight:bold;

}

.locked-box{

    min-height:180px;

    display:flex;
    flex-direction:column;

    justify-content:center;
    align-items:center;

    text-align:center;

}

.analysis-comment{

    margin:25px 0;

    padding:18px;

    background:#dbeafe;

    border-left:6px solid #2563eb;

    border-radius:16px;

    color:#1e40af;

    font-weight:700;

    line-height:1.8;

}

</style>
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

function makeReason(h){

    let html = "";

    if(Number(h.점수) >= 95){
        html += "🔥 최상급 전개<br>";
    }else if(Number(h.점수) >= 90){
        html += "⚡ 유리한 전개<br>";
    }else{
        html += "🏇 안정적인 전개<br>";
    }

    if(h.주행유형){
        html += `📍 ${h.주행유형}<br>`;
    }

    if(h.점수){
        html += `📊 전개점수 ${h.점수}`;
    }

    return html;
}

async function loadPaceAnalysis(
region,
raceNo,
raceDate
){


const res =
await fetch(
`/pace-analysis-data/${region}/${raceNo}/${raceDate}`
);

const data = await res.json();

const top5 = [...data]
    .sort((a,b)=>Number(b.점수)-Number(a.점수))
    .slice(0,5);

// 기본분석 데이터
const basicRes =
    await fetch(
        `/basic-analysis-data/${region}/${raceNo}/${raceDate}`
    );

const basicData =
    await basicRes.json();


// 혈통분석 데이터
const bloodRes =
    await fetch(
        `/blood-analysis-data/${region}/${raceNo}/${raceDate}`
    );

const bloodData =
    await bloodRes.json();


// ★ 이것만 추가
console.log("basicData[0] =", basicData[0]);
console.log("bloodData[0] =", bloodData[0]);


// =========================
// 능력점수 목록 생성
// =========================

const abilityList =

    basicData.map(b=>{

        const blood =
            bloodData.find(
                x=>x.번호 == b.번호
            );

        const abilityScore = Math.round(

            Number(b.점수 || 0) * 0.7 +

            Number(blood?.점수 || 0) * 0.3

        );

        return{

            번호 : b.번호,
            마명 : b.마명,
            점수 : abilityScore

        };

    });

    
    console.log("basicData 첫말:", basicData[0]);
    console.log("bloodData 첫말:", bloodData[0]);
    console.log("abilityList:", abilityList);
    console.table(abilityList);

// =========================
// 번호별 능력점수 저장
// =========================

const abilityMap = {};

abilityList.forEach(h=>{

    abilityMap[h.번호] = h.점수;

});


// =========================
// 능력마 선정
// =========================

const abilityHorse =

    abilityList

    .filter(h=>

        !top5.some(
            t=>t.번호 == h.번호
        )

    )

    .sort(
        (a,b)=>b.점수-a.점수
    )[0];

const top5Html = `

<div id="top5" class="top5-area">

<h3>🏆 AI 추천 TOP5(+능력마)</h3>

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

${abilityHorse ? `

<div class="top5-card darkhorse-card">

    <div class="top5-rank">
        🐎
    </div>

    <div class="top5-name">
        ${abilityHorse.번호}
        ${abilityHorse.마명}
    </div>

    <div class="top5-score">
        ${abilityHorse.점수}점
    </div>

    <div class="top5-reason">
        💎 숨은 능력마
    </div>

</div>

` : ""}
</div>

</div>

`;

console.log(
"TRACK_DATA=",
TRACK_DATA
);

console.log(
"전개 데이터",
data
);

console.log(
"첫번째 말",
data[0]
);
    // =====================
    // 주행유형 카운트
    // =====================

    let lead = 0;
    let middle = 0;
    let chase = 0;
    let normal = 0;

    data.forEach(r=>{

        if(r.주행유형 === "선행"){
            lead++;
        }

        else if(r.주행유형 === "선입"){
            middle++;
        }

        else if(r.주행유형 === "추입"){
            chase++;
        }

        else{
            normal++;
        }

    });

    // =====================
    // 말 표시 함수
    // =====================

    function horseChip(h){

    let icon="";

    if(h.주행유형==="선행")
    icon="🥇";

    else if(h.주행유형==="선입")
    icon="🥈";

    else if(h.주행유형==="추입")
    icon="🔥";

    return `

    <span class="track-horse">

    ${icon}
    ${h.번호}

    </span>

    `;

    }

    // =====================
    // 출발 게이트 순서
    // =====================

    const gateOrder =
    [...data]
    .sort(
    (a,b)=>
    Number(b.번호) -
    Number(a.번호)
    );

    // ====================
    // AI 전개요약 생성
    // ====================

    let summary = "";

    if(lead >= 4){

        summary =
        "선행형 마필이 다수 포진하여 초반 페이스가 빠르게 전개될 가능성이 높습니다.";

    }
    else if(lead >= 2){

        summary =
        "일부 선행마가 존재하나 과도한 선행 경쟁은 예상되지 않습니다.";

    }
    else{

        summary =
        "선행마가 부족하여 비교적 차분한 전개가 예상됩니다.";

    }

    if(chase >= 5){

        summary +=
        "<br><br>추입형 마필이 다수 포진하여 종반 역전 가능성이 높은 경주입니다.";

    }

    document.getElementById("analysis-area")
    .insertAdjacentHTML(
        "afterbegin",
        top5Html
    );

    document.getElementById("pace-summary").innerHTML = `

    <div class="pace-summary-box">

    <div class="pace-card lead">

    🐎

    <br><br>

    선행형

    <br>

    ${lead}두

    </div>

    <div class="pace-card middle">

    🚩

    <br><br>

    선입형

    <br>

    ${middle}두

    </div>

    <div class="pace-card chase">

    ⚡

    <br><br>

    추입형

    <br>

    ${chase}두

    </div>

    <div class="pace-card normal">

    🏇

    <br><br>

    보통형

    <br>

    ${normal}두

    </div>

    </div>

    <br>

    <div class="pace-ai-box">

    <h4>
    📌 AI 전개 해석
    </h4>

    ${summary}

    </div>

    `;

    const leadHorses =
    data.filter(
    r=>r.주행유형==="선행"
    );

    const middleHorses =
    data.filter(
    r=>r.주행유형==="선입"
    );

    const chaseHorses =
    data.filter(
    r=>r.주행유형==="추입"
    );

    const normalHorses =
    data.filter(
    r=>

    r.주행유형!=="선행" &&
    r.주행유형!=="선입" &&
    r.주행유형!=="추입"

    );


    const middleAll =
    getMiddleAll(data);

    const distance =
    parseInt(
    data[0].거리
    );

    const key =
    `${region}-${distance}`;

    const track =
    TRACK_DATA[key];
    if(!track){
    currentTrack = track;
    originalData = data;

    [...data];

    currentData =
    [...data].sort(
    (a,b)=>
    Number(a.번호) -
    Number(b.번호)
    );    

    console.log(
    "좌표 데이터 없음:",
    key
    );

    return;
    }

    let currentPoint =
    track.start;

    currentTrack = track;

    originalData =
    [...data];

    currentData =
    [...data].sort(
    (a,b)=>
    Number(a.번호) -
    Number(b.번호)
    );

    const startOrder =
    [...data].sort(
    (a,b)=>
    Number(a.번호) -
    Number(b.번호)
    );

    const horseCount =
    startOrder.length;

    const lanePositions = [];

    for(

    let i=0;
    i<horseCount;
    i++

    ){

    const ratio =

    (horseCount===1)

    ? 0

    : i/(horseCount-1);

    const safeMargin = 0.12;

    const adjustedRatio =

    safeMargin +

    (
    ratio *
    (1 - safeMargin*2)
    );
    const x =
    track.start.innerX +
    (
    track.start.outerX -
    track.start.innerX
    )
    *
    adjustedRatio;

    const y =
    track.start.innerY +
    (
    track.start.outerY -
    track.start.innerY
    )
    *
    adjustedRatio;

    lanePositions.push({
    x,
    y
    });

    }

    console.log(
    "KEY=",
    key
    );

    console.log(
    "TRACK=",
    track
    );

    console.log(
    "lanePositions=",
    lanePositions
    );



    const svgPoints =
    startOrder.map((h,i)=>{

    const pos =
    lanePositions[i];

    const x = pos.x;
    const y = pos.y;

    let icon = "🐴";

    let badge = "";

    if(i===0){

    badge = "🥇";

    }
    else if(i===1){

    badge = "🥈";

    }
    else if(i===2){

    badge = "🥉";

    }
    else if(i===4){

    badge = "🔥";

    }

    if(h.주행유형==="선행"){
    icon="🔴🏇";
    }
    else if(h.주행유형==="선입"){
    icon="🟡🐎";
    }
    else if(h.주행유형==="중위"){
    icon="🟢🐴";
    }
    else if(h.주행유형==="추입"){
    icon="🔵🦄";
    }
    else{
    icon="⚪🐴";
    }

    icon =
    badge + icon;

    return `

    <g
    id="horse-${h.번호}"
    transform="translate(${x},${y})"
    style="
    transition:
    transform 3.5s cubic-bezier(
    0.18,
    0.95,
    0.28,
    1
    );
    "
    >

    <text
    x="0"
    y="0"
    font-size="18"
    text-anchor="end"
    dominant-baseline="middle"
    >
    ${icon}
    </text>

    <text
    x="8"
    y="4"
    font-size="11"
    font-weight="bold"
    text-anchor="middle"
    fill="black"
    >
    ${h.번호}
    </text>

    </g>

    `;

    }).join("");

    const lateAll =
    getLateAll(data);

    /*
    document.getElementById(
    "pace-map"
    ).innerHTML = `

    <div class="track-board">

    <div class="track-start">
    START
    </div>

    <div class="track-line"></div>

    <div class="track-area">

    <div class="track-row">
    ${leadHorses.map(h=>horseChip(h)).join("")}
    </div>

    <div class="track-row">
    ${middleHorses.map(h=>horseChip(h)).join("")}
    </div>

    <div class="track-row">
    ${normalHorses.map(h=>horseChip(h)).join("")}
    </div>

    <div class="track-row">
    ${chaseHorses.map(h=>horseChip(h)).join("")}
    </div>

    </div>

    <div class="track-line"></div>

    <div class="track-goal">
    GOAL
    </div>

    </div>

    `;
    */
    
    const cornerPos = [

    {left:60, top:18},

    {left:57, top:26},
    {left:63, top:26},

    {left:54, top:34},
    {left:60, top:34},
    {left:66, top:34},

    {left:51, top:42},
    {left:57, top:42},
    {left:63, top:42},
    {left:69, top:42},
    {left:75, top:42}

    ];

    const finishPos = [

    {left:82, top:70}, // 1위

    {left:76, top:70},
    {left:70, top:70},

    {left:84, top:82},
    {left:78, top:82},
    {left:72, top:82},

    {left:88, top:94},
    {left:82, top:94},
    {left:76, top:94},
    {left:70, top:94},

    {left:64, top:94}

    ];

    const finish1 =
    lateAll.slice(0,1);

    const finish2 =
    lateAll.slice(1,3);

    const finish3 =
    lateAll.slice(3,6);

    const finish4 =
    lateAll.slice(6);

    /*
    document.getElementById(
    "finish-map"
    ).innerHTML = `

    <div class="race-track-wrap">

    <img
    src="/static/seoul-track.png"
    class="race-track-img"
    >

    ${lateAll.map((h,i)=>`

    <div
    class="track-point"
    style="
    left:${finishPos[i]?.left || 50}%;
    top:${finishPos[i]?.top || 50}%;
    "
    >

    ${h.번호}

    </div>

    `).join("")}

    `;
    */

    /*
    document.getElementById(
    "corner-map"
    ).innerHTML = `

    <div class="race-track-wrap">

    <img
    src="/static/seoul-track.png"
    class="race-track-img"
    >

    ${middleAll.map((h,i)=>`

    <div
    class="track-point"
    style="
    left:${cornerPos[i]?.left || 50}%;
    top:${cornerPos[i]?.top || 50}%;
    "
    >

    ${h.번호}

    </div>

    `).join("")}

    </div>

    `;
    */

    console.log(
    "전개 데이터",
    data
    );

    if(!data || data.length === 0){

        document.getElementById(
        "pace-summary"
        ).innerHTML =
        "전개 데이터가 없습니다.";

        return;
    }

    console.log(
    "전개 데이터",
    data
    );

    if(
        !data ||
        data.length === 0
    ){

        console.log(
            "전개 데이터 없음"
        );

        document.getElementById(
            "pace-summary"
        ).innerHTML =
        "전개 데이터가 없습니다.";

        return;
    }


    if(region === "부산"){

        startPos = {

            1000:{x:120,y:90},

            1200:{x:360,y:120},
            1300:{x:460,y:120},
            1400:{x:560,y:120},

            1500:{x:650,y:120},
            1600:{x:730,y:120},

            1800:{x:250,y:380},
            1900:{x:350,y:380},
            2000:{x:450,y:380},

            2200:{x:600,y:420}

        };

    }

    else{

        startPos = {

            1000:{x:120,y:250},
            1200:{x:180,y:250},
            1300:{x:230,y:250},
            1400:{x:280,y:250},

            1600:{x:380,y:250},
            1800:{x:500,y:250},
            2000:{x:600,y:250}

        };

    }

    const start =
    startPos[distance] ||
    {x:120,y:250};


    const startPoints =
    data.map((h,i)=>`

    <circle
    cx="${start.x}"
    cy="${start.y + (i*28)}"
    r="7"
    fill="#4da3df"
    />

    <text
    x="${start.x}"
    y="${start.y + (i*28) + 5}"
    font-size="7"
    text-anchor="middle"
    fill="white"
    >
    ${h.번호}
    </text>

    `).join("");    

    const startTextX =
    (
    currentTrack.start.innerX +
    currentTrack.start.outerX
    ) / 2;

    const startTextY =
    currentTrack.start.outerY - 20;
    
    document.getElementById(
    "race-svg"
    ).innerHTML = `

    <div style="margin-bottom:10px;">

    <button
    class="track-btn"
    onclick="moveStep('start')"
    >
    🏁 출발
    </button>

    <button
    class="track-btn"
    onclick="moveStep('step1')"
    >
    ① 진행1
    </button>

    <button
    class="track-btn"
    onclick="moveStep('step2')"
    >
    ② 진행2
    </button>

    <button
    class="track-btn"
    onclick="moveStep('step3')"
    >
    ③ 진행3
    </button>

    <button
    class="track-btn"
    onclick="moveStep('step4')"
    >
    🏆 진행4
    </button>

    <button
    class="track-btn"
    disabled
    style="opacity:0.55; cursor:not-allowed;"
    >
    ▶ 자동재생 <small>(준비중)</small>
    </button>

    </div>    

    <svg
    width="100%"
    viewBox="0 0 1000 1000"
    style="display:block; overflow:visible;"
    >display:block;"
    >

    <!-- 경주로 -->

    <!-- 외곽 트랙 -->

    <rect
    x="80"
    y="40"
    width="900"
    height="900"
    rx="250"
    fill="#d8c9a3"
    />

    <!-- 내곽 잔디 -->

    <rect
    x="220"
    y="200"
    width="620"
    height="500"
    rx="120"
    fill="#b9e28c"
    />

    <!-- 트랙 경계 -->

    <rect
    x="150"
    y="100"
    width="760"
    height="760"
    rx="180"
    fill="none"
    stroke="#ffffff"
    stroke-width="4"
    />

    <!-- 결승선 -->

    <line
    x1="686"
    y1="705"
    x2="686"
    y2="934"
    stroke="red"
    stroke-width="5"
    />

    <!-- 출발선 -->
    <line
    x1="${currentTrack.start.innerX}"
    y1="${currentTrack.start.innerY}"
    x2="${currentTrack.start.outerX}"
    y2="${currentTrack.start.outerY}"
    stroke="red"
    stroke-width="5"
    />

    <!-- START -->
    <text
    x="${startTextX}"
    y="${startTextY}"
    font-size="28"
    font-weight="bold"
    fill="red"
    text-anchor="middle"
    >
    START
    </text>

    <!-- START -->

    <text
    x="${startTextX}"
    y="${startTextY}"
    font-size="28"
    font-weight="bold"
    fill="red"
    text-anchor="middle"
    >
    START
    </text>


    <!-- 중간글자 -->    
    <text
    x="532"
    y="410"
    font-size="40"
    font-weight="bold"
    fill="#666"
    text-anchor="middle"
    >
    🏇 ${region} ${raceNo}경주
    </text>

    <text
    x="532"
    y="470"
    font-size="50"
    font-weight="900"
    fill="white"
    stroke="#2563eb"
    stroke-width="2"
    paint-order="stroke"
    text-anchor="middle"
    >
    ${distance}m
    </text>

    <!-- GOAL -->

    <text
    x="634"
    y="693"
    font-size="28"
    font-weight="bold"
    fill="red"
    >
    GOAL
    </text>

    <!-- 코너 표시 -->

    <text
    x="251"
    y="237"
    font-size="34"
    font-weight="900"
    fill="white"
    stroke="#2563eb"
    stroke-width="3"
    paint-order="stroke"
    text-anchor="middle"
    >
    1C
    </text>

    <text
    x="251"
    y="680"
    font-size="34"
    font-weight="900"
    fill="white"
    stroke="#2563eb"
    stroke-width="3"
    paint-order="stroke"
    text-anchor="middle"
    >
    2C
    </text>

    <text
    x="806"
    y="680"
    font-size="34"
    font-weight="900"
    fill="white"
    stroke="#2563eb"
    stroke-width="3"
    paint-order="stroke"
    text-anchor="middle"
    >
    3C
    </text>

    <text
    x="806"
    y="237"
    font-size="34"
    font-weight="900"
    fill="white"
    stroke="#2563eb"
    stroke-width="3"
    paint-order="stroke"
    text-anchor="middle"
    >
    4C
    </text>

    <g id="horse-layer">
    ${svgPoints}
    </g>

    </svg>

    <div class="legend-mini">

    <table>

    <tr>
    <th>주행유형</th>
    <th>순위표시</th>
    <th>경주로</th>
    </tr>

    <tr>
    <td>🔴 선행</td>
    <td>🥇 예상1위</td>
    <td>START</td>
    </tr>

    <tr>
    <td>🟡 선입</td>
    <td>🥈 예상2위</td>
    <td>GOAL</td>
    </tr>

    <tr>
    <td>🟢 중위</td>
    <td>🥉 예상3위</td>
    <td>1C~4C</td>
    </tr>

    <tr>
    <td>🔵 추입</td>
    <td>🔥 복병마</td>
    <td>-</td>
    </tr>

    </table>

    </div>

    `;

    const svg =
    document.querySelector(
    "#race-svg svg"
    );

    svg.addEventListener(
    "click",
    (e)=>{

        const pt =
        svg.createSVGPoint();

        pt.x = e.clientX;
        pt.y = e.clientY;

        const p =
        pt.matrixTransform(
            svg.getScreenCTM().inverse()
        );

        console.log(
            "SVG X=",
            Math.round(p.x),
            "SVG Y=",
            Math.round(p.y)
        );

    });

    // ③ 랭킹

    const rank =
    [...data]
    .sort(
        (a,b)=>
        b.점수-a.점수
    )
    .slice(0,5);

    document.getElementById(
        "pace-ranking"
    ).innerHTML =

    rank.map((r,i)=>{

    let medal = "🏅";

    if(i===0) medal="🥇";
    if(i===1) medal="🥈";
    if(i===2) medal="🥉";

    return `

    <div class="pace-rank-card">

    <div class="pace-rank-left">

    <div>

    ${medal}
    ${r.번호}번 ${r.마명}

    </div>

    <div class="pace-rank-sub">

    ${makePaceReason(r)}

    </div>

    </div>

    <div class="pace-rank-score">

    ${r.점수}점

    </div>

    </div>

    `;

    }).join("");

    // ④ 상세표

document.getElementById(
"pace-detail"
).innerHTML =

data.map(row=>{

const isFirstChallenge =
    row.최근순위 === "-" ||
    !row.최근순위;

return `

<div class="horse-card">

<div class="horse-header">

🏇 ${row.번호}번
${row.마명}

<span class="horse-score">

${isFirstChallenge
    ? `${abilityMap[row.번호] ?? "-"}점`
    : `${row.점수}점`
}

</span>

</div>

<div class="horse-status-grid">

<div class="status-item">

<div class="status-title">

🏃 주행유형

</div>

<div class="status-value">

${row.주행유형}

</div>

</div>

<div class="status-item">

<div class="status-title">

📈 최근흐름

</div>

<div class="status-value">

${row.최근흐름}

</div>

</div>

<div class="status-item">

<div class="status-title">

🛣 코스적합

</div>

<div class="status-value">

${row.코스적합}

</div>

</div>

</div>

<div class="horse-data-grid">

<div class="data-box">

<div class="data-title">
📊 최근순위
</div>

<div class="data-value">
${
isFirstChallenge
? "기록없음(첫도전)"
: (!row.최근순위 || row.최근순위 === "null")
    ? "-"
    : row.최근순위
}
</div>

</div>

<div class="data-box">

<div class="data-title">
📏 도착차
</div>

<div class="data-value">
${
isFirstChallenge
? "기록없음(첫도전)"
: (!row.도착차 || row.도착차 === "null")
    ? "-"
    : row.도착차
}
</div>

</div>

<div class="data-box">

<div class="data-title">
🚀 평균G3F
</div>

<div class="data-value">
${
isFirstChallenge
? "기록없음(첫도전)"
: (!row.평균G3F || row.평균G3F === "null")
    ? "-"
    : row.평균G3F
}
</div>

<div class="data-rank">
${
isFirstChallenge
? ""
: getTopPercent(data, row, "평균G3F")
}
</div>

</div>

<div class="data-box">

<div class="data-title">
⚡ 최고G3F
</div>

<div class="data-value">
${
isFirstChallenge
? "기록없음(첫도전)"
: (!row.최고G3F || row.최고G3F === "null")
    ? "-"
    : row.최고G3F
}
</div>

<div class="data-rank">
${
isFirstChallenge
? ""
: getTopPercent(data, row, "최고G3F")
}
</div>

</div>

<div class="data-box">

<div class="data-title">
💪 평균훈련량
</div>

<div class="data-value">
${
isFirstChallenge
? "기록없음(첫도전)"
: (!row.평균훈련량 || row.평균훈련량 === "null")
    ? "-"
    : row.평균훈련량
}
</div>

</div>

<div class="data-box">

<div class="data-title">
🏊 수영훈련
</div>

<div class="data-value">
${
isFirstChallenge
? "기록없음(첫도전)"
: (!row.수영훈련 || row.수영훈련 === "null")
    ? "-"
    : row.수영훈련
}
</div>

</div>

${isFirstChallenge ? `

<div class="ai-first-card">

    <div class="ai-first-title">
    🏇 AI 경주전개 능력지수
    </div>

    <div class="ai-first-score">
    ${abilityMap[row.번호]}점
    </div>

    <div class="ai-first-desc">

    📌 거리 첫도전으로 전개 데이터가 부족하여<br>
    기본분석(70%) + 혈통분석(30%)을<br>
    반영한 AI 능력지수를 제공합니다.

    </div>

</div>

` : ""}

</div>

<div class="analysis-comment">

📝

${row.코멘트 || "코멘트 없음"}

</div>

</div>

`;
}).join("");

    // ⑤ 결론

    const top =
    rank.slice(0,3);

    const earlyTop =
    getEarlyTop3(data);

    const middleTop =
    getMiddleTop3(data);

    const lateTop =
    getLateTop3(data);

    document.getElementById(
    "pace-final"
).innerHTML = `

<div class="simulation-box">

<h3>
🏁 출발 ~ 200m
</h3>

<div id="early-phase">

분석중...

</div>

</div>

<div class="simulation-box">

<h3>
↩ 3코너 진입
</h3>

<div id="middle-phase">

분석중...

</div>

</div>

<div class="simulation-box">

<h3>
🚀 결승선 200m 전
</h3>

<div id="late-phase">

분석중...

</div>

</div>

<div class="simulation-box">

<h3>
🏆 AI 추천마
</h3>

<div id="best-horse">

분석중...

</div>

</div>

<div class="simulation-box">

<div class="simulation-box dark-horse-box">
    <h3>🎯 AI 복병마</h3>

<div id="dark-horse">

분석중...

</div>

</div>

`;

document.getElementById(
"early-phase"
).innerHTML = `

🥇 ${earlyTop[0]?.번호}번 ${earlyTop[0]?.마명}<br>
🥈 ${earlyTop[1]?.번호}번 ${earlyTop[1]?.마명}<br>
🥉 ${earlyTop[2]?.번호}번 ${earlyTop[2]?.마명}

<br><br>

초반 선두권 형성이 예상됩니다.

`;

document.getElementById(
"middle-phase"
).innerHTML = `

🥇 ${middleTop[0]?.번호}번 ${middleTop[0]?.마명}<br>
🥈 ${middleTop[1]?.번호}번 ${middleTop[1]?.마명}<br>
🥉 ${middleTop[2]?.번호}번 ${middleTop[2]?.마명}

<br><br>

3코너 구간 경쟁이 예상됩니다.

`;

document.getElementById(
"late-phase"
).innerHTML = `

🥇 ${lateTop[0]?.번호}번 ${lateTop[0]?.마명}<br>
🥈 ${lateTop[1]?.번호}번 ${lateTop[1]?.마명}<br>
🥉 ${lateTop[2]?.번호}번 ${lateTop[2]?.마명}

<br><br>

종반 가속력이 우수한 마필들입니다.

`;

document.getElementById(
"best-horse"
).innerHTML = `

🏇 ${top[0]?.번호}번
${top[0]?.마명}

<br><br>

전개상 가장 유리한 위치를
차지할 것으로 예상됩니다.

`;

document.getElementById(
"dark-horse"
).innerHTML = `

🏇 ${top[2]?.번호}번
${top[2]?.마명}

<br><br>

전개 흐름에 따라
의외의 선전 가능성이 있습니다.

`;
}

function getTopPercent(
data,
row,
key
){

const values =
data
.map(r=>Number(r[key]))
.filter(v=>!isNaN(v));

const target =
Number(row[key]);

if(
isNaN(target) ||
values.length===0
){
return "-";
}

const rank =

values
.filter(v=>v<target)
.length + 1;

const percent =

Math.round(
(rank/values.length)*100
);

return `상위 ${percent}%`;

}

function makePaceReason(row){

let reason = "";

if(row.주행유형 === "선행"){

    reason +=
    "초반 주도권 확보 가능성이 높으며 ";

}

else if(row.주행유형 === "선입"){

    reason +=
    "중위권 전개 운영이 가능하며 ";

}

else if(row.주행유형 === "추입"){

    reason +=
    "종반 추입력이 기대되며 ";

}

if(row.코스적합 === "우수"){

    reason +=
    "코스 적성이 매우 우수합니다.";

}
else if(row.코스적합 === "양호"){

    reason +=
    "코스 적성이 양호합니다.";

}
else{

    reason +=
    "전개 변수에 따라 성적이 달라질 수 있습니다.";

}

return reason;

}

function horseRankChip(h,i){

let medal="";

if(i===0) medal="🥇";
else if(i===1) medal="🥈";
else if(i===2) medal="🥉";

return `

<span
class="track-horse"
>

${medal}
${h.번호}

</span>

`;

}

function getMiddleAll(data){

return [...data]
.map(r=>{

let score = Number(r.점수 || 0);

const flow =
String(r.평균경주전개 || "");

if(flow.includes("1")) score += 20;
if(flow.includes("2")) score += 15;
if(flow.includes("3")) score += 10;

if(r.주행유형==="선행")
score += 40;

else if(r.주행유형==="선입")
score += 25;

else if(r.주행유형==="추입")
score -= 20;

return {
...r,
simScore:score
};

})
.sort((a,b)=>b.simScore-a.simScore);

}

function getLateAll(data){

return [...data]
.map(r=>{

let score = Number(r.점수 || 0);

score += 50 - Number(r.평균G3F || 50);
score += 50 - Number(r.최고G3F || 50);
score += 20 - Number(r.평균G1F || 20);

if(r.주행유형==="추입") score += 15;
if(r.주행유형==="선입") score += 8;

return {
...r,
simScore:score
};

})
.sort((a,b)=>b.simScore-a.simScore);

}

function getEarlyTop3(data){

return [...data]

.map(r=>{

let score = 0;

if(r.주행유형==="선행") score+=40;
else if(r.주행유형==="선입") score+=25;
else if(r.주행유형==="보통") score+=10;

score +=
(20 - Number(r.평균S1F || 20));

return {
...r,
simScore:score
};

})

.sort(
(a,b)=>
b.simScore-a.simScore
)

.slice(0,3);

}

function getMiddleTop3(data){

return [...data]

.map(r=>{

let score = 0;

const flow =
String(
r.평균경주전개 || ""
);

if(flow.includes("1"))
score += 30;

if(flow.includes("2"))
score += 20;

if(flow.includes("3"))
score += 10;

score +=
Number(r.점수 || 0);

return {
...r,
simScore:score
};

})

.sort(
(a,b)=>
b.simScore-a.simScore
)

.slice(0,3);

}

function getLateTop3(data){

return [...data]

.map(r=>{

let score = 0;

score +=
(50 - Number(
r.평균G3F || 50
));

score +=
(50 - Number(
r.최고G3F || 50
));

score +=
(20 - Number(
r.평균G1F || 20
));

return {
...r,
simScore:score
};

})

.sort(
(a,b)=>
b.simScore-a.simScore
)

.slice(0,3);

}

function getLanePositions(
point,
horses,
step
){

const positions=[];

for(

let i=0;
i<horses.length;
i++

){

const h =
horses[i];

const ratio =

horses.length===1

? 0.5

: i/(horses.length-1);

const seed =
i + 1;

let zigzagX = 0;
let zigzagY = 0;

if(step==="step1"){

zigzagX =
Math.sin(seed * 1.7) * 3;

zigzagY =
Math.cos(seed * 1.3) * 2;

}
else if(step==="step2"){

zigzagX =
Math.sin(seed * 1.7) * 8;

zigzagY =
Math.cos(seed * 1.3) * 5;

}
else if(step==="step3"){

zigzagX =
Math.sin(seed * 1.7) * 15;

zigzagY =
Math.cos(seed * 1.3) * 10;

}
else if(step==="step4"){

zigzagX =
Math.sin(seed * 1.7) * 30;

zigzagY =
Math.cos(seed * 1.3) * 20;

}

let spreadX = 0;
let spreadY = 0;

if(step==="step1"){

spreadX =
Math.sin(i * 2.1) * 2;

spreadY =
(i - (horses.length-1)/2)
* 1;

}
else if(step==="step2"){

spreadX =
Math.sin(i * 2.1) * 3;

spreadY =
(i - (horses.length-1)/2)
* 1.5;

}
else if(step==="step3"){

spreadX =
Math.sin(i * 2.1) * 18;

spreadY =
(i - (horses.length-1)/2)
* 8;

}
else if(step==="step4"){

spreadX =
(horses.length - i)
* 15;

spreadY =
Math.sin(i * 1.5)
* 20;

}

let styleX = 0;
let styleY = 0;

if(step !== "start"){

if(h.주행유형==="선행"){

if(step==="step1"){
styleX = 12;
}
else if(step==="step2"){
styleX = 4;
}
else if(step==="step3"){
styleX = 2;
}
else{
styleX = 8;
}

}

else if(h.주행유형==="선입"){

if(step==="step1"){
styleX = 6;
}
else if(step==="step2"){
styleX = 6;
}
else if(step==="step3"){
styleX = 5;
}
else{
styleX = 4;
}

}

if(step==="step4"){

if(h.주행유형==="선행"){
styleX += 120;
}

else if(h.주행유형==="선입"){
styleX += 60;
}

else if(h.주행유형==="중위"){
styleX += 20;
}

else if(h.주행유형==="추입"){
styleX -= 30;
}

}

}

const minX =
Math.min(
point.innerX,
point.outerX
);

const maxX =
Math.max(
point.innerX,
point.outerX
);

let x =
point.innerX +
(
point.outerX -
point.innerX
)
*
ratio
+
zigzagX
+
spreadX
+
styleX;

let y =
point.innerY +
(
point.outerY -
point.innerY
)
*
ratio
+
zigzagY
+
spreadY
+
styleY;

if(step !== "step4"){

x = Math.max(
minX + 10,
Math.min(
maxX - 10,
x
)
);

}

positions.push({

x,
y

});

}

return positions;

}


function moveStep(step){

console.log(
"step=",
step
);

console.log(
"originalData=",
originalData
);

console.log(
"currentTrack=",
currentTrack
);

if(!originalData){

console.log(
"originalData 없음"
);

return;
}

if(step==="start"){

currentData =
[...originalData].sort(
(a,b)=>
Number(a.번호) -
Number(b.번호)
);

}
else if(

step==="mid2" ||
step==="step4"

){

currentData =
getLateAll(
originalData
);

}
else{

currentData =
getMiddleAll(
originalData
);

}

const point =
currentTrack[step];

if(!point){
return;
}

const lanePositions =
getLanePositions(
point,
currentData,
step
);

currentData.forEach(

(h,i)=>{

const pos =
lanePositions[i];

const horse =
document.getElementById(
`horse-${h.번호}`
);

if(horse){

horse.setAttribute(
"transform",
`translate(${pos.x},${pos.y})`
);

}

});

}



async function playRace(){

moveStep("start");

await sleep(1000);

// ====================
// START → STEP1
// ====================

currentData =
getMiddleAll(originalData);

await animateBetween(
currentTrack.start,
currentTrack.step1,
30,
"step1"
);

moveStep("step1");

// ====================
// STEP1 → MID1
// ====================

await animateBetween(
currentTrack.step1,
currentTrack.mid1,
60,
"step1"
);


moveStep("mid1");

// ====================
// MID1 → STEP2
// ====================

await animateBetween(
currentTrack.mid1,
currentTrack.step2,
60,
"step2"
);

moveStep("step2");

// ====================
// STEP2 → STEP3
// ====================

currentData =
getMiddleAll(originalData);

await animateBetween(
currentTrack.step2,
currentTrack.step3,
60,
"step3"
);

moveStep("step3");

// ====================
// STEP3 → MID2
// ====================

currentData =
getLateAll(originalData);

await animateBetween(
currentTrack.step3,
currentTrack.mid2,
60,
"step3"
);

moveStep("mid2");

// ====================
// MID2 → STEP4
// ====================

await animateBetween(
currentTrack.mid2,
currentTrack.step4,
60,
"step4"
);

moveStep("step4");

}

async function animateBetween(
fromPoint,
toPoint,
frames,
step
){

for(
let f=1;
f<=frames;
f++
){

const t =
f / frames;

const point = {

innerX:
fromPoint.innerX +
(
toPoint.innerX -
fromPoint.innerX
)
* t,

innerY:
fromPoint.innerY +
(
toPoint.innerY -
fromPoint.innerY
)
* t,

outerX:
fromPoint.outerX +
(
toPoint.outerX -
fromPoint.outerX
)
* t,

outerY:
fromPoint.outerY +
(
toPoint.outerY -
fromPoint.outerY
)
* t

};

const lanePositions =
getLanePositions(
point,
currentData,
step
);

console.log(
"lanePositions",
step,
lanePositions
);

currentData.forEach((h,i)=>{

const horse =
document.getElementById(
`horse-${h.번호}`
);

if(horse){

horse.setAttribute(
"transform",
`translate(
${lanePositions[i].x},
${lanePositions[i].y}
)`
);

}

});

await sleep(16);

}

}

function goMyPage(){

    location.href =
    "mypage.html";

}

function goPointLog(){

    location.href =
    "point-log.html";

}

function logout(){

    localStorage.removeItem(
        "token"
    );

    location.href =
    "login.html";

}

function goMyPage(){

    location.href =
    "my.html";

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

window.scrollTo({

top:0,

behavior:"smooth"

});


}
