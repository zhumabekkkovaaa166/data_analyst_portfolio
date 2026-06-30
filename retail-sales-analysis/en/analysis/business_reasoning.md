# How I approach metric selection

This document is about thinking, not SQL. The queries live in [`../queries/`](../queries).
What matters here is the core skill: **how a business question becomes a metric**, and
where the brief diverges from what the metric actually measures.

> The principle the whole project is built on:
> **a metric is not derived from the data — it's derived from the decision it will support.**
> So my first question is never "what columns do I have", but
> "what decision should this answer support?".

---

## Same SQL, different metrics

Three challenges (Top Customers, Best Products, Supplier Performance) use nearly
identical SQL. Yet their metrics differ — because the **decisions** differ. This is the
key lesson for me: the metric is set by the physics of the decision, not by the data.

| Challenge | Decision verb | What I measure | Why |
|---|---|---|---|
| Top Customers | reward a customer | money — `SUM(Price * Quantity)` | customer value is counted in currency |
| Best Products | restock a shelf | units — `SUM(Quantity)` | a warehouse doesn't care if an item is cheap or dear |
| Supplier Performance | choose a partner | turnover — `SUM(Price * Quantity)` | negotiation priority by volume |

If I'd used revenue in the restock task, one expensive low-volume product would top the
list — and purchasing would restock the wrong thing. The metric is dictated by how the
result will be used.

---

## Where the brief is broader than the metric

In several challenges the word in the brief promises more than the query computes.
Spotting that gap is the analyst's core value. I don't silently compute what was asked —
I state what's actually measured and where it diverges from intent.

### "Loyal" customers (Challenge 2)

The brief asks for **loyal** customers; the metric computes **total spend**. Not the
same thing. Loyalty is regularity and retention (how often they return, how long
they've been with us). A large total can be a single big order — a whale, not a loyal
customer. In production I'd build **RFM** (recency, frequency, monetary), not a raw
`SUM`. Otherwise the offer goes to someone who bought once and left.

### Employee performance and Goodhart's Law (Challenge 4)

`COUNT(orders)` is a volume metric, but a bonus should reflect contribution. Once it
drives pay, **Goodhart's Law** kicks in: "when a measure becomes a target, it ceases to
be a good measure." People optimize the counter — splitting orders, taking only easy
ones, trading quality for volume. So when handing such a metric to HR, I'm obliged to
flag the risk and propose a bundle (revenue/margin per employee + a quality signal)
that's harder to game alone.

### Supplier "profitability" (Challenge 6)

What's computed is turnover of a supplier's products on the sales side, not the
profitability of working *with* them. A contract decision should weigh purchase cost,
supply reliability, and dependency risk (60% of turnover on one supplier is a risk, not
just a plus). "How much of their product we sold" answers "who matters by turnover" —
fine for prioritizing negotiations, but calling it "profitability" is strictly wrong.

### "CLV" (Final)

What's computed is **historical** cumulative revenue, not CLV in the strict sense. True
Customer Lifetime Value is a *predictive* quantity: how much a customer will bring in
the *future*, accounting for churn probability. Here it's the sum of the past. Fine to
call it "simplified CLV", but the difference matters: a customer with a large historical
total may already have churned.

---

## Segment thresholds: absolute vs. quantiles

In the final challenge the High/Medium/Low boundaries are round numbers (10000 / 5000) —
picked out of thin air. In real segmentation I set boundaries by **quantiles**, because
they're computed from the data itself:

| | Absolute threshold (10000) | Quantile (top 20%) |
|---|---|---|
| Where the boundary comes from | I set it by hand | computed from the distribution |
| How many land in High | unpredictable | a fixed share |
| Under growth / inflation | breaks, needs resetting | the boundary moves itself |

"Top 20%" = above the 80th percentile = top quintile. In Trino:
`ntile(5) OVER (ORDER BY revenue DESC)` to bucket, or
`approx_percentile(revenue, 0.8)` for the boundary value itself.

---

## Technical choices with business meaning

| Pattern | Rule | Why it's a business question |
|---|---|---|
| `WHERE` vs `HAVING` | `WHERE` before aggregation, `HAVING` after | "above the category average" filters groups -> `HAVING` |
| `GROUP BY` on dates | year and month together | otherwise same months across years collapse, trend disappears |
| `RANK` vs `ROW_NUMBER` | how ties are handled | dedup -> `ROW_NUMBER`; fair report ranking -> `RANK` |
| `CASE WHEN` + aggregate | runs after `GROUP BY` | segment thresholds are a hidden assumption — explain where they come from |

---

## The checklist I run before shipping any analysis

- [ ] What decision does this number support?
- [ ] Does the word in the brief ("loyal", "performance", "CLV") equal the metric, or is it broader?
- [ ] Is the metric in the right units (money / units / frequency)?
- [ ] If this becomes a KPI or bonus — how would it be gamed?
- [ ] Thresholds: absolute (fragile) or relative (quantiles)?
- [ ] Does the time granularity reveal what was actually asked?
