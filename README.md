#  Cloudflare Edge Fabric — Apple Style Serverless Dashboard

Apple.com 특유의 고급스럽고 모던한 미학적 디자인 시스템과 Cloudflare 완전 네이티브 아키텍처 기반으로 제작된 정적(Serverless) React 대시보드 애플리케이션입니다.

---

## 🛠️ Cloudflare Pages 빌드 실패 원인 & 해결 가이드 (Build Fix)

### ❓ 원인 (Root Cause)
Cloudflare Pages에 GitHub 저장소를 연결할 때, 기본 설정(Framework preset)이 React/Next.js/Vite 등으로 자동 감지되면서 Cloudflare가 존재하지 않는 `npm run build` 명령을 실행하려고 하여 **`npm ERR! missing script: build`** 또는 빌드 에러가 발생합니다.

### ✅ 해결책 (Fix)
1. **`package.json` 추가 완료**: 프로젝트 루트에 `"build": "echo 'Static build ready'"` 스크립트가 포함된 `package.json`을 추가하여 Cloudflare가 `npm run build`를 실행하더라도 오류 없이 빌드가 통과되도록 조치했습니다.
2. **Cloudflare Pages 대시보드 권장 설정**:
   - **Framework preset**: `None`
   - **Build command**: `(비워두기)` 또는 `npm run build`
   - **Build output directory**: `/` 또는 `.`

---

## 📁 디렉토리 구조 (Project Structure)

```
.
├── index.html            # 메인 HTML 엔트리 포인트
├── style.css             # Apple Design System 전용 CSS 스타일시트
├── app.js                # React 컴포넌트 & 대시보드 로직 (JSX)
├── package.json          # Cloudflare Pages 빌드 세팅 호환용 패키지 파일
├── _headers              # Cloudflare Pages 엣지 보안 & 캐시 헤더
├── _redirects            # Cloudflare Pages 라우팅 규칙
├── wrangler.toml         # Cloudflare Wrangler CLI 배포 설정
└── functions/
    └── api/
        └── stats.js      # Cloudflare Pages Edge Serverless API
```

---

## 🚀 배포 방법 (Deployment Guide)

### 옵션 1. GitHub 자동 연결 (Cloudflare Pages Dashboard)
1. [Cloudflare Dashboard](https://dash.cloudflare.com/) > **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**
2. `Plamingo/Product-builder-first` 저장소 선택
3. Build configuration 설정:
   - **Framework preset**: `None`
   - **Build command**: (비워둠 또는 `npm run build`)
   - **Build output directory**: `/`
4. **Save and Deploy** 클릭!

### 옵션 2. Cloudflare CLI (Wrangler) 직접 배포
```bash
npx wrangler pages deploy ./ --project-name=cloudflare-apple-dashboard
```
