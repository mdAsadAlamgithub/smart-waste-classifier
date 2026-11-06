RECOMMENDATIONS = {
    "plastic": {
        "title": "Plastic",
        "advice": "Empty and rinse the item, then place it in the dry or recyclable waste bin where plastic is accepted. Remove food residue first.",
    },
    "paper": {
        "title": "Paper",
        "advice": "Keep it dry and clean, and put it with paper recycling. Greasy or heavily soiled paper usually can't be recycled.",
    },
    "glass": {
        "title": "Glass",
        "advice": "Handle carefully. Rinse if possible and use a designated glass collection point. Wrap broken glass before disposal.",
    },
    "metal": {
        "title": "Metal",
        "advice": "Rinse cans and containers and send them for metal recycling. Scrap metal can often be sold to local scrap collectors.",
    },
    "cardboard": {
        "title": "Cardboard",
        "advice": "Flatten the box and keep it dry. Remove tape or plastic where possible, then send for cardboard recycling.",
    },
    "organic": {
        "title": "Organic waste",
        "advice": "Separate food scraps and put them in the wet waste bin, or compost them at home where possible.",
    },
}

OTHER = {
    "title": "Not a supported waste type",
    "advice": "This doesn't look like one of the supported categories. Medicines, batteries, electronics and chemicals need special handling, so follow local guidelines for hazardous or special waste.",
}

UNCERTAIN = {
    "title": "Not sure",
    "advice": "The model isn't confident about this photo. Retake it with one item, good lighting and a plain background.",
}

DISCLAIMER = "General guidance only. Follow your local waste collection rules."


def get_recommendation(label, status):
    if status == "uncertain":
        return UNCERTAIN
    if status == "other":
        return OTHER
    return RECOMMENDATIONS.get(label, OTHER)

import random  # noqa: F401  (used by app.py via ECO_TIPS)

CATEGORIES = [
    {"key": "plastic", "title": "Plastic", "emoji": "🧴", "color": "#2563eb",
     "examples": "Bottles, containers, packaging",
     "dos": ["Empty and rinse the item", "Crush bottles to save space", "Check local rules for caps and lids"],
     "donts": ["Don't burn plastic", "Don't recycle heavily food-soiled containers"]},
    {"key": "paper", "title": "Paper", "emoji": "📄", "color": "#d97706",
     "examples": "Newspapers, office paper, magazines",
     "dos": ["Keep it dry and clean", "Remove plastic covers or spiral binding", "Stack and tie bundles"],
     "donts": ["Don't recycle greasy or wet paper", "Don't mix tissues or used napkins with clean paper"]},
    {"key": "glass", "title": "Glass", "emoji": "🍾", "color": "#0891b2",
     "examples": "Bottles and jars",
     "dos": ["Rinse bottles and jars", "Wrap broken glass in paper before disposal", "Use a designated glass collection point"],
     "donts": ["Don't mix with ceramics, mirrors or window glass", "Don't put loose broken glass in bags"]},
    {"key": "metal", "title": "Metal", "emoji": "🥫", "color": "#64748b",
     "examples": "Aluminium cans, tins, scrap",
     "dos": ["Rinse cans and tins", "Crush cans to save space", "Sell larger scrap to local collectors"],
     "donts": ["Don't put pressurised or non-empty aerosol cans in normal bins", "Don't throw batteries in with metal waste"]},
    {"key": "cardboard", "title": "Cardboard", "emoji": "📦", "color": "#a16207",
     "examples": "Boxes, cartons, packaging",
     "dos": ["Flatten boxes", "Keep them dry", "Remove tape and plastic where possible"],
     "donts": ["Don't recycle grease-soaked parts (e.g. pizza box bottoms)", "Don't leave cardboard out in the rain"]},
    {"key": "organic", "title": "Organic", "emoji": "🍎", "color": "#16a34a",
     "examples": "Food scraps, fruit and vegetable waste",
     "dos": ["Use the wet waste bin or compost", "Drain liquids first", "Chop large scraps to compost faster"],
     "donts": ["Don't wrap food waste in plastic bags", "Avoid meat and dairy in simple home compost"]},
]
CATEGORY_MAP = {c["key"]: c for c in CATEGORIES}

ECO_TIPS = [
    "Rinsing containers before recycling helps keep a whole batch of recyclables clean.",
    "Separating wet and dry waste at home makes recycling much easier downstream.",
    "Flattening boxes and crushing cans saves space in your bin.",
    "Carry a reusable bag and bottle to reduce plastic waste at the source.",
    "Composting food scraps turns kitchen waste into useful soil.",
]