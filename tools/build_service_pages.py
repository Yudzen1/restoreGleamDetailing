#!/usr/bin/env python3
"""Генератор страниц услуг для Restore Gleam Detailing.

Берёт <style>, <header> и <footer> из index.html, чтобы страницы услуг
выглядели как основной сайт и не расходились с ним при правках стиля.
Запуск:  python3 tools/build_service_pages.py
"""
import io, re, json, os

BASE  = 'https://restoregleam.vip/'
PHONE = '+18479643474'
PHONE_H = '(847) 964-3474'
EMAIL = 'restoregleamdetailing@gmail.com'
ENDPOINT = ('https://script.google.com/macros/s/AKfycbxhT55oiZDuvLfCWeIitxBl'
            'U5D1R8RikS0BjmEisOTlco4TuhTInvGxKmkSM90qqKmw0w/exec')
GA = 'G-1YXYM2Y1Q7'

src = io.open('index.html', encoding='utf-8').read()
STYLE  = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
FOOTER = re.search(r'<footer>.*?</footer>', src, re.S).group(0)

SERVICES = [
 dict(slug='paint-correction-chicago',
   h1='Paint Correction in Chicago',
   title='Paint Correction Chicago | Swirl & Scratch Polishing | Restore Gleam',
   desc='Mobile paint correction in Chicago and the North Shore. Machine polishing that removes swirls and light scratches. Send photos for a free estimate.',
   name='Paint Correction',
   option='Paint Correction / Polishing',
   lede='Machine polishing that brings depth and gloss back to tired paint. We come to you anywhere in Chicago and the North Shore.',
   body=[
    ('What paint correction actually does',
     'Over years of washing, parking and weather, a clear coat collects fine '
     'swirl marks, water spots and oxidation. Those defects scatter light, '
     'which is why dark paint starts to look dull and grey rather than deep. '
     'Paint correction levels a microscopic amount of clear coat with a '
     'machine polisher and progressively finer compounds, so light reflects '
     'evenly again.'),
    ('An honest word about scratches',
     'Polishing removes swirls and light scratches very effectively. Deeper '
     'scratches that you can feel with a fingernail have gone through the '
     'clear coat, and no amount of polishing brings those back — they need '
     'touch-up paint or a body shop. We will tell you which kind you have '
     'before any work starts, not after. Send a few photos in daylight and '
     'you will get a straight answer.'),
    ('What affects your estimate',
     'Vehicle size, how many stages of polishing the paint needs, the '
     'condition of the clear coat, paint hardness, and whether you want a '
     'wax or ceramic coating applied afterwards to protect the result. We '
     'quote per vehicle after seeing photos, never from a generic price list.'),
   ],
   checks=['Swirl mark and oxidation removal','Single or multi-stage machine polishing',
     'Water spot and light scratch correction','Paint protection applied afterwards on request',
     'We come to your home or workplace'],
   imgs=[('assets/gallery/mercedes-e63s-polishing.jpg','Machine polishing a Mercedes E63 S by Restore Gleam Detailing'),
         ('assets/gallery/lamborghini-urus-polishing.jpg','Paint polishing on a Lamborghini Urus in the Chicago area')]),

 dict(slug='interior-detailing-chicago',
   h1='Interior Detailing in Chicago',
   title='Interior Detailing Chicago | Deep Cleaning & Pet Hair | Restore Gleam',
   desc='Mobile interior car detailing in Chicago and the North Shore. Deep cleaning, stains, odors and pet hair. Send photos for a free estimate.',
   name='Interior Detailing',
   option='Interior Detailing',
   lede='A full reset of the cabin — seats, carpets, vents, glass and every surface you touch. Done at your driveway or parking spot.',
   body=[
    ('What gets done',
     'We vacuum the entire cabin including under the seats and in the seat '
     'rails, clean and condition the surfaces, shampoo or extract carpets and '
     'upholstery where the fabric allows it, wipe down the door jambs, clean '
     'the interior glass, and work the vents and tight seams that normally '
     'get skipped. Leather is cleaned with products made for leather rather '
     'than an all-purpose cleaner.'),
    ('Pet hair, stains and odors',
     'Tell us about these before we arrive, because they change how long the '
     'job takes. Pet hair woven into carpet fibers needs dedicated extraction '
     'and is charged accordingly. Most stains improve significantly and many '
     'disappear, but an outcome depends on what the stain is, how long it has '
     'been there and what the material is — we will not promise a result we '
     'cannot see yet. Odors are usually tied to a source, so the source gets '
     'removed rather than covered with fragrance.'),
    ('What affects your estimate',
     'Vehicle size and number of seats, the overall condition, pet hair, '
     'stains, spilled liquids or food, smoke odor, and whether you want a '
     'standard interior detail or a deep clean. A few photos of the seats and '
     'carpets are usually enough for an accurate number.'),
   ],
   checks=['Full vacuum including seat rails and under seats','Carpet and upholstery extraction where suitable',
     'Leather cleaned and conditioned','Vents, seams, door jambs and interior glass',
     'Pet hair, stain and odor work on request'],
   imgs=[('assets/gallery/lamborghini-interior-detail.jpg','Detailed car interior by Restore Gleam Detailing in Chicago'),
         ('assets/gallery/mercedes-interior-detail.jpg','Interior detailing of a Mercedes in the Chicago area')]),

 dict(slug='ceramic-coating-chicago',
   h1='Ceramic Coating in Chicago',
   title='Ceramic Coating Chicago | Paint Protection | Restore Gleam Detailing',
   desc='Mobile ceramic coating in Chicago and the North Shore. Paint prepared and protected against salt, rain and sun. Send photos for a free estimate.',
   name='Ceramic Coating',
   option='Ceramic Coating',
   lede='A durable protective layer bonded to prepared paint. Easier washing, better gloss, and real protection through Chicago winters.',
   body=[
    ('Why preparation matters more than the coating',
     'A coating locks in whatever is underneath it. Applied over swirls and '
     'contamination, it seals the defects in and they become much harder to '
     'fix later. That is why a coating job is mostly preparation: decontaminate '
     'the paint, then polish it, then coat it. Any shop quoting a coating '
     'without talking about the prep stage is quoting you a problem.'),
    ('What it does and does not do',
     'A coating makes the surface hydrophobic, so water beads and sheets off, '
     'road salt and brake dust release more easily, and washing takes less '
     'effort. It adds gloss and helps resist UV fading. It is not body armor: '
     'it will not stop rock chips, door dings or someone keying a panel, and '
     'it does not make the car self-cleaning. Maintenance washing still '
     'matters — we will show you how to wash it so the coating lasts.'),
    ('What affects your estimate',
     'Vehicle size, the condition of the paint and therefore how much '
     'correction it needs first, which coating product and durability tier '
     'you choose, and whether you want trim, wheels or glass coated as well. '
     'Availability of specific coating products should be confirmed when you '
     'contact us.'),
   ],
   checks=['Paint decontamination and polishing before coating',
     'Hydrophobic, easier-to-wash finish','Added gloss and UV resistance',
     'Trim, wheel and glass coating on request','Aftercare washing guidance included'],
   imgs=[('assets/gallery/porsche-taycan-detail.jpg','Coated and polished Porsche Taycan by Restore Gleam Detailing'),
         ('assets/gallery/luxury-detailing-3.jpg','Protected glossy paint finish on a luxury car in Chicago')]),

 dict(slug='headlight-restoration-chicago',
   h1='Headlight Restoration in Chicago',
   title='Headlight Restoration Chicago | Clear Up Foggy Lights | Restore Gleam',
   desc='Mobile headlight restoration in Chicago and the North Shore. Foggy, yellowed headlights sanded, polished and sealed. Send photos for an estimate.',
   name='Headlight Restoration',
   option='Headlight Restoration',
   lede='Yellowed, cloudy headlights sanded back, polished clear and sealed — usually in a single visit at your location.',
   body=[
    ('Why headlights turn yellow',
     'Modern headlight housings are polycarbonate with a thin factory UV '
     'coating on the outside. Sun, road grit and washing wear that coating '
     'away, and once it is gone the plastic underneath oxidizes and clouds '
     'over. That haze scatters your beam, which is both a safety issue at '
     'night and the fastest way to make an otherwise clean car look old.'),
    ('How the work is done',
     'The lens is masked off, wet-sanded through progressively finer grits to '
     'cut past the oxidized layer, then machine polished back to clarity, and '
     'finally sealed with a fresh UV protectant. The sealing step is what '
     'decides how long the result lasts — a polish with no sealant looks '
     'great for a few months and then hazes again.'),
    ('When restoration is not the answer',
     'If a housing is cracked, has moisture inside it, or the clouding is on '
     'the inner surface of the lens, restoration will not fix it and the unit '
     'needs replacing. Photos taken in daylight tell us which case you have '
     'before you spend anything.'),
   ],
   checks=['Wet sanding through multiple grits','Machine polishing back to clarity',
     'Fresh UV sealant so the haze does not return quickly',
     'Both headlights treated for an even match','Usually completed in one visit'],
   imgs=[('assets/split_compare.jpg','Before and after exterior detailing by Restore Gleam Detailing')]),

 dict(slug='boat-detailing-chicago',
   h1='Boat Detailing in Chicago',
   title='Boat Detailing Chicago | Hull Oxidation & Polishing | Restore Gleam',
   desc='Mobile boat detailing near Chicago. Gelcoat oxidation removal, hull polishing and wax protection. Send photos and boat size for an estimate.',
   name='Boat Detailing',
   option='Boat Detailing',
   lede='Gelcoat washing, oxidation removal, polishing and wax protection — at your marina, dock or storage lot.',
   body=[
    ('Gelcoat is not car paint',
     'Gelcoat is thicker and more porous than automotive clear coat, and it '
     'chalks rather than swirls. Sun and water leave it faded and dusty to '
     'the touch, and the hull picks up a waterline stain that normal washing '
     'will not lift. The correction process is similar in principle to paint '
     'correction but uses different compounds and pads.'),
    ('What the work covers',
     'Wash and decontamination, waterline and stain treatment, oxidation '
     'removal and compounding where the gelcoat needs it, polishing, and a '
     'marine wax or sealant so the finish holds up through the season. '
     'Interior and vinyl cleaning can be included — mention it when you '
     'contact us.'),
    ('What affects your estimate',
     'Length and type of boat, how heavily the gelcoat has oxidized, how much '
     'of the hull is above and below the waterline, where the boat is stored, '
     'and whether power and water are available on site. Please send photos, '
     'the boat length and its location.'),
   ],
   checks=['Gelcoat wash and decontamination','Oxidation removal and compounding',
     'Waterline and stain treatment','Marine wax or sealant protection',
     'Vinyl and interior cleaning on request'],
   imgs=[('assets/gallery/boat-detailing-1.jpg','Boat detailing by Restore Gleam Detailing near Chicago'),
         ('assets/gallery/boat-polishing-red.jpg','Polishing a red boat hull after oxidation removal'),
         ('assets/gallery/sailboat-polishing.jpg','Sailboat hull polishing near Chicago')]),
]

