import streamlit as st

st.set_page_config(page_title="プレビュー終了", page_icon="🔒", layout="centered")
st.markdown(
    """
    <style>
    #MainMenu, footer, header, [data-testid="stToolbar"] {display:none !important;}
    .stApp {background:#020817;color:#fff;}
    .retired {max-width:680px;margin:20vh auto;padding:2rem;border:1px solid #31425f;
      border-radius:24px;background:#071225;text-align:center;}
    .retired h1 {font-size:clamp(1.8rem,6vw,3rem);}
    .retired p {color:#c7d4e8;line-height:1.8;}
    </style>
    <div class="retired">
      <h1>このプレビューは終了しました</h1>
      <p>このURLは正規のライブパルス版ではないため、利用できない状態にしました。</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.stop()

from pathlib import Path

# Keep the verified public-flow logic in app_core.py and only override media loading here.
# HQ assets are used only after every expected chunk exists; otherwise the known-good
# legacy media in app_core.py remains active. This prevents partial/corrupt media from
# ever becoming public during staged uploads.
core_path = Path(__file__).resolve().with_name("app_core.py")
source = core_path.read_text(encoding="utf-8")

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
