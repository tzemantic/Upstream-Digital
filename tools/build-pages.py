"""Generates the static sub pages of site/: services, case studies, privacy policy, sitemap.xml and robots.txt.

Usage (from the repo root):  python3 tools/build-pages.py site

Edit page content in the SERVICES, CASES, FAQ and PRIVACY data below, then re-run.
The homepage (site/index.html) is edited by hand; keep its header and footer in sync with head() and FOOT here.
"""
import json, os, re, sys, html

SITE = sys.argv[1]
DOMAIN = "https://www.getupstreamdigital.com"
OG_IMG = DOMAIN + "/assets/about.webp"
TODAY = "2026-11-13"
ASSET_V = "20261115d"  # bump when styles.css or main.js change so browsers fetch fresh copies

def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- content
CASES = [
 dict(
  slug="phibro-renewoil", name="Phibro RenewOil", logo="t-phibro.webp", url="https://www.phibrorenewoil.com/", host="phibrorenewoil.com",
  sector="Used cooking oil collection", where="Connecticut, New York & New Jersey",
  services=["Meta Ads","Google Ads","Web Design & Development","SEO / AEO"],
  title="Phibro RenewOil: Paid Ads, Web & SEO Case Study",
  desc="How we helped Phibro RenewOil go from relying on paid ads to bringing in most of its new business online, with ads, a new website and SEO.",
  h1="How Phibro RenewOil gets most of its new business online",
  intro="When Phibro RenewOil came to us in 2023, almost all of their new customers came from paid ads. Now their ads, website and Google search all bring in leads, and most of their new business comes in online.",
  card_stat=("36%","lead conversion rate on one of their top campaigns"),
  card_lede="Ads, a new website and local SEO that now bring in most of their new business.",
  stats=[("3+ yrs","Working together"),("36%","Lead conversion rate on one of their top campaigns"),("110+","Town pages across Connecticut and New York")],
  client="Phibro RenewOil picks up used cooking oil from restaurants, commercial kitchens, food trucks, hotels and other food businesses across Connecticut and parts of New York and New Jersey. They provide secure containers, come by on a regular schedule, and pay for every gallon they collect. The oil gets recycled into things like biodiesel.",
  challenge=["Most restaurant owners have no idea their used cooking oil is worth anything, so the offer has to be explained before anyone’s interested.",
  "When we started, nearly all of Phibro’s new customers came from paid ads, and they barely showed up on Google. If the ad budget went down, so did new business."],
  did=[("Facebook and Instagram ads","We built Meta campaigns around the simplest selling point: you get paid for your used oil. We kept testing new images and videos and put more money behind whatever worked. We also ran ads in Spanish to reach Spanish-speaking restaurant owners."),
       ("Google Ads","We ran Google Ads alongside Meta to catch restaurants already searching for oil pickup. As Phibro started showing up on Google on its own, we moved the ad budget over to Meta."),
       ("Website","We redesigned the site around the businesses Phibro works with, from restaurants and food trucks to hotels and towns, and made the payment and pickup details easy to find. Getting in touch takes one short form."),
       ("Local SEO and AEO","We built more than 110 pages for the towns Phibro serves across Connecticut and New York, keep their Google Business Profile up to date, and check how things are going every month. Leads now come in from ads, the contact form, phone calls and their Google Business Profile.")],
  results=["Today, Phibro’s ads, website and Google search all bring in leads, and those leads turn into new customers month after month. Most of their new business now comes in online.",
  "And because more people find them through search, new business doesn’t hinge on the ad budget anymore."],
  quote=("The results have been outstanding—the ads they crafted are engaging and effective, resulting in a significant increase in traffic and leads.","Robert Kirk","Chief Operating Officer, Phibro RenewOil"),
 ),
 dict(
  slug="spade-security", name="Spade Security", logo="t-spade.webp", url="https://www.spade-security.com/", host="spade-security.com",
  sector="Turnstiles and access control", where="Installations across the US",
  services=["Google Ads","Web Design & Development","SEO / AEO"],
  title="Spade Security: 96% Lower Cost per Lead",
  desc="How we cut Spade Security’s cost per qualified lead by 96% and their ad spend by 25% with better Google Ads, a new website and SEO.",
  h1="How Spade Security cut its cost per qualified lead by 96%",
  intro="Spade Security came to us with a slow website and an agency that was spending a lot on ads that weren’t bringing in the right leads. We rebuilt their Google Ads, built them a fast new website and started working on their SEO. Within two months, their cost per qualified lead dropped 96%, and they’re spending 25% less on ads.",
  card_stat=("96%","lower cost per qualified lead after switching to us"),
  card_lede="They spend less on ads now and get far better leads.",
  stats=[("2+ yrs","Working together"),("96%","Lower cost per qualified lead"),("25%","Less spent on ads")],
  client="Spade Security sells and installs turnstiles, access control, vehicle access systems, bollards, guard shacks and security cameras. They’ve been in the business for more than ten years and work with companies, government buildings, colleges, entertainment venues, factories and warehouses across the US, Canada, Mexico and the UK.",
  challenge=["They were paying far too much for every lead. Their previous agency was spending their budget, but the leads weren’t the right ones. The team had started to think their website was just too new to do well on Google.",
  "Their website was also loading very slowly. Visitors were leaving before the page finished loading, so even the right clicks often didn’t turn into quote requests.",
  "Turnstiles are a big purchase and there aren’t that many buyers, so every wasted click costs real money."],
  did=[("Google Ads","We rebuilt the account so their budget goes to people who are actually shopping for turnstiles and access control, and cut the spending that wasn’t bringing in real leads. Within two months, their cost per qualified lead was down 96%, and the new campaigns had brought in more qualified leads than their previous agency did in the entire year before."),
       ("A fast, SEO-ready website","We designed a new website that loads quickly and is built for search from the ground up, so visitors stay long enough to look around and Google can find every page. It showcases all of their products and services, with a page for each type of turnstile (biometric, optical, full height and waist height), installation, and their other security products. We also added sections for the industries they work in, a simple four-step process, and easy ways to ask for a free quote."),
       ("Real projects","We added a projects section that shows installs they’ve done for clients like USPS, Target, Weber State University and the San Diego Hall of Justice."),
       ("SEO and AEO","We started with a full SEO audit, rewrote the turnstile pages so they’re easier to find on Google, and keep working on their SEO and AEO so Spade shows up when buyers search or ask an AI assistant.")],
  results=["Within two months of switching to us, Spade’s cost per qualified lead dropped 96%, and we’d brought in more qualified leads than their previous agency did all of the year before. Their ad spend went down 25%. Put simply, they’re spending less and getting a lot more of the right leads.",
  "Their new website loads quickly, keeps visitors on the site, and holds its own next to their biggest competitors."],
  quote=("Since partnering with Upstream Digital, we’ve seen a 96% decrease in cost per lead, which has significantly improved our visibility and lead generation.","Edward Fasone","President, Spade Security"),
 ),
 dict(
  slug="olson-floor-supply", name="Olson Floor Supply", logo="t-olson.webp", url="https://www.olsonfloors.com/", host="olsonfloors.com",
  sector="Hardwood flooring, supplies and Benjamin Moore paint", where="New York City, Long Island & Westchester",
  services=["Web Design & Development","SEO"],
  title="Olson Floor Supply: Website & SEO Case Study",
  desc="How we built Olson Floor Supply a new website from scratch, plus 32 local pages to help customers across NYC, Long Island and Westchester find them.",
  h1="Building Olson Floor Supply a new website from scratch",
  intro="Olson Floor Supply has been serving contractors and homeowners for more than 20 years. We built their website from the ground up, product by product, and we’ve kept working on their SEO ever since. That’s more than two years now.",
  card_stat=("32","local pages across New York City, Long Island and Westchester"),
  card_lede="A new website, built from scratch for a family business with decades of loyal customers.",
  stats=[("2+ yrs","Working together"),("32","Local pages"),("8","Areas covered"),("4","Product lines, each with its own catalog")],
  client="Olson Floor Supply is a family-owned business that sells hardwood flooring, supplies, tools, machines and Benjamin Moore paint. Contractors, developers and homeowners across New York City, Long Island, Westchester and nearby Connecticut have been buying from them for more than 20 years.",
  challenge=["Olson’s business was built on word of mouth and customers who keep coming back. They needed a website that showed everything they sell, made it easy to send in orders ahead of pickup, and helped new customers in the area find them on Google."],
  did=[("Built from scratch","We went through every product detail with the owner, so the site is genuinely useful to customers. Everything is organized into flooring, Benjamin Moore paint, supplies and machines."),
       ("Built around how people buy","There are sections for contractors, developers and homeowners, a list of authorized dealers, customer reviews, and a spot where the team posts updates like the next machine service pickup date. A simple form lets customers send in orders ahead of time so they’re ready when they arrive."),
       ("Local SEO","We created 32 local pages, one for each product line in Brooklyn, Queens, Manhattan, the Bronx, Staten Island, Nassau County, Suffolk County and Westchester County."),
       ("Ongoing SEO","We keep working on Olson’s Google rankings so more people can find the store.")],
  results=["Olson now has a website that shows everything they carry, plus local pages for all eight areas they serve. In the owner’s words, the finished site exceeded his expectations."],
  quote=("They took the time to listen to my ideas and consistently delivered updates and improvements that matched exactly what I had in mind.","Kenny Olson","Owner, Olson Floor Supply"),
 ),
 dict(
  slug="italian-consulate-connecticut", name="Honorary Consulate of Italy in Connecticut", logo="t-consulate.webp", url="https://www.italianconsulatect.com/", host="italianconsulatect.com",
  sector="Consular services", where="Hartford, Connecticut",
  services=["Web Design & Development","Local SEO"],
  title="Italian Consulate in CT: #1 on Google",
  desc="How we built the Honorary Consulate of Italy in Connecticut a clear new website and helped it reach #1 on Google with more than 100 Google reviews.",
  h1="How the Honorary Consulate of Italy in Connecticut got to #1 on Google",
  intro="The consulate needed a website that explained its services clearly, and an office people could actually find. We built the site and helped it get to #1 on Google, with more than 100 Google reviews.",
  card_stat=("#1","on Google, with more than 100 Google reviews"),
  card_lede="A clear new website, #1 on Google, and more than 100 Google reviews.",
  stats=[("3+ yrs","Working together"),("#1","On Google"),("100+","Google reviews")],
  client="The Honorary Consulate of Italy in Hartford helps Italian citizens and residents across Connecticut with passports, citizenship, notary services and the Italian tax ID code. Visits are by appointment only.",
  challenge=["Consular services come with a lot of requirements, and people often aren’t sure which office handles what. The consulate needed one clear place that explained each service and how to book, and it needed to show up when people searched for it."],
  did=[("New website","We designed and built a new website with its own page for passports, citizenship, notary services and the Italian tax ID code. Each page lays out what you need and how to book."),
       ("Clear next steps","Every service page explains how appointments work, and the contact page has a simple form, phone numbers and directions."),
       ("Easy to keep up to date","A news section makes it easy to post updates like voting notices and citizenship guidance."),
       ("Google Business Profile and local SEO","We improved the consulate’s Google Business Profile and helped the office keep the reviews coming, so it’s the first result when people in Connecticut search for it.")],
  results=["The consulate is now #1 on Google and has more than 100 Google reviews. People can find the right service, see what they need and book an appointment without having to call first."],
  quote=("From the beginning, they focused on understanding our needs and the purpose of the website.","Barbara Zichichi","Honorary Consulate of Italy in Connecticut"),
 ),
]

