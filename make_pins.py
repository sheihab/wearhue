"""Generates ~200 unique Wearhue Pinterest pins + the posting schedule.
Outputs:
  pins/*.png                      1000x1500 pin images (served on the site)
  pin-schedule.json               every pin with its publish time (used by the daily feed robot)
  pinterest-csv/batch-XX.csv      backup: 10 pins per file for Pinterest "Bulk create Pins"
  pinterest-plan.csv              one-sheet overview of every pin (date, time, title, link)
Run: python3 make_pins.py   (needs playwright + chromium)"""
import asyncio, csv, os, json, datetime, html
from playwright.async_api import async_playwright
import gen_pages as G   # regenerates pages + gives colour data

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://sheihab.github.io/wearhue/"
B_SKIN, B_MATCH, B_STYLE = "Colours for your skin tone", "What colours go together", "Outfit colour palettes"
SYD = datetime.timezone(datetime.timedelta(hours=11))   # Sydney summer time (AEDT)
FIRST_DAY, LAST_DAY = datetime.date(2026, 11, 23), datetime.date(2027, 1, 30)
SLOTS = [(7, 30), (12, 30), (19, 30)]                   # morning, afternoon, evening (Sydney)
esc = html.escape
PINS = []
def add(**k): PINS.append(k)

SK = {"fair":"#EECDB6","medium":"#C08A63","olive":"#B08A5E","dark":"#5A3825"}
PG = {"fair":"best-colours-for-fair-skin.html","medium":"best-colours-for-medium-skin.html","olive":"best-colours-for-medium-skin.html","dark":"best-colours-for-dark-skin.html"}
KW = {"dark":"colours for dark skin, colors for brown skin, black skin outfits","medium":"colours for medium skin, tan skin outfits",
      "olive":"colours for olive skin, olive skin outfits","fair":"colours for pale skin, fair skin outfits"}
NEUTRAL_BOTTOMS = [("#1F2A44","Navy"),("#F1E3C8","Cream"),("#577590","Denim"),("#111111","Black"),("#D8C3A5","Beige"),("#9E9E9E","Grey")]

