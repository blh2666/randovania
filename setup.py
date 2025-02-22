from setuptools import setup
from setuptools.command.build_py import build_py

try:
    from pyqt_distutils.build_ui import build_ui
except ModuleNotFoundError:
    build_ui = None


class custom_build_py(build_py):
    def run(self):
        self.run_command('build_ui')
        super().run()


def version_scheme(version):
    import setuptools_scm.version
    if version.exact:
        return setuptools_scm.version.guess_next_simple_semver(
            version.tag, retain=setuptools_scm.version.SEMVER_LEN, increment=False
        )
    else:
        if version.branch != "stable":
            return version.format_next_version(
                setuptools_scm.version.guess_next_simple_semver, retain=setuptools_scm.version.SEMVER_MINOR
            )
        else:
            return version.format_next_version(
                setuptools_scm.version.guess_next_simple_semver, retain=setuptools_scm.version.SEMVER_PATCH
            )


setup(
    use_scm_version={
        "version_scheme": version_scheme,
        "local_scheme": "no-local-version",
        "write_to": "randovania/version.py",
    },
    cmdclass={
        "build_ui": build_ui,
        "build_py": custom_build_py
    },
)