FAQ = {
 'phibro-renewoil': [
  ("What did Upstream Digital do for Phibro RenewOil?", "We’ve run their Meta and Google ads, redesigned their website, built more than 110 town pages across Connecticut and New York, and handle their local SEO and AEO."),
  ("How did Phibro RenewOil start getting leads consistently?", "By getting a few things working together: ads to reach people now, a website that makes it easy to get in touch, and local SEO so restaurants find Phibro when they search. Most of their new business now comes in online.")],
 'spade-security': [
  ("What did Upstream Digital do for Spade Security?", "We rebuilt their Google Ads, replaced their slow website with a fast, SEO-ready one that has a page for each turnstile and security product, ran an SEO audit, and keep working on their SEO and AEO."),
  ("How did Spade Security lower its cost per lead by 96%?", "We stopped paying for clicks that weren’t going anywhere and put the budget behind people actually looking to buy. Within two months, their cost per qualified lead was down 96%, and they had more qualified leads than their previous agency brought in the whole year before. Then we sent that traffic to a fast, clear website that keeps visitors around and makes it easy to ask for a quote.")],
 'olson-floor-supply': [
  ("What did Upstream Digital build for Olson Floor Supply?", "A new website built from scratch, with catalogs for flooring, Benjamin Moore paint, supplies and machines, plus 32 local pages and ongoing SEO."),
  ("Which areas do Olson Floor Supply’s local pages cover?", "Brooklyn, Queens, Manhattan, the Bronx, Staten Island, Nassau County, Suffolk County and Westchester County. Each area has a page for each product line.")],
 'italian-consulate-connecticut': [
  ("What did Upstream Digital do for the Honorary Consulate of Italy in Connecticut?", "We designed and built their website, with its own page for passports, citizenship, notary services and the Italian tax ID code, and improved their Google Business Profile."),
  ("How did the consulate get to #1 on Google?", "A clear website that explains each service, a well-kept Google Business Profile, and a steady flow of Google reviews. They now have more than 100.")],
}

