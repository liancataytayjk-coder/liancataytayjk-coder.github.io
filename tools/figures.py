"""Black-and-white journal figures for every portfolio project.

Usage: python3 figures.py <repos_dir> <site_dir>
Writes PNGs to <site>/assets/figures/ and a manifest (figures.json) of
captions and source notes that build.py uses.
"""
import json
import sys
import warnings
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter, PercentFormatter  # noqa: E402

warnings.filterwarnings("ignore")
REPOS, SITE = Path(sys.argv[1]), Path(sys.argv[2])
OUT = SITE / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

PAPER, INK, DARK, MID, LIGHT, FAINT = "#f8f9fb", "#111318", "#474b52", "#8a8f97", "#bfc3c9", "#e3e6ea"
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "Tinos", "DejaVu Serif"],
    "font.size": 12.5,
    "axes.edgecolor": INK, "axes.linewidth": 0.8, "axes.labelcolor": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.facecolor": PAPER, "figure.facecolor": PAPER, "savefig.facecolor": PAPER,
    "xtick.color": INK, "ytick.color": INK, "xtick.direction": "out", "ytick.direction": "out",
    "axes.grid": False, "legend.frameon": False, "legend.fontsize": 11.5,
    "hatch.color": INK, "hatch.linewidth": 0.6,
})

MANIFEST = {}
thousands = FuncFormatter(lambda v, _: f"{v:,.0f}")
millions = FuncFormatter(lambda v, _: f"${v / 1e6:,.0f}M")


def new(w=8, h=4.5):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    fig.subplots_adjust(left=0.1, right=0.96, top=0.95, bottom=0.13)
    return fig, ax


def save(fig, slug, n, title, note):
    name = f"{slug}-{n}.png"
    fig.savefig(OUT / name)
    plt.close(fig)
    MANIFEST.setdefault(slug, []).append({"src": f"assets/figures/{name}", "title": title, "note": note})


def hbar(ax, labels, values, fmt, colors=None, hatches=None, xmax=None):
    y = np.arange(len(labels))
    bars = ax.barh(y, values, color=colors or DARK, height=0.62, edgecolor=INK, linewidth=0.6)
    if hatches:
        for b, h in zip(bars, hatches):
            b.set_hatch(h)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    top = xmax or max(values) * 1.18
    ax.set_xlim(0, top)
    for yi, v in zip(y, values):
        ax.text(v + top * 0.012, yi, fmt(v), va="center", fontsize=11.5)
    return bars


def date_axis(ax):
    loc = matplotlib.dates.AutoDateLocator(minticks=4, maxticks=7)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b %Y"))


def year_axis(ax, step=None):
    if step:
        ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(step))


# ------------------------------------------------------------- Sentiment
slug = "customer-sentiment-intelligence-dashboard"
sd = pd.read_csv(REPOS / "customer-sentiment-intelligence-dashboard/data/processed/powerbi_ready_dataset.csv")
share = sd.sentiment.value_counts(normalize=True).reindex(["Positive", "Neutral", "Negative"]) * 100
fig, ax = new(8, 3.4)
fig.subplots_adjust(left=0.14, bottom=0.18)
hbar(ax, share.index.tolist(), share.values.tolist(), lambda v: f"{v:.1f}%", colors=[INK, LIGHT, PAPER],
     hatches=["", "", "////"], xmax=60)
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_xlabel("Share of 500 reviews")
save(fig, slug, 1, "Sentiment of 500 multilingual customer reviews",
     "Net Promoter Score of 30. Source: Customer Sentiment Intelligence Dashboard repository.")

themes = sd.Themes.dropna().str.split(", ").explode().value_counts().head(8)
fig, ax = new(8, 4.2)
fig.subplots_adjust(left=0.2)
hbar(ax, themes.index.tolist(), themes.values.tolist(), lambda v: f"{v:,.0f}", colors=DARK)
ax.set_xlabel("Reviews mentioning the theme")
save(fig, slug, 2, "Most frequently mentioned themes in customer reviews",
     "A review can mention several themes. Source: Customer Sentiment Intelligence Dashboard repository.")

lang = sd.groupby("language").sentiment.apply(lambda s: (s == "Negative").mean() * 100).sort_values(ascending=False)
n_lang = sd.language.value_counts()
fig, ax = new(8, 3.2)
fig.subplots_adjust(left=0.2, bottom=0.2)
hbar(ax, [f"{l} (n={n_lang[l]})" for l in lang.index], lang.values.tolist(), lambda v: f"{v:.1f}%", colors=MID, xmax=max(lang.max() * 1.2, 30))
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_xlabel("Share of reviews that are negative")
save(fig, slug, 3, "Negative sentiment by review language",
     "Source: Customer Sentiment Intelligence Dashboard repository.")

# ------------------------------------------------------------- Retention
slug = "ecommerce-customer-retention-analytics"
RD = REPOS / "ecommerce-customer-retention-analytics/ecommerce-customer-retention-analytics/data/processed/dashboard"
rt = pd.read_csv(RD / "dash_revenue_trend.csv")
rt = rt[rt.total_orders >= 100]
rt = rt[rt.order_month >= "2017-01"]
rt["order_month"] = pd.to_datetime(rt.order_month)
fig, ax = new()
ax.plot(rt.order_month, rt.total_revenue, color=INK, linewidth=1.4, marker="o", markersize=3.5)
ax.set_ylim(0, None)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v / 1e6:,.1f}M"))
ax.set_ylabel("Monthly revenue")
date_axis(ax)
save(fig, slug, 1, "Monthly marketplace revenue, 2017 to 2018",
     "Months with fewer than 100 orders are omitted. Olist Brazilian e-commerce data. Source: E-commerce Customer Retention Analytics repository.")

seg = pd.read_csv(RD / "dash_segment_profile.csv").sort_values("revenue_share_pct", ascending=False)
fig, ax = new()
x = np.arange(len(seg))
ax.bar(x - 0.2, seg.customer_share_pct, 0.38, color=LIGHT, edgecolor=INK, linewidth=0.6, label="Share of customers")
ax.bar(x + 0.2, seg.revenue_share_pct, 0.38, color=INK, edgecolor=INK, linewidth=0.6, label="Share of revenue")
ax.set_xticks(x, seg.segment, rotation=0, fontsize=11)
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.legend(loc="upper right")
save(fig, slug, 2, "Customer and revenue share by RFM segment",
     "Source: E-commerce Customer Retention Analytics repository.")

