===================
nethserver-tancredi
===================

Download the latest version of Tancredi and prepare an RPM for NethServer.

API tests
---------

The test suite expects a clean system and removes existing data. **Do not run it
on a production system!**

After installing the ``nethserver-tancredi`` RPM enter the ``test/`` directory
under the package documentation directory and run the test suite: ::

    cd /usr/share/doc/nethserver-tancredi-*/test
    bash run.sh