# ---------------------------------------------------------------- shared chrome
def head(title, desc, path, og_type="website", schema=()):
    url = DOMAIN + path
    ld = "\n".join('<script type="application/ld+json">\n%s\n</script>' % json.dumps(s, ensure_ascii=False) for s in schema)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
/* Consent Mode v2 defaults: everything optional is denied until the visitor chooses. Load GTM/GA after this. */
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}
gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',functionality_storage:'denied',personalization_storage:'denied',security_storage:'granted',wait_for_update:500}});
try{{var c=JSON.parse(localStorage.getItem('ud_consent_v1'));if(c){{var g=function(v){{return v?'granted':'denied'}};gtag('consent','update',{{functionality_storage:g(c.functional),personalization_storage:g(c.functional),analytics_storage:g(c.analytics),ad_storage:g(c.marketing),ad_user_data:g(c.marketing),ad_personalization:g(c.marketing)}})}}}}catch(e){{}}
</script>
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#070D1C">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Upstream Digital">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMG}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400..800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css?v={ASSET_V}">
{ld}
</head>
<body class="sub">
<a class="skip" href="#main">Skip to content</a>

<header class="bar">
  <div class="wrap">
    <div class="bar-inner">
      <a class="logo" href="/" aria-label="Upstream Digital home"><img src="/assets/logo-white.webp" alt="Upstream Digital" width="600" height="88"></a>
      <nav class="menu" id="menu" aria-label="Main">
        <a href="/#about">About</a>
        <a href="/services/"{' aria-current="page"' if path.startswith('/services/') else ''}>Services</a>
        <a href="/case-studies/"{' aria-current="page"' if path.startswith('/case-studies/') else ''}>Case Studies</a>
        <a href="/#testimonials">Testimonials</a>
        <a href="/#contact">Contact Us</a>
        <a class="btn btn-solid" href="/#contact">Get Started</a>
      </nav>
      <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><i></i><i></i><i></i></button>
    </div>
  </div>
</header>

<main id="main">
'''

FOOT = '''
</main>

<footer class="foot">
  <div class="wrap">
    <a class="foot-cta" href="/#contact"><span class="foot-cta-text">Get Upstream.</span><span class="foot-cta-go" aria-hidden="true">→</span><span class="visually-hidden"> Contact us</span></a>
    <div class="foot-grid">
      <div><img src="/assets/logo-white.webp" alt="Upstream Digital" width="600" height="88" loading="lazy"></div>
      <nav aria-label="Services">
        <h2>Services</h2>
        <ul>
          <li><a href="/services/paid-advertising/">Paid Advertising</a></li>
          <li><a href="/services/seo-aeo/">SEO &amp; AEO</a></li>
          <li><a href="/services/website-design-development/">Website Design &amp; Development</a></li>
          <li><a href="/services/content-creation/">Content Creation</a></li>
          <li><a href="/services/digital-marketing-consulting/">Digital Marketing Consulting</a></li>
        </ul>
      </nav>
      <nav aria-label="Quick links">
        <h2>Quick Links</h2>
        <ul>
          <li><a href="/#about">About</a></li>
          <li><a href="/services/">Services</a></li>
          <li><a href="/case-studies/">Case Studies</a></li>
          <li><a href="/#testimonials">Testimonials</a></li>
          <li><a href="/#contact">Contact Us</a></li>
        </ul>
      </nav>
      <div>
        <h2>Contact</h2>
        <address>
          <a href="mailto:info@getupstreamdigital.com">info@getupstreamdigital.com</a>
          <a href="tel:+18604506983">+1 (860) 450-6983</a>
          <span>Greenwich, CT 06830</span>
        </address>
      </div>
    </div>
    <div class="foot-base">
      <a href="/privacy-policy/">Privacy Policy</a>
      <span>© 2026 by Upstream Digital LLC</span>
    </div>
  </div>
</footer>

