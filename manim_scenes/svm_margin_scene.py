"""Manim scene: maximum-margin intuition.

Render locally (NOT in Streamlit):
    manim -pqh manim_scenes/svm_margin_scene.py SVMMarginScene

Then copy the output mp4 to:
    assets/videos/svm_margin_intro.mp4
"""

from manim import (
    BLUE,
    RED,
    YELLOW,
    GREEN,
    WHITE,
    GREY,
    DOWN,
    UP,
    Scene,
    Axes,
    Dot,
    Line,
    Text,
    VGroup,
    Create,
    Write,
    FadeIn,
    FadeOut,
    Transform,
)


class SVMMarginScene(Scene):
    def construct(self):
        axes = Axes(x_range=[-1, 7, 1], y_range=[-1, 7, 1], tips=False)

        # Two linearly separable clusters.
        class_a = [(1, 5), (1.5, 6), (2, 5.5), (1.2, 4.5), (2.2, 6.2)]
        class_b = [(5, 1.5), (5.5, 2), (6, 1), (4.8, 2.3), (5.8, 2.6)]

        dots_a = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in class_a])
        dots_b = VGroup(*[Dot(axes.c2p(x, y), color=RED) for x, y in class_b])

        title = Text("SVM: which line is best?", font_size=32).to_edge(UP)

        self.play(Create(axes), Write(title))
        self.play(FadeIn(dots_a), FadeIn(dots_b))
        self.wait(0.5)

        # A few "bad" candidate separating lines.
        bad1 = Line(axes.c2p(0, 3.2), axes.c2p(4, 6.5), color=GREY)
        bad2 = Line(axes.c2p(2.5, -0.5), axes.c2p(6.5, 4.5), color=GREY)
        self.play(Create(bad1))
        self.wait(0.3)
        self.play(Transform(bad1, bad2))
        self.wait(0.3)

        # The maximum-margin boundary (the good one).
        boundary = Line(axes.c2p(0.5, 0.5), axes.c2p(6, 6), color=GREEN, stroke_width=5)
        margin_up = Line(axes.c2p(-0.2, 1.3), axes.c2p(5.3, 6.8), color=YELLOW)
        margin_dn = Line(axes.c2p(1.2, -0.2), axes.c2p(6.7, 5.3), color=YELLOW)

        new_title = Text("Maximum margin boundary", font_size=32).to_edge(UP)
        self.play(Transform(bad1, boundary), Transform(title, new_title))
        self.play(Create(margin_up), Create(margin_dn))
        self.wait(0.5)

        # Highlight support vectors (closest points to the boundary).
        sv_points = [axes.c2p(2, 5.5), axes.c2p(2.2, 6.2), axes.c2p(4.8, 2.3)]
        svs = VGroup(*[Dot(p, color=YELLOW, radius=0.12) for p in sv_points])
        sv_label = Text("Support Vectors", font_size=26, color=YELLOW).to_edge(DOWN)
        self.play(FadeIn(svs), Write(sv_label))
        self.wait(0.5)

        caption = Text(
            "SVM chooses the hyperplane with the maximum margin",
            font_size=26,
            color=WHITE,
        ).to_edge(DOWN)
        self.play(FadeOut(sv_label), Write(caption))
        self.wait(2)
