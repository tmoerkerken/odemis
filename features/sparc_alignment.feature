Feature: Sparc Alignment

    # @automated_until_then
    # Scenario: Verify mirror position after engage
    #     Given the backend runs with a simulated SPARC FPLM microscope file
    #     And the GUI is started
    #     When the mirror is engaged
    #     Then the mirror is correctly positioned


    # @automated
    # Scenario: Verify  engaged
    #     Given the backend runs with a simulated SPARC FPLM microscope file
    #     And the GUI is started
    #     When the mirror is engaged
    #     Then the following tabs shall be accessible:
    #         | Acquisition |
    #         | Analysis    |
    #         | Chamber     |
    #         | Alignment   |


    @automated
    Scenario Outline: Verify tab status before mirror engage
        Given the backend runs with a simulated SPARC FPLM microscope file
        And the GUI is started
        When the mirror is not engaged
        Then the <tab> tab is <status>

        Examples:
            | tab           | status        |
            | acquisition   | available     |
            | analysis      | available     |
            | chamber       | active        |
            | alignment     | not available |
