Feature: Sparc Alignment

@automated
Scenario: Verify the alignment tab is unaccessible when mirror in not engaged
    Given the backend runs with a simulated SPARC FPLM microscope file
    And the GUI is started
    When the mirror is engaged
#     Then alignment tab is unaccessible

# @automated
# Scenario: Verify the alignment tab is accessible when mirror is engaged
#     Given the backend runs with a simulated SPARC FPLM microscope file
#     When the GUI is started
#     And the mirror is engaged
#     Then alignment tab is accessible
