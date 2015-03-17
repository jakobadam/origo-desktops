.. _introduction:

Introduction
============

.. _`Remote Desktop Services`: https://technet.microsoft.com/en-us/windowsserver/ee236407.aspx 

`Remote Desktop Services`_ (RDS) is a product Windows Server 2012 R2 bundled
product that brings native windows applications to any device
anywhere. The infrastructure of RDS consists of these
components:

#. Broker
#. Gateway
#. Web
#. License
#. Session Host
#. Database

Some of the components may reside on the same server, others not. In
addition, to get a working RDS solution, the following non-RDS
components are also needed:

#. Active Directory
#. Public DNS

To make things easy for you we have pre-baked an architecture, ready
to spin up; it's depicted below.

.. image:: /_static/rds-architecture.png

RDS Orchestrator helps orchestrate and spin up several RDS farms with
the architecture above. To do so is a four step process consisting of:

#. `Configuring Active Directory`_
#. `Uploading software`_
#. `Installing software`_
#. `Deploying farm`_

The different states of the farm are:

.. image:: /_static/rds-farm-states.png

To begin with, a farm is *open* for installing software. When all
software is installed, the farm can be *sealed*, preventing further
software modifications.

In practice, software is installed on a single RDS Session Host
server. The administrator can then test and adapt the farm to
feedback, and when finished, seal it and deploy it in multiple
instances to production.

Configuring Active Directory
============================

A required component of RDS is the Active Directory (AD). There are
two options for AD: either use the one bundled with RDS Orchestrator
or connect your existing AD.

In order to register new RDS servers and DNS entries in the AD you
*must* provide RDS Orchestrator with credentials for a user with
administrative rights to the AD.

The credentials are validated against the specified IP when submitting
the form; a screenshot of the form is shown below.

.. image:: /_static/rds-connect-active-directory.png

All administrative traffic between the RDS Orchestrator, the Active
Directory and the RDS Servers use Kerberos authentication.

.. TODO: What about the WEB UI when iframed in origo.io?
.. TODO: Currently user credentials are saved in cleartext. If
   possible, instead save a token!

Uploading software
==================

RDS Orchestrator includes a catalog of software to which new software
installers should be uploaded; supported installers can be of the
types MSI, EXE or BAT. The installers must run without any user input
during installation, allowing a completely automated installation of
all software on the RDS session host.

If the installer consists of multiple files it can be zipped before
uploading. After the ZIP is uploaded, the software is automatically
extracted, and a heuristic determines which file is the
installer. Executable files whose name contains 'install' or 'setup'
are prioritized first. If not present, the first of any executable is
chosen.

Installers might require additional arguments which you can supply
when uploading. As an example, the screenshot shows a silent install
flag `-ms` added to the Firefox package in order to suppress GUI
prompts during installation.

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

Installing software
===================

After you have uploaded a software package you install it on the farm
by clicking on the install button on the software packages page:

.. image:: /_static/rds-software-list.png

On the page there's a dropdown with your farms. To install software to
another of these farms first select it from that dropdown.

If the install process is unsuccessful you will get an option to view
the error message. You can then edit the software package
appropriately and re-run the installation.

Deploying farm
==============

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
