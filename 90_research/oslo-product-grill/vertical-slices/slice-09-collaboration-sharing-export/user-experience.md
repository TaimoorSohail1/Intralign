# Slice 9 — Collaboration, Sharing & Export · User Experience

> ## ⚑ AMENDED 2026-07-11 — the ratified register (D123 · D124 · D125 · D126)
> Passages below that pre-date this amendment are **superseded, not deleted** — read them together with the **AMENDMENT** section at the end of this document, which wins. The one-line governing principle (**D126**):
>
> > **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**
>
> Headlines: **tier gating is LIVE in Alpha** (D123 — Basic is purchasable; this *reverses* the earlier N-1 advice) · **two limits, never conflated** (D124 — PHASE invites vs TIER seats; the product must always name which one blocked you) · **reviewer grants are FREE and UNMETERED on every tier in every phase** (CR-2 — structurally required) · allocation **Basic 5/mo · Free 2/mo** (CR-1/T-2) · **one identity** (N-2 — `Principal` + `Membership` + `ReviewGrant`; "Participant" is a *view*) · **no points economy** (CR-4) · **no pay-to-skip** (CR-7).


**Cumulative:** Slices 1–8 **+ Slice 9**. This slice fills the last two top-bar seams (**Share**, **Export**), un-gates the collaboration notification categories, and lands the centerpiece: **CRR — CAF Review Requests**. Everything from Slices 1–8 is preserved 1:1 (onboarding funnel, Overview, Attention map, full artifact editor, Issues, History + trend, Workspace Home, project switcher, notifications, Settings, theme, command palette, OSLO chat, feature tour).

Decisions encoded: **D110** (sharing dialog), **D111** (comments + @mentions), **D112** (export), **D113** (collaboration notifications un-gated + Settings → Collaboration), **D114** (CRR-01…05), **D115** (reviewer-response semantics — doctrinal), **D116** (reviewer view — **proposal, owner-open**), **D117** (share-link hygiene), **D118** (Free-tier CRR cap) — plus inherited **D001** advisory-only, **D002** confidence = neutral maturity, **D003** severity-only color, **D006/D088** analysis-update-only resolution, **D009** Panel Model, **D011** epistemic notation, **D048** visibility-first tiering, **D092** no user-facing "reanalysis" mechanism, **D096** append-only History.

---

## The one idea this slice turns on

**A stakeholder's answer is evidence, not truth.**

That single sentence shapes every surface here. When your sponsor says *"yes, the venue confirmed it"*, a lesser product closes the issue and moves on. OSLO does not. Their answer goes onto the record as **"Attested by Marcus Hale"** — a *third* kind of claim, sitting beside **"From OSLO"** (what OSLO worked out) and **"Confirmed by you"** (what you stood behind). It triggers a fresh analysis run, because more evidence is genuinely more to go on, and your **reliability** rises accordingly. But the issue **stays open**, the **assessment is not overwritten**, and **OSLO never accepts it on your behalf**. An approval is evidence that *a stakeholder approves* — never proof that the plan is sound. The call stays yours.

That is the whole difference between a review tool and an understanding tool.

---

## What's NEW in Slice 9

