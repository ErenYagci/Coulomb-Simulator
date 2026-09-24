import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from physics import PointCharge, calculate_net_force

class InteractiveCoulombSimulator:
    def __init__(self):
        self.sources: list[PointCharge] = []
        self.test_charge = PointCharge(charge=1e-6, x=0.0, y=0.0, label="Test")
        self.default_source_magnitude = 5e-6  # 5 microcoulombs

        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("key_press_event", self.on_key)

        # Görünüm sınırlarını başlangıçta bir kez belirle
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_xlabel("X (meters)")
        self.ax.set_ylabel("Y (meters)")

    def on_click(self, event):
        # Eksen dışındaki tıklamaları veya toolbar araçları (Zoom/Pan) aktifken olan tıklamaları yoksay
        if event.inaxes != self.ax:
            return
        if self.fig.canvas.toolbar.mode != "":
            return

        x, y = round(event.xdata, 2), round(event.ydata, 2)

        # Test yükünü taşı (Orta tık veya Shift + Sol tık)
        if event.button == 2 or (event.button == 1 and event.key == "shift"):
            self.test_charge.x = x
            self.test_charge.y = y
        # Pozitif yük ekle (+) (Sol tık)
        elif event.button == 1:
            idx = len(self.sources) + 1
            self.sources.append(PointCharge(self.default_source_magnitude, x, y, label=f"q{idx}"))
        # Negatif yük ekle (-) (Sağ tık)
        elif event.button == 3:
            idx = len(self.sources) + 1
            self.sources.append(PointCharge(-self.default_source_magnitude, x, y, label=f"q{idx}"))

        self.render()

    def on_key(self, event):
        # 'C' tuşuna basıldığında kaynak yükleri temizle
        if event.key and event.key.lower() == "c":
            self.sources.clear()
            self.render()

    def render(self):
        # Eksen sınırlarını (xlim/ylim) ve toolbar geçmişini korumak için 
        # ax.clear() yerine sadece çizilmiş nesneleri (artists) temizliyoruz
        while self.ax.collections:
            self.ax.collections[0].remove()
        while self.ax.texts:
            self.ax.texts[0].remove()
        while self.ax.lines:
            self.ax.lines[0].remove()
        while self.ax.patches:
            self.ax.patches[0].remove()

        # Izgara ve referans eksen çizgileri
        self.ax.axhline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
        self.ax.axvline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
        self.ax.grid(True, linestyle=":", alpha=0.6)

        # Kaynak yükleri çiz
        for q in self.sources:
            color = "crimson" if q.charge > 0 else "royalblue"
            self.ax.scatter(q.x, q.y, color=color, s=150, zorder=3)
            sign = "+" if q.charge > 0 else ""
            self.ax.annotate(f"{q.label} ({sign}{q.charge*1e6:.0f}µC)", 
                             (q.x, q.y), textcoords="offset points", xytext=(8, 8), fontweight="bold")

        # Test yükünü çiz
        self.ax.scatter(self.test_charge.x, self.test_charge.y, color="gold", marker="s", 
                        s=160, edgecolors="black", linewidth=1.5, zorder=4, label="Test Charge (1µC)")

        # Bileşke kuvvet vektörünü hesapla ve çiz
        if self.sources:
            fx, fy, mag, angle = calculate_net_force(self.sources, self.test_charge)
            if mag > 0:
                scale_len = 0.8
                dx = (fx / mag) * scale_len
                dy = (fy / mag) * scale_len
                self.ax.quiver(self.test_charge.x, self.test_charge.y, dx, dy, 
                               angles="xy", scale_units="xy", scale=1, color="black", 
                               width=0.007, zorder=5, label="Net Force Vector")

            status_text = (f"Sources: {len(self.sources)} | "
                           f"Fx: {fx:+.2e} N | Fy: {fy:+.2e} N | "
                           f"|F|: {mag:.2e} N | Angle: {angle:.1f}°")
        else:
            status_text = "Click anywhere to place charges."

        self.ax.set_title(f"Interactive Coulomb's Law Simulator\n{status_text}", fontsize=11)

        # Bilgilendirme kutucuğu
        help_str = "Controls:\n• Left-Click: +5µC\n• Right-Click: -5µC\n• Shift+Click: Move Test Charge\n• 'C' Key: Clear Canvas"
        self.ax.text(0.02, 0.02, help_str, transform=self.ax.transAxes, fontsize=8,
                     verticalalignment="bottom", bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.85))

        self.ax.legend(loc="upper right", fontsize=8)
        self.fig.canvas.draw_idle()

    def run(self):
        self.render()
        plt.show()