# ---------------------------------------------------------------- skin palettes
SKIN = [
 ("dark","warm","warm dark skin","Golden undertone · gold jewellery",[("#FFB703","Saffron"),("#FB8500","Tangerine"),("#D62828","Tomato red"),("#2A9D8F","Teal"),("#6A994E","Leaf green"),("#9B2226","Oxblood"),("#C9A227","Old gold"),("#FFF3E0","Warm white"),("#F4A261","Apricot")],[("#8B6B4A","Mid brown"),("#A0A0A0","Mid grey"),("#C2B280","Khaki"),("#E6E6FA","Pale lilac")]),
 ("dark","cool","cool dark skin","Blue or ashy undertone · silver",[("#0047AB","Cobalt"),("#FF1493","Hot pink"),("#00A86B","Jade"),("#7B2CBF","Violet"),("#DC143C","Crimson"),("#00B4D8","Cyan"),("#FFFFFF","Crisp white"),("#4361EE","Royal blue"),("#800080","Purple")],[("#8B6B4A","Mid brown"),("#B8860B","Dark mustard"),("#C2B280","Khaki"),("#DCC7AA","Nude")]),
 ("dark","neutral","dark brown skin","Bright, rich colours make deep skin glow",[("#E63946","Red"),("#FFB703","Sun yellow"),("#3A86FF","Bright blue"),("#8338EC","Violet"),("#06D6A0","Mint"),("#FF006E","Pink"),("#FFFFFF","White"),("#2A9D8F","Teal"),("#FB5607","Orange")],[("#7A6A53","Dull brown"),("#A0A0A0","Mid grey"),("#C2B280","Sand"),("#DCC7AA","Nude")]),
 ("medium","warm","warm medium skin","Golden undertone · tans easily",[("#E07A5F","Terracotta"),("#F2A541","Marigold"),("#6B8E23","Olive"),("#2A9D8F","Teal"),("#C1440E","Rust"),("#E9C46A","Mustard"),("#9C6644","Cinnamon"),("#F1E3C8","Cream"),("#BC4749","Brick")],[("#B0C4DE","Icy blue"),("#E0B0FF","Lavender"),("#F8F8FF","Stark white"),("#A7A9AC","Cool grey")]),
 ("medium","cool","cool medium skin","Rosy undertone · silver jewellery",[("#0F52BA","Sapphire"),("#50C878","Emerald"),("#8E44AD","Purple"),("#E0115F","Ruby"),("#4682B4","Steel blue"),("#DE5D83","Blush"),("#008080","Teal"),("#FFFFFF","White"),("#1F2A44","Navy")],[("#FF8C00","Orange"),("#DAA520","Goldenrod"),("#C19A6B","Camel"),("#808000","Olive")]),
 ("olive","neutral","olive skin","Earth & jewel tones are your sweet spot",[("#6B8E23","Olive"),("#E07A5F","Terracotta"),("#800020","Burgundy"),("#2A9D8F","Teal"),("#50C878","Emerald"),("#E9C46A","Mustard"),("#F1E3C8","Cream"),("#1F2A44","Navy"),("#C19A6B","Camel")],[("#FFFF99","Pale yellow"),("#D8C3A5","Beige"),("#CCFF00","Neon lime"),("#A7A9AC","Cool grey")]),
 ("fair","warm","warm fair skin","Peachy undertone · freckles & gold",[("#F28C6B","Coral"),("#F4A68C","Peach"),("#A8B26A","Pistachio"),("#5BAE9C","Turquoise"),("#C7714E","Terracotta"),("#E7C27D","Wheat"),("#C19A6B","Camel"),("#F3E7D3","Ivory"),("#2F3B59","Soft navy")],[("#000000","Harsh black"),("#DDE3EE","Icy grey"),("#C8A2C8","Cool lilac"),("#C2185B","Magenta")]),
 ("fair","cool","cool pale skin","Pink undertone · burns easily",[("#7FA7D9","Powder blue"),("#E6A8C3","Rose pink"),("#9C89B8","Lavender"),("#3E7CB1","Sapphire"),("#C94C7C","Raspberry"),("#7DB7A5","Jade mint"),("#B8577E","Berry"),("#2E3A59","Navy"),("#A9A9B3","Dove grey")],[("#E07A2F","Orange"),("#D4A017","Mustard"),("#C19A6B","Camel"),("#6B8E23","Olive")]),
 ("fair","neutral","fair neutral skin","Soft, muted shades never overpower",[("#E8A0A0","Dusty rose"),("#8FBC8F","Sage"),("#6C8EBF","Soft blue"),("#F4C095","Apricot"),("#5F9EA0","Teal grey"),("#D6A2AD","Mauve"),("#B39DDB","Soft violet"),("#F5F0E8","Off-white"),("#2F3E46","Slate")],[("#FF00FF","Neon magenta"),("#CCFF00","Neon lime"),("#FF6600","Neon orange"),("#FFFF66","Lemon")]),
]
for skin,und,label,sub,cols,avoid in SKIN:
    names = ", ".join(n for _,n in cols[:6]).lower()
    base_kw = f"{KW[skin]}, {und} undertone colours, colour analysis, what colours suit me"
    add(kind="grid", fn=f"{skin}-{und}-palette", a="Best colours for", b=label, sub=sub, chip=SK[skin], cols=cols, page=PG[skin], board=B_SKIN,
        title=f"Best colours for {label}: clothing colour palette",
        desc=f"The clothing colours that suit {label}: {names} and more. Save this palette for your next shop, then find your exact colours free in 30 seconds with Wearhue.", kw=base_kw)
    add(kind="outfits", fn=f"{skin}-{und}-outfits", a="Outfit ideas for", b=label, sub="Colour on top, neutral below", skin=SK[skin],
        outfits=[(cols[i], NEUTRAL_BOTTOMS[(i*2) % 6]) for i in (0,3,5)], page=PG[skin], board=B_SKIN,
        title=f"3 easy outfit ideas for {label}",
        desc=f"Easy outfits for {label}: {cols[0][1].lower()}, {cols[3][1].lower()} and {cols[5][1].lower()} tops with simple neutrals. Find the colours that flatter you most, free, on Wearhue.", kw=base_kw + ", outfit ideas")
    add(kind="dodont", fn=f"{skin}-{und}-wear-avoid", a="Wear this, not that", b=label, sub="What flatters you vs what washes you out", chip=SK[skin], good=cols[:6], bad=avoid, page=PG[skin], board=B_SKIN,
        title=f"Colours to wear and avoid with {label}",
        desc=f"Wear {names}. Avoid {', '.join(n for _,n in avoid).lower()} near your face; they wash {label} out. Get your full personal palette free on Wearhue.", kw=base_kw + ", colours to avoid")

# men's versions
for skin,label,cols in [("dark","dark skin",SKIN[2][4]),("medium","brown skin",SKIN[3][4]),("olive","olive skin",SKIN[5][4]),("fair","pale skin",SKIN[7][4])]:
    add(kind="grid", fn=f"mens-colours-{skin}-skin", a="Best colours for men", b=f"with {label}", sub="Shirts, knits & jackets that flatter you", chip=SK[skin], cols=cols, page=PG[skin], board=B_SKIN,
        title=f"Best colours for men with {label}",
        desc=f"The best shirt and jacket colours for men with {label}: {', '.join(n for _,n in cols[:5]).lower()} and more. Find your exact colours free on Wearhue.", kw=f"best colours for men with {label}, mens style, {KW[skin]}")
    add(kind="outfits", fn=f"mens-outfits-{skin}-skin", a="Men's outfit ideas", b=f"for {label}", sub="Easy shirt + trouser combinations", skin=SK[skin],
        outfits=[(cols[1], ("#1F2A44","Navy")), (cols[4], ("#D8C3A5","Beige")), (cols[6], ("#111111","Black"))], page=PG[skin], board=B_SKIN,
        title=f"Men's outfit ideas for {label}",
        desc=f"Three easy men's outfits for {label}, built on colours that flatter you. Check any shirt and trouser combo on your skin tone free with Wearhue.", kw=f"mens outfit ideas, mens outfits for {label}, mens colour combinations")

