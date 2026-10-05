---
description: Organizational visualization standards for charts in notebooks and Python
applyTo: "**/*.ipynb,**/viz/**/*.py,**/*plot*.py,**/*chart*.py"
---

# Visualization standards

<!-- TODO(content): align applyTo with the real folder where chart code lives. -->

- Call `org_style.apply()` once before plotting. Take colors from `org_style.PALETTE` and its named colors, never hex literals.
- Titles state the insight ("Deposits grew 12% YoY"), not the metric name.
- Format numbers for the reader: `45.2%`, `$1.2M`, `2.3K`.
- Bar charts start at zero; categories sorted by value unless there is a natural order.
- Save figures with `org_style.save(fig, name)` so size, DPI and output folder are consistent.

<!-- TODO(content): add the team's chart rules (logo, footer with source, allowed chart types, presentation sizes). -->
