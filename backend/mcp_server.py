from mcp.server.fastmcp import FastMCP
mcp = FastMCP("MindWell Policy Evidence")
SOURCES = [
{"title":"WHO Guidelines on Mental Health at Work (2022)","url":"https://www.who.int/publications/i/item/9789240053052","topics":"workplace stress employees managers organisational intervention","summary":"WHO guidance covers organisational interventions, manager and worker training, individual interventions and return-to-work support. Policy implication: assess workload and management practices, not only individual coping.","caveat":"Adapt guidance to local context; the page is not a local cost estimate."},
{"title":"WHO World Mental Health Report (2022)","url":"https://www.who.int/publications/i/item/9789240049338","topics":"public health mental health systems community counselling access prevention","summary":"WHO calls for comprehensive, community-based, rights-oriented mental health systems, including promotion, prevention and accessible care. Wellbeing programmes should complement professional services.","caveat":"Broad system report; does not estimate local programme effects or costs."},
{"title":"WHO: Doing What Matters in Times of Stress","url":"https://www.who.int/publications/i/item/9789240003927","topics":"stress management mindfulness grounding general public","summary":"A practical guide provides stress-management skills for the general public and can inform optional low-intensity educational materials.","caveat":"A self-help guide alone does not prove a particular programme will work at scale."},
{"title":"WHO/UNESCO: Making Every School a Health-Promoting School","url":"https://www.who.int/publications/i/item/9789240025073","topics":"schools students teachers wellbeing school health","summary":"Promotes a whole-school approach rather than isolated activities. Link wellbeing work to school climate, staff capacity, families and referral pathways.","caveat":"Use age-appropriate safeguarding, consent and locally suitable delivery."},
{"title":"NICE: Depression in Adults—Treatment and Management","url":"https://www.nice.org.uk/guidance/ng222","topics":"depression clinical psychological intervention professional care","summary":"Clinical guidance describes treatment options in defined contexts. Do not present a general wellbeing session as treatment for depression.","caveat":"Recommendations are indication-specific; avoid generalising beyond the source."}
]
@mcp.tool()
def search_policy_evidence(query: str) -> dict:
    """Search curated public-health evidence. Returns source titles, URLs, summaries and caveats. Call before drafting policy recommendations."""
    words = [w.lower().strip(".,?!:;") for w in query.split() if len(w) > 3]
    ranked = []
    for source in SOURCES:
        text = (source["title"] + " " + source["topics"] + " " + source["summary"]).lower()
        score = sum(w in text for w in words)
        if score: ranked.append((score, source))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return {"query": query, "catalogue_size": len(SOURCES), "results": [s for _,s in ranked[:4]] or SOURCES[:3]}
if __name__ == "__main__":
    mcp.run(transport="stdio")
