"""Manim scene: support vectors determine the margin.

Render locally:
    manim -pqh manim_scenes/support_vectors_scene.py SupportVectorsScene

Then copy the output mp4 to:
    assets/videos/support_vectors_intro.mp4
"""

from manim import (
    BLUE,
    RED,
    YELLOW,
    GREEN,
    WHITE,
    UP,
    DOWN,
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
    Indicate,
)


class SupportVectorsScene(Scene):
    def construct(self):
        axes = Axes(x_range=[-1, 7, 1], y_range=[-1, 7, 1], tips=False)

        class_a = [(1, 5), (1.5, 6), (2, 5.5), (1.2, 4.5), (2.2, 6.2)]
        class_b = [(5, 1.5), (5.5, 2), (6, 1), (4.8, 2.3), (5.8, 2.6)]
        dots_a = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in class_a])
        dots_b = VGroup(*[Dot(axes.c2p(x, y), color=RED) for x, y in class_b])

        title = Text("Support Vectors", font_size=34).to_edge(UP)
        self.play(Create(axes), Write(title))
        self.play(FadeIn(dots_a), FadeIn(dots_b))

        # Decision boundary.
        boundary = Line(axes.c2p(0.5, 0.5), axes.c2p(6, 6), color=GREEN, stroke_width=5)
        self.play(Create(boundary))
        self.wait(0.4)

        # Highlight the closest points -> support vectors.
        sv_points = [axes.c2p(2, 5.5), axes.c2p(2.2, 6.2), axes.c2p(4.8, 2.3)]
        svs = VGroup(*[Dot(p, color=YELLOW, radius=0.13) for p in sv_points])
        label = Text("These closest points are Support Vectors", font_size=26, color=YELLOW).to_edge(DOWN)
        self.play(FadeIn(svs), Write(label))
        self.play(*[Indicate(sv, color=YELLOW) for sv in svs])
        self.wait(0.6)

        caption = Text(
            "Only support vectors determine the margin",
            font_size=28,
            color=WHITE,
        ).to_edge(DOWN)
        self.play(FadeOut(label), Write(caption))
        self.wait(2)
