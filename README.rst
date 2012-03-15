armstrong.core.arm_content
==========================
Provides the foundation for all content inside Armstrong.

Usage
-----
You can use ``armstrong.core.arm_content`` to build out the custom models of
your site while following the DRY (Don't Repeat Yourself) principle.  It is the
foundation that the rest of the Armstrong content types are built off of.

For more information, please see the `full documentation`_.

.. change this link to point to docs inside docs.armstrongcms.org once its done
.. _full documentation: http://armstrong.github.com/armstrong.core.arm_content/

Installation & Configuration
----------------------------
You can install the latest release of ``armstrong.core.arm_content`` using
`pip`_:

::

    pip install armstrong.core.arm_content

You don't need to add ``armstrong.core.arm_content`` to your installed apps
unless you want to use the include template tags.  You can add it like this:

::

	INSTALLED_APPS += ["armstrong.core.arm_content", ]

Note that you do not need to run ``syncdb`` or ``migrate`` after installing
``armstrong.core.arm_content`` as it does not have any models.

.. _pip: http://www.pip-installer.org/


State of Project
----------------
Armstrong is an open-source news platform that is freely available to any
organization.  It is the result of a collaboration between the `Texas Tribune`_
and `Bay Citizen`_, and a grant from the `John S. and James L. Knight
Foundation`_.

To follow development, be sure to join the `Google Group`_.

``armstrong.core.arm_content`` is part of the `Armstrong`_ project.  You're
probably looking for that.


.. _Armstrong: http://www.armstrongcms.org/
.. _Bay Citizen: http://www.baycitizen.org/
.. _John S. and James L. Knight Foundation: http://www.knightfoundation.org/
.. _Texas Tribune: http://www.texastribune.org/
.. _Google Group: http://groups.google.com/group/armstrongcms


License
-------
Copyright 2011-2012 Bay Citizen and Texas Tribune

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
