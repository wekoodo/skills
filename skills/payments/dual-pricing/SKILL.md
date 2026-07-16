---
name: dual-pricing
description: "Domain knowledge for dual pricing — what it is, the three distinct pricing models (dual pricing, cash discount, surcharge) and how they differ, Visa/Mastercard/Amex/Discover network rules, disclosure requirements, receipt rules, US state and international legal landscape, and merchant/customer experience considerations. Use this skill whenever working on any feature, system, or integration that involves dual pricing, cash vs card price differentiation, payment method-based pricing, surcharges, cash discounts, processing fee recovery, or compliance with card network pricing rules — regardless of platform or technology stack."
license: MIT
metadata:
  author: wekoodo
  version: "1.0"
---

# Dual Pricing

Platform-neutral reference on dual pricing and its sibling models: what they are, how they differ, the rules governing them, and the merchant and customer experience implications.

## A Note on Terminology

"Dual pricing" is used in two related but distinct senses, and this document is careful to keep them separate:

1. **As an umbrella concept** — offering different prices for the same product or service based on the customer's payment method. This is the general industry usage and the reason this document is titled "dual pricing."
2. **As a specific pricing model** — one of three models (alongside cash discount and surcharge) where both the cash price and the card price are visibly displayed side by side from the start.

Throughout this document, **"dual pricing" refers to the specific model** except where explicitly called out as the umbrella concept. The three specific models discussed are **Dual Pricing**, **Cash Discount**, and **Surcharge** — they are legally, operationally, and perceptually distinct and should not be used interchangeably.

## Why Merchants Adopt Payment-Method Pricing

In 2023, US merchants paid $224 billion in card processing fees — a 30% jump year-over-year (volumes have continued to grow since). For businesses with thin margins, even a 3% processing fee represents a significant profit leak. When implemented correctly, any of the three models can recover 70–90% of processing costs.

**How it differs from a uniform price increase:** Payment-method pricing is transparent — customers who want to avoid the card markup can do so by paying cash (or, in the case of dual pricing, by seeing both prices before they decide). Raising all prices uniformly to cover card fees is opaque and gives customers no choice.

## How the Three Models Differ at a Glance

| | Dual Pricing | Cash Discount | Surcharge |
|---|---|---|---|
| Prices displayed | Both cash and card, side by side | Only the card price (the higher one) | Only the cash price (the lower one) |
| Cash customer pays | Cash price (listed) | Card price minus a discount | Listed amount |
| Card customer pays | Card price (listed) | Card price (listed) | Listed amount plus a fee |
| Customer perception | Fully informed choice | Cash payer "saves" | Card payer "pays extra" |
| Legal exposure | Lowest — not framed as a surcharge | Low — accepted broadly | Higher — banned or restricted in some US states |
| Compliance overhead | Minimal | Low | Highest — registration, caps, state review |

**Dual pricing** is the most transparent approach: two fully-listed prices are displayed side by side from the start, and the customer chooses with full visibility. **Cash discount** displays only one listed price (the higher, card-inclusive price) and applies a discount at checkout for cash payers. **Surcharge** displays only the lower cash price and adds a fee at checkout for card payers — which regulators and customers both tend to treat as a surprise penalty.

## The Three Models

### Dual Pricing (recommended)

Both the cash price and the card price are displayed side by side at every price touchpoint — product pages, menus, shelves, cart, checkout, and receipts.

- **Customer psychology:** most positive — customers have full information and an active, informed choice before they pay
- **Display:** every price touchpoint shows both cash and card amounts
- **Receipt:** shows the total for the payment method actually used; no "discount" or "surcharge" line item needed because the customer already saw both prices up front
- **Legal exposure:** lowest of any model — no surcharge framing, no hidden fees, transparent to regulators and customers alike
- **Card networks:** fully permitted by Visa, Mastercard, Amex, and Discover, with no surcharge-registration obligations (the card price is simply the listed price, not a surcharge added on top of one)
- **Best for:** most merchants — especially online storefronts where both prices can be displayed automatically, and any merchant prioritizing customer trust and compliance simplicity

