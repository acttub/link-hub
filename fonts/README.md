# 폰트

이 폴더의 `pretendard-*.woff2`는 **Pretendard**를 `index.html`에 쓰인 글자만
남기고 서브셋한 파일이다.

- 원저작자: 길형진 (orioncactus)
- 프로젝트: https://github.com/orioncactus/pretendard
- 라이선스: **SIL Open Font License 1.1** — https://github.com/orioncactus/pretendard/blob/main/LICENSE

OFL은 서브셋·재배포를 허용하며, 폰트 자체를 판매하지 않고 라이선스를 함께
배포할 것을 요구한다. 이 문서가 그 고지다.

## 다시 만들려면

`index.html`의 문구를 고치면 새 글자가 서브셋에 없어 시스템 폰트로 렌더된다.
저장소 루트에서:

```bash
uv run --with "fonttools[woff]" python build-fonts.py
```

원본 otf는 이 저장소에 없다(볼트 `brand/fonts/`에 있다).
