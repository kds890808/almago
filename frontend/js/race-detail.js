async function goAI(
    region,
    raceNo,
    raceDate
){

    if(!region || !raceNo || !raceDate){

        alert("경주 정보가 부족합니다. 다시 선택해주세요.");

        console.log("goAI 오류", {
            region,
            raceNo,
            raceDate
        });

        return;

    }

    const safeDate =
    encodeURIComponent(raceDate);

    location.href =
    `analysis-select.html?region=${region}&raceNo=${raceNo}&raceDate=${safeDate}`;

}

async function showRaceDetail(
region,
raceNo,
date
){

console.log(
"지역:",
region,
"경주:",
raceNo
);

const url =
`/race-detail-data/${raceNo}?date=${date}&region=${region}`;

console.log(
"호출URL:",
url
);

const res=await fetch(url);

const data=await res.json();

console.log(
"받은데이터:",
data
);

let html=`

<div class="card">

<div class="click-info-guide">
💡 색상이 있는 이름을 누르면 상세정보를 볼 수 있습니다.
</div>

<div
class="race-scroll-wrap"
style="overflow-x:auto;"
>

<table class="race-detail-table" style="
width:max-content;
min-width:100%;
border-collapse:collapse;
font-size:13px;
">

<style>
th,td{
border:1px solid #ddd;
padding:8px;
white-space:nowrap;
text-align:center;
}

th{
background:#f5f7ff;
position:sticky;
top:0;
}

.menu-item{

cursor:pointer;

transition:.2s;

}

.menu-item:active{

transform:scale(.95);

}
</style>

<tr>

<th>지역</th>
<th>날짜</th>
<th>경주번호</th>
<th>번호</th>
<th>마명</th>
<th>마종</th>
<th>성별</th>
<th>연령</th>
<th>인기도</th>
<th>
    통산전적<br>
    <span style="font-size:11px; font-weight:600;">
        출전수(1위/2위/3위/4위/5위)
    </span>
</th>
${region !== "제주" ? "<th>최근전적</th>" : ""}
<th>레이팅</th>
<th>중량</th>
<th>증감</th>
<th>기수명</th>
<th>조교사명</th>
<th>마주명</th>
<th>조교횟수</th>
<th>출전주기</th>
<th>장구현황</th>
<th>특이사항</th>

</tr>

`;

data.forEach(row=>{

const popularity =
Number(row["인기도"]);

const top5Class =
popularity >= 1 &&
popularity <= 5
? "popularity-top5"
: "";

html+=`

<tr class="${top5Class}">

<td>${row["지역"] || ""}</td>
<td>${row["경주일자"] || ""}</td>
<td>${row["경주"] || ""}</td>
<td>${row["번호"] || ""}</td>

<td>

<a
href="#"
onclick="
event.preventDefault();
showHorseInfo(
'${row["마명"]}'
)
"
style="
color:#2563eb;
font-weight:bold;
text-decoration:none;
"
>

${row["마명"] || ""}

</a>

</td>

<td>${row["마종"] || ""}</td>
<td>${row["성별"] || ""}</td>
<td>${row["나이"] || ""}</td>
<td>${row["인기도"] || "-"}</td>
<td>${row["통산전적"] || "-"}</td>
${region !== "제주"
? `<td>${
    row["최근전적"]
    ? String(row["최근전적"])
        .trim()
        .split(/\s+/)
        .map(v => v + "위")
        .join(" ")
    : "-"
}</td>`
: ""}
<td>${row["레이팅"] || ""}</td>
<td>${row["부담중량"] || ""}</td>
<td>${row["증감"] || ""}</td>

<td>

<a
href="#"
onclick="
event.preventDefault();
showJockeyInfo(
'${row["기수"]}'
)
"
style="
color:#16a34a;
font-weight:bold;
text-decoration:none;
"
>

${row["기수"] || ""}

</a>

</td>

<td>

<a
href="#"
onclick="
event.preventDefault();
showTrainerInfo(
'${row["조교사"]}'
)
"
style="
color:#dc2626;
font-weight:bold;
text-decoration:none;
"
>

${row["조교사"] || ""}

</a>

</td>

<td>${row["마주명"] || ""}</td>
<td>${row["조교횟수"] || ""}</td>
<td>${row["출전주기"] || ""}</td>
<td>${row["장구현황"] || ""}</td>
<td>${row["특이사항"] || ""}</td>

</tr>

`;

});


html += `
</table>

<div class="basic-scroll-guide">
    <span>←</span>
    <b>좌우로 밀어서 확인하세요</b>
    <span>→</span>
</div>

</div>
</div>
`;

let displayDate = date;
const rawDate =
String(displayDate || "")
.replace(/\D/g, "");

const raceDate =
rawDate.length === 8
? `${rawDate.slice(0,4)}/${rawDate.slice(4,6)}/${rawDate.slice(6,8)}`
: displayDate;

document.getElementById(
"modal-title"
).innerText =
`${region} ${raceNo}경주 ${raceDate}`;

document.getElementById(
"modal-body"
).innerHTML = html;

document.getElementById(
"race-modal"
).style.display="flex";

}

function closeRaceModal(){

document.getElementById(
"race-modal"
).style.display="none";

}


// 팝업 바깥 누르면 닫힘
window.onclick=function(e){

const raceModal=
document.getElementById(
"race-modal"
);

const horseModal=
document.getElementById(
"horse-modal"
);

if(e.target===raceModal){
raceModal.style.display="none";
}

if(e.target===horseModal){
horseModal.style.display="none";
}

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
th,td{
border:1px solid #ddd;
padding:8px;
text-align:center;
white-space:nowrap;
}

th{
background:#f5f7ff;
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