### Cash Discount

Only the card price is displayed as the listed/advertised price. Cash customers receive a discount at the register or checkout equal to the card processing markup. In other words, the merchant raises all prices to cover card costs, displays the higher price, and rewards cash payers with a discount.

- **Customer psychology:** positive — customers feel rewarded for paying cash, though they do not see the cash price until they opt to pay with cash
- **Display:** one price at product touchpoints (the card price); the discount surfaces only at the payment stage
- **Receipt:** shows the discounted total for cash payers; shows the standard card price for card payers — no extra line items
- **Legal exposure:** low — generally accepted in all US jurisdictions that permit any payment-method pricing, because the difference is framed as a discount rather than a fee
- **Card networks:** fully permitted under Visa and Mastercard rules; no surcharge registration required
- **Best for:** brick-and-mortar merchants with counter staff who explain the discount at payment time, and merchants who do not want to maintain two visible prices at every display touchpoint

### Surcharge

The cash price is the listed/advertised price. A fee is added at checkout for card payments.

- **Customer psychology:** most negative — customers can feel penalized for using a card, especially when the fee first surfaces at payment
- **Display:** one price at product touchpoints (the cash price); the surcharge surfaces only at checkout or payment
- **Receipt:** the cash price is the base, with an itemized surcharge line added for card payers
- **Legal exposure:** highest — banned or restricted in some US states; requires jurisdiction-specific compliance review before adopting
- **Card networks:** permitted but capped, and requires advance registration with each network before going live
- **Best for:** industries where surcharging is already the norm (some B2B, professional services, utilities); generally not recommended when dual pricing or cash discount are viable alternatives

## The Math

For a $100 base item with a 3% card-side markup:

| Model | Price(s) displayed | Cash customer pays | Card customer pays |
|---|---|---|---|
| Dual Pricing | $100 cash / $103 card (both shown) | $100 | $103 |
| Cash Discount | $103 (card price only shown) | $100 (3% discount applied) | $103 |
| Surcharge | $100 (cash price only shown) | $100 | $103 (3% surcharge added) |

The end totals are identical across all three models. What differs is what the customer sees before they decide, their perception of the price difference, the receipt formatting, and the legal treatment.

## Card Network Rules

All four major US card networks permit payment-method pricing but impose specific conditions that primarily target the **surcharge** model. Violations can result in fines or suspension of the merchant's ability to process that network's cards.

Dual pricing and cash discount programs generally do not trigger surcharge registration or caps, because they are not structured as surcharges. Disclosure rules still apply.

### Visa
- **Surcharge cap:** the lesser of the merchant's **actual average effective Merchant Discount Rate (MDR)** or **3%** — whichever is lower
- **30-day advance registration:** merchants must notify **their acquirer (processor)** at least 30 days before implementing any surcharge program. The processor then handles compliance reporting to Visa.
- **Disclosure points:** surcharge must be disclosed at (1) point of entry, (2) point of sale, and (3) on the receipt
- **Debit cards:** surcharges on debit card transactions are **prohibited**
- **Receipt rule:** the displayed card price must be the total on the receipt — no service fee appended after the fact

**How the "actual cost" cap works in practice (especially Interchange+ pricing):** Merchants calculate their historical average effective MDR from the most recent processor statements (typically the last 30–90 days of Visa credit-card volume and total fees paid). Software applies this **fixed percentage** uniformly at checkout. Real-time per-transaction interchange is not used; the fixed rate is what must stay under the cap. Processors often provide this average or tools to compute it.

### Mastercard
- **Surcharge cap:** the lesser of the merchant's **actual average effective MDR** or **4%** (or actual cost of acceptance, whichever is less)
- Same 30-day advance acquirer notification requirement (processors handle Mastercard compliance filings)
- Same three-point disclosure requirement
- Debit card surcharging prohibited

