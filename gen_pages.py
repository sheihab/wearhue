"""Generates Wearhue's guide pages, sitemap and robots.txt.
Run:  python3 gen_pages.py   (writes next to this file)
Add a new 'what colours go with X' page by adding an entry to GOES_WITH."""
import os, json, html
OUT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://sheihab.github.io/wearhue/"
TODAY = "2026-11-22"
esc = html.escape

CSS = """*{box-sizing:border-box}body{margin:0;background:#F7F3EE;color:#1B1A19;font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
a{color:inherit}main{max-width:760px;margin:0 auto;padding:12px 20px 60px}
.top{display:flex;justify-content:space-between;align-items:center;height:56px;max-width:760px;margin:0 auto;padding:0 20px}
.logo{font-family:"Iowan Old Style",Palatino,Georgia,serif;font-size:22px;text-decoration:none}.top a.go{font-size:15px}
h1,h2,h3{font-family:"Iowan Old Style",Palatino,Georgia,serif;font-weight:500;letter-spacing:-.015em;line-height:1.15}
h1{font-size:clamp(32px,6vw,44px);margin:14px 0 10px}h2{font-size:26px;margin:38px 0 10px}h3{font-size:20px;margin:22px 0 6px}
.lead{color:#5F5A54;font-size:19px}.k{font-size:13px;color:#6F6A64;margin:0}
.answer{background:#fff;border-left:4px solid #1B1A19;border-radius:0 14px 14px 0;padding:16px 18px;margin:18px 0}
.cta{display:inline-block;background:#1B1A19;color:#fff;text-decoration:none;border-radius:999px;padding:14px 24px;font-weight:600;margin:8px 0}
.card{background:#fff;border-radius:18px;padding:20px;box-shadow:0 1px 2px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.05);margin:14px 0}
.sw{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;margin-top:10px}
.sw div{font-size:12px;line-height:1.2;color:#6F6A64}.sw i{display:block;aspect-ratio:1;border-radius:12px;margin-bottom:6px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.06);position:relative;overflow:hidden}
.sw i b{position:absolute;left:50%;bottom:-30%;width:60%;aspect-ratio:1;border-radius:50%;transform:translateX(-50%)}
.pair{display:flex;gap:14px;align-items:flex-start;padding:14px 0;border-top:1px solid #EEE8E0}.pair:first-child{border-top:0;padding-top:0}
.duo{display:flex;flex:none;margin-top:3px}.duo i{width:46px;height:46px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.06)}.duo i:first-child{border-radius:10px 0 0 10px}.duo i:last-child{border-radius:0 10px 10px 0}
.pair b{display:block}.pair span{color:#5F5A54;font-size:16px}
ul{padding-left:20px}li{margin:6px 0}
.more{display:flex;flex-wrap:wrap;gap:8px}.more a{background:#fff;border:1px solid #E6E0D8;border-radius:999px;padding:7px 14px;font-size:14px;text-decoration:none}
footer{text-align:center;color:#6F6A64;font-size:13px;padding:20px}
@media(max-width:520px){.sw{grid-template-columns:repeat(3,minmax(0,1fr))}.duo i{width:38px;height:38px}}"""

ALL_LINKS = []  # filled below: (file, label)

def page(fn, title, desc, body, faq=None):
    ld = [{"@context":"https://schema.org","@type":"Article","headline":title.split(" | ")[0],"description":desc,
           "url":BASE+fn,"datePublished":TODAY,"dateModified":TODAY,"author":{"@type":"Organization","name":"Wearhue"},
           "publisher":{"@type":"Organization","name":"Wearhue"}},
          {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Wearhue","item":BASE},
            {"@type":"ListItem","position":2,"name":title.split(" | ")[0],"item":BASE+fn}]}]
    if faq:
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
    faq_html = ""
    if faq:
        faq_html = "<h2>Quick answers</h2>" + "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q,a in faq)
    more = "".join(f'<a href="{f}">{esc(l)}</a>' for f,l in ALL_LINKS if f != fn)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{BASE}{fn}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="article"><meta property="og:url" content="{BASE}{fn}"><meta property="og:image" content="{BASE}og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:site_name" content="Wearhue"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="icon-192.png"><link rel="apple-touch-icon" href="icon-180.png"><link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#F7F3EE">
