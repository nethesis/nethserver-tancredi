===================
nethserver-tancredi
===================

Download the latest version of `Tancredi <https://nethesis.github.io/tancredi/>`_
and prepare an RPM for NethServer.

API tests
---------

The test suite expects a clean system and removes existing data. **Do not run it
on a production system!**

After installing the ``nethserver-tancredi`` RPM enter the ``test/`` directory
under the package documentation directory and run the test suite: ::

    cd /usr/share/doc/nethserver-tancredi-*/test
    bash run.sh

PHP upload mitigation
---------------------

The Tancredi PHP-FPM pool disables ``session.upload_progress.enabled`` and
``file_uploads`` using administrator flags. Apache rejects ``multipart/*``
requests to both ``/provisioning`` and ``/tancredi/api/v1`` with HTTP 403 before
PHP parses the body. File upload settings alone do not disable multipart parsing.
Each PHP-FPM worker serves one request and then exits (``pm.max_requests = 1``),
so no state can leak from one request to the next.

This also disables legitimate multipart forms and uploads of provisioning assets.
URL-encoded forms, JSON API requests, and provisioning downloads remain available.
After installing the updated RPM, run ``signal-event nethserver-tancredi-update``
to regenerate the configuration and restart PHP-FPM. Verify multipart rejection
on both routes and normal provisioning/API behavior on a test instance.
