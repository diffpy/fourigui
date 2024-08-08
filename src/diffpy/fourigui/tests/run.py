#!/usr/bin/env python
##############################################################################
#
# (c) 2024 The Trustees of Columbia University in the City of New York.
# All rights reserved.
#
# File coded by: Billinge Group members and community contributors.
#
# See GitHub contributions for a more detailed list of contributors.
# https://github.com/diffpy/fourigui/graphs/contributors
#
# See LICENSE.rst for license information.
#
##############################################################################
"""Convenience module for executing all unit tests with
python -m diffpy.fourigui.tests.run
"""

if __name__ == "__main__":
    import sys

    # show warnings by default
    if not sys.warnoptions:
        import os
        import warnings

        warnings.simplefilter("default")
        # also affect subprocesses
        os.environ["PYTHONWARNINGS"] = "default"
    import diffpy.fourigui.tests.integration_test as integration_test
    import diffpy.fourigui.tests.unit_test as unit_test

    # produce zero exit code for a successful test
    sys.exit(
        (not integration_test.main().wasSuccessful())
        or (not unit_test.main().wasSuccessful())
    )


# Consider upgrading to pytest
# import sys
#
# import pytest
#
# if __name__ == "__main__":
#     # show output results from every test function
#     args = ["-v"]
#     # show the message output for skipped and expected failure tests
#     if len(sys.argv) > 1:
#         args.extend(sys.argv[1:])
#     print("pytest arguments: {}".format(args))
#     # call pytest and exit with the return code from pytest
#     exit_res = pytest.main(args)
#     sys.exit(exit_res)

# End of file
