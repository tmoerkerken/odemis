TAG_WHITELIST = [
    "automated",
    "automated_until_then"
]


def before_scenario(context, scenario):
    tag_whitelist = set(TAG_WHITELIST)
    scenario_tags = set(scenario.tags)
    if tag_whitelist & scenario_tags:
        pass
    else:
        context.scenario.skip("Skip: Fully manual test")


def before_step(context, step):
    if ("automated_until_then" in context.tags
        and step.step_type == "then"):
        context.scenario.skip("Skip: Requires manual verification")
