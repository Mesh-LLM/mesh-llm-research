import sys, runpy, types
parent = sys.argv.pop(1)
helper = types.ModuleType('helper_code')
helper.__path__ = [parent + '/helper_code']
sys.modules['helper_code'] = helper
sys.argv[0] = parent + '/swe_bench_pro_eval.py'
runpy.run_path(sys.argv[0], run_name='__main__')
