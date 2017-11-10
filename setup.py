from distutils.core import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext, Extension


ext_modules = [
    Extension("modules.Computation", ["modules/Computation.py"]),
    Extension("modules.Conditions", ["modules/Conditions.py"]),
    Extension("modules.Elements", ["modules/Elements.py"]),
    Extension("modules.Material", ["modules/Material.py"]),
    Extension("modules.Plotter", ["modules/Plotter.py"])]


setup(
    name="modules",
    version='0.1',
    author='Ewen BRUN; Pierre HAON',
    author_email='ewen.brun@ecam.fr',
    packages=["modules"],
    description='Finite Elements Method implementation',
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
)
