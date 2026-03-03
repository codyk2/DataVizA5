"""
Build earnest and deceptive OECD GHG visualizations.
Reads data/ghg_emissions.csv, produces a2_earnest.png and a2_deceptive.png.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "ghg_emissions.csv")
COUNTRIES = ["United States", "United Kingdom", "Germany", "Japan", "Canada"]


def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df[df["country"].isin(COUNTRIES) & (df["year"] >= 1990) & (df["year"] <= 2019)]
    return df


def index_1990(df):
    """Index emissions to 1990 = 100 per country."""
    out = []
    for country in COUNTRIES:
        sub = df[df["country"] == country].sort_values("year")
        base = sub[sub["year"] == 1990]["emissions_mt"].values
        if len(base) == 0:
            continue
        base = base[0]
        sub = sub.copy()
        sub["index"] = (sub["emissions_mt"] / base) * 100
        out.append(sub)
    return pd.concat(out, ignore_index=True)


def build_earnest(df_indexed):
    """Earnest chart: 5 countries, 1990–2019, index 1990=100, full y-axis."""
    fig, ax = plt.subplots(figsize=(10, 6))
    for country in COUNTRIES:
        sub = df_indexed[df_indexed["country"] == country].sort_values("year")
        if sub.empty:
            continue
        ax.plot(sub["year"], sub["index"], label=country, linewidth=2)
    # UK reduction callout (compute from data)
    uk = df_indexed[df_indexed["country"] == "United Kingdom"].sort_values("year")
    if not uk.empty and 2019 in uk["year"].values:
        idx_2019 = uk[uk["year"] == 2019]["index"].values[0]
        pct = round(100 - idx_2019)
        ax.annotate(
            f"UK emissions reduced by ~{pct}% since 1990.",
            xy=(2019, idx_2019),
            xytext=(2005, 75),
            fontsize=9,
            arrowprops=dict(arrowstyle="->", color="gray", lw=1),
        )
    ax.set_xlim(1989, 2020)
    ymax = df_indexed["index"].max()
    ax.set_ylim(0, max(120, min(140, int(ymax) + 15)))
    ax.set_xlabel("Year")
    ax.set_ylabel("Emissions index (1990 = 100)")
    ax.set_title(
        "How Have Greenhouse Gas Emissions Changed in Major OECD Countries Since 1990?",
        fontsize=12,
    )
    fig.text(0.5, 0.02, "Total greenhouse gas emissions (CO₂ equivalent), all sectors, 1990–2019. Source: OECD.", ha="center", fontsize=9, style="italic")
    ax.legend(loc="upper right", frameon=True)
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(1990, 2020, 5))
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    out_path = os.path.join(os.path.dirname(__file__), "a2_earnest.png")
    fig.savefig(out_path, dpi=150, bbox_inches="tight", pad_inches=0.15)
    plt.close()
    print(f"Saved {out_path}")


def build_deceptive(df):
    """Deceptive chart: US only, 2010–2019, raw Mt, truncated y-axis, 3-year moving average."""
    us = df[(df["country"] == "United States") & (df["year"] >= 2010) & (df["year"] <= 2019)].sort_values("year")
    if us.empty:
        return
    us = us.copy()
    us["ma3"] = us["emissions_mt"].rolling(3, center=True, min_periods=1).mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(us["year"], us["emissions_mt"], color="steelblue", linewidth=1.5, alpha=0.7, label="Annual")
    ax.plot(us["year"], us["ma3"], color="darkblue", linewidth=2.5, label="3-year moving average")
    ax.annotate(
        "Emissions fluctuate within a narrow band.",
        xy=(2015, us["emissions_mt"].mean()),
        xytext=(2012, 6650),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="gray", lw=1),
    )
    ax.set_ylim(6400, 7000)  # Truncated range so variation appears small (data ~6522–6885)
    ax.set_xlim(2009.5, 2019.5)
    ax.set_xlabel("Year")
    ax.set_ylabel("Million tonnes CO₂ eq.")
    ax.set_title("Have U.S. Emissions Stabilized in the Past Decade?", fontsize=12)
    fig.text(0.5, 0.02, "Total greenhouse gas emissions, 2010–2019. Source: OECD.", ha="center", fontsize=9, style="italic")
    ax.legend(loc="upper right", frameon=True)
    ax.grid(True, alpha=0.3)
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    out_path = os.path.join(os.path.dirname(__file__), "a2_deceptive.png")
    fig.savefig(out_path, dpi=150, bbox_inches="tight", pad_inches=0.15)
    plt.close()
    print(f"Saved {out_path}")


def main():
    df = load_data()
    df_indexed = index_1990(df)
    build_earnest(df_indexed)
    build_deceptive(df)


if __name__ == "__main__":
    main()
