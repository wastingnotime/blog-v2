from __future__ import annotations

LEGACY_EPISODE_HTML = {
    'sagas/hireflow/the-origin-blueprint/the-first-brick': """

    
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>The First Brick — HireFlow</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>
    <style>
        html { font-kerning: normal; }

         
        .menu a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        .menu a:hover {
            color:#fff;
            text-decoration:underline;
        }
        .menu a.active {
            color:#fff;
            font-weight:500;
        }
        .menu a.active::after {
            content:"•";
            margin-left:0.4em;
            opacity:0.6;
            font-weight:400;
        }

         
        a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        a:hover {
            color:#fff;
            text-decoration:underline;
        }

         
        ul {
            list-style:none;
            padding-left:0;
            margin:0;
        }

         
        .intro:empty {
            display:none;
        }

         
        .space-y-1 > * + * { margin-top: .25rem; }
        .space-y-2 > * + * { margin-top: .5rem; }
        .space-y-3 > * + * { margin-top: .75rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }

        .breadcrumb {
            font-size:0.9rem;
            color:#888;
            margin-bottom:1.5rem;
        }
        .breadcrumb a {
            color:#aaa;
            text-decoration:none;
        }
        .breadcrumb a:hover {
            text-decoration:underline;
            color:#fff;
        }
        .breadcrumb .sep {
            margin:0 .4rem;
            color:#555;
        }

        .arc-name,
        .episode-title {
            color:#fff;
            font-weight:500;
            margin:0 0 1rem 0;
            font-size:1.1rem;
        }

        .topic-link {
            border-width:1px;
            border-color: rgb(39 39 42);
            border-style: solid;
            border-radius:.25rem;
            padding:.5rem .75rem;
            color: rgb(244 244 245);
            text-decoration:none;
            transition: color .15s ease, border-color .15s ease;
        }
        .topic-link:hover {
            border-color: rgba(255,255,255,.4);
            color:#fff;
            text-decoration:underline;
        }

          
          

         .prose {
             max-width: none;
             --wnt-text-100: rgb(244 244 245);
             --wnt-text-200: rgb(228 228 231);
             --wnt-text-300: rgb(212 212 216);
             --wnt-text-400: rgb(161 161 170);
             --wnt-border:   rgb(39 39 42);
         }

         
        .prose h2 {
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #fff;
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.6;
        }
        .prose h3 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: var(--wnt-text-200);
            font-weight: 500;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .prose h3 strong { font-weight: 500; }

         
        .prose p {
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
            color: var(--wnt-text-200);
        }
        .prose h2 + p,
        .prose h3 + p { margin-top: 0.75rem; }

         
        .prose blockquote {
            border-left: 2px solid rgb(63 63 70);
            padding-left: 1rem;
            margin: 1.75rem 0;
            color: var(--wnt-text-300);
            font-style: italic;
            line-height: 1.8;
        }
        .prose blockquote p { margin: 0; }
        .prose blockquote strong { color: #fff; font-weight: 500; }

         
        .prose ul { list-style: disc; }
        .prose ol { list-style: decimal; }
        .prose ul, .prose ol {
            margin: 1.25rem 0;
            padding-left: 1.25rem;
            color: var(--wnt-text-200);
        }
        .prose li + li { margin-top: 0.35rem; }
        .prose li > p { margin: 0.25rem 0; }

         
        .prose code {
            background: rgba(255,255,255,0.04);
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            color: var(--wnt-text-100);
        }
        .prose pre {
            margin: 1.5rem 0;
            padding: 1rem;
            background: #0b0b0b;
            border: 1px solid var(--wnt-border);
            border-radius: 0.5rem;
            overflow: auto;
        }
        .prose pre code { background: transparent; padding: 0; border-radius: 0; }

         
        .prose a {
            color: var(--wnt-text-400);
            text-decoration: underline;
            text-decoration-thickness: .06em;
            text-underline-offset: 2px;
        }
        .prose a:hover { color: #fff; }

         
        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }
        .prose figure { margin: 1.75rem 0; }
        .prose figcaption {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--wnt-text-400);
            text-align: center;
        }
        .prose hr {
            border: 0;
            border-top: 1px solid var(--wnt-border);
            margin: 2rem 0;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            color: var(--wnt-text-200);
        }
        .prose thead th {
            text-align: left;
            font-weight: 600;
            color: #fff;
            border-bottom: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }
        .prose tbody td {
            border-top: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }

         
        .prose :last-child { margin-bottom: 0 !important; }
    </style>
    
</head>
<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">
<div class="max-w-3xl mx-auto px-4 py-6">
    <header class="mb-6">
        <nav class="menu text-sm text-zinc-400">
            <a class="" href="/">HOME</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/studio/">STUDIO</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="active" href="/sagas/">SAGAS</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/library/">LIBRARY</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/about/">ABOUT</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a href="/feed.xml">RSS</a>
        </nav>

        
        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep 01] The First Brick — The Origin Blueprint / HireFlow</h1>
    </header>

    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">
    </p>

    
    <nav class="breadcrumb">
        <a href="/sagas/hireflow/">← HireFlow</a>
        <span class="sep">/</span>
        <a href="/sagas/hireflow/the-origin-blueprint/">The Origin Blueprint</a>
    </nav>
    <h2 class="episode-title">The First Brick</h2>
    <div class="text-xs text-zinc-500 mb-3">
        2025-11-14 · <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/">back to arc</a>
    </div>
    
    <p class="text-sm text-zinc-400 mb-4">We explore why HireFlow exists, what it will simulate, and how microservices architecture will emerge through iterative design.</p>
    

    <article class="prose prose-invert max-w-none">
        <h3>The First Brick</h3>
<p>In the last five years I’ve been building microservices applications. It’s a wonderful architectural style for systems that need to scale, evolve, and survive failure. But—as Uncle Ben would say—<strong>“with great power comes great responsibility.”</strong> Microservices look elegant from the outside, but inside them live drivers, constraints, and trade-offs that shape every decision.</p>
<p>Building an application using this style <em>just because it’s cool</em> is a mistake. But there’s a paradox here: if you don’t build it, how do you learn how it behaves? How do you feel the pain points, understand the patterns, and discover what actually works?</p>
<p>That’s the proposition of this saga.<br>
The only real way to understand microservices is to walk through a real project—one that is meaningful enough to behave like production, but fictional enough to let us bend, adapt, and reshape it as we learn.</p>
<p>Microservices don’t come with a “manual.” There’s no ISO-certified definition. What we do have are characteristics: independence, loose coupling, bounded context, fault isolation. Some implementations honor those principles. Others cut corners—like the infamous “shared database” pattern. It’s criticized today and labeled an anti-pattern, yet it still appears everywhere because reality is messy.</p>
<p>So, to explore the real world (and its imperfections), we need a living lab. A space where we can try approaches, break things safely, and validate architectural behaviors.</p>
<p>And that’s exactly why we’re creating <strong>HireFlow</strong> together.</p>
<blockquote>
<p><strong>HireFlow is a fictional hiring platform designed as a real microservices playground. It simulates a modern recruitment workflow—from companies creating jobs to candidates applying and moving through stages—giving us a safe laboratory to test architectural decisions, patterns, failures, and refactorings.</strong></p>
</blockquote>
<p>Through HireFlow we’ll iterate on the entire lifecycle of building a microservices system. We’ll discuss decisions, highlight trade-offs, evaluate alternatives, and let the architecture <em>emerge</em> from the forces that shape it.<br>
Not top-down. Not imposed. Just evolving naturally through refactoring and learning.</p>
<p>This mirrors a key principle: <strong>emergent architecture</strong>.<br>
Instead of designing the final form upfront, we allow the system to grow in response to its drivers. We adapt. We adjust. We watch how change propagates, and the architecture reveals itself.</p>
<p>Now, let’s ground the idea with a simple briefing—our initial view of what HireFlow must do.</p>
<blockquote>
<p><strong>Briefing — Desired Functional Outcomes</strong></p>
<ul>
<li>A company can register and create open job positions.</li>
<li>Recruiters can manage job listings, view candidates, and update stages.</li>
<li>Candidates can apply by submitting personal information and a résumé.</li>
<li>The system evaluates applications with a basic screening score.</li>
<li>Recruiters can move candidates through the hiring pipeline (screening → interview → decision).</li>
<li>Interview slots can be scheduled and notifications sent.</li>
<li>Each step is traceable, auditable, and isolated to the service responsible for it.</li>
<li>The full flow works even when parts of the system are degraded—embracing microservices behavior.</li>
</ul>
</blockquote>
<p>Okay—this is our starting point.</p>
<p>In the next post, we’ll talk about the <strong>solution outline</strong> and how to slice the problem into independent domains.</p>
<p>Then we dive into the tech.</p>

    </article>

    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">
        <span></span>
        <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/interpreting-the-briefing/">Ep 02 Interpreting the Briefing →</a>
    </nav>


    <footer class="mt-10 text-xs text-zinc-500">
        © 2025 wastingnotime.org — built with Go
    </footer>
</div>
</body>
</html>


        """,
    'sagas/hireflow/the-origin-blueprint/interpreting-the-briefing': """

    
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Interpreting the Briefing — HireFlow</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>
    <style>
        html { font-kerning: normal; }

         
        .menu a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        .menu a:hover {
            color:#fff;
            text-decoration:underline;
        }
        .menu a.active {
            color:#fff;
            font-weight:500;
        }
        .menu a.active::after {
            content:"•";
            margin-left:0.4em;
            opacity:0.6;
            font-weight:400;
        }

         
        a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        a:hover {
            color:#fff;
            text-decoration:underline;
        }

         
        ul {
            list-style:none;
            padding-left:0;
            margin:0;
        }

         
        .intro:empty {
            display:none;
        }

         
        .space-y-1 > * + * { margin-top: .25rem; }
        .space-y-2 > * + * { margin-top: .5rem; }
        .space-y-3 > * + * { margin-top: .75rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }

        .breadcrumb {
            font-size:0.9rem;
            color:#888;
            margin-bottom:1.5rem;
        }
        .breadcrumb a {
            color:#aaa;
            text-decoration:none;
        }
        .breadcrumb a:hover {
            text-decoration:underline;
            color:#fff;
        }
        .breadcrumb .sep {
            margin:0 .4rem;
            color:#555;
        }

        .arc-name,
        .episode-title {
            color:#fff;
            font-weight:500;
            margin:0 0 1rem 0;
            font-size:1.1rem;
        }

        .topic-link {
            border-width:1px;
            border-color: rgb(39 39 42);
            border-style: solid;
            border-radius:.25rem;
            padding:.5rem .75rem;
            color: rgb(244 244 245);
            text-decoration:none;
            transition: color .15s ease, border-color .15s ease;
        }
        .topic-link:hover {
            border-color: rgba(255,255,255,.4);
            color:#fff;
            text-decoration:underline;
        }

          
          

         .prose {
             max-width: none;
             --wnt-text-100: rgb(244 244 245);
             --wnt-text-200: rgb(228 228 231);
             --wnt-text-300: rgb(212 212 216);
             --wnt-text-400: rgb(161 161 170);
             --wnt-border:   rgb(39 39 42);
         }

         
        .prose h2 {
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #fff;
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.6;
        }
        .prose h3 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: var(--wnt-text-200);
            font-weight: 500;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .prose h3 strong { font-weight: 500; }

         
        .prose p {
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
            color: var(--wnt-text-200);
        }
        .prose h2 + p,
        .prose h3 + p { margin-top: 0.75rem; }

         
        .prose blockquote {
            border-left: 2px solid rgb(63 63 70);
            padding-left: 1rem;
            margin: 1.75rem 0;
            color: var(--wnt-text-300);
            font-style: italic;
            line-height: 1.8;
        }
        .prose blockquote p { margin: 0; }
        .prose blockquote strong { color: #fff; font-weight: 500; }

         
        .prose ul { list-style: disc; }
        .prose ol { list-style: decimal; }
        .prose ul, .prose ol {
            margin: 1.25rem 0;
            padding-left: 1.25rem;
            color: var(--wnt-text-200);
        }
        .prose li + li { margin-top: 0.35rem; }
        .prose li > p { margin: 0.25rem 0; }

         
        .prose code {
            background: rgba(255,255,255,0.04);
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            color: var(--wnt-text-100);
        }
        .prose pre {
            margin: 1.5rem 0;
            padding: 1rem;
            background: #0b0b0b;
            border: 1px solid var(--wnt-border);
            border-radius: 0.5rem;
            overflow: auto;
        }
        .prose pre code { background: transparent; padding: 0; border-radius: 0; }

         
        .prose a {
            color: var(--wnt-text-400);
            text-decoration: underline;
            text-decoration-thickness: .06em;
            text-underline-offset: 2px;
        }
        .prose a:hover { color: #fff; }

         
        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }
        .prose figure { margin: 1.75rem 0; }
        .prose figcaption {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--wnt-text-400);
            text-align: center;
        }
        .prose hr {
            border: 0;
            border-top: 1px solid var(--wnt-border);
            margin: 2rem 0;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            color: var(--wnt-text-200);
        }
        .prose thead th {
            text-align: left;
            font-weight: 600;
            color: #fff;
            border-bottom: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }
        .prose tbody td {
            border-top: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }

         
        .prose :last-child { margin-bottom: 0 !important; }
    </style>
    
</head>
<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">
<div class="max-w-3xl mx-auto px-4 py-6">
    <header class="mb-6">
        <nav class="menu text-sm text-zinc-400">
            <a class="" href="/">HOME</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/studio/">STUDIO</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="active" href="/sagas/">SAGAS</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/library/">LIBRARY</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/about/">ABOUT</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a href="/feed.xml">RSS</a>
        </nav>

        
        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep 02] Interpreting the Briefing — The Origin Blueprint / HireFlow</h1>
    </header>

    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">
    </p>

    
    <nav class="breadcrumb">
        <a href="/sagas/hireflow/">← HireFlow</a>
        <span class="sep">/</span>
        <a href="/sagas/hireflow/the-origin-blueprint/">The Origin Blueprint</a>
    </nav>
    <h2 class="episode-title">Interpreting the Briefing</h2>
    <div class="text-xs text-zinc-500 mb-3">
        2025-11-24 · <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/">back to arc</a>
    </div>
    
    <p class="text-sm text-zinc-400 mb-4">Before writing a single line of code, we extract meaning from the briefing. We translate informal expectations into structured understanding — identifying actors, clarifying roles, and shaping the first contours of Hireflow’s architecture.</p>
    

    <article class="prose prose-invert max-w-none">
        <h3>Interpreting the Briefing</h3>
<p>There are many ways to begin building a system.<br>
Some people open the IDE immediately, as if typing fast enough could compensate for not knowing where they are going.</p>
<p>But if we do that, we lose the most important part of the journey:<br>
<strong>the map</strong>.</p>
<p>Why care about a map if it will probably change?<br>
Exactly because it will change.</p>
<p>A map is not a prophecy.<br>
It is a shared language — a temporary agreement that lets everyone understand <em>where we think we are</em> and <em>what we believe matters right now</em>.<br>
We draw enough to move. We avoid drawing more than we can carry.</p>
<p>So let’s begin.</p>
<hr>
<h4>From Briefing to Understanding</h4>
<p>In real projects, information arrives in three familiar shapes:</p>
<ol>
<li>
<p><strong>The Ancient Manuscript</strong><br>
Pages of comprehensive documentation written by people who may no longer work in the company.<br>
Heavy, complete, and often outdated the moment you open it.</p>
</li>
<li>
<p><strong>The Coffee-Break Download</strong><br>
A rushed explanation from a stakeholder who is already late for another meeting.<br>
Incomplete, fragmented, sometimes contradictory.</p>
</li>
<li>
<p><strong>Silence</strong><br>
No documents, no explanations, only expectations.</p>
</li>
</ol>
<p>So the first universal step is always the same:<br>
<strong>discovery</strong>.</p>
<p>In Hireflow, we keep things lightweight.<br>
This Saga is not about bureaucratic analysis — it’s about constructing a real system, with just enough reasoning to support the next move.</p>
<p>But even a “fair tale” needs a bit of structure.</p>
<hr>
<h4>What Do We Mean by “System”?</h4>
<p>A <em>system</em>, in the most generic sense, is a set of components that interact to achieve a purpose.<br>
It has inputs, outputs, internal rules, boundaries, and behaviors that emerge from the interaction of its parts.<br>
Your body is a system.<br>
A city is a system.<br>
A hiring platform — with people, processes, queues, and decisions — is undeniably a system.</p>
<p>This broad definition helps us because it removes the illusion of “software = code”.<br>
Software is <em>behavior</em> built intentionally.</p>
<hr>
<h4>Why Big Design Upfront Fails in Reality</h4>
<p>There was an era when architecture meant designing everything before writing anything — the famous <strong>Big Design Up Front</strong>.</p>
<p>It sounds rational:<br>
“If we think hard enough in the beginning, we won’t make mistakes.”</p>
<p>But that’s not how the world works.</p>
<p>Every plan is exposed to external forces — market shifts, new priorities, sudden meetings, interruptions, team rotations.<br>
Like an adversarial game, every player competes for the same limited resource: <strong>time</strong>.</p>
<p>So the problem with a giant upfront design is simple:<br>
<strong>the world moves while you are drawing</strong>.</p>
<p>By the time you finish, part of your masterpiece is already obsolete.</p>
<p>Agile emerged to counter this, embracing an uncomfortable truth:<br>
planning still matters, just not <em>all at once</em>.<br>
We plan just enough to take the next coherent step, and we validate direction along the way.</p>
<p>Chaotic? Sometimes.<br>
Effective? Usually.</p>
<p>This is the spirit we’ll follow.</p>
<hr>
<h4>Back to the Briefing: Extracting Structure</h4>
<p>We now take the first pass on the briefing and try to understand it in a structured way.</p>
<p>Let’s borrow some ideas from <strong>Object-Oriented Analysis</strong> — not because it’s perfect, but because it offers a clear conceptual vocabulary.<br>
And we’ll follow a relaxed version, adapted to WNT’s minimalistic and pragmatic tone.</p>
<p>Other common techniques include:</p>
<ul>
<li><em>Use-Case Modeling</em> (UML)</li>
<li><em>Domain-Driven Design discovery methods</em> (event storming, ubiquitous language)</li>
<li><em>User Stories</em> (agile)</li>
<li><em>Business Process Modeling</em></li>
<li><em>Impact Mapping</em></li>
<li><em>Functional Decomposition</em></li>
</ul>
<p>We’re not committing to any of them formally — we’re borrowing whatever helps us think with clarity.</p>
<hr>
<h4>Identifying Actors</h4>
<p>First step:<br>
<strong>Who interacts with the system?</strong><br>
These are our <em>actors</em> — human or non-human entities that trigger behavior.</p>
<p>Extracted directly from the briefing:</p>
<ul>
<li>company</li>
<li>recruiters</li>
<li>candidates</li>
<li>the system</li>
<li>scheduler</li>
</ul>
<p>Now refine:</p>
<h5>Company</h5>
<p>A company itself doesn’t “act”.<br>
A person in a role does.<br>
So we materialize it as <strong>Company Admin</strong> — a simple, descriptive (and intentionally uncreative) name.</p>
<h5>The System</h5>
<p>“The system evaluates applications.”<br>
This is not an actor — it’s a <strong>business rule</strong> inside the system.</p>
<h5>Scheduler</h5>
<p>This one <em>is</em> an actor.<br>
Time-based triggers behave like external events.<br>
If an external system wakes us, that system becomes the actor.<br>
If time itself wakes us, the actor is the <strong>Timer</strong>.</p>
<h5>Recruiters &amp; Candidates</h5>
<p>Clear and straightforward.</p>
<p>So our final list becomes:</p>
<ul>
<li>
<p><strong>Company Admin</strong></p>
</li>
<li>
<p><strong>Recruiter</strong></p>
</li>
<li>
<p><strong>Candidate</strong></p>
</li>
<li>
<p><strong>Timer</strong></p>
</li>
</ul>
<p>These are the four identities our system must support from day one.</p>
<p>And this implies one foundational service:<br>
<strong>Identity Service</strong> — the place where roles live and authentication/authorization is anchored.</p>
<p>So far, the map expands naturally.</p>
<hr>
<h4>Next Step: Identifying Services</h4>
<p>With actors in hand, the next movement is to identify <strong>what services exist</strong> and <strong>what each service owns</strong> — but that is the next part of the episode.</p>

    </article>

    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">
        <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/the-first-brick/">← Ep 01 The First Brick</a>
        <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/identifying-our-first-services/">Ep 03 Identifying Our First Services →</a>
    </nav>


    <footer class="mt-10 text-xs text-zinc-500">
        © 2025 wastingnotime.org — built with Go
    </footer>
</div>
</body>
</html>


        """,
    'sagas/hireflow/the-origin-blueprint/identifying-our-first-services': """

    
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Identifying Our First Services — HireFlow</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>
    <style>
        html { font-kerning: normal; }

         
        .menu a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        .menu a:hover {
            color:#fff;
            text-decoration:underline;
        }
        .menu a.active {
            color:#fff;
            font-weight:500;
        }
        .menu a.active::after {
            content:"•";
            margin-left:0.4em;
            opacity:0.6;
            font-weight:400;
        }

         
        a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        a:hover {
            color:#fff;
            text-decoration:underline;
        }

         
        ul {
            list-style:none;
            padding-left:0;
            margin:0;
        }

         
        .intro:empty {
            display:none;
        }

         
        .space-y-1 > * + * { margin-top: .25rem; }
        .space-y-2 > * + * { margin-top: .5rem; }
        .space-y-3 > * + * { margin-top: .75rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }

        .breadcrumb {
            font-size:0.9rem;
            color:#888;
            margin-bottom:1.5rem;
        }
        .breadcrumb a {
            color:#aaa;
            text-decoration:none;
        }
        .breadcrumb a:hover {
            text-decoration:underline;
            color:#fff;
        }
        .breadcrumb .sep {
            margin:0 .4rem;
            color:#555;
        }

        .arc-name,
        .episode-title {
            color:#fff;
            font-weight:500;
            margin:0 0 1rem 0;
            font-size:1.1rem;
        }

        .topic-link {
            border-width:1px;
            border-color: rgb(39 39 42);
            border-style: solid;
            border-radius:.25rem;
            padding:.5rem .75rem;
            color: rgb(244 244 245);
            text-decoration:none;
            transition: color .15s ease, border-color .15s ease;
        }
        .topic-link:hover {
            border-color: rgba(255,255,255,.4);
            color:#fff;
            text-decoration:underline;
        }

          
          

         .prose {
             max-width: none;
             --wnt-text-100: rgb(244 244 245);
             --wnt-text-200: rgb(228 228 231);
             --wnt-text-300: rgb(212 212 216);
             --wnt-text-400: rgb(161 161 170);
             --wnt-border:   rgb(39 39 42);
         }

         
        .prose h2 {
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #fff;
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.6;
        }
        .prose h3 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: var(--wnt-text-200);
            font-weight: 500;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .prose h3 strong { font-weight: 500; }

         
        .prose p {
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
            color: var(--wnt-text-200);
        }
        .prose h2 + p,
        .prose h3 + p { margin-top: 0.75rem; }

         
        .prose blockquote {
            border-left: 2px solid rgb(63 63 70);
            padding-left: 1rem;
            margin: 1.75rem 0;
            color: var(--wnt-text-300);
            font-style: italic;
            line-height: 1.8;
        }
        .prose blockquote p { margin: 0; }
        .prose blockquote strong { color: #fff; font-weight: 500; }

         
        .prose ul { list-style: disc; }
        .prose ol { list-style: decimal; }
        .prose ul, .prose ol {
            margin: 1.25rem 0;
            padding-left: 1.25rem;
            color: var(--wnt-text-200);
        }
        .prose li + li { margin-top: 0.35rem; }
        .prose li > p { margin: 0.25rem 0; }

         
        .prose code {
            background: rgba(255,255,255,0.04);
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            color: var(--wnt-text-100);
        }
        .prose pre {
            margin: 1.5rem 0;
            padding: 1rem;
            background: #0b0b0b;
            border: 1px solid var(--wnt-border);
            border-radius: 0.5rem;
            overflow: auto;
        }
        .prose pre code { background: transparent; padding: 0; border-radius: 0; }

         
        .prose a {
            color: var(--wnt-text-400);
            text-decoration: underline;
            text-decoration-thickness: .06em;
            text-underline-offset: 2px;
        }
        .prose a:hover { color: #fff; }

         
        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }
        .prose figure { margin: 1.75rem 0; }
        .prose figcaption {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--wnt-text-400);
            text-align: center;
        }
        .prose hr {
            border: 0;
            border-top: 1px solid var(--wnt-border);
            margin: 2rem 0;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            color: var(--wnt-text-200);
        }
        .prose thead th {
            text-align: left;
            font-weight: 600;
            color: #fff;
            border-bottom: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }
        .prose tbody td {
            border-top: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }

         
        .prose :last-child { margin-bottom: 0 !important; }
    </style>
    
</head>
<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">
<div class="max-w-3xl mx-auto px-4 py-6">
    <header class="mb-6">
        <nav class="menu text-sm text-zinc-400">
            <a class="" href="/">HOME</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/studio/">STUDIO</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="active" href="/sagas/">SAGAS</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/library/">LIBRARY</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/about/">ABOUT</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a href="/feed.xml">RSS</a>
        </nav>

        
        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep 03] Identifying Our First Services — The Origin Blueprint / HireFlow</h1>
    </header>

    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">
    </p>

    
    <nav class="breadcrumb">
        <a href="/sagas/hireflow/">← HireFlow</a>
        <span class="sep">/</span>
        <a href="/sagas/hireflow/the-origin-blueprint/">The Origin Blueprint</a>
    </nav>
    <h2 class="episode-title">Identifying Our First Services</h2>
    <div class="text-xs text-zinc-500 mb-3">
        2025-12-05 · <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/">back to arc</a>
    </div>
    
    <p class="text-sm text-zinc-400 mb-4">From actors to boundaries — we translate the briefing into concrete service domains. Each service emerges from responsibility, authority, and clarity, forming the first stable shape of Hireflow’s architecture.</p>
    

    <article class="prose prose-invert max-w-none">
        <h3>Identifying Our First Services</h3>
<p>Now that the actors are mapped, the natural next step is to ask a deceptively simple question:</p>
<p><strong>“What exists in this world?”</strong></p>
<p>Actors show <em>who</em> interacts with the system.<br>
Services define <em>where</em> responsibility lives.</p>
<p>A service is not “a controller” or “a folder” — it is a <strong>boundary of authority</strong>.<br>
It owns a part of the domain, the data, and the decisions within it.</p>
<p>So we return to the briefing and extract nouns and verbs that hint at areas of responsibility.<br>
Not implementation details — <em>domains of meaning</em>.</p>
<p>From the original briefing, the ecosystem seems to revolve around:</p>
<ul>
<li>
<p>companies</p>
</li>
<li>
<p>job postings</p>
</li>
<li>
<p>recruiters</p>
</li>
<li>
<p>candidates</p>
</li>
<li>
<p>applications</p>
</li>
<li>
<p>evaluations</p>
</li>
<li>
<p>notifications</p>
</li>
<li>
<p>search</p>
</li>
<li>
<p>automated workflows</p>
</li>
</ul>
<p>If we squint, these concepts start clustering naturally — as if the system is revealing its own topology.</p>
<p>Let’s process them one by one with WNT’s “calm, deliberate” approach.</p>
<hr>
<h4>1. Identity &amp; Roles</h4>
<p>We identified earlier that we have four roles:</p>
<ul>
<li>
<p>Company Admin</p>
</li>
<li>
<p>Recruiter</p>
</li>
<li>
<p>Candidate</p>
</li>
<li>
<p>Timer (system-triggered behavior)</p>
</li>
</ul>
<p>This already defines our first service:</p>
<h5>Identity Service</h5>
<p><strong>Responsibility:</strong></p>
<ul>
<li>
<p>authentication</p>
</li>
<li>
<p>authorization</p>
</li>
<li>
<p>role management</p>
</li>
<li>
<p>issuing tokens</p>
</li>
<li>
<p>basic user lifecycle</p>
</li>
</ul>
<p><strong>Authority:</strong><br>
Owns everything related to identity.</p>
<p><strong>Reasoning:</strong><br>
Identity is foundational.<br>
Every other service depends on knowing <em>who</em> is acting and <em>what they can do</em>.</p>
<p>So the Identity Service is not optional — it is the gatekeeper.</p>
<hr>
<h4>2. Company &amp; Job Management</h4>
<p>Companies create job postings.<br>
Recruiters manage them.<br>
Candidates apply to them.</p>
<p>This gives us a second clear boundary:</p>
<h5>Company-Jobs Service</h5>
<p><strong>Responsibility:</strong></p>
<ul>
<li>
<p>company profiles</p>
</li>
<li>
<p>job postings</p>
</li>
<li>
<p>recruiter associations</p>
</li>
<li>
<p>job visibility rules</p>
</li>
</ul>
<p><strong>Authority:</strong><br>
Owns jobs and their lifecycle.</p>
<p><strong>Why separate it?</strong><br>
Because job management is a domain in itself.<br>
It evolves independently from candidates or evaluations.</p>
<hr>
<h4>3. Candidates Service</h4>
<p>Candidates are not just entities — they have profiles, histories, resumes, preferences.</p>
<h5>Candidates Service</h5>
<p><strong>Responsibility:</strong></p>
<ul>
<li>
<p>candidate profiles</p>
</li>
<li>
<p>resume metadata</p>
</li>
<li>
<p>activity history</p>
</li>
<li>
<p>candidate-side settings</p>
</li>
</ul>
<p><strong>Authority:</strong><br>
Owns candidate data and its evolution.</p>
<p>This avoids mixing candidate information with job or application information, which is a trap monoliths often fall into.</p>
<hr>
<h4>4. Applications Service</h4>
<p>The heart of the hiring flow:<br>
A candidate applies, a recruiter evaluates, a decision is made.</p>
<h5>Applications Service</h5>
<p><strong>Responsibility:</strong></p>
<ul>
<li>
<p>applications</p>
</li>
<li>
<p>status transitions</p>
</li>
<li>
<p>evaluation records</p>
</li>
<li>
<p>scoring or screening logic (initial, not ML)</p>
</li>
</ul>
<p><strong>Authority:</strong><br>
Owns the lifecycle of an application.</p>
<p>This is where business rules grow dense.<br>
Separating applications keeps the rest of the system clean.</p>
<hr>
<h4>5. Notifications Service</h4>
<p>Whenever certain events happen — application submitted, recruiter invited — someone needs to be notified.</p>
<h5>Notifications Service</h5>
<p><strong>Responsibility:</strong></p>
<ul>
<li>
<p>sending emails</p>
</li>
<li>
<p>preparing message templates</p>
</li>
<li>
<p>acting on events</p>
</li>
</ul>
<p><strong>Authority:</strong><br>
Owns outbound communications.</p>
<p>This service listens to events (RabbitMQ in our architecture) and emits notifications.</p>
<hr>
<h4>6. Search Service</h4>
<p>Across companies, jobs, and candidates, search becomes an important operational capability.</p>
<h5>Search Service</h5>
<p><strong>Responsibility:</strong></p>
<ul>
<li>
<p>indexing data from other services</p>
</li>
<li>
<p>exposing search endpoints</p>
</li>
<li>
<p>providing “quick access” queries</p>
</li>
</ul>
<p><strong>Authority:</strong><br>
Owns search indexes and denormalized views.</p>
<p>This service <em>does not store source of truth data</em> — it mirrors other domains through events.</p>
<hr>
<h4>7. Gateway</h4>
<p>Even though it is not a domain service, the system needs a stable entry point.</p>
<h5>Gateway</h5>
<p><strong>Responsibility:</strong></p>
<ul>
<li>
<p>API routing</p>
</li>
<li>
<p>request composition</p>
</li>
<li>
<p>rate limiting (future)</p>
</li>
<li>
<p>authentication pass-through</p>
</li>
</ul>
<p><strong>Authority:</strong><br>
Owns how the outside world enters the platform.</p>
<p>It is the front door.</p>
<hr>
<h4>8. Timer / Automated Workflows</h4>
<p>Timers trigger cleanup routines, periodic evaluations, or automated transitions.<br>
These are orchestrated not inside the services but through scheduled messages.</p>
<h5>Workflow Scheduler</h5>
<p>Not exactly a “service”, but a mechanism:</p>
<p><strong>Responsibility:</strong></p>
<ul>
<li>
<p>producing time-triggered messages</p>
</li>
<li>
<p>orchestrating routine tasks</p>
</li>
</ul>
<p><strong>Authority:</strong><br>
Owns temporal events.</p>
<p>This could be implemented with Kubernetes CronJobs, or a lightweight internal scheduler.</p>
<hr>
<h3>Current Map (Early Draft)</h3>
<p>By now, the system begins to reveal its natural structure:</p>
<ul>
<li>
<p><strong>identity</strong></p>
</li>
<li>
<p><strong>company-jobs</strong></p>
</li>
<li>
<p><strong>candidates</strong></p>
</li>
<li>
<p><strong>applications</strong></p>
</li>
<li>
<p><strong>notifications</strong></p>
</li>
<li>
<p><strong>search</strong></p>
</li>
<li>
<p><strong>gateway</strong></p>
</li>
<li>
<p><strong>scheduler (cron/timer)</strong></p>
</li>
</ul>
<p>This list will evolve.<br>
It always does.<br>
But it already gives us enough clarity to design paths, boundaries, and interactions.</p>
<p>And more importantly:<br>
it gives us confidence that each service has a purpose and a clean responsibility.</p>

    </article>

    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">
        <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/interpreting-the-briefing/">← Ep 02 Interpreting the Briefing</a>
        <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/interactions-flows-and-early-event-design/">Ep 04 Interactions, Flows &amp; Early Event Design →</a>
    </nav>


    <footer class="mt-10 text-xs text-zinc-500">
        © 2025 wastingnotime.org — built with Go
    </footer>
</div>
</body>
</html>


        """,
    'sagas/hireflow/the-origin-blueprint/interactions-flows-and-early-event-design': """

    
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Interactions, Flows &amp; Early Event Design — HireFlow</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>
    <style>
        html { font-kerning: normal; }

         
        .menu a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        .menu a:hover {
            color:#fff;
            text-decoration:underline;
        }
        .menu a.active {
            color:#fff;
            font-weight:500;
        }
        .menu a.active::after {
            content:"•";
            margin-left:0.4em;
            opacity:0.6;
            font-weight:400;
        }

         
        a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        a:hover {
            color:#fff;
            text-decoration:underline;
        }

         
        ul {
            list-style:none;
            padding-left:0;
            margin:0;
        }

         
        .intro:empty {
            display:none;
        }

         
        .space-y-1 > * + * { margin-top: .25rem; }
        .space-y-2 > * + * { margin-top: .5rem; }
        .space-y-3 > * + * { margin-top: .75rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }

        .breadcrumb {
            font-size:0.9rem;
            color:#888;
            margin-bottom:1.5rem;
        }
        .breadcrumb a {
            color:#aaa;
            text-decoration:none;
        }
        .breadcrumb a:hover {
            text-decoration:underline;
            color:#fff;
        }
        .breadcrumb .sep {
            margin:0 .4rem;
            color:#555;
        }

        .arc-name,
        .episode-title {
            color:#fff;
            font-weight:500;
            margin:0 0 1rem 0;
            font-size:1.1rem;
        }

        .topic-link {
            border-width:1px;
            border-color: rgb(39 39 42);
            border-style: solid;
            border-radius:.25rem;
            padding:.5rem .75rem;
            color: rgb(244 244 245);
            text-decoration:none;
            transition: color .15s ease, border-color .15s ease;
        }
        .topic-link:hover {
            border-color: rgba(255,255,255,.4);
            color:#fff;
            text-decoration:underline;
        }

          
          

         .prose {
             max-width: none;
             --wnt-text-100: rgb(244 244 245);
             --wnt-text-200: rgb(228 228 231);
             --wnt-text-300: rgb(212 212 216);
             --wnt-text-400: rgb(161 161 170);
             --wnt-border:   rgb(39 39 42);
         }

         
        .prose h2 {
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #fff;
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.6;
        }
        .prose h3 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: var(--wnt-text-200);
            font-weight: 500;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .prose h3 strong { font-weight: 500; }

         
        .prose p {
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
            color: var(--wnt-text-200);
        }
        .prose h2 + p,
        .prose h3 + p { margin-top: 0.75rem; }

         
        .prose blockquote {
            border-left: 2px solid rgb(63 63 70);
            padding-left: 1rem;
            margin: 1.75rem 0;
            color: var(--wnt-text-300);
            font-style: italic;
            line-height: 1.8;
        }
        .prose blockquote p { margin: 0; }
        .prose blockquote strong { color: #fff; font-weight: 500; }

         
        .prose ul { list-style: disc; }
        .prose ol { list-style: decimal; }
        .prose ul, .prose ol {
            margin: 1.25rem 0;
            padding-left: 1.25rem;
            color: var(--wnt-text-200);
        }
        .prose li + li { margin-top: 0.35rem; }
        .prose li > p { margin: 0.25rem 0; }

         
        .prose code {
            background: rgba(255,255,255,0.04);
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            color: var(--wnt-text-100);
        }
        .prose pre {
            margin: 1.5rem 0;
            padding: 1rem;
            background: #0b0b0b;
            border: 1px solid var(--wnt-border);
            border-radius: 0.5rem;
            overflow: auto;
        }
        .prose pre code { background: transparent; padding: 0; border-radius: 0; }

         
        .prose a {
            color: var(--wnt-text-400);
            text-decoration: underline;
            text-decoration-thickness: .06em;
            text-underline-offset: 2px;
        }
        .prose a:hover { color: #fff; }

         
        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }
        .prose figure { margin: 1.75rem 0; }
        .prose figcaption {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--wnt-text-400);
            text-align: center;
        }
        .prose hr {
            border: 0;
            border-top: 1px solid var(--wnt-border);
            margin: 2rem 0;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            color: var(--wnt-text-200);
        }
        .prose thead th {
            text-align: left;
            font-weight: 600;
            color: #fff;
            border-bottom: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }
        .prose tbody td {
            border-top: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }

         
        .prose :last-child { margin-bottom: 0 !important; }
    </style>
    
</head>
<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">
<div class="max-w-3xl mx-auto px-4 py-6">
    <header class="mb-6">
        <nav class="menu text-sm text-zinc-400">
            <a class="" href="/">HOME</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/studio/">STUDIO</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="active" href="/sagas/">SAGAS</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/library/">LIBRARY</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/about/">ABOUT</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a href="/feed.xml">RSS</a>
        </nav>

        
        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep 04] Interactions, Flows &amp; Early Event Design — The Origin Blueprint / HireFlow</h1>
    </header>

    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">
    </p>

    
    <nav class="breadcrumb">
        <a href="/sagas/hireflow/">← HireFlow</a>
        <span class="sep">/</span>
        <a href="/sagas/hireflow/the-origin-blueprint/">The Origin Blueprint</a>
    </nav>
    <h2 class="episode-title">Interactions, Flows &amp; Early Event Design</h2>
    <div class="text-xs text-zinc-500 mb-3">
        2025-12-28 · <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/">back to arc</a>
    </div>
    
    <p class="text-sm text-zinc-400 mb-4">With the service boundaries defined, we explore how they communicate. Direct calls, asynchronous events, and the early hiring flow reveal the first shape of Hireflow’s behavior — resilient, decoupled, and event-driven.</p>
    

    <article class="prose prose-invert max-w-none">
        <h3>Interactions, Flows &amp; Early Event Design</h3>
<p>Now that the system’s boundaries exist on the map, another question appears — and it is one of the most important in any distributed architecture:</p>
<p><strong>How do these services talk to each other without becoming dependent on each other?</strong></p>
<p>This question is the hinge between <em>software that scales</em> and <em>software that collapses under its own weight</em>.</p>
<p>Because services are not just folders separated by network calls.<br>
They are <strong>small worlds with independent authority</strong>, and the space between them — the communication — is where reliability is either preserved or lost.</p>
<p>So in this episode, we take the first step into that space.</p>
<hr>
<h4>1. Two Ways to Interact: Direct Calls vs. Events</h4>
<p>In any distributed system, there are only two fundamental coordination patterns:</p>
<ol>
<li>
<p><strong>Direct synchronous calls</strong></p>
<ul>
<li>
<p>predictable</p>
</li>
<li>
<p>transactional feel</p>
</li>
<li>
<p>tightly coupled</p>
</li>
<li>
<p>sensitive to latency and availability</p>
</li>
</ul>
</li>
<li>
<p><strong>Asynchronous events</strong></p>
<ul>
<li>
<p>decoupled</p>
</li>
<li>
<p>more resilient</p>
</li>
<li>
<p>eventual consistency</p>
</li>
<li>
<p>harder to reason about at first</p>
</li>
</ul>
</li>
</ol>
<p>Neither is “right” or “wrong”.</p>
<p>But each tells a different story about your system.</p>
<p>At Hireflow, events are the main structure.<br>
Not because it is fashionable, but because the hiring flow is naturally <strong>event-driven</strong>:</p>
<ul>
<li>
<p>a job is created</p>
</li>
<li>
<p>a candidate applies</p>
</li>
<li>
<p>an application enters a new stage</p>
</li>
<li>
<p>a notification is sent</p>
</li>
<li>
<p>search indexes update</p>
</li>
<li>
<p>recruiters perform actions</p>
</li>
<li>
<p>the system reacts</p>
</li>
</ul>
<p>If we tried to model this with purely synchronous calls, we would recreate a monolith over HTTP — brittle, slow, and over-structured.</p>
<p>Events give the system space to breathe.</p>
<hr>
<h4>2. Designing the First Critical Flow: The Happy Path</h4>
<p>Milestone 1 is the “Happy Path.”<br>
The simplest complete scenario a user experiences:</p>
<ol>
<li>
<p>A company posts a job.</p>
</li>
<li>
<p>A candidate discovers the job.</p>
</li>
<li>
<p>The candidate applies.</p>
</li>
<li>
<p>Recruiters see the application.</p>
</li>
<li>
<p>Notifications go out.</p>
</li>
<li>
<p>Search updates.</p>
</li>
<li>
<p>The system remains consistent.</p>
</li>
</ol>
<p>Let’s break it down service by service.</p>
<hr>
<h4>Step 1 — Company Admin Creates a Job</h4>
<p><strong>Actor:</strong> Company Admin<br>
<strong>Entry:</strong> Gateway → Company-Jobs Service</p>
<p>When a job is created, Company-Jobs becomes the <strong>source of truth</strong>.
But other services also care about this event:</p>
<ul>
<li>
<p>Search (to index the job)</p>
</li>
<li>
<p>Applications (to allow future applications)</p>
</li>
<li>
<p>Notifications (in some scenarios)</p>
</li>
</ul>
<p>So Company-Jobs publishes:</p>
<pre><code>job.created
</code></pre>
<p><strong>Payload (early sketch):</strong></p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>{
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;jobId&#34;</span>: <span style="color:#f1fa8c">&#34;guid&#34;</span>,
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;companyId&#34;</span>: <span style="color:#f1fa8c">&#34;guid&#34;</span>,
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;title&#34;</span>: <span style="color:#f1fa8c">&#34;...&#34;</span>,
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;createdAt&#34;</span>: <span style="color:#f1fa8c">&#34;timestamp&#34;</span>
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>(Details will evolve; for now we sketch only shape, not depth.)</p>
<hr>
<h4>Step 2 — Candidate Applies</h4>
<p><strong>Actor:</strong> Candidate<br>
<strong>Entry:</strong> Gateway → Applications Service</p>
<p>Applications is authoritative here.<br>
But this creates a cascading responsibility:</p>
<ul>
<li>
<p>Notifications should inform recruiters</p>
</li>
<li>
<p>Search must update the “application count” or visibility</p>
</li>
<li>
<p>Recruiters rely on fresh application data</p>
</li>
</ul>
<p>So Applications publishes:</p>
<pre><code>application.submitted
</code></pre>
<p><strong>Payload (early sketch):</strong></p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>{
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;applicationId&#34;</span>: <span style="color:#f1fa8c">&#34;guid&#34;</span>,
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;candidateId&#34;</span>: <span style="color:#f1fa8c">&#34;guid&#34;</span>,
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;jobId&#34;</span>: <span style="color:#f1fa8c">&#34;guid&#34;</span>,
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;submittedAt&#34;</span>: <span style="color:#f1fa8c">&#34;timestamp&#34;</span>
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>This event becomes the heart of the hiring workflow.</p>
<hr>
<h4>Step 3 — Recruiter Visibility</h4>
<p>Recruiters consume the application list from Applications Service via the Gateway.</p>
<p>But they do <strong>not</strong> make direct calls to Candidates Service for candidate profiles.<br>
That would create dependency loops.</p>
<p>Instead, Applications only stores candidate identifiers.<br>
If Applications needs candidate display data later, it listens to:</p>
<pre><code>candidate.updated
</code></pre>
<p>or</p>
<pre><code>candidate.created
</code></pre>
<p>and caches what it needs internally.</p>
<p>This ensures that the flow remains stable even if one service is down.</p>
<hr>
<h4>Step 4 — Notifications Triggered</h4>
<p>Notifications Service subscribes to many early events, but one is foundational:</p>
<pre><code>application.submitted
</code></pre>
<p>When it receives this event, it:</p>
<ul>
<li>
<p>formats notification templates</p>
</li>
<li>
<p>routes messages to recruiters</p>
</li>
<li>
<p>delivers messages asynchronously</p>
</li>
</ul>
<p>This also allows throttling, retry strategies, and idempotency — all crucial for reliability.</p>
<hr>
<h4>Step 5 — Search Updates</h4>
<p>Search does not call anyone.<br>
Search listens.</p>
<p>From day one this rule keeps Search simple, reactive, and safe to rebuild.</p>
<p>Events Search listens to:</p>
<ul>
<li><code>job.created</code></li>
<li><code>job.updated</code></li>
<li><code>application.submitted</code></li>
<li>(later) <code>candidate.updated</code></li>
</ul>
<p>Search builds its own denormalized views optimized for querying.</p>
<p>This gives us the first mental diagram:</p>
<pre><code>           job.created
       ┌──────────┴───────────┐
Company-Jobs             Search Service
       │
       └──────&gt; application.submitted
                      │
                      ├──&gt; Notifications
                      └──&gt; Search Service (again)
</code></pre>
<p>This is not the final design, but it captures the spirit:
<strong>events radiating outward, each service reacting according to its responsibility.</strong></p>
<hr>
<h4>3. Event Naming Conventions (Early Version)</h4>
<p>Simple. Verb past tense. Domain-prefixed.</p>
<p>Examples:</p>
<ul>
<li>
<p><code>job.created</code></p>
</li>
<li>
<p><code>job.updated</code></p>
</li>
<li>
<p><code>application.submitted</code></p>
</li>
<li>
<p><code>application.status_changed</code></p>
</li>
<li>
<p><code>candidate.created</code></p>
</li>
<li>
<p><code>candidate.updated</code></p>
</li>
</ul>
<p>Clear, predictable, semantically stable.</p>
<p>We avoid things like <code>jobCreateEventV2</code><br>
because events should evolve by payload, not name.</p>
<hr>
<h4>4. Event Contracts: The Early Philosophy</h4>
<p>At this early stage, our contracts follow three rules:</p>
<h5>Rule 1 — Minimal but Sufficient</h5>
<p>Include only what other services truly need.<br>
If something can be fetched by ID later, send IDs.</p>
<h5>Rule 2 — Never Break Consumers</h5>
<p>If an event must evolve, extend the payload — do not change meaning.</p>
<h5>Rule 3 — Events Describe Facts, Not Commands</h5>
<p>Events are past tense.<br>
They announce what happened, not what should happen.</p>
<p>This keeps publishers honest and consumers stable.</p>
<hr>
<h4>5. Fault Tolerance at the Edges</h4>
<p>One of the early questions we must answer:</p>
<p><strong>“What happens when a service is down?”</strong></p>
<p>Event-driven architecture answers this elegantly:</p>
<ul>
<li>
<p>Services publish events independently.</p>
</li>
<li>
<p>Consumers pick them up when they come back online.</p>
</li>
<li>
<p>The system self-heals through message persistence.</p>
</li>
</ul>
<p>This is why Hireflow chooses RabbitMQ early — not for scale, but for <strong>predictable behavior during partial failures</strong>.</p>
<p>It’s not perfect, but it’s reliable.</p>
<hr>
<h4>6. The First Architecture Flow</h4>
<p>Here’s the distilled early picture — the skeleton that Milestone 1 will bring to life:</p>
<pre><code>Gateway
   │
   ▼
Identity  ←→  Company-Jobs  → emits job.created
                        │
                        └─────→ Search (index job)

Gateway
   │
   ▼
Applications → emits application.submitted
       │
       ├────→ Notifications
       └────→ Search (update indexes)
</code></pre>
<p>A small system, already alive.</p>
<p>Small enough to reason about.
Large enough to reveal its nature.</p>
<hr>
<h4>Closing Reflection</h4>
<p>Interaction design is not about drawing arrows.<br>
It is about understanding <em>who depends on what</em><br>
and <em>how to protect each service from accidental entanglement</em>.</p>
<p>In Hireflow, events become a quiet contract between domains.</p>
<p>They give us:</p>
<ul>
<li>
<p>resilience</p>
</li>
<li>
<p>evolution</p>
</li>
<li>
<p>isolation</p>
</li>
<li>
<p>clarity</p>
</li>
</ul>
<p>…which are the ingredients that allow a small system to become a reliable one.</p>
<p>Episode 5 will take us deeper into the specifics:</p>
<ul>
<li>
<p>modeling the first real events</p>
</li>
<li>
<p>shaping the topic structure</p>
</li>
<li>
<p>choosing idempotency strategies</p>
</li>
<li>
<p>designing the “Happy Path” sequence concretely</p>
</li>
</ul>

    </article>

    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">
        <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/identifying-our-first-services/">← Ep 03 Identifying Our First Services</a>
        <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/architecture-diagram-and-narrative/">Ep 05 Architecture Diagram &amp; Narrative →</a>
    </nav>


    <footer class="mt-10 text-xs text-zinc-500">
        © 2025 wastingnotime.org — built with Go
    </footer>
</div>
</body>
</html>


        """,
    'sagas/hireflow/the-origin-blueprint/architecture-diagram-and-narrative': """

    
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Architecture Diagram &amp; Narrative — HireFlow</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>
    <style>
        html { font-kerning: normal; }

         
        .menu a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        .menu a:hover {
            color:#fff;
            text-decoration:underline;
        }
        .menu a.active {
            color:#fff;
            font-weight:500;
        }
        .menu a.active::after {
            content:"•";
            margin-left:0.4em;
            opacity:0.6;
            font-weight:400;
        }

         
        a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        a:hover {
            color:#fff;
            text-decoration:underline;
        }

         
        ul {
            list-style:none;
            padding-left:0;
            margin:0;
        }

         
        .intro:empty {
            display:none;
        }

         
        .space-y-1 > * + * { margin-top: .25rem; }
        .space-y-2 > * + * { margin-top: .5rem; }
        .space-y-3 > * + * { margin-top: .75rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }

        .breadcrumb {
            font-size:0.9rem;
            color:#888;
            margin-bottom:1.5rem;
        }
        .breadcrumb a {
            color:#aaa;
            text-decoration:none;
        }
        .breadcrumb a:hover {
            text-decoration:underline;
            color:#fff;
        }
        .breadcrumb .sep {
            margin:0 .4rem;
            color:#555;
        }

        .arc-name,
        .episode-title {
            color:#fff;
            font-weight:500;
            margin:0 0 1rem 0;
            font-size:1.1rem;
        }

        .topic-link {
            border-width:1px;
            border-color: rgb(39 39 42);
            border-style: solid;
            border-radius:.25rem;
            padding:.5rem .75rem;
            color: rgb(244 244 245);
            text-decoration:none;
            transition: color .15s ease, border-color .15s ease;
        }
        .topic-link:hover {
            border-color: rgba(255,255,255,.4);
            color:#fff;
            text-decoration:underline;
        }

          
          

         .prose {
             max-width: none;
             --wnt-text-100: rgb(244 244 245);
             --wnt-text-200: rgb(228 228 231);
             --wnt-text-300: rgb(212 212 216);
             --wnt-text-400: rgb(161 161 170);
             --wnt-border:   rgb(39 39 42);
         }

         
        .prose h2 {
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #fff;
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.6;
        }
        .prose h3 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: var(--wnt-text-200);
            font-weight: 500;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .prose h3 strong { font-weight: 500; }

         
        .prose p {
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
            color: var(--wnt-text-200);
        }
        .prose h2 + p,
        .prose h3 + p { margin-top: 0.75rem; }

         
        .prose blockquote {
            border-left: 2px solid rgb(63 63 70);
            padding-left: 1rem;
            margin: 1.75rem 0;
            color: var(--wnt-text-300);
            font-style: italic;
            line-height: 1.8;
        }
        .prose blockquote p { margin: 0; }
        .prose blockquote strong { color: #fff; font-weight: 500; }

         
        .prose ul { list-style: disc; }
        .prose ol { list-style: decimal; }
        .prose ul, .prose ol {
            margin: 1.25rem 0;
            padding-left: 1.25rem;
            color: var(--wnt-text-200);
        }
        .prose li + li { margin-top: 0.35rem; }
        .prose li > p { margin: 0.25rem 0; }

         
        .prose code {
            background: rgba(255,255,255,0.04);
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            color: var(--wnt-text-100);
        }
        .prose pre {
            margin: 1.5rem 0;
            padding: 1rem;
            background: #0b0b0b;
            border: 1px solid var(--wnt-border);
            border-radius: 0.5rem;
            overflow: auto;
        }
        .prose pre code { background: transparent; padding: 0; border-radius: 0; }

         
        .prose a {
            color: var(--wnt-text-400);
            text-decoration: underline;
            text-decoration-thickness: .06em;
            text-underline-offset: 2px;
        }
        .prose a:hover { color: #fff; }

         
        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }
        .prose figure { margin: 1.75rem 0; }
        .prose figcaption {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--wnt-text-400);
            text-align: center;
        }
        .prose hr {
            border: 0;
            border-top: 1px solid var(--wnt-border);
            margin: 2rem 0;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            color: var(--wnt-text-200);
        }
        .prose thead th {
            text-align: left;
            font-weight: 600;
            color: #fff;
            border-bottom: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }
        .prose tbody td {
            border-top: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }

         
        .prose :last-child { margin-bottom: 0 !important; }
    </style>
    
</head>
<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">
<div class="max-w-3xl mx-auto px-4 py-6">
    <header class="mb-6">
        <nav class="menu text-sm text-zinc-400">
            <a class="" href="/">HOME</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/studio/">STUDIO</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="active" href="/sagas/">SAGAS</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/library/">LIBRARY</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/about/">ABOUT</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a href="/feed.xml">RSS</a>
        </nav>

        
        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep 05] Architecture Diagram &amp; Narrative — The Origin Blueprint / HireFlow</h1>
    </header>

    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">
    </p>

    
    <nav class="breadcrumb">
        <a href="/sagas/hireflow/">← HireFlow</a>
        <span class="sep">/</span>
        <a href="/sagas/hireflow/the-origin-blueprint/">The Origin Blueprint</a>
    </nav>
    <h2 class="episode-title">Architecture Diagram &amp; Narrative</h2>
    <div class="text-xs text-zinc-500 mb-3">
        2025-12-29 · <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/">back to arc</a>
    </div>
    
    <p class="text-sm text-zinc-400 mb-4">We consolidate the Origin Blueprint into a coherent MVP architecture. This episode presents the system map, explains the architectural intent, and defines what ‘done’ means for Hireflow’s first milestone.</p>
    

    <article class="prose prose-invert max-w-none">
        <h3>Architecture Diagram &amp; Narrative</h3>
<p>Every arc needs a moment of stillness.</p>
<p>Not because everything is solved —
but because enough structure exists to stop wandering and start building with intention.</p>
<p>This episode closes <strong>The Origin Blueprint</strong>.
Here we freeze the map <em>just enough</em> to move forward.</p>
<hr>
<h4>1. What We Have Built So Far (Conceptually)</h4>
<p>Across the previous episodes, Hireflow emerged organically:</p>
<ul>
<li>from an ambiguous briefing</li>
<li>through actors and roles</li>
<li>into service boundaries</li>
<li>connected by events</li>
<li>shaped by real-world constraints</li>
</ul>
<p>We did not start with boxes and arrows.
The boxes appeared because responsibility demanded them.</p>
<p>Now we can finally step back and look at the system as a whole.</p>
<hr>
<h4>2. The MVP Architecture (Narrative View)</h4>
<p>At MVP level, Hireflow is composed of <strong>small, authoritative services</strong>, each owning a clear part of the domain.</p>
<h5>Core Services</h5>
<ul>
<li>
<p><strong>Identity</strong></p>
<ul>
<li>authentication</li>
<li>authorization</li>
<li>role management (Company Admin, Recruiter, Candidate)</li>
</ul>
</li>
<li>
<p><strong>Company-Jobs</strong></p>
<ul>
<li>companies</li>
<li>job postings</li>
<li>recruiter associations</li>
</ul>
</li>
<li>
<p><strong>Candidates</strong></p>
<ul>
<li>candidate profiles</li>
<li>resumes (metadata, not files yet)</li>
<li>candidate lifecycle</li>
</ul>
</li>
<li>
<p><strong>Applications</strong></p>
<ul>
<li>applications</li>
<li>status transitions</li>
<li>screening / evaluation (basic rules)</li>
</ul>
</li>
<li>
<p><strong>Notifications</strong></p>
<ul>
<li>outbound communication</li>
<li>email delivery</li>
<li>template handling</li>
</ul>
</li>
<li>
<p><strong>Search</strong></p>
<ul>
<li>denormalized views</li>
<li>job and application indexing</li>
<li>fast querying</li>
</ul>
</li>
<li>
<p><strong>Gateway</strong></p>
<ul>
<li>single entry point</li>
<li>routing</li>
<li>token validation</li>
</ul>
</li>
<li>
<p><strong>Scheduler / Timer</strong></p>
<ul>
<li>time-based triggers</li>
<li>cleanup</li>
<li>delayed workflows</li>
</ul>
</li>
</ul>
<p>Each service:</p>
<ul>
<li>owns its data</li>
<li>owns its decisions</li>
<li>communicates via events</li>
</ul>
<p>No shared databases.
No hidden coupling.</p>
<hr>
<h4>3. The Architecture Diagram (Mental Model)</h4>
<p>Instead of a visually dense diagram, Hireflow favors a <strong>mental model that fits in your head</strong>:</p>
<pre><code>                 ┌──────────┐
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
</code></pre>
<p>Events flow <em>outward</em>.
Authority flows <em>inward</em>.</p>
<p>This asymmetry is intentional.</p>
<hr>
<h4>4. The MVP Definition (What “Done” Means)</h4>
<p>For Hireflow, <strong>MVP does not mean feature-complete</strong>.
It means <strong>end-to-end coherent</strong>.</p>
<h5><strong>MVP Capabilities</strong></h5>
<ul>
<li>Company Admin can create a company</li>
<li>Company Admin can post a job</li>
<li>Candidate can create a profile</li>
<li>Candidate can apply for a job</li>
<li>Recruiter can see applications</li>
<li>Notifications are sent asynchronously</li>
<li>Search indexes jobs and applications</li>
<li>System survives partial failures</li>
</ul>
<p>No AI.<br>
No advanced ranking.<br>
No UI polish.</p>
<p>Just a working, believable hiring flow.</p>
<hr>
<h4>5. The Real Milestones (What Exists, What Matters, Where We Are)</h4>
<p>With the Origin Blueprint complete, progress is no longer abstract.
From here on, milestones are not ideas — they are <strong>operational checkpoints</strong>.</p>
<p>Each one answers a single question:
<em>“What must exist for the system to be considered real at this stage?”</em></p>
<hr>
<h5>Milestone 0 — Bootable Skeleton</h5>
<p>This milestone answers a fundamental question:</p>
<blockquote>
<p><em>Can the system exist, start, deploy, and communicate — even before doing anything useful?</em></p>
</blockquote>
<p><strong>Services</strong></p>
<ul>
<li>Identity</li>
<li>Company &amp; Jobs</li>
<li>Candidates</li>
<li>Applications</li>
<li>Search</li>
<li>Notifications</li>
<li>Gateway</li>
</ul>
<p><strong>Infrastructure</strong></p>
<ul>
<li>Kubernetes</li>
<li>RabbitMQ</li>
<li>SQL Server</li>
<li>MongoDB</li>
<li>Redis</li>
<li>Blob storage</li>
</ul>
<p><strong>CI/CD</strong></p>
<ul>
<li>build</li>
<li>test</li>
<li>Helm deploy</li>
<li>smoke tests</li>
</ul>
<p>At this stage, the system may feel empty — and that is intentional.
A system that cannot boot, deploy, or be redeployed safely is not a system yet.</p>
<hr>
<h5>Milestone 1 — The “Happy Path”</h5>
<p>Once the skeleton stands, we breathe life into it.</p>
<p>This milestone defines the <strong>first believable hiring flow</strong>, end to end:</p>
<ul>
<li>create company &amp; recruiter</li>
<li>publish job</li>
<li>candidate applies (resume upload)</li>
<li>screening score is calculated</li>
<li>application moves to interview</li>
<li>interview slot is scheduled</li>
<li>notification email is sent</li>
</ul>
<p>No edge cases.
No optimization.
Just the core story working from start to finish.</p>
<p>If this works, Hireflow becomes demonstrable — not impressive, but real.</p>
<hr>
<h5>Milestone 2 — Scale &amp; Resiliency</h5>
<p>This is where the system stops pretending the world is kind.</p>
<p>Here, we assume:</p>
<ul>
<li>queues grow</li>
<li>services fail</li>
<li>traffic spikes</li>
<li>retries happen</li>
<li>messages duplicate</li>
</ul>
<p>And we design for that reality.</p>
<p><strong>Focus areas</strong></p>
<ul>
<li>KEDA scaling based on queue depth</li>
<li>circuit breaker on Search</li>
<li>outbox pattern for Applications → Messaging</li>
<li>retries and dead-letter queues</li>
<li>DLQ viewer for operational visibility</li>
</ul>
<p>This milestone does not add features.
It adds <strong>trust</strong>.</p>
<p>A system that survives pressure is more valuable than one with more buttons.</p>
<hr>
<h5>Milestone 3 — Observability &amp; Security</h5>
<p>Once the system survives, we make it <em>visible</em> and <em>responsible</em>.</p>
<p><strong>Observability</strong></p>
<p>Trace a request across:</p>
<ul>
<li>gateway → applications → workers</li>
<li>Jaeger-based distributed tracing</li>
<li>correlation IDs as first-class citizens</li>
</ul>
<p><strong>Security</strong></p>
<ul>
<li>RBAC unit tests</li>
<li>PII encryption at rest</li>
<li>GDPR “export my data” and “delete me” jobs</li>
</ul>
<p>This is the point where Hireflow can be operated with confidence — not just built.</p>
<hr>
<h5>After the MVP: UX &amp; Intelligence</h5>
<p>UX and AI come <strong>after</strong> the MVP — deliberately.</p>
<p>They are not foundations; they are amplifiers.</p>
<ul>
<li>recruiter dashboards</li>
<li>candidate experience polish</li>
<li>AI-assisted resume analysis</li>
<li>scoring explanations and matching</li>
</ul>
<p>By postponing them, we ensure they sit on top of something solid — not something fragile.</p>
<hr>
<h5>Why This Ordering Matters</h5>
<p>Most systems fail because they invert this order:</p>
<ul>
<li>UX before resilience</li>
<li>intelligence before observability</li>
<li>features before trust</li>
</ul>
<p>Hireflow does the opposite.</p>
<p>That is not faster.
But it is durable.</p>
<p>And durability is what allows a system — and a team — to keep moving forward.</p>
<hr>
<h4>6. Why This Arc Ends Here</h4>
<p>The Origin Blueprint ends not because uncertainty is gone —
but because <strong>ambiguity has been reduced enough to act</strong>.</p>
<p>From now on:</p>
<ul>
<li>code will appear</li>
<li>infrastructure will matter</li>
<li>mistakes will be concrete</li>
<li>trade-offs will be visible</li>
</ul>
<p>The narrative shifts from <em>why</em> to <em>how</em>.</p>
<p>This is the natural transition from <strong>thinking</strong> to <strong>execution</strong>.</p>
<hr>
<h4>Closing Reflection</h4>
<p>Good architecture does not feel clever.
It feels calm.</p>
<p>It leaves space for change.
It resists urgency.
It makes the next decision easier than the previous one.</p>
<p>With the Origin Blueprint complete, Hireflow is no longer an idea.
It is a system with intent.</p>
<p>And now, we build.</p>
<hr>
<h4>Arc Closed</h4>
<p><strong>Hireflow — The Origin Blueprint</strong></p>

    </article>

    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">
        <a class="hover:underline" href="/sagas/hireflow/the-origin-blueprint/interactions-flows-and-early-event-design/">← Ep 04 Interactions, Flows &amp; Early Event Design</a>
        
    </nav>


    <footer class="mt-10 text-xs text-zinc-500">
        © 2025 wastingnotime.org — built with Go
    </footer>
</div>
</body>
</html>


        """,
    'sagas/game-hub/the-first-breath/the-first-steps': """

    
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>The First Steps — Game Hub</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>
    <style>
        html { font-kerning: normal; }

         
        .menu a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        .menu a:hover {
            color:#fff;
            text-decoration:underline;
        }
        .menu a.active {
            color:#fff;
            font-weight:500;
        }
        .menu a.active::after {
            content:"•";
            margin-left:0.4em;
            opacity:0.6;
            font-weight:400;
        }

         
        a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        a:hover {
            color:#fff;
            text-decoration:underline;
        }

         
        ul {
            list-style:none;
            padding-left:0;
            margin:0;
        }

         
        .intro:empty {
            display:none;
        }

         
        .space-y-1 > * + * { margin-top: .25rem; }
        .space-y-2 > * + * { margin-top: .5rem; }
        .space-y-3 > * + * { margin-top: .75rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }

        .breadcrumb {
            font-size:0.9rem;
            color:#888;
            margin-bottom:1.5rem;
        }
        .breadcrumb a {
            color:#aaa;
            text-decoration:none;
        }
        .breadcrumb a:hover {
            text-decoration:underline;
            color:#fff;
        }
        .breadcrumb .sep {
            margin:0 .4rem;
            color:#555;
        }

        .arc-name,
        .episode-title {
            color:#fff;
            font-weight:500;
            margin:0 0 1rem 0;
            font-size:1.1rem;
        }

        .topic-link {
            border-width:1px;
            border-color: rgb(39 39 42);
            border-style: solid;
            border-radius:.25rem;
            padding:.5rem .75rem;
            color: rgb(244 244 245);
            text-decoration:none;
            transition: color .15s ease, border-color .15s ease;
        }
        .topic-link:hover {
            border-color: rgba(255,255,255,.4);
            color:#fff;
            text-decoration:underline;
        }

          
          

         .prose {
             max-width: none;
             --wnt-text-100: rgb(244 244 245);
             --wnt-text-200: rgb(228 228 231);
             --wnt-text-300: rgb(212 212 216);
             --wnt-text-400: rgb(161 161 170);
             --wnt-border:   rgb(39 39 42);
         }

         
        .prose h2 {
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #fff;
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.6;
        }
        .prose h3 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: var(--wnt-text-200);
            font-weight: 500;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .prose h3 strong { font-weight: 500; }

         
        .prose p {
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
            color: var(--wnt-text-200);
        }
        .prose h2 + p,
        .prose h3 + p { margin-top: 0.75rem; }

         
        .prose blockquote {
            border-left: 2px solid rgb(63 63 70);
            padding-left: 1rem;
            margin: 1.75rem 0;
            color: var(--wnt-text-300);
            font-style: italic;
            line-height: 1.8;
        }
        .prose blockquote p { margin: 0; }
        .prose blockquote strong { color: #fff; font-weight: 500; }

         
        .prose ul { list-style: disc; }
        .prose ol { list-style: decimal; }
        .prose ul, .prose ol {
            margin: 1.25rem 0;
            padding-left: 1.25rem;
            color: var(--wnt-text-200);
        }
        .prose li + li { margin-top: 0.35rem; }
        .prose li > p { margin: 0.25rem 0; }

         
        .prose code {
            background: rgba(255,255,255,0.04);
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            color: var(--wnt-text-100);
        }
        .prose pre {
            margin: 1.5rem 0;
            padding: 1rem;
            background: #0b0b0b;
            border: 1px solid var(--wnt-border);
            border-radius: 0.5rem;
            overflow: auto;
        }
        .prose pre code { background: transparent; padding: 0; border-radius: 0; }

         
        .prose a {
            color: var(--wnt-text-400);
            text-decoration: underline;
            text-decoration-thickness: .06em;
            text-underline-offset: 2px;
        }
        .prose a:hover { color: #fff; }

         
        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }
        .prose figure { margin: 1.75rem 0; }
        .prose figcaption {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--wnt-text-400);
            text-align: center;
        }
        .prose hr {
            border: 0;
            border-top: 1px solid var(--wnt-border);
            margin: 2rem 0;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            color: var(--wnt-text-200);
        }
        .prose thead th {
            text-align: left;
            font-weight: 600;
            color: #fff;
            border-bottom: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }
        .prose tbody td {
            border-top: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }

         
        .prose :last-child { margin-bottom: 0 !important; }
    </style>
    
</head>
<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">
<div class="max-w-3xl mx-auto px-4 py-6">
    <header class="mb-6">
        <nav class="menu text-sm text-zinc-400">
            <a class="" href="/">HOME</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/studio/">STUDIO</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="active" href="/sagas/">SAGAS</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/library/">LIBRARY</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/about/">ABOUT</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a href="/feed.xml">RSS</a>
        </nav>

        
        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep 01] The First Steps — The First Breath / Game Hub</h1>
    </header>

    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">
    </p>

    
    <nav class="breadcrumb">
        <a href="/sagas/game-hub/">← Game Hub</a>
        <span class="sep">/</span>
        <a href="/sagas/game-hub/the-first-breath/">The First Breath</a>
    </nav>
    <h2 class="episode-title">The First Steps</h2>
    <div class="text-xs text-zinc-500 mb-3">
        2025-10-31 · <a class="hover:underline" href="/sagas/game-hub/the-first-breath/">back to arc</a>
    </div>
    
    <p class="text-sm text-zinc-400 mb-4">Every creation starts with a breath. This episode shares how WastingNoTime came to life through curiosity, challenge, and a bit of rebellion — choosing to build a Game Hub as a living lab for ideas and code.</p>
    

    <article class="prose prose-invert max-w-none">
        <h3>The First Steps</h3>
<p>There’s nothing like a challenge to wake us up — to stretch our skills, flip our perspective, and remind us how it feels to build something from zero.<br>
That’s exactly what we’ll do here.</p>
<p>From infinite possibilities, I chose one simple act: <strong>take an idea and make it real.</strong><br>
That’s the whole mission.<br>
From now on, we’ll think, design, test, break, and rebuild — together.</p>
<p>Sometimes the model won’t fit reality. Sometimes reality will whisper, <em>“No, not that way.”</em><br>
And that’s part of the process.<br>
The only way to never walk the wrong path is to have already mapped it — and no one starts with a map.<br>
Every first time carries a chance to fail, but failure isn’t the end; it’s the moment the compass finally points the right direction.</p>
<p>Across the next episodes, we’ll explore and reason side by side, turning ideas into code, and code into understanding.</p>
<p>As a starting point, I wanted something ambitious but playful — something that mixes architecture, fun, and learning.<br>
So I thought: <strong>why not build a small Game Hub?</strong><br>
A space where multiple games can live, grow, and talk to each other — like a tiny ecosystem in the cloud.</p>
<hr>
<h3>Why a Game Hub?</h3>
<p>Choosing what to build is harder than building itself.<br>
Many creators freeze in front of a blank page, thinking, <em>“Where do I even start?”</em></p>
<p>To make it simpler, I created one rule: <strong>no more to-do lists.</strong><br>
They’re the go-to demo, but too sterile — no emotion, no tension, no story.<br>
And if we don’t even use them ourselves, what’s the point?</p>
<p>On the other hand, going too far — like an ERP or banking system — would be too heavy.<br>
We’d lose the spark of experimentation.<br>
And here at <em>WastingNoTime</em>, there’s one non-negotiable rule:</p>
<blockquote>
<p><strong>We must have fun, or we’re doing it wrong.</strong></p>
</blockquote>
<p>So by balancing complexity, size, and joy, games became the perfect playground.<br>
But instead of building <em>a</em> game, we’ll build <em>the place where games live</em>: a <strong>Game Hub</strong>.</p>
<p>It’s the perfect middle ground — technically rich, creatively open, and built to evolve.</p>
<hr>
<h3>So What’s a Game Hub?</h3>
<p>Imagine a small digital arcade in the cloud.<br>
Players arrive, pick a game, challenge each other, maybe check their scores — all in one connected space.<br>
The hub doesn’t care if the game is trivia, cards, or chess — it just handles what every game needs: identity, communication, matches, and results.</p>
<p>That’s our canvas.</p>
<hr>
<h3>The Journey Ahead</h3>
<p>In the real world, software starts from requirements; someone already knows what the customer wants.<br>
But here, we’ve chosen a different mode: <strong>exploration.</strong><br>
We’ll discover what we need as we build it.<br>
That takes maturity, curiosity, and a bit of bravery — the same values that shape <em>WastingNoTime</em> itself.</p>
<p>And to give our Game Hub its first breath, we need one simple thing: a game.<br>
Something we can use to test, validate, and grow the hub.</p>
<p>That’s when our AI partner leaned in and said:</p>
<blockquote>
<p>“Hey human, to validate your hub, skip the hard graphics and physics. Go with something that’s simple, fun, and competitive — like a <strong>Trivia Duel.</strong>”</p>
</blockquote>
<p>And just like that, our first duel was born.<br>
A spark. A breath. The first steps of something that will keep evolving.</p>

    </article>

    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">
        <span></span>
        <a class="hover:underline" href="/sagas/game-hub/the-first-breath/epic-continues/">Ep 02 Epic Continues — The Duel Begins →</a>
    </nav>


    <footer class="mt-10 text-xs text-zinc-500">
        © 2025 wastingnotime.org — built with Go
    </footer>
</div>
</body>
</html>


        """,
    'sagas/game-hub/the-first-breath/epic-continues': """

    
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Epic Continues — The Duel Begins — Game Hub</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>
    <style>
        html { font-kerning: normal; }

         
        .menu a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        .menu a:hover {
            color:#fff;
            text-decoration:underline;
        }
        .menu a.active {
            color:#fff;
            font-weight:500;
        }
        .menu a.active::after {
            content:"•";
            margin-left:0.4em;
            opacity:0.6;
            font-weight:400;
        }

         
        a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        a:hover {
            color:#fff;
            text-decoration:underline;
        }

         
        ul {
            list-style:none;
            padding-left:0;
            margin:0;
        }

         
        .intro:empty {
            display:none;
        }

         
        .space-y-1 > * + * { margin-top: .25rem; }
        .space-y-2 > * + * { margin-top: .5rem; }
        .space-y-3 > * + * { margin-top: .75rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }

        .breadcrumb {
            font-size:0.9rem;
            color:#888;
            margin-bottom:1.5rem;
        }
        .breadcrumb a {
            color:#aaa;
            text-decoration:none;
        }
        .breadcrumb a:hover {
            text-decoration:underline;
            color:#fff;
        }
        .breadcrumb .sep {
            margin:0 .4rem;
            color:#555;
        }

        .arc-name,
        .episode-title {
            color:#fff;
            font-weight:500;
            margin:0 0 1rem 0;
            font-size:1.1rem;
        }

        .topic-link {
            border-width:1px;
            border-color: rgb(39 39 42);
            border-style: solid;
            border-radius:.25rem;
            padding:.5rem .75rem;
            color: rgb(244 244 245);
            text-decoration:none;
            transition: color .15s ease, border-color .15s ease;
        }
        .topic-link:hover {
            border-color: rgba(255,255,255,.4);
            color:#fff;
            text-decoration:underline;
        }

          
          

         .prose {
             max-width: none;
             --wnt-text-100: rgb(244 244 245);
             --wnt-text-200: rgb(228 228 231);
             --wnt-text-300: rgb(212 212 216);
             --wnt-text-400: rgb(161 161 170);
             --wnt-border:   rgb(39 39 42);
         }

         
        .prose h2 {
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #fff;
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.6;
        }
        .prose h3 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: var(--wnt-text-200);
            font-weight: 500;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .prose h3 strong { font-weight: 500; }

         
        .prose p {
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
            color: var(--wnt-text-200);
        }
        .prose h2 + p,
        .prose h3 + p { margin-top: 0.75rem; }

         
        .prose blockquote {
            border-left: 2px solid rgb(63 63 70);
            padding-left: 1rem;
            margin: 1.75rem 0;
            color: var(--wnt-text-300);
            font-style: italic;
            line-height: 1.8;
        }
        .prose blockquote p { margin: 0; }
        .prose blockquote strong { color: #fff; font-weight: 500; }

         
        .prose ul { list-style: disc; }
        .prose ol { list-style: decimal; }
        .prose ul, .prose ol {
            margin: 1.25rem 0;
            padding-left: 1.25rem;
            color: var(--wnt-text-200);
        }
        .prose li + li { margin-top: 0.35rem; }
        .prose li > p { margin: 0.25rem 0; }

         
        .prose code {
            background: rgba(255,255,255,0.04);
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            color: var(--wnt-text-100);
        }
        .prose pre {
            margin: 1.5rem 0;
            padding: 1rem;
            background: #0b0b0b;
            border: 1px solid var(--wnt-border);
            border-radius: 0.5rem;
            overflow: auto;
        }
        .prose pre code { background: transparent; padding: 0; border-radius: 0; }

         
        .prose a {
            color: var(--wnt-text-400);
            text-decoration: underline;
            text-decoration-thickness: .06em;
            text-underline-offset: 2px;
        }
        .prose a:hover { color: #fff; }

         
        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }
        .prose figure { margin: 1.75rem 0; }
        .prose figcaption {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--wnt-text-400);
            text-align: center;
        }
        .prose hr {
            border: 0;
            border-top: 1px solid var(--wnt-border);
            margin: 2rem 0;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            color: var(--wnt-text-200);
        }
        .prose thead th {
            text-align: left;
            font-weight: 600;
            color: #fff;
            border-bottom: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }
        .prose tbody td {
            border-top: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }

         
        .prose :last-child { margin-bottom: 0 !important; }
    </style>
    
</head>
<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">
<div class="max-w-3xl mx-auto px-4 py-6">
    <header class="mb-6">
        <nav class="menu text-sm text-zinc-400">
            <a class="" href="/">HOME</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/studio/">STUDIO</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="active" href="/sagas/">SAGAS</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/library/">LIBRARY</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/about/">ABOUT</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a href="/feed.xml">RSS</a>
        </nav>

        
        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep 02] Epic Continues — The Duel Begins — The First Breath / Game Hub</h1>
    </header>

    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">
    </p>

    
    <nav class="breadcrumb">
        <a href="/sagas/game-hub/">← Game Hub</a>
        <span class="sep">/</span>
        <a href="/sagas/game-hub/the-first-breath/">The First Breath</a>
    </nav>
    <h2 class="episode-title">Epic Continues — The Duel Begins</h2>
    <div class="text-xs text-zinc-500 mb-3">
        2025-11-07 · <a class="hover:underline" href="/sagas/game-hub/the-first-breath/">back to arc</a>
    </div>
    
    <p class="text-sm text-zinc-400 mb-4">The spark of Trivia Duel marks the moment when play meets architecture. Beneath the simplicity of two minds facing a question, patterns of state, timing, and fairness begin to unfold — the quiet architecture behind every duel.</p>
    

    <article class="prose prose-invert max-w-none">
        <h3>Epic continues — the duel begins</h3>
<p>Alright, so we have our north star: <strong>Trivia Duel</strong> — a simple, fun, and competitive game.</p>
<p>The name already brings movement: two minds, one question, and a bit of pride on the line. It’s light enough to test fast, but structured enough to teach us about user sessions, score tracking, concurrency, and fairness — the kind of things that appear in real systems all the time.</p>
<p>But before we start coding anything, let’s slow down.<br>
We need to understand what <em>“a duel”</em> really means in system terms.</p>
<p>Two players → a match.<br>
Each match → a sequence of questions.<br>
Each question → a small interaction cycle.<br>
Each cycle → requests, responses, and timeouts.</p>
<p>It sounds simple, but inside those lines hide every challenge we love to face: state management, latency, synchronization, and the eternal dance between <strong>frontend experience</strong> and <strong>backend reliability</strong>.</p>
<p>So yes, it’s a “simple game,” but in disguise, it’s a <strong>distributed system</strong> in miniature — perfect terrain for what <em>wasting no time</em> is all about.</p>
<hr>
<h3>Starting by the invisible part</h3>
<p>We’ll begin, as usual, by the part no one sees: the backend.<br>
Not because we don’t care about visuals, but because <strong>structure creates freedom</strong>. Once the rules are clear, everything else can grow on solid ground.</p>
<p>The first steps will be small:</p>
<ol>
<li>
<p>Define how players join a duel.</p>
</li>
<li>
<p>Define how questions are delivered and answered.</p>
</li>
<li>
<p>Track progress, score, and results.</p>
</li>
<li>
<p>Keep everything stateless — or as stateless as possible — so it can scale later.</p>
</li>
</ol>
<p>Simple goals, but each one opens doors to concepts like event-driven flows, in-memory caching, and API orchestration.</p>
<hr>
<h3>Designing from curiosity, not from fear</h3>
<p>We won’t rush.<br>
Every design decision will be a conversation: between code, context, and curiosity.</p>
<p>Sometimes the answer will come fast.<br>
Sometimes, we’ll stop, think, and say, <em>“This doesn’t feel right yet.”</em><br>
And that’s fine. Because here, there’s no rush to impress — only a steady pace toward understanding.</p>
<p>This is not just a tutorial; it’s a record of thought in motion — one that others can read, fork, and build upon.</p>
<p>So, let’s prepare the ground for our duel.<br>
Next: we’ll describe <strong>how a duel is born</strong> — from a simple API call to the first spark of competition.</p>

    </article>

    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">
        <a class="hover:underline" href="/sagas/game-hub/the-first-breath/the-first-steps/">← Ep 01 The First Steps</a>
        <a class="hover:underline" href="/sagas/game-hub/the-first-breath/how-a-duel-is-born/">Ep 03 How a Duel Is Born →</a>
    </nav>


    <footer class="mt-10 text-xs text-zinc-500">
        © 2025 wastingnotime.org — built with Go
    </footer>
</div>
</body>
</html>


        """,
    'sagas/game-hub/the-first-breath/how-a-duel-is-born': """

    
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>How a Duel Is Born — Game Hub</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>
    <style>
        html { font-kerning: normal; }

         
        .menu a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        .menu a:hover {
            color:#fff;
            text-decoration:underline;
        }
        .menu a.active {
            color:#fff;
            font-weight:500;
        }
        .menu a.active::after {
            content:"•";
            margin-left:0.4em;
            opacity:0.6;
            font-weight:400;
        }

         
        a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        a:hover {
            color:#fff;
            text-decoration:underline;
        }

         
        ul {
            list-style:none;
            padding-left:0;
            margin:0;
        }

         
        .intro:empty {
            display:none;
        }

         
        .space-y-1 > * + * { margin-top: .25rem; }
        .space-y-2 > * + * { margin-top: .5rem; }
        .space-y-3 > * + * { margin-top: .75rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }

        .breadcrumb {
            font-size:0.9rem;
            color:#888;
            margin-bottom:1.5rem;
        }
        .breadcrumb a {
            color:#aaa;
            text-decoration:none;
        }
        .breadcrumb a:hover {
            text-decoration:underline;
            color:#fff;
        }
        .breadcrumb .sep {
            margin:0 .4rem;
            color:#555;
        }

        .arc-name,
        .episode-title {
            color:#fff;
            font-weight:500;
            margin:0 0 1rem 0;
            font-size:1.1rem;
        }

        .topic-link {
            border-width:1px;
            border-color: rgb(39 39 42);
            border-style: solid;
            border-radius:.25rem;
            padding:.5rem .75rem;
            color: rgb(244 244 245);
            text-decoration:none;
            transition: color .15s ease, border-color .15s ease;
        }
        .topic-link:hover {
            border-color: rgba(255,255,255,.4);
            color:#fff;
            text-decoration:underline;
        }

          
          

         .prose {
             max-width: none;
             --wnt-text-100: rgb(244 244 245);
             --wnt-text-200: rgb(228 228 231);
             --wnt-text-300: rgb(212 212 216);
             --wnt-text-400: rgb(161 161 170);
             --wnt-border:   rgb(39 39 42);
         }

         
        .prose h2 {
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #fff;
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.6;
        }
        .prose h3 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: var(--wnt-text-200);
            font-weight: 500;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .prose h3 strong { font-weight: 500; }

         
        .prose p {
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
            color: var(--wnt-text-200);
        }
        .prose h2 + p,
        .prose h3 + p { margin-top: 0.75rem; }

         
        .prose blockquote {
            border-left: 2px solid rgb(63 63 70);
            padding-left: 1rem;
            margin: 1.75rem 0;
            color: var(--wnt-text-300);
            font-style: italic;
            line-height: 1.8;
        }
        .prose blockquote p { margin: 0; }
        .prose blockquote strong { color: #fff; font-weight: 500; }

         
        .prose ul { list-style: disc; }
        .prose ol { list-style: decimal; }
        .prose ul, .prose ol {
            margin: 1.25rem 0;
            padding-left: 1.25rem;
            color: var(--wnt-text-200);
        }
        .prose li + li { margin-top: 0.35rem; }
        .prose li > p { margin: 0.25rem 0; }

         
        .prose code {
            background: rgba(255,255,255,0.04);
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            color: var(--wnt-text-100);
        }
        .prose pre {
            margin: 1.5rem 0;
            padding: 1rem;
            background: #0b0b0b;
            border: 1px solid var(--wnt-border);
            border-radius: 0.5rem;
            overflow: auto;
        }
        .prose pre code { background: transparent; padding: 0; border-radius: 0; }

         
        .prose a {
            color: var(--wnt-text-400);
            text-decoration: underline;
            text-decoration-thickness: .06em;
            text-underline-offset: 2px;
        }
        .prose a:hover { color: #fff; }

         
        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }
        .prose figure { margin: 1.75rem 0; }
        .prose figcaption {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--wnt-text-400);
            text-align: center;
        }
        .prose hr {
            border: 0;
            border-top: 1px solid var(--wnt-border);
            margin: 2rem 0;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            color: var(--wnt-text-200);
        }
        .prose thead th {
            text-align: left;
            font-weight: 600;
            color: #fff;
            border-bottom: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }
        .prose tbody td {
            border-top: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }

         
        .prose :last-child { margin-bottom: 0 !important; }
    </style>
    
</head>
<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">
<div class="max-w-3xl mx-auto px-4 py-6">
    <header class="mb-6">
        <nav class="menu text-sm text-zinc-400">
            <a class="" href="/">HOME</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/studio/">STUDIO</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="active" href="/sagas/">SAGAS</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/library/">LIBRARY</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/about/">ABOUT</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a href="/feed.xml">RSS</a>
        </nav>

        
        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep 03] How a Duel Is Born — The First Breath / Game Hub</h1>
    </header>

    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">
    </p>

    
    <nav class="breadcrumb">
        <a href="/sagas/game-hub/">← Game Hub</a>
        <span class="sep">/</span>
        <a href="/sagas/game-hub/the-first-breath/">The First Breath</a>
    </nav>
    <h2 class="episode-title">How a Duel Is Born</h2>
    <div class="text-xs text-zinc-500 mb-3">
        2025-11-14 · <a class="hover:underline" href="/sagas/game-hub/the-first-breath/">back to arc</a>
    </div>
    
    <p class="text-sm text-zinc-400 mb-4">A duel begins not with code, but with intent — two players entering the same rhythm of curiosity. Here we shape the invisible choreography: how sessions emerge, how rules awaken, and how a spark becomes a match.</p>
    

    <article class="prose prose-invert max-w-none">
        <h3>How a Duel is Born</h3>
<p>Every story begins with a spark — and in our case, that spark is a <strong>player’s decision to start a duel.</strong></p>
<p>Someone, somewhere, clicks <em>“Play.”</em><br>
That single action sets the system in motion.</p>
<p>Behind that innocent button, a few invisible steps happen — the kind that make the difference between a toy and a working system.</p>
<hr>
<h4><strong>Step 1 — The Challenge</strong></h4>
<p>When a player hits “Play,” the frontend sends a simple request to the backend:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>POST /duel/start
</span></span></code></pre><p>That endpoint doesn’t create a duel right away — it creates a <strong>challenge</strong>.<br>
A challenge is like saying: “I’m ready. Find me an opponent.”</p>
<p>This step lets us separate <strong>intention</strong> from <strong>action.</strong><br>
In distributed systems, that’s gold — it means we can queue, match, or cancel safely without breaking the flow.</p>
<p>The backend stores this challenge in a lightweight structure:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>{
</span></span><span style="display:flex;"><span>  playerID: <span style="color:#f1fa8c">&#34;P001&#34;</span>,
</span></span><span style="display:flex;"><span>  status: <span style="color:#f1fa8c">&#34;waiting&#34;</span>,
</span></span><span style="display:flex;"><span>  createdAt: <span style="color:#f1fa8c">&#34;2025-10-31T18:00:00Z&#34;</span>
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>Simple, but scalable.<br>
If no opponent arrives within a few seconds, we can even trigger an AI opponent — a fallback that keeps the experience smooth.</p>
<hr>
<h4><strong>Step 2 — The Matchmaker</strong></h4>
<p>Somewhere in our cloud, a <strong>matchmaker process</strong> wakes up.<br>
Its only job is to watch for lonely challengers and connect them.<br>
When it finds two compatible players (or one human and one AI), it creates a new record:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>{
</span></span><span style="display:flex;"><span>  duelID: <span style="color:#f1fa8c">&#34;D123&#34;</span>,
</span></span><span style="display:flex;"><span>  players: [<span style="color:#f1fa8c">&#34;P001&#34;</span>, <span style="color:#f1fa8c">&#34;P002&#34;</span>],
</span></span><span style="display:flex;"><span>  state: <span style="color:#f1fa8c">&#34;starting&#34;</span>,
</span></span><span style="display:flex;"><span>  questions: [],
</span></span><span style="display:flex;"><span>  createdAt: <span style="color:#ff79c6">...</span>
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>That’s the birth of a duel — a microcosm of logic, waiting to unfold.</p>
<hr>
<h4><strong>Step 3 — The Arena</strong></h4>
<p>Once the duel is created, both players receive a notification:</p>
<blockquote>
<p>“Opponent found. Get ready!”</p>
</blockquote>
<p>Here we have a decision to make — should we use WebSockets for live interaction or keep it simple with request/response polling?</p>
<p>We’ll start simple.<br>
A good architect doesn’t overcomplicate the first step — we’ll use stateless APIs and maybe a touch of in-memory state to simulate real-time behavior. Later, we can evolve to WebSockets, event streams, or even serverless functions triggered by updates.</p>
<p>This staged growth mirrors real projects: <strong>start with clarity, evolve with purpose.</strong></p>
<hr>
<h4><strong>Step 4 — The Game Loop</strong></h4>
<p>The duel begins.<br>
Each round, the backend picks a question from a shared trivia bank (stored in a JSON or DynamoDB table), sends it to both players, and waits for their answers.</p>
<p>Players answer through:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>POST /duel/{duelID}/answer
</span></span></code></pre><p>The backend checks correctness, updates the score, and sends feedback.<br>
After a few rounds, the duel ends — not with fireworks, but with a neat, quiet line of JSON:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>{
</span></span><span style="display:flex;"><span>  duelID: <span style="color:#f1fa8c">&#34;D123&#34;</span>,
</span></span><span style="display:flex;"><span>  winner: <span style="color:#f1fa8c">&#34;P001&#34;</span>,
</span></span><span style="display:flex;"><span>  score: { <span style="color:#f1fa8c">&#34;P001&#34;</span>: <span style="color:#bd93f9">4</span>, <span style="color:#f1fa8c">&#34;P002&#34;</span>: <span style="color:#bd93f9">2</span> },
</span></span><span style="display:flex;"><span>  finishedAt: <span style="color:#ff79c6">...</span>
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>And that’s it — a completed duel, ready for leaderboard recording or replay.</p>
<hr>
<h3><strong>Step 5 — The Cycle Repeats</strong></h3>
<p>Every new duel feeds the system with experience:</p>
<ul>
<li>
<p>How fast players answered</p>
</li>
<li>
<p>Which questions were too easy or too hard</p>
</li>
<li>
<p>How balanced matches were</p>
</li>
</ul>
<p>That feedback loop is how the hub evolves — not through magic, but through <strong>data and iteration</strong>.</p>
<hr>
<h3><strong>From Concept to Cloud</strong></h3>
<p>This is how ideas start breathing.<br>
A click turns into an event.<br>
An event turns into data.<br>
Data turns into insight.<br>
And insight becomes the next version of our system.</p>
<p>Every small piece we build will follow this philosophy:</p>
<ul>
<li>
<p><strong>Simple first.</strong></p>
</li>
<li>
<p><strong>Understand before optimizing.</strong></p>
</li>
<li>
<p><strong>Evolve from clarity, not from noise.</strong></p>
</li>
</ul>
<p>And just like that, our <em>Game Hub</em> starts to exist — not fully formed, but alive.</p>

    </article>

    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">
        <a class="hover:underline" href="/sagas/game-hub/the-first-breath/epic-continues/">← Ep 02 Epic Continues — The Duel Begins</a>
        <a class="hover:underline" href="/sagas/game-hub/the-first-breath/designing-the-first-api/">Ep 04 Designing the First API — /duel/start →</a>
    </nav>


    <footer class="mt-10 text-xs text-zinc-500">
        © 2025 wastingnotime.org — built with Go
    </footer>
</div>
</body>
</html>


        """,
    'sagas/game-hub/the-first-breath/designing-the-first-api': """

    
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Designing the First API — /duel/start — Game Hub</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>
    <style>
        html { font-kerning: normal; }

         
        .menu a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        .menu a:hover {
            color:#fff;
            text-decoration:underline;
        }
        .menu a.active {
            color:#fff;
            font-weight:500;
        }
        .menu a.active::after {
            content:"•";
            margin-left:0.4em;
            opacity:0.6;
            font-weight:400;
        }

         
        a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        a:hover {
            color:#fff;
            text-decoration:underline;
        }

         
        ul {
            list-style:none;
            padding-left:0;
            margin:0;
        }

         
        .intro:empty {
            display:none;
        }

         
        .space-y-1 > * + * { margin-top: .25rem; }
        .space-y-2 > * + * { margin-top: .5rem; }
        .space-y-3 > * + * { margin-top: .75rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }

        .breadcrumb {
            font-size:0.9rem;
            color:#888;
            margin-bottom:1.5rem;
        }
        .breadcrumb a {
            color:#aaa;
            text-decoration:none;
        }
        .breadcrumb a:hover {
            text-decoration:underline;
            color:#fff;
        }
        .breadcrumb .sep {
            margin:0 .4rem;
            color:#555;
        }

        .arc-name,
        .episode-title {
            color:#fff;
            font-weight:500;
            margin:0 0 1rem 0;
            font-size:1.1rem;
        }

        .topic-link {
            border-width:1px;
            border-color: rgb(39 39 42);
            border-style: solid;
            border-radius:.25rem;
            padding:.5rem .75rem;
            color: rgb(244 244 245);
            text-decoration:none;
            transition: color .15s ease, border-color .15s ease;
        }
        .topic-link:hover {
            border-color: rgba(255,255,255,.4);
            color:#fff;
            text-decoration:underline;
        }

          
          

         .prose {
             max-width: none;
             --wnt-text-100: rgb(244 244 245);
             --wnt-text-200: rgb(228 228 231);
             --wnt-text-300: rgb(212 212 216);
             --wnt-text-400: rgb(161 161 170);
             --wnt-border:   rgb(39 39 42);
         }

         
        .prose h2 {
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #fff;
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.6;
        }
        .prose h3 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: var(--wnt-text-200);
            font-weight: 500;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .prose h3 strong { font-weight: 500; }

         
        .prose p {
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
            color: var(--wnt-text-200);
        }
        .prose h2 + p,
        .prose h3 + p { margin-top: 0.75rem; }

         
        .prose blockquote {
            border-left: 2px solid rgb(63 63 70);
            padding-left: 1rem;
            margin: 1.75rem 0;
            color: var(--wnt-text-300);
            font-style: italic;
            line-height: 1.8;
        }
        .prose blockquote p { margin: 0; }
        .prose blockquote strong { color: #fff; font-weight: 500; }

         
        .prose ul { list-style: disc; }
        .prose ol { list-style: decimal; }
        .prose ul, .prose ol {
            margin: 1.25rem 0;
            padding-left: 1.25rem;
            color: var(--wnt-text-200);
        }
        .prose li + li { margin-top: 0.35rem; }
        .prose li > p { margin: 0.25rem 0; }

         
        .prose code {
            background: rgba(255,255,255,0.04);
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            color: var(--wnt-text-100);
        }
        .prose pre {
            margin: 1.5rem 0;
            padding: 1rem;
            background: #0b0b0b;
            border: 1px solid var(--wnt-border);
            border-radius: 0.5rem;
            overflow: auto;
        }
        .prose pre code { background: transparent; padding: 0; border-radius: 0; }

         
        .prose a {
            color: var(--wnt-text-400);
            text-decoration: underline;
            text-decoration-thickness: .06em;
            text-underline-offset: 2px;
        }
        .prose a:hover { color: #fff; }

         
        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }
        .prose figure { margin: 1.75rem 0; }
        .prose figcaption {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--wnt-text-400);
            text-align: center;
        }
        .prose hr {
            border: 0;
            border-top: 1px solid var(--wnt-border);
            margin: 2rem 0;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            color: var(--wnt-text-200);
        }
        .prose thead th {
            text-align: left;
            font-weight: 600;
            color: #fff;
            border-bottom: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }
        .prose tbody td {
            border-top: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }

         
        .prose :last-child { margin-bottom: 0 !important; }
    </style>
    
</head>
<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">
<div class="max-w-3xl mx-auto px-4 py-6">
    <header class="mb-6">
        <nav class="menu text-sm text-zinc-400">
            <a class="" href="/">HOME</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/studio/">STUDIO</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="active" href="/sagas/">SAGAS</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/library/">LIBRARY</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/about/">ABOUT</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a href="/feed.xml">RSS</a>
        </nav>

        
        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep 04] Designing the First API — /duel/start — The First Breath / Game Hub</h1>
    </header>

    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">
    </p>

    
    <nav class="breadcrumb">
        <a href="/sagas/game-hub/">← Game Hub</a>
        <span class="sep">/</span>
        <a href="/sagas/game-hub/the-first-breath/">The First Breath</a>
    </nav>
    <h2 class="episode-title">Designing the First API — /duel/start</h2>
    <div class="text-xs text-zinc-500 mb-3">
        2025-11-24 · <a class="hover:underline" href="/sagas/game-hub/the-first-breath/">back to arc</a>
    </div>
    
    <p class="text-sm text-zinc-400 mb-4">The first endpoint of Trivia Duel — /duel/start — defines how intention becomes structure. A simple request opens the door for matchmaking, concurrency, and the quiet choreography behind a duel.</p>
    

    <article class="prose prose-invert max-w-none">
        <h3>Designing the First API: <code>/duel/start</code></h3>
<p>Every system begins with a single request.<br>
For our Game Hub, that first one is humble but symbolic:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>POST /duel/start
</span></span></code></pre><p>It’s the handshake between a player’s curiosity and the system’s logic.<br>
And the funny thing about beginnings is — they look simple, but they set the tone for everything that follows.</p>
<hr>
<h4>Defining What “Start” Means</h4>
<p>When a player calls <code>/duel/start</code>, what are they <em>really</em> asking?</p>
<p>Not to “play right now,” but to <em>declare intention</em>:</p>
<blockquote>
<p>“Hey system, I’m ready. Pair me with someone.”</p>
</blockquote>
<p>That’s not a duel yet — it’s a <strong>challenge request</strong>.</p>
<p>We could easily jump straight into creating a duel record, but that would break scalability.<br>
Real systems need breathing room — time to match, to handle concurrency, to fail gracefully.<br>
So instead of forcing the duel into existence, we’ll queue that intention and let another component (the matchmaker) decide when the duel truly begins.</p>
<hr>
<h4>Step 1 — The Data Model</h4>
<p>Let’s start small — in Go, we define a <code>Challenge</code> struct.</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span><span style="color:#ff79c6">package</span> domain
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#ff79c6">import</span> <span style="color:#f1fa8c">&#34;time&#34;</span>
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#8be9fd;font-style:italic">type</span> Challenge <span style="color:#8be9fd;font-style:italic">struct</span> {
</span></span><span style="display:flex;"><span>    ID        <span style="color:#8be9fd">string</span>    <span style="color:#f1fa8c">`json:&#34;id&#34;`</span>
</span></span><span style="display:flex;"><span>    PlayerID  <span style="color:#8be9fd">string</span>    <span style="color:#f1fa8c">`json:&#34;player_id&#34;`</span>
</span></span><span style="display:flex;"><span>    Status    <span style="color:#8be9fd">string</span>    <span style="color:#f1fa8c">`json:&#34;status&#34;`</span>     <span style="color:#6272a4">// waiting, matched, cancelled
</span></span></span><span style="display:flex;"><span><span style="color:#6272a4"></span>    CreatedAt time.Time <span style="color:#f1fa8c">`json:&#34;created_at&#34;`</span>
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>Each challenge is like a small heartbeat — alive for a short time, waiting for its counterpart.</p>
<p>Later, we might add things like <code>SkillLevel</code>, <code>Region</code>, or <code>GameMode</code> to improve matchmaking, but for now, minimalism wins.</p>
<hr>
<h4>Step 2 — The Handler</h4>
<p>In Go, handlers are where ideas meet HTTP reality.<br>
Our first one looks like this:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span><span style="color:#ff79c6">package</span> handlers
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#ff79c6">import</span> (
</span></span><span style="display:flex;"><span>    <span style="color:#f1fa8c">&#34;encoding/json&#34;</span>
</span></span><span style="display:flex;"><span>    <span style="color:#f1fa8c">&#34;net/http&#34;</span>
</span></span><span style="display:flex;"><span>    <span style="color:#f1fa8c">&#34;time&#34;</span>
</span></span><span style="display:flex;"><span>    <span style="color:#f1fa8c">&#34;github.com/google/uuid&#34;</span>
</span></span><span style="display:flex;"><span>	<span style="color:#f1fa8c">&#34;github.com/wastingnotime/game-hub/domain&#34;</span>
</span></span><span style="display:flex;"><span>)
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#8be9fd;font-style:italic">func</span> <span style="color:#50fa7b">StartDuelHandler</span>(w http.ResponseWriter, r <span style="color:#ff79c6">*</span>http.Request) {
</span></span><span style="display:flex;"><span>    <span style="color:#8be9fd;font-style:italic">var</span> req <span style="color:#8be9fd;font-style:italic">struct</span> {
</span></span><span style="display:flex;"><span>        PlayerID <span style="color:#8be9fd">string</span> <span style="color:#f1fa8c">`json:&#34;player_id&#34;`</span>
</span></span><span style="display:flex;"><span>    }
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>    <span style="color:#ff79c6">if</span> err <span style="color:#ff79c6">:=</span> json.<span style="color:#50fa7b">NewDecoder</span>(r.Body).<span style="color:#50fa7b">Decode</span>(<span style="color:#ff79c6">&amp;</span>req); err <span style="color:#ff79c6">!=</span> <span style="color:#ff79c6">nil</span> {
</span></span><span style="display:flex;"><span>        http.<span style="color:#50fa7b">Error</span>(w, <span style="color:#f1fa8c">&#34;invalid request body&#34;</span>, http.StatusBadRequest)
</span></span><span style="display:flex;"><span>        <span style="color:#ff79c6">return</span>
</span></span><span style="display:flex;"><span>    }
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>    challenge <span style="color:#ff79c6">:=</span> domain.Challenge{
</span></span><span style="display:flex;"><span>        ID:        uuid.<span style="color:#50fa7b">New</span>().<span style="color:#50fa7b">String</span>(),
</span></span><span style="display:flex;"><span>        PlayerID:  req.PlayerID,
</span></span><span style="display:flex;"><span>        Status:    <span style="color:#f1fa8c">&#34;waiting&#34;</span>,
</span></span><span style="display:flex;"><span>        CreatedAt: time.<span style="color:#50fa7b">Now</span>().<span style="color:#50fa7b">UTC</span>(),
</span></span><span style="display:flex;"><span>    }
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>    <span style="color:#6272a4">// TODO: Save challenge (in-memory, Redis, or DB)
</span></span></span><span style="display:flex;"><span><span style="color:#6272a4"></span>    <span style="color:#6272a4">// For now, just return it
</span></span></span><span style="display:flex;"><span><span style="color:#6272a4"></span>    w.<span style="color:#50fa7b">Header</span>().<span style="color:#50fa7b">Set</span>(<span style="color:#f1fa8c">&#34;Content-Type&#34;</span>, <span style="color:#f1fa8c">&#34;application/json&#34;</span>)
</span></span><span style="display:flex;"><span>    json.<span style="color:#50fa7b">NewEncoder</span>(w).<span style="color:#50fa7b">Encode</span>(challenge)
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>No database yet, no queues, no fancy logic — just structure.<br>
You could call this the “paper prototype” of an API: something that looks real, but is light enough to move around without fear.</p>
<hr>
<h4>Step 3 — The Philosophy of Simple Starts</h4>
<p>Why so basic?<br>
Because complexity grows by itself — you never need to plant it.</p>
<p>At <em>WastingNoTime</em>, the rule is:</p>
<blockquote>
<p>Build something that runs,<br>
then build something that matters.</p>
</blockquote>
<p>The first build is for <em>you</em> — to visualize the flow.<br>
The second is for <em>the system</em> — to stand on its own.</p>
<p>So before touching Redis, DynamoDB, or even Docker, we’ll test this endpoint locally with a simple request:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>curl -X POST http://localhost:8080/duel/start <span style="color:#f1fa8c"></span></span></span><span style="display:flex;"><span><span style="color:#f1fa8c"></span>  -H <span style="color:#f1fa8c">&#34;Content-Type: application/json&#34;</span> <span style="color:#f1fa8c"></span></span></span><span style="display:flex;"><span><span style="color:#f1fa8c"></span>  -d <span style="color:#f1fa8c">&#39;{&#34;player_id&#34;: &#34;P001&#34;}&#39;</span>
</span></span></code></pre><p>Response:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>{
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;id&#34;</span>: <span style="color:#f1fa8c">&#34;df92ac8e-4c92-4bb2-932f-98e71c6e4db5&#34;</span>,
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;player_id&#34;</span>: <span style="color:#f1fa8c">&#34;P001&#34;</span>,
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;status&#34;</span>: <span style="color:#f1fa8c">&#34;waiting&#34;</span>,
</span></span><span style="display:flex;"><span>  <span style="color:#ff79c6">&#34;created_at&#34;</span>: <span style="color:#f1fa8c">&#34;2025-10-31T21:00:00Z&#34;</span>
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>That’s it.<br>
A first breath of life.</p>
<hr>
<h4>Step 4 — Looking Ahead</h4>
<p>Now we have our entry point.<br>
From here, we can:</p>
<ul>
<li>
<p>Persist this challenge in memory (for testing).</p>
</li>
<li>
<p>Create a simple <strong>matchmaker goroutine</strong> that checks for pairs every few seconds.</p>
</li>
<li>
<p>Generate a duel once two players are ready.</p>
</li>
</ul>
<p>Step by step, the <em>hub</em> will start to emerge — not from a blueprint, but from dialogue between code and curiosity.</p>
<hr>
<h4>Closing Thought</h4>
<p>Software isn’t born perfect — it grows like a story.<br>
And every story starts with a scene that seems small, until you look back and realize it was everything.</p>
<p>That’s our <code>/duel/start</code>.<br>
A humble endpoint, but the root of all motion.</p>
<hr>
<p><strong>Source for this episode:</strong><br>
Tag <strong>v0.1.0-e04-trivia-duel</strong><br>
<a href="https://github.com/wastingnotime/game-hub/tree/v0.1.0-e04-trivia-duel">https://github.com/wastingnotime/game-hub/tree/v0.1.0-e04-trivia-duel</a></p>

    </article>

    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">
        <a class="hover:underline" href="/sagas/game-hub/the-first-breath/how-a-duel-is-born/">← Ep 03 How a Duel Is Born</a>
        <a class="hover:underline" href="/sagas/game-hub/the-first-breath/building-the-matchmaker/">Ep 05 Building the Matchmaker: Where Waiting Meets Destiny →</a>
    </nav>


    <footer class="mt-10 text-xs text-zinc-500">
        © 2025 wastingnotime.org — built with Go
    </footer>
</div>
</body>
</html>


        """,
    'sagas/game-hub/the-first-breath/building-the-matchmaker': """

    
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Building the Matchmaker: Where Waiting Meets Destiny — Game Hub</title>
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>
    <style>
        html { font-kerning: normal; }

         
        .menu a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        .menu a:hover {
            color:#fff;
            text-decoration:underline;
        }
        .menu a.active {
            color:#fff;
            font-weight:500;
        }
        .menu a.active::after {
            content:"•";
            margin-left:0.4em;
            opacity:0.6;
            font-weight:400;
        }

         
        a {
            color:#a1a1aa;
            text-decoration:none;
            transition: color .15s ease;
        }
        a:hover {
            color:#fff;
            text-decoration:underline;
        }

         
        ul {
            list-style:none;
            padding-left:0;
            margin:0;
        }

         
        .intro:empty {
            display:none;
        }

         
        .space-y-1 > * + * { margin-top: .25rem; }
        .space-y-2 > * + * { margin-top: .5rem; }
        .space-y-3 > * + * { margin-top: .75rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }

        .breadcrumb {
            font-size:0.9rem;
            color:#888;
            margin-bottom:1.5rem;
        }
        .breadcrumb a {
            color:#aaa;
            text-decoration:none;
        }
        .breadcrumb a:hover {
            text-decoration:underline;
            color:#fff;
        }
        .breadcrumb .sep {
            margin:0 .4rem;
            color:#555;
        }

        .arc-name,
        .episode-title {
            color:#fff;
            font-weight:500;
            margin:0 0 1rem 0;
            font-size:1.1rem;
        }

        .topic-link {
            border-width:1px;
            border-color: rgb(39 39 42);
            border-style: solid;
            border-radius:.25rem;
            padding:.5rem .75rem;
            color: rgb(244 244 245);
            text-decoration:none;
            transition: color .15s ease, border-color .15s ease;
        }
        .topic-link:hover {
            border-color: rgba(255,255,255,.4);
            color:#fff;
            text-decoration:underline;
        }

          
          

         .prose {
             max-width: none;
             --wnt-text-100: rgb(244 244 245);
             --wnt-text-200: rgb(228 228 231);
             --wnt-text-300: rgb(212 212 216);
             --wnt-text-400: rgb(161 161 170);
             --wnt-border:   rgb(39 39 42);
         }

         
        .prose h2 {
            margin-top: 3rem;
            margin-bottom: 1rem;
            color: #fff;
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.6;
        }
        .prose h3 {
            margin-top: 2rem;
            margin-bottom: 0.75rem;
            color: var(--wnt-text-200);
            font-weight: 500;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .prose h3 strong { font-weight: 500; }

         
        .prose p {
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
            line-height: 1.7;
            color: var(--wnt-text-200);
        }
        .prose h2 + p,
        .prose h3 + p { margin-top: 0.75rem; }

         
        .prose blockquote {
            border-left: 2px solid rgb(63 63 70);
            padding-left: 1rem;
            margin: 1.75rem 0;
            color: var(--wnt-text-300);
            font-style: italic;
            line-height: 1.8;
        }
        .prose blockquote p { margin: 0; }
        .prose blockquote strong { color: #fff; font-weight: 500; }

         
        .prose ul { list-style: disc; }
        .prose ol { list-style: decimal; }
        .prose ul, .prose ol {
            margin: 1.25rem 0;
            padding-left: 1.25rem;
            color: var(--wnt-text-200);
        }
        .prose li + li { margin-top: 0.35rem; }
        .prose li > p { margin: 0.25rem 0; }

         
        .prose code {
            background: rgba(255,255,255,0.04);
            padding: 0.1rem 0.35rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            color: var(--wnt-text-100);
        }
        .prose pre {
            margin: 1.5rem 0;
            padding: 1rem;
            background: #0b0b0b;
            border: 1px solid var(--wnt-border);
            border-radius: 0.5rem;
            overflow: auto;
        }
        .prose pre code { background: transparent; padding: 0; border-radius: 0; }

         
        .prose a {
            color: var(--wnt-text-400);
            text-decoration: underline;
            text-decoration-thickness: .06em;
            text-underline-offset: 2px;
        }
        .prose a:hover { color: #fff; }

         
        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }
        .prose figure { margin: 1.75rem 0; }
        .prose figcaption {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--wnt-text-400);
            text-align: center;
        }
        .prose hr {
            border: 0;
            border-top: 1px solid var(--wnt-border);
            margin: 2rem 0;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            color: var(--wnt-text-200);
        }
        .prose thead th {
            text-align: left;
            font-weight: 600;
            color: #fff;
            border-bottom: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }
        .prose tbody td {
            border-top: 1px solid var(--wnt-border);
            padding: 0.5rem 0.75rem;
        }

         
        .prose :last-child { margin-bottom: 0 !important; }
    </style>
    
</head>
<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">
<div class="max-w-3xl mx-auto px-4 py-6">
    <header class="mb-6">
        <nav class="menu text-sm text-zinc-400">
            <a class="" href="/">HOME</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/studio/">STUDIO</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="active" href="/sagas/">SAGAS</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/library/">LIBRARY</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a class="" href="/about/">ABOUT</a>
            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>
            <a href="/feed.xml">RSS</a>
        </nav>

        
        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep 05] Building the Matchmaker: Where Waiting Meets Destiny — The First Breath / Game Hub</h1>
    </header>

    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">
    </p>

    
    <nav class="breadcrumb">
        <a href="/sagas/game-hub/">← Game Hub</a>
        <span class="sep">/</span>
        <a href="/sagas/game-hub/the-first-breath/">The First Breath</a>
    </nav>
    <h2 class="episode-title">Building the Matchmaker: Where Waiting Meets Destiny</h2>
    <div class="text-xs text-zinc-500 mb-3">
        2025-12-03 · <a class="hover:underline" href="/sagas/game-hub/the-first-breath/">back to arc</a>
    </div>
    
    <p class="text-sm text-zinc-400 mb-4">A quiet background loop becomes the first true heartbeat of the Game Hub, pairing waiting challengers into living duels and revealing the beauty of coordination, state, and synchronization.</p>
    

    <article class="prose prose-invert max-w-none">
        <h3>Building the Matchmaker: Where Waiting Meets Destiny</h3>
<p>Every world needs a force that connects its wandering souls.<br>
In our Game Hub, that force is the <strong>matchmaker</strong> — the quiet engine that watches, waits, and says,</p>
<blockquote>
<p>“You two. You’ll duel.”</p>
</blockquote>
<p>It’s not glamorous code. It doesn’t print shiny UI or speak to the player.<br>
But it gives shape to chaos — and that’s what makes it beautiful.</p>
<hr>
<h4>The Role of the Matchmaker</h4>
<p>From the previous episode, we know that every time a player hits:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>POST /duel/start
</span></span></code></pre><p>we create a <code>Challenge</code> and store it with a status of <code>&quot;waiting&quot;</code>.<br>
Now we need a background process that checks for pairs of waiting players and creates a <strong>duel</strong> when two are found.</p>
<p>Sounds simple, right?<br>
But even a tiny piece of coordination teaches us a lot about concurrency, state, and synchronization — three words that every backend developer eventually learns to respect.</p>
<hr>
<h4>Step 1 — A Minimal In-Memory World</h4>
<p>Let’s begin with something almost poetic: a small in-memory room where challenges wait.</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span><span style="color:#ff79c6">package</span> memory
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#ff79c6">import</span> <span style="color:#f1fa8c">&#34;github.com/wastingnotime/game-hub/domain&#34;</span>
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#8be9fd;font-style:italic">var</span> WaitingChallenges = <span style="color:#8be9fd;font-style:italic">make</span>([]domain.Challenge, <span style="color:#bd93f9">0</span>)
</span></span></code></pre><p>It’s fragile, temporary, and perfect for the moment — like a prototype carved in sand before we cast it in stone.</p>
<p>Later, we’ll move this to Redis or DynamoDB, but for now, this is where stories start.</p>
<hr>
<h4>Step 2 — The Matchmaker Loop</h4>
<p>Now, let’s write the heartbeat.<br>
A loop that wakes up every few seconds, looks at the waiting list, and pairs the first two lonely challengers it finds.</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span><span style="color:#ff79c6">package</span> services
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#ff79c6">import</span> (
</span></span><span style="display:flex;"><span>    <span style="color:#f1fa8c">&#34;fmt&#34;</span>
</span></span><span style="display:flex;"><span>    <span style="color:#f1fa8c">&#34;sync&#34;</span>
</span></span><span style="display:flex;"><span>    <span style="color:#f1fa8c">&#34;time&#34;</span>
</span></span><span style="display:flex;"><span>	<span style="color:#f1fa8c">&#34;github.com/wastingnotime/game-hub/domain&#34;</span>
</span></span><span style="display:flex;"><span>	<span style="color:#f1fa8c">&#34;github.com/wastingnotime/game-hub/memory&#34;</span>
</span></span><span style="display:flex;"><span>)
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#8be9fd;font-style:italic">var</span> mu sync.Mutex
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#8be9fd;font-style:italic">func</span> <span style="color:#50fa7b">StartMatchmaker</span>() {
</span></span><span style="display:flex;"><span>    <span style="color:#ff79c6">go</span> <span style="color:#8be9fd;font-style:italic">func</span>() {
</span></span><span style="display:flex;"><span>        <span style="color:#ff79c6">for</span> {
</span></span><span style="display:flex;"><span>            time.<span style="color:#50fa7b">Sleep</span>(<span style="color:#bd93f9">2</span> <span style="color:#ff79c6">*</span> time.Second) <span style="color:#6272a4">// small heartbeat
</span></span></span><span style="display:flex;"><span><span style="color:#6272a4"></span>            <span style="color:#50fa7b">matchPlayers</span>()
</span></span><span style="display:flex;"><span>        }
</span></span><span style="display:flex;"><span>    }()
</span></span><span style="display:flex;"><span>}
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#8be9fd;font-style:italic">func</span> <span style="color:#50fa7b">matchPlayers</span>() {
</span></span><span style="display:flex;"><span>    mu.<span style="color:#50fa7b">Lock</span>()
</span></span><span style="display:flex;"><span>    <span style="color:#ff79c6">defer</span> mu.<span style="color:#50fa7b">Unlock</span>()
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>    <span style="color:#ff79c6">for</span> <span style="color:#8be9fd;font-style:italic">len</span>(memory.WaitingChallenges) <span style="color:#ff79c6">&gt;=</span> <span style="color:#bd93f9">2</span> {
</span></span><span style="display:flex;"><span>        p1 <span style="color:#ff79c6">:=</span> memory.WaitingChallenges[<span style="color:#bd93f9">0</span>]
</span></span><span style="display:flex;"><span>        p2 <span style="color:#ff79c6">:=</span> memory.WaitingChallenges[<span style="color:#bd93f9">1</span>]
</span></span><span style="display:flex;"><span>        memory.WaitingChallenges = memory.WaitingChallenges[<span style="color:#bd93f9">2</span>:]
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>        duel <span style="color:#ff79c6">:=</span> domain.<span style="color:#50fa7b">NewDuel</span>(p1.PlayerID, p2.PlayerID)
</span></span><span style="display:flex;"><span>        fmt.<span style="color:#50fa7b">Printf</span>(<span style="color:#f1fa8c">&#34;✨ New duel started! %s vs %s → ID: %s
&#34;</span>, p1.PlayerID, p2.PlayerID, duel.ID)
</span></span><span style="display:flex;"><span>    }
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>Nothing fancy — just Go doing what Go does best: lightweight concurrency with almost no ceremony.<br>
Every few seconds, it looks around, finds a pair, and says, “Let’s go.”</p>
<p>You can feel the system breathing.</p>
<hr>
<h4>Step 3 — The Duel Entity</h4>
<p>Now we need to define what a <em>duel</em> actually is — the thing born from that matchmaker spark.</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span><span style="color:#ff79c6">package</span> domain
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#ff79c6">import</span> (
</span></span><span style="display:flex;"><span>    <span style="color:#f1fa8c">&#34;time&#34;</span>
</span></span><span style="display:flex;"><span>    <span style="color:#f1fa8c">&#34;github.com/google/uuid&#34;</span>
</span></span><span style="display:flex;"><span>)
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#8be9fd;font-style:italic">type</span> Duel <span style="color:#8be9fd;font-style:italic">struct</span> {
</span></span><span style="display:flex;"><span>    ID        <span style="color:#8be9fd">string</span>    <span style="color:#f1fa8c">`json:&#34;id&#34;`</span>
</span></span><span style="display:flex;"><span>    Players   []<span style="color:#8be9fd">string</span>  <span style="color:#f1fa8c">`json:&#34;players&#34;`</span>
</span></span><span style="display:flex;"><span>    State     <span style="color:#8be9fd">string</span>    <span style="color:#f1fa8c">`json:&#34;state&#34;`</span> <span style="color:#6272a4">// starting, active, finished
</span></span></span><span style="display:flex;"><span><span style="color:#6272a4"></span>    CreatedAt time.Time <span style="color:#f1fa8c">`json:&#34;created_at&#34;`</span>
</span></span><span style="display:flex;"><span>}
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#8be9fd;font-style:italic">func</span> <span style="color:#50fa7b">NewDuel</span>(p1, p2 <span style="color:#8be9fd">string</span>) Duel {
</span></span><span style="display:flex;"><span>    <span style="color:#ff79c6">return</span> Duel{
</span></span><span style="display:flex;"><span>        ID:        uuid.<span style="color:#50fa7b">New</span>().<span style="color:#50fa7b">String</span>(),
</span></span><span style="display:flex;"><span>        Players:   []<span style="color:#8be9fd">string</span>{p1, p2},
</span></span><span style="display:flex;"><span>        State:     <span style="color:#f1fa8c">&#34;starting&#34;</span>,
</span></span><span style="display:flex;"><span>        CreatedAt: time.<span style="color:#50fa7b">Now</span>().<span style="color:#50fa7b">UTC</span>(),
</span></span><span style="display:flex;"><span>    }
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>A duel is just a record of a connection — ephemeral yet real.<br>
Each one marks the moment two intentions found each other.</p>
<hr>
<h4>Step 4 — Plugging It Together</h4>
<p>In your <code>handlers.go</code>:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span><span style="color:#ff79c6">package</span> handlers
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#ff79c6">import</span> (
</span></span><span style="display:flex;"><span>	<span style="color:#f1fa8c">&#34;encoding/json&#34;</span>
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>	<span style="color:#f1fa8c">&#34;github.com/google/uuid&#34;</span>
</span></span><span style="display:flex;"><span>	<span style="color:#f1fa8c">&#34;github.com/wastingnotime/game-hub/domain&#34;</span>
</span></span><span style="display:flex;"><span>	<span style="color:#f1fa8c">&#34;github.com/wastingnotime/game-hub/memory&#34;</span>
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>	<span style="color:#f1fa8c">&#34;net/http&#34;</span>
</span></span><span style="display:flex;"><span>	<span style="color:#f1fa8c">&#34;time&#34;</span>
</span></span><span style="display:flex;"><span>)
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span><span style="color:#8be9fd;font-style:italic">func</span> <span style="color:#50fa7b">StartDuelHandler</span>(w http.ResponseWriter, r <span style="color:#ff79c6">*</span>http.Request) {
</span></span><span style="display:flex;"><span>	<span style="color:#8be9fd;font-style:italic">var</span> req <span style="color:#8be9fd;font-style:italic">struct</span> {
</span></span><span style="display:flex;"><span>		PlayerID <span style="color:#8be9fd">string</span> <span style="color:#f1fa8c">`json:&#34;player_id&#34;`</span>
</span></span><span style="display:flex;"><span>	}
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>	<span style="color:#ff79c6">if</span> err <span style="color:#ff79c6">:=</span> json.<span style="color:#50fa7b">NewDecoder</span>(r.Body).<span style="color:#50fa7b">Decode</span>(<span style="color:#ff79c6">&amp;</span>req); err <span style="color:#ff79c6">!=</span> <span style="color:#ff79c6">nil</span> {
</span></span><span style="display:flex;"><span>		http.<span style="color:#50fa7b">Error</span>(w, <span style="color:#f1fa8c">&#34;invalid request body&#34;</span>, http.StatusBadRequest)
</span></span><span style="display:flex;"><span>		<span style="color:#ff79c6">return</span>
</span></span><span style="display:flex;"><span>	}
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>	challenge <span style="color:#ff79c6">:=</span> domain.Challenge{
</span></span><span style="display:flex;"><span>		ID:        uuid.<span style="color:#50fa7b">New</span>().<span style="color:#50fa7b">String</span>(),
</span></span><span style="display:flex;"><span>		PlayerID:  req.PlayerID,
</span></span><span style="display:flex;"><span>		Status:    <span style="color:#f1fa8c">&#34;waiting&#34;</span>,
</span></span><span style="display:flex;"><span>		CreatedAt: time.<span style="color:#50fa7b">Now</span>().<span style="color:#50fa7b">UTC</span>(),
</span></span><span style="display:flex;"><span>	}
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>	memory.WaitingChallenges = <span style="color:#8be9fd;font-style:italic">append</span>(memory.WaitingChallenges, challenge)
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>	w.<span style="color:#50fa7b">Header</span>().<span style="color:#50fa7b">Set</span>(<span style="color:#f1fa8c">&#34;Content-Type&#34;</span>, <span style="color:#f1fa8c">&#34;application/json&#34;</span>)
</span></span><span style="display:flex;"><span>	json.<span style="color:#50fa7b">NewEncoder</span>(w).<span style="color:#50fa7b">Encode</span>(challenge)
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>In your <code>main.go</code>:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span><span style="color:#8be9fd;font-style:italic">func</span> <span style="color:#50fa7b">main</span>() {
</span></span><span style="display:flex;"><span>    fmt.<span style="color:#50fa7b">Println</span>(<span style="color:#f1fa8c">&#34;🕹️ Game Hub starting...&#34;</span>)
</span></span><span style="display:flex;"><span>    services.<span style="color:#50fa7b">StartMatchmaker</span>()
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>    <span style="color:#6272a4">//POST /duel/start
</span></span></span><span style="display:flex;"><span><span style="color:#6272a4"></span>    http.<span style="color:#50fa7b">HandleFunc</span>(<span style="color:#f1fa8c">&#34;/duel/start&#34;</span>, handlers.StartDuelHandler)
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>    s <span style="color:#ff79c6">:=</span> <span style="color:#ff79c6">&amp;</span>http.Server{
</span></span><span style="display:flex;"><span>        Addr: <span style="color:#f1fa8c">&#34;:8080&#34;</span>,
</span></span><span style="display:flex;"><span>    }
</span></span><span style="display:flex;"><span>
</span></span><span style="display:flex;"><span>    log.<span style="color:#50fa7b">Fatal</span>(s.<span style="color:#50fa7b">ListenAndServe</span>())
</span></span><span style="display:flex;"><span>}
</span></span></code></pre><p>Now run it.<br>
Then, from another terminal, call:</p>
<pre tabindex="0" style="color:#f8f8f2;background-color:#282a36;"><code><span style="display:flex;"><span>curl -X POST http://localhost:8080/duel/start -d <span style="color:#f1fa8c">&#39;{&#34;player_id&#34;:&#34;P001&#34;}&#39;</span> -H <span style="color:#f1fa8c">&#34;Content-Type: application/json&#34;</span>
</span></span><span style="display:flex;"><span>curl -X POST http://localhost:8080/duel/start -d <span style="color:#f1fa8c">&#39;{&#34;player_id&#34;:&#34;P002&#34;}&#39;</span> -H <span style="color:#f1fa8c">&#34;Content-Type: application/json&#34;</span>
</span></span></code></pre><p>And a few seconds later, in your logs:</p>
<pre><code>✨ New duel started! P001 vs P002 → ID: a82b0f32-7f83-4f8b-8f9c-33db76a08a0b
</code></pre>
<p>It’s alive.</p>
<hr>
<h4>Step 5 — The First Breath of the Hub</h4>
<p>This moment always feels special.<br>
There’s no frontend, no graphics, no noise — but under the surface, something <em>connected</em>.</p>
<p>It’s the invisible part of creation that makes everything else possible.<br>
From here, we can grow in many directions:</p>
<ul>
<li>
<p>Persist duels and challenges</p>
</li>
<li>
<p>Add timeouts and retries</p>
</li>
<li>
<p>Introduce AI opponents</p>
</li>
<li>
<p>Expand to WebSockets or event-driven communication</p>
</li>
</ul>
<p>But the essence remains: <strong>two requests met each other and created meaning</strong>.</p>
<hr>
<h4>Closing Thought</h4>
<p>Software is never born whole — it’s assembled from conversations between ideas.<br>
Here, our matchmaker is the quiet listener in that dialogue.<br>
It doesn’t decide who wins or loses — it just ensures the right people meet at the right time.</p>
<p>And that, in its own way, is a kind of art.</p>
<hr>
<p><strong>Source for this episode:</strong><br>
Tag <strong>v0.2.0-e05-trivia-duel</strong><br>
<a href="https://github.com/wastingnotime/game-hub/tree/v0.2.0-e05-trivia-duel">https://github.com/wastingnotime/game-hub/tree/v0.2.0-e05-trivia-duel</a></p>

    </article>

    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">
        <a class="hover:underline" href="/sagas/game-hub/the-first-breath/designing-the-first-api/">← Ep 04 Designing the First API — /duel/start</a>
        
    </nav>


    <footer class="mt-10 text-xs text-zinc-500">
        © 2025 wastingnotime.org — built with Go
    </footer>
</div>
</body>
</html>


        """,
}

def render_legacy_episode_page(permalink: str) -> str:
    key = permalink.strip("/")
    return LEGACY_EPISODE_HTML[key].removeprefix("\n").rstrip() + "\n\n"
