hat-quickstart
==============

This repository contains a minimal working example that uses the `Hat-open
<https://hat-open.com/docs>`_ components for its infrastructure. The example
makes use of all ``hat-open`` components that interact with monitor and event
server, other components may be used optionally. To run, install the
requirements and run scripts in the ``playground/run`` directory.

Installation
------------

To install the dependencies, first install the packages contained in the
``requirements.<your_package_manager>.txt``. If your package manager is not
covered in the requirements, try either setting it up on your system (e.g.
pacman can be installed on Windows via the MSYS2 stack), or find equivalent
packages on the package manager you use.

Note: on Ubuntu and other distributions that use apt, yarn must be installed
using an alternate method, e.g. over npm or by adding a new apt repository.

After that, install the Python dependencies by calling::
    
    pip install -r requirements.pip.txt

Docker
~~~~~~

If nothing works, a Dockerfile is included that sets up a docker image with the
neccessary requirements. To use it, run::
    
    docker build . -t project-name

This will build the docker image that can be used to run containers. This is
done by calling::
    
    docker run -p host_port:vm_port -v /host/path:/vm/path project-name

This example uses the ``-p`` option that configures a mapping between the ports
on the host machine and the container, e.g. a mapping like ``9999:80`` would
serve whatever the container is serving at the port ``80`` on host machine's
port ``9999``.

The ``-v`` option configures a shared filesystem. This allows the container to
access any files stored under the given path (or in the subdirectories) and
vice versa, if container writes to a file under that directory, that will be
visible from the host machine. On some operating systems, problems concerning
user access privileges might arise, e.g. warnings being written when attempting
to delete shared files, this is normal and can be ignored.

For more information on how to use docker see the `Docker documentation
<https://docs.docker.com/get-started/>`_.

Building
--------

This repository uses doit as its build tool, make sure to call ``doit list`` to
check available tasks. Some functions require certain tasks to be executed
before they can run properly, e.g. calling ``doit js_view`` is necessary to be
able to access the graphical interface.

Usage
-----

This repository was meant to be used in the following way:

#. Download it from github
#. Rename any references from the generic project to the actual project name
   (e.g. ``src_py/project`` -> ``src_py_<your_actual_project_name>``)
#. Write implementations of
   `devices <https://hat-gateway.hat-open.com/gateway.html>`_,
   `modules <https://hat-event.hat-open.com/event.html>`_,
   and `adapters <https://hat-gui.hat-open.com/gui.html>`_ in the
   ``src_py/project`` directory
#. Write implementations of various
   `views <https://hat-gui.hat-open.com/gui.html#views>`_ in the
   ``src_js/views`` directory
#. Use the build tools to build the user interfaces (``doit js_view``) or any
   other neccessary resources
#. Run the system from different subdirectories of the ``playground``
   directory.
    - This directory also contains configurations to various hat components
      which may need to be adapted in cases different settings are needed or
      new modules/devices/adapters are implemented.