# undertones
UND = [("warm","warm undertones","Earthy & golden · gold jewellery",[("#E07A5F","Terracotta"),("#E9C46A","Mustard"),("#6B8E23","Olive"),("#C1440E","Rust"),("#F28C6B","Coral"),("#2A9D8F","Teal"),("#C19A6B","Camel"),("#F1E3C8","Cream"),("#9B2226","Oxblood")]),
       ("cool","cool undertones","Jewel & blue-based · silver jewellery",[("#0F52BA","Sapphire"),("#50C878","Emerald"),("#B8577E","Berry"),("#9C89B8","Lavender"),("#E0115F","Ruby"),("#1F2A44","Navy"),("#FFFFFF","Crisp white"),("#9E9E9E","Grey"),("#008080","Teal")]),
       ("neutral","neutral undertones","Muted mid-tones · gold or silver",[("#E8A0A0","Dusty rose"),("#3C9D5D","Jade"),("#577590","Denim"),("#A23B72","Plum"),("#EDAE49","Honey"),("#5F9EA0","Teal grey"),("#F5F0E8","Soft white"),("#6A4C93","Grape"),("#2F3E46","Slate")])]
for und,label,sub,cols in UND:
    kw = f"{und} undertone colours, warm vs cool undertone, am I warm or cool toned, colour analysis"
    add(kind="grid", fn=f"{und}-undertone-palette", a="Best colours for", b=label, sub=sub, chip="#C68B59", cols=cols, page="warm-vs-cool-undertone.html", board=B_SKIN,
        title=f"Best colours for {label}: clothing palette", desc=f"Have {label}? These clothing colours flatter you most: {', '.join(n for _,n in cols[:6]).lower()}. Not sure which you are? Take the free 30-second test on Wearhue.", kw=kw)
    add(kind="outfits", fn=f"{und}-undertone-outfits", a="Outfit ideas for", b=label, sub=sub, skin="#C68B59", outfits=[(cols[0],NEUTRAL_BOTTOMS[0]),(cols[1],NEUTRAL_BOTTOMS[2]),(cols[3],NEUTRAL_BOTTOMS[1])],
        page="warm-vs-cool-undertone.html", board=B_SKIN, title=f"Outfit ideas for {label}", desc=f"Three easy outfits built on colours that suit {label}. Find out if you're warm, cool or neutral free on Wearhue.", kw=kw)

add(kind="rows", fn="gold-or-silver-jewellery", a="Gold or silver?", b="Find your undertone", sub="The quickest undertone test there is",
    rows=[("Gold suits you","#D4AF37","Warm undertone",None),("Silver suits you","#C0C0C0","Cool undertone",None),("Both look good","#E0B097","Neutral undertone",None),("Green wrist veins","#6B8E4E","Warm",None),("Blue / purple veins","#5B6EAE","Cool",None),("Tan easily","#C68B59","Often warm",None),("Burn first","#E57373","Often cool",None)],
    page="warm-vs-cool-undertone.html", board=B_SKIN, title="Gold or silver jewellery? The easy undertone test",
    desc="Does gold or silver suit you? Gold = warm undertone, silver = cool, both = neutral. Plus the vein and sun tests. Take the full free undertone test on Wearhue.", kw="warm or cool undertone, gold or silver jewellery, undertone test")