<script src="/assets/main.js?v={ASSET_V}" defer></script>
</body>
</html>
'''
FOOT = FOOT.replace("{ASSET_V}", ASSET_V)

ORG = {"@type": "Organization", "name": "Upstream Digital", "url": DOMAIN + "/", "logo": DOMAIN + "/assets/logo-white.webp"}

def stat_html(v):
    # wrap %, +, → in <i> for the accent color
    return re.sub(r'(%|\+|→)', r'<i>\1</i>', esc(v)).replace('&gt;', '>')

def card(c, level="h3"):
    v, label = c["card_stat"]
    return f'''      <article class="work-card">
        <img src="/assets/{c["logo"]}" alt="" width="320" height="320" loading="lazy">
        <p class="work-sector">{esc(c["sector"])}</p>
        <{level}><a href="/case-studies/{c["slug"]}/">{esc(c["name"])}</a></{level}>
        <p class="work-lede">{esc(c["card_lede"])}</p>
        <p class="work-stat"><b>{stat_html(v)}</b><span>{esc(label)}</span></p>
        <span class="work-more" aria-hidden="true">Read the case study <span>→</span></span>
      </article>'''

def cards(level="h3", only=None):
    return "\n".join(card(c, level) for c in CASES if not only or c["slug"] in only)

CTA = '''
<section class="band cta-band">
  <div class="wrap cta-inner">
    <div>
      <h2 class="title">Want results like these?</h2>
      <p>Start with a free, no-obligation call. We’ll look at what you’re doing now and tell you honestly where we see room to grow.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-solid" href="/#contact">Get Started</a>
      <a class="btn btn-ghost" href="tel:+18604506983">Call +1 (860) 450-6983</a>
    </div>
  </div>
</section>
'''

# ---------------------------------------------------------------- case pages
def case_page(c):
    path = f"/case-studies/{c['slug']}/"
    schema = [
      {"@context": "https://schema.org", "@type": "Article", "headline": c["h1"], "description": c["desc"],
       "image": OG_IMG, "url": DOMAIN + path, "mainEntityOfPage": DOMAIN + path,
       "datePublished": TODAY, "dateModified": TODAY, "author": ORG, "publisher": ORG,
       "about": {"@type": "Organization", "name": c["name"], "url": c["url"]}},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Case Studies", "item": DOMAIN + "/case-studies/"},
        {"@type": "ListItem", "position": 3, "name": c["name"], "item": DOMAIN + path}]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[c["slug"]]]},
    ]
    faq = "\n".join(f'          <details class="faq-item"><summary><h3>{esc(q)}</h3></summary><p>{esc(a)}</p></details>' for q, a in FAQ[c["slug"]])
    tags = "".join(f"<li>{esc(t)}</li>" for t in c["services"])
    stats = "\n".join(f'        <li><b>{stat_html(v)}</b><span>{esc(l)}</span></li>' for v, l in c["stats"])
    did = "\n".join(f'          <h3>{esc(h)}</h3>\n          <p>{esc(p)}</p>' for h, p in c["did"])
    chal = "\n".join(f"          <p>{esc(p)}</p>" for p in c["challenge"])
    res = "\n".join(f"          <p>{esc(p)}</p>" for p in c["results"])
    q, who, role = c["quote"]
    others = [o["slug"] for o in CASES if o["slug"] != c["slug"]]
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol><li><a href="/">Home</a></li><li><a href="/case-studies/">Case Studies</a></li><li><span aria-current="page">{esc(c["name"])}</span></li></ol>
    </nav>
    <p class="kicker">Case study</p>
    <h1 class="title">{esc(c["h1"])}</h1>
    <p class="page-intro">{esc(c["intro"])}</p>
    <div class="cs-client">
      <img src="/assets/{c["logo"]}" alt="{esc(c["name"])} logo" width="320" height="320">
      <dl>
        <div><dt>Client</dt><dd>{esc(c["name"])}</dd></div>
        <div><dt>Industry</dt><dd>{esc(c["sector"])}</dd></div>
        <div><dt>Location</dt><dd>{esc(c["where"])}</dd></div>
        <div><dt>Website</dt><dd><a href="{c["url"]}" target="_blank" rel="noopener">{esc(c["host"])}<span aria-hidden="true">&nbsp;↗</span></a></dd></div>
      </dl>
    </div>
    <ul class="tags tags-dark" aria-label="Services">{tags}</ul>
  </div>
</section>

<section class="band light cs-main">
  <div class="wrap">
    <h2 class="visually-hidden">Results at a glance</h2>
    <ul class="case-stats cs-stats">
{stats}
    </ul>
    <div class="cs-grid">
      <div class="cs-text">
        <section aria-labelledby="client">
          <h2 id="client">The client</h2>
          <p>{esc(c["client"])}</p>
        </section>
        <section aria-labelledby="challenge">
          <h2 id="challenge">The challenge</h2>
{chal}
        </section>
        <section aria-labelledby="approach">
          <h2 id="approach">What we did</h2>
{did}
        </section>
        <section aria-labelledby="results">
          <h2 id="results">The results</h2>
{res}
        </section>
        <section aria-labelledby="faq" class="cs-faq">
          <h2 id="faq">Questions about this project</h2>
{faq}
        </section>
      </div>
      <aside class="cs-aside">
        <figure class="cs-quote">
          <blockquote><p>“{esc(q)}”</p></blockquote>
          <figcaption><strong>{esc(who)}</strong>{esc(role)}</figcaption>
        </figure>
        <a class="btn btn-solid" href="/#contact">Let’s talk about your business</a>
      </aside>
    </div>
  </div>
</section>

<section class="band more-work">
  <div class="wrap">
    <div class="work-head-row">
      <h2 class="title">More case studies</h2>
      <a class="text-link" href="/case-studies/">See all case studies <span aria-hidden="true">→</span></a>
    </div>
    <div class="work-grid work-grid-3">
{cards("h3", others)}
    </div>
  </div>
</section>
{CTA}'''
    return head(f'{c["title"]} | Upstream Digital', c["desc"], path, "article", schema) + body + FOOT