### American Express
- **Surcharge cap:** generally aligns with the lowest network cap in practice (typically Visa’s 3% for most merchants due to network parity rules)
- Amex has its own Merchant Regulations (updated biannually) and registration process through the Amex merchant portal. Consult your processor for the exact steps.
- Same three-point disclosure requirements apply

### Discover
- **Surcharge cap:** the lesser of the merchant's **actual average effective MDR** or **4%** (or actual cost of acceptance, whichever is less) — aligned with Mastercard and Amex
- Same 30-day advance acquirer notification requirement
- Same three-point disclosure requirements apply
- Same network parity principle: effective cap is the lowest across networks the merchant accepts

### Cross-network principle

The customer must never be surprised. Whatever price is shown at the start of the purchase must be exactly what appears on the receipt — no additional fees introduced for the first time at the end of the transaction. This is as true for dual pricing and cash discount models as it is for surcharge programs.

Modern processors typically calculate and enforce the compliant surcharge rate once the merchant is registered, and handle the network compliance filings. Confirm current requirements with the specific processor — automation varies.

## Disclosure Requirements

Compliance begins with visibility. The governing principle: **any place a price appears, both prices must appear** (or the pricing methodology must be clearly disclosed nearby).

### Required disclosure touchpoints

| Touchpoint | Requirement |
|---|---|
| Point of entry (store entrance, website homepage) | Notice explaining that two prices exist and how they work |
| Product / item listing (menu, shelf, product page) | Both cash and card prices shown (dual pricing); or the listed price plus a clear note about the cash discount or card surcharge |
| Point of sale / checkout | Both prices visible; selected total matches the chosen payment method |
| Receipt / order confirmation | The price corresponding to the actual payment method — no additions that were not previously disclosed |

### What disclosure must say

A compliant disclosure covers three things:
1. That two prices exist
2. Which is the cash price and which is the card price
3. How the difference is calculated or what it represents

Plain-language example: *"We offer two prices: a Cash Price and a Card Price. The Card Price includes a processing fee that covers the cost of accepting credit and debit cards. You may always pay the Cash Price with cash, check, or debit."*

Labeling clarity matters. "Card price" and "cash price" are unambiguous. "Service fee," "convenience fee," and "processing fee" mean different things to different customers and create confusion — avoid them as primary labels.

### Receipt rules

- **Cash payment:** receipt shows the cash total. No reference to what the card price would have been.
- **Card payment:** receipt shows the card total. No extra "processing fee" or "service fee" line appended after the subtotal — the card price is the total, not a base plus a fee.
- **Surcharge model only:** an itemized surcharge line on card receipts is acceptable, but the amount must exactly match what was disclosed before payment. Nothing on the receipt should be new information to the customer.

## Price Consumers: Crawlers vs. Catalog Syncs

Any system that stores and serves dual prices must handle two fundamentally different consumers, each of which needs a different price — and confusing them creates either a compliance violation or a broken external catalog.

### Card network crawlers must see the card price

Card networks (Visa, Mastercard, etc.) audit merchant compliance by crawling store pages and reading structured data — HTML, JSON-LD product schema, Open Graph tags, and similar outputs. They compare the price a customer would see on a product page against what appears on receipts.

**The rule:** the card price must be the merchant's advertised/listed price. If a crawler sees $18.00 on the product page but receipts show $18.54 for card purchases, the network interprets this as the merchant advertising a lower price than what is actually charged — a compliance violation. The card price must be what is visible to any user or bot rendering the store.

This means:
- The card price should be the value returned by any public-facing price rendering path
- Structured data outputs (JSON-LD `price`, Open Graph `og:price:amount`, etc.) must reflect the card price
- Any price a search engine or compliance bot could read must be the card price

### Third-party catalog syncs need the raw cash price

