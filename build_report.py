import csv
import datetime
import html
import os
import re
import statistics
import sys

# The progress messages use ✓, which the default Windows console encoding cannot print.
sys.stdout.reconfigure(encoding="utf-8")


# ==================== CONFIGURATION ====================
METRICS_CSV = "software_metrics.csv"
REDLYNE_CSV = "redlyne_summary.csv"
FINDINGS_CSV = "redlyne_findings.csv"
TASKS_DIR = os.path.join("bottle_repo", "prompts")
RESULTS_DIR = "results"

# (keyword in folder name, display name, group), in display order.
ORIGINS = [
    ("human", "Human", "Human"),
    ("qwen", "Qwen2.5-Coder 32B", "Open-weight"),
    ("gemma", "Gemma 2 9B", "Open-weight"),
    ("gpt", "ChatGPT (gpt-4.1)", "Closed"),
    ("gemini", "Gemini (web)", "Closed"),
]

# One color per group (first three slots of the validated categorical
# palette), each with its own light- and dark-mode step.
GROUP_COLORS = {
    "Human": ("#1baf7a", "#199e70"),
    "Open-weight": ("#2a78d6", "#3987e5"),
    "Closed": ("#eb6834", "#d95926"),
}

# Sequential blue ramp (step 150 -> 700) for the vulnerability matrix.
BLUE_RAMP = [
    "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
    "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
]
# =======================================================


def origin_of(model_run):
    folder = re.split(r"[\\/]", model_run)[0].lower()
    for keyword, name, group in ORIGINS:
        if keyword in folder:
            return name
    return None


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def vulnerability_count(row):
    """Distinct OWASP categories flagged in a file, as the Redlyne extension reports them."""
    return len([c for c in row.get("OWASP_Categories", "").split(";") if c.strip()])


def mean(values):
    values = [v for v in values if v is not None]
    return statistics.mean(values) if values else None


def fmt(value, digits=1, suffix=""):
    return "—" if value is None else f"{value:.{digits}f}{suffix}"


# ------------------------------------------------------------------ data

def summarize(metrics, redlyne):
    summary = {}
    for keyword, name, group in ORIGINS:
        m_rows = [r for r in metrics if origin_of(r["Model_Run"]) == name]
        valid = [r for r in m_rows if r["Status"] == "Valid"]
        r_rows = [
            r for r in redlyne
            if origin_of(r["Model_Run"]) == name and r["Status"] != "Scan Error"
        ]
        vulnerable = [r for r in r_rows if r["Status"] == "Vulnerable"]

        summary[name] = {
            "Origin": name,
            "Group": group,
            "Files": len(m_rows),
            "Syntax_Errors": len(m_rows) - len(valid),
            "Mean_SLOC": mean(number(r["SLOC"]) for r in valid),
            "Mean_Cyclomatic_Complexity": mean(
                number(r["Avg_Cyclomatic_Complexity"]) for r in valid
            ),
            "Mean_Maintainability_Index": mean(
                number(r["Maintainability_Index"]) for r in valid
            ),
            "Files_Scanned": len(r_rows),
            "Files_With_Vulnerabilities": len(vulnerable),
            "Vulnerability_Rate_Pct": (
                100 * len(vulnerable) / len(r_rows) if r_rows else None
            ),
            "Mean_Vulnerabilities_Per_File": mean(
                vulnerability_count(r) for r in r_rows
            ),
        }
    return summary


def build_matrix(tasks, redlyne):
    """Mean Redlyne vulnerabilities per file for each task x origin (None = no data)."""
    cells = {}
    for task in tasks:
        for _, name, _ in ORIGINS:
            rows = [
                r for r in redlyne
                if origin_of(r["Model_Run"]) == name
                and os.path.splitext(r["File"])[0] == task
                and r["Status"] != "Scan Error"
            ]
            cells[(task, name)] = (
                mean(vulnerability_count(r) for r in rows) if rows else None
            )
    return cells