def hub_page():
    path = "/case-studies/"
    title = "Case Studies: Digital Marketing Results | Upstream Digital"
    desc = "See how Upstream Digital has helped real clients grow with paid ads, SEO and AEO, and new websites: where they started, what we did, and how it turned out."
    schema = [
      {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Case Studies", "description": desc, "url": DOMAIN + path,
       "isPartOf": {"@type": "WebSite", "name": "Upstream Digital", "url": DOMAIN + "/"},
       "mainEntity": {"@type": "ItemList", "itemListElement": [
          {"@type": "ListItem", "position": i + 1, "url": f"{DOMAIN}/case-studies/{c['slug']}/", "name": c["h1"]} for i, c in enumerate(CASES)]}},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Case Studies", "item": DOMAIN + path}]},
    ]
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol><li><a href="/">Home</a></li><li><span aria-current="page">Case Studies</span></li></ol>
    </nav>
    <p class="kicker">Case studies</p>
    <h1 class="title">Real clients, real results</h1>
    <p class="page-intro">Here’s how we’ve helped a few of our clients grow with ads, SEO and AEO, and new websites: where they started, what we did, and how it turned out.</p>
  </div>
</section>

<section class="band more-work hub-work">
  <div class="wrap">
    <h2 class="visually-hidden">All case studies</h2>
    <div class="work-grid">
{cards("h3")}
    </div>
  </div>