Inventory and catalog sync tools — Amazon, eBay, POS systems, ERP integrations, comparison shopping engines — typically pull product data programmatically via an API. These tools use the price they receive to populate the merchant's listings on external platforms. If they receive the inflated card price, that becomes the price advertised on Amazon or eBay, which is almost certainly not what the merchant intends.

**The rule:** programmatic catalog reads should always receive the raw cash price — the merchant's base price before any payment-method markup is applied. This ensures external listings reflect accurate, merchant-intended pricing.

This applies to:
- Any product API endpoint used by sync integrations
- Data feeds (CSV, XML, JSON) exported for external catalog use
- Backend administrative reads used by inventory or pricing management tools
- CLI or scripted data access that bypasses the customer-facing storefront

### Why the two requirements seem to conflict — and how they don't

At first glance these requirements pull in opposite directions: public-facing output must show the card price, but programmatic output must show the cash price. The resolution is that the two consumers access data through different paths:

- **HTML rendering / structured data** → card price (what customers and compliance bots see)
- **API / data feeds / admin interfaces** → cash price (what sync tools and backend systems use)

An implementation that conflates these paths — serving the same price to both — will either expose inflated prices to external catalogs or expose cash prices to network compliance crawlers. Both outcomes are wrong. The system must be aware of the consumer context and serve the appropriate price accordingly.

### Practical implication for any implementation

Before writing any price-serving code, identify which consumer category each path serves:

| Access pattern | Consumer | Price to serve |
|---|---|---|
| Rendered storefront HTML | Customers + network crawlers | Card price |
| Product structured data (JSON-LD, schema.org) | Search engines + network crawlers | Card price |
| Product API / data feed | Catalog sync tools, POS, ERP | Cash price |
| Admin / backend UI | Merchant managing inventory | Cash price |
| Receipt / order confirmation | Customer post-purchase | Price matching payment method used |

Any dual pricing implementation that doesn't explicitly account for this split is incomplete, regardless of platform.

### Payment-method classification: which methods can serve cash pricing

A separate question, downstream of price-consumer split: of the payment methods a merchant accepts, which ones should serve the cash price at checkout, and which should serve the card price? The naive answer — "non-card methods get cash pricing, card methods get card pricing" — is correct but insufficient as a UX specification, because real-world payment methods don't cleanly bucket into "card" and "non-card."

Three practical buckets:

**Cash-equivalent.** Methods where the merchant pays no per-transaction processing fee, or fees so small they don't warrant fee recovery. Direct bank transfer (ACH / wire), check, cash on delivery, peer-to-peer payment apps that settle to bank (Zelle, some Venmo / Cash App configurations). These genuinely belong on the cash side of the price split — the merchant collects the cash price, no fee is absorbed, no markup is needed. The merchant should be encouraged to mark these as cash-pricing methods.

