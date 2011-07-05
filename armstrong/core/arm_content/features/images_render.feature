Feature: Images can render themselves
  In order to easily render the visual representations of various content
    types from templates
  I want to be able to call a method to render a thumbnail

  Scenario Outline: Render a thumbnail
    Given I have an Image that refers to <path>
    And I have the following thumbnail presets:
      | name    | width | height | crop |
      | small   | 50    | 50     | 50%  |
      | sidebar | 300   |        | 50%  |
    When I render its small thumbnail
    Then I see an IMG tag

  Examples:
    | path              |
    | a.png             |
    | test.jpg          |
    | animated_meme.gif |
    | cute-kitten.jpeg  |
