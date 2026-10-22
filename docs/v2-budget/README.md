# STM v2 at UCSD: budget

`STM_v2_budget.xlsx` is the budget for building a second STM at UCSD. It is written for Prof. Oscar Vasquez and the UCSD budget office. It has two tabs:

- **v2 budget.** This is the main tab. It opens with a summary of the four possible totals and a short "How to read this sheet" guide that explains what an STM is and defines the few technical terms used. Every part is grouped by what it does in the microscope. Each part has a plain description of what it is for, a "Compared with v1" note saying whether it is new or changed and why, the seller, the part number, the quantity, the price, where the price came from (catalog, v1 receipt or estimate) and a link.
  - Sections 1 to 7 are a complete, working microscope built around v1's piezo disc, which the main board drives directly. Section 7 is the batteries: the whole microscope runs on batteries, with no wall power.
  - Section 8 is the optional **piezo tube upgrade** (Prof. Vasquez's suggestion): the tube, its mount and wiring, a battery-powered high-voltage driver, and its own shipping and import fees. One **Yes/No switch** adds it to or removes it from the total. The switch starts at **No**: our studies recommend building without the tube first. A spare tube is an optional row inside it, set to **No**.
  - Every purchase line in sections 1 to 8 has a **Fund?** choice (Yes/No; Yes by default, except the few rows marked optional, which start at No) so the professor or budget office can mark what to pay for. **No** removes the line from every total, along with any shipping or import fee that only that line needed.
  - Section 9 lists items a UCSD lab may already have. Choosing **Yes** in its last column takes that item off the total.
- **v1 (what it cost).** This tab shows what the first instrument actually cost, $1,408.43. The 42 Amazon purchases are grouped into plain categories.

| v2 total | UCSD supplies nothing in section 9 | UCSD supplies everything in section 9 |
|---|---|---|
| Without the piezo upgrade | $2,619.08 | $1,644.91 |
| With the piezo upgrade (spare tube not included) | $3,292.19 | $2,318.02 |

v1 actually cost $1,408.43, including the three 1/4-80 brass bushings for the adjustment screws, which were missing from earlier versions of the v1 tab.

Prices were checked on 2026-10-21, in USD. The JLCPCB circuit boards are priced at what v1 paid in July 2026. The high-voltage driver circuit is not designed yet, so its parts are estimates, as are the tube mount and wiring parts. Every total includes shipping, the 35% US tariff on circuit boards, other import fees, 7.75% sales tax and 10% spare money.
