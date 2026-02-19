# soopuniv-slides

SoopUniv VRChat 월드의 강의 슬라이드를 호스팅하는 저장소입니다.

운영자가 Dropbox에 PDF를 업로드하면 자동으로 이미지로 변환되어 VRChat 월드에 반영됩니다.
**월드 재업로드 없이** PDF 파일 교체만으로 슬라이드를 갱신할 수 있습니다.

---

## 동작 방식

```
운영자가 Dropbox 폴더에 PDF 업로드
    ↓
GitHub Actions가 1시간마다 자동 감지
    ↓
PDF → 1920×1080 JPG 이미지로 자동 변환
    ↓
이 저장소의 Web/slides/ 에 자동 커밋
    ↓
GitHub Pages로 자동 배포 (~1분)
    ↓
VRChat 월드에서 즉시 사용 가능
```

---

## 저장소 구조

```
soopuniv-slides/
├── .github/
│   └── workflows/
│       ├── pdf-to-slides.yml   ← PDF 자동 변환 파이프라인 (Cron + 수동)
│       └── static.yml          ← GitHub Pages 배포 워크플로우
├── Web/                        ← GitHub Pages로 배포되는 폴더
│   ├── meta.json               ← 슬라이드 메타데이터 (총 페이지 수 등)
│   └── slides/
│       ├── slide_001.jpg
│       ├── slide_002.jpg
│       └── ...
├── scripts/
│   └── convert_pdf_to_slides.py  ← PDF → JPG 변환 스크립트
└── README.md
```

배포 후 URL 형식:
- 메타데이터: `https://juninjune.github.io/soopuniv-slides/meta.json`
- 슬라이드: `https://juninjune.github.io/soopuniv-slides/slides/slide_001.jpg`

---

## 슬라이드 교체 방법 (운영자용)

### 1. Dropbox에 PDF 업로드

1. Dropbox 공유 폴더(`/SoopUniv/slides-upload`)에 접속
2. 기존 PDF 파일이 있으면 **삭제** 후 새 파일 업로드
   (폴더 안에 PDF가 2개 이상이면 자동 변환이 실행되지 않습니다)
3. 최대 1시간 후 자동 반영

> **즉시 반영이 필요한 경우** → 아래 수동 트리거 참고

### 2. 수동 트리거 (즉시 반영)

1. 이 저장소의 **Actions** 탭 클릭
2. 왼쪽 목록에서 **"PDF to Slides"** 클릭
3. 오른쪽의 **"Run workflow"** 버튼 클릭 → **"Run workflow"** 확인
4. 워크플로우 실행 완료까지 약 2~3분 대기
5. 완료 후 초록색 체크(✅)가 표시되면 배포 완료

### 3. 반영 확인

브라우저에서 아래 URL을 열어 `total_pages` 숫자가 바뀌었는지 확인합니다.

```
https://juninjune.github.io/soopuniv-slides/meta.json
```

---

## VRChat 월드에서의 로딩 동작

- 월드 입장 후 슬라이드가 **1장당 약 5초** 간격으로 자동 로딩됩니다.
- 방송 **10분 전 미리 입장**하면 강의 시작 시점에 모든 슬라이드가 준비됩니다.
- 현재 페이지 주변 슬라이드가 우선 로딩되므로 천천히 넘기는 경우 바로 볼 수 있습니다.

---

## 슬라이드 사양

| 항목 | 사양 |
|------|------|
| 해상도 | 1920 × 1080 (16:9) |
| 포맷 | JPG (85% 품질) |
| 권장 장수 | 150장 이하 (이상은 별도 테스트 필요) |
| 파일명 형식 | `slide_001.jpg`, `slide_002.jpg`, ... |
