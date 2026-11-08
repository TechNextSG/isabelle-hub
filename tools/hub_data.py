"""Everything the hub lists. Groups render in this order; each item becomes one card."""

GROUPS = [
    ("sites", "Websites", "Isabelle's three live websites. Open a card's page list to jump straight to any page."),
    ("events", "Event pages & conference", "Stand-alone event pages and the TRE™ Worldwide Conference site."),
    ("brand", "Brand & design", "The brand guide, one brand kit per brand and the BHD Asia design preview."),
    ("plans", "Planning", "Isabelle's content and event schedule."),
]

ITEMS = [
    # websites (page lists come from tools/pages.json)
    dict(slug="hummingbeing", g="sites", title="HummingBeing", url="https://hummingbeing.com/",
         host="hummingbeing.com", status="Live", pages="hb",
         desc="TRE™ sessions, somatic coaching, retreats and Isabelle's events in Singapore, Europe and online."),
    dict(slug="bhdasia", g="sites", title="BHD Asia", url="https://bhdasia.com/",
         host="bhdasia.com", status="Live", pages="bhd",
         desc="Executive coaching, HR consulting and TRE™ resilience programmes for organisations, since 2012."),
    dict(slug="tre-singapore", g="sites", title="TRE™ in Singapore", url="https://tre-in-singapore.com/",
         host="tre-in-singapore.com", status="Live", pages="tre",
         desc="TRE™ provider certification, facilitators, events and the TRE™ blog."),
    # event pages
    dict(slug="tre-bali", g="events", title="TRE™ Worldwide Conference · Bali 2027",
         url="https://technextmarketing.github.io/tre-bali-conference/", host="Event website", status="Preview",
         desc="The conference website: programme, speakers, venue and ticket options."),
    dict(slug="tre-bali-showcase", g="events", title="Bali 2027 marketing showcase",
         url="https://technextmarketing.github.io/tre-bali-marketing-showcase/", host="Showcase", status="Preview",
         desc="How the conference is marketed: website, social content and the booking journey."),
    dict(slug="atelier-shaking", g="events", title="From Shaking to Shaping",
         url="https://technextsg.github.io/atelier-event-pages/detail-pages/event-shaking-to-shaping.html",
         host="Event page", status="Preview",
         desc="Atelier-style event page for the TRE™ in a coaching context workshop, Bucharest and online."),
    dict(slug="atelier-highlight", g="events", title="TRE® events highlight",
         url="https://technextsg.github.io/atelier-event-pages/events-highlight/events-highlight.html",
         host="Event section", status="Preview",
         desc="A ready-to-embed events section with a live countdown for From Shaking to Shaping and TRE® Module 1."),
    # brand & design
    dict(slug="bb-hummingbeing", g="brand", title="HummingBeing brand book",
         url="https://technextmarketing.github.io/hummingbeing/brand/index.html", host="Brand book", status="Live",
         desc="HummingBeing's story, voice, logo system, colour, type, photography, posters and downloads in one book."),
    dict(slug="bb-bhdasia", g="brand", title="BHD Asia brand book",
         url="https://technextmarketing.github.io/bhdasia/brand/index.html", host="Brand book", status="Live",
         desc="BHD Asia's story, voice, logo system, colour, type, photography, co-branding and downloads in one book."),
    dict(slug="bb-tre", g="brand", title="TRE™ in Singapore brand book",
         url="https://technextmarketing.github.io/tre-in-singapore/brand/index.html", host="Brand book", status="Live",
         desc="TRE™ in Singapore's story, voice, logo, colour, type, photography, events and downloads in one book."),
    # planning
    dict(slug="schedule", g="plans", title="Isabelle's schedule",
         url="https://technextmarketing.github.io/isabelle-schedule/", host="Calendar", status="Live",
         desc="Events, posts and videos by month, week or list, with filters and a detail view."),
]
