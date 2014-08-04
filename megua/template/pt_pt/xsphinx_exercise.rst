
.. code-block:: python

   meg.save(r'''

.. code-block:: html

   %SUMMARY {{ sections_text }}
{{ summary }}



.. code-block:: html

   %PROBLEM {{ suggestive_name }}
{{ problem }}


.. code-block:: html

   %ANSWER
{{ answer }}


.. code-block:: python

{{ sage_python }}

.. code-block:: python

   ''')


{#
.. code-block:: python

   meg.save(r'''

   %SUMMARY {{ sections_text }}
    {{ summary }}

   %PROBLEM {{ suggestive_name }}
    {{ problem }}

   %ANSWER
    {{ answer }}

   {{sage_python}}

   ''')
#}

{#

**Sumário**

.. code-block:: latex

{{ summary }}


**Problema**

.. code-block:: latex

{{ problem }}


**Resolução**

.. code-block:: latex

{{ answer }}

**Sage/Python**

.. code-block:: python

{{ sage_python }}

#}



