"""Manim scene: the kernel trick, shown as a real 3D lift.

2D concentric-circles data is not linearly separable. We map each point up into
a third dimension with z = x^2 + y^2 (an RBF/polynomial-style feature), which
pushes the outer ring high and keeps the inner cluster low. A flat plane can
then slice cleanly between them -- that separating plane is the "hyperplane" the
kernel trick gives us.

Render locally:
    manim -qh manim_scenes/kernel_trick_scene.py KernelTrickScene

Then copy the output mp4 to:
    assets/videos/kernel_trick_intro.mp4
"""

import math

from manim import (
    BLUE,
    RED,
    GREEN,
    WHITE,
    DEGREES,
    DOWN,
    UP,
    ThreeDScene,
    ThreeDAxes,
    Dot3D,
    Line,
    Surface,
    Text,
    VGroup,
    Create,
    Write,
    FadeIn,
    FadeOut,
)


# Lift function: the higher-dimensional feature. Outer points rise, inner stay low.
def _z(x, y):
    return 0.3 * (x * x + y * y)


class KernelTrickScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[0, 3, 1],
            x_length=6,
            y_length=6,
            z_length=3,
        )

        # Inner cluster (class 0) and outer ring (class 1) -- not linearly separable in 2D.
        inner_xy = [(1.2 * math.cos(2 * math.pi * k / 8), 1.2 * math.sin(2 * math.pi * k / 8)) for k in range(8)]
        outer_xy = [(2.6 * math.cos(2 * math.pi * k / 14), 2.6 * math.sin(2 * math.pi * k / 14)) for k in range(14)]

        inner = VGroup(*[Dot3D(axes.c2p(x, y, 0), color=BLUE, radius=0.09) for x, y in inner_xy])
        outer = VGroup(*[Dot3D(axes.c2p(x, y, 0), color=RED, radius=0.09) for x, y in outer_xy])

        # Start looking straight down so it reads as a flat 2D plot.
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        title = Text("Kernel Trick", font_size=36).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        self.play(FadeIn(inner), FadeIn(outer))

        cap1 = Text("In 2D, a straight line cannot separate the circles", font_size=24).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(cap1)
        self.play(Write(cap1))

        # A doomed attempt at a straight separator (in the xy-plane).
        bad_line = Line(axes.c2p(-3.2, -1.5, 0), axes.c2p(3.2, 1.5, 0), color=GREEN, stroke_width=5)
        self.play(Create(bad_line))
        self.wait(0.8)
        self.play(FadeOut(bad_line))

        # Lift each point to z = x^2 + y^2 while tilting the camera into a 3D view.
        cap2 = Text("Map data into a higher dimension:  z = x² + y²", font_size=24).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(cap2)
        self.play(FadeOut(cap1), Write(cap2))

        lift_anims = []
        for d, (x, y) in zip(inner, inner_xy):
            lift_anims.append(d.animate.move_to(axes.c2p(x, y, _z(x, y))))
        for d, (x, y) in zip(outer, outer_xy):
            lift_anims.append(d.animate.move_to(axes.c2p(x, y, _z(x, y))))

        self.move_camera(
            phi=65 * DEGREES,
            theta=-50 * DEGREES,
            added_anims=lift_anims + [Create(axes)],
            run_time=2.5,
        )
        self.wait(0.3)

        # A flat plane slides in between the lifted clusters -> linearly separable now.
        plane = Surface(
            lambda u, v: axes.c2p(u, v, 1.1),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(1, 1),
            fill_color=GREEN,
            fill_opacity=0.4,
            checkerboard_colors=[GREEN, GREEN],
            stroke_width=0,
        )
        cap3 = Text("Now a flat plane separates them", font_size=24).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(cap3)
        self.play(FadeOut(cap2), Create(plane), Write(cap3))
        self.wait(0.5)

        # Slow rotation to show off the 3D separation.
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        caption = Text(
            "Kernel Trick helps SVM separate non-linear data",
            font_size=26,
            color=WHITE,
        ).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(FadeOut(cap3), Write(caption))
        self.wait(2)
