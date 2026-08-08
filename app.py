from pathlib import Path

# Keep the verified public-flow logic in app_core.py and only override media loading here.
core_path = Path(__file__).resolve().with_name("app_core.py")
source = core_path.read_text(encoding="utf-8")

hq_dir = Path(__file__).resolve().parent / "embedded_hq"
guide_parts = [hq_dir / "guide_hq_01.b64", hq_dir / "guide_hq_02.b64"]
if all(path.is_file() for path in guide_parts):
    source = source.replace(
        'GUIDE_IMAGE_B64 = read_embedded_text("guide.b64")',
        'GUIDE_IMAGE_B64 = "".join((ROOT_DIR / "embedded_hq" / name).read_text(encoding="utf-8").strip() for name in ("guide_hq_01.b64", "guide_hq_02.b64"))',
    )
    source = source.replace(
        'img_uri = f"data:image/webp;base64,{GUIDE_IMAGE_B64}" if GUIDE_IMAGE_B64 else ""',
        'img_uri = f"data:image/jpeg;base64,{GUIDE_IMAGE_B64}" if GUIDE_IMAGE_B64 else ""',
    )

video_names = tuple(f"facade_hq_{index:02d}.b64" for index in range(9))
video_parts = [hq_dir / name for name in video_names]
if all(path.is_file() for path in video_parts):
    old_video_loader = '''FACADE_VIDEO_B64 = "".join(\n    read_embedded_text(name)\n    for name in ("facade_01.b64", "facade_02.b64", "facade_03.b64")\n)'''
    new_video_loader = 'FACADE_VIDEO_B64 = "".join((ROOT_DIR / "embedded_hq" / name).read_text(encoding="utf-8").strip() for name in ' + repr(video_names) + ')'
    source = source.replace(old_video_loader, new_video_loader)

exec(compile(source, str(core_path), "exec"), globals(), globals())
