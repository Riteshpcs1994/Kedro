from pathlib import Path
from kedro.config import OmegaConfigLoader
from kedro.framework.hooks import hook_impl
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Config loader setup
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONF_SOURCE = str(PROJECT_ROOT / "conf")

CONFIG_LOADER_CLASS = OmegaConfigLoader
CONFIG_LOADER_ARGS = {
    "conf_source": CONF_SOURCE,
    "env": "base",
    "runtime_params": None,
}

class MergeParamsHook:
    @hook_impl
    def before_pipeline_run(self, run_params: Dict[str, Any], pipeline, catalog):
        """Merge all configuration parameters, excluding specified patterns."""
        try:
            conf_loader = OmegaConfigLoader(
                conf_source=CONF_SOURCE,
                env="base",
                runtime_params=run_params.get("runtime_params", {})
            )
            
            all_conf = conf_loader["**"]
            merged = {}
            excluded_patterns = {"spark"}  # Add more patterns as needed
            
            for key, value in all_conf.items():
                if key in excluded_patterns:
                    continue
                if isinstance(value, dict):
                    merged.update(value)
                else:
                    merged[key] = value
            
            # Merge with existing parameters (new values take precedence)
            existing_params = run_params.get("parameters", {})
            run_params["parameters"] = {**merged, **existing_params}
            
            logger.debug(f"Merged {len(merged)} configuration parameters")
            
        except Exception as e:
            logger.error(f"Parameter merging failed: {e}")
            # Ensure parameters key exists even if merging fails
            if "parameters" not in run_params:
                run_params["parameters"] = {}

# Register hook
HOOKS = (MergeParamsHook(),)