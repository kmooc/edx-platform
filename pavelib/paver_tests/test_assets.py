"""Unit tests for the Paver asset tasks."""

import ddt
from paver.easy import call_task
from mock import patch
from path import Path

from pavelib import assets
from .utils import PaverTestCase


@ddt.ddt
class TestPaverAssetTasks(PaverTestCase):
    """
    Test the Paver asset tasks.
    """
    @ddt.data(
        [""],
        ["--force"],
        ["--debug"],
        ["--system=lms"],
        ["--system=lms --force"],
        ["--system=studio"],
        ["--system=studio --force"],
        ["--system=lms,studio"],
        ["--system=lms,studio --force"],
    )
    @ddt.unpack
    def test_compile_sass(self, options):
        """
        Test the "compile_sass" task.
        """
        parameters = options.split(" ")
        system = []
        if "--system=studio" not in parameters:
            system += ["lms"]
        if "--system=lms" not in parameters:
            system += ["studio"]
        debug = "--debug" in parameters
        force = "--force" in parameters
        self.reset_task_messages()
        call_task('pavelib.assets.compile_sass', options={"system": system, "debug": debug, "force": force})
        expected_messages = []
        if force:
            expected_messages.append("rm -rf common/static/css/*.css")
        expected_messages.append("libsass common/static/sass")
        if "lms" in system:
            if force:
                expected_messages.append("rm -rf lms/static/css/*.css")
            expected_messages.append("libsass lms/static/sass")
            if force:
                expected_messages.append("rm -rf lms/static/css/*.css")
            expected_messages.append("libsass lms/static/themed_sass")
            if force:
                expected_messages.append("rm -rf lms/static/certificates/css/*.css")
            expected_messages.append("libsass lms/static/certificates/sass")
        if "studio" in system:
            if force:
                expected_messages.append("rm -rf cms/static/css/*.css")
            expected_messages.append("libsass cms/static/sass")
        self.assertEquals(self.task_messages, expected_messages)


@ddt.ddt
class TestPaverThemeAssetTasks(PaverTestCase):
    """
    Test the Paver asset tasks.
    """

    @classmethod
    def setUpClass(cls):
        with patch(
            "pavelib.assets.Env.env_tokens",
            {'COMPREHENSIVE_THEME_DIR': Path("/edx/app/edxapp/edx-platform/common/test/test-theme")}
        ):
            # Configure path for themes
            assets.configure_paths()
        super(TestPaverThemeAssetTasks, cls).setUpClass()

    @ddt.data(
        [""],
        ["--force"],
        ["--debug"],
        ["--system=lms"],
        ["--system=lms --force"],
        ["--system=studio"],
        ["--system=studio --force"],
        ["--system=lms,studio"],
        ["--system=lms,studio --force"],
    )
    @ddt.unpack
    def test_compile_theme_sass(self, options):
        """
        Test the "compile_sass" task.
        """
        parameters = options.split(" ")
        system = []

        if "--system=studio" not in parameters:
            system += ["lms"]
        if "--system=lms" not in parameters:
            system += ["studio"]

        debug = "--debug" in parameters
        force = "--force" in parameters

        self.reset_task_messages()
        call_task('pavelib.assets.compile_sass', options={"system": system, "debug": debug, "force": force})

        expected_messages = []

        if force:
            expected_messages.append("rm -rf common/static/css/*.css")
        expected_messages.append("libsass common/static/sass")

        if "lms" in system:
            # Test that first lms sass is compiled with overrides from partial
            if force:
                expected_messages.append(
                    "rm -rf /edx/app/edxapp/edx-platform/common/test/test-theme/lms/static/css/*.css",
                )
            expected_messages.append("libsass lms/static/sass")

            # Test that after compiling lms sass theme sass is compiled that overrides existing css if any
            if force:
                expected_messages.append(
                    "rm -rf /edx/app/edxapp/edx-platform/common/test/test-theme/lms/static/css/*.css",
                )
            expected_messages.append("libsass /edx/app/edxapp/edx-platform/common/test/test-theme/lms/static/sass")

        if "studio" in system:
            # Test that first cms sass is compiled with overrides from partial
            if force:
                expected_messages.append(
                    "rm -rf /edx/app/edxapp/edx-platform/common/test/test-theme/cms/static/css/*.css",
                )
            expected_messages.append("libsass cms/static/sass")

            # Test that after compiling cms sass theme sass is compiled that overrides existing css if any
            if force:
                expected_messages.append(
                    "rm -rf /edx/app/edxapp/edx-platform/common/test/test-theme/cms/static/css/*.css",
                )
            expected_messages.append("libsass /edx/app/edxapp/edx-platform/common/test/test-theme/cms/static/sass")

        self.assertEquals(self.task_messages, expected_messages)