coh = pd.read_csv(RD / "dash_cohort_long.csv")
coh = coh[(coh.cohort_index >= 1) & (coh.cohort_index <= 12)]
curve = coh.groupby("cohort_index").apply(lambda g: g.active_customers.sum() / g.cohort_size.sum() * 100)
fig, ax = new()
ax.plot(curve.index, curve.values, color=INK, linewidth=1.4, marker="o", markersize=5, markerfacecolor=PAPER)
ax.set_xticks(range(1, 13))
ax.set_xlabel("Months since first purchase")
ax.set_ylim(0, max(curve.max() * 1.3, 1))
ax.yaxis.set_major_formatter(PercentFormatter(decimals=1))
ax.set_ylabel("Customers purchasing again")
save(fig, slug, 3, "Repeat purchasing by months since first purchase, all monthly cohorts",
     "Very few customers return after their first order, which drives the 59.1% churn rate. "
     "Source: E-commerce Customer Retention Analytics repository.")

# ------------------------------------------------------------- Ads
slug = "ecommerce-marketplace-ads-performance-dashboard"
AD = REPOS / "ecommerce-marketplace-ads-performance-dashboard/data_processed"
pp = pd.read_csv(AD / "platform_performance_summary.csv").sort_values("ROAS", ascending=False)
fig, ax = new(8, 3.4)
fig.subplots_adjust(left=0.16, bottom=0.18)
hbar(ax, pp.platform.tolist(), pp.ROAS.tolist(), lambda v: f"{v:.2f}", colors=DARK, xmax=8.2)
ax.set_xlabel("Return on ad spend (ad revenue per dollar of spend)")
save(fig, slug, 1, "Return on ad spend by marketplace platform",
     "Simulated ad exports across four platforms. Source: eCommerce Marketplace Ads Performance Dashboard repository.")

ba = pd.read_csv(AD / "budget_allocation_summary.csv").recommended_budget_action.value_counts()
fig, ax = new(8, 3.6)
fig.subplots_adjust(left=0.2, bottom=0.17)
hbar(ax, ba.index.tolist(), ba.values.tolist(), lambda v: f"{v:,.0f}",
     colors=[LIGHT if i == "Fix Data First" else DARK for i in ba.index],
     hatches=["////" if i == "Fix Data First" else "" for i in ba.index])
ax.xaxis.set_major_formatter(thousands)
ax.set_xlabel("Campaign and SKU rows")
save(fig, slug, 2, "Recommended budget action for each campaign and SKU",
     "Rows with unreliable KPIs are routed to data fixes before any budget change. Source: eCommerce Marketplace Ads Performance Dashboard repository.")

# ------------------------------------------------------------- FP&A
slug = "fpa-revenue-cost-expense-forecasting-dashboard"
FD = REPOS / "fpa-revenue-cost-expense-forecasting-dashboard/data_processed"
rv = pd.read_csv(FD / "revenue_cost_margin_summary.csv", parse_dates=["month"]).groupby("month").revenue.sum()
sc = pd.read_csv(FD / "forecast_scenario_output.csv", parse_dates=["forecast_month"])
sc = sc.groupby(["scenario", "forecast_month"]).forecasted_revenue.sum().unstack(0)
fig, ax = new()
ax.plot(rv.index, rv.values, color=INK, linewidth=1.4, label="Actual")
styles = {"Upside": (MID, (0, (1, 1.5))), "Base": (INK, (0, (4, 2))), "Conservative": (MID, (0, (6, 2, 1, 2)))}
for name, (c, ls) in styles.items():
    ax.plot(sc.index, sc[name], color=c, linewidth=1.3, linestyle=ls, label=f"{name} forecast")
ax.axvline(sc.index.min(), color=MID, linewidth=0.6)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v / 1e6:,.0f}M"))
ax.set_ylabel("Monthly revenue")
ax.legend(loc="upper left", ncol=2)
ax.set_ylim(0, max(rv.max(), sc.max().max()) * 1.25)
ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(4e6))
date_axis(ax)
save(fig, slug, 1, "Monthly revenue, 2023 to 2025, with 2026 forecast scenarios",
     "Synthetic financials. Source: FP&A Revenue, Cost & Expense Forecasting Dashboard repository.")

gm = pd.read_csv(FD / "revenue_cost_margin_summary.csv").groupby("business_unit")[["revenue", "gross_margin"]].sum()
gm = (gm.gross_margin / gm.revenue * 100).sort_values(ascending=False)
fig, ax = new(8, 3.8)
fig.subplots_adjust(left=0.3, bottom=0.16)
hbar(ax, gm.index.tolist(), gm.values.tolist(), lambda v: f"{v:.1f}%", colors=DARK, xmax=70)
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_xlabel("Gross margin, 2023 to 2025")
save(fig, slug, 2, "Gross margin by business unit",
     "Overall gross margin 50.8%. Source: FP&A Revenue, Cost & Expense Forecasting Dashboard repository.")

# ------------------------------------------------------------- CRM
slug = "crm-event-marketing-data-hygiene-system"
CD = REPOS / "crm-event-marketing-data-hygiene-system/data_processed"
steps = [("Raw CRM records", 1500), ("Duplicates removed", 313), ("Unique contacts", 1187), ("Contactable leads", 1124)]
fig, ax = new(8, 3.4)
fig.subplots_adjust(left=0.22, bottom=0.18)
hbar(ax, [s for s, _ in steps], [v for _, v in steps], lambda v: f"{v:,.0f}",
     colors=[LIGHT, PAPER, DARK, INK], hatches=["", "////", "", ""], xmax=1800)
ax.set_xlabel("Records")
save(fig, slug, 1, "From raw export to contactable leads",
     "469 invalid emails and 283 invalid phone numbers were also flagged. Source: CRM & Event Marketing Data Hygiene System repository.")

ref = pd.read_csv(CD / "summary_referrals_by_status.csv").sort_values("referrals", ascending=False)
fig, ax = new(8, 3.6)
fig.subplots_adjust(left=0.22, bottom=0.17)
hbar(ax, ref.referral_status.tolist(), ref.referrals.tolist(), lambda v: f"{v:,.0f}", colors=DARK)
ax.set_xlabel("Referrals")
save(fig, slug, 2, "Referrals by follow-up status",
     "310 referrals prepared for sales and marketing follow-up. Source: CRM & Event Marketing Data Hygiene System repository.")

