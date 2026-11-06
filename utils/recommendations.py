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