def write_outputs(summary, tasks, cells):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    fields = list(next(iter(summary.values())).keys())
    with open(os.path.join(RESULTS_DIR, "origin_summary.csv"), "w",
              newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in summary.values():
            writer.writerow({
                k: (round(v, 2) if isinstance(v, float) else ("" if v is None else v))
                for k, v in row.items()
            })

    with open(os.path.join(RESULTS_DIR, "vulnerability_matrix.csv"), "w",
              newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Task", *[name for _, name, _ in ORIGINS]])
        for task in tasks:
            writer.writerow([
                task,
                *["" if cells[(task, name)] is None else round(cells[(task, name)], 2)
                  for _, name, _ in ORIGINS],
            ])


# ------------------------------------------------------------------ charts

def esc(text):
    return html.escape(str(text), quote=True)


def bar_chart(summary, key, title, unit="", digits=1, max_value=None):
    """Horizontal bars, one per origin, colored by group, directly labeled."""
    row_h, gap, label_w, plot_w, value_w = 30, 10, 170, 380, 70
    names = [name for _, name, _ in ORIGINS]
    values = [summary[n][key] for n in names]
    top = max_value or max([v for v in values if v is not None] or [1]) * 1.1 or 1
    height = len(names) * (row_h + gap) + 30

    parts = [
        f'<svg viewBox="0 0 {label_w + plot_w + value_w} {height}" role="img"'
        f' aria-label="{esc(title)}">'
    ]
    # Recessive baseline.
    parts.append(
        f'<line x1="{label_w}" y1="0" x2="{label_w}" y2="{height - 30}"'
        ' class="axis"/>'
    )
    for i, (name, value) in enumerate(zip(names, values)):
        y = i * (row_h + gap)
        group = summary[name]["Group"]
        parts.append(
            f'<text x="{label_w - 10}" y="{y + row_h / 2}" class="label"'
            f' text-anchor="end" dominant-baseline="middle">{esc(name)}</text>'
        )
        if value is None:
            parts.append(
                f'<text x="{label_w + 8}" y="{y + row_h / 2}" class="muted"'
                ' dominant-baseline="middle">no data yet</text>'
            )
            continue
        w = max(plot_w * value / top, 2)
        tip = f"{name} ({group}): {fmt(value, digits, unit)}"
        # Square at the baseline, 4px rounded data end.
        parts.append(
            f'<path d="M{label_w},{y + 4} h{max(w - 4, 0)} a4,4 0 0 1 4,4'
            f' v{row_h - 16} a4,4 0 0 1 -4,4 h{-max(w - 4, 0)} z"'
            f' class="bar g-{group.lower().replace("-", "")}">'
            f'<title>{esc(tip)}</title></path>'
        )
        parts.append(
            f'<text x="{label_w + w + 8}" y="{y + row_h / 2}" class="value"'
            f' dominant-baseline="middle">{fmt(value, digits, unit)}</text>'
        )
    # Axis tick labels at 0 and the top of the scale.
    parts.append(
        f'<text x="{label_w}" y="{height - 10}" class="muted" text-anchor="middle">0</text>'
        f'<text x="{label_w + plot_w}" y="{height - 10}" class="muted"'
        f' text-anchor="middle">{fmt(top, 0, unit)}</text>'
    )
    parts.append("</svg>")
    return "".join(parts)


def ramp_color(value, top):
    if top <= 0:
        return BLUE_RAMP[0]
    index = round((len(BLUE_RAMP) - 1) * min(value / top, 1))
    return BLUE_RAMP[index]


def heatmap(tasks, cells):
    cell_w, cell_h, label_w, head_h = 112, 26, 160, 46
    names = [name for _, name, _ in ORIGINS]
    width = label_w + len(names) * cell_w
    height = head_h + len(tasks) * cell_h
    present = [v for v in cells.values() if v is not None]
    top = max(present) if present else 0

    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img"'
        ' aria-label="Redlyne vulnerabilities per task and code origin">'
    ]
    for j, name in enumerate(names):
        x = label_w + j * cell_w + cell_w / 2
        words = name.split(" ", 1)
        parts.append(
            f'<text x="{x}" y="16" class="label" text-anchor="middle">{esc(words[0])}</text>'
        )
        if len(words) > 1:
            parts.append(
                f'<text x="{x}" y="33" class="muted" text-anchor="middle">{esc(words[1])}</text>'
            )
    for i, task in enumerate(tasks):
        y = head_h + i * cell_h
        parts.append(
            f'<text x="{label_w - 10}" y="{y + cell_h / 2}" class="label mono"'
            f' text-anchor="end" dominant-baseline="middle">{esc(task)}</text>'
        )
        for j, name in enumerate(names):
            x = label_w + j * cell_w
            value = cells[(task, name)]
            if value is None:
                fill_class, fill, text, text_class = "cell-empty", "", "—", "muted"
            elif value == 0:
                fill_class, fill, text, text_class = "cell-zero", "", "0", "muted"
            else:
                fill = ramp_color(value, top)
                fill_class = "cell"
                text = fmt(value, 1).rstrip("0").rstrip(".")
                dark = BLUE_RAMP.index(fill) >= 5
                text_class = "cell-text-light" if dark else "cell-text-dark"
            tip = (
                f"{task} · {name}: "
                + ("no outputs scanned" if value is None
                   else f"{fmt(value, 2)} vulnerabilities per file (mean of runs)")
            )
            style = f' style="fill:{fill}"' if fill else ""
            # 2px surface gap between cells.
            parts.append(
                f'<rect x="{x + 1}" y="{y + 1}" width="{cell_w - 2}" height="{cell_h - 2}"'
                f' rx="3" class="{fill_class}"{style}><title>{esc(tip)}</title></rect>'
                f'<text x="{x + cell_w / 2}" y="{y + cell_h / 2}" class="{text_class}"'
                f' text-anchor="middle" dominant-baseline="middle">{esc(text)}</text>'
            )
    parts.append("</svg>")
    return "".join(parts)


def summary_table(summary):
    head = (
        "<tr><th>Origin</th><th>Group</th><th>Files</th><th>Syntax errors</th>"
        "<th>Mean SLOC</th><th>Mean CC</th><th>Mean MI</th>"
        "<th>Files with vulnerabilities</th><th>Vulnerability rate</th>"
        "<th>Vulnerabilities / file</th></tr>"
    )
    rows = []
    for s in summary.values():
        rows.append(
            "<tr>"
            f"<td>{esc(s['Origin'])}</td><td>{esc(s['Group'])}</td>"
            f"<td>{s['Files']}</td><td>{s['Syntax_Errors'] if s['Files'] else '—'}</td>"
            f"<td>{fmt(s['Mean_SLOC'])}</td>"
            f"<td>{fmt(s['Mean_Cyclomatic_Complexity'])}</td>"
            f"<td>{fmt(s['Mean_Maintainability_Index'])}</td>"
            f"<td>{s['Files_With_Vulnerabilities'] if s['Files_Scanned'] else '—'}"
            f"{' / ' + str(s['Files_Scanned']) if s['Files_Scanned'] else ''}</td>"
            f"<td>{fmt(s['Vulnerability_Rate_Pct'], 0, '%')}</td>"
            f"<td>{fmt(s['Mean_Vulnerabilities_Per_File'], 2)}</td>"
            "</tr>"
        )
    return f"<table><thead>{head}</thead><tbody>{''.join(rows)}</tbody></table>"


def locations_table(findings):
    """Every flagged line, grouped by task, so reviewers can see where in each
    function the vulnerable code is."""
    order = {name: i for i, (_, name, _) in enumerate(ORIGINS)}
    rows = []
    for f in findings:
        origin = origin_of(f["Model_Run"])
        if origin is None:
            continue
        run = re.search(r"run_(\d+)", f["Model_Run"])
        rows.append({
            "task": os.path.splitext(f["File"])[0],
            "origin": origin,
            "run": run.group(1) if run else "—",
            "line": int(number(f["Line"]) or 0),
            "category": f["OWASP_Categories"],
            "rule": f["Rule_ID"],
            "code": f["Code"],
            "note": f["Comment"],
        })
    rows.sort(key=lambda r: (r["task"], order[r["origin"]], r["run"], r["line"]))

    head = (
        "<tr><th>Origin</th><th>Run</th><th>Line</th><th>Vulnerability</th>"
        "<th>Rule</th><th>Flagged code</th></tr>"
    )
    body = []
    current = None
    for r in rows:
        if r["task"] != current:
            current = r["task"]
            count = sum(1 for x in rows if x["task"] == current)
            body.append(
                f'<tr class="task-row"><td colspan="6"><span class="mono">{esc(current)}</span>'
                f' <span class="muted-text">· {count} flagged line{"s" if count != 1 else ""}</span></td></tr>'
            )
        body.append(
            "<tr>"
            f"<td>{esc(r['origin'])}</td><td>{esc(r['run'])}</td><td>{r['line']}</td>"
            f"<td>{esc(r['category'])}<div class=\"muted-text\">{esc(r['note'])}</div></td>"
            f"<td class=\"mono\">{esc(r['rule'])}</td>"
            f"<td><code>{esc(r['code'])}</code></td>"
            "</tr>"
        )
    return (
        f'<table class="loc"><thead>{head}</thead><tbody>{"".join(body)}</tbody></table>'
    )


def legend():
    items = "".join(
        f'<span class="key"><span class="swatch g-{g.lower().replace("-", "")}"></span>{esc(g)}</span>'
        for g in GROUP_COLORS
    )
    return f'<div class="legend">{items}</div>'


CSS = """
:root {
  color-scheme: light;
  --surface: #fcfcfb; --surface-2: #f1f0ec; --border: #e2e1dc;
  --text-primary: #0b0b0b; --text-secondary: #52514e; --text-muted: #7a7974;
  --g-human: %(human_l)s; --g-open: %(open_l)s; --g-closed: %(closed_l)s;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --surface: #1a1a19; --surface-2: #262624; --border: #3a3a37;
    --text-primary: #f0efec; --text-secondary: #c3c2b7; --text-muted: #8f8e86;
    --g-human: %(human_d)s; --g-open: %(open_d)s; --g-closed: %(closed_d)s;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --surface: #1a1a19; --surface-2: #262624; --border: #3a3a37;
  --text-primary: #f0efec; --text-secondary: #c3c2b7; --text-muted: #8f8e86;
  --g-human: %(human_d)s; --g-open: %(open_d)s; --g-closed: %(closed_d)s;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--surface); color: var(--text-primary);
  font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 1040px; margin: 0 auto; padding: 32px 16px 64px; }
h1 { font-size: 26px; margin: 0 0 4px; }
h2 { font-size: 19px; margin: 40px 0 4px; }
p.sub, .note { color: var(--text-secondary); margin: 0 0 16px; }
.note { font-size: 13px; }
.status { background: var(--surface-2); border: 1px solid var(--border);
  border-radius: 8px; padding: 12px 16px; font-size: 14px; color: var(--text-secondary); }
.status strong { color: var(--text-primary); }
.chart { background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  padding: 16px; margin: 8px 0; }
.chart svg { width: 100%%; height: auto; display: block; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }
.grid h3 { font-size: 14px; margin: 0 0 8px; color: var(--text-secondary); font-weight: 600; }
svg text { font-size: 13px; fill: var(--text-primary); }
svg .label { fill: var(--text-primary); }
svg .value { fill: var(--text-primary); font-weight: 600; }
svg .muted { fill: var(--text-muted); font-size: 12px; }
svg .mono { font-family: ui-monospace, Consolas, monospace; font-size: 12px; }
svg .axis { stroke: var(--border); stroke-width: 1; }
svg .bar:hover, svg .cell:hover { opacity: .8; }
.g-human { fill: var(--g-human); background: var(--g-human); }
.g-openweight { fill: var(--g-open); background: var(--g-open); }
.g-closed { fill: var(--g-closed); background: var(--g-closed); }
.cell-zero { fill: var(--surface-2); }
.cell-empty { fill: none; stroke: var(--border); stroke-dasharray: 3 3; }
.cell-text-dark { fill: #0b0b0b; font-weight: 600; }
.cell-text-light { fill: #ffffff; font-weight: 600; }
.legend { display: flex; gap: 16px; flex-wrap: wrap; font-size: 13px;
  color: var(--text-secondary); margin: 4px 0 8px; }
.key { display: inline-flex; align-items: center; gap: 6px; }
.swatch { width: 12px; height: 12px; border-radius: 3px; display: inline-block; }
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%%; font-size: 13px; }
th, td { text-align: right; padding: 6px 10px; border-bottom: 1px solid var(--border);
  white-space: nowrap; }
th:first-child, td:first-child, th:nth-child(2), td:nth-child(2) { text-align: left; }
table.loc th, table.loc td { text-align: left; vertical-align: top; white-space: normal; }
table.loc td:nth-child(2), table.loc td:nth-child(3) { text-align: right; white-space: nowrap; }
table.loc tr.task-row td { background: var(--surface-2); font-weight: 600; padding-top: 10px; }
table.loc code { font-family: ui-monospace, Consolas, monospace; font-size: 12px;
  word-break: break-word; }
.mono { font-family: ui-monospace, Consolas, monospace; }
.muted-text { color: var(--text-muted); font-size: 12px; font-weight: 400; }
th { color: var(--text-secondary); font-weight: 600; }
"""


def build_html(summary, tasks, cells, has_redlyne, redlyne_version, findings):
    css = CSS % {
        "human_l": GROUP_COLORS["Human"][0], "human_d": GROUP_COLORS["Human"][1],
        "open_l": GROUP_COLORS["Open-weight"][0], "open_d": GROUP_COLORS["Open-weight"][1],
        "closed_l": GROUP_COLORS["Closed"][0], "closed_d": GROUP_COLORS["Closed"][1],
    }

    missing_code = [s["Origin"] for s in summary.values() if not s["Files"]]
    missing_scan = [
        s["Origin"] for s in summary.values() if s["Files"] and not s["Files_Scanned"]
    ]
    status = []
    if missing_code:
        status.append(f"<strong>No outputs yet:</strong> {esc(', '.join(missing_code))}.")
    if not has_redlyne:
        status.append(
            "<strong>No Redlyne results yet.</strong> Run "
            "<code>python run_redlyne.py</code> to fill in RQ1 and the matrix."
        )
    elif missing_scan:
        status.append(f"<strong>Not scanned by Redlyne:</strong> {esc(', '.join(missing_scan))}.")
    status_html = (
        f'<div class="status">{" ".join(status)}</div>' if status else ""
    )

    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    rq1_max = 100

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DeVAIC Study Results</title>
<style>{css}</style>
</head>
<body>
<main>
<h1>DeVAIC Study Results</h1>
<p class="sub">Five code origins on the same 20 Bottle tasks: the original human code,
two open-weight models run locally, and two closed commercial models.
AI origins have 3 outputs per task. Qwen, Gemma and ChatGPT were generated on the revised
prompts with temperature 0.2 and seeds 43–45; the Gemini outputs were made earlier in the
Gemini web interface, where the prompts differed and the model version and temperature are unknown.</p>
{status_html}

<h2>RQ1 · Vulnerability rate by code origin</h2>
<p class="note">Share of files with at least one Redlyne vulnerability.</p>
{legend()}
<div class="chart">{bar_chart(summary, "Vulnerability_Rate_Pct", "Vulnerability rate by code origin", "%", 0, rq1_max)}</div>

<h2>Vulnerability matrix · vulnerabilities per task</h2>
<p class="note">Mean Redlyne vulnerabilities per file — each OWASP category counted once per file, as in the Redlyne extension (AI origins averaged over 3 runs).
Darker = more vulnerabilities · 0 = none found · — = no outputs scanned.</p>
<div class="chart">{heatmap(tasks, cells)}</div>

<h2>RQ2 · Code length vs. complexity</h2>
<p class="note">Means over syntactically valid files. Longer code (SLOC) with similar cyclomatic
complexity means more lines without more control-flow branching.</p>
{legend()}
<div class="grid">
  <div class="chart"><h3>Source lines of code (SLOC)</h3>{bar_chart(summary, "Mean_SLOC", "Mean SLOC")}</div>
  <div class="chart"><h3>Cyclomatic complexity</h3>{bar_chart(summary, "Mean_Cyclomatic_Complexity", "Mean cyclomatic complexity")}</div>
  <div class="chart"><h3>Maintainability index (0–100)</h3>{bar_chart(summary, "Mean_Maintainability_Index", "Mean maintainability index", max_value=100)}</div>
</div>

<h2>Where the vulnerabilities are</h2>
<p class="note">Every line Redlyne flagged, grouped by task. Line numbers refer to the cleaned
file in clean_outputs/ (comments and docstrings removed). One vulnerability can be flagged on
several lines.</p>
<div class="table-wrap">{locations_table(findings) if findings else '<p class="note">No Redlyne results yet.</p>'}</div>

<h2>Summary table</h2>
<div class="table-wrap">{summary_table(summary)}</div>

<p class="note" style="margin-top:24px">Generated {generated} by build_report.py from
{METRICS_CSV}{" and " + REDLYNE_CSV if has_redlyne else ""}.
Metrics: Radon. Security scan: Redlyne {esc(redlyne_version)} (DeVAIC rule set).</p>
</main>
</body>
</html>
"""


def main():
    metrics = read_csv(METRICS_CSV)
    redlyne = read_csv(REDLYNE_CSV)

    if not metrics:
        print(f"Error: '{METRICS_CSV}' not found or empty; run get_metrics.py first.")
        sys.exit(1)

    tasks = sorted(
        os.path.splitext(name)[0]
        for name in os.listdir(TASKS_DIR) if name.endswith(".txt")
    )
    summary = summarize(metrics, redlyne)
    cells = build_matrix(tasks, redlyne)
    redlyne_version = next(
        (r.get("Redlyne_Version") for r in redlyne if r.get("Redlyne_Version")), "—"
    )

    write_outputs(summary, tasks, cells)
    with open(os.path.join(RESULTS_DIR, "report.html"), "w", encoding="utf-8") as f:
        f.write(build_html(
            summary, tasks, cells, bool(redlyne), redlyne_version,
            read_csv(FINDINGS_CSV),
        ))

    for s in summary.values():
        print(
            f" {s['Origin']:<20} files={s['Files']:<3} SLOC={fmt(s['Mean_SLOC'])}"
            f" CC={fmt(s['Mean_Cyclomatic_Complexity'])}"
            f" MI={fmt(s['Mean_Maintainability_Index'])}"
            f" vuln={fmt(s['Vulnerability_Rate_Pct'], 0, '%')}"
        )
    print(
        f"\n✓ Report written to '{os.path.join(RESULTS_DIR, 'report.html')}'"
        " (plus origin_summary.csv and vulnerability_matrix.csv)."
    )


if __name__ == "__main__":
    main()
