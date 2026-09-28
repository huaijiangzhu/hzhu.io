"""Generate blog SVG/PNG figures from the verified MuJoCo / Pinocchio example."""

import os
from pathlib import Path
import tempfile
import zipfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "featherstone-mpl"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnnotationBbox, DrawingArea, HPacker, TextArea
from matplotlib.patches import Circle, Polygon
from matplotlib.text import Text
import numpy as np

from compare_libraries import make_models, sample, verify

OUTPUT = Path(__file__).resolve().parents[2] / "static/images/featherstone"
BLUE = "#2368b5"
MOTION = "#77469b"
ORANGE = "#bf5b26"
INK = "#263340"
GRAY = "#687682"
LIGHT = "#c9d1d8"
BODY_AXIS_COLORS = ("#cf4146", "#278a50", "#2867bf")


def save(fig, name):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "png"):
        metadata = {"Date": None} if extension == "svg" else {}
        fig.savefig(OUTPUT / f"{name}.{extension}", dpi=200,
                    facecolor="white", metadata=metadata)
    plt.close(fig)


def package_example():
    source = Path(__file__).resolve().parent
    destination = OUTPUT.parents[1] / "downloads/featherstone-example.zip"
    destination.parent.mkdir(parents=True, exist_ok=True)
    filenames = [
        ".gitignore", "README.md", "requirements.txt", "compare_libraries.py",
        "plot_figures.py", "verified-results.json",
    ]
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in filenames:
            archive.write(source / name, "examples/featherstone/" + name)


def arrow(ax, origin, vector, color, width=2.2, scale=0.42, zorder=5, shrink_b=0):
    start = np.asarray(origin)[:2]
    end = start + scale * np.asarray(vector)[:2]
    ax.annotate("", xy=end, xytext=start,
                arrowprops={"arrowstyle": "-|>", "lw": width,
                            "color": color, "mutation_scale": 15,
                            "shrinkA": 0, "shrinkB": shrink_b},
                zorder=zorder)


def column_vector_label(ax, position, symbol, components, unit, color):
    """A square-bracket column vector, with mathtext symbols and upright units."""
    matrix = DrawingArea(24, 46, clip=False)
    for x in ([6,1,1,6], [18,23,23,18]):
        matrix.add_artist(Line2D(x, [45,45,1,1], color=color, lw=1))
    for value, y in zip(components, [38,23,8]):
        matrix.add_artist(Text(12, y, f"${value}$", ha="center", va="center",
                               fontsize=13, color=color))
    label = HPacker(children=[
        TextArea(f"${symbol}=$", textprops={"fontsize":13, "color":color}),
        matrix,
        TextArea(r"$\mathrm{" + unit + "}$",
                 textprops={"fontsize":13, "color":color}),
    ], align="center", pad=0, sep=4)
    ax.add_artist(AnnotationBbox(label, position, xycoords="data",
                                frameon=False, box_alignment=(0,.5), pad=0,
                                zorder=9))


