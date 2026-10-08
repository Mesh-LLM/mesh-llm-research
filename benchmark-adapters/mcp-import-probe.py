import sys, json, runpy, mcp_completion, mcp_completion.main
runpy.run_path(sys.argv[1], run_name='_mcp_import_only')
runpy.run_path(sys.argv[2], run_name='_mcp_import_only')
names = ['mcp_completion','mcp_completion.main','pandas','numpy','aiohttp','aiofiles','aiocsv','requests','dotenv','datasets','litellm','tenacity','tqdm','matplotlib','nest_asyncio','uvicorn','fastapi','pydantic','httpx']
print(json.dumps({n: sys.modules[n].__file__ for n in names}))
