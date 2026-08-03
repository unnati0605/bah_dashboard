def irrigation_recommendation(crop, eta, rainfall, deficit):

    if rainfall > eta:
        return (
            "🟢 No Irrigation Needed",
            "Rainfall is sufficient for the selected location."
        )

    if deficit > 50:
        return (
            "🔴 Irrigate Immediately",
            f"Apply approximately {deficit:.1f} mm irrigation."
        )

    if deficit > 20:
        return (
            "🟡 Moderate Irrigation",
            f"Apply approximately {deficit:.1f} mm irrigation."
        )

    return (
        "🟢 Soil Moisture Adequate",
        "No irrigation required today."
    )