</section>
{CTA}'''
    return head(title, desc, path, "website", schema) + body + FOOT


# ---------------------------------------------------------------- services
SERVICES = [
 dict(slug="paid-advertising", outcomes=['More qualified leads, not just more clicks', 'Your ad budget goes to what’s actually working', 'You always know what each lead costs'], proof=('Spade Security cut its cost per qualified lead by 96% after switching to us.', '/case-studies/spade-security/'), name="Paid Advertising", sub="Meta, Google, LinkedIn",
  title="Meta, Google & LinkedIn Ads Management",
  desc="Paid advertising on Meta, Google and LinkedIn from Upstream Digital in Greenwich, CT. Campaigns built to bring in qualified leads and make your ad spend work harder.",
  h1="Paid advertising on Meta, Google and LinkedIn",
  intro="We build and manage ad campaigns that put your business in front of the right people. The focus is simple: generate qualified leads and make your ad spend work harder.",
  card="Campaigns on Meta, Google and LinkedIn built to bring in qualified leads.",
  included=[("Strategy that fits your goals","We start with what you’re trying to achieve and your budget, then pick the platforms where your customers actually are."),
            ("Targeting and keywords","Audience targeting on Meta and LinkedIn, and keyword research on Google, so your ads reach people likely to become customers."),
            ("Ad creative","Image, video and copy built around your clearest offer, tested and refreshed so ads don’t go stale."),
            ("Lead forms and landing pages","Simple ways for people to get in touch, whether that’s an instant form, a call or a landing page."),
            ("Conversion tracking","Tracking set up so you know which ads bring in leads, not just clicks."),
            ("Ongoing optimization","We watch performance closely and move budget to what’s working, month after month.")],
  approach=["Ads aren’t something we launch and walk away from. We stay involved, monitor performance closely, and keep making improvements based on real data.",
            "We also only recommend the platforms that make sense for you. Sometimes that’s Meta and Google together; sometimes it’s just one."],
  cases=["phibro-renewoil","spade-security"],
  faq=[("Which ad platforms do you manage?","Meta (Facebook and Instagram), Google and LinkedIn."),
       ("Do I need to advertise on every platform?","No. We recommend the platforms where your customers are and that fit your budget, and focus spend there."),
       ("How do you measure whether ads are working?","By the leads they bring in and what each qualified lead costs, not just clicks or impressions. We set up conversion tracking so those numbers are clear."),
       ("How much should I budget for ads?","It depends on your business and your goals. Monthly ad budgets can be anywhere from $500 to several thousand dollars, and we’ll tailor the campaigns to fit."),
       ("How is ad spend billed?","Google, Meta and other ad platforms charge your own payment method directly. You pay us separately for our services, with one invoice at the end of each month. Your reports show exactly what was spent. The platforms can spend slightly more or less than the monthly budget we set, because ad prices are decided in live auctions."),
       ("Who owns my ad accounts?","You do. We may set up your ad accounts for you, but they belong to you and stay with you if you ever leave.")]),
 dict(slug="seo-aeo", outcomes=['Customers find you when they search Google or ask AI', 'More calls and visits from people searching nearby', 'A steady flow of leads that doesn’t depend on ad spend'], proof=('The Honorary Consulate of Italy in Connecticut ranks #1 on Google, with more than 100 Google reviews.', '/case-studies/italian-consulate-connecticut/'), name="SEO & AEO", sub="Search engine and answer engine optimization",
  title="SEO & AEO Services in Greenwich, CT",
  desc="SEO and AEO from Upstream Digital: help your business rank higher on Google and show up in answers from AI assistants, with local SEO and content strategy.",
  h1="Search engine optimization (SEO) and answer engine optimization (AEO)",
  intro="We help your website rank higher on Google so people can actually find your business. From technical improvements to content strategy, we focus on long term growth in search, including the answers people now get from AI assistants.",
  card="Rank higher on Google and show up in answers from AI assistants.",
  included=[("SEO audit","A full review of your site’s technical health, content and local presence, so we know where the opportunities are."),
            ("Keyword and content strategy","We find what your customers search for and plan pages and content around it."),
            ("Service and location pages","Pages for each service and area you cover, so you show up for local searches across your market."),
            ("Google Business Profile","Optimizing your profile and helping you build a steady stream of reviews."),
            ("AEO","Clear, well-organized content that helps AI assistants and Google’s AI Overviews understand and recommend your business."),
            ("Monthly tracking","Progress tracked every month in Google Search Console, with clear updates.")],
  approach=["SEO builds over time. We focus on steady, long term growth rather than quick tricks, and keep you updated on what we’re doing and why.",
            "AEO builds on the same foundations. When your content clearly answers the questions customers ask, it’s easier for both search engines and AI assistants to recommend you."],
  cases=["phibro-renewoil","italian-consulate-connecticut","olson-floor-supply"],
  faq=[("What is AEO?","AEO, or answer engine optimization, helps your business show up in answers from AI assistants and search features like Google’s AI Overviews, not just in the regular list of search results. It builds on good SEO: clear, well-structured content that answers the questions your customers ask."),
       ("How long does SEO take?","It depends on your market and where your site is starting from. SEO usually builds steadily over months, which is why we track progress every month and keep you updated."),
       ("Do you do local SEO?","Yes. We build service and location pages, optimize your Google Business Profile, and help you build reviews so you show up when people search nearby.")]),
 dict(slug="website-design-development", outcomes=['More visitors become calls, form fills and customers', 'A professional first impression that builds trust', 'A site that’s ready to rank and easy to grow'], proof=('Olson Floor Supply got a new website built from scratch, with 32 local pages to help customers find them.', '/case-studies/olson-floor-supply/'), name="Website Design & Development", sub="",
  title="Website Design & Development",
  desc="Website design and development from Upstream Digital: fast, easy to navigate websites built to turn visitors into customers, with SEO built in from the start.",
  h1="Website design and development",
  intro="Your website should do more than look good. We design and build websites that are fast, easy to navigate, and built to turn visitors into customers.",
  card="Fast, easy to navigate websites built to turn visitors into customers.",
  included=[("Design that fits your business","A custom design that reflects who you are and what sets you apart."),
            ("Fast and mobile-friendly","Sites that load quickly and work well on every screen size."),
            ("Built to convert","Clear structure, clear calls to action and simple forms that make it easy to get in touch."),
            ("SEO from the start","Built the way search engines like, with clear pages, titles and descriptions, so the site is ready to rank."),
            ("Forms and tracking","Contact forms and analytics set up so you can see where your leads come from."),
            ("Support after launch","We stay hands-on after launch with updates and improvements.")],
  approach=["We start by understanding your business and your customers, then work closely with you through every detail. You’ll always know where things stand.",
            "Whether you need a site built from scratch or a redesign of the one you have, the goal is the same: a website that brings in business."],
  cases=["olson-floor-supply","italian-consulate-connecticut","spade-security"],
  faq=[("Do you build new websites or redesign existing ones?","Both. We’ve built sites from scratch and redesigned existing ones, depending on what your business needs."),
       ("Will my new website be set up for search?","Yes. Every site we build is set up to rank, with clear page structure, page titles and descriptions, and the behind-the-scenes code search engines read."),
       ("Who owns my website?","You do. Everything we build for you is yours, and it stays with you if you ever leave."),
       ("Do you help after the site launches?","Yes. We stay hands-on after launch with updates, improvements and ongoing support.")]),
 dict(slug="content-creation", outcomes=['Ads people notice and click', 'Pages that answer customer questions and show up in search', 'A consistent voice that builds trust in your brand'], proof=('Phibro RenewOil’s ads, website and local SEO now bring in most of their new business.', '/case-studies/phibro-renewoil/'), name="Content Creation", sub="",
  title="Content Creation for Ads, SEO & Your Website",
  desc="Content creation from Upstream Digital: ad creative, website copy and SEO content that builds trust, attracts the right audience and helps your brand stand out.",
  h1="Content creation",
  intro="Great content helps build trust and attract the right audience. We create content that supports your ads, improves SEO, and helps your brand stand out online.",
  card="Content that supports your ads, improves SEO and helps your brand stand out.",
  included=[("Ad creative","Image and video ads built around your strongest offer."),
            ("Website copy","Clear, conversational copy for your homepage, service pages and landing pages."),
            ("SEO content","Service and location pages that help you show up in local searches."),
            ("Answers to customer questions","Articles and FAQs that answer what your customers ask, which helps with both SEO and AEO."),
            ("Consistent voice","Content that sounds like your business across your ads, website and search listings.")],
  approach=["Good content starts with knowing your customers. We learn how you talk about your business and what your customers care about, then write and design around that.",
            "Everything we create has a job to do, whether that’s getting a click, ranking in search or turning a visitor into a lead."],
  cases=["phibro-renewoil","olson-floor-supply"],
  faq=[("What kind of content do you create?","Image and video ad creative, website and landing page copy, service and location pages for SEO, and articles and FAQs that answer customer questions."),
       ("How does content help SEO?","Search engines and AI assistants recommend pages that clearly answer what people are looking for. Well-structured content on the right topics helps you show up for those searches.")]),
 dict(slug="digital-marketing-consulting", outcomes=['Know what’s working and what’s wasting money', 'A clear plan focused on what will make an impact', 'Your budget goes only to what your business needs'], proof=('Spade Security came to us after their last agency spent heavily on ads that weren’t bringing in the right leads.', '/case-studies/spade-security/'), name="Digital Marketing Consulting", sub="",
  title="Digital Marketing Consulting",
  desc="Digital marketing consulting from Upstream Digital: honest feedback on what’s working, the opportunities you’re missing, and a clear strategy for growth.",
  h1="Digital marketing consulting",
  intro="Not sure where to start or what’s working? We help businesses make sense of their marketing, identify opportunities, and build a clear strategy for growth.",
  card="Make sense of your marketing and build a clear strategy for growth.",
  included=[("A look at what you’re doing now","We review your ads, website, search presence and current results."),
            ("Honest feedback","A straight answer on what’s working, what isn’t, and why."),
            ("Opportunities","Where you could be getting more from your budget, your website or search."),
            ("A clear strategy","A focused plan built around what your business actually needs, not a list of every possible service."),
            ("A second opinion","If you already work with an agency, an outside view on whether you’re getting the results you should.")],
  approach=["We don’t throw the entire kitchen sink at a problem. Our goal is to understand your business first and focus on the strategies that will actually make an impact.",
            "That might mean targeted ad campaigns, improving your website, or helping you rank higher on Google. Whatever the case, we focus on what you truly need."],
  cases=["spade-security","phibro-renewoil"],
  faq=[("What happens in a consultation?","We start with a quick, no obligation call to learn about your business, your goals and what you’re currently doing. We’ll give you honest feedback on what we’re seeing and where there may be opportunities to improve."),
       ("Do I have to sign up for other services?","No. We only recommend what your business actually needs, and we work month to month with no long-term lock-in.")]),
]

CHECK = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def svc_card(v):
    return f'''      <article class="svc-card">
        <p class="work-sector">{esc(v["sub"] or "Service")}</p>
        <h3><a href="/services/{v["slug"]}/">{esc(v["name"])}</a></h3>
        <p class="work-lede">{esc(v["card"])}</p>
        <span class="work-more" aria-hidden="true">Learn more <span>→</span></span>
      </article>'''

def faq_block(items, hid="faq", title="Common questions"):
    body = "\n".join(f'          <details class="faq-item"><summary><h3>{esc(q)}</h3></summary><p>{esc(a)}</p></details>' for q, a in items)
    return f'''        <section aria-labelledby="{hid}" class="cs-faq">
          <h2 id="{hid}">{title}</h2>
{body}
        </section>'''

def service_page(v):
    path = f"/services/{v['slug']}/"
    schema = [
      {"@context": "https://schema.org", "@type": "Service", "name": v["name"], "serviceType": v["name"], "description": v["desc"], "url": DOMAIN + path,
       "provider": {"@type": "ProfessionalService", "name": "Upstream Digital", "url": DOMAIN + "/", "telephone": "+1-860-450-6983",
                    "address": {"@type": "PostalAddress", "addressLocality": "Greenwich", "addressRegion": "CT", "postalCode": "06830", "addressCountry": "US"}},
       "areaServed": [{"@type": "State", "name": "Connecticut"}, {"@type": "State", "name": "New York"}, {"@type": "Country", "name": "United States"}]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Services", "item": DOMAIN + "/services/"},
        {"@type": "ListItem", "position": 3, "name": v["name"], "item": DOMAIN + path}]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in v["faq"]]},
    ]
    impact = "\n".join(f'            <li><span class="svc-check">{CHECK}</span>{esc(o)}</li>' for o in v["outcomes"])
    inc = "\n".join(f'            <li><span class="svc-check">{CHECK}</span><div><h3>{esc(h)}</h3><p>{esc(t)}</p></div></li>' for h, t in v["included"])
    appr = "\n".join(f"          <p>{esc(x)}</p>" for x in v["approach"])
    others = "\n".join(f'            <li><a href="/services/{o["slug"]}/">{esc(o["name"])}<span aria-hidden="true">→</span></a></li>' for o in SERVICES if o["slug"] != v["slug"])
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol><li><a href="/">Home</a></li><li><a href="/services/">Services</a></li><li><span aria-current="page">{esc(v["name"])}</span></li></ol>
    </nav>
    <p class="kicker">Services</p>
    <h1 class="title">{esc(v["h1"])}</h1>
    <p class="page-intro">{esc(v["intro"])}</p>
    <div class="page-cta">
      <a class="btn btn-solid" href="/#contact">Get a free consultation</a>
      <a class="btn btn-ghost" href="#included">What’s included</a>
    </div>
  </div>
</section>

<section class="band light cs-main">
  <div class="wrap">
    <div class="cs-grid">
      <div class="cs-text">
        <section aria-labelledby="impact" class="svc-impact">
          <h2 id="impact">What it does for your business</h2>
          <ul class="impact-list">
{impact}
          </ul>
        </section>
        <section aria-labelledby="included" class="svc-included">
          <h2 id="included">What’s included</h2>
          <ul class="svc-list">
{inc}
          </ul>
        </section>
        <section aria-labelledby="approach">
          <h2 id="approach">How we approach it</h2>
{appr}
          <p><a class="inline-link" href="/#process">See our three-step process</a></p>
        </section>
{faq_block(v["faq"])}
      </div>
      <aside class="cs-aside">
        <div class="svc-aside-card">
          <h2>Start with a free consultation</h2>
          <p>A quick, no obligation call to learn about your business and goals. Month to month, no long-term lock-in.</p>
          <a class="btn btn-solid" href="/#contact">Get Started</a>
          <a class="svc-phone" href="tel:+18604506983">Or call +1 (860) 450-6983</a>
        </div>
        <nav class="svc-others" aria-label="Other services">
          <h2>Other services</h2>
          <ul>
{others}
          </ul>
        </nav>
      </aside>
    </div>
  </div>
</section>

<section class="band more-work">
  <div class="wrap">
    <div class="work-head-row">
      <h2 class="title">Related case studies</h2>
      <a class="text-link" href="/case-studies/">See all case studies <span aria-hidden="true">→</span></a>
    </div>
    <div class="work-grid {"work-grid-3" if len(v["cases"]) == 3 else ""}">
{cards("h3", v["cases"])}
    </div>
  </div>
</section>
{CTA}'''
    return head(f'{v["title"]} | Upstream Digital', v["desc"], path, "website", schema) + body + FOOT

