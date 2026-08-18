from pathlib import Path

# Keep the verified public-flow logic in app_core.py and only override media loading here.
# HQ assets are used only after every expected chunk exists; otherwise the known-good
# legacy media in app_core.py remains active. This prevents partial/corrupt media from
# ever becoming public during staged uploads.
core_path = Path(__file__).resolve().with_name("app_core.py")
source = core_path.read_text(encoding="utf-8")

# Public display-only compatibility layer for the legacy Streamlit deployment.
# Do not rename internal repository/source identifiers or payload keys here.
_PUBLIC_DISPLAY_REPLACEMENTS = (
    (
        'page_title="Meta RC Pulse | あなたの夢に、確かな一歩を。"',
        'page_title="EJIMA WORLD | あなたの夢に、確かな一歩を。"',
    ),
    (
        '<div class="hero-kicker">META RC PULSE</div>',
        '<div class="hero-kicker">EJIMA WORLD</div>',
    ),
    (
        '案内人を選んで、Meta RC Pulseを始めてください。',
        '案内人を選んで、EJIMA WORLDを始めてください。',
    ),
    (
        'alt="Meta RC Pulse 女性・男性パルス案内人"',
        'alt="EJIMA WORLD 女性・男性パルス案内人"',
    ),
    (
        'ようこそ、Meta RC パルスへ。私は、パルスと申します。本日はコンシェルジュとして、お客様をご案内いたします。',
        'ようこそ、EJIMA WORLDへ。EJIMA WORLDのAIコンシェルジュ、パルスです。',
    ),
)
for before, after in _PUBLIC_DISPLAY_REPLACEMENTS:
    source = source.replace(before, after)

hq_dir = Path(__file__).resolve().parent / "embedded_hq"
guide_names = tuple(f"guide_full_{index:02d}.b64" for index in range(26))
guide_parts = [hq_dir / name for name in guide_names]
if all(path.is_file() for path in guide_parts):
    source = source.replace(
        'GUIDE_IMAGE_B64 = read_embedded_text("guide.b64")',
        'GUIDE_IMAGE_B64 = "".join((ROOT_DIR / "embedded_hq" / name).read_text(encoding="utf-8").strip() for name in ' + repr(guide_names) + ')',
    )
    source = source.replace(
        'img_uri = f"data:image/webp;base64,{GUIDE_IMAGE_B64}" if GUIDE_IMAGE_B64 else ""',
        'img_uri = f"data:image/jpeg;base64,{GUIDE_IMAGE_B64}" if GUIDE_IMAGE_B64 else ""',
    )

video_names = tuple(f"facade_hq_{index:02d}.b64" for index in range(17))
video_parts = [hq_dir / name for name in video_names]
if all(path.is_file() for path in video_parts):
    old_video_loader = '''FACADE_VIDEO_B64 = "".join(\n    read_embedded_text(name)\n    for name in ("facade_01.b64", "facade_02.b64", "facade_03.b64")\n)'''
    new_video_loader = 'FACADE_VIDEO_B64 = "".join((ROOT_DIR / "embedded_hq" / name).read_text(encoding="utf-8").strip() for name in ' + repr(video_names) + ')'
    source = source.replace(old_video_loader, new_video_loader)

exec(compile(source, str(core_path), "exec"), globals(), globals())
