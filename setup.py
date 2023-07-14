from distutils.core import setup
import VNCGrubber

setup(name="VNCGrubber",
      version=VNCGrubber.__version__,
      author="MrNom4ik",
      url="https://github.com/MrNom4ik/VNCGrubber",
      install_requires=["pydantic", "asyncvnc", "aiohttp"])

