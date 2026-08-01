#  Cloudflare Edge Fabric — Apple Style Serverless Dashboard

Apple.com 특유의 고급스럽고 모던한 미학적 디자인 시스템과 Cloudflare 완전 네이티브 아키텍처 기반으로 제작된 정적(Serverless) React 대시보드 애플리케이션입니다.

## 🌟 주요 특징 (Key Features)

- **Apple.com 디자인 언어 준수**:
  - SF Pro / Inter 기반 프리미엄 서체 및 미니멀 레이아웃
  - `backdrop-filter` 기반의 고품격 글래스모피즘(Glassmorphism)
  - Bento Box 그리드 스타일 카드 구성
  - iOS/macOS 제어센터 형태의 인터랙티브 슬라이더 및 스위치 컨트롤
  - 다크 모드 / 라이트 모드 테마 전환
- **완전 정적 (Serverless Native)**:
  - 별도의 Node.js 번들러/빌드 과정 없이 CDN 방식의 React 18, Babel standalone, Chart.js, Lucide Icons 적용
  - `index.html`, `style.css`, `app.js` 3개 메인 파일로 완전히 분리된 클린 구조
- **Cloudflare 완전 네이티브 구성**:
  - `_headers` : 보안 헤더 및 엣지 캐싱 규칙
  - `_redirects` : SPA 라우팅 지원
  - `functions/api/stats.js` : Cloudflare Pages Functions 기반 엣지 서버리스 API 핸들러
  - `wrangler.toml` : Cloudflare CLI 1-클릭 배포 구성

---

## 📁 디렉토리 구조 (Project Structure)

```
.
├── index.html            # 메인 HTML 엔트리 포인트
├── style.css             # Apple Design System 전용 CSS 스타일시트
├── app.js                # React 컴포넌트 & 대시보드 로직 (JSX)
├── _headers              # Cloudflare Pages 엣지 보안 & 캐시 헤더
├── _redirects            # Cloudflare Pages 라우팅 규칙
├── wrangler.toml         # Cloudflare Wrangler CLI 배포 설정
└── functions/
    └── api/
        └── stats.js      # Cloudflare Pages Edge Serverless API
```

---

## 🚀 배포 방법 (Deployment Guide)

### 옵션 1. Cloudflare CLI (Wrangler) 이용
터미널에서 아래 명령어 한 줄로 즉시 Cloudflare Pages에 글로벌 배포할 수 있습니다:

```bash
npx wrangler pages deploy ./ --project-name=cloudflare-apple-dashboard
```

### 옵션 2. GitHub 연동 (Cloudflare Pages Dashboard)
1. 이 프로젝트를 GitHub 저장소에 push합니다.
2. [Cloudflare Dashboard](https://dash.cloudflare.com/) > **Workers & Pages** > **Create application** > **Pages**로 이동합니다.
3. GitHub 저장소를 연결하고 Build Setting을 다음과 같이 입력합니다:
   - **Framework preset**: None
   - **Build command**: (비워둠)
   - **Build output directory**: `/` 또는 `.`

---

## 🖥️ 로컬 미리보기 (Local Preview)

간단한 정적 웹 서버를 통해 로컬에서 즉시 확인 가능합니다:

```bash
npx serve .
# 또는
python -m http.server 8000
```
웹 브라우저에서 `http://localhost:8000` 접속.
