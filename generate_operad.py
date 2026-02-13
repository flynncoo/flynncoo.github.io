import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_little_cubes_composition():
    line_color = "#ffffff"
    line_width = 1.2

    fig, ax = plt.subplots(1, 1, figsize=(3, 10), dpi=300)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_aspect('equal')

    def draw_config(ox, oy, size, cubes, labels=None):
        rect = patches.Rectangle((ox, oy), size, size,
                                 linewidth=line_width, edgecolor=line_color, facecolor="none")
        ax.add_patch(rect)
        for i, (cx, cy, cw, ch) in enumerate(cubes):
            abs_x = ox + cx * size
            abs_y = oy + cy * size
            abs_w, abs_h = cw * size, ch * size
            cube = patches.Rectangle((abs_x, abs_y), abs_w, abs_h,
                                     linewidth=line_width, edgecolor=line_color,
                                     facecolor="none")
            ax.add_patch(cube)
            if labels and i < len(labels):
                ax.text(abs_x + abs_w / 2, abs_y + abs_h / 2, labels[i],
                        fontsize=8, ha='center', va='center',
                        color=line_color, fontfamily='serif')

    # Configs
    config_A = [
        (0.08, 0.6, 0.22, 0.22),
        (0.38, 0.28, 0.32, 0.32),
        (0.76, 0.06, 0.16, 0.16),
    ]
    config_B = [
        (0.15, 0.08, 0.65, 0.32),
        (0.15, 0.55, 0.65, 0.32),
    ]

    # Composite: plug B into slot 1 of A
    target = config_A[1]
    tx, ty, tw, th = target
    composite = []
    for i, c in enumerate(config_A):
        if i == 1:
            for sx, sy, sw, sh in config_B:
                composite.append((tx + sx * tw, ty + sy * th, sw * tw, sh * th))
        else:
            composite.append(c)

    # Vertical layout: top to bottom with gaps for labels
    # Config A at top — label inner cubes 1, 2, 3
    draw_config(0, 9, 3, config_A, labels=["1", "2", "3"])

    # circ_2 label (in the gap between A and B)
    ax.text(1.5, 8.25, r"$\circ_2$", fontsize=18, ha='center', va='center',
            color=line_color, fontfamily='serif')

    # Config B in middle — label inner cubes 1, 2
    draw_config(0, 4.5, 3, config_B, labels=["1", "2"])

    # = label (in the gap between B and result)
    ax.text(1.5, 3.75, r"$=$", fontsize=18, ha='center', va='center',
            color=line_color, fontfamily='serif')

    # Composite at bottom — relabelled sequentially
    draw_config(0, 0, 3, composite, labels=["1", "2", "3", "4"])

    plt.tight_layout(pad=0)
    plt.savefig("little_cubes_composition.svg", transparent=True, bbox_inches='tight', pad_inches=0.1)
    # Also save a preview PNG with dark background to verify
    fig.patch.set_facecolor("#312450")
    fig.patch.set_alpha(1)
    plt.savefig("little_cubes_preview.png", facecolor="#312450", bbox_inches='tight', pad_inches=0.1)
    plt.close()

if __name__ == "__main__":
    draw_little_cubes_composition()
