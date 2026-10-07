python := env_var_or_default('MESH_RESEARCH_PYTHON', 'python3.12')

offline-checks:
    {{python}} -I -B -m unittest discover -s tests -v
