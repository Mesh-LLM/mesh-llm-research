import sys, runpy
parent = sys.argv.pop(1)
sys.path.insert(0, parent + '/helper_code')
sys.argv[0] = parent + '/helper_code/generate_sweagent_instances.py'
runpy.run_path(sys.argv[0], run_name='__main__')