# ------------------------------------------------------------- Churn
slug = "ai-customer-churn-intelligence-system"
CH = REPOS / "ai-customer-churn-intelligence-system/data"
tel = pd.read_csv(CH / "raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
tel["churn"] = tel.Churn.eq("Yes")
scored = pd.read_csv(CH / "processed/churn_dashboard_data.csv")
seg = scored.groupby("RiskSegment").ActualChurn.mean().reindex(["High Risk", "Medium Risk", "Low Risk"]) * 100
nseg = scored.RiskSegment.value_counts()
fig, ax = new(8, 3.4)
fig.subplots_adjust(left=0.2, bottom=0.18)
hbar(ax, [f"{s} (n={nseg[s]})" for s in seg.index], seg.values.tolist(), lambda v: f"{v:.1f}%",
     colors=[INK, MID, PAPER], hatches=["", "", "////"], xmax=100)
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_xlabel("Observed churn rate")
save(fig, slug, 1, "Observed churn by model risk segment",
     "1,409 customers scored by the model. Source: AI Customer Churn Intelligence System repository.")

ct = tel.groupby("Contract").churn.mean().sort_values(ascending=False) * 100
fig, ax = new(8, 3.2)
fig.subplots_adjust(left=0.2, bottom=0.2)
hbar(ax, ct.index.tolist(), ct.values.tolist(), lambda v: f"{v:.1f}%", colors=DARK, xmax=55)
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_xlabel("Churn rate")
save(fig, slug, 2, "Churn rate by contract type",
     "Telco customer churn data, 7,043 customers. Source: AI Customer Churn Intelligence System repository.")

tel["band"] = pd.cut(tel.tenure, [-1, 12, 24, 48, 72], labels=["0 to 12", "13 to 24", "25 to 48", "49 to 72"])
tb = tel.groupby("band").churn.mean() * 100
fig, ax = new(8, 3.8)
ax.plot(range(len(tb)), tb.values, color=INK, marker="o", markersize=6, markerfacecolor=PAPER, linewidth=1.3)
for i, v in enumerate(tb.values):
    ax.text(i, v + 2, f"{v:.1f}%", ha="center", fontsize=11.5)
ax.set_xticks(range(len(tb)), tb.index)
ax.set_xlabel("Tenure (months)")
ax.set_ylim(0, 55)
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_ylabel("Churn rate")
save(fig, slug, 3, "Churn rate by customer tenure",
     "Source: AI Customer Churn Intelligence System repository.")

# ------------------------------------------------------------- Banking
slug = "banking-risk-and-financial-performance-analysis"
BK = REPOS / "banking-risk-and-financial-performance-analysis/data/processed"
loans = pd.read_csv(BK / "credit_risk_capstone_scored.csv")
order = ["Very Low", "Low", "Moderate", "High", "Very High"]
dr = loans.groupby("risk_band").default_flag.mean().reindex(order) * 100
fig, ax = new()
ax.bar(order, dr.values, color=[PAPER, LIGHT, MID, DARK, INK], edgecolor=INK, linewidth=0.6, width=0.6,
       hatch=None)
ax.patches[0].set_hatch("////")
for i, v in enumerate(dr.values):
    ax.text(i, v + 1.2, f"{v:.0f}%", ha="center", fontsize=11.5)
ax.set_ylim(0, 62)
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_ylabel("Observed default rate")
ax.set_xlabel("Model risk band (400 loans each)")
save(fig, slug, 1, "Observed default rate by model risk band",
     "Synthetic 2,000-loan portfolio; overall default rate 20.8%. Source: Banking Risk and Financial Performance Analysis repository.")

fi = pd.read_csv(BK / "credit_risk_feature_importance.csv").head(8)
names = {"credit_score": "Credit score", "interest_rate": "Interest rate", "revolving_utilization": "Revolving utilization",
         "loan_grade_F": "Loan grade F", "loan_grade_E": "Loan grade E", "installment_amount": "Installment amount",
         "debt_to_income_ratio": "Debt-to-income ratio", "oldest_credit_line_age": "Oldest credit line age"}
labels = [names.get(f.split("__", 1)[1], f.split("__", 1)[1].replace("_", " ").capitalize()) for f in fi.feature]
fig, ax = new(8, 4.2)
fig.subplots_adjust(left=0.24)
hbar(ax, labels, fi.importance.tolist(), lambda v: f"{v:.3f}", colors=DARK)
ax.set_xlabel("Feature importance")
save(fig, slug, 2, "Leading drivers of default risk",
     "Model ROC AUC 0.72. Source: Banking Risk and Financial Performance Analysis repository.")

el = loans.groupby("risk_band").expected_loss_proxy.sum().reindex(order)
el = el / el.sum() * 100
fig, ax = new(8, 3.6)
fig.subplots_adjust(left=0.14, bottom=0.17)
hbar(ax, order[::-1], el.values[::-1].tolist(), lambda v: f"{v:.1f}%", colors=[INK, DARK, MID, LIGHT, PAPER],
     hatches=["", "", "", "", "////"], xmax=65)
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_xlabel("Share of portfolio expected-loss exposure")
save(fig, slug, 3, "Expected-loss exposure by risk band",
     "Source: Banking Risk and Financial Performance Analysis repository.")

# ------------------------------------------------------------- Attrition (no public data: key figures only)
slug = "employee-attrition-risk-and-workforce-intelligence-analysis"
fig = plt.figure(figsize=(8, 3.2), dpi=200)
stats = [("21.6%", "estimated attrition risk\nacross employee groups"), ("9", "teams flagged for\nmanager-level review"),
         ("14", "retention signals used\nto summarize risk")]
for i, (big, small) in enumerate(stats):
    x0 = 0.04 + i * 0.33
    fig.text(x0, 0.62, big, fontsize=40, fontweight="bold", color=INK, va="center")
    fig.text(x0, 0.3, small, fontsize=13, color=DARK, va="center", linespacing=1.3)
    if i:
        fig.add_artist(plt.Line2D([x0 - 0.03, x0 - 0.03], [0.15, 0.85], color=LIGHT, linewidth=0.8))
fig.add_artist(plt.Line2D([0.04, 0.96], [0.94, 0.94], color=INK, linewidth=0.8))
fig.add_artist(plt.Line2D([0.04, 0.96], [0.06, 0.06], color=INK, linewidth=0.8))
save(fig, slug, 1, "Key figures from the workforce attrition analysis",
     "Summary figures as reported in the project; the underlying HR data are not public.")

# ------------------------------------------------------------- CARP synthetic control
slug = "agricultural-scm-productivity-analysis"
AX = REPOS / "agricultural-scm-productivity-analysis/data/raw/Analysis.xlsx"
carp = [("laborA", "Labor productivity", "Output per worker (thousand 2015 USD)", 1, "about 18.2% lower"),
        ("landA", "Land productivity", "Output per 1,000 hectares (thousand 2015 USD)", 1, "about 16.1% lower"),
        ("TFPA", "Total factor productivity", "TFP index", 1, "about 9% lower"),
        ("GDP", "GDP per capita (placebo check)", "GDP per capita (2015 USD)", 1, "only 2.5% lower")]
for n, (sheet, title, ylab, scale, gap) in enumerate(carp, start=1):
    d = pd.read_excel(AX, sheet_name=sheet).iloc[:, :3]
    d.columns = ["year", "ph", "synth"]
    d = d[pd.to_numeric(d.year, errors="coerce").notna()].astype(float)
    d = d[d.year >= 1970]
    fig, ax = new()
    ax.plot(d.year, d.ph / scale, color=INK, linewidth=1.5, label="Philippines")
    ax.plot(d.year, d.synth / scale, color=DARK, linewidth=1.3, linestyle=(0, (4, 2)), label="Synthetic Philippines")
    ax.axvline(1988, color=MID, linewidth=0.8, linestyle=":")
    ymax = max(d.ph.max(), d.synth.max()) / scale
    ax.text(1988.5, ymax * 1.02, "CARP, 1988", fontsize=11.5, color=DARK, va="bottom")
    ax.set_ylim(0, ymax * 1.12)
    ax.set_xlim(1970, 2008)
    ax.set_ylabel(ylab)
    ax.legend(loc="upper left")
    if scale == 1 and ymax > 100:
        ax.yaxis.set_major_formatter(thousands)
    save(fig, slug, n, f"{title}: the Philippines and its synthetic control, 1970 to 2008",
         f"After 1988 the Philippines averages {gap} than its synthetic control (1989 to 2008). "
         "Source: Cataytay, Deluna and Evangelio, synthetic control analysis.")

# ------------------------------------------------------------- Labor market
slug = "philippines-labor-market-trend-analysis"
LX = REPOS / "philippines-labor-market-trend-analysis/data/raw/Employment Indicators.xlsx"
rates = pd.read_excel(LX, sheet_name="0_Rates", header=1)
rates = rates[pd.to_numeric(rates["Row Labels"], errors="coerce").notna()].copy()
rates["year"] = rates["Row Labels"].astype(int)
fig, ax = new()
ax.plot(rates.year, rates["Underemployment Rate"] * 100, color=INK, linewidth=1.5, marker="o", markersize=3.5, label="Underemployment rate")
ax.plot(rates.year, rates["Unemployment Rate"] * 100, color=DARK, linewidth=1.3, linestyle=(0, (4, 2)), marker="s",
        markersize=3.5, markerfacecolor=PAPER, label="Unemployment rate")
ax.set_ylim(0, None)
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.legend(loc="upper right")
ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
year_axis(ax, 4)
save(fig, slug, 1, f"Unemployment and underemployment rates, {rates.year.min()} to {rates.year.max()}",
     "Annual figures from Labor Force Survey indicators. Source: project repository.")

fig, ax = new()
ax.plot(rates.year, rates["Labor Force Participation Rate"] * 100, color=INK, linewidth=1.5, marker="o", markersize=3.5)
ax.set_ylim(55, 70)
ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_ylabel("Labor force participation rate")
year_axis(ax, 4)
save(fig, slug, 2, f"Labor force participation rate, {rates.year.min()} to {rates.year.max()}",
     "Vertical axis starts at 55%. Source: project repository.")

sex = pd.read_excel(LX, sheet_name="1_Sex", header=1)
sex = sex[pd.to_numeric(sex["Row Labels"], errors="coerce").notna()].copy()
sex["year"] = sex["Row Labels"].astype(int)
fig, ax = new()
ax.plot(sex.year, sex["Male LFPR"] * 100, color=INK, linewidth=1.5, label="Men")
ax.plot(sex.year, sex["Female LFPR"] * 100, color=DARK, linewidth=1.3, linestyle=(0, (4, 2)), label="Women")
ax.set_ylim(0, 100)
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_ylabel("Labor force participation rate")
ax.legend(loc="lower right")
year_axis(ax, 4)
save(fig, slug, 3, "Labor force participation by sex",
     "Source: project repository.")

# ------------------------------------------------------------- Media insight
slug = "media-audience-engagement-analysis"
MX = REPOS / "media-audience-engagement-analysis/reports/excel/visualizations.xlsx"
mv = pd.read_excel(MX, sheet_name="Sheet2", header=None)
infl = mv.iloc[1:6, :2].copy()
infl.columns = ["month", "rate"]
infl["month"] = pd.to_datetime(infl.month)
infl["rate"] = infl.rate.astype(float) * 100
fig, ax = new(8, 4)
ax.plot(infl.month.dt.strftime("%b %Y"), infl.rate, color=INK, linewidth=1.5, marker="o", markersize=6, markerfacecolor=PAPER)
for i, v in enumerate(infl.rate):
    ax.text(i, v + 0.35, f"{v:.1f}%", ha="center", fontsize=11.5)
ax.set_ylim(0, 8.5)
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_ylabel("Headline inflation")
save(fig, slug, 1, "Philippine headline inflation, December 2025 to April 2026",
     "Source: Philippine Statistics Authority figures compiled in the media insight report.")

seg_rows = mv.iloc[16:20, :3].copy()
seg_rows.columns = ["month", "segment", "rate"]
seg_rows["month"] = pd.to_datetime(seg_rows.month).dt.strftime("%B %Y")
seg_rows["rate"] = seg_rows.rate.astype(float) * 100
pv = seg_rows.pivot(index="month", columns="segment", values="rate").reindex(["March 2026", "April 2026"])
fig, ax = new(8, 4)
x = np.arange(len(pv))
cols = list(pv.columns)
ax.bar(x - 0.19, pv[cols[0]], 0.36, color=LIGHT, edgecolor=INK, linewidth=0.6, label=cols[0])
ax.bar(x + 0.19, pv[cols[1]], 0.36, color=INK, edgecolor=INK, linewidth=0.6, label=cols[1])
for i in range(len(pv)):
    ax.text(i - 0.19, pv[cols[0]].iloc[i] + 0.15, f"{pv[cols[0]].iloc[i]:.1f}%", ha="center", fontsize=11.5)
    ax.text(i + 0.19, pv[cols[1]].iloc[i] + 0.15, f"{pv[cols[1]].iloc[i]:.1f}%", ha="center", fontsize=11.5)
ax.set_xticks(x, pv.index)
ax.set_ylim(0, 10)
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.legend(loc="upper left")
save(fig, slug, 2, "Inflation for all households and for the bottom 30%",
     "Source: Philippine Statistics Authority figures compiled in the media insight report.")

# ------------------------------------------------------------- Emigration
slug = "philippine-emigration-ardl-macroeconomic-analysis"
EM = REPOS / "philippine-emigration-ardl-macroeconomic-analysis/philippine-emigration-ardl-macroeconomic-analysis/data/raw"
mig = pd.read_stata(EM / "migration_ardl_workfile.dta")
mig = mig.dropna(subset=["year", "emig"])
mig["yr"] = pd.to_datetime(mig.year).dt.year.astype(int)
mig = mig.drop_duplicates("yr")
fig, ax = new()
ax.plot(mig.yr, mig.emig / 1000, color=INK, linewidth=1.5, marker="o", markersize=3.5)
row = mig[mig.yr == 2020].iloc[0]
ax.annotate("COVID-19, 2020", (2020, row.emig / 1000), xytext=(-12, -18), textcoords="offset points", ha="right", fontsize=11.5,
            arrowprops=dict(arrowstyle="-", color=MID, linewidth=0.8))
ax.set_ylim(0, None)
ax.set_ylabel("Permanent emigrants (thousands)")
year_axis(ax, 5)
save(fig, slug, 1, "Permanent Philippine emigrants, 1981 to 2023",
     "Permanent emigrant counts. Source: project repository.")

fig, ax = new()
ax.scatter(mig.lnPH_GDP, mig.lnM, s=26, facecolor=PAPER, edgecolor=INK, linewidth=0.9)
for _, r in mig[mig.yr.isin([1981, 2000, 2010, 2020, 2023])].iterrows():
    ax.annotate(str(int(r.yr)), (r.lnPH_GDP, r.lnM), xytext=(5, 4), textcoords="offset points", fontsize=10.5, color=DARK)
ax.set_xlabel("Log of Philippine GDP per capita")
ax.set_ylabel("Log of emigrants")
save(fig, slug, 2, "Emigration and Philippine GDP per capita, 1981 to 2023",
     "In the baseline ARDL model, a 1% rise in GDP per capita is linked to a 0.46% fall in long-run emigration. "
     "Source: project repository.")

# ============================================================= Additional figures
# Each project gets further figures that carry its argument on their own.


def step_hist(ax, a, b, bins, labels):
    ax.hist(a, bins=bins, histtype="step", color=INK, linewidth=1.4, density=True, label=labels[0])
    ax.hist(b, bins=bins, histtype="step", color=DARK, linewidth=1.2, linestyle=(0, (4, 2)), density=True, label=labels[1])
    ax.set_ylabel("Density")
    ax.legend(loc="upper right")


# ------------------------------------------------------------- Sentiment (more)
slug = "customer-sentiment-intelligence-dashboard"
rating = sd.rating.value_counts().sort_index()
fig, ax = new(8, 3.8)
ax.bar(rating.index.astype(str), rating.values, color=[INK if r <= 2 else (MID if r == 3 else LIGHT) for r in rating.index],
       edgecolor=INK, linewidth=0.6, width=0.62)
for i, v in enumerate(rating.values):
    ax.text(i, v + rating.max() * 0.02, f"{v} ({v / rating.sum() * 100:.0f}%)", ha="center", fontsize=11.5)
ax.set_xlabel("Star rating")
ax.set_ylabel("Reviews")
ax.set_ylim(0, rating.max() * 1.18)
save(fig, slug, 4, "Distribution of star ratings across 500 reviews",
     "One- and two-star reviews in black. Source: Customer Sentiment Intelligence Dashboard repository.")

sd["ym"] = pd.to_datetime(sd.Year_Month)
monthly = sd.groupby("ym").sentiment.apply(lambda s: (s == "Negative").mean() * 100)
counts = sd.groupby("ym").size()
monthly = monthly[counts >= 10]
fig, ax = new()
ax.plot(monthly.index, monthly.values, color=INK, linewidth=1.4, marker="o", markersize=4, markerfacecolor=PAPER)
ax.axhline((sd.sentiment == "Negative").mean() * 100, color=MID, linewidth=0.8, linestyle=":")
ax.text(monthly.index[0], (sd.sentiment == "Negative").mean() * 100 + 1, "Average, 25.4%", fontsize=11, color=DARK)
ax.set_ylim(0, max(monthly.max() * 1.25, 40))
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_ylabel("Share of reviews that are negative")
date_axis(ax)
save(fig, slug, 5, "Negative sentiment by month",
     "Months with fewer than 10 reviews are omitted. Source: Customer Sentiment Intelligence Dashboard repository.")

# ------------------------------------------------------------- Retention (more)
slug = "ecommerce-customer-retention-analytics"
st = pd.read_csv(RD / "dash_state_performance.csv").sort_values("total_revenue", ascending=False).head(10)
fig, ax = new(8, 4.4)
fig.subplots_adjust(left=0.12)
hbar(ax, st.customer_state.tolist(), (st.total_revenue / 1e6).tolist(),
     lambda v: f"${v:.1f}M", colors=DARK, xmax=st.total_revenue.max() / 1e6 * 1.5)
for yi, c in enumerate(st.churn_rate_pct):
    ax.text(ax.get_xlim()[1], yi, f"churn {c:.0f}%", va="center", ha="right", fontsize=10.5, color=DARK, style="italic")
ax.set_xlabel("Revenue (US dollars, millions)")
save(fig, slug, 4, "Revenue and churn rate for the ten largest Brazilian states",
     "São Paulo (SP) alone accounts for 37.5% of revenue. Source: E-commerce Customer Retention Analytics repository.")

RAW = RD.parent.parent / "raw"
cat = pd.read_csv(RD / "dash_product_category.csv")
tr = pd.read_csv(RAW / "product_category_name_translation.csv")
cat = cat.merge(tr, on="product_category_name", how="left")
cat["name"] = cat.product_category_name_english.fillna(cat.product_category_name).str.replace("_", " ").str.capitalize()
cat = cat.sort_values("total_revenue", ascending=False).head(10)
fig, ax = new(8, 4.4)
fig.subplots_adjust(left=0.24)
hbar(ax, cat.name.tolist(), cat.revenue_share_pct.tolist(), lambda v: f"{v:.1f}%", colors=MID, xmax=12)
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_xlabel("Share of total revenue")
save(fig, slug, 5, "Revenue share of the ten largest product categories",
     "Category names translated with the dataset's own translation table. Source: E-commerce Customer Retention Analytics repository.")

# ------------------------------------------------------------- Ads (more)
slug = "ecommerce-marketplace-ads-performance-dashboard"
prod = pd.read_csv(AD / "product_performance_summary.csv")
pc = prod.groupby("product_category")[["ad_spend", "ad_revenue"]].sum()
pc["roas"] = pc.ad_revenue / pc.ad_spend
pc = pc.sort_values("ad_revenue", ascending=False).head(8)
fig, ax = new(8, 4.2)
fig.subplots_adjust(left=0.22)
hbar(ax, pc.index.tolist(), (pc.ad_revenue / 1e6).tolist(), lambda v: f"${v:.1f}M", colors=DARK,
     xmax=pc.ad_revenue.max() / 1e6 * 1.45)
for yi, r in enumerate(pc.roas):
    ax.text(ax.get_xlim()[1], yi, f"ROAS {r:.1f}", va="center", ha="right", fontsize=10.5, color=DARK, style="italic")
ax.set_xlabel("Ad revenue (US dollars, millions)")
save(fig, slug, 3, "Ad revenue and return on ad spend for the eight largest product categories",
     "Source: eCommerce Marketplace Ads Performance Dashboard repository.")

slow = pd.read_csv(AD / "slow_moving_product_analysis.csv")
inv = slow.inventory_status.value_counts()
fig, ax = new(8, 3.8)
fig.subplots_adjust(left=0.18, bottom=0.16)
hbar(ax, inv.index.tolist(), inv.values.tolist(), lambda v: f"{v:,}",
     colors=[LIGHT if i == "Unknown" else DARK for i in inv.index], hatches=["////" if i == "Unknown" else "" for i in inv.index])
ax.set_xlabel("SKUs")
save(fig, slug, 4, "Inventory status recorded for each SKU",
     "Most SKUs have no reliable inventory status, which is why budget actions start with data fixes. "
     "Source: eCommerce Marketplace Ads Performance Dashboard repository.")

# ------------------------------------------------------------- FP&A (more)
slug = "fpa-revenue-cost-expense-forecasting-dashboard"
opx = pd.read_csv(FD / "operating_expense_summary.csv").groupby("operating_expense_category")[["actual_expense", "expense_budget"]].sum()
opx["var"] = (opx.actual_expense / opx.expense_budget - 1) * 100
opx = opx.sort_values("var", ascending=False)
cap = 25
fig, ax = new(8, 4.6)
fig.subplots_adjust(left=0.3)
vals = [min(v, cap) for v in opx["var"]]
hbar(ax, opx.index.tolist(), vals, lambda v: f"+{v:.1f}%", colors=DARK, xmax=cap * 1.35)
for yi, v in enumerate(opx["var"]):
    if v > cap:
        ax.texts[yi].set_text(f"+{v:,.0f}%")
        ax.patches[yi].set_hatch("////")
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_xlabel("Actual spending above budget, 2023 to 2025")
save(fig, slug, 3, "Operating expenses above budget, by category",
     "Every category ran over budget. The hatched bar is cut at 25%: Learning & Development spent $0.96M against a $0.11M budget. "
     "Source: FP&A Revenue, Cost & Expense Forecasting Dashboard repository.")

ano = pd.read_csv(FD / "anomaly_detection_output.csv")
tab = ano.groupby(["anomaly_type", "severity"]).size().unstack(fill_value=0).reindex(columns=["Critical", "High", "Medium"], fill_value=0)
tab = tab.loc[tab.sum(axis=1).sort_values(ascending=False).index]
fig, ax = new(8, 3.8)
fig.subplots_adjust(left=0.36, bottom=0.17)
left = np.zeros(len(tab))
for sev, col, h in [("Critical", INK, ""), ("High", MID, ""), ("Medium", PAPER, "////")]:
    ax.barh(range(len(tab)), tab[sev], left=left, color=col, edgecolor=INK, linewidth=0.6, height=0.62, hatch=h, label=sev)
    left += tab[sev].values
ax.set_yticks(range(len(tab)), tab.index)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.legend(loc="lower right", title="Severity", title_fontsize=11)
ax.set_xlabel("Flagged business-unit months")
save(fig, slug, 4, "369 flagged anomalies by type and severity",
     "Source: FP&A Revenue, Cost & Expense Forecasting Dashboard repository.")

# ------------------------------------------------------------- CRM (more)
slug = "crm-event-marketing-data-hygiene-system"
iss = pd.read_csv(CD / "summary_invalid_contact_issues.csv")
em = iss[iss.email_issue_type != "Valid"].groupby("email_issue_type").records.sum().sort_values(ascending=False)
ph = iss[iss.phone_issue_type != "Valid"].groupby("phone_issue_type").records.sum().sort_values(ascending=False)
fig, axes = plt.subplots(1, 2, figsize=(8, 3.8), dpi=200)
fig.subplots_adjust(left=0.2, right=0.97, wspace=0.95, bottom=0.17, top=0.88)
for ax_, ser, title in [(axes[0], em, "Email problems"), (axes[1], ph, "Phone problems")]:
    hbar(ax_, ser.index.tolist(), ser.values.tolist(), lambda v: f"{v:,}", colors=DARK)
    ax_.set_title(title, fontsize=12.5, loc="left", fontweight="bold")
    ax_.tick_params(axis="y", labelsize=10.5)
    ax_.set_xlabel("Records")
save(fig, slug, 3, "Why contacts failed validation",
     "Source: CRM & Event Marketing Data Hygiene System repository.")

reg = pd.read_csv(CD / "summary_contacts_by_region.csv").dropna(subset=["region"])
reg["region"] = reg.region.replace({"Ncr": "NCR", "Car": "CAR"})
reg = reg.groupby("region", as_index=False).contacts.sum().sort_values("contacts", ascending=False)
fig, ax = new(8, 4.4)
fig.subplots_adjust(left=0.24)
hbar(ax, reg.region.tolist(), reg.contacts.tolist(), lambda v: f"{v:,}", colors=MID)
ax.set_xlabel("Clean contacts")
save(fig, slug, 4, "Clean contacts by region",
     "Region spellings merged (e.g. Ncr into NCR); 5 contacts with no region omitted. Source: CRM & Event Marketing Data Hygiene System repository.")

ev = pd.read_csv(CD / "summary_event_attendance_by_city.csv").dropna(subset=["city"])
ev = ev.pivot_table(index="city", columns="attended_flag", values="registrations", aggfunc="sum", fill_value=0)
ev["total"] = ev.sum(axis=1)
ev["rate"] = ev.get("Yes", 0) / ev.total * 100
ev = ev.sort_values("total", ascending=False).head(10).sort_values("rate", ascending=False)
fig, ax = new(8, 4.4)
fig.subplots_adjust(left=0.26)
hbar(ax, [f"{c} (n={int(t)})" for c, t in zip(ev.index, ev.total)], ev.rate.tolist(), lambda v: f"{v:.0f}%", colors=DARK, xmax=60)
ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_xlabel("Registrants who attended")
save(fig, slug, 5, "Event attendance rate in the ten cities with the most registrations",
     "Source: CRM & Event Marketing Data Hygiene System repository.")

# ------------------------------------------------------------- Churn (more)
slug = "ai-customer-churn-intelligence-system"
for n, (col, title) in enumerate([("InternetService", "Churn rate by internet service"),
                                  ("PaymentMethod", "Churn rate by payment method")], start=4):
    g = tel.groupby(col).churn.mean().sort_values(ascending=False) * 100
    fig, ax = new(8, 3.4)
    fig.subplots_adjust(left=0.3, bottom=0.18)
    hbar(ax, g.index.str.replace(" (automatic)", ", automatic", regex=False).tolist(), g.values.tolist(),
         lambda v: f"{v:.1f}%", colors=DARK, xmax=55)
    ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.set_xlabel("Churn rate")
    save(fig, slug, n, title, "Telco customer churn data, 7,043 customers. Source: AI Customer Churn Intelligence System repository.")

fig, ax = new()
step_hist(ax, tel[tel.churn].MonthlyCharges, tel[~tel.churn].MonthlyCharges, np.arange(15, 125, 5), ["Churned", "Stayed"])
ax.set_xlabel("Monthly charges (US dollars)")
save(fig, slug, 6, "Monthly charges of customers who churned and customers who stayed",
     "Churners cluster at higher monthly charges. Source: AI Customer Churn Intelligence System repository.")

# ------------------------------------------------------------- Banking (more)
slug = "banking-risk-and-financial-performance-analysis"
gr = loans.groupby("loan_grade").default_flag.agg(["mean", "size"]).sort_index()
fig, ax = new()
ax.plot(gr.index, gr["mean"] * 100, color=INK, linewidth=1.4, marker="o", markersize=6, markerfacecolor=PAPER)
for i, (g, r) in enumerate(gr.iterrows()):
    ax.text(i, r["mean"] * 100 + 2.5, f"{r['mean'] * 100:.0f}%\n(n={int(r['size'])})", ha="center", fontsize=10.5)
ax.set_ylim(0, gr["mean"].max() * 100 * 1.35)
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_xlabel("Loan grade")
ax.set_ylabel("Observed default rate")
save(fig, slug, 4, "Observed default rate by loan grade",
     "Source: Banking Risk and Financial Performance Analysis repository.")

fig, ax = new()
step_hist(ax, loans[loans.default_flag == 1].credit_score, loans[loans.default_flag == 0].credit_score,
          np.arange(300, 860, 20), ["Defaulted", "Repaid"])
ax.set_xlabel("Credit score")
save(fig, slug, 5, "Credit scores of loans that defaulted and loans that were repaid",
     "Credit score is the strongest single driver in the model. Source: Banking Risk and Financial Performance Analysis repository.")

# ------------------------------------------------------------- CARP (rigor)
slug = "agricultural-scm-productivity-analysis"
d = pd.read_excel(AX, sheet_name="laborA").iloc[:, :5]
d.columns = ["year", "ph", "synth", "gap", "gap_pct"]
d = d[pd.to_numeric(d.year, errors="coerce").notna()].astype(float)
d = d[d.year >= 1970]
fig, ax = new()
ax.bar(d.year, d.gap_pct * 100, color=[LIGHT if y <= 1988 else INK for y in d.year], edgecolor=INK, linewidth=0.4, width=0.8)
ax.axhline(0, color=INK, linewidth=0.8)
ax.axvline(1988.5, color=MID, linewidth=0.8, linestyle=":")
ax.text(1989, 12, "After CARP", fontsize=11.5, color=DARK)
ax.text(1987.5, 12, "Before", fontsize=11.5, color=DARK, ha="right")
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_ylabel("Gap from synthetic control")
ax.set_xlim(1969, 2009)
save(fig, slug, 5, "Yearly labor productivity gap between the Philippines and its synthetic control",
     "Grey bars are the pre-treatment fit; black bars are post-1988 gaps (average 18.2%). "
     "Source: Cataytay, Deluna and Evangelio, synthetic control analysis.")

pl = []
for sheet, label in [("Labor_Placebo", "Labor productivity"), ("Land_Placebo", "Land productivity"), ("TFP_Placebo", "TFP")]:
    t = pd.read_excel(AX, sheet_name=sheet).iloc[:, :7]
    t = t[t.unit_name.notna()]
    pl.append((label, t))
fig, axes = plt.subplots(1, 3, figsize=(8, 3.9), dpi=200, sharey=False)
fig.subplots_adjust(left=0.08, right=0.98, wspace=0.35, bottom=0.16, top=0.86)
for ax_, (label, t) in zip(axes, pl):
    r = t.sort_values("mspe_ratio", ascending=False).reset_index(drop=True)
    is_ph = r.unit_name.astype(str).str.contains("Philippines")
    ax_.bar(range(len(r)), r.mspe_ratio, color=[INK if p else LIGHT for p in is_ph], width=0.85, linewidth=0)
    ph_row = r[is_ph].iloc[0]
    ax_.set_title(f"{label}\nrank 1 of {len(r)}, p = {ph_row.fishers_exact_pvalue:.3f}", fontsize=11, loc="left")
    ax_.set_xticks([])
    ax_.set_xlabel("Countries, ranked")
axes[0].set_ylabel("Post/pre-1988 MSPE ratio")
save(fig, slug, 6, "Placebo tests: the Philippines against every donor country",
     "Each bar reassigns the 1988 reform to one country; the Philippines (black) has the largest post-treatment divergence in all three outcomes. "
     "p is Fisher's exact permutation p-value. Source: study workbook.")

wt = pd.read_excel(AX, sheet_name="Country Weights (W)").iloc[:10, :4]
wt.columns = ["country", "Labor productivity", "Land productivity", "TFP"]
wt = wt.set_index("country").apply(pd.to_numeric, errors="coerce").fillna(0)
fig, ax = new(8, 4.4)
fig.subplots_adjust(left=0.24)
x = np.arange(len(wt))
for k, (colname, col, h) in enumerate([("Labor productivity", INK, ""), ("Land productivity", MID, ""), ("TFP", PAPER, "////")]):
    ax.barh(x + (k - 1) * 0.26, wt[colname], height=0.26, color=col, edgecolor=INK, linewidth=0.5, hatch=h, label=colname)
ax.set_yticks(x, wt.index)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.set_xlabel("Weight in the synthetic Philippines")
fig.subplots_adjust(top=0.88)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3)
save(fig, slug, 7, "Donor countries and their weights in each synthetic control",
     "Weights sum to one for each outcome; pre-1988 fit error is about 5 to 6% of the outcome level. Source: study workbook.")

