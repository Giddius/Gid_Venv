

LOAD_ENV_SNIPPET = """
@echo off

rem ----------------------------------------------------------------
rem ##################### setting vars from $!$DEV_META_ENV_FILE_PATH$!$
for /f %%i in ($!$DEV_META_ENV_FILE_PATH$!$) do set %%i
rem ----------------------------------------------------------------

"""