### 1. Sharing is real (D110) — was: *"Sharing — arrives in Slice 9"* toast
The top-bar **⤴** opens a **sharing dialog**: invite by email, pick a role, see who's on the project, and hand out a **view-only snapshot link**. Three participant types, each with **one plain line** about what they can do — *Owner* (can change the plan, share it, export it, send review requests), *Collaborator* (can comment and answer a review request, but can't change the plan), *Viewer* (can read the plan and OSLO's read of it — nothing else). The dialog says out loud that **roles are shown, not enforced** — there is no permission engine in R1, and pretending otherwise would be the lie.

The snapshot link is the honest part. It shows OSLO's read **as it stood when you made the link**. The moment analysis moves on, that link is relabelled **"previous analysis"** — and anyone opening it is told so. A stale read is never quietly passed off as current.

### 2. Comments live on the issue — and only on the issue (D111)
Threaded comments sit **inside the Issue Panel**. There is no comment inbox, no orphan thread surface — that would be a second place where the truth about an issue lives, and OSLO doesn't do that (Panel Model, D009). They are **append-only**: nothing is edited or deleted after the fact. `@` brings up your teammates, or **"Invite someone new…"** which drops you into the sharing dialog. Every comment lands on the **History** timeline.

And under the box, permanently: **"Comments never change the assessment."** Talking about the read is not the same as moving it.

### 3. Export says when the read was produced, and what it isn't (D112)
The top-bar **⤓** opens **Export a snapshot**. Two things are non-negotiable and always present: an **analysis-currency marker** (*"produced by the Extended run, 2h ago · Current"*) and the **disclaimer** — *this reflects understanding maturity, not project health, readiness, or probability of success*. A document that leaves OSLO and lands in a steering pack must not be able to be misread as a health score.

**Free gets PDF.** Copy and Link are shown, tier-locked, with a *See plans →* path — visible rather than hidden, so you can see what a plan buys you (D048). And: **"Export generates no new assessment and never triggers an analysis."** It writes down the read you already have.

### 4. CRR — send one issue out for review (D114)
This is the centerpiece. On an issue, **⤴ Share for review** sends **one thing** to **one person**: the finding, its context, OSLO's recommendation, and the artifact it came from. You see the **exact package** before you send it, you pick who gets it, and you can add a note.

**Validation recommendations are prime candidates** (REC-05) — a finding like *"venue Wi-Fi capacity is unconfirmed"* is not something OSLO can think its way out of. Somebody has to phone the venue. On those issues, *Share for review* is the **primary** action, and OSLO says why.

They respond with exactly one of four things: **Comment · Approve · Reject · Suggest Alternative**. Structured, preserved in full, shown on the issue forever.

**And when they *take a position*, OSLO learns something specific — about alignment (D133).** A stakeholder saying *"this doesn't read right to me"* is not just noise on the record; it is **evidence about Alignment**, one of the three CAF dimensions. So a **Reject** moves Alignment down, and — **symmetrically, because neither direction is privileged** — an **Approve** moves it up. The response card says so plainly, and says what it does **not** mean:

> **Attested by Priya Raman · Folded into Alignment — as evidence (D133).** A stakeholder **disagreeing** with a finding is information about **alignment** specifically — whether the people who have to live with this plan actually read it the same way. So it moved **Alignment** in the analysis run above, and reliability with it.
> **What that does not mean:** OSLO has *not* concluded the plan is wrong, invalid, or that this finding is re-opened. Disagreement is not proof either. It is one attested input, weighed with everything else. An **Approve** and a **Reject** carry the same weight here — OSLO does not privilege the direction it is pointed in.

The read can therefore **fall** after a Reject. That is the honest outcome, and the trend line shows the fall **with its cause**. What never happens: the issue is never auto-resolved, never auto-re-opened, and OSLO never adopts the reviewer's view as its own. *"Priya rejected this"* — never *"this is now wrong."*

### 5. The workspace says where understanding is *blocked on a person* (CRR-05 / MRI-07)
Once a request is out, the issue wears an **"◷ Awaiting review · Marcus"** chip in the Issues list and the Issue Panel. And a new first-class block — **Understanding dependencies** — lands on **both** the Overview and the Attention map:

> **1 issue awaiting sponsor review.** OSLO can't firm up its read on this one until someone else answers. This isn't a weakness in the plan — it's where understanding is **blocked on a person**.

That is a genuinely different kind of blocker from a weak plan artifact, and it deserved its own block rather than being folded into severity. It is drawn in **neutral chrome**: waiting on somebody is not a severity (D003).

### 6. The reviewer's experience — **now a gated token grant** (D119; supersedes D116's no-account view)
*Preview reviewer view →* shows exactly what the recipient gets. The link they were sent **carries a token that grants them Reviewer Principal access** (DL-049), scoped to **exactly that package**. They land on a one-click grant — *"Idris invited you to review one finding"* — and go **straight into the package**: **no password, no signup wall, and never anonymous.** The invite *is* the authentication. They read the finding in context, and answer. **Only after they answer** does OSLO offer them anything for themselves: *"Want to see your own plan the way they see theirs?"* Never before value.

This surface carries a permanent **"Proposal — pending owner ratification"** ribbon. The recipient experience is the binding constraint on the growth loop and is explicitly **owner-open** (virality audit P0). It is built so it can be *looked at* — not adopted by default. Anti-Assumption is honored: **proposed, not inferred.**

### 7. Links are revocable and scoped — and expiry is honestly unset (D117)
Every link is either **one snapshot** or **one issue package**, and every link can be **revoked**. A revoked link opens **nothing** — not even an old copy of the read. **Expiry has no ratified default**, so the control shows **"Not yet set — owner decision"** rather than a made-up 30 days.

### 8. Bound seats, never bound evidence (D120; reframes D118)
This is the crux rule of the whole controlled-release design, and getting it wrong would do real damage.

An invite is spent on **exactly one thing: admitting a new human to OSLO** — a collaborator seat, or a first-time reviewer. **Asking someone who is already here for their read costs nothing, forever, and is never metered.** A review request is not a marketing share. It is how you *get your answer*. Every request a product blocks is a user whose understanding it deliberately degraded — and a product whose entire claim is *"I will tell you the truth about your plan"* cannot do that to manage its own supply.

So the **Share for review** button is **never disabled**. The reviewer picker says the cost on the person, before you choose: **Marcus — "free — already in"**; **Dana — "new — admits them (cost owner-TBD · CR-2)"**. The allocation only ever bites when you try to bring in someone new, and when it does, the honest fallback is the **waitlist** — not an upsell.

`CRR_CAP` is still `null`. The **{N} per {period}** is an owner decision (**CR-1**) that has not been made, so the balance renders **unset** — never as a fake count and never as urgency.

### 9. Chat knows about all of it — and still won't act (D108/D109 machinery)
Ask OSLO *"what's blocking my understanding?"* and it names the issue, the person, and what will happen when they answer. Ask it about a response and it tells you what that response **did** (evidence → an analysis run → reliability rose) and, just as plainly, what it **did not do** (it did not close the issue; OSLO did not accept it for you).

Ask it to *send* the request, *accept* the response, or *resolve* the issue and it says: **"That one isn't mine to take."** Then it opens the **review package preview** so you can decide. The chat explains and hands you back to the surface that owns the action. It has never been able to act, and this slice does not change that.

---

## INHERITED (unchanged from Slices 1–8)

- **Onboarding funnel** — invite → activation → intake → Initial Analysis → orientation (Slices 1–2).
- **Overview** — confidence-led console: focal score, CAF maturity bars, reliability basis, false-confidence flag, Start here, Progress, More (Slice 3).
- **Attention map** — the co-primary heatmap (artifacts × Clarity/Alignment/Feasibility), neutral intensity ramp, all-clear state (Slice 4).
- **Artifact workspace** — the full rich-text editor: tables, provenance gutter, inline annotations, find/replace, slash menu, link popover (Slice 5).
- **Issues** — the all-issues surface, the Issue Panel, lifecycle Open → Addressed → Resolved, recommendations + Apply-this-fix, clarifications (Slice 6).
- **History & trend** — the append-only, run-grouped timeline + "Understanding over runs" (Slice 7). Slice 9 adds a **Collaboration** filter chip; comments, requests, responses, shares and exports are all events on the same append-only log.
- **Workspace, awareness, Settings, theme** — Workspace Home, project switcher, notifications, the eleven Settings sections, dark/light (Slice 8).
- **Shell** — persistent sidebar, top bar, confidence pill, ⌘K palette, OSLO chat rail, feature tour.


---

## AMENDMENT — Controlled Release & Demand (D119–D122)

### The invite is the authentication (D119)
The old reviewer view had a hole in it: *"no account needed"* is an **anonymous** product interaction, and Alpha forbids those (D021). The resolution isn't a signup wall — it's noticing that **a link sent to a named person by name is already an invitation**. The token in that link **grants them Reviewer Principal access** (DL-049), scoped to exactly the package they were sent. They are *identified and invited*, never anonymous. They click once. They never see a password field.

What they see first: *"Idris invited you to review one finding."* And underneath, plainly: **this link lets you into this one package and nothing else in DevNorth 2026** — not the rest of the plan, not the other issues, not anyone else's comments. Frictionless, and **granted** rather than anonymous.

### The waitlist, and why it exists (D121)
After they answer — **only** after — OSLO offers them something for themselves. Not an account: a **waitlist**, with the reason said out loud.

> *"OSLO is in Alpha, and we are deliberately limiting how many people we let in — not to make you want it, but because we can only do this properly for a small number of people at a time. So there's a waitlist, and it's a real one."*

Their position is their **actual position** (#5 of 5), out of a **real total**. What moves it — a converted referral, being **review-requested** by someone with a real plan, role/org fit — is stated. And so is what we don't know: **how much each of those is worth is an owner decision that hasn't been made (CR-4 / CR-5)**, so the list is in arrival order and says so, rather than showing an order we invented. The inviter can also simply **grant them a seat** from their own allocation, from the issue itself.

### The mechanism sunsets — visibly (D121)
Flip the phase bar to **Beta** and the same gate loosens. Flip it to **GA** and it **disappears**: the allocation reads *"Retired at GA"*, the waitlist reads *"Nobody waits. There is nothing to wait for."*, anonymous access is permitted (D021/D024), and the reviewer's convert-moment becomes an ordinary *Create your own project*. That is the whole point of building it this way: **scarcity here is a supply lever for the period when supply is genuinely constrained, and it is designed to kill itself.** It is not the business model.

### Why the honesty isn't decoration
OSLO's growth engine **is its epistemic credibility**. A product whose entire claim is *"I will tell you the truth about your plan, including what I don't know"* **cannot lie in its growth surfaces** — that would be self-refuting. So: no "3 spots left" unless there are exactly 3. No countdown. No dark pattern. And no charging you for the one thing the product exists to do: **ask someone what they know.**

### A share link is not an export link (escalation #2, resolved in the UI)
They were being confused because they were both called "a link". They are two different objects, and now they are labelled as two different objects, in both surfaces:
- **Share link** (D110) — view-only access to the **live project**, revocable, relabelled *"previous analysis"* when the read moves on. **Free.**
- **Export link** (D112) — a hosted copy of **one exported snapshot**, frozen at the moment you exported it. **Paid format.**

---

# AMENDMENT — D123–D126: what the user now actually experiences

## The one sentence the whole surface is built around (D126)

> **Meter who gets a seat. Never meter who gets an answer. And always say which limit you just hit.**

It is printed, verbatim, at the top of **Access & invites** and at the top of **Plans**.

## The moment that matters: being blocked

The user meets **two** limits in this product, and they feel completely different — deliberately.

**Out of invites (PHASE).** *"You're out of invites for this month. Replenishes 1 August."* Cool/blue box, labelled **"Phase limit — invites"**. It explains that this is about **how many new people you can bring into the Alpha**, not about your plan. It offers **the waitlist**. **It does not offer an upgrade.** It says, in plain words, that the queue is throttled by how many people we can onboard properly — and that **buying does not create onboarding capacity**, so we are not going to sell you a way past it. That refusal *is* the feature.

**Seats are full (TIER).** *"Free projects hold {N} collaborator seats — Basic holds more."* Brand/orange box, labelled **"Plan limit — collaborator seats"**. It says plainly that **your invites are untouched** (and shows how many you have left). It offers the **free remedy first** — *"a Viewer holds no seat; you can add them as a Viewer today"* — and then a genuine upgrade path.

Hit **both** at once and you see **both boxes**, separately. They are never merged into one "you've hit your limit" sentence, because that sentence is the dark pattern.

## The moment that matters most: asking for evidence

**Nothing blocks a review request. Ever.**

A user with **zero invites left**, on **Free**, in **Alpha**, sending to someone who has **never heard of OSLO**, still sends. The Share-for-review dialog says so out loud in that state:

> *"Your invite allocation is spent this month — and it makes no difference here. The allocation meters seats. It does not meter evidence. This request sends, free, right now."*

The reviewer picker prices every person the same way: **free**. A stranger reads *"free — a review grant costs nothing"*, and the panel underneath explains that they get a **scoped grant, no invite, no seat**, expiring when the issue resolves or in 14 days. The cost note is honest about who pays: *"every reviewer response triggers an Extended Analysis, which draws on a token budget (DL-048) — that is a **cost** control on compute, never a monetization gate. You are not charged, throttled or upsold for seeking evidence."*

## The waitlist a reviewer actually sees

Three bands, and they are named: **review-requested** · **referred by an active user** · **cold** — date-ordered inside each. A reviewer who just answered a real question lands in **band 1**, and is told why: *"someone with a real plan needed your read — that's the strongest signal we have."*

No points. No score. No credits. No "invite 3 friends and skip the line." No countdown. The reviewer is told, plainly, that admits are **hand-curated** and that **nobody can pay to get in faster**.

## Free is not a demo

Free gives the **entire core read**: intake → Fast Pass → Overview → Attention → Issues → **CRR review requests**, unlimited. The Plans surface says this in the Free column with ticks, and says the Basic column sells **depth and volume** — more projects, more Extended Analysis, more artifacts, more seats, more export formats, longer retention. It also says, spanning both columns, what OSLO will **never** sell you: **asking someone for their read**.

The **price is blank** — an explicit dashed *"price not set — owner-TBD (T-3)"* chip. The upgrade button is labelled **"(simulated)"**. Nothing pretends there is a billing rail here, because there isn't one (T-4).

## What a Viewer feels like (N-3)

Admitting someone off the waitlist gives them a **Viewer** seat — the least you can give them, and the cheapest: **no tier seat**. Next to their name is a **"Make Collaborator"** button. Pressing it is the moment the seat cap can bite — and if it does, the message says **TIER**, and never mentions invites.

---

# AMENDMENT — D128–D131: what the user now actually experiences

## The sentence that governs everything (D128, alongside D126)

> **Meter only what costs money or defines scope. Never meter the epistemic record. And never sell safety.**

## The thing a user should notice, and *feel*

Open **Plans** on Free and the first thing above the two columns is not a price and not a limit. It is this:

> **Two things are never metered, on any plan: your artifacts, and your History.**
> Artifacts are uncapped. History never expires and is never truncated.

That is deliberate. On a product whose whole claim is *"I will tell you the truth about your plan, including what
I don't know"*, the **record of how your understanding changed** is the product. Charging to keep it — or trimming
it on the free tier — would be selling back the one thing OSLO says is inviolable. So the Plans surface leads with
what it **won't** take away, and only then tells you what Basic adds.

The same move, twice more:

- **Safety is not an upgrade.** Link revocation and purpose-scoped expiry are identical on Free and Basic. The
  Share dialog says *"same on every plan — safety is never sold"*, where a lesser product would put a lock icon.
- **Viewers are unlimited.** Letting more people *read* your plan costs OSLO nothing and helps you. So it is free,
  on every tier, forever.

## The moment that matters: being blocked at the seat cap

You are on Free. The project has **3 collaborator seats — including you** — and all three are filled. You invite a
fourth as a Collaborator. What you get:

> **Plan limit — collaborator seats.** Free projects hold **3** collaborator seats, including you — and all 3 are
> filled. Basic holds **10**. This is a **plan** limit — it is **not** a supply limit, and it has nothing to do with
> your invites (you still have 2 this month, and they are not the problem here).
> **A Viewer holds no seat, and Viewers are unlimited on every plan** — you can add them as a **Viewer** right now,
> for free, and they will see everything OSLO understands about this plan.
> **And you can still ask them for their read** — a review request costs nothing and is never metered.
> *Or upgrade for more seats.*

Note the order: **the limit is named**, the **other** limit is explicitly cleared of blame, the **free remedy comes
first**, the **evidence path is reaffirmed**, and only then is there an upgrade link. It never says *"out of
invites"*, because that would be a lie, and a dark pattern (D124).

## The moment that reveals the honesty: a pending invite expires

You invite someone new. Your balance drops by one — but it says **held**, not spent:

> *2 of 2 left · 1 held by a pending invite (returned to you if it expires unaccepted).*

And next to their name is a **date**, not a countdown:

> *Dana Whitlock · dana@thegridvenue.com · **invite pending** · expires **25 July** · returns to your balance if unused*

That second clause is not decoration — it is the point. **A product that showed you an expiry date and stopped there
would be manufacturing scarcity.** OSLO shows you the date *and* tells you, in the same breath, that you get the
invite back. The window is **14 days** (ratified — X-2a/D132): long enough for a busy stakeholder to get to it,
short enough that supply is not parked indefinitely. There is **no countdown, no urgency colour, and no "expires
soon" nudge**, because there is nothing to hurry: if it lapses, you are made whole automatically.

They never accept. The invite expires. **You get it back**, and History says why:

> *Invite to Dana expired — returned to your allocation. She never accepted, so **no human was admitted to OSLO and
> no supply was consumed**. The invite is refunded.*

But if she **had** accepted, and you later removed her from the project — **you would not get it back**. History
says that too, and says why: *an invite admits a **human to OSLO**, not a membership to a project.* Refunding on
removal would let anyone recycle one invite forever. The asymmetry is deliberate, and it is explained rather than
hidden.

## The moment that proves the whole thing: you downgrade, and **nobody disappears**

You were on Basic. Ten people were working in your project. Money got tight, and you dropped back to Free — which
holds three.

**Nothing happens to them. Nobody is removed.**

All ten are still there. Everything they contributed is still attributed to them in History. The project simply says,
plainly, what is now true:

> **This project has 10 collaborators; Free adds up to 3.** No one has been removed, and no one will be. The only
> thing that changed: **you cannot add another Collaborator** until this project is back under 3 — or you upgrade.
> You can still add **Viewers** (unlimited, no seat), and you can still **ask anyone for their read** (free — CR-2).
> **Removing someone is always your decision, never a side-effect of a plan change.**

This is the single most important sentence in the tiering model, and it is worth being blunt about why. **Evicting
humans from a project to enforce a billing change is prohibited on a trust product.** OSLO's entire pitch is that it
tells you the truth and does not act behind your back. Silently deleting collaborators — real people, with real
attributions in an append-only record — because a card expired would be the most self-refuting thing this product
could possibly do. The non-destructive rule costs nothing, and it is now canon (D132).

The **seat cap gates who you can *add*. It is never a licence to take people out of your project.** And OSLO says so
**on the Plans page, before you downgrade** — so you never have to wonder what will happen to your people.

## Free is not a demo — now with numbers

**Free:** the whole core read · 1 project · **3 collaborator seats** · **unlimited Viewers** · **unlimited
artifacts** · **full History** · **unlimited review requests** · link revocation + expiry · a *small* monthly
Extended Analysis budget (the number is the owner's, and OSLO says so rather than inventing one) · PDF export.

**Basic:** 10 projects · 10 seats · a *generous* Extended Analysis budget · all export formats — and **exactly the
same** artifacts, History, Viewers, review requests and link security. Basic gives you more **room**, never more
**truth**.

**The price?** OSLO doesn't know. It says so, where the number would go.
