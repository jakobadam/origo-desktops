.. _introduction:

Introduction
============

.. _`Remote Desktop Services`: https://technet.microsoft.com/en-us/windowsserver/ee236407.aspx 

`Remote Desktop Services`_ (RDS) is a Windows Server 2012 R2 bundled
product that brings native windows applications to any device
anywhere. The infrastructure of RDS consists of quite a few
components:

#. Broker
#. Gateway
#. Web
#. License
#. Session Host
#. Database

It's possible to place some of the components on the same server,
others, e.g., broker and database, not! In addition, the get a working
RDS solution, the following non-RDS components are also needed:

#. Active Directory
#. Public DNS

To make things easy for you we have pre-baked an opinionated
architecture, ready to spin up; it's depicted below.

.. image:: /_static/rds-architecture.png

RDS Orchestrator helps orchestrate and spin up several RDS farms with
the architecture above. Initially to do so is a four step process
consisting of:

#. `Configuring Active Directory`_
#. `Uploading software`_
#. `Installing software to farm`_
#. `Start farm`_

Underneath the different states of the farm is depicted:

.. image:: /_static/rds-farm-states.png

Initially a farm is *open* for installing software. When all
software is installed, the farm can be *sealed*. In practice,
software is installed on a single server, and when finished, the disk
on that server is sealed and thereafter used as a base for all future
RDS Session Hosts on the farm.

Configuring Active Directory
============================

A required component of RDS is the Active Directory (AD). There are
two options for AD: either use the one bundled with RDS Orchestrator
or connect to your existing AD.

In order to register new RDS servers and DNS entries in the AD you
*must* provide RDS Orchestrator with credentials for a user with
administrative rights to the AD.

The credentials are validated against the specified IP when submitting
the form; a screenshot of the form is shown below.

.. image:: /_static/rds-connect-active-directory.png

All administrative traffic between the RDS Orchestrator, the Active
Directory and the RDS Servers use Kerberos, avoiding passing
credentials around in the clear.

.. TODO: What about the WEB UI when iframed in origo.io?
.. TODO: Currently user credentials are saved in cleartext. If
   possible, instead save a token!

Uploading software
==================

RDS Orchestrator includes a catalog of software to which new software
installers should be uploaded; supported installers can be of the
types MSI, EXE or BAT. These installers *must* be able to run
without any user input during installation. The point is to completely
automate installation of all software on the RDS session host.

If the installer consists of multiple files it *must* be zipped,
before uploading. After the ZIP is uploaded, the software is
extracted, and a qualified guess on which file is the installer is
made. Executable files which name contains 'install' or 'setup' are
prioritized first. If not present, the first of any executable is
chosen.

Installers might require additional arguments. This can be put into
`args` when adding or updating a software package; e.g., in the
screenshot below a silent install flag `-ms` is added to the Firefox
package in order to avoid any GUI prompts during installation -- a GUI
which is not available during the automated setup.

.. image:: /_static/rds-software-add.png

Sometimes the argument refers to a file next to the installer, in
which case, the variable `{dirname}` can be used. The args argument
then looks like:

::

    TRANSFORMS="{dirname}/transform.mst"

Arbitrary tweaks are possible by supplying an `install.bat`. The
following install file copies all files from its location including
sub-directories from the software catalog to the server. The code
makes uses of the Windows batch variable `%~dp0` to get the absolute
dirname path of `install.bat`:

::

    set DIR="%ProgramFiles(x86)%\MyProgram"
    md %DIR%
    xcopy %~dp0* %DIR% /s /e

Installing software to farm
=======================

After you have uploaded a software package you install it on the farm
by clicking on the install button on the software packages page. Here's a
screenshot of it:

.. image:: /_static/rds-software-list.png

On the page there's a dropdown with your farms. To install software to
another of these farms first select it from that dropdown.

If the install process is un-successful you will get an option to view
the error message, you can then edit the software package
appropriately and then re-run the installation for the specific
erroneous software packages.

Start farm
=========

When your required software is installed successfully on the farm, the
next step is to start the farm; this process shuts down the server
which had the software installed and seals the disk image. That image
is then used as base for spinning up RDS Session Hosts.

Configuring farm
================

Per default all users in the AD have access to applications published
in RDS. If you want to restrict the users which have access, you can
configure RDS to only allow connections from users belonging to a
specific user group in the AD.

.. image:: /_static/rds-farm-properties.png

Farm Servers
============

Overview of the servers in a farm:

.. image:: /_static/rds-farm-servers.png

