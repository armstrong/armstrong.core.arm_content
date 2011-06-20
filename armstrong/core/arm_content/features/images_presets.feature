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
    Then each thumbnail has the specified settings

  Examples:
    | path              |
    | a.png             |
    | test.jpg          |
    | animated_meme.gif |
    | cute-kitten.jpeg  |

    
  Scenario Outline: Basic defaults
    Given I have an Image that refers to <path>
    And I have a default preset quality of 100
    And I have the following thumbnail presets:
      | name    | width | height | crop |
      | small   | 50    | 50     | 50%  |
      | sidebar | 300   |        | 50%  |
    When I ask for each preset thumbnail for the image
    Then each thumbnail has the specified settings
    And each thumbnail has a quality of 100

  Examples:
    | path              |
    | a.png             |
    | test.jpg          |
    | animated_meme.gif |
    | cute-kitten.jpeg  |

  Scenario Outline: Override a default
    Given I have an Image that refers to <path>
    And I have a default preset quality of 100
    And I have the following thumbnail presets:
      | name              | width | height | crop | quality |
      | small             | 50    | 50     | 50%  |         |
      | small_low_quality | 50    | 50     | 50%  | 25      |
      | sidebar           | 300   |        | 50%  |         |
    When I ask for each preset thumbnail for the image
    Then each thumbnail has the specified settings
    And the thumbnails without specified quality settings have a quality of 100

  Examples:
    | path              |
    | a.png             |
    | test.jpg          |
    | animated_meme.gif |
    | cute-kitten.jpeg  |

  Scenario Outline: Fetch the original image
    Given I have an Image that refers to <path>
    And I have the following thumbnail presets:
      | name    | width | height | crop |
      | small   | 50    | 50     | 50%  |
      | sidebar | 300   |        | 50%  |
    When I ask for the original thumbnail for the image
    Then the returned thumbnail is the original image

  Examples:
    | path              |
    | a.png             |
    | test.jpg          |
    | animated_meme.gif |
    | cute-kitten.jpeg  |
