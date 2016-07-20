=============================
HR Payslip Change State
=============================

This module introduces the following features:
* The module payroll_cancel allows change the state of many payslips form the
    tree view
* The module checks if the require state is allowed for each payslip
* If the required state is not allowed the paylip reamins without any changes

Installation
============

It depends on hr_payroll_cancel. There is a pull request here:
https://github.com/OCA/hr/pull/247

Configuration
=============

No needed.

Usage
=====
1. Go to the payslip list and select the ones you want to cancel.
2. Unfold the "More" menu on the top
3. Select the required state
4. To compelte the request, click on "Execute" button.