# ---------------------------------------------------------------- what goes with X (29 colours x 4 designs)
for g in G.GOES_WITH:
    name, hx, slug = g["name"], g["hex"], g["slug"]
    pairs = [(n,h) for n,h,_ in g["pairs"]][:6]
    page = f"what-colours-go-with-{slug}.html"
    kw = f"what colours go with {name}, what goes with {name}, {name} outfit ideas, what colour shirt goes with {name} pants, colour combinations for clothes"
    lst = ", ".join(n.lower() for n,_ in pairs)
    Name = name[0].upper()+name[1:]
    add(kind="grid", fn=f"goes-with-{slug}-grid", a="What colours", b=f"go with {name}?", sub=f"{len(pairs)} combinations that always work", chip=hx, cols=[(h,n) for n,h in pairs], page=page, board=B_MATCH,
        title=f"What colours go with {name}? {len(pairs)} outfit combinations", desc=f"What to wear with {name}: {lst}. Plus shoes and colours to avoid. Check any colour pair on your skin tone free with Wearhue.", kw=kw)
    add(kind="rows", fn=f"goes-with-{slug}-pairs", a=f"{Name} outfit", b="colour combinations", sub="Save for your next outfit",
        rows=[(Name,hx,n,h) for n,h in pairs], page=page, board=B_MATCH,
        title=f"{Name} outfit colour combinations", desc=f"{Name} + {pairs[0][0].lower()}, {name} + {pairs[1][0].lower()}, {name} + {pairs[2][0].lower()} and more. Easy outfit colour pairings, plus a free tool to check any combo on your skin tone.", kw=kw)
    add(kind="outfits", fn=f"goes-with-{slug}-outfits", a="How to wear", b=name, sub="3 easy outfit ideas", skin="#B08A5E",
        outfits=[((hx,Name),(pairs[0][1],pairs[0][0])), ((pairs[1][1],pairs[1][0]),(hx,Name)), ((hx,Name),(pairs[3][1],pairs[3][0]))],
        page=page, board=B_MATCH, title=f"How to wear {name}: 3 outfit ideas", desc=f"Three easy ways to wear {name}: with {pairs[0][0].lower()}, {pairs[1][0].lower()} and {pairs[3][0].lower()}. See the full colour guide and test it on your skin tone free on Wearhue.", kw=kw + ", how to wear " + name)
    add(kind="dodont", fn=f"goes-with-{slug}-dos-donts", a=f"{Name}:", b="pair it, avoid it", sub="Colours that work, and two that don't", chip=hx, good=[(h,n) for n,h in pairs], bad=g.get("avoid_cols",[]), page=page, board=B_MATCH,
        title=f"What goes with {name} (and what doesn't)", desc=f"Pair {name} with {lst}. Avoid {', '.join(n.lower() for n,_ in g.get('avoid_cols',[]))}. Full guide plus a free outfit colour checker on Wearhue.", kw=kw + ", colours that don't go together")

# ---------------------------------------------------------------- combos & aesthetics
add(kind="rows", fn="8-combinations-always-work", a="8 colour combinations", b="that always work", sub="Save this for your next outfit",
    rows=[("Navy","#1F2A44","White","#FFFFFF"),("Black","#111111","Camel","#C19A6B"),("Olive","#6B8E23","Cream","#F1E3C8"),("Grey","#9E9E9E","Burgundy","#800020"),("Light blue","#A3C4E0","Tan","#C19A6B"),("Terracotta","#E07A5F","Denim","#577590"),("Emerald","#00875A","White","#FFFFFF"),("Pink","#E6A8C3","Grey","#9E9E9E")],
    page="what-colours-go-together.html", board=B_MATCH, title="8 clothing colour combinations that always work",
    desc="Navy + white, black + camel, olive + cream, grey + burgundy and more. Learn the 5 simple rules for matching clothes on Wearhue.", kw="colour combinations for clothes, what colours go together, outfit colour combinations, how to match clothes")
add(kind="rows", fn="mens-colour-combinations", a="Men's outfit colour", b="combinations", sub="Easy pairings for shirts & trousers",
    rows=[("Navy","#1F2A44","Light blue","#A3C4E0"),("Charcoal","#36454F","White","#FFFFFF"),("Olive","#6B8E23","Navy","#1F2A44"),("Beige","#D8C3A5","Black","#111111"),("Burgundy","#800020","Grey","#9E9E9E"),("Brown","#6F4E37","Light blue","#A3C4E0"),("Black","#111111","Grey","#9E9E9E"),("Camel","#C19A6B","Cream","#FFFDF7")],
    page="what-colours-go-together.html", board=B_MATCH, title="Men's outfit colour combinations: shirts & trousers",
    desc="Easy men's colour combinations: navy + light blue, olive + navy, beige + black, burgundy + grey and more. Never guess what shirt goes with your trousers again.", kw="mens outfit colour combinations, what shirt goes with what pants, mens colour matching")
add(kind="rows", fn="colours-go-with-everything", a="Colours that go", b="with everything", sub="The 8 neutrals every wardrobe needs",
    rows=[(n,h,"",None) for n,h in [("White","#FFFFFF"),("Black","#111111"),("Navy","#1F2A44"),("Grey","#9E9E9E"),("Beige","#D8C3A5"),("Camel","#C19A6B"),("Denim","#577590"),("Cream","#FFFDF7")]],
    page="what-colours-go-together.html", board=B_MATCH, title="Colours that go with everything: 8 wardrobe neutrals",
    desc="White, black, navy, grey, beige, camel, denim and cream go with almost any colour. Pair one bright piece with these and your outfit always works.", kw="colours that go with everything, neutral colours clothes, capsule wardrobe colours")
