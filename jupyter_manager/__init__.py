from pathlib import Path
from string import Template


__prog__ = 'jupyter_manager'
__version__ = '1.0'
__author__ = 'George Young'
__maintainer__ = 'George Young'
__email__ = 'bioinformatics@lms.mrc.ac.uk'
__status__ = 'Production'
__license__ = 'MIT'

SESSION_STORE = Path.home() / '.jupyter_manager'
SESSION_STORE.mkdir(exist_ok=True)

SINGULARITY_STORE = Path('/opt/software/apps/singularity/jupyter')
SINGULARITY_IMAGE = Template(str(SINGULARITY_STORE / 'minimal-notebook_python-$vers.sif'))

R_VERSIONS = \
    sorted(
        sif.stem.removeprefix('minimal-notebook_python-')
        for sif in SINGULARITY_STORE.glob('*.sif')
    )