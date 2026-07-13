"""Make figure backgrounds transparent via border flood-fill.
Removes near-white background connected to the image border while preserving
interior white (text, markers, heatmap cells). Used on all final figures."""
import os, sys, numpy as np
from PIL import Image
from scipy import ndimage

def transparent_bg(path, thresh=245):
    im = Image.open(path).convert("RGBA")
    a = np.array(im); rgb = a[:, :, :3]
    white = (rgb >= thresh).all(axis=2)
    lab, n = ndimage.label(white)
    border = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
    border.discard(0)
    a[np.isin(lab, list(border)), 3] = 0
    Image.fromarray(a).save(path)
    return int(np.isin(lab, list(border)).sum())

if __name__ == "__main__":
    figdir = sys.argv[1] if len(sys.argv) > 1 else "paper/figures"
    for f in sorted(os.listdir(figdir)):
        if f.endswith(".png"):
            n = transparent_bg(os.path.join(figdir, f))
            print(f"{f}: {n} px -> transparent")
