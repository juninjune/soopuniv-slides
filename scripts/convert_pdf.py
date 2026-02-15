#!/usr/bin/env python3
"""
PDF → 슬라이드 이미지 변환 스크립트.
PDF 파일을 1920x1080 JPG 이미지로 변환하고 meta.json을 생성한다.
"""

import json
import os
import shutil
import sys
from datetime import datetime, timezone

from pdf2image import convert_from_path
from PIL import Image

# --- 설정 ---
OUTPUT_DIR = "Web/slides"
META_PATH = "Web/meta.json"
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
JPG_QUALITY = 85
DPI = 200  # PDF 렌더링 해상도. 높을수록 선명하지만 느림


def convert_pdf_to_slides(pdf_path: str) -> None:
    """PDF를 슬라이드 이미지로 변환한다."""

    pdf_filename = os.path.basename(pdf_path)
    print(f"[1/4] PDF 로드: {pdf_filename}")

    # PDF → PIL Image 리스트
    pages = convert_from_path(pdf_path, dpi=DPI)
    total_pages = len(pages)
    print(f"       {total_pages}페이지 감지됨")

    # 기존 slides 폴더 전체 삭제 후 재생성
    print(f"[2/4] {OUTPUT_DIR}/ 폴더 초기화")
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # 각 페이지를 1920x1080 JPG로 저장
    print(f"[3/4] 이미지 변환 중 ({TARGET_WIDTH}x{TARGET_HEIGHT}, JPG {JPG_QUALITY}%)")
    for i, page in enumerate(pages):
        page_num = i + 1
        # 1920x1080으로 리사이즈 (비율 유지하지 않고 맞춤)
        resized = page.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
        # RGB 변환 (RGBA인 경우 대비)
        if resized.mode != "RGB":
            resized = resized.convert("RGB")

        filename = f"slide_{page_num:03d}.jpg"
        filepath = os.path.join(OUTPUT_DIR, filename)
        resized.save(filepath, "JPEG", quality=JPG_QUALITY)

        file_size_kb = os.path.getsize(filepath) / 1024
        print(f"       {filename} ({file_size_kb:.0f} KB)")

    # meta.json 생성
    print(f"[4/4] meta.json 생성")
    meta = {
        "total_pages": total_pages,
        "version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_pdf": pdf_filename,
    }
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"\n완료! {total_pages}장 변환됨 → {OUTPUT_DIR}/")
    print(f"meta.json → {META_PATH}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"사용법: python {sys.argv[0]} <PDF 파일 경로>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.exists(pdf_path):
        print(f"에러: 파일을 찾을 수 없습니다: {pdf_path}")
        sys.exit(1)

    convert_pdf_to_slides(pdf_path)
