Feature: Preset image settings
  In order to refer to commonly used image thumbnail settings more easily
  I want to be able to use a name to refer to sets of thumbnail settings

  Scenario Outline: Fetch the URL for an image with pre-set settings
    Given I have an Image that refers to <path>
    And I have the following thumbnail presets:
      | name    | width | height | crop |
      | small   | 50    | 50     | 50%  |
      | sidebar | 300   |        | 50%  |
    When I ask for each preset thumbnail for the image
    Then each URL refers to an image with the appropriate settings

  Examples:
    | path              |
    | a.png             |
    | test.jpg          |
    | animated_meme.gif |
    | cute-kitten.jpeg  |

    
Feature: Preset defaults
  In order to simplify setting commonly used options
  I want to be able to specify default options that presets inherit unless overridden

  Scenario: Basic defaults

  Scenario: Override a default