add(kind="rows", fn="colour-matching-rules", a="5 rules for matching", b="clothes colours", sub="Never guess again",
    rows=[("1. One colour + neutrals","#2A9D8F","always works",None),("2. Max 2–3 colours","#E07A5F","per outfit",None),("3. Neighbours blend","#3A86FF","blue + teal",None),("4. Opposites pop","#F28C28","as a small accent",None),("5. Mix light & dark","#1F2A44","not same brightness",None)],
    page="what-colours-go-together.html", board=B_MATCH, title="5 simple rules for matching clothes colours",
    desc="One colour plus neutrals, max 2–3 colours, neighbours blend, opposites pop, mix light and dark. The 5 rules that cover almost every outfit, explained on Wearhue.", kw="how to match clothes colours, colour matching rules, what colours go together")

AESTHETIC = [
 ("old-money","Old money","colour palette","Quiet, timeless & expensive-looking",[("#F1E3C8","Cream"),("#1F2A44","Navy"),("#C19A6B","Camel"),("#2E5E4E","Forest"),("#800020","Burgundy"),("#FFFFFF","White"),("#6F4E37","Chocolate"),("#9E9E9E","Grey"),("#D8C3A5","Beige")]),
 ("quiet-luxury","Quiet luxury","colour palette","Soft neutrals, no logos",[("#F5F0E8","Ivory"),("#D8C3A5","Oat"),("#B8B0A2","Greige"),("#C19A6B","Camel"),("#6F4E37","Mocha"),("#2B2B2B","Charcoal"),("#FFFFFF","White"),("#1F2A44","Navy"),("#8A7F72","Taupe")]),
 ("streetwear","Streetwear","colour palette","Neutral base, one loud accent",[("#111111","Black"),("#FFFFFF","White"),("#9E9E9E","Heather grey"),("#6B6B3A","Olive"),("#D8C3A5","Sand"),("#F28C28","Orange"),("#2952CC","Royal blue"),("#C1121F","Red"),("#36454F","Charcoal")]),
 ("summer","Summer outfit","colour palette","Light, fresh & bright",[("#FFFFFF","White"),("#A3C4E0","Sky blue"),("#F28C6B","Coral"),("#98D7C2","Mint"),("#FFD23F","Lemon"),("#F1E3C8","Linen"),("#008080","Teal"),("#E6A8C3","Pink"),("#577590","Denim")]),
 ("autumn","Autumn outfit","colour palette","Warm, earthy & rich",[("#B7410E","Rust"),("#E9C46A","Mustard"),("#6B8E23","Olive"),("#800020","Burgundy"),("#C19A6B","Camel"),("#6F4E37","Chocolate"),("#F1E3C8","Cream"),("#2E5E4E","Forest"),("#E07A5F","Terracotta")]),
 ("winter","Winter outfit","colour palette","Deep tones & crisp contrast",[("#111111","Black"),("#FFFFFF","Snow white"),("#1F2A44","Navy"),("#800020","Burgundy"),("#00875A","Emerald"),("#36454F","Charcoal"),("#C19A6B","Camel"),("#6A4C93","Plum"),("#9E9E9E","Grey")]),
 ("spring","Spring outfit","colour palette","Soft pastels & fresh greens",[("#E8B4B8","Blush"),("#B39DDB","Lavender"),("#8FBC8F","Sage"),("#FFE9A8","Butter"),("#A3C4E0","Powder blue"),("#FFFFFF","White"),("#F4C095","Peach"),("#98D7C2","Mint"),("#D8C3A5","Beige")]),
 ("earth-tones","Earth tone","colour palette","Natural, calm & warm",[("#6F4E37","Brown"),("#C19A6B","Camel"),("#6B8E23","Olive"),("#B7410E","Rust"),("#D8C3A5","Sand"),("#F1E3C8","Cream"),("#8A7F72","Taupe"),("#E9C46A","Ochre"),("#2E5E4E","Moss")]),
 ("wedding-guest","Wedding guest","colours that work","Elegant, never white",[("#00875A","Emerald"),("#1F2A44","Navy"),("#800020","Burgundy"),("#E8B4B8","Blush"),("#B39DDB","Lavender"),("#8FBC8F","Sage"),("#C9A227","Gold"),("#6A4C93","Plum"),("#008080","Teal")]),
 ("business-casual","Business casual","colour palette","Smart, simple & easy to mix",[("#1F2A44","Navy"),("#9E9E9E","Grey"),("#FFFFFF","White"),("#A3C4E0","Light blue"),("#D8C3A5","Khaki"),("#36454F","Charcoal"),("#800020","Burgundy"),("#C19A6B","Camel"),("#111111","Black")]),
 ("date-night","Date night","colour palette","Confident, warm & flattering",[("#111111","Black"),("#800020","Wine"),("#C1121F","Red"),("#00875A","Emerald"),("#1F2A44","Navy"),("#C9A227","Gold"),("#E8B4B8","Blush"),("#FFFFFF","White"),("#6A4C93","Plum")]),
 ("minimalist","Minimalist wardrobe","colour palette","Few colours, endless outfits",[("#FFFFFF","White"),("#111111","Black"),("#9E9E9E","Grey"),("#1F2A44","Navy"),("#D8C3A5","Beige"),("#C19A6B","Camel"),("#577590","Denim"),("#F1E3C8","Cream"),("#36454F","Charcoal")]),
 ("monochrome","Monochrome","outfit ideas","One colour, different shades",[("#0B1F3A","Deep navy"),("#1F3A5F","Navy"),("#3E6A99","Mid blue"),("#7FA7D9","Sky"),("#BFD7EA","Ice"),("#2E5E4E","Forest"),("#3C9D5D","Jade"),("#8FBC8F","Sage"),("#CFE8D5","Mint")]),
 ("pastel","Pastel","colour palette","Soft, sweet & spring-ready",[("#E8B4B8","Pink"),("#B39DDB","Lilac"),("#A3C4E0","Baby blue"),("#98D7C2","Mint"),("#FFE9A8","Butter"),("#F4C095","Peach"),("#D6A2AD","Mauve"),("#CFE8D5","Pistachio"),("#FFFFFF","White")]),
 ("christmas","Christmas outfit","colours","Festive without the costume",[("#800020","Burgundy"),("#00875A","Emerald"),("#C9A227","Gold"),("#FFFFFF","Snow white"),("#111111","Black"),("#C1121F","Red"),("#2E5E4E","Forest"),("#F1E3C8","Cream"),("#C0C0C0","Silver")]),
 ("beach","Beach & holiday","colour palette","Sun-ready brights & neutrals",[("#FFFFFF","White"),("#F1E3C8","Linen"),("#008080","Teal"),("#F28C6B","Coral"),("#FFD23F","Sunshine"),("#2952CC","Ocean blue"),("#98D7C2","Mint"),("#D8C3A5","Sand"),("#E6A8C3","Pink")]),
]
for slug,a,b,sub,cols in AESTHETIC:
    t = f"{a} {b}"
    kw = f"{t.lower()}, {a.lower()} outfits, {a.lower()} aesthetic, outfit colour palette, colour combinations for clothes"
    add(kind="grid", fn=f"aesthetic-{slug}", a=a, b=b, sub=sub, chip="#B08A5E", cols=cols, page="what-colours-go-together.html", board=B_STYLE,
        title=f"{t}: outfit colours to save", desc=f"The {t.lower()}: {', '.join(n for _,n in cols[:6]).lower()}. Mix any two and they work. Check how each colour suits your skin tone free on Wearhue.", kw=kw)
    add(kind="outfits", fn=f"aesthetic-{slug}-outfits", a=a, b="outfit ideas", sub=sub, skin="#B08A5E", outfits=[(cols[0],cols[1]),(cols[2],cols[3]),(cols[4],cols[5])],
        page="what-colours-go-together.html", board=B_STYLE, title=f"{a} outfit ideas: 3 colour combinations",
        desc=f"Three {a.lower()} outfit colour combinations: {cols[0][1].lower()} + {cols[1][1].lower()}, {cols[2][1].lower()} + {cols[3][1].lower()}, {cols[4][1].lower()} + {cols[5][1].lower()}. Find the colours that suit you free on Wearhue.", kw=kw + ", outfit ideas")