# ------------------------------------------------------------- Labor market (more)
slug = "philippines-labor-market-trend-analysis"
SX = REPOS / "philippines-labor-market-trend-analysis/data/raw/Number of Employed per Sector.xlsx"
sec = pd.read_excel(SX, sheet_name="0_Annual per Sector")
sec = sec[pd.to_numeric(sec.year, errors="coerce").notna()].copy()
sec["year"] = sec.year.astype(int)
sec = sec[sec.year <= 2025]
fig, ax = new()
for col, lab, c, ls, dy in [("Service Sector (%)", "Services", INK, "-", 0), ("Agricultural Sector (%)", "Agriculture", DARK, (0, (4, 2)), 2.2),
                            ("Industry Sector (%)", "Industry", MID, (0, (1, 1.5)), -2.2)]:
    ax.plot(sec.year, sec[col] * 100, color=c, linestyle=ls, linewidth=1.5)
    ax.text(sec.year.iloc[-1] + 0.3, sec[col].iloc[-1] * 100 + dy, lab, va="center", fontsize=11.5)
ax.set_xlim(sec.year.min(), sec.year.max() + 3)
ax.set_ylim(0, 70)
ax.yaxis.set_major_formatter(PercentFormatter(decimals=0))
ax.set_ylabel("Share of employed persons")
year_axis(ax, 2)
save(fig, slug, 4, f"Employment by sector, {sec.year.min()} to {sec.year.max()}",
     "Source: project repository.")

