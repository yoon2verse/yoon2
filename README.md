# 픽셀 웨딩홀 청첩장 배포 방법 (약 10분)

## 1. 화면만 먼저 올리기 (3분, 방명록은 각자 기기에만 저장)
1. https://app.netlify.com/drop 접속 → 구글 계정으로 로그인
2. 이 `pixel-wedding` 폴더를 통째로 끌어다 놓기
3. 생기는 주소(예: xxx.netlify.app)를 폰으로 열기 → Site settings에서 이름 변경 가능

## 2. 방명록 모두 공유되게 하기 (7분)
1. https://supabase.com → 로그인 → New project (무료)
2. 왼쪽 SQL Editor → `supabase.sql` 내용 붙여넣기 → Run
3. Project Settings → API 에서 `Project URL`, `anon public` 키 복사
4. `index.html` 에서 `SUPABASE_URL=''`, `SUPABASE_KEY=''` 따옴표 안에 붙여넣기
5. Netlify 사이트 → Deploys 탭에 폴더 다시 끌어다 놓기

## 수정할 곳 (index.html)
- 상단 배지: `민준 ♥ 서연 · 2026.11.21 SAT`
- 예식 안내: `<dl>` 안 일시·장소·이름
- 신랑신부 캐릭터 이름: `couple=[` 부분
- 샘플 하객: `NAMES` 목록 (실제 방명록이 생기면 점점 줄어듦)