**Card processors.** Methods where the customer's funds reach the merchant via card-network rails (Visa, Mastercard, Amex, Discover) and the merchant pays per-transaction interchange + processing markup. Direct card gateways (the merchant's primary card processor — Stripe, Square, Authorize.net, processor-branded gateways like a PayArc or North adapter) and any "pay with card" button hosted by a third party (PayPal's Standard Card Button, Apple Pay or Google Pay when funded by a card). These should NEVER serve cash pricing — the merchant would pay the card fee on the lower price and lose money on every transaction. A merchant-facing UI that lets the merchant configure the cash-side allowlist should treat these as ineligible (greyed-out / disabled) rather than as a free choice. Hard-disable, not warn — the only reason to mark a card processor as cash-side is a misunderstanding of the model.

**Ambiguous.** Methods that aren't pure card-network transactions but DO carry per-transaction processing fees comparable to card processing. PayPal's smart button (the customer's PayPal balance, linked bank, or linked card all clear through PayPal's fee structure), regional bank-direct methods routed through aggregators (iDeal, Bancontact, Trustly when surfaced via PayPal or Stripe), and BNPL services (Klarna, Afterpay) all sit here. Visa/MC compliance rules don't directly govern these — they're not card transactions in the strict sense — but the merchant economics are the same: setting the method to cash-pricing means the merchant absorbs the processing fee on the lower price. The right UX treatment is to allow the merchant to mark these as cash-side if they have a specific reason (sometimes promotional or partnership-driven), but with an explicit warning that processing fees apply. The compliance self-check should not credit these toward "a non-card method is enabled" — only true cash-equivalents satisfy that requirement.

The distinction matters because dual pricing's customer-facing promise is that the cash price is what you pay if you avoid the merchant's card processing cost. Letting a merchant route PayPal smart-button transactions through cash pricing breaks that promise on both sides — customers pay "cash" prices for a method that isn't cash, and merchants eat the fee they were trying to recover.

## Legal Landscape

### United States — Federal Level

Payment-method pricing is generally legal at the federal level. The 2010 Durbin Amendment, which capped debit card interchange fees for large issuers, drew attention to card processing costs and opened the door to mainstream payment-method pricing.

For many years, major card networks prohibited payment-method pricing through merchant agreements. Legal challenges resolved this, and all major networks now permit dual pricing, cash discount, and surcharge models with the conditions described above.

### US State Variations

State law creates a patchwork of requirements. As of 2026, surcharge prohibitions or strict limits remain in effect in states such as **Connecticut, Massachusetts, Maine, California (SB 478)**, **Puerto Rico**, and others with additional rules (e.g., Colorado at a 2% cap, New York with display restrictions). Merchants should always verify current law in their operating state (or use a compliance service) before choosing the surcharge model.

- **Dual pricing advantage:** Dual pricing — displaying both cash and card prices side by side — typically falls outside the scope of state surcharge bans entirely, because no surcharge is being added to an advertised price. The customer sees both prices up front and chooses between them. This makes dual pricing the safest model across US state jurisdictions.
- **Cash discount advantage:** In states with surcharge restrictions, the cash discount model is also generally safe because it frames the difference as a discount rather than a fee. Less transparent than dual pricing, but still avoids most surcharge-specific legislation.

Merchants operating across multiple states need location-specific policies. For online merchants, consider which state's law governs: the merchant's location, the customer's billing address, or the customer's shipping address.

### International

- **European Union:** Dual pricing and cash discount programs are generally permitted. The Payment Services Directive (PSD2) bans excessive surcharges but allows merchants to pass on their actual card acceptance costs when surcharging is used.
- **Australia:** All three models are permitted; transparent dual pricing is encouraged. Surcharges are capped at the merchant's actual cost of acceptance — excessive surcharging is prohibited.
- **Canada:** All three models — dual pricing, cash discount, and surcharge — are permitted. Credit card surcharging specifically became allowed in 2022 under Visa and Mastercard merchant agreements following legal settlements; dual pricing and cash discount have been permitted longer and carry less compliance overhead. Quebec has additional consumer disclosure requirements.
- **United Kingdom:** Consumer card surcharges are banned under the Payment Services Regulations 2017. **Dual pricing (displaying both prices) and cash discount programs remain permitted** because neither involves adding a surcharge to the advertised price of a consumer card transaction. Business card surcharges may still apply in some B2B contexts.

When operating internationally, verify local law before implementing any model. Dual pricing generally carries the lowest cross-border legal risk because it avoids the "surcharge" classification entirely; cash discount is a close second.

## Merchant Considerations

### Financial impact

Payment-method pricing's core value is processing cost recovery. Beyond direct savings, cash payments settle immediately — unlike card transactions, which carry a 24–72 hour settlement delay. This improves working capital for cash-flow-constrained businesses.

Estimated annual processing costs and recovery potential by business type:

| Business type | Monthly card volume | Typical processing fee | Annual cost | Potential recovery |
|---|---|---|---|---|
| Restaurant | $100,000 | 3.0% | $36,000 | $25,200–$32,400 |
| Retail store | $75,000 | 2.5% | $22,500 | $15,750–$20,250 |
| Service business | $50,000 | 2.8% | $16,800 | $11,760–$15,120 |
| E-commerce | $120,000 | 2.9% | $41,760 | $29,232–$37,584 |

### Accounting and reconciliation

Payment-method pricing requires tracking sales separately by payment method. Surcharges and discounts must be categorized correctly for tax and financial reporting. Capturing the payment method at the transaction level — and routing the resulting amounts into the right accounting entries — is required for any of the three models.

### Staff training

Staff need to be able to explain the pricing structure clearly, without apologizing or creating uncertainty. They also need to process transactions correctly for the chosen model and handle edge cases like partial cash payment, split tenders, and refunds.

Effective framing under a dual pricing model: *"We show two prices — one for cash and one for card — so you can choose. The card price includes a small processing fee. Which works better for you?"*

Effective framing under a cash discount model: *"We reward customers who pay with cash with a lower price. Card payments include a small fee that covers what the card company charges us — but you can always avoid it by paying cash."*

## Customer Experience Considerations

### Framing determines reception

Research consistently shows that customers respond very differently to the same price difference depending on how it is framed:

- **Dual pricing display (both prices shown upfront)** → customer feels informed and in control (most positive)
- **"Cash discount" framing** → customer feels rewarded (positive)
- **"Card surcharge" framing** → customer feels penalized (negative)
- **Percentage vs. dollar amount:** Customers perceive percentage-framed discounts more favorably than equivalent dollar amounts, especially when the amount is relatively large.

68–72% of customers prefer transparent pricing that separates fees from the base price — they appreciate understanding why prices differ, even when the total they pay is identical.

### Eliminating friction

The most damaging customer experience failure is late disclosure — introducing the price difference for the first time at the final checkout step. Studies show 36% of customers abandon online shopping carts because of unexpected costs at checkout. The same effect occurs in physical stores.

Rules for minimizing friction:
- Show both prices at every touchpoint where any price appears — not just at checkout (this is mandatory under the dual pricing model, and strongly advised even under cash discount and surcharge models)
- Use consistent labels throughout the purchase journey
- Never let the final receipt total surprise the customer

### Handling objections

Most customer pushback dissolves with a simple, confident explanation. A useful approach: *"We show a cash price and a card price — cash customers pay less because there's no processing fee. Which works better for you?"* Giving the customer an active, informed choice, rather than presenting a rule imposed on them, defuses most objections.

## Key Rules Summary

1. **Three distinct models — use terms precisely:** *Dual Pricing* (both prices displayed side by side), *Cash Discount* (card price displayed, discount applied at checkout for cash payers), and *Surcharge* (cash price displayed, fee added at checkout for card payers). They are not interchangeable.
2. **Dual pricing is the safest and most transparent model** — it avoids surcharge framing entirely and carries the lowest compliance risk and the best customer perception.
3. **For dual pricing specifically, both prices must appear wherever any price is shown** — product pages, cart, checkout, receipts, and anywhere else a price surfaces.
4. **Surcharge caps:** determined by the merchant’s historical average MDR or the network cap (Visa 3%, Mastercard 4%, etc.), whichever is lower. Network parity typically caps the effective rate at the lowest cap across networks. No network allows surcharging debit cards.
5. **Register with your acquirer/processor 30 days before going live** with any surcharge program (not required for dual pricing or cash discount models).
6. **Receipt totals must never surprise** — what the customer sees before paying must match what appears on the receipt, regardless of model.
7. **Verify state law before choosing the surcharge model** — dual pricing and cash discount avoid most state-level legal risk.
8. **Transparency is the compliance principle** — every rule flows from the requirement that customers must never be deceived or surprised about what they are paying.