SERVICE_OPTIONS = ['Interior Detailing','Exterior Wash & Wax','Interior + Exterior Detailing',
  'Paint Correction / Polishing','Ceramic Coating','Headlight Restoration',
  'Touch-Up Paint','Boat Detailing']

def esc(t):
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def page(sv):
    url = BASE + sv['slug'] + '.html'
    others = ''.join(
        '<li><a href="%s.html">%s</a></li>' % (o['slug'], esc(o['name']))
        for o in SERVICES if o['slug'] != sv['slug'])

    schema = {"@context":"https://schema.org","@type":"Service",
      "name": sv['name'] + ' — Chicago & North Shore', "serviceType": sv['name'],
      "url": url, "description": sv['desc'],
      "provider":{"@type":"AutoDetailing","@id":BASE+"#business",
        "name":"Restore Gleam Detailing","telephone":"+1-847-964-3474","url":BASE},
      "areaServed":[{"@type":"City","name":c,"containedInPlace":{"@type":"State","name":"Illinois"}}
        for c in ["Chicago","Evanston","Skokie","Wilmette","Glenview","Northbrook",
                  "Deerfield","Highland Park","Park Ridge"]],
      "availableChannel":{"@type":"ServiceChannel","servicePhone":
        {"@type":"ContactPoint","telephone":"+1-847-964-3474"},"serviceUrl":url}}

    crumbs = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":BASE},
      {"@type":"ListItem","position":2,"name":sv['name'],"item":url}]}

    sections = ''.join(
      '\n      <h2 class="section-title">%s</h2>\n      <p class="area-text">%s</p>' %
      (esc(h), esc(b)) for h, b in sv['body'])

    gallery = ''.join(
      '<figure class="work-card"><img src="%s" alt="%s" loading="lazy" width="800" height="600"></figure>'
      % (src_, esc(alt)) for src_, alt in sv['imgs'])

    opts = ''.join('<option%s>%s</option>' %
      (' selected' if o == sv['option'] else '', esc(o)) for o in SERVICE_OPTIONS)

    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{ga}');
  </script>
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{url}" />
  <meta name="theme-color" content="#07101f" />
  <meta property="og:url" content="{url}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Restore Gleam Detailing" />
  <meta property="og:title" content="{h1} | Restore Gleam Detailing" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="{img0}" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">
{schema}
  </script>
  <script type="application/ld+json">
{crumbs}
  </script>
  <style>{style}</style>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header><div class="wrap nav">
    <a class="brand" href="./"><img src="logo.png" alt="Restore Gleam Detailing" width="40" height="40"><span class="brand-name">Restore Gleam</span></a>
    <div class="buttons">
      <a class="btn secondary" href="./">All Services</a>
      <a class="btn" href="tel:{phone}">Call {phone_h}</a>
    </div>
  </div></header>

  <main id="main">
    <section class="hero"><div class="wrap">
      <p class="muted"><a href="./">Home</a> → {name}</p>
      <h1>{h1}</h1>
      <p class="area-text">{lede}</p>
      <div class="buttons">
        <a class="btn" href="#quote">Get My Free Estimate</a>
        <a class="btn secondary" href="sms:{phone}">Text Photos</a>
      </div>
    </div></section>

    <section><div class="wrap">
      <ul class="checks">{checks}</ul>
    </div></section>

    <section><div class="wrap">{sections}
    </div></section>

    <section><div class="wrap">
      <h2 class="section-title">Recent work</h2>
      <div class="gallery">{gallery}</div>
      <p class="muted">Photos of work completed by Restore Gleam Detailing. Results vary with the condition of each vehicle.</p>
    </div></section>

    <section id="quote"><div class="wrap quote-grid">
      <div>
        <h2 class="section-title">Get an estimate for {name_l}</h2>
        <p class="area-text">Mobile service across Chicago and the North Shore. Send your suburb or ZIP code so we can check travel and availability.</p>
        <ol class="steps"><li>Tell us your vehicle, location and service.</li><li>Text 2–3 clear photos, including any damage.</li><li>Receive an estimate and confirm the scope before booking.</li></ol>
        <p class="muted">Pricing depends on size, condition and the work requested. Every estimate is confirmed by the owner before any booking.</p>
      </div>
      <form id="quote-form" class="quote-panel">
        <h3>Request your free quote</h3>
        <label for="quote-name">Your name</label><input id="quote-name" maxlength="120" autocomplete="name" required>
        <label for="quote-phone">Phone number</label><input id="quote-phone" type="tel" maxlength="40" autocomplete="tel" required>
        <label for="quote-email">Email (optional)</label><input id="quote-email" type="email" maxlength="120" autocomplete="email">
        <label for="quote-service">Service</label><select id="quote-service" required>{opts}</select>
        <label for="quote-vehicle">Vehicle or boat model</label><input id="quote-vehicle" maxlength="120" placeholder="e.g., 2014 Tesla Model S" required>
        <label for="quote-location">Suburb or ZIP code</label><input id="quote-location" maxlength="120" autocomplete="postal-code" required>
        <label for="quote-notes">Condition / preferred day (optional)</label><textarea id="quote-notes" maxlength="600"></textarea>
        <div style="position:absolute;left:-9999px" aria-hidden="true"><label for="quote-company">Company</label><input id="quote-company" tabindex="-1" autocomplete="off"></div>
        <button class="btn" type="submit">Send My Request</button>
        <p><small>We usually reply the same day. Photos help us quote accurately — after sending, you can text them to us in one tap.</small></p>
        <div id="quote-output" class="quote-output" aria-live="polite"></div>
        <a id="quote-send" class="btn" hidden>Text Us Your Photos</a>
      </form>
    </div></section>

    <section><div class="wrap">
      <h2 class="section-title">Other services</h2>
      <ul class="checks">{others}</ul>
    </div></section>
  </main>

