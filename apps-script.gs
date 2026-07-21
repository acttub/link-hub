// link.acttub.com/go 유입 기록 수신용 Apps Script (2026-07-21 작성)
//
// 설정 순서:
//   1. 구글 드라이브에서 새 스프레드시트를 만든다 (이름 예: "acttub 유입 기록").
//   2. 확장 프로그램 → Apps Script → 이 코드를 붙여넣는다.
//   3. 배포 → 새 배포 → 유형 "웹 앱"
//        실행: 나 / 액세스 권한: 모든 사용자
//   4. 나온 배포 URL을 go.html의 ENDPOINT 에 붙여넣고 push 한다.
//
// ⚠️ 리뷰 폼과 시트·배포를 절대 공유하지 않는다.
//    이 저장소는 공개라 배포 URL이 go.html에 그대로 노출된다. 즉 누구나 이 주소로
//    POST를 보낼 수 있다. 최악의 경우 이 시트에 가짜 행이 쌓이는 정도라 감수할 만하지만,
//    전화번호가 들어 있는 리뷰 응답 시트에는 절대 같은 문을 열어주면 안 된다.

const CLICK_HEADERS = ["at", "from", "src", "ref", "click_id"];

const LABELS = {
  at: "도착 시각",
  from: "채널",
  src: "링크 파라미터",
  ref: "출처 사이트",
  click_id: "클릭 ID"
};

function label(k) { return LABELS[k] || k; }

// 시트는 "="로 시작하는 문자열을 수식으로 해석해 실행한다.
// 이 웹 앱은 누구나 POST할 수 있으므로(주소가 공개 저장소에 있다) 그대로 넣으면
// =IMPORTXML(...) 같은 걸 심어 시트가 외부로 요청을 보내게 만들 수 있다.
// 앞에 작은따옴표를 붙이면 시트가 "이건 글자다"로 받아 실행하지 않는다.
function asText(v) {
  const s = String(v == null ? "" : v);
  return /^[=+\-@\t\r]/.test(s) ? "'" + s : s;
}

function appendTo(ss, name, headers, data) {
  let s = ss.getSheetByName(name);
  if (!s) s = ss.insertSheet(name);
  if (s.getLastRow() === 0) s.appendRow(headers.map(label));
  s.appendRow(headers.map(function (h) { return asText(data[h]); }));
}

function doPost(e) {
  // 빈 요청·깨진 JSON에 스크립트가 죽지 않게 한다. 기록 실패가 사람의 이동을 막지는
  // 않지만(그건 go.html에서 이미 분리했다), 오류 메일이 계속 오는 걸 막는다.
  try {
    const data = JSON.parse(e.postData.contents);
    if (data.type !== "click") return ContentService.createTextOutput("ignored");
    appendTo(SpreadsheetApp.getActiveSpreadsheet(), "유입", CLICK_HEADERS, data);
    return ContentService.createTextOutput("ok");
  } catch (err) {
    return ContentService.createTextOutput("bad request");
  }
}