def setup_figure(models):
    state = sample(models, 0.0)
    p = state["position_mujoco"]
    velocity = state["mujoco_velocity"][3:]

    # Orthographically project 3D geometry; annotate in the image plane so that
    # labels stay legible at the blog's column width.
    azimuth, elevation = np.deg2rad([-58, 28])
    right = np.array([-np.sin(azimuth), np.cos(azimuth), 0])
    up = np.array([-np.sin(elevation)*np.cos(azimuth),
                   -np.sin(elevation)*np.sin(azimuth), np.cos(elevation)])

    def project(points):
        return np.asarray(points) @ np.stack([right, up]).T

    def path(points, **kwargs):
        xy = project(points)
        ax.plot(xy[:, 0], xy[:, 1], **kwargs)

    def vector(origin, displacement, color, width=1.5, zorder=5):
        arrow(ax, project(origin), project(displacement), color,
              width=width, scale=1, zorder=zorder)

    def ring(theta, radius=1.2, z=0):
        return np.column_stack([radius*np.cos(theta), radius*np.sin(theta),
                                np.full_like(theta, z)])

    fig, ax = plt.subplots(figsize=(8.6, 5.3))
    fig.subplots_adjust(left=.025, right=.985, top=.96, bottom=.045)

    # Give the disk a visible rim. Its top represents the xy plane, z = 0.
    # Only the half facing the camera contributes to the visible side wall.
    front = np.linspace(azimuth-np.pi/2, azimuth+np.pi/2, 100)
    upper, lower = ring(front), ring(front, z=-.13)
    side = np.vstack([upper, lower[::-1]])
    ax.add_patch(Polygon(project(side), facecolor="#d6e0e9",
                         edgecolor="#aabac8", lw=1, zorder=1))
    theta = np.linspace(0, 2*np.pi, 240)
    ax.add_patch(Polygon(project(ring(theta)), facecolor="#f0f5f9",
                         edgecolor="#aabac8", lw=1.2, zorder=2))

    # World axes share O. The solid angular-velocity vector lies on +z.
    for direction, label in [(np.array([1.65,0,0]), r"$x$"),
                             (np.array([0,1.65,0]), r"$y$")]:
        vector(np.zeros(3), direction, LIGHT, width=1.2, zorder=3)
        label_xy = project(1.08*direction)
        ax.text(*label_xy, label, color=GRAY, fontsize=13,
                ha="center", va="center")
    path([[0,0,-.42], [0,0,0]], color=LIGHT, lw=1.1,
         linestyle=(0,(3,3)), zorder=0)
    vector([0,0,0], [0,0,1.63], LIGHT, width=1.2, zorder=3)
    ax.text(*project([0,0,1.77]), r"$z$", color=GRAY, fontsize=13, ha="center")
    vector([0,0,0], [0,0,1.18], INK, width=2.3, zorder=6)
    column_vector_label(ax, (.15,1.02), r"\omega", [0,0,1], "rad/s", INK)

    # P's circular path and the body-fixed radius make the rotation tangible.
    path(ring(theta, radius=1), color="#becbd6", lw=1,
         linestyle=(0,(4,4)), zorder=3)
    path([np.zeros(3), p], color=GRAY, lw=1.8, zorder=4)
    radius_label = project(.5*p) + [0,-.13]
    ax.text(*radius_label, r"$1\,\mathrm{m}$", color=GRAY, fontsize=12, ha="center")
    arc = ring(np.linspace(np.deg2rad(155),np.deg2rad(275),70), radius=.64)
    path(arc, color=GRAY, lw=1.7, zorder=4)
    vector(arc[-4], arc[-1]-arc[-4], GRAY, width=1.7, zorder=5)

    ax.scatter(0,0,s=38,color=INK,zorder=7)
    ax.annotate(r"$O$ · world origin", (0,0), xytext=(-1.43,.66),
                color=INK, fontsize=12,
                arrowprops={"arrowstyle":"-", "color":GRAY, "lw":.9,
                            "connectionstyle":"angle,angleA=0,angleB=135,rad=4"})
    point_xy = project(p)
    vector(p, .9*velocity, MOTION, width=2.6, zorder=7)
    column_vector_label(ax, (1.30,.45), r"\dot{p}", [0,1,0], "m/s", MOTION)
    ax.text(1.30,.14,"Tangent velocity",color=MOTION,fontsize=11)

    # Both model frames have R = I at q = 0. Draw the complete attached triad;
    # y_B deliberately shares the direction of the longer velocity arrow.
    body_axes = [
        ([.40,0,0], r"$x_B$", (8,-13)),
        ([0,.40,0], r"$y_B$", (10,-13)),
        ([0,0,.55], r"$z_B$", (-12,7)),
    ]
    for (direction, label, offset), color in zip(body_axes, BODY_AXIS_COLORS):
        vector(p, direction, color, width=1.7, zorder=10)
        ax.annotate(label, project(p+direction), xytext=offset,
                    textcoords="offset points", color=color, fontsize=12,
                    zorder=11)
    ax.scatter(*point_xy,s=95,color=INK,edgecolors="white",linewidths=1.5,zorder=12)
    ax.annotate(r"$P$", point_xy, xytext=(-14,-19), textcoords="offset points",
                color=INK, fontsize=14)
    ax.annotate(r"Body frame $\{B\}$", point_xy, xytext=(.99,-.76),
                color=INK, fontsize=12,
                arrowprops={"arrowstyle":"-", "color":LIGHT, "lw":.9,
                            "shrinkA":3, "shrinkB":12})
    ax.annotate("Rigid body", (-.80,-.25), xytext=(-1.40,-.80),
                color=GRAY, fontsize=11,
                arrowprops={"arrowstyle":"-", "color":LIGHT, "lw":.9})
    ax.set(xlim=(-1.55,2.66),ylim=(-.91,1.7),aspect="equal")
    ax.axis("off")
    save(fig,"rotating-frame")


