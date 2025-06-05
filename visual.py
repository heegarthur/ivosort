import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from math import floor
from matplotlib.animation import FuncAnimation

def tier_cascade_sort_visual_full(data, map_grootte=6, laag_pct=0.3, mid_pct=0.4, hoog_pct=0.3):
    def split_map(lst):
        lst.sort()
        n = len(lst)
        l = floor(n * laag_pct)
        m = floor(n * mid_pct)
        h = n - l - m
        return lst[:l], lst[l:l+m], lst[l+m:]

    kleine_mappen, midden_mappen, grote_mappen = [], [], []
    buffer = []
    snapshots = []  
    buffers_snapshots = [] 
    
    for getal in data:
        buffer.append(getal)
        buffers_snapshots.append(buffer[:])  
        if len(buffer) >= map_grootte:
            klein, midden, groot = split_map(buffer)
            kleine_mappen.append(klein)
            midden_mappen.append(midden)
            grote_mappen.append(groot)
            snapshots.append((klein[:], midden[:], groot[:]))
            buffer = []

    if buffer:
        klein, midden, groot = split_map(buffer)
        kleine_mappen.append(klein)
        midden_mappen.append(midden)
        grote_mappen.append(groot)
        snapshots.append((klein[:], midden[:], groot[:]))

    alles = []
    cumulatief_snapshots = []
    for m in kleine_mappen + midden_mappen + grote_mappen:
        alles.extend(m)
        cumulatief_snapshots.append(sorted(alles[:]))  

    def is_sorted(lst):
        return all(lst[i] <= lst[i+1] for i in range(len(lst) - 1))

    if not is_sorted(alles):
        for i in range(1, len(alles)):
            key = alles[i]
            j = i - 1
            while j >= 0 and alles[j] > key:
                alles[j + 1] = alles[j]
                j -= 1
            alles[j + 1] = key
        cumulatief_snapshots.append(alles[:])  

    return alles, snapshots, buffers_snapshots, cumulatief_snapshots

def animate_full_process(snapshots, buffers_snapshots, cumulatief_snapshots):
    colors = ['#3498db', '#2ecc71', '#e74c3c']  
    labels = ['little', 'mid', 'big']

    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(12, 5), gridspec_kw={'height_ratios':[3, 1]})
    
    ax_top.set_xlim(0, 30)
    ax_top.set_ylim(0, 1)
    ax_top.axis('off')
    
    ax_bottom.set_xlim(0, 30)
    ax_bottom.set_ylim(0, 1)
    ax_bottom.axis('off')
    
    total_steps = len(buffers_snapshots) + len(snapshots) + len(cumulatief_snapshots)

    def draw_buffer(buffer):
        ax_top.clear()
        ax_top.set_xlim(0, 30)
        ax_top.set_ylim(0, 1)
        ax_top.axis('off')
        ax_top.set_title('Buffer vullen')

        x_pos = 0
        width = 1
        height = 0.6
        for num in buffer:
            rect = patches.Rectangle((x_pos, 0.2), width, height, linewidth=1, edgecolor='black', facecolor='#34495e')
            ax_top.add_patch(rect)
            ax_top.text(x_pos + 0.5, 0.5, str(num), ha='center', va='center', fontsize=10, color='white')
            x_pos += width

    def draw_split(klein, midden, groot, step):
        ax_top.clear()
        ax_top.set_xlim(0, 30)
        ax_top.set_ylim(0, 1)
        ax_top.axis('off')
        ax_top.set_title(f'Splits {step + 1} - {len(snapshots)}')

        x_pos = 0
        width = 1
        height = 0.6
        for j, groep in enumerate([klein, midden, groot]):
            for num in groep:
                rect = patches.Rectangle((x_pos, 0.2), width, height, linewidth=1, edgecolor='black', facecolor=colors[j])
                ax_top.add_patch(rect)
                ax_top.text(x_pos + 0.5, 0.5, str(num), ha='center', va='center', fontsize=10, color='white')
                x_pos += width

    def draw_cumulatief(alles, step, final=False):
        ax_bottom.clear()
        ax_bottom.set_xlim(0, 30)
        ax_bottom.set_ylim(0, 1)
        ax_bottom.axis('off')
        titel = f'step {step + 1} - {len(cumulatief_snapshots)}'
        if final:
            titel += " (fully sorted)"
        ax_bottom.set_title(titel)

        x_pos = 0
        width = 1
        height = 0.6
        for num in alles:
            rect = patches.Rectangle((x_pos, 0.2), width, height, linewidth=1, edgecolor='black', facecolor='#9b59b6')
            ax_bottom.add_patch(rect)
            ax_bottom.text(x_pos + 0.5, 0.5, str(num), ha='center', va='center', fontsize=10, color='white')
            x_pos += width

    def update(frame):
        if frame < len(buffers_snapshots):
            draw_buffer(buffers_snapshots[frame])
            ax_bottom.clear()
            ax_bottom.axis('off')
            ax_bottom.set_title('processing result')
        elif frame < len(buffers_snapshots) + len(snapshots):
            idx = frame - len(buffers_snapshots)
            klein, midden, groot = snapshots[idx]
            draw_split(klein, midden, groot, idx)
            ax_bottom.clear()
            ax_bottom.axis('off')
            ax_bottom.set_title('processing result')
        else:
            idx = frame - len(buffers_snapshots) - len(snapshots)
            if idx >= len(cumulatief_snapshots):
                idx = len(cumulatief_snapshots) - 1
            final = (idx == len(cumulatief_snapshots) - 1)
            draw_cumulatief(cumulatief_snapshots[idx], idx, final=final)

        return []

    ani = FuncAnimation(fig, update, frames=total_steps, interval=1, blit=False, repeat=False)
    plt.tight_layout()
    plt.show()

random.seed(420)
lijst = random.sample(range(1, 1000), 200)
gesorteerd, snaps, buffers_snapshots, cumulatief_snapshots = tier_cascade_sort_visual_full(lijst)

print("Original:", lijst)
print("sorted:", gesorteerd)
animate_full_process(snaps, buffers_snapshots, cumulatief_snapshots)