WELCOME = dict(kind="grid", fn="wearhue-find-your-colours", a="Find the colours", b="that love your skin", sub="Free · 30 seconds · no sign-up", chip="#A5714C",
    cols=[("#E07A5F","Terracotta"),("#2A9D8F","Teal"),("#E9C46A","Mustard"),("#0F52BA","Sapphire"),("#E6A8C3","Rose pink"),("#6B8E23","Olive"),("#800020","Burgundy"),("#F1E3C8","Cream"),("#1F2A44","Navy")],
    page="", board=B_SKIN, title="Find the clothing colours that suit your skin tone (free)",
    desc="Pick your skin tone or take a selfie, answer 3 quick questions, and get your best colours, outfit ideas and a 'does it match?' checker. Free, no sign-up, photos never leave your phone.",
    kw="colour analysis, what colours suit me, skin tone colours, best colours for my skin tone, free colour analysis")

# ---------------------------------------------------------------- rendering
def fs_big(b): return 86 if len(b) < 18 else 74 if len(b) < 24 else 64
HEAD = '<html><body style="margin:0"><div style="width:1000px;height:1500px;background:#F7F3EE;font-family:-apple-system,Segoe UI,Roboto,Helvetica,sans-serif;color:#1B1A19;display:flex;flex-direction:column;align-items:center;padding:86px 64px 70px;box-sizing:border-box">'
FOOT = ('<div style="margin-top:40px;display:flex;flex-direction:column;align-items:center;gap:10px"><div style="background:#1B1A19;color:#fff;border-radius:999px;padding:22px 44px;font-size:32px;font-weight:600">Find your colours free →</div>'
        '<div style="font-size:26px;color:#6F6A64">sheihab.github.io/wearhue</div></div></div></body></html>')
