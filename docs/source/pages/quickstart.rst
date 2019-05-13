Quickstart
==========

Installation
------------

PyBunpro can be installed as follows using pip::

   $ pip install pybunpro

Usage
-----

First, we need to import and instantiate an instance of the client with your API key.
See the `Bunpro API docs <https://www.bunpro.jp/api>`_ to get your API key.

.. code-block:: python

   from pybunpro import BunproClient

   api_key = '<your_bunpro_api_key>'
   client = BunproClient(api_key)

PyBunpro includes methods for each endpoint, offering optional parameters when available.

.. code-block:: python
   
   user_information, study_queue = client.study_queue()

   # Get a maximum of 15 recent items. If omitted, the Bunpro API defaults to 10 items.
   user_information, recent_items = client.recent_items(limit=15)

Each function returns a tuple where the first member is the calling user's information followed by
the requested resource.

For details on the properties available on these objects, please refer to the :ref:`pybunpro-api-docs`.

API Errors
^^^^^^^^^^

When an API errors occurs, PyBunpro raises a ``BunproAPIError``.

.. code-block:: python

   try:
       user_information, study_queue = client.study_queue()
   except BunproAPIError as e:
       logger.error(e.status_code) # The response HTTP error code
       logger.error(e.errors) # A list of error messages from the API response    

In the case where PyBunpro cannot parse the response, a ``SchemaError`` is raised.
This is unlikely, but please refer to the :ref:`pybunpro-api-docs` for the structure of this error.
