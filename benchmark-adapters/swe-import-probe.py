import sys, json, runpy, types, sweagent, swerex
import swerex.deployment.modal, swerex.runtime.remote
parent = sys.argv[1]
helper = types.ModuleType('helper_code')
helper.__path__ = [parent + '/helper_code']
sys.modules['helper_code'] = helper
sys.path.insert(0, parent + '/helper_code')
for path in ['helper_code/generate_sweagent_instances.py','helper_code/gather_patches.py','swe_bench_pro_eval.py']:
    runpy.run_path(parent + '/' + path, run_name='_swe_sdk_import_only')
print(json.dumps({'sweagent_version': sweagent.__version__, 'swerex_version': swerex.__version__, 'modules': {'sweagent': sweagent.__file__, 'swerex': swerex.__file__}}))