def head(p):
    return (f'<div style="font-family:Iowan Old Style,Palatino,Georgia,serif;font-size:58px;line-height:1.06;text-align:center">{esc(p["a"])}<br>'
            f'<span style="font-size:{fs_big(p["b"])}px">{esc(p["b"])}</span></div><div style="font-size:30px;color:#6F6A64;margin-top:20px;text-align:center">{esc(p["sub"])}</div>')
def chip(h, nm, size, skin, cross=False):
    x = '<div style="position:absolute;inset:0;background:linear-gradient(to top right,transparent calc(50% - 3px),rgba(255,255,255,.9) calc(50% - 3px),rgba(255,255,255,.9) calc(50% + 3px),transparent calc(50% + 3px))"></div>' if cross else ""
    sk = f'<div style="position:absolute;left:50%;bottom:-{size*0.28:.0f}px;width:{size*0.6:.0f}px;height:{size*0.6:.0f}px;border-radius:50%;background:{skin};transform:translateX(-50%)"></div>' if skin else ""
    return f'<div style="text-align:center"><div style="width:{size}px;height:{size}px;border-radius:{size//8}px;background:{h};position:relative;overflow:hidden;box-shadow:inset 0 0 0 2px rgba(0,0,0,.07)">{sk}{x}</div><div style="font-size:27px;margin-top:10px">{esc(nm)}</div></div>'
def figure(top, bottom, skin, w=200):
    st = 'stroke="rgba(0,0,0,.12)" stroke-width=".6"'
    return (f'<svg width="{w}" height="{int(w*1.7)}" viewBox="0 0 100 170"><circle cx="50" cy="20" r="14" fill="{skin}"/><rect x="45" y="32" width="10" height="8" fill="{skin}"/>'
            f'<path d="M28 42 Q50 36 72 42 L76 90 L24 90 Z" fill="{top}" {st}/><path d="M18 46 L28 42 L26 74 L17 72 Z" fill="{top}" {st}/><path d="M82 46 L72 42 L74 74 L83 72 Z" fill="{top}" {st}/>'
            f'<circle cx="21" cy="78" r="4" fill="{skin}"/><circle cx="79" cy="78" r="4" fill="{skin}"/><path d="M26 90 L74 90 L70 152 L53 152 L50 104 L47 152 L30 152 Z" fill="{bottom}" {st}/>'
            f'<rect x="27" y="152" width="20" height="9" rx="4" fill="#2B2B2B"/><rect x="53" y="152" width="20" height="9" rx="4" fill="#2B2B2B"/></svg>')
def render(p):
    k = p["kind"]
    if k == "grid":
        n = len(p["cols"]); size = 230 if n > 6 else 260
        body = f'<div style="display:grid;grid-template-columns:repeat(3,{size}px);gap:34px;margin:auto 0">' + "".join(chip(h,nm,size,p["chip"]) for h,nm in p["cols"]) + "</div>"
    elif k == "outfits":
        cells = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;background:#fff;border-radius:28px;padding:26px 10px 20px;width:272px;box-sizing:border-box">{figure(t[0],b[0],p["skin"])}<div style="font-size:25px;margin-top:12px;text-align:center;line-height:1.25"><b>{esc(t[1])}</b><br>+ {esc(b[1])}</div></div>' for t,b in p["outfits"])
        body = f'<div style="display:flex;gap:20px;margin:auto 0">{cells}</div>'
    elif k == "dodont":
        good = "".join(chip(h,nm,170,p["chip"]) for h,nm in p["good"])
        bad = "".join(chip(h,nm,170,p["chip"],cross=True) for h,nm in p["bad"])
        body = (f'<div style="margin:auto 0;display:flex;flex-direction:column;gap:24px;align-items:center"><div style="font-size:32px;font-weight:700;color:#2F7D5B">✓ Wear / pair with</div>'
                f'<div style="display:grid;grid-template-columns:repeat(3,170px);gap:18px 40px">{good}</div>'
                f'<div style="font-size:32px;font-weight:700;color:#B23A3A;margin-top:8px">✕ Go easy on</div><div style="display:flex;gap:34px;justify-content:center">{bad}</div></div>')
    else:  # rows
        many = len(p["rows"]) > 7; sq = 76 if many else 84; rows = ""
        for l1,h1,l2,h2 in p["rows"]:
            sw = f'<div style="display:flex;flex:none"><div style="width:{sq}px;height:{sq}px;background:{h1};border-radius:{"16px 0 0 16px" if h2 else "16px"};box-shadow:inset 0 0 0 2px rgba(0,0,0,.07)"></div>' + (f'<div style="width:{sq}px;height:{sq}px;background:{h2};border-radius:0 16px 16px 0;box-shadow:inset 0 0 0 2px rgba(0,0,0,.07)"></div>' if h2 else "") + '</div>'
            txt = f'<b>{esc(l1)}</b>' + (f' + <b>{esc(l2)}</b>' if h2 else (f'<span style="color:#6F6A64"> · {esc(l2)}</span>' if l2 else ""))
            rows += f'<div style="display:flex;align-items:center;gap:28px;background:#fff;border-radius:22px;padding:{14 if many else 16}px 26px;font-size:34px;width:800px;box-sizing:border-box">{sw}<div>{txt}</div></div>'
        body = f'<div style="display:flex;flex-direction:column;gap:{14 if many else 18}px;margin:auto 0">{rows}</div>'
    return HEAD + head(p) + body + FOOT