def displacement_figure():
    """A small, smoothly rounded body supports the displacement triangle."""
    center = np.array([1.40, .35, .62])

    def surface(directions):
        unit = np.asarray(directions, dtype=float)
        unit = unit / np.linalg.norm(unit, axis=-1, keepdims=True)
        # A gentle asymmetry avoids both a perfect ellipsoid and a faceted block.
        radius = 1 + .20*unit[...,0]*unit[...,1] + .14*unit[...,1]*(1-unit[...,2]**2)
        return center + radius[...,None]*unit*np.array([.70,.60,.28])

    p = surface([.60,-.55,.58])
    x = surface([-.65,.55,.80])
    r = x-p
    azimuth, elevation = np.deg2rad([-58, 28])
    right = np.array([-np.sin(azimuth), np.cos(azimuth), 0])
    up = np.array([-np.sin(elevation)*np.cos(azimuth),
                   -np.sin(elevation)*np.sin(azimuth), np.cos(elevation)])
    view = np.array([np.cos(elevation)*np.cos(azimuth),
                     np.cos(elevation)*np.sin(azimuth), np.sin(elevation)])

    def project(points):
        return np.asarray(points) @ np.stack([right, up]).T

    def vector(origin, displacement, color, width=2.2, zorder=5, shrink_b=0):
        arrow(ax, project(origin), project(displacement), color,
              width=width, scale=1, zorder=zorder, shrink_b=shrink_b)

    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    fig.subplots_adjust(left=.035, right=.98, top=.96, bottom=.12)

    # A softly shaded surface gives depth without decorative edges. Both marked
    # points are sampled from this same surface; O remains outside the body.
    latitude, longitude = np.meshgrid(np.linspace(0,np.pi,49),
                                      np.linspace(0,2*np.pi,97), indexing="ij")
    mesh = surface(np.stack([np.sin(latitude)*np.cos(longitude),
                             np.sin(latitude)*np.sin(longitude),
                             np.cos(latitude)], axis=-1))
    light = np.array([-.25,-.45,.86])
    light /= np.linalg.norm(light)
    faces = []
    for i in range(mesh.shape[0]-1):
        for j in range(mesh.shape[1]-1):
            face = np.array([mesh[i,j],mesh[i+1,j],mesh[i+1,j+1],mesh[i,j+1]])
            normal = np.cross(face[2]-face[0],face[3]-face[1])
            normal /= np.linalg.norm(normal)
            if normal @ view > 0:
                shade = .82 + .18*max(0,normal @ light)
                faces.append((face.mean(axis=0) @ view,project(face),
                              np.array([.89,.92,.95])*shade))
    faces.sort(key=lambda f:f[0])
    ax.add_collection(PolyCollection([f[1] for f in faces],
                                     facecolors=[f[2] for f in faces],
                                     edgecolors="face", linewidths=.25,
                                     antialiased=False, zorder=2))

    # World-position arrows start outside the solid. The relative arrow joins
    # two marked material points on its visible top face.
    vector(np.zeros(3), p, GRAY, width=2.1, shrink_b=6)
    vector(np.zeros(3), x, GRAY, width=2.1, shrink_b=6)
    vector(p, r, MOTION, width=2.8, zorder=7, shrink_b=6)
    ax.text(*(project(.45*p)+[0,-.12]), r"$p$", color=GRAY,
            fontsize=17, ha="center")
    ax.text(*(project(.45*x)+[-.12,.02]), r"$x$", color=GRAY,
            fontsize=17, ha="center")
    ax.text(*(project(p+.53*r)+[-.15,.02]), r"$r$", color=MOTION, fontsize=18)

    axes = [([.30,0,0], r"$x_B$", (5,-13)),
            ([0,.30,0], r"$y_B$", (9,0)),
            ([0,0,.32], r"$z_B$", (4,5))]
    for (direction, label, offset), color in zip(axes, BODY_AXIS_COLORS):
        vector(p, direction, color, width=1.4, zorder=8)
        ax.annotate(label, project(p+direction), xytext=offset,
                    textcoords="offset points", color=color, fontsize=11,
                    zorder=10)

    # Show the rotation around the world z-axis through O. The circular arrow
    # lies in an xy plane and uses the same 3D projection as the body.
    vector(np.zeros(3), [0,0,1.60], GRAY, width=1.4, zorder=5)
    ax.annotate(r"$z_W$", project([0,0,1.60]), xytext=(8,0),
                textcoords="offset points", color=GRAY, fontsize=14,
                va="center")
    angles = azimuth + np.deg2rad(np.linspace(155,405,140))
    arc = np.column_stack([.28*np.cos(angles), .28*np.sin(angles),
                           np.full_like(angles,1.06)])
    arc_xy = project(arc)
    front = np.cos(angles-azimuth) >= 0
    for mask, color, linestyle, order in [
        (~front, GRAY, (0,(3,3)), 4),
        (front, INK, "-", 6),
    ]:
        visible_arc = np.where(mask[:,None], arc_xy, np.nan)
        ax.plot(visible_arc[:,0], visible_arc[:,1], color=color,
                lw=1.6, linestyle=linestyle, zorder=order)
    vector(arc[-5], arc[-1]-arc[-5], INK, width=1.6, zorder=7)
    ax.text(.37,.88,r"$\omega$", color=INK, fontsize=17)

    for point, color in [(np.zeros(3), INK), (p, INK), (x, INK)]:
        ax.scatter(*project(point), s=88, color=color, edgecolors="white",
                   linewidths=1.4, zorder=10)
    ax.text(-.10,-.18,r"$O$", color=INK, fontsize=14)
    ax.text(-.10,-.34,"World origin", color=GRAY, fontsize=11)
    ax.annotate(r"$P$", project(p), xytext=(-14,-19),
                textcoords="offset points", color=INK, fontsize=14)
    ax.annotate(r"Point at $x$", project(x), xytext=(.66,1.14),
                color=INK, fontsize=13,
                arrowprops={"arrowstyle":"-", "color":LIGHT, "lw":1,
                            "shrinkB":8})
    ax.annotate("Rigid body", project(surface([-.55,-.8,.05])), xytext=(.86,-.18),
                color=INK, fontsize=13,
                arrowprops={"arrowstyle":"-", "color":"#8296a7", "lw":1})
    ax.annotate(r"Body frame $\{B\}$", project(p), xytext=(1.91,-.31),
                color=INK, fontsize=12,
                arrowprops={"arrowstyle":"-", "color":LIGHT, "lw":.9,
                            "shrinkA":3, "shrinkB":12})
    ax.set(xlim=(-.48,2.90), ylim=(-.55,1.54), aspect="equal")
    ax.axis("off")
    fig.text(.5,.055,r"Both points are fixed to the body. The arrow between them is $r=x-p$.",
             ha="center", color=INK, fontsize=12)
    save(fig, "body-displacement")