{footer}
<script>
const LEAD_ENDPOINT = '{endpoint}';
const LEAD_SOURCE   = '{slug}';

function track(name, params){{
  try {{ if (typeof gtag === 'function') gtag('event', name, params || {{}}); }} catch(e){{}}
}}
function val(id){{ return (document.getElementById(id).value || '').trim(); }}

document.getElementById('quote-form').addEventListener('submit', function(event){{
  event.preventDefault();
  const out  = document.getElementById('quote-output');
  const link = document.getElementById('quote-send');
  const btn  = this.querySelector('button[type=submit]');

  const d = {{ name:val('quote-name'), phone:val('quote-phone'), email:val('quote-email'),
              service:val('quote-service'), vehicle:val('quote-vehicle'),
              zip:val('quote-location'), notes:val('quote-notes'),
              company:val('quote-company'), source:LEAD_SOURCE }};

  if(!d.name || !d.phone || !d.service || !d.vehicle || !d.zip){{
    out.textContent = 'Please fill in your name, phone, service, vehicle and location.';
    return;
  }}

  const message = ['Hi Restore Gleam! I would like a quote.','Name: '+d.name,
    'Service: '+d.service,'Vehicle / boat: '+d.vehicle,'Location: '+d.zip,
    d.notes?'Notes: '+d.notes:'',
    'I will attach photos. Please confirm the estimate and availability.'
  ].filter(Boolean).join('\\n');
  link.href = 'sms:{phone}?body=' + encodeURIComponent(message);

  btn.disabled = true;
  out.textContent = 'Sending your request\\u2026';

  fetch(LEAD_ENDPOINT, {{ method:'POST',
    headers:{{'Content-Type':'text/plain;charset=utf-8'}}, body: JSON.stringify(d) }})
  .then(function(r){{ return r.json(); }})
  .then(function(res){{
    if(res && res.status === 'ok'){{
      out.textContent = 'Thanks, ' + d.name + '! We received your request and will contact you at ' + d.phone + '. Next step: text us 2\\u20133 photos so we can quote accurately.';
      link.hidden = false; btn.textContent = 'Request Sent';
      track('generate_lead', {{ service: d.service, method: LEAD_SOURCE }});
    }} else {{ throw new Error('rejected'); }}
  }})
  .catch(function(){{
    track('lead_form_error', {{ service: d.service }});
    out.textContent = 'We could not send that automatically. Please text or call us at {phone_h} \\u2014 tap the button below and your details are already filled in.';
    link.hidden = false; btn.disabled = false;
  }});
}});