def services_hub():
    path = "/services/"
    title = "Digital Marketing Services | Upstream Digital"
    desc = "Paid advertising, SEO and AEO, website design and development, content creation and consulting from Upstream Digital, a digital marketing agency in Greenwich, CT."
    schema = [
      {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Services", "description": desc, "url": DOMAIN + path,
       "mainEntity": {"@type": "ItemList", "itemListElement": [
          {"@type": "ListItem", "position": i + 1, "url": f"{DOMAIN}/services/{v['slug']}/", "name": v["name"]} for i, v in enumerate(SERVICES)]}},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Services", "item": DOMAIN + path}]},
    ]
    allc = "\n".join(svc_card(v) for v in SERVICES)
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol><li><a href="/">Home</a></li><li><span aria-current="page">Services</span></li></ol>
    </nav>
    <p class="kicker">Services</p>
    <h1 class="title">A full range of digital services to help your business grow</h1>
    <p class="page-intro">From strategy to execution, we help businesses attract the right audience, generate leads, and grow online. We only recommend the services your business actually needs.</p>
  </div>
</section>

<section class="band more-work hub-work">
  <div class="wrap">
    <h2 class="visually-hidden">All services</h2>
    <div class="work-grid svc-grid">
{allc}
    </div>
  </div>
</section>
{CTA}'''
    return head(title, desc, path, "website", schema) + body + FOOT

# ---------------------------------------------------------------- privacy policy
PRIVACY = [
 ("Information We Collect", [
   ("h3", "Information You Provide"),
   ("p", "If you contact us through a form, email, or other method, we may collect information such as:"),
   ("ul", ["Name", "Email address", "Phone number", "Company name", "Any information you include in your message"]),
   ("p", "We use this information only to respond to your inquiry or provide requested services."),
   ("h3", "Automatically Collected Information"),
   ("p", "When you visit our website, certain information may be collected automatically, including:"),
   ("ul", ["IP address", "Browser type", "Device type", "Pages visited", "Time spent on pages", "Referring website"]),
   ("p", "This information helps us understand how visitors use our website and allows us to improve user experience.")]),
 ("Use of Analytics and Tracking Technologies", [
   ("p", "We use tools such as Google Analytics and Google Tag Manager to better understand website traffic and user behavior."),
   ("p", "These tools may use cookies or similar technologies to collect anonymous information about how visitors interact with our website."),
   ("p", "The information collected may include:"),
   ("ul", ["Pages visited", "Time spent on the site", "Traffic sources", "General geographic location"]),
   ("p", "This data helps us improve our website performance and user experience. We do not use this information to personally identify visitors."),
   ("html", 'You can learn more about how Google uses information here: <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">https://policies.google.com/privacy</a>')]),
 ("Cookies", [
   ("p", "Our website may use cookies to improve functionality and analyze traffic."),
   ("p", "Cookies are small files stored on your device that help websites remember information about your visit."),
   ("p", "You can choose to disable cookies through your browser settings. Please note that some parts of the website may not function properly if cookies are disabled.")]),
 ("How We Use Your Information", [
   ("p", "We may use the information we collect to:"),
   ("ul", ["Respond to inquiries or requests", "Provide services or information you request", "Improve website functionality and performance", "Analyze website traffic and usage trends", "Maintain website security"]),
   ("p", "We do not sell, rent, or trade your personal information to third parties.")]),
 ("Third-Party Services", [
   ("p", "Our website may use trusted third-party services to help operate the website or analyze traffic, including:"),
   ("ul", ["Google Analytics", "Google Tag Manager"]),
   ("p", "These services may collect information in accordance with their own privacy policies.")]),
 ("Data Security", [("p", "We take reasonable measures to protect the information collected through our website. However, no method of transmission over the internet is completely secure.")]),
 ("Links to Other Websites", [("p", "Our website may contain links to other websites. We are not responsible for the privacy practices of external sites.")]),
 ("Changes to This Privacy Policy", [("p", "We may update this Privacy Policy from time to time. Any changes will be posted on this page with an updated effective date.")]),
 ("Contact Us", [("html", 'If you have any questions about this Privacy Policy, you may contact us at: <a href="mailto:info@getupstreamdigital.com">info@getupstreamdigital.com</a>')]),
]

def slugify(t): return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def privacy_page():
    path = "/privacy-policy/"
    title = "Privacy Policy | Upstream Digital"
    desc = "How Upstream Digital collects, uses and protects the information you share through our website, including analytics, cookies and third-party services."
    schema = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Privacy Policy", "item": DOMAIN + path}]}]
    secs = []
    for h, blocks in PRIVACY:
        out = [f'        <section aria-labelledby="{slugify(h)}">', f'          <h2 id="{slugify(h)}">{esc(h)}</h2>']
        for kind, val in blocks:
            if kind == "h3": out.append(f"          <h3>{esc(val)}</h3>")
            elif kind == "p": out.append(f"          <p>{esc(val)}</p>")
            elif kind == "html": out.append(f"          <p>{val}</p>")
            elif kind == "ul": out.append('          <ul class="prose-list">' + "".join(f"<li>{esc(x)}</li>" for x in val) + "</ul>")
        out.append("        </section>")
        secs.append("\n".join(out))
    toc = "\n".join(f'            <li><a href="#{slugify(h)}">{esc(h)}</a></li>' for h, _ in PRIVACY)
    body = f'''