def chain_figure():
    """Oblique 3D view of two links with a 90-degree elbow bend."""
    shoulder = np.zeros(3)
    elbow = np.array([1.,0.,0.])
    ee = np.array([1.,1.,0.])
    azimuth, elevation = np.deg2rad([-58,28])
    right = np.array([-np.sin(azimuth),np.cos(azimuth),0])
    up = np.array([-np.sin(elevation)*np.cos(azimuth),
                   -np.sin(elevation)*np.sin(azimuth),np.cos(elevation)])
    view = np.array([np.cos(elevation)*np.cos(azimuth),
                     np.cos(elevation)*np.sin(azimuth),np.sin(elevation)])

    def project(points):
        return np.asarray(points) @ np.stack([right,up]).T

    def vector(origin, displacement, color, width=1.4, zorder=5):
        arrow(ax,project(origin),project(displacement),color,
              width=width,scale=1,zorder=zorder)

    fig, ax = plt.subplots(figsize=(8.6,5.4))
    fig.subplots_adjust(left=.035,right=.98,top=.97,bottom=.045)

    # Every joint rotates about a vertical axis; the arm itself lies in xy.
    for direction, label, offset in [
        ([2.18,0,0],r"$x_W$",(.08,-.04)),
        ([0,1.90,0],r"$y_W$",(.07,.06)),
        ([0,0,1.50],r"$z_W$",(.09,.02)),
    ]:
        vector(shoulder,direction,GRAY if direction[2] else LIGHT,
               width=1.2,zorder=5 if direction[2] else 0)
        ax.text(*(project(direction)+offset),label,color=GRAY,fontsize=13)
    vector(elbow,[0,0,1.20],GRAY,width=1.2,zorder=5)

    # Shaded link bars and short cylindrical hinges make the depth explicit.
    faces=[]
    light=np.array([-.2,-.5,.84])
    light/=np.linalg.norm(light)

    def face(vertices, color, edge="none"):
        vertices=np.asarray(vertices)
        normal=np.cross(vertices[1]-vertices[0],vertices[2]-vertices[0])
        normal/=np.linalg.norm(normal)
        if normal @ view > 0:
            shade=.77+.23*max(0,normal @ light)
            faces.append((vertices.mean(axis=0) @ view,project(vertices),
                          np.asarray(color)*shade,edge))

    def prism(outline, height, bottom, color, side_edges="none"):
        top=np.column_stack([outline,np.full(len(outline),height)])
        lower=np.column_stack([outline,np.full(len(outline),bottom)])
        face(top,color,"#92a3b2")
        for i in range(len(top)):
            j=(i+1)%len(top)
            face([top[i],lower[i],lower[j],top[j]],color,side_edges)

    for start,end,color in [(shoulder,elbow,[.86,.90,.94]),
                             (elbow,ee,[.79,.85,.91])]:
        direction=end[:2]-start[:2]
        side=np.array([-direction[1],direction[0]])*.065
        prism([start[:2]-side,end[:2]-side,end[:2]+side,start[:2]+side],
              -.025,-.12,color,"#92a3b2")
        midpoint=project((start+end)/2)
        projected=project(end-start)
        offset=np.array([projected[1],-projected[0]])
        offset*=.19/np.linalg.norm(offset)
        ax.text(*(midpoint+offset),r"$1\,\mathrm{m}$",ha="center",
                va="center",color=GRAY,fontsize=12)
    theta=np.linspace(0,2*np.pi,64,endpoint=False)
    for joint,radius in [(shoulder,.105),(elbow,.105),(ee,.065)]:
        outline=joint[:2]+radius*np.column_stack([np.cos(theta),np.sin(theta)])
        prism(outline,0,-.16,[.89,.92,.95])
    faces.sort(key=lambda f:f[0])
    ax.add_collection(PolyCollection([f[1] for f in faces],
                                     facecolors=[f[2] for f in faces],
                                     edgecolors=[f[3] for f in faces],
                                     linewidths=.7,zorder=2))

    for joint,height,start,end,speed,label_xy in [
        (shoulder,.95,155,405,"+1",(.25,1.08)),
        (elbow,.78,205,-45,"-1",(1.13,.62)),
    ]:
        angles=azimuth+np.deg2rad(np.linspace(start,end,140))
        arc=joint+np.column_stack([.22*np.cos(angles),.22*np.sin(angles),
                                   np.full_like(angles,height)])
        xy=project(arc)
        front=np.cos(angles-azimuth)>=0
        for mask,color,style,order in [(~front,GRAY,(0,(3,3)),4),
                                        (front,INK,"-",6)]:
            visible=np.where(mask[:,None],xy,np.nan)
            ax.plot(visible[:,0],visible[:,1],color=color,lw=1.6,
                    linestyle=style,zorder=order)
        vector(arc[-5],arc[-1]-arc[-5],INK,width=1.6,zorder=7)
        ax.text(*label_xy,f"${speed}\\,\\mathrm{{rad/s}}$",color=INK,fontsize=12)

    for point in (shoulder,elbow,ee):
        ax.scatter(*project(point),s=52,color=INK,edgecolors="white",
                   linewidths=1.1,zorder=8)
    for point,label,position,align in [
        (shoulder,"Shoulder\n(world origin)",(-.10,-.36),"right"),
        (elbow,"Elbow",(.84,-.65),"center"),
        (ee,"End effector",(1.86,-.29),"center"),
    ]:
        ax.annotate(label,project(point),xytext=position,ha=align,
                    color=INK,fontsize=11,
                    arrowprops={"arrowstyle":"-","color":LIGHT,"lw":.9,
                                "shrinkB":8})
    vector(ee,[0,.70,0],MOTION,width=2.4,zorder=7)
    ax.text(1.89,.51,r"$1\,\mathrm{m/s}$",color=MOTION,fontsize=12)
    ax.text(1.89,.35,r"along $+y$",color=MOTION,fontsize=11)
    ax.set(xlim=(-.72,2.65),ylim=(-.78,1.50),aspect="equal")
    ax.axis("off")
    save(fig,"twist-chain")


