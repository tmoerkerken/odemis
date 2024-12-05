def before_scenario(context, scenario):
    if "automated" in scenario.tags:
        pass
    else:
        context.scenario.skip("manual test.")