<section class="page-hero page-hero-sm">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">
      <ol><li><a href="/">Home</a></li><li><span aria-current="page">Privacy Policy</span></li></ol>
    </nav>
    <p class="kicker">Legal</p>
    <h1 class="title">Privacy Policy</h1>
    <p class="page-intro">Upstream Digital ("we", "our", or "us") respects your privacy and is committed to protecting the information you share with us through our website.</p>
    <p class="page-intro page-intro-2">This Privacy Policy explains how we collect, use, and safeguard your information when you visit our website.</p>
  </div>
</section>

<section class="band light cs-main">
  <div class="wrap">
    <div class="cs-grid legal-grid">
      <aside class="cs-aside legal-toc">
        <nav aria-label="On this page">
          <h2>On this page</h2>
          <ol>
{toc}
          </ol>
        </nav>
      </aside>
      <div class="cs-text prose">
{chr(10).join(secs)}
      </div>
    </div>
  </div>
</section>
'''
    return head(title, desc, path, "website", schema) + body + FOOT

def write(rel, s):
    p = os.path.join(SITE, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(s)

write("case-studies/index.html", hub_page())
write("services/index.html", services_hub())
for v in SERVICES:
    write(f"services/{v['slug']}/index.html", service_page(v))
write("privacy-policy/index.html", privacy_page())
for c in CASES:
    write(f"case-studies/{c['slug']}/index.html", case_page(c))


urls = ["/", "/services/"] + [f"/services/{v['slug']}/" for v in SERVICES] + ["/case-studies/"] + [f"/case-studies/{c['slug']}/" for c in CASES] + ["/privacy-policy/"]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
write("sitemap.xml", sm)
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
print("built", len(urls), "urls")
