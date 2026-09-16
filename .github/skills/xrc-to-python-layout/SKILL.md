---
name: xrc-to-python-layout
description: Convert an Odemis wxPython XRC layout from src/odemis/gui/xmlh/resources into a maintainable pure-Python component under src/odemis/gui/layout. Use when converting, migrating, replacing, or reviewing an XRC GUI definition.
---

# Convert an Odemis XRC layout to Python

Convert one XRC top-level window at a time. Preserve its behavior and externally
used interface, but do not mechanically reproduce every generated attribute.

## Inputs

Identify:

- The source XRC file under `src/odemis/gui/xmlh/resources`.
- The corresponding generated class in `src/odemis/gui/main_xrc.py`.
- The controller, dialog, or tab that constructs or inherits from that class.
- The target module under `src/odemis/gui/layout/components`.

Do not modify unrelated layouts.

## Investigation

Before editing:

1. Read the complete top-level XRC object being converted.
2. Inspect its generated class in `src/odemis/gui/main_xrc.py`.
3. Search the repository for every use of the generated class.
4. Search controllers and tests for widget attributes accessed on the layout.
5. For custom XRC classes, inspect their resource handlers in
   `src/odemis/gui/xmlh/xh_delmic.py`.
6. Inspect existing converted components for established layout patterns.

Create `self.<name>` attributes only for controls accessed outside the layout
class or required by wx lifecycle behavior. Keep purely structural panels,
sizers, labels, and spacers as local variables.

Do not expose every named XRC object merely because `pywxrc` generated an
attribute for it.

## Implementation

Create a class that inherits from the equivalent `wx.Panel`, `wx.Dialog`, or
`wx.Frame`.

The constructor must remain compatible with the existing call site. Use type
hints and build the layout immediately after initializing the wx base class.

Preserve all relevant XRC behavior:

- Parent-child hierarchy.
- Control classes and constructor arguments.
- Styles and extra styles.
- Initial size and minimum size.
- Sizer orientation and nesting.
- Proportions, borders, flags, spacers, and growable rows or columns.
- Labels, values, ranges, selections, tooltips, and icons.
- Foreground and background colours.
- Initial visibility and enabled state.
- Scrolling configuration.
- Control ordering.
- Custom-control registration behavior from `xh_delmic.py`.
- Explicit layout calls required before controllers access calculated state.

Use `hbox()` and `vbox()` from
`odemis.gui.layout.util.sizers` for box sizers so indentation shows the visual
hierarchy. Instantiate other sizer types directly.

Split large components into private builder methods corresponding to meaningful
visual sections. Do not create a method for every individual widget.

Use local variables for implementation details. Assign a widget to `self` only
when another module accesses it, a test requires it, or the class itself needs
it after construction.

Call `SetName` only when code actually uses the wx name at runtime, such as
through `FindWindowByName`. A name in XRC alone is not sufficient reason.

## Strings

Search `src/odemis/gui/layout/constants/strings.py` before adding a string.

- Reuse an existing constant when the same user-visible text already exists.
- Add a constant when text is shared by multiple layout modules.
- Keep layout-specific, one-off text in the component.
- Do not centralize empty labels, whitespace placeholders, axis symbols, or
  values whose meaning depends only on one widget.
- Preserve spelling, capitalization, punctuation, ellipses, and whitespace
  from the XRC unless the task explicitly changes the UI.

## Theme

Search `src/odemis/gui/layout/constants/theme.py` and `odemis.gui` constants
before adding theme data.

- Reuse existing semantic colours, font sizes, and spacing values.
- Add a theme value only when it is genuinely reusable by multiple layouts or
  represents an application-wide visual role.
- Keep one-off dimensions and spacing local to the component.
- Do not add a theme field for every literal found in an XRC file.
- Do not turn widget configuration such as control width, gauge margin, or a
  section-specific indent into global theme API without demonstrated reuse.
- Prefer an existing `odemis.gui` constant over duplicating its value.

Do not expand the theme object merely to eliminate all numeric or colour
literals.

## Documentation and style

Follow the repository's Python and docstring conventions.

- Give the class a short description of the represented layout.
- Do not include an `Attributes` section enumerating every widget.
- Document non-obvious compatibility requirements or wx behavior only.
- Use concise reStructuredText docstrings for functions and methods.
- Include `:param:` and `:return:` fields where useful, without repeating type
  information already present in annotations.
- Avoid decorative Unicode separators and generated-looking commentary.
- Comment only where the reason for a wx workaround is not apparent.

## Preview support

Add this guard to independently preview the component:

```python
if __name__ == "__main__":
    from odemis.gui.layout.util.preview import run_preview

    run_preview(ComponentClass)

Run it as a module:

python3 -m odemis.gui.layout.components.module_name

Use  ODEMIS_PREVIEW_SHOW_ALL=1  when hidden controls must be inspected.

## Wiring

After implementing the component:

1. Export it from  src/odemis/gui/layout/components/__init__.py .
2. Ensure it is available through  odemis.gui.layout  if that is the existing
import convention.
3. Replace the relevant generated XRC constructor or base class at its call
site.
4. Do not change unrelated call sites.
5. Keep the XRC source and generated class unless the task explicitly requests
their removal. They remain useful for comparison during the migration.

## Validation

Before finishing:

1. Verify every externally accessed widget attribute exists with the same name
and compatible control type.
2. Verify structural widgets that are not externally accessed remain local.
3. Compare the Python hierarchy and sizer options against the XRC.
4. Check hidden and disabled initial states.
5. Check custom controls against their XRC resource handlers.
6. Run the component preview and inspect resizing and scrolling.
7. Run the smallest relevant existing test.
8. Run:
9. Confirm no unused imports, copied attribute inventories, or unnecessary
additions to  theme.py  and  strings.py  remain.

Report any behavior that could not be reproduced exactly.