def field_figure(models):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5.5))
    fig.subplots_adjust(left=.075, right=.97, top=.79, bottom=.17, wspace=.22)
    fig.suptitle("The velocity field stays still. The material point accelerates.",
                 y=.98, fontsize=16, fontweight="normal", color=INK)
    handles = [
        Line2D([], [], color=GRAY, lw=1.4, label="Velocity at fixed positions"),
        Line2D([], [], color=BLUE, marker="o", lw=2, label="Velocity of P"),
        Line2D([], [], color=ORANGE, lw=2, label="Acceleration of P"),
    ]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.5,.92),
               ncol=3, frameon=False, fontsize=11)

    grid = np.linspace(-1, 1, 7)
    xx, yy = np.meshgrid(grid, grid)
    mask = (xx*xx + yy*yy < 1.35) & (xx*xx + yy*yy > .02)
    for ax, q, title in zip(axes, [0, np.pi/2], [r"$t=0$ s", r"$t=\pi/2$ s"]):
        state = sample(models, q)
        p = state["position_mujoco"][:2]
        velocity = state["mujoco_velocity"][3:5]
        acceleration = state["mujoco_acceleration"][3:5]
        ax.add_patch(Circle((0,0), 1.2, facecolor="#f4f7fa",
                            edgecolor=LIGHT, lw=1, zorder=0))
        ax.add_patch(Circle((0,0), 1, fill=False, edgecolor=LIGHT,
                            lw=1, linestyle=(0,(3,4)), zorder=1))
        ax.quiver(xx[mask], yy[mask], -yy[mask], xx[mask],
                  color=GRAY, alpha=.55, angles="xy", scale_units="xy",
                  scale=1/.42, width=.004, headwidth=3.5, zorder=2)
        # The radius below is fixed to the body and follows P.
        ax.plot([0,p[0]],[0,p[1]],color=LIGHT,lw=1.5,zorder=1)
        fixed_q = np.array([-.72, -.62])
        ax.scatter(*fixed_q, marker="s", s=65, facecolors="white",
                   edgecolors=INK, linewidths=1.6, zorder=6)
        ax.annotate("Q", fixed_q, xytext=(-17,-17), textcoords="offset points", color=INK)
        arrow(ax, fixed_q, [-fixed_q[1], fixed_q[0]], GRAY, 1.7)
        ax.scatter(0,0,s=24,color=INK,zorder=7)
        ax.annotate("O",(0,0),xytext=(7,-15),textcoords="offset points",color=INK)
        arrow(ax, p, velocity, BLUE)
        arrow(ax, p, acceleration, ORANGE)
        ax.scatter(*p,s=85,color=BLUE,edgecolors="white",linewidths=1.5,zorder=8)
        ax.annotate("P",p,xytext=(10,8),textcoords="offset points",color=BLUE)
        ax.set(xlim=(-1.4,1.5),ylim=(-1.4,1.5),xticks=[-1,0,1],yticks=[-1,0,1],
               xlabel="x (m)",ylabel="y (m)",aspect="equal",title=title)
        ax.spines[["top","right"]].set_visible(False)
        for spine in ("bottom","left"):
            ax.spines[spine].set_color(LIGHT)
        ax.tick_params(colors=GRAY)
    fig.text(.5,.04,"Q stays at a fixed location; P follows the body.  OP = 1 m, angular speed = 1 rad/s.",
             ha="center",color=GRAY,fontsize=11)
    save(fig,"velocity-field-snapshots")