document.addEventListener('click', function(ev){{
  const a = ev.target.closest && ev.target.closest('a[href^="tel:"], a[href^="sms:"]');
  if(!a) return;
  track('contact', {{ method: a.getAttribute('href').indexOf('tel:') === 0 ? 'phone_call' : 'sms' }});
}}, true);
</script>
</body>
</html>
""".format(
      ga=GA, title=esc(sv['title']), desc=esc(sv['desc']), url=url,
      h1=esc(sv['h1']), name=esc(sv['name']), name_l=esc(sv['name'].lower()),
      lede=esc(sv['lede']), img0=BASE+sv['imgs'][0][0],
      schema=json.dumps(schema, indent=2), crumbs=json.dumps(crumbs, indent=2),
      style=STYLE, phone=PHONE, phone_h=PHONE_H,
      checks=''.join('<li class="check">%s</li>' % esc(c) for c in sv['checks']),
      sections=sections, gallery=gallery, opts=opts, others=others,
      footer=FOOTER, endpoint=ENDPOINT, slug=sv['slug'])

if __name__ == '__main__':
    for sv in SERVICES:
        for rel, _ in sv['imgs']:
            if not os.path.exists(rel):
                raise SystemExit('НЕТ ФАЙЛА: ' + rel)
        out = sv['slug'] + '.html'
        io.open(out, 'w', encoding='utf-8').write(page(sv))
        print('создано: %-38s %6d байт' % (out, os.path.getsize(out)))

    urls = [(BASE, '1.0')] + [(BASE + s['slug'] + '.html', '0.8') for s in SERVICES]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, p in urls:
        sm += ['  <url>', '    <loc>%s</loc>' % u, '    <lastmod>2026-11-14</lastmod>',
               '    <changefreq>monthly</changefreq>', '    <priority>%s</priority>' % p, '  </url>']
    sm.append('</urlset>')
    io.open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
    print('sitemap.xml: %d URL' % len(urls))