# ---------------------------------------------------------------- schedule
def interleave2(pins):
    groups = {}
    for p in pins: groups.setdefault(p["board"], []).append(p)
    rank = {"grid":0, "rows":1, "outfits":2, "dodont":3}
    for b in groups:   # spread each topic's 2-4 designs across the whole period
        groups[b] = [p for _,_,p in sorted(((rank[p["kind"]], i, p) for i,p in enumerate(groups[b])), key=lambda x: (x[0], x[1]))]
    keyed = []
    for b,l in groups.items():
        for i,p in enumerate(l): keyed.append(((i+0.5)/len(l), b, p))
    keyed.sort(key=lambda x: (x[0], x[1]))
    return [p for _,_,p in keyed]

TODAY_START = [datetime.datetime(2026, 11, 22, 15, 20, tzinfo=SYD), datetime.datetime(2026, 11, 22, 19, 30, tzinfo=SYD)]
def schedule(n):
    days = (LAST_DAY - FIRST_DAY).days + 1
    slots = TODAY_START + [datetime.datetime.combine(FIRST_DAY + datetime.timedelta(d), datetime.time(h, m), SYD) for d in range(days) for h,m in SLOTS]
    return [slots[round(i * (len(slots)-1) / max(1, n-1))] for i in range(n)]

async def main():
    os.makedirs(os.path.join(HERE, "pins"), exist_ok=True)
    for f in os.listdir(os.path.join(HERE, "pins")):
        if f.endswith(".png"): os.remove(os.path.join(HERE, "pins", f))
    async with async_playwright() as pw:
        br = await pw.chromium.launch(); pg = await br.new_page(viewport={"width":1000,"height":1500})
        for p in PINS:
            await pg.set_content(render(p))
            await pg.screenshot(path=os.path.join(HERE, "pins", p["fn"]+".png"), clip={"x":0,"y":0,"width":1000,"height":1500})
        await pg.set_content(render(WELCOME))
        await pg.screenshot(path=os.path.join(HERE, "pins", WELCOME["fn"]+".png"), clip={"x":0,"y":0,"width":1000,"height":1500})
        await br.close()
    os.makedirs(os.path.join(HERE, "pinterest-csv"), exist_ok=True)
    with open(os.path.join(HERE, "pinterest-csv", "test-welcome-pin.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
        w.writerow([WELCOME["title"], SITE+"pins/"+WELCOME["fn"]+".png", WELCOME["board"], "", WELCOME["desc"], SITE+"?utm_source=pinterest&utm_medium=pin&utm_campaign=welcome", "", WELCOME["kw"]])
    pins = interleave2(PINS); times = schedule(len(pins))
    rows = [dict(time=t.isoformat(), utc=t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
                 title=p["title"][:100], description=p["desc"][:500], keywords=p["kw"], board=p["board"],
                 image=f"{SITE}pins/{p['fn']}.png", link=SITE+p["page"], id=p["fn"]) for p,t in zip(pins, times)]
    json.dump(rows, open(os.path.join(HERE, "pin-schedule.json"), "w"), indent=1)
    with open(os.path.join(HERE, "pinterest-plan.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["#","Date (Sydney)","Time","Board","Title","Link","Image","Keywords"])
        for i,r in enumerate(rows,1):
            t = datetime.datetime.fromisoformat(r["time"])
            w.writerow([i, t.strftime("%a %d %b %Y"), t.strftime("%I:%M %p").lstrip("0"), r["board"], r["title"], r["link"], r["image"], r["keywords"]])
    d = os.path.join(HERE, "pinterest-csv"); os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if not f.startswith("test-"): os.remove(os.path.join(d, f))
    for b in range(0, len(rows), 10):
        with open(os.path.join(d, f"batch-{b//10+1:02d}.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"])
            for r in rows[b:b+10]:
                w.writerow([r["title"], r["image"], r["board"], "", r["description"], r["link"]+"?utm_source=pinterest&utm_medium=pin&utm_campaign="+r["id"], r["utc"], r["keywords"]])
    old = os.path.join(HERE, "pinterest-bulk.csv")
    if os.path.exists(old): os.remove(old)
    print(len(rows), "pins;", rows[0]["time"], "->", rows[-1]["time"])
asyncio.run(main())
