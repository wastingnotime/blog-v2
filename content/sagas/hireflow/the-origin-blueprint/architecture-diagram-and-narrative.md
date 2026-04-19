---
title: "Architecture Diagram & Narrative"
type: "episode"
saga: "HireFlow"
arc: "The Origin Blueprint"
studio: "WastingNoTime Studio"
status: "in progress"
number: 5
summary: "We consolidate the Origin Blueprint into a coherent MVP architecture. This episode presents the system map, explains the architectural intent, and defines what 'done' means for Hireflow's first milestone."
date: "2025-12-29"
tags:
  - distributed-systems
  - architecture
  - microservices
  - mvp
  - system-design
  - blueprint
---

### Architecture Diagram & Narrative

Every arc needs a moment of stillness.

Not because everything is solved -
but because enough structure exists to stop wandering and start building with intention.

This episode closes **The Origin Blueprint**.
Here we freeze the map *just enough* to move forward.

#### 1. What We Have Built So Far (Conceptually)

Across the previous episodes, Hireflow emerged organically:

* from an ambiguous briefing
* through actors and roles
* into service boundaries
* connected by events
* shaped by real-world constraints

We did not start with boxes and arrows.
The boxes appeared because responsibility demanded them.

Now we can finally step back and look at the system as a whole.

#### 2. The MVP Architecture (Narrative View)

At MVP level, Hireflow is composed of **small, authoritative services**, each owning a clear part of the domain.

##### Core Services

* **Identity**

  * authentication
  * authorization
  * role management (Company Admin, Recruiter, Candidate)

* **Company-Jobs**

  * companies
  * job postings
  * recruiter associations

* **Candidates**

  * candidate profiles
  * resumes (metadata, not files yet)
  * candidate lifecycle

* **Applications**

  * applications
  * status transitions
  * screening / evaluation (basic rules)

* **Notifications**

  * outbound communication
  * email delivery
  * template handling

* **Search**

  * denormalized views
  * job and application indexing
  * fast querying

* **Gateway**

  * single entry point
  * routing
  * token validation

* **Scheduler / Timer**

  * time-based triggers
  * cleanup
  * delayed workflows

Each service:

* owns its data
* owns its decisions
* communicates via events

No shared databases.
No hidden coupling.

#### 3. The Architecture Diagram (Mental Model)

Instead of a visually dense diagram, Hireflow favors a **mental model that fits in your head**:

```
                 ┌──────────┐
                 │ Identity │
                 └────┬─────┘
                      │
                   (auth)
                      │
                  ┌───▼───┐
                  │Gateway│
                  └───┬───┘
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
Company-Jobs     Applications       Candidates
      │               │
      │               ├─────────────┐
      │               │             │
      ▼               ▼             ▼
   Search         Notifications   Search
```

Events flow *outward*.
Authority flows *inward*.

This asymmetry is intentional.

#### 4. The MVP Definition (What “Done” Means)

For Hireflow, **MVP does not mean feature-complete**.
It means **end-to-end coherent**.

##### **MVP Capabilities**

- Company Admin can create a company
- Company Admin can post a job
- Candidate can create a profile
- Candidate can apply for a job
- Recruiter can see applications
- Notifications are sent asynchronously
- Search indexes jobs and applications
- System survives partial failures

No AI.  
No advanced ranking.  
No UI polish.

Just a working, believable hiring flow.
