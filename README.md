# Wearhue: colours that love your skin

A free web app. Pick your skin tone, answer 3 undertone questions, and get your best colours, neutrals, colours to avoid, jewellery metals, outfit combinations, and a "Does it match?" checker for any two colours.

Works on phone and laptop, and can be installed like an app (Add to Home Screen). It needs no sign-up and has no backend, and photos never leave the user's device.

## Live at: https://sheihab.github.io/wearhue/

Hosted free on GitHub Pages (repo `sheihab/wearhue`). Upload changed files to the repo and the site updates within a minute.

### Make Google find it (do once, free)
1. Go to Google Search Console → Add property → **URL prefix** → `https://sheihab.github.io/wearhue/`
2. Choose "HTML tag" verification, then paste the tag into `index.html` where it says `<!-- Google Search Console -->`.
3. Sitemaps → submit `sitemap.xml`.
4. URL inspection → "Request indexing" for the homepage and each guide page.

### Track your visitors (free)
- **Google Search Console** shows which Google searches show your site, clicks and position. Data starts appearing a few days after you verify.
- **Google Analytics 4** shows visitors, countries, devices, and how many people finish the test (`palette_result` event) or share. Create a GA4 property, then paste the `G-…` ID into `analytics.js`. Every page uses that one file.

### Android & laptop
- **Android:** open the link in Chrome → "Install app" button (or menu → Add to Home screen). It then opens full-screen like a normal app.
- **Laptop:** Chrome/Edge show an install icon in the address bar. It also works in any browser without installing.
- **Mac:** Chrome → install icon in the address bar, or Safari → File → Add to Dock (macOS Sonoma or later).
- **Google Play (later):** package with PWABuilder.com (Trusted Web Activity). It needs a one-time US$25 Google Play developer fee, plus a file at the *root* of the domain (`/.well-known/assetlinks.json`). So either add a `sheihab.github.io` repo for that file, or do it after buying a domain.
- **Mac App Store (later):** needs an Apple Developer account (US$99/yr). The free "Add to Dock" install covers Mac users until then.

## Making money: the realistic order

| Stage | What to do | Cost |
|---|---|---|
| Now | Grow traffic (see below). The "Shop this colour" button is **hidden** until you add an affiliate tag, so you never send free traffic anywhere. | $0 |
| Optional | **Affiliate links** pay you a commission when someone buys. Apply to Amazon Associates AU (or The Iconic / SHEIN via affiliate networks), then put your tagged link in `SHOP_URL` and the button appears. | $0 |
| ~1–3k visitors/month | **Buy a domain** (~$15–20/yr, e.g. wearhue.app or wearhue.co if available) and connect it in GitHub Pages settings. | ~$20/yr |
| With the domain | **Apply for Google AdSense.** Paste your `ca-pub-…` id and slot ids into `CONFIG` in `index.html`, and put your pub id in `ads.txt`. Ad slots stay hidden until you do. | $0 |
| Later | Premium extras (e.g. 12-season deep analysis or a printable palette card) as a one-off purchase. **No weekly subscriptions**: that's what users hate about competitors. | — |

> `ads.txt` and `robots.txt` only work at the root of a domain, so they start working once you connect your own domain.
> AdSense usually rejects free subdomains (github.io, vercel.app, netlify.app), so treat the domain as the step that unlocks ads. Affiliate programs generally don't require one.

## Email list (optional, not required)
Create a free Google Form or Tally form and paste its link into `NEWSLETTER_URL`. A small "Join the list" box then appears under the results. Never force sign-up before showing results: that kills conversions.

## Keywords this site targets
Each guide page is written around what people actually type into Google:
- "what colours suit my skin tone", "colour analysis free" → home page
- "best colours for dark skin" / "colors for brown skin" → `best-colours-for-dark-skin.html`
- "colours for olive / medium skin" → `best-colours-for-medium-skin.html`
- "colours for pale / fair skin" → `best-colours-for-fair-skin.html`
- "warm vs cool undertone", "how to find my undertone" → `warm-vs-cool-undertone.html`
- "what colours go together clothes" → `what-colours-go-together.html`

To add more pages, edit and re-run `gen_pages.py`. Aim for one new guide every week or two, e.g. "what colour shirt goes with navy pants" or "colours for olive skin men".

## Getting customers (free)
- **TikTok / Reels / Shorts**: "What colours suit dark skin?" videos screen-recording the app. Colour analysis is a huge trend on these platforms.
- **Reddit**: r/coloranalysis, r/malefashionadvice, r/femalefashionadvice, r/IndianFashionAddicts (follow each sub's self-promo rules).
- **Share links**: every result has a Share button that creates a link (`?t=7&u=warm`) showing that palette, which makes it easy to spread.
- **ANU / campus**: clubs, hall socials, Instagram stories.
- **SEO pages (next step)**: add pages like `/best-colours-for-dark-skin`, `/what-colours-go-with-olive` and so on. These are what people search for.

## Files
- `analytics.js`: paste your Google Analytics ID here
- `gen_pages.py`: generates all guide pages + sitemap (add new "what goes with X" pages here)
- `index.html`: the whole app (edit `CONFIG` at the top of the script)
- `privacy.html`: privacy policy (AdSense requires one; update the contact email)
- `manifest.webmanifest`, `sw.js`, `icon.svg`: make it installable and work offline
- `ads.txt`: replace the placeholder with your AdSense publisher id