sub = pd.read_excel(SX, sheet_name="1_Service Sector Disaggregation")
sub = sub.iloc[: sub.year.isna().idxmax()]  # first block holds levels (thousands); the block below holds shares
sub = sub[pd.to_numeric(sub.year, errors="coerce").notna()]
last = sub[sub.year.astype(int) == 2025].iloc[0]
parts = last.drop(["year", "services"]).astype(float).sort_values(ascending=False).head(8)
fig, ax = new(8, 4.4)
fig.subplots_adjust(left=0.34)
hbar(ax, [p.capitalize().replace("Pubad", "Public administration") for p in parts.index], (parts / 1000).tolist(), lambda v: f"{v:.1f}M", colors=DARK)
ax.set_xlabel("Employed persons (millions)")
save(fig, slug, 5, f"Largest service subsectors by employment, {int(last.year)}",
     "Source: project repository.")

# ------------------------------------------------------------- Emigration (more)
slug = "philippine-emigration-ardl-macroeconomic-analysis"
fig, axes = plt.subplots(2, 2, figsize=(8, 5.2), dpi=200, sharex=True)
fig.subplots_adjust(left=0.1, right=0.97, hspace=0.42, wspace=0.28, top=0.93, bottom=0.08)
for ax_, (col, title, fmt) in zip(axes.flat, [("ph_gdp", "Philippine GDP per capita (US dollars)", thousands),
                                            ("ph_csg", "Government consumption share of GDP", PercentFormatter(1.0, decimals=0)),
                                            ("ph_labsh", "Labor income share of GDP", PercentFormatter(1.0, decimals=0)),
                                            ("exc", "Pesos per US dollar", thousands)]):
    ax_.plot(mig.yr, mig[col], color=INK, linewidth=1.3)
    ax_.set_title(title, fontsize=11.5, loc="left")
    ax_.yaxis.set_major_formatter(fmt)
    ax_.tick_params(labelsize=10.5)