<script type="application/ld+json">{json.dumps(ld)}</script>
<script src="analytics.js" defer></script><style>{CSS}</style></head><body>
<div class="top"><a class="logo" href="./">Wearhue</a><a class="go" href="./">Find my colours →</a></div>
<main>{body}{faq_html}
<div class="card" style="text-align:center;margin-top:36px"><h2 style="margin-top:0">Find the colours that suit you</h2><p style="color:#5F5A54;margin-top:0">Free, 30 seconds, no sign-up. Works with a selfie or by picking your shade.</p><a class="cta" href="./">Start now →</a></div>
<h2>More colour guides</h2><div class="more">{more}</div></main>
<footer>© Wearhue · <a href="./">Colour analysis</a> · <a href="privacy.html">Privacy</a></footer></body></html>"""

def duo(a, b): return f'<div class="duo"><i style="background:{a}"></i><i style="background:{b}"></i></div>'
def swatches(items, skin):
    return '<div class="sw">' + "".join(
        f'<div><i style="background:{h}"><b style="background:{skin}"></b></i>{esc(n)}</div>' for h,n in items) + "</div>"

# ---------------------------------------------------------------- skin tone pages
SKIN_PAGES = [
 dict(fn="best-colours-for-dark-skin.html", label="Colours for dark & brown skin", skin="#5A3825",
  title="Best Colours for Dark & Brown Skin (Clothes Guide) | Wearhue",
  desc="The clothing colours that look best on dark and brown skin: brights, jewel tones and crisp white, plus what to avoid and easy outfit ideas for men and women.",
  h1="The best colours for dark and brown skin",
  answer="<b>Short answer:</b> bright, saturated colours look best on dark and brown skin: cobalt blue, emerald, fuchsia, orange, red and mustard. So do crisp white and pastels, which create strong contrast. Be careful with browns and khakis close to your own shade, and with all-black outfits that hide your features.",
  sections=[
   ("Why bright colours work", "Deep skin has a lot of natural richness, so colours need enough intensity to stand next to it. Muted, dusty shades can make skin look dull. Strong, clear colours make it glow. High contrast (white, bright yellow, cobalt) looks especially sharp."),
  ],
  by_under=[
   ("Warm undertone (golden or reddish)", "Gold jewellery suits you; skin glows in sunlight.",
    [("#FFB703","Saffron"),("#FB8500","Tangerine"),("#D62828","Tomato red"),("#2A9D8F","Teal"),("#6A994E","Leaf green"),("#9B2226","Oxblood")]),
   ("Cool undertone (blue or ashy)", "Silver suits you; skin can look slightly blue or plum in shade.",
    [("#0047AB","Cobalt"),("#FF1493","Hot pink"),("#00A86B","Jade"),("#7B2CBF","Violet"),("#DC143C","Crimson"),("#00B4D8","Cyan")]),
   ("Neutral undertone", "Gold and silver both look good.",
    [("#E63946","Red"),("#FFB703","Sun yellow"),("#3A86FF","Bright blue"),("#8338EC","Purple"),("#06D6A0","Mint"),("#FF006E","Pink")]),
  ],
  avoid=["<b>Browns and tans that match your skin.</b> From a distance they blend in and you lose definition. Go lighter (camel, cream) or much darker.",
         "<b>Head-to-toe black or navy.</b> It can swallow your features. Break it up with a white tee, a bright shirt or a light jacket.",
         "<b>Muddy, greyed-out shades</b> like dull olive or mid grey right next to your face."],
  outfits=["White T-shirt + cobalt chinos + white trainers",
           "Mustard knit + dark denim + brown boots",
           "Emerald shirt or dress + gold jewellery",
           "All-cream outfit (cream trousers + cream knit). Simple, but striking on dark skin.",
           "Orange or coral top + white jeans for summer"],
  faq=[("What colours look good on brown skin?","Bright and rich colours such as cobalt blue, emerald green, red, orange, mustard and fuchsia, plus crisp white and cream. Earthy shades like olive and rust also suit warm brown skin."),
       ("What colours should dark-skinned people avoid?","Mainly colours very close to your own skin tone, such as mid browns and some khakis, and outfits that are entirely black or navy. They reduce contrast and can make your features harder to see."),
       ("Does white look good on dark skin?","Yes. Crisp white is one of the most flattering colours on dark skin because of the strong contrast.")]),
 dict(fn="best-colours-for-medium-skin.html", label="Colours for medium & olive skin", skin="#C08A63",
  title="Best Colours for Medium & Olive Skin (Clothes Guide) | Wearhue",
  desc="Which clothing colours suit medium, olive and tan skin? The best shades by undertone, what to avoid, and outfit ideas that work every time.",
  h1="The best colours for medium and olive skin",
  answer="<b>Short answer:</b> medium and olive skin suits rich, mid-depth colours such as teal, terracotta, olive, burgundy, mustard and sapphire. Earth tones flatter warm and olive skin; jewel tones flatter cooler medium skin. Avoid pale yellows and beiges that sit close to your skin colour, which can make you look washed out.",
  sections=[
   ("Olive skin is often neutral-to-warm", "Olive skin has a green or grey cast that confuses most undertone tests: veins can look both blue and green. That's normal. Earth tones and deep jewel tones usually win, and very bright neon or pale pastels usually lose."),
  ],
  by_under=[
   ("Warm undertone (golden, olive)", "Gold suits you; you tan easily.",
    [("#E07A5F","Terracotta"),("#F2A541","Marigold"),("#6B8E23","Olive"),("#2A9D8F","Teal"),("#C1440E","Rust"),("#E9C46A","Mustard")]),
   ("Cool undertone (pink, rosy)", "Silver suits you; you may go pink before tanning.",
    [("#0F52BA","Sapphire"),("#50C878","Emerald"),("#8E44AD","Purple"),("#E0115F","Ruby"),("#4682B4","Steel blue"),("#DE5D83","Rose")]),
   ("Neutral undertone", "Gold and silver both work.",
    [("#2E86AB","Ocean blue"),("#A23B72","Plum"),("#F18F01","Amber"),("#3C9D5D","Jade"),("#6A4C93","Grape"),("#577590","Denim")]),
  ],
  avoid=["<b>Beige, nude and pale yellow</b> close to your skin colour. They blend in and drain your face.",
         "<b>Neon brights.</b> They tend to overpower medium skin and make it look sallow.",
         "<b>Grey right next to your face</b>, especially for olive skin. Choose navy or charcoal instead."],
  outfits=["Olive overshirt + white tee + dark jeans",
           "Burgundy knit + charcoal trousers",
           "Terracotta top + cream trousers + tan sandals",
           "Teal shirt or dress + gold accessories",
           "Navy suit + light blue shirt (a classic that suits almost every medium skin tone)"],
  faq=[("What colours look best on olive skin?","Earth tones and jewel tones: olive, khaki, terracotta, burgundy, teal, emerald and mustard. Navy and cream are the best neutrals."),
       ("What colours should olive skin avoid?","Pale yellows, beiges close to your skin colour, and very bright neons, which can make olive skin look sallow or washed out."),
       ("Is olive skin warm or cool?","Usually neutral to warm, but the green tint can make it read as cool. If both gold and silver suit you, treat yourself as neutral.")]),
 dict(fn="best-colours-for-fair-skin.html", label="Colours for fair & pale skin", skin="#EECDB6",
  title="Best Colours for Fair & Pale Skin (Clothes Guide) | Wearhue",
  desc="The most flattering clothing colours for fair and pale skin, by undertone. Why softer shades win, what to avoid, and outfit ideas.",
  h1="The best colours for fair and pale skin",
  answer="<b>Short answer:</b> fair skin looks best in soft to medium colours that don't overpower it. Think navy, soft blue, sage, dusty rose, lavender and berry for cool skin, and coral, peach, camel and warm green for warm skin. Be careful with stark black, neon and beige or nude shades that match your skin.",
  sections=[
   ("Why softer shades win", "Very intense colours can dominate fair skin, so people notice the clothes before your face. Medium-strength colours and gentle contrast balance it. You can still wear dark colours: navy and charcoal are usually kinder than pure black."),
  ],
  by_under=[
   ("Warm undertone (peachy, golden)", "Freckles and gold jewellery suit you.",
    [("#F28C6B","Coral"),("#F4A68C","Peach"),("#A8B26A","Pistachio"),("#5BAE9C","Warm turquoise"),("#C7714E","Terracotta"),("#E7C27D","Wheat")]),
   ("Cool undertone (pink, rosy)", "Silver suits you; you burn easily.",
    [("#7FA7D9","Powder blue"),("#E6A8C3","Rose pink"),("#9C89B8","Lavender"),("#3E7CB1","Sapphire"),("#C94C7C","Raspberry"),("#7DB7A5","Jade mint")]),
   ("Neutral undertone", "Gold and silver both work.",
    [("#E8A0A0","Dusty rose"),("#8FBC8F","Sage"),("#6C8EBF","Soft blue"),("#F4C095","Apricot"),("#5F9EA0","Teal grey"),("#D6A2AD","Mauve")]),
  ],
  avoid=["<b>Pure black right at your face.</b> It can make fair skin look washed out or tired. Try navy, charcoal or chocolate instead.",
         "<b>Neon and very bright yellow or orange</b>, which overpower pale skin.",
         "<b>Nude, beige and pale pink</b> close to your skin colour, unless you add contrast with a darker piece."],
  outfits=["Navy knit + light jeans + white trainers",
           "Soft blue shirt + stone chinos",
           "Sage top + cream trousers",
           "Berry or burgundy dress + silver jewellery (cool skin)",
           "Camel coat + cream roll-neck (warm skin)"],
  faq=[("What colours look good on pale skin?","Soft and medium colours: navy, soft blue, sage, dusty rose, lavender, berry and burgundy suit cool pale skin, while coral, peach, camel and warm greens suit warm pale skin."),
       ("Should pale people wear black?","You can, but pure black right next to your face can look harsh. Navy, charcoal or chocolate brown give a similar look and are usually more flattering."),
       ("What colours make pale skin look tanned?","Mid-tone warm colours like coral, terracotta and teal make fair skin look warmer and healthier. White and pastels can make it look paler.")]),
]

# ---------------------------------------------------------------- 'goes with' pages
GOES_WITH = [
 dict(slug="navy", name="navy", hex="#1F2A44",
  answer="Navy goes with white, light blue, grey, camel, burgundy, pink and mustard. White and camel are the safest; burgundy and mustard add colour without clashing.",
  pairs=[("White","#FFFFFF","The cleanest, sharpest combination: navy chinos with a white shirt or tee, or a navy blazer over white."),
         ("Light blue","#A3C4E0","Tonal and smart. The classic navy suit with a light blue shirt."),
         ("Camel / tan","#C19A6B","Warm and rich: camel coat over navy, or tan shoes and a belt with navy trousers."),
         ("Grey","#9E9E9E","Calm and professional. A grey knit with navy trousers works for work or uni."),
         ("Burgundy","#800020","Deep and stylish: a burgundy jumper or tie with navy."),
         ("Pink","#E6A8C3","Soft pink lifts navy and suits most skin tones, especially fair and medium."),
         ("Mustard","#E9C46A","Complementary contrast for a confident, autumn look.")],
  avoid="Black and navy together can look like a mistake unless the black is clearly intentional (e.g. black shoes with a navy suit is fine; a black top with navy trousers often isn't). Very dark green is also too close to navy to read well.",
  shoes="Brown, tan, white trainers or burgundy loafers. Black works for formal suits.",
  skin="Navy is one of the most universally flattering colours. On very dark skin, add a light colour near your face (white, light blue) so the outfit isn't too low-contrast.",
  faq=[("What colour shirt goes with navy pants?","White, light blue, pink, grey, and soft yellow shirts all work with navy trousers. For something bolder, try burgundy or mustard."),
       ("Can you wear black with navy?","Yes, but carefully. Black shoes or a black belt with navy are fine. Black and navy as two large pieces (top and trousers) often look mismatched because they're so close in darkness.")]),
 dict(slug="black", name="black", hex="#111111",
  answer="Black goes with almost everything. White is the classic, and grey, camel, red, pink, cobalt and emerald all look great. Bright colours look especially vivid next to black.",
  pairs=[("White","#FFFFFF","Maximum contrast, always clean. Black jeans with a white tee is a uniform for a reason."),
         ("Grey","#9E9E9E","Monochrome and modern. A grey hoodie or coat with black trousers."),
         ("Camel","#C19A6B","Black and camel is a timeless, expensive-looking pair, especially in coats and knits."),
         ("Red","#C1121F","Bold and classic. Use red as one piece: a top, bag or shoes."),
         ("Cobalt blue","#0047AB","A brighter alternative to navy that pops against black."),
         ("Emerald","#00875A","Rich and elegant, great for evening outfits."),
         ("Blush pink","#E8B4B8","Softens black, a good balance of edgy and gentle.")],
  avoid="Navy and very dark brown can look muddy next to black. Head-to-toe black is fine, but break it up with texture (denim, knit, leather) so it doesn't look flat.",
  shoes="Black, white trainers, or a bold accent colour. Brown with black is now acceptable in casual outfits.",
  skin="Fair skin can look washed out in all black near the face; add a lighter layer. Dark skin looks great with black plus a bright or white accent.",
  faq=[("What colour shirt goes with black pants?","White, grey, light blue, pink, red, emerald and camel shirts all work with black trousers. Black on black works too if the fabrics have different textures."),
       ("Does brown go with black?","Yes, in casual outfits: a camel or tan coat over black is popular. Mid brown and black can look dull together, so choose a lighter brown.")]),
 dict(slug="grey", name="grey", hex="#8E8E8E",
  answer="Grey goes with navy, white, black, burgundy, pink, light blue, yellow and green. It's a neutral, so almost any colour works. Soft pastels and deep jewel tones look best.",
  pairs=[("Navy","#1F2A44","The smart-casual classic: grey trousers and a navy knit, or the reverse."),
         ("White","#FFFFFF","Fresh and clean, ideal for summer."),
         ("Burgundy","#800020","Warms up grey and looks polished."),
         ("Pink","#E6A8C3","Grey and pink is soft and modern, great for knits."),
         ("Light blue","#A3C4E0","The office staple: a grey suit with a light blue shirt."),
         ("Mustard yellow","#E9C46A","Brings life to a grey outfit; a mustard beanie or knit is enough."),
         ("Forest green","#2E5E4E","Earthy and calm, good for autumn and winter.")],
  avoid="Brown and mid grey can look dull together. Grey that's very close to your skin tone (common on olive and tan skin) can drain your face, so keep it on your bottom half.",
  shoes="White trainers, black, brown, burgundy or grey suede.",
  skin="Cool-toned skin suits grey near the face best. Warm and olive skin should pick charcoal or warm grey, or wear grey on the bottom half.",
  faq=[("What colour shirt goes with grey pants?","White, light blue, navy, pink, black and burgundy shirts all go with grey trousers."),
       ("What colour shoes go with grey?","White trainers, black, brown, burgundy and grey suede shoes all work with grey outfits.")]),
 dict(slug="beige", name="beige", hex="#D8C3A5",
  answer="Beige goes with white, navy, brown, black, olive, light blue and burgundy. Beige with white or cream creates the popular 'quiet luxury' look; navy and black add contrast.",
  pairs=[("White / cream","#FFFDF7","Soft, tonal and expensive-looking: the neutral 'old money' style."),
         ("Navy","#1F2A44","Classic contrast, e.g. beige chinos with a navy polo."),
         ("Brown","#6F4E37","Tonal earth tones: a beige trench with brown boots."),
         ("Black","#111111","Sharp and minimal, e.g. a black top with beige trousers."),
         ("Olive","#6B8E23","Earthy and relaxed, great for warm skin tones."),
         ("Light blue","#A3C4E0","Fresh and summery, especially in shirts and denim."),
         ("Burgundy","#800020","Adds a rich accent to beige for autumn.")],
  avoid="Beige right next to your face if it's close to your skin colour, which is common on fair-to-medium skin. Wear it on the bottom half or add a contrasting layer. Neon brights can look cheap next to beige.",
  shoes="White trainers, brown or tan leather, black loafers.",
  skin="Dark skin looks great in beige because of the contrast. Fair and medium skin should break up beige near the face with navy, white or a stronger colour.",
  faq=[("What colour top goes with beige pants?","White, black, navy, light blue, olive, burgundy and brown tops all work with beige trousers."),
       ("Does beige suit everyone?","Not always near the face. If beige is close to your skin tone it can wash you out, so wear it as trousers or a coat with a contrasting colour at the top.")]),
 dict(slug="olive-green", name="olive green", hex="#6B6B3A",
  answer="Olive green goes with white, cream, black, navy, beige, brown, burgundy and mustard. White and cream are easiest; burgundy and mustard give a richer, autumn look.",
  pairs=[("White / cream","#FFFDF7","The easiest pairing: olive cargos or jacket with a white tee."),
         ("Black","#111111","Utility and streetwear: an olive bomber over a black hoodie."),
         ("Navy","#1F2A44","Smart and understated: an olive overshirt with navy chinos."),
         ("Beige / tan","#D8C3A5","An earthy, natural palette that works well together."),
         ("Burgundy","#800020","A rich autumn combination, e.g. a burgundy knit with olive trousers."),
         ("Mustard","#E9C46A","Warm and bold, great for warm skin tones."),
         ("Rust / orange","#C1440E","Earth-tone contrast, stylish for autumn.")],
  avoid="Bright green or lime with olive usually clashes. Grey with olive can look drab; choose cream or navy instead.",
  shoes="White trainers, brown boots, tan suede, black boots.",
  skin="Olive green flatters warm and medium skin. Very fair cool skin and very dark skin should add white or cream near the face for brightness.",
  faq=[("What colour shirt goes with olive green pants?","White, cream, black, navy, light blue, beige and burgundy shirts all work with olive trousers or cargos."),
       ("What colour shoes go with olive green?","White trainers, brown or tan boots, and black boots all go well with olive green.")]),
 dict(slug="brown", name="brown", hex="#6F4E37",
  answer="Brown goes with cream, white, beige, light blue, navy, olive, orange and pink. Cream and light blue are the most flattering; olive and rust make a warm, earthy outfit.",
  pairs=[("Cream / white","#FFFDF7","Soft and stylish: brown trousers with a cream knit."),
         ("Light blue","#A3C4E0","Cool against warm: a light blue shirt with brown is a classic."),
         ("Beige","#D8C3A5","Tonal neutrals that look polished."),
         ("Navy","#1F2A44","Navy with brown shoes or a brown jacket, smart and timeless."),
         ("Olive","#6B8E23","Earthy and relaxed, great for autumn."),
         ("Orange / rust","#C1440E","Warm and bold, best on warm skin tones."),
         ("Pink","#E8B4B8","Unexpected but soft and modern.")],
  avoid="Mid brown with mid grey or black can look dull and heavy. Brown close to your skin colour (common on medium and brown skin) blends in, so go lighter or darker than your skin.",
  shoes="Tan, darker brown, cream trainers or suede.",
  skin="Brown flatters warm undertones. On brown and dark skin, pick a brown clearly lighter (camel) or darker (chocolate) than your skin.",
  faq=[("What colour goes with brown pants?","Cream, white, light blue, beige, navy, olive and pink tops all go with brown trousers."),
       ("Do brown and black go together?","They can in casual outfits, especially a light brown like camel with black. Mid or dark brown with black often looks muddy.")]),
 dict(slug="burgundy", name="burgundy", hex="#800020",
  answer="Burgundy goes with navy, grey, cream, beige, black, olive and pink. Navy and grey are the safest; cream and beige make burgundy look softer and more elegant.",
  pairs=[("Navy","#1F2A44","Deep and classy, e.g. a burgundy knit with navy chinos."),
         ("Grey","#9E9E9E","Balanced and smart, ideal for work outfits."),
         ("Cream","#FFFDF7","Soft and elegant: a burgundy coat over cream."),
         ("Beige / camel","#C19A6B","Warm and rich for autumn."),
         ("Black","#111111","Dramatic and evening-ready."),
         ("Olive","#6B8E23","Earthy contrast, very autumnal."),
         ("Blush pink","#E8B4B8","Tonal and romantic.")],
  avoid="Bright red with burgundy can look off unless done deliberately as a tonal outfit. Orange and burgundy is bold. Try it as an accent only.",
  shoes="Black, dark brown, tan or burgundy leather, white trainers.",
  skin="Burgundy flatters almost every skin tone and is one of the best 'safe' colours to wear near your face.",
  faq=[("What colour shirt goes with burgundy pants?","White, cream, light blue, grey, navy and black shirts all work with burgundy trousers."),
       ("What colours go with burgundy for a wedding outfit?","Navy, grey, cream, gold and blush pink pair beautifully with burgundy for formal occasions.")]),
]


# ---- more colours (compact form): slug, name, hex, pairs[(name,hex,tip)], avoid, shoes, skin, avoid_cols
def gw(slug,name,hx,pairs,avoid,shoes,skin,avoid_cols):
    top=", ".join(p[0].lower() for p in pairs[:-1])+" and "+pairs[-1][0].lower()
    GOES_WITH.append(dict(slug=slug,name=name,hex=hx,pairs=pairs,avoid=avoid,shoes=shoes,skin=skin,avoid_cols=avoid_cols,
      answer=f"{name[0].upper()+name[1:]} goes with {top}. {pairs[0][0]} and {pairs[1][0].lower()} are the easiest; {pairs[-2][0].lower()} and {pairs[-1][0].lower()} are bolder choices.",
      faq=[(f"What colour goes with {name} clothes?",f"{top[0].upper()+top[1:]} all pair well with {name}. {avoid}"),
           (f"What colour shoes go with {name}?",shoes)]))
gw("white","white","#FFFFFF",[("Navy","#1F2A44","The crispest classic: white tee or shirt with navy trousers."),("Black","#111111","Maximum contrast: clean, graphic and always sharp."),("Denim","#577590","White tee + jeans: the most reliable casual outfit there is."),("Beige","#D8C3A5","Soft and expensive-looking, perfect for summer."),("Olive","#6B8E23","Fresh and relaxed: white with olive chinos or cargos."),("Red","#C1121F","Bold and clean: a red piece pops against white.")],
 "White goes with nearly everything; just avoid pairing it with cream or ivory, which makes the white look dull or the cream look dirty.","White trainers, tan or brown leather, navy or black shoes.","Crisp white flatters dark and medium skin especially. Very fair cool skin may prefer soft white or off-white near the face.",[("#FFFDF0","Ivory"),("#F3E5C9","Cream")])
gw("cream","cream","#F1E3C8",[("Brown","#6F4E37","Warm and tonal: cream with chocolate or tan."),("Camel","#C19A6B","The 'quiet luxury' pairing: soft, warm neutrals."),("Navy","#1F2A44","Gentler than navy + white, very elegant."),("Olive","#6B8E23","Earthy and natural, great for warm skin."),("Burgundy","#800020","Rich contrast for autumn and winter."),("Black","#111111","Softer than black + white, still sharp.")],
 "Avoid pure white next to cream (it makes the cream look yellowish) and pale yellow, which blends in.","Brown or tan leather, cream or white trainers, burgundy loafers.","Cream is softer than white, so it flatters fair and warm skin especially. On deep skin it looks rich and luxurious.",[("#FFFFFF","Pure white"),("#FFF59D","Pale yellow")])
gw("red","red","#C1121F",[("Black","#111111","Classic and powerful: red top or dress with black."),("White","#FFFFFF","Fresh and confident, great for summer."),("Navy","#1F2A44","Balances red's heat; a timeless pairing."),("Denim","#577590","Casual red: a red knit with jeans."),("Camel","#C19A6B","Warm and grown-up, great for coats."),("Pink","#E8B4B8","Bold colour-blocking: fashion-forward and fun.")],
 "Avoid orange and bright green with red unless you're deliberately colour-blocking, and avoid several reds of different tones together.","Black, nude/tan, white trainers, or red as an accent.","Warm undertones suit tomato and orange-reds; cool undertones suit blue-reds like crimson and cherry. Deep skin looks stunning in any bright red.",[("#FF6600","Orange"),("#00C853","Bright green")])
gw("pink","pink","#E6A8C3",[("Grey","#9E9E9E","Soft and modern: pink knit with grey trousers."),("Navy","#1F2A44","Smart and fresh: a pink shirt with navy."),("White","#FFFFFF","Light and summery."),("Denim","#577590","Easy casual: pink top with jeans."),("Burgundy","#800020","Tonal and romantic."),("Olive","#6B8E23","Unexpected but stylish, earthy meets soft.")],
 "Avoid pairing pink with very similar reds or oranges, which can clash, and avoid pale pink right next to fair skin of a similar shade.","White trainers, grey, tan, navy or nude shoes.","Cool undertones suit blue-pinks (rose, raspberry); warm undertones suit peachy and coral pinks. Hot pink is stunning on deep skin.",[("#FF6600","Orange"),("#F3D9C6","Nude")])
gw("light-blue","light blue","#A3C4E0",[("Navy","#1F2A44","Tonal and smart, the classic office pairing."),("White","#FFFFFF","Crisp, clean and summery."),("Beige","#D8C3A5","Light blue shirt + beige chinos: easy smart-casual."),("Grey","#9E9E9E","Calm and professional."),("Brown","#6F4E37","Light blue with brown is a timeless combination."),("Pink","#E6A8C3","Soft pastel pairing for spring.")],
 "Avoid pairing light blue with black (looks harsh) and with other pale pastels of the same lightness, which can look washed out.","Brown or tan leather, white trainers, navy suede.","Light blue flatters cool and neutral undertones, and looks fresh against deep skin. Warm skin may prefer aqua or turquoise.",[("#111111","Black"),("#E0E0E0","Pale grey")])
gw("green","forest green","#2E5E4E",[("Cream","#F1E3C8","Soft and natural, the easiest pairing."),("Camel","#C19A6B","Rich and autumnal, great for coats and knits."),("Navy","#1F2A44","Deep and understated."),("Burgundy","#800020","Jewel-tone richness for winter."),("Grey","#9E9E9E","Calm and smart."),("Mustard","#E9C46A","Warm and bold, best on warm skin.")],
 "Avoid bright lime or neon green with forest green, and avoid black, which makes the outfit look too dark and heavy.","Brown or tan leather, white trainers, black boots.","Forest green flatters warm, olive and deep skin. Very fair cool skin should add cream or white near the face.",[("#CCFF00","Neon lime"),("#111111","All black")])
gw("yellow","yellow","#FFD23F",[("Navy","#1F2A44","The best balance for yellow: bright meets deep."),("White","#FFFFFF","Fresh and summery."),("Grey","#9E9E9E","Grounds yellow so it feels wearable."),("Denim","#577590","Easy casual summer outfit."),("Black","#111111","High-impact and graphic."),("Lavender","#B39DDB","Complementary pastels for spring.")],
 "Avoid yellow right next to your face if your skin has a lot of yellow in it (common on olive skin), and avoid pairing it with orange or brown, which looks muddy.","White trainers, tan, navy or grey shoes.","Bright yellow is stunning on deep skin. Fair and olive skin often suit softer butter yellow or mustard better.",[("#FF6600","Orange"),("#8B6B4A","Mid brown")])
gw("mustard","mustard","#E9C46A",[("Navy","#1F2A44","The classic mustard pairing: rich and balanced."),("Grey","#9E9E9E","Calm grey lets mustard shine."),("Olive","#6B8E23","Earthy autumn outfit."),("Burgundy","#800020","Warm and rich for cold months."),("Denim","#577590","Easy casual."),("Cream","#F1E3C8","Soft and warm, very flattering on warm skin.")],
 "Avoid mustard near the face if it's close to your skin tone (common on olive and medium-warm skin), and avoid neon colours with it.","Brown boots, white trainers, tan or burgundy leather.","Mustard flatters warm and deep skin beautifully. Cool, fair skin can wear it away from the face, as trousers or a bag.",[("#CCFF00","Neon lime"),("#DCC7AA","Nude")])
gw("orange","orange","#F28C28",[("Navy","#1F2A44","Complementary contrast, the best partner for orange."),("White","#FFFFFF","Bright and summery."),("Denim","#577590","Easy casual."),("Olive","#6B8E23","Earthy and relaxed."),("Cream","#F1E3C8","Soft and warm."),("Cobalt","#0047AB","Bold colour-blocking for the confident.")],
 "Avoid orange with red or pink (it can clash) and with black near the face, which can look harsh.","White trainers, tan, brown or navy shoes.","Orange is fantastic on deep and warm skin. Cool fair skin may prefer coral or soft peach.",[("#C1121F","Red"),("#FF1493","Hot pink")])
gw("purple","purple","#6A4C93",[("Grey","#9E9E9E","Smart and calm."),("Black","#111111","Dramatic and elegant."),("White","#FFFFFF","Crisp and fresh."),("Mustard","#E9C46A","Complementary contrast: bold and stylish."),("Denim","#577590","Casual purple."),("Olive","#6B8E23","Unexpected, earthy and modern.")],
 "Avoid purple with red or orange (clashes) and with brown, which can look muddy.","Black, grey, white trainers, silver or metallic accents.","Purple flatters cool undertones and deep skin especially. Warm skin should try warmer plum or aubergine.",[("#C1121F","Red"),("#8B6B4A","Brown")])
gw("lavender","lavender","#B39DDB",[("Grey","#9E9E9E","Soft and modern."),("White","#FFFFFF","Fresh and pretty."),("Navy","#1F2A44","Grounds the pastel for work."),("Denim","#577590","Easy casual."),("Sage","#8FBC8F","A pastel pairing perfect for spring."),("Cream","#F1E3C8","Soft and gentle.")],
 "Avoid lavender with bright orange or mustard right next to each other unless deliberate, and avoid it near the face on very warm, golden skin.","White trainers, silver, grey or nude shoes.","Lavender suits cool and fair skin, and looks fresh on deep skin. Warm skin may prefer warmer lilac or mauve.",[("#FF6600","Orange"),("#C9A227","Old gold")])
gw("teal","teal","#008080",[("Cream","#F1E3C8","Soft and elegant."),("Navy","#1F2A44","Deep and sophisticated."),("Coral","#F28C6B","Complementary pop, great for summer."),("Grey","#9E9E9E","Calm and smart."),("Mustard","#E9C46A","Rich and bold."),("Camel","#C19A6B","Warm and grown-up.")],
 "Avoid teal with bright green or bright blue of similar strength; they compete rather than complement.","Tan or brown leather, white trainers, navy or black.","Teal is one of the most universally flattering colours: it suits almost every skin tone.",[("#00C853","Bright green"),("#2962FF","Bright blue")])
gw("emerald","emerald green","#00875A",[("White","#FFFFFF","Fresh, high-contrast and elegant."),("Black","#111111","Dramatic evening look."),("Navy","#1F2A44","Deep jewel tones together."),("Camel","#C19A6B","Warm and luxurious."),("Burgundy","#800020","Jewel-tone richness for winter."),("Gold","#C9A227","Festive and glamorous.")],
 "Avoid emerald with lime or neon green, and with bright red unless you want a festive look.","Black, nude/tan, gold or white shoes.","Emerald flatters cool and deep skin especially, and looks stunning on dark skin.",[("#CCFF00","Neon lime"),("#FF0000","Bright red")])
gw("camel","camel","#C19A6B",[("Black","#111111","Timeless and expensive-looking."),("White","#FFFFFF","Clean and fresh."),("Navy","#1F2A44","Classic smart-casual."),("Cream","#F1E3C8","Soft tonal neutrals."),("Burgundy","#800020","Rich and warm."),("Denim","#577590","Easy casual: camel coat over jeans.")],
 "Avoid camel right next to your face if it's close to your skin colour (common on medium and tan skin). Add a white or dark layer between.","Black, brown, white trainers, burgundy loafers.","Camel suits warm and deep skin beautifully. Cool skin can wear it with a white or navy layer near the face.",[("#DCC7AA","Nude"),("#B8860B","Dark mustard")])
gw("khaki","khaki","#BDB76B",[("White","#FFFFFF","Fresh and casual."),("Navy","#1F2A44","Classic khaki chinos + navy."),("Black","#111111","Utility style."),("Light blue","#A3C4E0","Smart-casual staple."),("Olive","#6B8E23","Tonal earth tones."),("Burgundy","#800020","Warm autumn contrast.")],
 "Avoid khaki with beige or tan that's almost the same shade, which looks like a mistake, and keep it away from the face if it matches your skin.","White trainers, brown or tan leather, navy suede.","Khaki flatters warm and deep skin. Fair and olive skin should keep it on the bottom half.",[("#D8C3A5","Beige"),("#C2B280","Sand")])
gw("denim","denim blue","#577590",[("White","#FFFFFF","The most reliable outfit there is."),("Black","#111111","Sharp and casual."),("Camel","#C19A6B","Warm and polished."),("Red","#C1121F","Classic Americana."),("Grey","#9E9E9E","Calm and easy."),("Mustard","#E9C46A","Warm pop of colour.")],
 "Avoid matching your denim top and bottom in exactly the same wash. Make them clearly different shades.","White trainers, brown boots, black boots, loafers.","Denim suits every skin tone. Very dark skin looks great in lighter washes for contrast.",[("#577590","Same wash"),("#3B5998","Near match")])
gw("coral","coral","#F28C6B",[("Navy","#1F2A44","Bright meets deep, very flattering."),("White","#FFFFFF","Fresh and summery."),("Teal","#008080","Complementary pop."),("Denim","#577590","Easy casual."),("Cream","#F1E3C8","Soft and warm."),("Grey","#9E9E9E","Calm and modern.")],
 "Avoid coral with red or hot pink, and with orange of a similar strength.","Tan, nude, white trainers, gold sandals.","Coral is especially flattering on warm and fair skin, and glows on deep skin.",[("#C1121F","Red"),("#FF1493","Hot pink")])
gw("sage","sage green","#8FBC8F",[("Cream","#F1E3C8","Soft and natural."),("White","#FFFFFF","Fresh and clean."),("Beige","#D8C3A5","Earthy, calm neutrals."),("Navy","#1F2A44","Grounded and smart."),("Blush pink","#E8B4B8","Soft pastels for spring."),("Brown","#6F4E37","Warm and earthy.")],
 "Avoid sage with bright neon colours or very saturated greens, which make it look dull.","White trainers, tan, brown or cream shoes.","Sage flatters fair and neutral skin especially. Deep skin looks lovely in it too, paired with white.",[("#CCFF00","Neon lime"),("#00C853","Bright green")])
gw("rust","rust","#B7410E",[("Cream","#F1E3C8","Warm and soft."),("Navy","#1F2A44","Rich contrast."),("Olive","#6B8E23","Earthy autumn palette."),("Denim","#577590","Easy casual."),("Camel","#C19A6B","Warm tonal look."),("Teal","#008080","Complementary contrast.")],
 "Avoid rust with red or pink, and with bright cool colours of the same strength.","Brown or tan leather, white trainers, suede boots.","Rust is perfect for warm and deep skin. Cool fair skin should try a softer terracotta or keep rust away from the face.",[("#C1121F","Red"),("#E6A8C3","Pink")])
gw("mint","mint green","#98D7C2",[("White","#FFFFFF","Fresh and clean."),("Navy","#1F2A44","Grounded and smart."),("Grey","#9E9E9E","Soft and modern."),("Denim","#577590","Casual summer."),("Lavender","#B39DDB","Pastel pairing."),("Coral","#F28C6B","Bright summer pop.")],
 "Avoid mint with neon green or yellow-green, and with beige close to your skin colour.","White trainers, grey, nude or silver shoes.","Mint suits cool and deep skin especially. Warm skin may prefer a warmer jade or pistachio.",[("#CCFF00","Neon lime"),("#DCC7AA","Nude")])
gw("charcoal","charcoal grey","#36454F",[("White","#FFFFFF","Sharp and classic."),("Light blue","#A3C4E0","The office staple."),("Pink","#E6A8C3","Soft and modern."),("Burgundy","#800020","Rich and polished."),("Camel","#C19A6B","Warm and elegant."),("Mustard","#E9C46A","A bold pop.")],
 "Avoid charcoal with black, which looks muddy, and with navy that's almost as dark.","Black, brown or burgundy leather, white trainers.","Charcoal is kinder than black on fair and olive skin, and works for every skin tone.",[("#111111","Black"),("#1F2A44","Dark navy")])
gw("royal-blue","royal blue","#2952CC",[("White","#FFFFFF","Crisp and bright."),("Black","#111111","Bold and graphic."),("Grey","#9E9E9E","Smart and calm."),("Camel","#C19A6B","Warm contrast."),("Orange","#F28C28","Complementary colour-block."),("Pink","#E6A8C3","Fresh and playful.")],
 "Avoid royal blue with navy of a similar strength, and with purple, which can clash.","White trainers, black, tan or grey shoes.","Royal blue is stunning on deep and cool skin, and flatters almost everyone.",[("#1F2A44","Navy"),("#6A4C93","Purple")])
for g in GOES_WITH[:7]:
    g.setdefault("avoid_cols", {"navy":[("#111111","Black"),("#1E3D2F","Dark green")],"black":[("#1F2A44","Navy"),("#3E2723","Dark brown")],
      "grey":[("#8B6B4A","Mid brown"),("#B0A99F","Greige")],"beige":[("#CCFF00","Neon lime"),("#DCC7AA","Skin-tone nude")],
      "olive-green":[("#CCFF00","Lime"),("#9E9E9E","Grey")],"brown":[("#9E9E9E","Mid grey"),("#111111","Black")],"burgundy":[("#FF0000","Bright red"),("#F28C28","Orange")]}[g["slug"]])

# register links (order = how they appear in "More colour guides")
for p in SKIN_PAGES: ALL_LINKS.append((p["fn"], p["label"]))
ALL_LINKS.append(("warm-vs-cool-undertone.html","Warm vs cool undertone"))
ALL_LINKS.append(("what-colours-go-together.html","What colours go together"))
for g in GOES_WITH: ALL_LINKS.append((f'what-colours-go-with-{g["slug"]}.html', f'What goes with {g["name"]}'))

# ---- write skin pages
for p in SKIN_PAGES:
    b = f'<p class="k">Colour guide</p><h1>{p["h1"]}</h1><div class="answer">{p["answer"]}</div>'
    b += '<a class="cta" href="./">Find your exact colours in 30 seconds →</a>'
    for h, t in p["sections"]: b += f"<h2>{h}</h2><p>{t}</p>"
    b += "<h2>Best colours by undertone</h2><p>Not sure which you are? <a href=\"warm-vs-cool-undertone.html\">Take the 4 quick tests</a>.</p>"
    for t, d, items in p["by_under"]:
        b += f'<div class="card"><h3 style="margin-top:0">{t}</h3><p style="margin:0;color:#5F5A54;font-size:16px">{d}</p>{swatches(items,p["skin"])}</div>'
    b += "<h2>Colours to be careful with</h2><ul>" + "".join(f"<li>{x}</li>" for x in p["avoid"]) + "</ul>"
    b += "<p>Love a colour that isn't on your list? Wear it away from your face, as trousers, shoes or a bag.</p>"
    b += "<h2>Easy outfit ideas</h2><ul>" + "".join(f"<li>{x}</li>" for x in p["outfits"]) + "</ul>"
    open(os.path.join(OUT,p["fn"]),"w").write(page(p["fn"],p["title"],p["desc"],b,p["faq"]))

# ---- write goes-with pages
for g in GOES_WITH:
    fn = f'what-colours-go-with-{g["slug"]}.html'
    N = g["name"]; Nc = N[0].upper()+N[1:]
    b = f'<p class="k">Colour matching</p><h1>What colours go with {N}?</h1><div class="answer"><b>Short answer:</b> {g["answer"]}</div>'
    b += f'<h2>{len(g["pairs"])} colours that go with {N}</h2><div class="card">'
    b += "".join(f'<div class="pair">{duo(g["hex"],h)}<div><b>{Nc} + {esc(n)}</b><span>{esc(t)}</span></div></div>' for n,h,t in g["pairs"])
    b += "</div>"
    b += f"<h2>Colours to avoid with {N}</h2><p>{esc(g['avoid'])}</p>"
    b += f"<h2>What shoes go with {N}?</h2><p>{esc(g['shoes'])}</p>"
    b += f"<h2>Does {N} suit your skin tone?</h2><p>{esc(g['skin'])} <a href=\"./\">Check your own colours</a>, then use the <b>Does it match?</b> tool to test any two colours on your skin.</p>"
    title = f"What Colours Go With {N.title()}? {len(g['pairs'])} Outfit Combinations | Wearhue"
    desc = f"What colours go with {N} clothes? {g['answer'].split('.')[0]}. Plus colours to avoid, shoes, and how it suits your skin tone."
    open(os.path.join(OUT,fn),"w").write(page(fn,title,desc[:300],b,g["faq"]))

# ---- undertone guide
b='''<p class="k">Colour guide</p><h1>Warm vs cool undertone: 4 easy ways to tell</h1>
<div class="answer"><b>Short answer:</b> if the veins on your wrist look green, gold jewellery suits you and you tan easily, you're probably <b>warm</b>. If your veins look blue or purple, silver suits you and you burn easily, you're probably <b>cool</b>. A mix of both means <b>neutral</b>.</div>
<p>Your <b>skin tone</b> is how light or dark your skin is, and it changes with a tan. Your <b>undertone</b> is the colour underneath, and it stays the same. Undertone is what decides whether golden or blue-based colours flatter you.</p>
<a class="cta" href="./">Do the 30-second test →</a>
<h2>1. The vein test</h2><p>In daylight, look at the veins on your inner wrist. <b>Green or olive</b> suggests warm. <b>Blue or purple</b> suggests cool. If you honestly can't decide, you're likely neutral. This is harder on deep skin, so lean on the other tests too.</p>
<h2>2. The jewellery test</h2><p>Hold gold and then silver against your skin, or think about which one people compliment. <b>Gold</b> looking better suggests warm, <b>silver</b> suggests cool, and both suggests neutral.</p>
<h2>3. The sun test</h2><p><b>Tan easily, rarely burn:</b> often warm. <b>Burn or go pink first:</b> often cool. This works best on lighter skin; deeper skin rarely burns, whatever the undertone.</p>
<h2>4. The white paper test</h2><p>Hold pure white paper next to your bare face in daylight. If your skin looks <b>yellow, golden or peachy</b> by comparison you're warm, <b>pink or rosy</b> means cool, and <b>neither</b> means neutral.</p>
<h2>What to wear for your undertone</h2>
<div class="card"><h3 style="margin-top:0">Warm</h3><p style="margin:0">Earthy and golden colours: terracotta, mustard, olive, rust, coral, teal, cream and camel. Gold jewellery.</p></div>
<div class="card"><h3 style="margin-top:0">Cool</h3><p style="margin:0">Blue-based and jewel colours: sapphire, emerald, berry, lavender, crisp white, grey and navy. Silver jewellery.</p></div>
<div class="card"><h3 style="margin-top:0">Neutral</h3><p style="margin:0">Most colours, especially mid-tones: dusty rose, jade, denim, plum and soft white. Gold or silver.</p></div>'''
faq=[("Am I warm or cool toned?","Check your wrist veins in daylight (green = warm, blue or purple = cool), see whether gold or silver suits you, and notice if you tan or burn. Mixed results usually mean neutral."),
     ("Can you have a neutral undertone?","Yes. Neutral undertones show signs of both warm and cool and can wear most colours, especially muted and mid-tone shades."),
     ("Does your undertone change with a tan?","No. A tan changes your skin tone (how dark you are) but not your undertone.")]
open(os.path.join(OUT,"warm-vs-cool-undertone.html"),"w").write(page("warm-vs-cool-undertone.html","Am I Warm or Cool Toned? 4 Easy Undertone Tests | Wearhue","How to tell if your undertone is warm, cool or neutral with four quick tests (veins, jewellery, sun and white paper), plus which colours to wear for each.",b,faq))

# ---- what goes together (hub)
combos=[("Navy + white","#1F2A44","#FFFFFF","The most reliable pairing in fashion."),("Black + camel","#111111","#C19A6B","Timeless and expensive-looking."),
        ("Olive + cream","#6B8E23","#F1E3C8","Earthy and relaxed; great for warm skin."),("Grey + burgundy","#9E9E9E","#800020","Polished and rich."),
        ("Light blue + tan","#A3C4E0","#C19A6B","Fresh and smart-casual."),("Terracotta + denim","#E07A5F","#577590","Warm meets cool: balanced and easy."),
        ("Emerald + white","#00875A","#FFFFFF","High contrast, stunning on deep skin."),("Pink + grey","#E6A8C3","#9E9E9E","Soft and modern.")]
pairs="".join(f'<div class="pair">{duo(a,c)}<div><b>{n}</b><span>{d}</span></div></div>' for n,a,c,d in combos)
gw="".join(f'<a href="what-colours-go-with-{g["slug"]}.html">{g["name"].capitalize()}</a>' for g in GOES_WITH)
b=f'''<p class="k">Colour matching</p><h1>What colours go together? A simple guide to matching clothes</h1>
<div class="answer"><b>Short answer:</b> pair one colour with neutrals (white, black, grey, navy, beige, denim), and keep outfits to 2–3 main colours. Colours next to each other on the colour wheel blend easily. Opposites (blue + orange, purple + yellow) make a bold statement.</div>
<a class="cta" href="./">Test any two colours on your skin →</a>
<h2>The 5 rules that cover almost every outfit</h2>
<h3>1. One colour + neutrals always works</h3><p>Pick one coloured piece (a green tee, a red jumper) and keep everything else neutral: white, black, grey, navy, beige, brown or denim.</p>
<h3>2. Stick to 2–3 colours</h3><p>More than three main colours usually looks unplanned. Neutrals and denim don't count towards the limit.</p>
<h3>3. Neighbouring colours blend</h3><p>Colours next to each other on the colour wheel, like blue + green or red + orange, look naturally harmonious.</p>
<h3>4. Opposites make a statement</h3><p>Complementary colours (blue + orange, purple + yellow, red + green) are bold. Make one the main colour and use the other as a small accent.</p>
<h3>5. Mix light and dark</h3><p>One lighter and one darker piece reads better than two colours of the same brightness, which can look flat.</p>
<h2>8 combinations that always work</h2><div class="card">{pairs}</div>
<h2>What goes with…</h2><div class="more">{gw}</div>
<h2>Then make sure it suits you</h2><p>Two colours can go together and still not flatter <i>you</i>. Wear your best colours near your face and the rest on your bottom half. <a href="./">Find your best colours free</a>.</p>'''
faq=[("What colours go together in an outfit?","One colour plus neutrals always works. Beyond that, neighbouring colours on the colour wheel blend naturally, and opposite colours make a bold statement when one is used as an accent."),
     ("How many colours should an outfit have?","Two to three main colours. Neutrals like white, black, grey, navy, beige and denim don't count towards that."),
     ("What colour goes with everything?","Neutrals: white, black, grey, navy, beige and denim go with almost any colour.")]
open(os.path.join(OUT,"what-colours-go-together.html"),"w").write(page("what-colours-go-together.html","What Colours Go Together? How to Match Clothes Colours | Wearhue","How to match clothing colours: 5 simple rules, 8 combinations that always work, and guides for navy, black, grey, beige, olive, brown and burgundy.",b,faq))

# ---- sitemap + robots
urls=[""]+[f for f,_ in ALL_LINKS]+["privacy.html"]
open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
print("pages:", len(urls))
