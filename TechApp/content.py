"""
Editable site content for SirBrams Tech Solutions.

Change contact details and the homepage numbers here. The portfolio is no
longer edited in this file: add, edit and hide work from the admin panel
(/admin/ > Portfolio). PROJECTS and DESIGNS below are only the starter
samples loaded by `python manage.py seed_portfolio`.
"""

SITE = {
    "email": "sirbrams.b@gmail.com",
    "phone": "+254 742 524 370",
    "phone_link": "+254742524370",
    "whatsapp_channel": "https://whatsapp.com/channel/0029Vb3HC8R7dmebd5Awqs2T",
    "site_url": "https://sirbrams-branding.onrender.com/",
}

# Top announcement bar. Set "enabled" to False to hide it.
ANNOUNCEMENT = {
    "enabled": True,
    "badge": "New",
    "text": "Now booking web and branding projects for early 2027.",
    "link_text": "Get a free consultation",
}

# Homepage counters. Each value is written into the HTML, so it never shows
# "0" if JavaScript is slow or blocked; the count-up animation is a bonus.
STATS = [
    {"icon": "bi-people", "value": 2, "suffix": "+", "title": "Clients served",
     "desc": "Businesses and organisations we have partnered with"},
    {"icon": "bi-check2-circle", "value": 5, "suffix": "+", "title": "Projects delivered",
     "desc": "Websites, systems and brand pieces shipped"},
    {"icon": "bi-emoji-smile", "value": 96, "suffix": "%", "title": "Client satisfaction",
     "desc": "Clients who would recommend us"},
    {"icon": "bi-headset", "value": None, "static": "24/7", "title": "Support available",
     "desc": "Critical issues are never left waiting"},
]

# Starter websites and systems (see note at the top of this file).
PROJECTS = [
    {
        "name": "SirBrams Tech Solutions",
        "industry": "Technology agency",
        "summary": "A fast, mobile-first agency site with enquiry emails to the team and an automatic reply to every visitor.",
        "stack": ["Django", "Brevo email", "PWA"],
        "url": "https://sirbrams-branding.onrender.com/",
        "tone": "navy",
    },
    {
        "name": "SirBrams Virtual Campus",
        "industry": "Education",
        "summary": "Online learning for schools and tutors: classes, materials and learner progress managed in one place.",
        "stack": ["Django", "Bootstrap"],
        "url": "",
        "tone": "green",
    },
    {
        "name": "Job Portal and CV Builder",
        "industry": "Employment",
        "summary": "Job listings, an automated CV builder and WhatsApp alerts so applicants hear about openings quickly.",
        "stack": ["Django", "WhatsApp alerts"],
        "url": "",
        "tone": "gold",
    },
    {
        "name": "School Management System",
        "industry": "Education",
        "summary": "Admissions, student records, parent portals, classroom tracking and exams in a single dashboard.",
        "stack": ["Django", "Bootstrap"],
        "url": "",
        "tone": "navy",
    },
]

# Starter graphic design pieces. "image" lives in static/assets/img/design/.
DESIGNS = [
    {"id": "kijani", "title": "Kijani Coffee logo", "type": "Logo", "image": "assets/img/design/logo-kijani.svg",
     "brief": "A friendly mark for a small-batch coffee roaster that sources from Kenyan highlands.",
     "notes": "Forest green for freshness, warm cream for packaging, one gold dot as the signature detail."},
    {"id": "card", "title": "Amani Legal business card", "type": "Business card", "image": "assets/img/design/card-amani.svg",
     "brief": "A calm, confident card for a boutique law practice.",
     "notes": "Deep navy with a gold monogram. Soft-touch laminate and gold foil recommended for print."},
    {"id": "flyer", "title": "School open day flyer", "type": "Flyer", "image": "assets/img/design/flyer-openday.svg",
     "brief": "Invite parents to an open day with the date, venue and one clear action.",
     "notes": "Large date block for scanning from a distance. Navy and gold keep it formal but warm."},
    {"id": "social", "title": "Fresh Harvest Friday post", "type": "Social poster", "image": "assets/img/design/social-harvest.svg",
     "brief": "A weekly social post for a farmers' market stall.",
     "notes": "Emerald and cream with a rounded sun shape. Works as a square post or a story crop."},
    {"id": "brand", "title": "Jikoni brand board", "type": "Brand identity", "image": "assets/img/design/brand-board.svg",
     "brief": "A starter identity for a neighbourhood kitchen: palette, type and a logo lockup.",
     "notes": "Sage green and warm cream with ink-navy text, kept simple so it prints well on menus and packaging."},
    {"id": "event", "title": "Garden wedding invitation", "type": "Invitation", "image": "assets/img/design/invite-garden.svg",
     "brief": "A light, botanical invitation with room for names, date and RSVP details.",
     "notes": "Soft mint background, thin gold line work and generous margins for a premium feel."},
]