save(fig, slug, 3, "The determinants used in the ARDL models, 1981 to 2023",
     "All series are integrated of order one by ADF, Phillips-Perron and KPSS tests. Source: project repository.")

# ============================================================= Front-page hero layers
# The hero (index.html) is built from these: three chart clippings for the
# archive plane, and the real CARP labor-productivity series that the hero
# draws as inline SVG.
from PIL import Image  # noqa: E402

HERO = SITE / "assets" / "hero"
HERO.mkdir(parents=True, exist_ok=True)
for name, src in [("clip-banking", "banking-risk-and-financial-performance-analysis-1"),
                  ("clip-churn", "ai-customer-churn-intelligence-system-2"),
                  ("clip-emigration", "philippine-emigration-ardl-macroeconomic-analysis-1")]:
    im = Image.open(OUT / f"{src}.png").convert("RGB")
    im.thumbnail((640, 640), Image.LANCZOS)
    im.save(HERO / f"{name}.webp", "WEBP", quality=86, method=6)

d = pd.read_excel(AX, sheet_name="laborA").iloc[:, :5]
d.columns = ["year", "ph", "synth", "gap", "gap_pct"]
d = d[pd.to_numeric(d.year, errors="coerce").notna()].astype(float)
d = d[d.year >= 1970]
post = d[(d.year >= 1989) & (d.year <= 2008)]
(HERO / "carp-labor.json").write_text(json.dumps({
    "source": "Cataytay, Deluna and Evangelio, synthetic control analysis (Analysis.xlsx, sheet laborA)",
    "unit": "output per worker, thousand 2015 USD",
    "treatment_year": 1988,
    "average_gap_pct_1989_2008": round(float(post.gap_pct.mean() * 100), 2),
    "years": [int(y) for y in d.year],
    "philippines": [round(float(v), 1) for v in d.ph],
    "synthetic": [round(float(v), 1) for v in d.synth],
}, indent=1))

(Path(sys.argv[2]) / "assets" / "figures" / "figures.json").write_text(json.dumps(MANIFEST, indent=1))
print({k: len(v) for k, v in MANIFEST.items()}, sum(len(v) for v in MANIFEST.values()), "figures")
