Web dashboard
=======================================


Admin features and RESTful API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: password
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: RESTful

..py:function:: index()
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: admin
    :members:
    :undoc-members:
    :show-inheritance:

. <form action="/booklist" class="form-inline" method="post">
        {{ form.hidden_tag() }}
        {{ form.name(class='form-control', placeholder='Book Name')}}
        {{ form.author(class='form-control', placeholder='Author') }}
        {{ form.catalogue(class='form-control', placeholder='Catalogue')}}
        {{ form.code(class='form-control', placeholder='ISBN code ')}}
        {{ form.submit(class='btn btn-small btn-success')}}


Generate CLOUD data visualisation report
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: data
    :members:
    :undoc-members:
    :show-inheritance:

..py:function:: bookreport()
    :members:
    :undoc-members:
    :show-inheritance:


