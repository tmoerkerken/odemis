import threading

from odemis.gui import main
from odemis.util.testing import start_backend

from behave import given, when, then

system_lookup = {
    # TODO not hardcode
    "SPARC FPLM": "/home/moerkerken/development/odemis/install/linux/usr/share/odemis/sim/sparc2-fplm-sim.odm.yaml"
}



@given('the backend runs with a simulated {system} microscope file')
def step_start_backend(context, system):
    # config = system_lookup[system]
    # start_backend(config)
    pass

@given('the GUI is started')
def step_start_gui(context):
    # def run_gui():
    #     context.gui = main.main([])

    # # TODO better error handling
    # gui_thread = threading.Thread(target=run_gui)
    # gui_thread.start()
    pass


@when('the mirror is engaged')
def step_start_gui(context):
    pass


@when('the mirror is not engaged')
def step_start_gui(context):
    pass


@then('the mirror is correctly positioned')
def step_start_gui(context):
    pass


@then('the following tabs shall be accessible')
def step_start_gui(context):
    pass


@then('the {tab} tab is {status}')
def step_start_gui(context, tab, status):
    pass
