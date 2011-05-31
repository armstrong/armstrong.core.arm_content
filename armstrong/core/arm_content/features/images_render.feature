Feature: Images can render themselves
  In order to easily render the visual representations of various content
    types from templates
  I want to be able to call a method to render a thumbnail

  Scenario Outline: Render a thumbnail
    Given I have an Image that refers to <path>
    When I render its thumbnail
    Then I see an IMG tag
    And I see a tag with a src attribute that ends with <path>

  Examples:
    | path              |
    | a.png             |
    | test.jpg          |
    | animated_meme.gif |
    | cute-kitten.jpeg  |