def library_figure(models):
    angles = np.linspace(0, 2*np.pi, 181)
    # Every curve below is sampled from an API, not inserted analytically.
    states = [sample(models, q) for q in angles]
    values = {key: np.stack([s[key] for s in states]) for key in states[0]}
    degrees = np.degrees(angles)
    fig, axes = plt.subplots(2, 1, figsize=(9, 7.1))
    fig.subplots_adjust(left=.13,right=.975,top=.81,bottom=.105,hspace=.8)
    fig.suptitle("Same motion. Different API outputs.",x=.13,y=.98,ha="left",
                 fontsize=19,fontweight="normal",color=INK)
    fig.text(.13,.925,"A frame 1 m from a fixed axis, rotating at 1 rad/s. All components use world axes.",
             fontsize=11,color=GRAY)

    specs = [
        (axes[0], 4, "mujoco_velocity", "pinocchio_lwa_velocity",
         "pinocchio_world_velocity",
         "Velocity: choosing LWA makes the outputs agree",
         "Linear velocity, y (m/s)", "Pinocchio · LWA", "Pinocchio · WORLD"),
        (axes[1], 3, "mujoco_acceleration", "pinocchio_lwa_classical_acceleration",
         "pinocchio_lwa_spatial_acceleration",
         "Acceleration: LWA alone is not enough",
         "Linear acceleration, x (m/s²)", "Pinocchio · classical LWA",
         "Pinocchio · spatial LWA"),
    ]
    for ax, i, mjkey, pinkey, zero_key, title, ylabel, pinlabel, zerolabel in specs:
        ax.plot(degrees,values[zero_key][:,i],color=GRAY,lw=1.7,
                linestyle=(0,(5,4)),label=zerolabel,zorder=1)
        ax.plot(degrees,values[pinkey][:,i],color=BLUE,lw=2.2,
                label=pinlabel,zorder=2)
        ax.plot(degrees[::10],values[mjkey][::10,i],linestyle="none",
                marker="o",markersize=6,markeredgewidth=1.6,
                markerfacecolor="white",markeredgecolor=ORANGE,
                label="MuJoCo · world-oriented",zorder=3)
        ax.set(xlim=(-5,365),ylim=(-1.22,1.22),xticks=[0,90,180,270,360],
               yticks=[-1,0,1],xlabel="Rotation angle (degrees)",ylabel=ylabel)
        ax.set_title(title,loc="left",pad=38,fontsize=13,color=INK)
        # Legends stay outside the data region so coincidences remain visible.
        handles,labels=ax.get_legend_handles_labels()
        order=[2,1,0]
        ax.legend([handles[j] for j in order],[labels[j] for j in order],
                  loc="lower left",bbox_to_anchor=(0,1.015),ncol=3,
                  borderaxespad=0,frameon=False,fontsize=9.5,
                  handlelength=2,columnspacing=1.2)
        ax.grid(axis="y",color="#e6ebef",lw=.8)
        ax.spines[["top","right"]].set_visible(False)
        for spine in ("bottom","left"):
            ax.spines[spine].set_color(LIGHT)
        ax.tick_params(colors=GRAY)
    save(fig,"mujoco-pinocchio-comparison")


def main():
    plt.rcParams.update({
        "font.family":"serif", "font.serif":["STIXGeneral"], "font.size":12,
        "mathtext.fontset":"cm",
        "text.color":INK,"axes.labelcolor":INK,
        # Embed glyph outlines: browser font substitution otherwise displaces
        # mathtext accents and changes the spacing of SVG labels.
        "svg.fonttype":"path","svg.hashsalt":"featherstone-blog",
    })
    models = make_models()
    verify(models)
    setup_figure(models)
    displacement_figure()
    chain_figure()
    field_figure(models)
    library_figure(models)
    package_example()
    print(f"Saved SVG and PNG figures in {OUTPUT}")


if __name__ == "__main__":
    main()
