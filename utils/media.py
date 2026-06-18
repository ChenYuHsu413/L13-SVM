"""Helpers for locating and safely playing pre-rendered Manim videos.

The Streamlit app NEVER renders Manim at runtime. It only plays mp4 files that
were rendered locally and copied into assets/videos/. If a file is missing we
show a friendly hint instead of crashing.
"""

from pathlib import Path

import streamlit as st

# Project root = parent of the utils/ folder. Keeps paths relative (no absolute
# hard-coding) so the app works on Streamlit Community Cloud too.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIDEO_DIR = PROJECT_ROOT / "assets" / "videos"


def play_video(filename, caption=None):
    """Play assets/videos/<filename> if it exists, else show a hint.

    Parameters
    ----------
    filename : str
        e.g. "svm_margin_intro.mp4"
    caption : str, optional
        Caption shown above the video / hint.
    """
    if caption:
        st.caption(caption)

    video_path = VIDEO_DIR / filename
    if video_path.exists():
        st.video(str(video_path))
    else:
        st.info(
            f"🎬 影片尚未產生：`assets/videos/{filename}`\n\n"
            "請先在本機使用 Manim 渲染動畫，並把輸出的 mp4 複製到 "
            "`assets/videos/`。詳細指令請見 README。"
        )
