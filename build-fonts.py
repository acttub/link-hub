#!/usr/bin/env python3
"""index.html에 실제로 쓰인 글자만 담은 Pretendard woff2를 만든다.

페이지 문구가 고정이라 전체 한글(1.5MB/굵기)을 실을 이유가 없다.
쓰인 글자만 서브셋하면 굵기당 수 KB로 끝난다.

⚠️ index.html의 문구를 고치면 이 스크립트를 다시 돌려야 한다.
   안 돌리면 새로 쓴 글자가 시스템 폰트로 렌더돼 서체가 섞인다.

실행:
    uv run --with "fonttools[woff]" python build-fonts.py

원본 otf는 볼트 brand/fonts/ 에 있다(공개 저장소에 커밋하지 않는다).
"""
import html
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
SRC_DIR = pathlib.Path.home() / "Soma" / "brand" / "fonts"
OUT_DIR = HERE / "fonts"

# CSS font-weight -> 원본 파일
WEIGHTS = {
    500: "Pretendard-Medium.otf",    # 이 브랜드의 가장 얇은 굵기 (Regular 파일이 없다)
    600: "Pretendard-SemiBold.otf",
    700: "Pretendard-Bold.otf",
}

# 문구를 조금 고쳐도 깨지지 않도록 넣어두는 최소 안전망
ALWAYS = (
    "0123456789"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    " .,!?·—–-~:;'\"()[]/@&%+*#…"
)


def page_text() -> str:
    """index.html의 사람이 읽는 텍스트만 뽑는다 (style/script/태그 제외)."""
    src = (HERE / "index.html").read_text(encoding="utf-8")
    src = re.sub(r"<(style|script)\b.*?</\1>", " ", src, flags=re.S | re.I)
    # 사용자에게 보이는 속성값도 포함 (alt, content 등)
    attrs = " ".join(re.findall(r'(?:content|alt|title)="([^"]*)"', src))
    body = re.sub(r"<[^>]+>", " ", src)
    return html.unescape(body + " " + attrs)


def main() -> int:
    if not SRC_DIR.is_dir():
        print(f"원본 폰트 폴더가 없다: {SRC_DIR}", file=sys.stderr)
        return 1

    chars = sorted(set(page_text()) | set(ALWAYS))
    text = "".join(c for c in chars if c.isprintable() and not c.isspace())
    print(f"서브셋 대상 글자 {len(text)}자")

    OUT_DIR.mkdir(exist_ok=True)
    total = 0
    for weight, filename in WEIGHTS.items():
        src = SRC_DIR / filename
        if not src.is_file():
            print(f"  건너뜀 (원본 없음): {filename}", file=sys.stderr)
            continue
        out = OUT_DIR / f"pretendard-{weight}.woff2"
        subprocess.run(
            [
                "pyftsubset", str(src),
                f"--text={text}",
                "--flavor=woff2",
                "--layout-features=kern,liga",
                "--desubroutinize",
                f"--output-file={out}",
            ],
            check=True,
        )
        size = out.stat().st_size
        total += size
        print(f"  {out.name:24} {size/1024:6.1f}KB")

    print(f"합계 {total/1024:.1f}KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
